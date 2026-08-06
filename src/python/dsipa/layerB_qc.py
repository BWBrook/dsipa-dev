"""Layer B QC hardening: licensing, scope, and exposure diagnostics (WP0.15b)."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from shapely import wkb
from shapely.geometry import Point

from dsipa.git_state import ensure_clean_before_mutation, ensure_only_expected_changes
from dsipa.layerB_data import (
    DEFAULT_UNCERTAINTY_M,
    DEFAULT_YEARS,
    build_queries,
    find_latest_zip,
    normalize_columns,
)
from dsipa.manifest import build_manifest, write_manifest
from dsipa.nightlights import CORE_YEARS, download_year
from dsipa.paths import find_repo_root
from dsipa.schema import LAYERB_ALA_LICENSE_LEDGER_CSV, LAYERB_OCCURRENCE_SUMMARY_CSV, SCHEMA_VERSION


PA_UNION_CACHE = f"data/processed/cache/pa_union_v{SCHEMA_VERSION.replace('.', '_')}.wkb"
LAND_UNION_CACHE = "data/processed/cache/land_union_ne_110m.wkb"


@dataclass
class GroupConfig:
    key: str
    label: str
    raw_zip: Path | None
    processed_path: Path


@dataclass
class ExposureAccumulator:
    total: int = 0
    missing: int = 0
    values: list[np.ndarray] = None

    def __post_init__(self) -> None:
        if self.values is None:
            self.values = []

    def add(self, values: np.ndarray) -> None:
        self.total += len(values)
        valid = np.isfinite(values)
        self.missing += int((~valid).sum())
        if valid.any():
            self.values.append(values[valid])

    def summarize(self) -> dict[str, float]:
        if not self.values:
            return {
                "total": self.total,
                "missing": self.missing,
                "missing_fraction": np.nan,
                "zero_fraction": np.nan,
                "p50": np.nan,
                "p90": np.nan,
                "p95": np.nan,
                "p99": np.nan,
            }
        values = np.concatenate(self.values)
        missing_fraction = self.missing / self.total if self.total else np.nan
        zero_fraction = (values == 0).mean() if values.size else np.nan
        quantiles = np.quantile(values, [0.5, 0.9, 0.95, 0.99]) if values.size else [np.nan] * 4
        return {
            "total": self.total,
            "missing": self.missing,
            "missing_fraction": missing_fraction,
            "zero_fraction": zero_fraction,
            "p50": float(quantiles[0]),
            "p90": float(quantiles[1]),
            "p95": float(quantiles[2]),
            "p99": float(quantiles[3]),
        }


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _load_union(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing cached union geometry: {path}")
    return wkb.loads(path.read_bytes())


def _vectorized_contains(geom, xs: np.ndarray, ys: np.ndarray, points=None) -> np.ndarray:
    try:
        import shapely

        pts = points if points is not None else shapely.points(xs, ys)
        return shapely.contains(geom, pts)
    except Exception:
        from shapely.prepared import prep

        prepared = prep(geom)
        return np.array([prepared.contains(Point(x, y)) for x, y in zip(xs, ys)])


def _load_citation_table(zip_path: Path) -> pd.DataFrame:
    import zipfile

    with zipfile.ZipFile(zip_path) as zf:
        if "citation.csv" not in zf.namelist():
            raise RuntimeError(f"citation.csv missing in {zip_path}")
        with zf.open("citation.csv") as handle:
            citation = pd.read_csv(handle, dtype=str)

    citation = citation.rename(columns={c: c.strip().lower() for c in citation.columns})
    rename = {
        "uid": "data_resource_uid",
        "name": "provider_name",
        "doi": "doi",
        "citation": "citation",
        "rights": "rights",
        "more information": "more_information",
        "number of records in download": "download_records",
    }
    citation = citation.rename(columns=rename)
    for col in rename.values():
        if col not in citation.columns:
            citation[col] = pd.NA
    return citation[list(rename.values())]


def _iter_occurrence_chunks(path: Path, chunksize: int = 200_000) -> Iterable[pd.DataFrame]:
    reader = pd.read_csv(path, dtype=str, compression="gzip", chunksize=chunksize)
    for chunk in reader:
        yield normalize_columns(chunk)


def _prepare_groups(
    *,
    root: Path,
    raw_dir: Path,
    processed_dir: Path,
    group_keys: set[str],
) -> list[GroupConfig]:
    queries = build_queries(*DEFAULT_YEARS, DEFAULT_UNCERTAINTY_M)
    groups = []
    for query in queries:
        if query.key not in group_keys:
            continue
        raw_zip = find_latest_zip(raw_dir, query.key)
        processed_path = (
            processed_dir / f"{query.key}_occurrences_filtered_v{SCHEMA_VERSION.replace('.', '_')}.csv.gz"
        )
        if not processed_path.exists():
            raise FileNotFoundError(f"Missing processed occurrences: {processed_path}")
        groups.append(
            GroupConfig(
                key=query.key,
                label=query.label,
                raw_zip=raw_zip,
                processed_path=processed_path,
            )
        )
    if not groups:
        raise SystemExit("No groups selected; check --groups.")
    return groups


def build_license_ledger(groups: list[GroupConfig]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for group in groups:
        if group.raw_zip is None:
            continue
        citation = _load_citation_table(group.raw_zip)
        counts = Counter()
        total = 0
        for chunk in _iter_occurrence_chunks(group.processed_path):
            if "dataResourceUid" not in chunk.columns:
                continue
            values = chunk["dataResourceUid"].fillna("unknown").astype(str)
            counts.update(values)
            total += len(values)

        for uid, count in counts.items():
            entry = citation[citation["data_resource_uid"] == uid]
            row = {
                "schema_version": SCHEMA_VERSION,
                "group": group.key,
                "label": group.label,
                "data_resource_uid": uid,
                "processed_records": int(count),
                "processed_share": float(count / total) if total else np.nan,
            }
            if not entry.empty:
                rec = entry.iloc[0].to_dict()
                row.update(rec)
                try:
                    row["download_records"] = int(float(row.get("download_records", 0) or 0))
                except (TypeError, ValueError):
                    row["download_records"] = pd.NA
            rows.append(row)

    ledger = pd.DataFrame(rows)
    if not ledger.empty:
        ledger = ledger.sort_values(["group", "processed_records"], ascending=[True, False])
    return ledger


def write_license_report(ledger: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Layer B ALA license ledger",
        "",
        f"Generated: {_now_utc()}",
        "",
    ]
    if ledger.empty:
        lines.append("No license ledger rows available.")
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return

    for group, group_df in ledger.groupby("group"):
        lines.append(f"## {group}")
        lines.append("")
        rights_summary = (
            group_df.groupby(group_df["rights"].fillna("(missing)"))["processed_records"]
            .sum()
            .sort_values(ascending=False)
        )
        lines.append("Rights summary (processed records):")
        lines.append("")
        for rights, count in rights_summary.items():
            share = count / group_df["processed_records"].sum()
            lines.append(f"- {rights}: {int(count)} ({share:.1%})")
        lines.append("")

        top = group_df.head(10)[
            [
                "data_resource_uid",
                "provider_name",
                "rights",
                "processed_records",
                "processed_share",
            ]
        ]
        lines.append("Top providers (processed):")
        lines.append("")
        lines.append(top.to_string(index=False))
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def build_extended_qc(
    groups: list[GroupConfig],
    pa_union,
    land_union,
    buffer_km: float,
) -> dict[str, dict[str, object]]:
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
    pa_buffer = pa_union.buffer(buffer_km * 1000.0)

    results: dict[str, dict[str, object]] = {}
    for group in groups:
        provider_counts: Counter[str] = Counter()
        cell_counts: Counter[tuple[int, int]] = Counter()
        uncertainty_values: list[float] = []
        total = 0
        sign_error = 0
        bbox_outlier = 0
        offshore = 0
        inside_count = 0
        within_count = 0

        for chunk in _iter_occurrence_chunks(group.processed_path):
            total += len(chunk)
            lat = pd.to_numeric(chunk["decimalLatitude"], errors="coerce")
            lon = pd.to_numeric(chunk["decimalLongitude"], errors="coerce")
            unc = pd.to_numeric(chunk["coordinateUncertaintyInMeters"], errors="coerce")

            uncertainty_values.extend(unc.dropna().tolist())

            sign_error += int(((lat > 0) | (lon < 0)).sum())
            bbox_outlier += int(((lat < -55) | (lat > 0) | (lon < 90) | (lon > 180)).sum())

            x, y = transformer.transform(lon.to_numpy(), lat.to_numpy())
            try:
                import shapely

                points = shapely.points(x, y)
            except Exception:
                points = None
            inside = _vectorized_contains(pa_union, x, y, points=points)
            within = _vectorized_contains(pa_buffer, x, y, points=points)
            on_land = _vectorized_contains(land_union, x, y, points=points)

            offshore += int((~on_land).sum())
            inside_count += int(inside.sum())
            within_count += int((within & ~inside).sum())

            if "dataResourceUid" in chunk.columns:
                provider_counts.update(chunk["dataResourceUid"].fillna("unknown").astype(str))

            grid_x = np.floor(x / 1000.0).astype(int)
            grid_y = np.floor(y / 1000.0).astype(int)
            for gx, gy in zip(grid_x, grid_y):
                cell_counts[(int(gx), int(gy))] += 1

        uncertainty_arr = np.array(uncertainty_values) if uncertainty_values else np.array([])
        quantiles = np.quantile(uncertainty_arr, [0.5, 0.9, 0.95, 0.99]) if uncertainty_arr.size else [np.nan] * 4

        provider_total = sum(provider_counts.values()) or 0
        provider_top = provider_counts.most_common(10)
        provider_top_share = sum(count for _, count in provider_top) / provider_total if provider_total else np.nan

        cell_total = sum(cell_counts.values()) or 0
        top_cells = sorted(cell_counts.values(), reverse=True)[:100]
        top_cells_share = sum(top_cells) / cell_total if cell_total else np.nan

        results[group.key] = {
            "label": group.label,
            "total_records": total,
            "sign_error_fraction": sign_error / total if total else np.nan,
            "bbox_outlier_fraction": bbox_outlier / total if total else np.nan,
            "offshore_fraction": offshore / total if total else np.nan,
            "uncertainty_p50": float(quantiles[0]),
            "uncertainty_p90": float(quantiles[1]),
            "uncertainty_p95": float(quantiles[2]),
            "uncertainty_p99": float(quantiles[3]),
            "provider_top10_share": provider_top_share,
            "provider_top10": provider_top,
            "top100_cell_share": top_cells_share,
            "inside_count": inside_count,
            "within_10km_count": within_count,
            "outside_count": total - inside_count - within_count,
            "provider_counts": provider_counts,
        }
    return results


def write_extended_qc_report(
    summary_rows: pd.DataFrame,
    qc_results: dict[str, dict[str, object]],
    out_path: Path,
    simplify_m: float | None = None,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Layer B extended QC",
        "",
        f"Generated: {_now_utc()}",
    ]
    if simplify_m and simplify_m > 0:
        lines.append(f"Geometry simplification: {simplify_m:.0f} m")
    lines.append("")

    if summary_rows is not None and not summary_rows.empty:
        lines.append("## Stage counts + dedup loss")
        lines.append("")
        summary_rows = summary_rows.copy()
        summary_rows["dedup_loss_fraction"] = (
            (summary_rows["filtered_records"] - summary_rows["dedup_records"])
            / summary_rows["filtered_records"]
        )
        lines.append(
            summary_rows[
                ["group", "raw_records", "filtered_records", "dedup_records", "dedup_loss_fraction"]
            ].to_string(index=False)
        )
        lines.append("")

    for group, qc in qc_results.items():
        lines.append(f"## {group}")
        lines.append("")
        lines.append(
            "Coordinate checks (fractions): "
            f"sign_error={qc['sign_error_fraction']:.3f}, "
            f"bbox_outlier={qc['bbox_outlier_fraction']:.3f}, "
            f"offshore={qc['offshore_fraction']:.3f}"
        )
        lines.append(
            "Coordinate uncertainty quantiles (m): "
            f"p50={qc['uncertainty_p50']:.1f}, "
            f"p90={qc['uncertainty_p90']:.1f}, "
            f"p95={qc['uncertainty_p95']:.1f}, "
            f"p99={qc['uncertainty_p99']:.1f}"
        )
        lines.append(
            f"Spatial clustering: top100 1km cells share={qc['top100_cell_share']:.3f}"
        )
        lines.append(
            f"Provider concentration: top10 share={qc['provider_top10_share']:.3f}"
        )
        lines.append("")

        lines.append("Top providers (processed):")
        lines.append("")
        if qc["provider_top10"]:
            top_df = pd.DataFrame(
                qc["provider_top10"], columns=["dataResourceUid", "records"]
            )
            top_df["share"] = top_df["records"] / qc["total_records"]
            lines.append(top_df.to_string(index=False))
        else:
            lines.append("No provider counts available.")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_scope_report(
    qc_results: dict[str, dict[str, object]],
    out_path: Path,
    simplify_m: float | None = None,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Layer B scope coverage",
        "",
        f"Generated: {_now_utc()}",
    ]
    if simplify_m and simplify_m > 0:
        lines.append(f"Geometry simplification: {simplify_m:.0f} m")
    lines.append("")
    for group, qc in qc_results.items():
        total = qc["total_records"]
        inside = qc["inside_count"]
        within = qc["within_10km_count"]
        outside = qc["outside_count"]
        scope_count = inside + within
        lines.append(f"## {group}")
        lines.append("")
        lines.append(
            f"Inside PAs: {inside} ({inside / total:.1%})"
            if total
            else "Inside PAs: NA"
        )
        lines.append(
            f"Within 10 km: {within} ({within / total:.1%})"
            if total
            else "Within 10 km: NA"
        )
        lines.append(
            f"Outside 10 km: {outside} ({outside / total:.1%})"
            if total
            else "Outside 10 km: NA"
        )
        lines.append(
            f"Retained if scope enforced (inside + within 10 km): {scope_count} ({scope_count / total:.1%})"
            if total
            else "Retained if scope enforced: NA"
        )
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def _sample_raster(dataset, lons: np.ndarray, lats: np.ndarray) -> np.ndarray:
    coords = list(zip(lons, lats))
    values = np.array([val[0] for val in dataset.sample(coords)], dtype=float)
    scale = dataset.scales[0] if dataset.scales else None
    offset = dataset.offsets[0] if dataset.offsets else None
    scale_value = 1.0 if scale is None else float(scale)
    offset_value = 0.0 if offset is None else float(offset)
    values = values * scale_value + offset_value
    nodata = dataset.nodata
    if nodata is not None:
        values = np.where(values == nodata, np.nan, values)
    return values


def build_exposure_qc(
    groups: list[GroupConfig],
    pa_union,
    buffer_km: float,
    nightlights_dir: Path,
) -> dict[str, dict[str, dict[str, float]]]:
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
    pa_buffer = pa_union.buffer(buffer_km * 1000.0)
    raster_cache: dict[int, rasterio.DatasetReader] = {}
    results: dict[str, dict[str, ExposureAccumulator]] = defaultdict(
        lambda: {
            "inside": ExposureAccumulator(),
            "within_10km": ExposureAccumulator(),
            "outside": ExposureAccumulator(),
        }
    )

    for group in groups:
        for chunk in _iter_occurrence_chunks(group.processed_path):
            years = pd.to_numeric(chunk["year"], errors="coerce").astype("Int64")
            valid_year_mask = years.notna() & years.isin(list(CORE_YEARS))
            if not valid_year_mask.any():
                continue
            chunk = chunk.loc[valid_year_mask].copy()
            years = years.loc[valid_year_mask].astype(int).to_numpy()
            lons = pd.to_numeric(chunk["decimalLongitude"], errors="coerce").to_numpy()
            lats = pd.to_numeric(chunk["decimalLatitude"], errors="coerce").to_numpy()
            x, y = transformer.transform(lons, lats)
            try:
                import shapely

                points = shapely.points(x, y)
            except Exception:
                points = None
            inside = _vectorized_contains(pa_union, x, y, points=points)
            within = _vectorized_contains(pa_buffer, x, y, points=points)
            within = within & ~inside

            for year in np.unique(years):
                idx = years == year
                if not idx.any():
                    continue
                if year not in raster_cache:
                    raster = download_year(year, nightlights_dir)
                    raster_cache[year] = rasterio.open(raster.path)
                dataset = raster_cache[year]
                values = _sample_raster(dataset, lons[idx], lats[idx])

                results[group.key]["inside"].add(values[inside[idx]])
                results[group.key]["within_10km"].add(values[within[idx]])
                results[group.key]["outside"].add(values[(~inside[idx]) & (~within[idx])])

    for dataset in raster_cache.values():
        dataset.close()

    summarized: dict[str, dict[str, dict[str, float]]] = {}
    for group, strata in results.items():
        summarized[group] = {name: acc.summarize() for name, acc in strata.items()}
    return summarized


def write_exposure_report(
    exposure: dict[str, dict[str, dict[str, float]]],
    out_path: Path,
    simplify_m: float | None = None,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Layer B exposure QC (ALAN at occurrence locations)",
        "",
        f"Generated: {_now_utc()}",
    ]
    if simplify_m and simplify_m > 0:
        lines.append(f"Geometry simplification: {simplify_m:.0f} m")
    lines.append("")
    for group, strata in exposure.items():
        lines.append(f"## {group}")
        lines.append("")
        table = []
        for stratum, stats in strata.items():
            table.append(
                {
                    "stratum": stratum,
                    "total": stats["total"],
                    "missing_fraction": stats["missing_fraction"],
                    "zero_fraction": stats["zero_fraction"],
                    "p50": stats["p50"],
                    "p90": stats["p90"],
                    "p95": stats["p95"],
                    "p99": stats["p99"],
                }
            )
        df = pd.DataFrame(table)
        lines.append(df.to_string(index=False))
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Layer B QC hardening (WP0.15b).")
    parser.add_argument(
        "--groups",
        default="microbats,diurnal_birds",
        help="Comma-separated group keys to process.",
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw/ala_occurrences",
        help="Directory for raw ALA downloads.",
    )
    parser.add_argument(
        "--processed-dir",
        default="data/processed/layerB",
        help="Directory for processed occurrence tables.",
    )
    parser.add_argument("--buffer-km", type=float, default=10.0)
    parser.add_argument(
        "--nightlights-dir",
        default="data/raw/nightlights_zenodo_v0_4",
        help="Directory for nightlights rasters (downloaded if missing).",
    )
    parser.add_argument(
        "--skip-exposure",
        action="store_true",
        help="Skip exposure QC (ALAN sampling).",
    )
    parser.add_argument(
        "--skip-qc",
        action="store_true",
        help="Skip extended QC + scope reports (useful when rerunning exposure only).",
    )
    parser.add_argument(
        "--skip-ledger",
        action="store_true",
        help="Skip license ledger generation (useful when rerunning exposure only).",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow artefact generation with a dirty git tree.",
    )
    parser.add_argument(
        "--simplify-m",
        type=float,
        default=1000.0,
        help="Simplify union geometries (meters) to speed QC.",
    )
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    parser.add_argument(
        "--artefact-only",
        action="store_true",
        help="Only (re)write artefact/manifest from existing outputs.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    ledger_path = root / LAYERB_ALA_LICENSE_LEDGER_CSV
    license_report_path = root / "analysis" / "reports" / "layerB_ala_license_ledger.md"
    qc_report_path = root / "analysis" / "reports" / "layerB_qc_extended.md"
    scope_report_path = root / "analysis" / "reports" / "layerB_scope_coverage.md"
    exposure_report_path = root / "analysis" / "reports" / "layerB_exposure_qc.md"
    exposure_json_path = root / "analysis" / "reports" / "layerB_exposure_qc.json"
    upstream_outputs = [
        root / LAYERB_OCCURRENCE_SUMMARY_CSV,
        root / "analysis" / "reports" / "layerB_data_qc.md",
    ]
    expected_outputs = [
        ledger_path,
        license_report_path,
        qc_report_path,
        scope_report_path,
        exposure_report_path,
        exposure_json_path,
    ]
    expected_dirty_paths = upstream_outputs + expected_outputs

    if args.artefact_only:
        if not args.skip_artefact:
            ensure_only_expected_changes(
                root,
                expected_paths=expected_dirty_paths,
                allow_dirty=args.allow_dirty,
                context="Layer B QC artefact-only",
            )
            artefact_dir = root / "artefacts" / "wp0_15b_layerB_qc"
            artefact_dir.mkdir(parents=True, exist_ok=True)
            artefact_paths = []
            for path in (
                ledger_path,
                license_report_path,
                qc_report_path,
                scope_report_path,
                exposure_report_path,
                exposure_json_path,
            ):
                if path.exists():
                    artefact_paths.append(path)
                    shutil.copyfile(path, artefact_dir / path.name)
            manifest = build_manifest(
                run_id="wp0_15b_layerB_qc",
                wp="WP0.15b",
                root=root,
                outputs=[path.name for path in artefact_paths],
                inputs=["Atlas of Living Australia", "CAPAD 2024", "Zenodo nightlights v0.4"],
                require_clean=True,
                expected_dirty_paths=expected_dirty_paths,
                notes="WP0.15b Layer B licensing ledger + extended QC + exposure/scope diagnostics",
            )
            write_manifest(artefact_dir / "MANIFEST.json", manifest)
            (artefact_dir / "README.txt").write_text(
                "WP0.15b Layer B QC hardening artefact.\n", encoding="utf-8"
            )
        return 0
    ensure_clean_before_mutation(
        root,
        allow_dirty=args.allow_dirty,
        context="Layer B QC",
    )
    raw_dir = root / args.raw_dir
    processed_dir = root / args.processed_dir
    nightlights_dir = root / args.nightlights_dir

    group_keys = {key.strip() for key in args.groups.split(",") if key.strip()}
    groups = _prepare_groups(
        root=root,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        group_keys=group_keys,
    )

    pa_union = _load_union(root / PA_UNION_CACHE)
    land_union = _load_union(root / LAND_UNION_CACHE)
    if args.simplify_m and args.simplify_m > 0:
        pa_union = pa_union.simplify(args.simplify_m, preserve_topology=True)
        land_union = land_union.simplify(args.simplify_m, preserve_topology=True)

    if not args.skip_ledger:
        ledger = build_license_ledger(groups)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger.to_csv(ledger_path, index=False)
        write_license_report(ledger, license_report_path)

    summary_path = root / LAYERB_OCCURRENCE_SUMMARY_CSV
    summary_rows = None
    if summary_path.exists():
        summary_rows = pd.read_csv(summary_path)

    qc_results = None
    if not args.skip_qc:
        qc_results = build_extended_qc(groups, pa_union, land_union, args.buffer_km)
        write_extended_qc_report(summary_rows, qc_results, qc_report_path, simplify_m=args.simplify_m)
        write_scope_report(qc_results, scope_report_path, simplify_m=args.simplify_m)

    exposure_summary = None
    if not args.skip_exposure:
        exposure_summary = build_exposure_qc(groups, pa_union, args.buffer_km, nightlights_dir)
        write_exposure_report(exposure_summary, exposure_report_path, simplify_m=args.simplify_m)
        exposure_json_path.write_text(
            json.dumps(exposure_summary, indent=2),
            encoding="utf-8",
        )

    if not args.skip_artefact:
        ensure_only_expected_changes(
            root,
            expected_paths=expected_dirty_paths,
            allow_dirty=args.allow_dirty,
            context="Layer B QC",
        )
        artefact_dir = root / "artefacts" / "wp0_15b_layerB_qc"
        artefact_dir.mkdir(parents=True, exist_ok=True)
        artefact_paths = []
        if ledger_path.exists():
            artefact_paths.append(ledger_path)
        if license_report_path.exists():
            artefact_paths.append(license_report_path)
        if qc_report_path.exists():
            artefact_paths.append(qc_report_path)
        if scope_report_path.exists():
            artefact_paths.append(scope_report_path)
        for path in artefact_paths:
            (artefact_dir / path.name).write_text(path.read_text(encoding="utf-8"))
        if exposure_report_path.exists():
            shutil.copyfile(exposure_report_path, artefact_dir / exposure_report_path.name)
        if exposure_json_path.exists():
            shutil.copyfile(exposure_json_path, artefact_dir / exposure_json_path.name)

        manifest = build_manifest(
            run_id="wp0_15b_layerB_qc",
            wp="WP0.15b",
            root=root,
            outputs=[path.name for path in artefact_paths]
            + ([exposure_report_path.name] if exposure_report_path.exists() else [])
            + ([exposure_json_path.name] if exposure_json_path.exists() else []),
            inputs=["Atlas of Living Australia", "CAPAD 2024", "Zenodo nightlights v0.4"],
            require_clean=True,
            expected_dirty_paths=expected_dirty_paths,
            notes="WP0.15b Layer B licensing ledger + extended QC + exposure/scope diagnostics",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)
        (artefact_dir / "README.txt").write_text(
            "WP0.15b Layer B QC hardening artefact.\n", encoding="utf-8"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

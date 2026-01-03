"""Distance-to-edge ring profiles for smoke-test triad (WP0.7)."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask

from dsipa.manifest import build_manifest, write_manifest
from dsipa.nightlights import download_year
from dsipa.paths import find_repo_root
from dsipa.schema import EDGE_PROFILES_SMOKETEST_CSV, SCHEMA_VERSION, TRIAD_GEOMS_GPKG
from dsipa.triad import RING_BINS_KM, build_rings
SMOKETEST_YEARS = [2013, 2018, 2024]

TRIAD_GEOMS = TRIAD_GEOMS_GPKG
OUTPUT_TABLE = EDGE_PROFILES_SMOKETEST_CSV
REPORT_PATH = "analysis/reports/smoketest_edge_profiles.md"
PLOT_PATH = "analysis/reports/smoketest_edge_profiles.png"


@dataclass(frozen=True)
class RasterMeta:
    year: int
    path: Path
    nodata: float | None
    dtype: str
    scale: float | None
    offset: float | None


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _load_triads(path: Path, target_crs: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.empty:
        raise RuntimeError(f"No features found in {path}")
    return gdf.to_crs(target_crs)


def _stats_for_geom(
    dataset: rasterio.DatasetReader,
    geom,
    *,
    scale: float | None,
    offset: float | None,
) -> dict[str, float]:
    if geom is None or geom.is_empty:
        return {
            "pixel_count": 0,
            "valid_pixel_count": 0,
            "valid_fraction": 0.0,
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
        }

    nodata = dataset.nodata
    data, _ = mask(dataset, [geom], crop=True, filled=True, nodata=nodata)
    band = data[0]

    mask_invalid = np.isnan(band)
    if nodata is not None:
        mask_invalid |= band == nodata
    mask_invalid |= band < 0

    pixel_count = int(band.size)
    valid = band[~mask_invalid].astype("float64")
    scale_value = 1.0 if scale is None else float(scale)
    offset_value = 0.0 if offset is None else float(offset)
    valid = valid * scale_value + offset_value
    valid_count = int(valid.size)

    if valid_count == 0:
        return {
            "pixel_count": pixel_count,
            "valid_pixel_count": valid_count,
            "valid_fraction": 0.0,
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
            "frac_gt0": np.nan,
            "p95": np.nan,
        }

    return {
        "pixel_count": pixel_count,
        "valid_pixel_count": valid_count,
        "valid_fraction": float(valid_count / pixel_count),
        "mean": float(np.mean(valid)),
        "median": float(np.median(valid)),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
        "std": float(np.std(valid)),
        "frac_gt0": float(np.mean(valid > 0)),
        "p95": float(np.quantile(valid, 0.95)),
    }


def _raster_meta(dataset: rasterio.DatasetReader, year: int, path: Path) -> RasterMeta:
    scale = dataset.scales[0] if dataset.scales else None
    offset = dataset.offsets[0] if dataset.offsets else None
    return RasterMeta(
        year=year,
        path=path,
        nodata=dataset.nodata,
        dtype=str(dataset.dtypes[0]),
        scale=scale,
        offset=offset,
    )


def summarise_year(
    year: int,
    triads: gpd.GeoDataFrame,
    raster_path: Path,
) -> tuple[list[dict], RasterMeta]:
    records: list[dict] = []
    with rasterio.open(raster_path) as dataset:
        rings_metric = build_rings(triads, RING_BINS_KM)
        rings = rings_metric.to_crs(dataset.crs)
        meta = _raster_meta(dataset, year, raster_path)

        for _, row in rings.iterrows():
            stats = _stats_for_geom(dataset, row.geometry, scale=meta.scale, offset=meta.offset)
            records.append(
                {
                    "schema_version": SCHEMA_VERSION,
                    "pa_id": row["pa_id"],
                    "triad_role": row["triad_role"],
                    "year": year,
                    "ring_index": int(row["ring_index"]),
                    "ring_inner_km": float(row["ring_inner_km"]),
                    "ring_outer_km": float(row["ring_outer_km"]),
                    "scale_metadata": meta.scale,
                    "offset_metadata": meta.offset,
                    **stats,
                }
            )

    return records, meta


def write_outputs(df: pd.DataFrame, root: Path) -> Path:
    out_path = root / OUTPUT_TABLE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path


def write_plot(df: pd.DataFrame, plot_path: Path) -> None:
    import matplotlib.pyplot as plt

    plot_path.parent.mkdir(parents=True, exist_ok=True)

    pa_ids = df["pa_id"].unique().tolist()
    fig, axes = plt.subplots(1, len(pa_ids), figsize=(12, 4), sharey=True)
    if len(pa_ids) == 1:
        axes = [axes]

    for ax, pa_id in zip(axes, pa_ids):
        subset = df[df["pa_id"] == pa_id]
        for year in SMOKETEST_YEARS:
            year_df = subset[subset["year"] == year].sort_values("ring_index")
            midpoints = (year_df["ring_inner_km"] + year_df["ring_outer_km"]) / 2
            ax.plot(midpoints, year_df["mean"], marker="o", label=str(year))
        role = subset["triad_role"].iloc[0]
        ax.set_title(f"{pa_id} ({role})")
        ax.set_xlabel("Distance from boundary (km)")

    axes[0].set_ylabel("Mean night-light value (scaled units)")
    axes[-1].legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.tight_layout()
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)


def write_report(df: pd.DataFrame, meta: Iterable[RasterMeta], report_path: Path, plot_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    meta_lines = [
        f"- {item.year}: dtype={item.dtype}, nodata={item.nodata}, scale={item.scale}, offset={item.offset}"
        for item in meta
    ]

    low_pixels = df[df["valid_pixel_count"] < 10]
    empty_rings = (
        df.groupby("ring_index")["valid_pixel_count"].sum().reset_index()
    )
    empty_rings = empty_rings[empty_rings["valid_pixel_count"] == 0]["ring_index"].tolist()

    lines = [
        "# Smoke-test edge profile report",
        "",
        f"Generated: {_now_utc()}",
        "",
        "## Raster metadata (per year)",
        *meta_lines,
        "",
        "Note: Statistics computed on scaled values (scale/offset metadata applied).",
        "",
        "## Summary by ring",
        "",
        df.groupby(["year", "ring_index"])[["mean", "median", "valid_pixel_count"]]
        .describe()
        .round(3)
        .to_string(),
        "",
        "## Low pixel-count warnings (<10)",
        "",
    ]

    if low_pixels.empty:
        lines.append("None")
    else:
        lines.append(
            low_pixels[[
                "pa_id",
                "triad_role",
                "year",
                "ring_index",
                "valid_pixel_count",
            ]].to_string(index=False)
        )

    if empty_rings:
        lines.extend(
            [
                "",
                f"Note: rings with zero valid pixels across all triad PAs: {empty_rings}.",
            ]
        )

    lines.extend(
        [
            "",
            f"Plot: {plot_path.name}",
        ]
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_artefact(report_path: Path, plot_path: Path, table_path: Path, root: Path) -> Path:
    artefact_dir = root / "artefacts" / "wp0_7_edge_profiles_smoketest"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(plot_path, artefact_dir / plot_path.name)
    shutil.copyfile(table_path, artefact_dir / table_path.name)

    manifest = build_manifest(
        run_id="wp0_7_edge_profiles_smoketest",
        wp="WP0.7",
        root=root,
        outputs=[report_path.name, plot_path.name, table_path.name],
        inputs=[TRIAD_GEOMS, "data/raw/nightlights_zenodo_v0_4"],
        notes="WP0.7 smoke-test edge profiles",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.7 smoke-test edge profile artefact. Contains profile table, report, and plot.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke-test edge profile summaries (WP0.7).")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    raw_dir = root / "data" / "raw" / "nightlights_zenodo_v0_4"
    raster_files = [download_year(year, raw_dir) for year in SMOKETEST_YEARS]

    triads = _load_triads(root / TRIAD_GEOMS, target_crs="EPSG:3577")

    all_records: list[dict] = []
    meta_records: list[RasterMeta] = []
    for file in raster_files:
        records, meta = summarise_year(file.year, triads, file.path)
        all_records.extend(records)
        meta_records.append(meta)

    df = pd.DataFrame(all_records)
    table_path = write_outputs(df, root)

    report_path = root / REPORT_PATH
    plot_path = root / PLOT_PATH
    write_plot(df, plot_path)
    write_report(df, meta_records, report_path, plot_path)

    if not args.skip_artefact:
        write_artefact(report_path, plot_path, table_path, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

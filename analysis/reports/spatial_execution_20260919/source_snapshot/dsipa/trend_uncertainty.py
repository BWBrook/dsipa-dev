"""Spatially aware bootstrap for Layer A trend uncertainty (WP0.19)."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from dsipa.ibra import IBRA_GPKG, process_ibra, write_outputs as write_ibra_outputs
from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import (
    PA_GEOMETRIES_CSV,
    PA_GEOMETRIES_GPKG,
    PA_IBRA_ASSIGNMENT_CSV,
    PA_IBRA_ASSIGNMENT_COLUMNS,
    PA_TREND_BOOTSTRAP_SUMMARY_CSV,
    PA_TREND_BOOTSTRAP_SUMMARY_COLUMNS,
    RADIANCE_BUFFERS_NATIONAL_CSV,
    SCHEMA_VERSION,
)
from dsipa.trends import MIN_VALID_PIXELS, MIN_VALID_YEARS

try:
    from shapely import make_valid
except ImportError:  # pragma: no cover
    from shapely.validation import make_valid  # type: ignore


REPORT_PATH = "analysis/reports/pa_trend_uncertainty.md"
DOMINANCE_CSV = "analysis/reports/pa_trend_dominance_matrix.csv"
FOREST_FIG = "manuscript/figures/fig_layerA_trend_uncertainty_forest.png"
DOMINANCE_FIG = "manuscript/figures/fig_layerA_trend_dominance.png"

TARGET_CRS = "EPSG:3577"
PRIMARY_METRIC = "mean"
PRIMARY_BUFFER_TYPE = "inside"


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _theil_sen(years: np.ndarray, values: np.ndarray) -> float:
    n = len(values)
    if n < 2:
        return np.nan
    slopes = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            if years[j] == years[i]:
                continue
            slopes.append((values[j] - values[i]) / (years[j] - years[i]))
    if not slopes:
        return np.nan
    return float(np.median(slopes))


def _resample_time(
    years: np.ndarray, values: np.ndarray, block_len: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    n = len(years)
    if n == 0:
        return years, values
    if block_len <= 1 or n <= block_len:
        idx = rng.integers(0, n, size=n)
        return years[idx], values[idx]

    n_blocks = int(np.ceil(n / block_len))
    starts = rng.integers(0, n - block_len + 1, size=n_blocks)
    idx = np.concatenate([np.arange(s, s + block_len) for s in starts])[:n]
    return years[idx], values[idx]


def _fix_geometry(geom):
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        geom = make_valid(geom)
    return geom


def _ensure_ibra_gpkg(root: Path) -> Path:
    path = root / IBRA_GPKG
    if path.exists():
        return path
    gdf = process_ibra(root)
    return write_ibra_outputs(gdf, root)


def assign_ibra(pa_gdf: gpd.GeoDataFrame, ibra_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    pa = pa_gdf[["pa_id", "geometry"]].copy()
    ibra = ibra_gdf[["REG_CODE_7", "REG_NAME_7", "geometry"]].copy()

    pa["geometry"] = pa["geometry"].apply(_fix_geometry)
    ibra["geometry"] = ibra["geometry"].apply(_fix_geometry)

    pa = pa.to_crs(TARGET_CRS)
    ibra = ibra.to_crs(TARGET_CRS)

    pa["pa_area_km2"] = pa.geometry.area / 1_000_000.0
    intersections = gpd.overlay(pa, ibra, how="intersection", keep_geom_type=True)
    if intersections.empty:
        raise RuntimeError("IBRA/PA overlay returned no intersections.")

    intersections["ibra_area_km2"] = intersections.geometry.area / 1_000_000.0
    intersections = intersections.drop(columns=["geometry"], errors="ignore")

    overlap_counts = (
        intersections.groupby("pa_id")["REG_CODE_7"].nunique().rename("ibra_n")
    )
    agg = (
        intersections.groupby(["pa_id", "REG_CODE_7", "REG_NAME_7"])["ibra_area_km2"]
        .sum()
        .reset_index()
    )
    idx = agg.groupby("pa_id")["ibra_area_km2"].idxmax()
    dominant = agg.loc[idx].copy()
    dominant = dominant.merge(pa[["pa_id", "pa_area_km2"]], on="pa_id", how="left")
    dominant["ibra_share"] = dominant["ibra_area_km2"] / dominant["pa_area_km2"]
    dominant["ibra_share"] = dominant["ibra_share"].clip(lower=0, upper=1)
    dominant = dominant.merge(overlap_counts.reset_index(), on="pa_id", how="left")
    dominant = dominant.rename(
        columns={"REG_CODE_7": "ibra_code", "REG_NAME_7": "ibra_name"}
    )
    dominant["schema_version"] = SCHEMA_VERSION
    return dominant[
        [
            "schema_version",
            "pa_id",
            "ibra_code",
            "ibra_name",
            "ibra_area_km2",
            "pa_area_km2",
            "ibra_share",
            "ibra_n",
        ]
    ]


def _load_series(df: pd.DataFrame) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    series = {}
    for pa_id, group in df.groupby("pa_id"):
        years = group["year"].to_numpy(dtype=float)
        values = group[PRIMARY_METRIC].to_numpy(dtype=float)
        order = np.argsort(years)
        years = years[order]
        values = values[order]
        series[str(pa_id)] = (years, values)
    return series


def _bootstrap_slopes(
    series: dict[str, tuple[np.ndarray, np.ndarray]],
    ibra_map: dict[str, list[str]],
    n_boot: int,
    block_len: int,
    rng: np.random.Generator,
) -> dict[str, list[float]]:
    boot: dict[str, list[float]] = {pa_id: [] for pa_id in series}
    ibra_codes = list(ibra_map.keys())
    if not ibra_codes:
        return boot
    for _ in range(n_boot):
        sampled = rng.choice(ibra_codes, size=len(ibra_codes), replace=True)
        for code in sampled:
            for pa_id in ibra_map.get(code, []):
                years, values = series[pa_id]
                res_years, res_values = _resample_time(years, values, block_len, rng)
                slope = _theil_sen(res_years, res_values)
                if not np.isnan(slope):
                    boot[pa_id].append(float(slope))
    return boot


def build_summary(
    df: pd.DataFrame,
    ibra_assign: pd.DataFrame,
    *,
    n_boot: int,
    block_len: int,
    seed: int,
) -> tuple[pd.DataFrame, dict[str, list[float]]]:
    series = _load_series(df)
    valid_ids = set(series.keys())
    ibra_assign = ibra_assign[ibra_assign["pa_id"].astype(str).isin(valid_ids)].copy()
    ibra_map = (
        ibra_assign.groupby("ibra_code")["pa_id"].apply(lambda x: [str(v) for v in x]).to_dict()
    )
    rng = np.random.default_rng(seed)
    boot = _bootstrap_slopes(series, ibra_map, n_boot=n_boot, block_len=block_len, rng=rng)

    records = []
    for pa_id, (years, values) in series.items():
        slope_full = _theil_sen(years, values)
        samples = np.array(boot.get(pa_id, []), dtype=float)
        if samples.size == 0:
            rec = {
                "pa_id": pa_id,
                "n_years": int(len(values)),
                "slope_full": slope_full,
                "slope_median": np.nan,
                "slope_ci_low": np.nan,
                "slope_ci_high": np.nan,
                "prob_slope_gt0": np.nan,
                "n_boot": 0,
            }
        else:
            rec = {
                "pa_id": pa_id,
                "n_years": int(len(values)),
                "slope_full": slope_full,
                "slope_median": float(np.nanmedian(samples)),
                "slope_ci_low": float(np.nanquantile(samples, 0.025)),
                "slope_ci_high": float(np.nanquantile(samples, 0.975)),
                "prob_slope_gt0": float(np.mean(samples > 0)),
                "n_boot": int(samples.size),
            }
        records.append(rec)

    summary = pd.DataFrame(records)
    summary = summary.merge(
        ibra_assign[["pa_id", "ibra_code", "ibra_name", "ibra_share"]], on="pa_id", how="left"
    )
    summary["schema_version"] = SCHEMA_VERSION
    summary["method"] = "theil_sen"
    summary["bootstrap"] = "ibra_cluster_moving_block"
    summary["block_len"] = block_len
    summary["n_boot_target"] = n_boot
    summary["min_valid_pixels"] = MIN_VALID_PIXELS
    summary["min_valid_years"] = MIN_VALID_YEARS
    return summary, boot


def write_summary(df: pd.DataFrame, root: Path) -> Path:
    path = root / PA_TREND_BOOTSTRAP_SUMMARY_CSV
    path.parent.mkdir(parents=True, exist_ok=True)
    df = df.copy()
    missing = [col for col in PA_TREND_BOOTSTRAP_SUMMARY_COLUMNS if col not in df.columns]
    if not missing:
        df = df[list(PA_TREND_BOOTSTRAP_SUMMARY_COLUMNS)]
    df.to_csv(path, index=False)
    return path


def write_ibra_assignment(df: pd.DataFrame, root: Path) -> Path:
    path = root / PA_IBRA_ASSIGNMENT_CSV
    path.parent.mkdir(parents=True, exist_ok=True)
    df = df.copy()
    missing = [col for col in PA_IBRA_ASSIGNMENT_COLUMNS if col not in df.columns]
    if not missing:
        df = df[list(PA_IBRA_ASSIGNMENT_COLUMNS)]
    df.to_csv(path, index=False)
    return path


def write_report(
    summary: pd.DataFrame,
    ibra_assign: pd.DataFrame,
    report_path: Path,
    *,
    n_boot: int,
    block_len: int,
    seed: int,
    root: Path,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    total_pas = ibra_assign["pa_id"].nunique()
    multi_ibra = (ibra_assign["ibra_n"] > 1).mean() if not ibra_assign.empty else 0.0
    share_med = ibra_assign["ibra_share"].median() if not ibra_assign.empty else np.nan
    valid = summary["slope_median"].notna()
    n_valid = int(valid.sum())

    geoms = pd.read_csv(root / PA_GEOMETRIES_CSV)[["pa_id", "NAME", "STATE"]]
    total_all = geoms["pa_id"].nunique()
    missing = total_all - total_pas
    top = (
        summary[valid]
        .merge(geoms, on="pa_id", how="left")
        .sort_values("slope_median", ascending=False)
        .head(20)[
            [
                "pa_id",
                "NAME",
                "STATE",
                "slope_median",
                "slope_ci_low",
                "slope_ci_high",
                "prob_slope_gt0",
            ]
        ]
        .rename(columns={"NAME": "name", "STATE": "state"})
    )

    lines = [
        "# Layer A trend uncertainty (IBRA cluster bootstrap)",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Bootstrap: IBRA cluster + moving-block time resample (block_len={block_len}, n_boot={n_boot}, seed={seed}).",
        f"Trend metric: inside {PRIMARY_METRIC} radiance (Theil-Sen); min valid pixels={MIN_VALID_PIXELS}; min years={MIN_VALID_YEARS}.",
        f"Total PAs with IBRA assignment: {total_pas}",
        f"IBRA coverage: {total_pas}/{total_all} ({total_pas / total_all:.1%}) assigned; missing={missing}",
        f"Multi-IBRA overlap fraction: {multi_ibra:.1%}; median dominant share={share_med:.2f}",
        f"PAs with bootstrap summaries: {n_valid} ({n_valid / total_pas:.1%})",
        "",
        "## Top 20 by median slope (inside mean radiance)",
        "",
        top.round(6).to_string(index=False),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def plot_forest(summary: pd.DataFrame, root: Path, *, top_n: int) -> Path:
    import matplotlib.pyplot as plt

    geoms = pd.read_csv(root / PA_GEOMETRIES_CSV)[["pa_id", "NAME", "STATE"]]
    df = summary.merge(geoms, on="pa_id", how="left")
    df = df[df["slope_median"].notna()].sort_values("slope_median", ascending=False).head(top_n)
    if df.empty:
        raise RuntimeError("No bootstrap summaries available for forest plot.")

    labels = [
        f"{row.NAME} ({row.STATE})" if isinstance(row.NAME, str) else row.pa_id
        for row in df.itertuples(index=False)
    ]
    y = np.arange(len(df))

    fig, ax = plt.subplots(figsize=(9, 0.35 * len(df) + 1.5))
    ax.hlines(y, df["slope_ci_low"], df["slope_ci_high"], color="#3B6EA5", lw=2)
    ax.scatter(df["slope_median"], y, color="#1F4E79", zorder=3)
    ax.axvline(0, color="black", lw=0.8, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Inside mean radiance slope (Theil-Sen; scaled units/yr)")
    ax.set_title(f"Top {len(df)} PAs by median slope (IBRA bootstrap CI)")
    ax.invert_yaxis()
    fig.tight_layout()

    out_path = root / FOREST_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def write_dominance(
    summary: pd.DataFrame,
    boot: dict[str, list[float]],
    root: Path,
    *,
    top_n: int,
) -> tuple[Path, Path]:
    import matplotlib.pyplot as plt

    top_ids = (
        summary[summary["slope_median"].notna()]
        .sort_values("slope_median", ascending=False)["pa_id"]
        .head(top_n)
        .tolist()
    )
    if not top_ids:
        raise RuntimeError("No bootstrap summaries available for dominance matrix.")

    samples = [np.array(boot.get(pa_id, []), dtype=float) for pa_id in top_ids]
    probs = np.zeros((len(top_ids), len(top_ids)), dtype=float)
    for i, samp_i in enumerate(samples):
        for j, samp_j in enumerate(samples):
            if samp_i.size == 0 or samp_j.size == 0:
                probs[i, j] = np.nan
            else:
                probs[i, j] = (samp_i[:, None] > samp_j[None, :]).mean()

    matrix = pd.DataFrame(probs, index=top_ids, columns=top_ids)
    csv_path = root / DOMINANCE_CSV
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(csv_path)

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(probs, vmin=0, vmax=1, cmap="viridis")
    ax.set_xticks(range(len(top_ids)))
    ax.set_yticks(range(len(top_ids)))
    ax.set_xticklabels(top_ids, rotation=90, fontsize=6)
    ax.set_yticklabels(top_ids, fontsize=6)
    ax.set_title("P(slope_i > slope_j) across bootstrap draws")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()

    fig_path = root / DOMINANCE_FIG
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)
    return csv_path, fig_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Spatial bootstrap for Layer A trend uncertainty.")
    parser.add_argument("--n-boot", type=int, default=300, help="Number of bootstrap draws.")
    parser.add_argument("--block-len", type=int, default=3, help="Moving-block length (years).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--top-n", type=int, default=20, help="Top N PAs for forest/dominance plots.")
    parser.add_argument("--skip-artefact", action="store_true", help="Skip artefact folder output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    ibra_path = _ensure_ibra_gpkg(root)
    ibra_gdf = gpd.read_file(ibra_path)
    pa_gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)

    ibra_assign = assign_ibra(pa_gdf, ibra_gdf)
    assign_path = write_ibra_assignment(ibra_assign, root)

    df = pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV)
    inside = df[
        (df["zone"] == "inside")
        & (df["buffer_type"] == PRIMARY_BUFFER_TYPE)
        & (df["valid_pixel_count"] >= MIN_VALID_PIXELS)
    ].copy()
    inside = inside.dropna(subset=[PRIMARY_METRIC])

    years_per_pa = inside.groupby("pa_id")["year"].nunique()
    keep_ids = years_per_pa[years_per_pa >= MIN_VALID_YEARS].index.astype(str)
    inside = inside[inside["pa_id"].astype(str).isin(keep_ids)]

    summary, boot = build_summary(
        inside,
        ibra_assign,
        n_boot=args.n_boot,
        block_len=args.block_len,
        seed=args.seed,
    )
    summary_path = write_summary(summary, root)

    report_path = root / REPORT_PATH
    write_report(
        summary,
        ibra_assign,
        report_path,
        n_boot=args.n_boot,
        block_len=args.block_len,
        seed=args.seed,
        root=root,
    )

    forest_path = plot_forest(summary, root, top_n=args.top_n)
    dominance_csv, dominance_fig = write_dominance(summary, boot, root, top_n=min(args.top_n, 15))

    if not args.skip_artefact:
        artefact_dir = root / "artefacts" / "wp0_19_layerA_trend_uncertainty"
        artefact_dir.mkdir(parents=True, exist_ok=True)

        outputs = [assign_path, summary_path, report_path, forest_path, dominance_csv, dominance_fig]
        copied = []
        for path in outputs:
            if path is None:
                continue
            shutil.copyfile(path, artefact_dir / path.name)
            copied.append(path.name)

        manifest = build_manifest(
            run_id="wp0_19_layerA_trend_uncertainty",
            wp="WP0.19",
            root=root,
            outputs=copied,
            inputs=["CAPAD 2024 PA geometries", "IBRA7 regions", "Zenodo nightlights v0.4"],
            notes="IBRA cluster bootstrap for Layer A trend uncertainty.",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)
        (artefact_dir / "README.txt").write_text(
            "WP0.19 artefact: IBRA-based trend uncertainty (bootstrap summaries + figures).\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

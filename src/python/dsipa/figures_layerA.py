"""Generate Layer A paper-ready figures (WP0.13b)."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import EDGE_PROFILES_NATIONAL_CSV, PA_GEOMETRIES_GPKG, RADIANCE_BUFFERS_NATIONAL_CSV

BASELINE_FIG = "manuscript/figures/fig_layerA_baseline_map.png"
EDGE_FIG = "manuscript/figures/fig_layerA_edge_profiles_aggregate.png"
FIGURE_INVENTORY = "analysis/reports/figure_inventory.md"

YEARS = (2013, 2018, 2024)
MIN_VALID_PIXELS = 10


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def plot_baseline_map(root: Path) -> Path:
    import matplotlib.pyplot as plt

    df = pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV)
    inside = df[(df["zone"] == "inside") & (df["year"] == YEARS[-1])][["pa_id", "mean"]]
    gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)[["pa_id", "geometry"]]
    merged = gdf.merge(inside, on="pa_id", how="left")

    vmax = merged["mean"].quantile(0.99)
    missing = merged["mean"].isna()
    fig, ax = plt.subplots(figsize=(7, 6))
    if missing.any():
        merged[missing].plot(
            ax=ax,
            color="#D9D9D9",
            linewidth=0,
        )
    merged[~missing].plot(
        column="mean",
        ax=ax,
        cmap="magma",
        vmin=0,
        vmax=vmax,
        legend=True,
        legend_kwds={"label": "Mean radiance (scaled)"},
        linewidth=0,
    )
    ax.set_title(f"Inside-PA radiance ({YEARS[-1]}; grey = missing)")
    ax.set_axis_off()
    fig.tight_layout()

    out_path = root / BASELINE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def _select_complete_pas(df: pd.DataFrame, year: int) -> list[str]:
    n_rings = df["ring_index"].nunique()
    valid = df[df["valid_pixel_count"] >= MIN_VALID_PIXELS]
    year_df = valid[valid["year"] == year]
    counts = year_df.groupby("pa_id")["ring_index"].nunique()
    return counts[counts == n_rings].index.tolist()


def _select_example_pa(df: pd.DataFrame, pa_gdf: gpd.GeoDataFrame) -> str:
    n_rings = df["ring_index"].nunique()
    valid = df[df["valid_pixel_count"] >= MIN_VALID_PIXELS]
    year_counts = valid.groupby(["pa_id", "year"])["ring_index"].nunique()
    complete_years = year_counts[year_counts == n_rings].reset_index()
    complete_all = complete_years.groupby("pa_id")["year"].nunique()
    candidates = complete_all[complete_all >= len(YEARS)].index.tolist()
    if not candidates:
        candidates = _select_complete_pas(df, YEARS[-1])
    if not candidates:
        return df["pa_id"].iloc[0]
    areas = pa_gdf.set_index("pa_id").loc[candidates]["area_km2"]
    return areas.sort_values(ascending=False).index[0]


def plot_edge_profiles(root: Path) -> Path:
    import matplotlib.pyplot as plt

    df = pd.read_csv(root / EDGE_PROFILES_NATIONAL_CSV)
    pa_gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)[["pa_id", "area_km2"]]
    complete_pas = _select_complete_pas(df, YEARS[-1])
    if not complete_pas:
        complete_pas = df["pa_id"].unique().tolist()
    complete_df = df[(df["pa_id"].isin(complete_pas)) & (df["year"] == YEARS[-1])]
    complete_df = complete_df[complete_df["valid_pixel_count"] >= MIN_VALID_PIXELS]

    n_complete = complete_df["pa_id"].nunique()
    agg = (
        complete_df.groupby("ring_index")
        .agg(
            ring_inner_km=("ring_inner_km", "first"),
            ring_outer_km=("ring_outer_km", "first"),
            median=("mean", "median"),
            p25=("mean", lambda x: np.quantile(x, 0.25)),
            p75=("mean", lambda x: np.quantile(x, 0.75)),
        )
        .reset_index()
    )
    mid = (agg["ring_inner_km"] + agg["ring_outer_km"]) / 2

    example_pa = _select_example_pa(df, pa_gdf)
    example_df = df[df["pa_id"] == example_pa]
    example_df = example_df[example_df["valid_pixel_count"] >= MIN_VALID_PIXELS]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    axes[0].plot(mid, agg["median"], marker="o", color="#4C72B0")
    axes[0].fill_between(mid, agg["p25"], agg["p75"], color="#4C72B0", alpha=0.2)
    axes[0].set_title(f"Aggregate profile (n={n_complete})")
    axes[0].set_xlabel("Distance from boundary (km)")
    axes[0].set_ylabel("Mean radiance (scaled)")

    for year in YEARS:
        year_df = example_df[example_df["year"] == year].sort_values("ring_index")
        if year_df.empty:
            continue
        mid_example = (year_df["ring_inner_km"] + year_df["ring_outer_km"]) / 2
        axes[1].plot(mid_example, year_df["mean"], marker="o", label=str(year))
    axes[1].set_title(f"Example PA: {example_pa}")
    axes[1].set_xlabel("Distance from boundary (km)")
    axes[1].legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.tight_layout()

    out_path = root / EDGE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer A figures for WP0.13b.")
    parser.add_argument(
        "--skip-baseline",
        action="store_true",
        help="Skip baseline map figure.",
    )
    parser.add_argument(
        "--skip-edge",
        action="store_true",
        help="Skip edge profile figure.",
    )
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    baseline_path = plot_baseline_map(root) if not args.skip_baseline else None
    edge_path = plot_edge_profiles(root) if not args.skip_edge else None

    if not args.skip_artefact:
        artefact_dir = root / "artefacts" / "wp0_13b_layerA_figures"
        artefact_dir.mkdir(parents=True, exist_ok=True)

        outputs = []
        for path in [baseline_path, edge_path]:
            if path is None:
                continue
            shutil.copyfile(path, artefact_dir / path.name)
            outputs.append(path.name)

        for extra in [
            root / "manuscript" / "figures" / "fig_layerA_trend_distribution.png",
            root / "manuscript" / "figures" / "fig_layerA_retention_quadrant.png",
            root / FIGURE_INVENTORY,
        ]:
            if extra.exists():
                shutil.copyfile(extra, artefact_dir / extra.name)
                outputs.append(extra.name)

        manifest = build_manifest(
            run_id="wp0_13b_layerA_figures",
            wp="WP0.13b",
            root=root,
            outputs=outputs,
            notes="WP0.13b Layer A figure set",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)

        (artefact_dir / "README.txt").write_text(
            "WP0.13b Layer A figures artefact. Contains paper-ready figures and inventory.\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

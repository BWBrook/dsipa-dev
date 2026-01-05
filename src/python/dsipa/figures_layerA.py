"""Generate Layer A paper-ready figures (WP0.13c)."""

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
    inside = df[(df["zone"] == "inside") & (df["year"] == YEARS[-1])][
        ["pa_id", "mean", "valid_pixel_count"]
    ]
    inside["eligible"] = inside["valid_pixel_count"] >= MIN_VALID_PIXELS
    gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)[["pa_id", "geometry"]]
    merged = gdf.merge(inside, on="pa_id", how="left")

    eligible = merged["eligible"].fillna(False)
    zero_mass = (merged.loc[eligible, "mean"] == 0).mean() if eligible.any() else 0.0

    vmax = merged.loc[eligible, "mean"].quantile(0.99) if eligible.any() else 1.0
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    minx, miny, maxx, maxy = merged.total_bounds

    merged[~eligible].plot(ax=axes[0], color="#F0F0F0", linewidth=0)
    merged[eligible].plot(ax=axes[0], color="#2C7FB8", linewidth=0)
    n_total = len(merged)
    n_eligible = int(eligible.sum())
    n_missing = n_total - n_eligible
    axes[0].set_title(
        f"Eligibility (>= {MIN_VALID_PIXELS} px; eligible={n_eligible}, missing={n_missing})"
    )
    axes[0].set_axis_off()
    axes[0].set_xlim(minx, maxx)
    axes[0].set_ylim(miny, maxy)
    axes[0].set_aspect("equal")

    merged[~eligible].plot(ax=axes[1], color="#D9D9D9", linewidth=0)
    merged[eligible].plot(
        column="mean",
        ax=axes[1],
        cmap="magma",
        vmin=0,
        vmax=vmax,
        legend=True,
        legend_kwds={"label": "Mean radiance (scaled)", "shrink": 0.4, "aspect": 30, "pad": 0.01},
        linewidth=0,
    )
    axes[1].set_title(
        f"Inside mean radiance ({YEARS[-1]}; zero-mass={zero_mass:.1%}, n={n_eligible})"
    )
    axes[1].set_axis_off()
    axes[1].set_xlim(minx, maxx)
    axes[1].set_ylim(miny, maxy)
    axes[1].set_aspect("equal")

    fig.subplots_adjust(wspace=0.02, bottom=0.05, top=0.95)

    out_path = root / BASELINE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_edge_profiles(root: Path) -> Path:
    import matplotlib.pyplot as plt

    df = pd.read_csv(root / EDGE_PROFILES_NATIONAL_CSV)
    valid = df[df["valid_pixel_count"] >= MIN_VALID_PIXELS]
    year_df = valid[valid["year"] == YEARS[-1]]
    n_total = df["pa_id"].nunique()
    n_rings = df["ring_index"].nunique()

    ring_meta = df[["ring_index", "ring_inner_km", "ring_outer_km"]].drop_duplicates().sort_values("ring_index")
    ring_counts = (
        year_df.groupby("ring_index")["pa_id"]
        .nunique()
        .reindex(ring_meta["ring_index"].to_list())
    )
    ring_frac = ring_counts / n_total if n_total else ring_counts
    ring_labels = [
        f"{row.ring_inner_km:.0f}-{row.ring_outer_km:.0f} km" for _, row in ring_meta.iterrows()
    ]

    complete_counts = year_df.groupby("pa_id")["ring_index"].nunique()
    complete_ids = complete_counts[complete_counts == n_rings].index.tolist()
    complete_df = year_df[year_df["pa_id"].isin(complete_ids)]
    n_complete = complete_df["pa_id"].nunique()
    frac_nonzero = (complete_df["frac_gt0"] > 0).mean() if not complete_df.empty else 0.0

    agg = (
        complete_df.groupby("ring_index")
        .agg(
            ring_inner_km=("ring_inner_km", "first"),
            ring_outer_km=("ring_outer_km", "first"),
            median=("frac_gt0", "median"),
            mean=("frac_gt0", "mean"),
            p25=("frac_gt0", lambda x: np.quantile(x, 0.25)),
            p75=("frac_gt0", lambda x: np.quantile(x, 0.75)),
            nonzero_share=("frac_gt0", lambda x: (x > 0).mean()),
        )
        .reset_index()
    )
    mid = (agg["ring_inner_km"] + agg["ring_outer_km"]) / 2 if not agg.empty else []
    median_zero = bool((agg["median"] == 0).all()) if not agg.empty else False

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].bar(ring_labels, ring_frac.values, color="#4C72B0", alpha=0.8)
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("Fraction of PAs with valid ring")
    axes[0].set_xlabel("Ring (inner–outer)")
    axes[0].set_title(f"Ring feasibility (n={n_total}; complete={n_complete})")

    if not agg.empty:
        axes[1].plot(mid, agg["nonzero_share"], marker="o", color="#DD8452", label="Share > 0")
        axes[1].set_xlabel("Distance from boundary (km)")
        axes[1].set_ylabel("Share of PAs with any light")
        axes[1].set_ylim(0, 1)
        median_note = "median frac_gt0=0" if median_zero else "median frac_gt0>0"
        axes[1].set_title(
            f"Edge profile (share > 0; n={n_complete}; {median_note})"
        )
        axes[1].legend(frameon=False, fontsize=8)
    else:
        axes[1].text(0.5, 0.5, "No complete rings", ha="center", va="center")
        axes[1].set_axis_off()

    fig.tight_layout()

    out_path = root / EDGE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer A figures for WP0.13c.")
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
        artefact_dir = root / "artefacts" / "wp0_13c_layerA_figures"
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
            run_id="wp0_13c_layerA_figures",
            wp="WP0.13c",
            root=root,
            outputs=outputs,
            inputs=[RADIANCE_BUFFERS_NATIONAL_CSV, EDGE_PROFILES_NATIONAL_CSV, PA_GEOMETRIES_GPKG],
            require_clean=True,
            notes="WP0.13c Layer A figure set (censoring-aware)",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)

        (artefact_dir / "README.txt").write_text(
            "WP0.13c Layer A figures artefact. Contains paper-ready figures and inventory.\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Generate Layer A paper-ready figures (WP0.13)."""

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
EDGE_FIG = "manuscript/figures/fig_layerA_edge_profiles_examples.png"
FIGURE_INVENTORY = "analysis/reports/figure_inventory.md"

TRIAD_IDS = ("TAS_50483", "NSW_N0856", "QLD_0117LZI001")
YEARS = (2013, 2018, 2024)


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def plot_baseline_map(root: Path) -> Path:
    import matplotlib.pyplot as plt

    df = pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV)
    inside = df[(df["zone"] == "inside") & (df["year"] == YEARS[-1])][["pa_id", "mean"]]
    gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)[["pa_id", "geometry"]]
    merged = gdf.merge(inside, on="pa_id", how="left")

    vmax = merged["mean"].quantile(0.99)
    fig, ax = plt.subplots(figsize=(7, 6))
    merged.plot(
        column="mean",
        ax=ax,
        cmap="magma",
        vmin=0,
        vmax=vmax,
        legend=True,
        legend_kwds={"label": "Mean radiance (scaled)"},
        linewidth=0,
    )
    ax.set_title(f"Inside-PA radiance ({YEARS[-1]})")
    ax.set_axis_off()
    fig.tight_layout()

    out_path = root / BASELINE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_edge_profiles(root: Path) -> Path:
    import matplotlib.pyplot as plt

    df = pd.read_csv(root / EDGE_PROFILES_NATIONAL_CSV)
    fig, axes = plt.subplots(1, len(TRIAD_IDS), figsize=(12, 4), sharey=True)
    if len(TRIAD_IDS) == 1:
        axes = [axes]

    for ax, pa_id in zip(axes, TRIAD_IDS):
        subset = df[df["pa_id"] == pa_id]
        for year in YEARS:
            year_df = subset[subset["year"] == year].sort_values("ring_index")
            mid = (year_df["ring_inner_km"] + year_df["ring_outer_km"]) / 2
            ax.plot(mid, year_df["mean"], marker="o", label=str(year))
        ax.set_title(pa_id)
        ax.set_xlabel("Distance from boundary (km)")
    axes[0].set_ylabel("Mean radiance (scaled)")
    axes[-1].legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.tight_layout()

    out_path = root / EDGE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer A figures for WP0.13.")
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
        artefact_dir = root / "artefacts" / "wp0_13_layerA_figures"
        artefact_dir.mkdir(parents=True, exist_ok=True)

        outputs = []
        for path in [baseline_path, edge_path]:
            if path is None:
                continue
            shutil.copyfile(path, artefact_dir / path.name)
            outputs.append(path.name)

        for extra in [root / "manuscript" / "figures" / "fig_layerA_trend_distribution.png",
                      root / "manuscript" / "figures" / "fig_layerA_vulnerability_coefficients.png",
                      root / FIGURE_INVENTORY]:
            if extra.exists():
                shutil.copyfile(extra, artefact_dir / extra.name)
                outputs.append(extra.name)

        manifest = build_manifest(
            run_id="wp0_13_layerA_figures",
            wp="WP0.13",
            root=root,
            outputs=outputs,
            notes="WP0.13 Layer A figure set",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)

        (artefact_dir / "README.txt").write_text(
            "WP0.13 Layer A figures artefact. Contains paper-ready figures and inventory.\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

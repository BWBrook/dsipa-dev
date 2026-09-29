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


def _plot_extent(gdf: gpd.GeoDataFrame) -> tuple[float, float, float, float]:
    """Return a stable mainland/Tasmania plotting window in lon/lat."""
    # CAPAD also contains marine and remote-island features. A fixed window
    # keeps those features from expanding the map to mostly empty ocean.
    return (112.0, 155.0, -44.5, -9.0)


def plot_baseline_map(
    root: Path,
    output_root: Path | None = None,
    *,
    radiance_path: Path | None = None,
    geometry_path: Path | None = None,
) -> Path:
    import matplotlib.pyplot as plt

    df = pd.read_csv(radiance_path or (root / RADIANCE_BUFFERS_NATIONAL_CSV))
    inside = df[(df["zone"] == "inside") & (df["year"] == YEARS[-1])][
        ["pa_id", "mean", "valid_pixel_count"]
    ].copy()
    inside["eligible"] = inside["valid_pixel_count"] >= MIN_VALID_PIXELS
    source_gdf = gpd.read_file(geometry_path or (root / PA_GEOMETRIES_GPKG))[["pa_id", "geometry"]]
    projected = source_gdf.to_crs("EPSG:3577")
    # Simplify only the display footprints. Counts, eligibility, and centroid
    # markers below continue to use the full source geometries.
    display_gdf = projected.copy()
    display_gdf["geometry"] = display_gdf.geometry.simplify(250.0, preserve_topology=True)
    # Geographic coordinates make the fixed mainland extent and labels transparent.
    merged = display_gdf.to_crs("EPSG:4326").merge(inside, on="pa_id", how="left")

    eligible = merged["eligible"].fillna(False)
    zero = eligible & merged["mean"].eq(0)
    nonzero = eligible & merged["mean"].gt(0)
    zero_mass = zero.sum() / eligible.sum() if eligible.any() else 0.0
    positive = merged.loc[nonzero, "mean"]
    vmax = float(positive.quantile(0.99)) if not positive.empty else 1.0
    if not np.isfinite(vmax) or vmax <= 0:
        vmax = float(positive.max()) if not positive.empty else 1.0

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 4.0), constrained_layout=True)
    minx, maxx, miny, maxy = _plot_extent(merged)
    n_total = len(merged)
    n_eligible = int(eligible.sum())
    n_ineligible = n_total - n_eligible

    # Pale footprints provide context; coloured circles are explicitly
    # centroid markers so small bright PAs remain visible without suggesting
    # that a marker is the footprint itself.
    for ax in axes:
        merged.plot(ax=ax, color="#FFFFFF", edgecolor="#BDBDBD", linewidth=0.12)
        if (~eligible).any():
            merged.loc[~eligible].plot(
                ax=ax, color="#F2F2F2", edgecolor="#D0D0D0", linewidth=0.12
            )
        if zero.any():
            merged.loc[zero].plot(
                ax=ax, color="#D9D9D9", edgecolor="#969696", linewidth=0.16
            )
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_aspect("equal")
        ax.set_xlabel("Longitude (°E)")
        ax.set_ylabel("Latitude (°; south negative)")

    # Compute centroids in the projected source CRS, then transform them to
    # geographic coordinates for plotting.
    centroid_gdf = projected.merge(inside, on="pa_id", how="left")
    centroid_gdf = centroid_gdf.loc[nonzero].copy()
    centroid_gdf["geometry"] = centroid_gdf.geometry.centroid
    centroids = centroid_gdf.to_crs("EPSG:4326")
    full_bounds = source_gdf.to_crs("EPSG:4326").total_bounds
    span = max(full_bounds[2] - full_bounds[0], full_bounds[3] - full_bounds[1], 1.0)
    margin = 0.05 * span
    if not centroids.empty:
        axes[0].scatter(
            centroids.geometry.x,
            centroids.geometry.y,
            s=7,
            color="#C43C39",
            alpha=0.75,
            linewidths=0,
            label="Eligible, non-zero (centroid marker)",
            zorder=4,
        )
    for ax, color, edge, label in [
        (axes[0], "#F2F2F2", "#D0D0D0", "Ineligible (fewer than 10 valid pixels)"),
        (axes[0], "#D9D9D9", "#969696", "Eligible, zero mean"),
        (axes[1], "#F2F2F2", "#D0D0D0", "Ineligible (fewer than 10 valid pixels)"),
        (axes[1], "#E2E2E2", "#A0A0A0", "Eligible, zero mean"),
    ]:
        ax.scatter([], [], s=24, color=color, edgecolor=edge, label=label)
    axes[0].set_title(
        f"2024 inside-summary eligibility\n"
        f"eligible={n_eligible:,}; ineligible={n_ineligible:,}"
    )
    axes[0].legend(loc="lower left", fontsize=7.5, frameon=True, framealpha=0.92)

    if not centroids.empty:
        values = centroids["mean"].clip(lower=0, upper=vmax)
        sc = axes[1].scatter(
            centroids.geometry.x,
            centroids.geometry.y,
            c=values,
            cmap="magma",
            vmin=0,
            vmax=vmax,
            s=10,
            alpha=0.82,
            linewidths=0,
            label="Eligible, non-zero (centroid marker)",
            zorder=4,
        )
        cbar = fig.colorbar(sc, ax=axes[1], shrink=0.72, pad=0.015, extend="max")
        cbar.set_label("Product-scaled radiance", fontsize=8)
    axes[1].set_title(
        f"Inside mean radiance ({YEARS[-1]})\n"
        f"eligible zero mean={zero_mass:.1%}; n={n_eligible:,}"
    )
    axes[1].legend(loc="lower left", fontsize=7.5, frameon=True, framealpha=0.92)

    # Keep remote islands and offshore features available in a compact
    # overview without letting their extent dominate the mainland/Tasmania
    # panels. The inset is geographic context; the main quantitative encoding
    # remains the centroid marker and colour scale above.
    for ax, show_values in [(axes[0], False), (axes[1], True)]:
        inset = ax.inset_axes([0.73, 0.69, 0.25, 0.25])
        inset.set_facecolor("#EAF3F8")
        merged.plot(ax=inset, color="#FFFFFF", edgecolor="#BDBDBD", linewidth=0.05)
        if (~eligible).any():
            merged.loc[~eligible].plot(ax=inset, color="#F2F2F2", edgecolor="#D0D0D0", linewidth=0.05)
        if zero.any():
            merged.loc[zero].plot(ax=inset, color="#D9D9D9", edgecolor="#969696", linewidth=0.05)
        if not centroids.empty:
            if show_values:
                inset.scatter(
                    centroids.geometry.x,
                    centroids.geometry.y,
                    c=centroids["mean"].clip(lower=0, upper=vmax),
                    cmap="magma",
                    vmin=0,
                    vmax=vmax,
                    s=2,
                    linewidths=0,
                    zorder=4,
                )
            else:
                inset.scatter(
                    centroids.geometry.x,
                    centroids.geometry.y,
                    s=2,
                    color="#C43C39",
                    linewidths=0,
                    zorder=4,
                )
        inset.set_xlim(full_bounds[0] - margin, full_bounds[2] + margin)
        inset.set_ylim(full_bounds[1] - margin, full_bounds[3] + margin)
        inset.set_xticks([])
        inset.set_yticks([])
        inset.set_title("Offshore context", fontsize=7.5, pad=1)
        for spine in inset.spines.values():
            spine.set_linewidth(0.6)

    fig.text(
        0.5,
        0.005,
        "Display footprints simplified to 250 m; colour capped at 99th percentile; centroid markers use full geometries.",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color="#555555",
    )

    out_path = (output_root or root) / BASELINE_FIG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def plot_edge_profiles(
    root: Path,
    *,
    edge_profile_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    """Render the aggregate edge profile from an explicit input when given.

    The optional paths let corrected-run renderers keep inputs and outputs
    under a declared run root without changing the historical CLI behaviour.
    """
    import matplotlib.pyplot as plt

    df = pd.read_csv(edge_profile_path or (root / EDGE_PROFILES_NATIONAL_CSV))
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

    out_path = output_path or (root / EDGE_FIG)
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

"""Render the national distribution of reviewed reserve-level OLS contributions.

Adapted from the candidate render_brightening_map.py. No external basemap is
used: grey shapes are CAPAD footprints, simplified only for display. Centroids
use the full EPSG:3577 geometries. The mainland/Tasmania panel and a Christmas
Island inset together retain every non-zero contribution in the input budget.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


EXTENT = (112.0, 155.0, -44.5, -9.0)
UP, DOWN, INK, MUTED, FOOTPRINT = "#b84a24", "#2b66a1", "#23313d", "#66727c", "#d8dcd9"
MAX_MARKER_AREA, MIN_MARKER_AREA = 250.0, 4.0
LABELS = {
    "NSW_N0018": ("Kosciuszko", (143.4, -39.0)),
    "WA_11648": ("Barrow Island", (112.7, -18.4)),
    "WA_2803": ("Murujuga", (116.8, -18.2)),
    "WA_33174": ("Thevenard Island", (112.7, -24.0)),
    "SA_0247": ("Yellabinna", (128.0, -33.7)),
    "CWTH_IPA20": ("Anindilyakwa", (139.3, -12.1)),
    "WA_27575": ("Neerabup", (113.1, -35.5)),
    "CWTH_IPA51": ("Southern Tanami", (127.2, -24.6)),
}
# Separate the three adjacent north-west sites without moving their markers.
LABEL_ALIGNMENT = {"WA_11648": "right", "WA_2803": "center", "WA_33174": "right"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def marker_area(values, maximum: float):
    """Display area in pt²; square-root scale with an explicit visibility floor."""
    return np.maximum(MIN_MARKER_AREA, MAX_MARKER_AREA * np.sqrt(np.abs(values) / maximum))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    budget_path = root / "analysis/reports/brightening_budget/reserve_budget.csv"
    geometry_path = root / "data/processed/pa_geometries_v0_3_0.gpkg"
    budget = pd.read_csv(budget_path).set_index("pa_id")
    geometry = gpd.read_file(geometry_path, columns=["pa_id", "NAME"]).set_index("pa_id")
    assert not budget.index.has_duplicates and not geometry.index.has_duplicates
    assert geometry.crs.to_epsg() == 3577
    assert len(budget) == 4426 and budget.slope_2013_2024.notna().all()
    slopes = budget.slope_2013_2024
    assert (int((slopes > 0).sum()), int((slopes < 0).sum())) == (560, 75)
    centroids = geometry.loc[budget.index].geometry.centroid.to_crs(4326)
    budget["lon"], budget["lat"] = centroids.x, centroids.y
    budget["name"] = geometry.loc[budget.index, "NAME"]
    in_main = budget.lon.between(EXTENT[0], EXTENT[1]) & budget.lat.between(EXTENT[2], EXTENT[3])
    outside = budget.loc[~in_main & slopes.ne(0)]
    assert outside.index.tolist() == ["CWTH_05"], "Reassess inset if out-of-view non-zero contributors change"
    assert outside.iloc[0]["name"] == "Christmas Island"
    assert all(pid in budget.index and slopes.loc[pid] != 0 for pid in LABELS)
    maximum = float(slopes.abs().max())
    display = geometry.copy()
    display.geometry = display.geometry.simplify(1000, preserve_topology=True)
    display = display.to_crs(4326)
    visible_shapes = display.cx[EXTENT[0]:EXTENT[1], EXTENT[2]:EXTENT[3]]

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                         "text.color": INK, "axes.labelcolor": MUTED,
                         "axes.edgecolor": "#b4bdc4", "xtick.color": MUTED,
                         "ytick.color": MUTED, "pdf.fonttype": 42, "ps.fonttype": 42})
    fig = plt.figure(figsize=(7.2, 6.6))
    ax = fig.add_axes([0.075, 0.225, 0.90, 0.665])
    visible_shapes.plot(ax=ax, facecolor=FOOTPRINT, edgecolor="none", linewidth=0, zorder=1)
    for sign, colour in ((1, UP), (-1, DOWN)):
        points = budget.loc[in_main & (np.sign(slopes) == sign)].copy()
        points = points.loc[points.slope_2013_2024.abs().sort_values(ascending=False).index]
        ax.scatter(points.lon, points.lat, s=marker_area(points.slope_2013_2024, maximum),
                   facecolor=colour, edgecolor="white", linewidth=0.35, alpha=0.82, zorder=3)
    annotations = []
    for pid, (name, label_position) in LABELS.items():
        row = budget.loc[pid]
        leader_gap = (0.5 * np.sqrt(marker_area(row.slope_2013_2024, maximum)) + 0.8
                      if pid in LABEL_ALIGNMENT else 3)
        leader_start = (1.0, 0.5) if LABEL_ALIGNMENT.get(pid) == "right" else (0.5, 0.5)
        annotations.append(ax.annotate(
            name, (row.lon, row.lat), xytext=label_position, textcoords="data",
            fontsize=8, ha=LABEL_ALIGNMENT.get(pid, "left"), va="center", zorder=5,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2, "alpha": 0.9},
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6,
                        "shrinkB": leader_gap, "relpos": leader_start},
        ))
    ax.set_xlim(EXTENT[:2])
    ax.set_ylim(EXTENT[2:])
    ax.set_aspect(1 / np.cos(np.radians(27)))
    ax.set_xticks([115, 125, 135, 145, 155])
    ax.set_yticks([-40, -30, -20, -10])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}°E"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{abs(y):g}°S"))
    ax.tick_params(labelsize=7, length=2.5, pad=3)
    ax.spines[["top", "right"]].set_visible(False)

    # The sole non-zero contributor outside the main extent is shown at its
    # own geographic scale, with the same quantitative marker-area encoding.
    inset = ax.inset_axes([0.015, 0.835, 0.15, 0.14])
    island = display.loc[["CWTH_05"]]
    island.plot(ax=inset, facecolor=FOOTPRINT, edgecolor="#929d98", linewidth=0.4)
    row = outside.iloc[0]
    inset.scatter([row.lon], [row.lat], s=marker_area([row.slope_2013_2024], maximum),
                  facecolor=DOWN, edgecolor="white", linewidth=0.35, alpha=0.82, zorder=3)
    bounds = island.total_bounds
    inset.set_xlim(bounds[0] - .025, bounds[2] + .025)
    inset.set_ylim(bounds[1] - .025, bounds[3] + .025)
    inset.set_aspect(1 / np.cos(np.radians(row.lat)))
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_title("Christmas Island", fontsize=7, pad=3, loc="left")
    inset.text(.5, -.15, f"105.6°E, 10.5°S\nslope {row.slope_2013_2024:.2f}",
               transform=inset.transAxes, ha="center", va="top", fontsize=6.4, color=MUTED)
    for spine in inset.spines.values():
        spine.set_linewidth(.5)

    fig.text(.075, .965, "Where reserves contribute to measured radiance change", ha="left", va="top",
             fontsize=11, fontweight="bold")
    fig.text(.075, .925, "2013–2024 OLS slopes · 4,426 assessable reserves · 560 positive · 75 negative · 3,791 zero",
             ha="left", va="top", fontsize=8, color=MUTED)
    sign_handles = [Line2D([], [], marker="o", ls="", markersize=6, markerfacecolor=colour,
                           markeredgecolor="white", alpha=.82, label=label)
                    for colour, label in [(UP, "Positive contribution"), (DOWN, "Negative contribution")]]
    sign_handles.append(Patch(facecolor=FOOTPRINT, edgecolor="none", label="CAPAD 2024 reserve footprints"))
    fig.legend(handles=sign_handles, loc="lower left", bbox_to_anchor=(.055, .115), ncol=1,
               frameon=False, fontsize=7.6, handletextpad=.6, labelspacing=.65)
    references = [10, 100, 1000]
    size_handles = [Line2D([], [], marker="o", ls="", markersize=np.sqrt(marker_area(v, maximum)),
                          markerfacecolor="#7f8a93", markeredgecolor="white", alpha=.82)
                    for v in references]
    fig.legend(size_handles, [f"{v:,}" for v in references], loc="lower left", bbox_to_anchor=(.50, .115),
               title="Slope magnitude (product units × km²/year)", title_fontsize=7.6,
               frameon=False, fontsize=7.6, ncol=3, columnspacing=1.2, handletextpad=.6)
    fig.text(.075, .09, "Circle area uses a square-root scale; minimum display area is 4 pt². Circles mark reserve centroids.",
             fontsize=7, color=MUTED)
    fig.text(.075, .055, "Main panel: mainland and Tasmania. Inset: the sole non-zero contributor outside this extent.",
             fontsize=7, color=MUTED)
    fig.text(.075, .025, "Grey shapes are protected-area footprints, not a land basemap. Overlapping designations remain separate.",
             fontsize=7, color=MUTED)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = [annotation.get_bbox_patch().get_window_extent(renderer) for annotation in annotations]
    assert not any(a.overlaps(b) for i, a in enumerate(boxes) for b in boxes[i + 1:]), "Site labels overlap"
    assert not any(box.overlaps(inset.get_window_extent(renderer)) for box in boxes), "Inset covers a site label"

    outputs = {}
    for suffix in ("png", "pdf"):
        path = root / f"manuscript/figures/fig_editorial_map.{suffix}"
        metadata = {"Creator": "DSIPA editorial national contribution map"}
        if suffix == "pdf":
            metadata.update({"CreationDate": None, "ModDate": None})
        fig.savefig(path, dpi=300, facecolor="white", metadata=metadata)
        outputs[str(path.relative_to(root))] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    plt.close(fig)
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "national_map": {
            "script": {"path": str(Path(__file__).relative_to(root)), "sha256": sha256(Path(__file__))},
            "adapted_from": "analysis/render_brightening_map.py",
            "inputs": {str(p.relative_to(root)): sha256(p) for p in (budget_path, geometry_path)},
            "counts": {"assessable": len(budget), "positive": 560, "negative": 75, "zero": 3791,
                       "main_panel_nonzero": int((in_main & slopes.ne(0)).sum()), "inset_nonzero": len(outside)},
            "units": "OLS slope of approximate area-integrated product radiance, product units x km2 per year",
            "main_extent_lonlat": list(EXTENT),
            "outside_main_nonzero": [{"pa_id": pid, "name": r["name"], "lon": r.lon, "lat": r.lat,
                                      "slope_2013_2024": r.slope_2013_2024} for pid, r in outside.iterrows()],
            "all_nonzero_contributors_displayed": True,
            "centroids": "Full source geometry in EPSG:3577, transformed to EPSG:4326",
            "footprints": "All CAPAD 2024 geometries; simplified to 1000 m only for display; no external basemap",
            "marker_area": {"formula": "max(4, 250 * sqrt(abs(slope) / max_abs_slope))", "units": "pt2",
                            "max_abs_slope": maximum, "legend_values": references},
            "labelled_sites": {pid: name for pid, (name, _) in LABELS.items()},
            "label_positions_lonlat": {pid: list(position) for pid, (_, position) in LABELS.items()},
            "label_alignment": {pid: LABEL_ALIGNMENT.get(pid, "left") for pid in LABELS},
            "site_label_overlap_check": "PASS", "outputs": outputs,
        },
        "visual_qa": {"status": "pending"},
    }
    receipt = root / "analysis/reports/editorial_r4_map_20261019.json"
    receipt.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"counts": report["national_map"]["counts"], "outputs": outputs}, indent=2))


if __name__ == "__main__":
    main()

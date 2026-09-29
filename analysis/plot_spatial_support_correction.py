#!/usr/bin/env python3
"""Render a bounded visual audit of corrected coastal support geometry.

The figure is diagnostic evidence for the 19 September 2026 spatial-support
correction. It does not render radiance values or alter any source geometry.
Each panel is plotted in EPSG:3577 and shows the accepted CAPAD boundary, the
raw 1 km outward support used by the q128 geometry engine, the cached Natural
Earth land union, and the AIMS Coast50K Split land polygons.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import pandas as pd
from shapely import wkb
from shapely.geometry import GeometryCollection
from shapely.ops import unary_union

SCRIPT_REPO = Path(__file__).resolve().parents[1]
if str(SCRIPT_REPO / "src/python") not in sys.path:
    sys.path.insert(0, str(SCRIPT_REPO / "src/python"))

CRS = "EPSG:3577"
PA_IDS = ("WA_39584", "WA_05225", "NSW_LHI")
DEFAULT_OUTPUT = SCRIPT_REPO / "analysis/reports/spatial_correction_coastline_comparison.png"
DEFAULT_RECEIPT = SCRIPT_REPO / "analysis/reports/spatial_correction_coastline_comparison_manifest.json"
DEFAULT_PA_SOURCE = (
    "deep-server-ts:/data/codex/repos/dsipa-dev-goal012-20260723T115300Z/"
    "data/processed/pa_geometries_v0_3_0.gpkg"
)
DEFAULT_OLD_SOURCE = (
    "deep-server-ts:/data/codex/repos/dsipa-dev-goal012-20260723T115300Z/"
    "data/processed/cache/land_union_ne_110m.wkb"
)
DEFAULT_AIMS_SOURCE = (
    "deep-server-ts:/data/codex/scratch/dsipa-spatial-correction-20260919/"
    "coastline/Split/Split/AU_NESP-MaC-3-17_AIMS_Aus-Coastline-50k_2024_V1-1_split.shp"
)

NAMES = {
    "WA_39584": "Henderson",
    "WA_05225": "Torndirrup",
    "NSW_LHI": "Lord Howe Island",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pa-gpkg", type=Path, required=True, help="Accepted CAPAD geometry GPKG.")
    parser.add_argument("--old-land-wkb", type=Path, required=True, help="Cached Natural Earth union in EPSG:3577.")
    parser.add_argument("--aims-split", type=Path, required=True, help="AIMS Coast50K v1-1 Split polygon shapefile.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--context-km", type=float, default=5.0)
    parser.add_argument("--quad-segs", type=int, default=128)
    parser.add_argument("--pa-source-label", default=DEFAULT_PA_SOURCE)
    parser.add_argument("--old-land-source-label", default=DEFAULT_OLD_SOURCE)
    parser.add_argument("--aims-source-label", default=DEFAULT_AIMS_SOURCE)
    return parser.parse_args(argv)


def _source_record(path: Path, source_label: str) -> dict[str, object]:
    path = path.resolve()
    return {
        "path_used": str(path),
        "source_label": source_label,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def _clip_union(geometries: gpd.GeoSeries, window) -> object:
    pieces = [geometry.intersection(window) for geometry in geometries if not geometry.is_empty]
    return unary_union(pieces) if pieces else GeometryCollection()


def _add_scale_bar(ax, bounds: tuple[float, float, float, float]) -> None:
    xmin, xmax, ymin, ymax = bounds
    width = xmax - xmin
    length = 5000.0 if width >= 12000.0 else 2000.0 if width >= 6000.0 else 1000.0
    x0 = xmin + 0.07 * width
    y0 = ymin + 0.07 * (ymax - ymin)
    ax.plot([x0, x0 + length], [y0, y0], color="black", linewidth=3, solid_capstyle="butt", zorder=20)
    ax.text(x0 + length / 2, y0 + 0.02 * (ymax - ymin), f"{length / 1000:g} km", ha="center", va="bottom", fontsize=8)


def _add_north_arrow(ax, bounds: tuple[float, float, float, float]) -> None:
    xmin, xmax, ymin, ymax = bounds
    x = xmax - 0.09 * (xmax - xmin)
    y0 = ymin + 0.72 * (ymax - ymin)
    y1 = y0 + 0.12 * (ymax - ymin)
    ax.annotate("N", xy=(x, y1), xytext=(x, y0), ha="center", va="bottom", fontsize=10, fontweight="bold",
                arrowprops={"arrowstyle": "-|>", "color": "black", "linewidth": 1.2})


def _area_label(area_m2: float | None) -> str:
    if area_m2 is None:
        return "none in 5 km window"
    return f"{area_m2 / 1_000_000:.2f} km²"


def _shapefile_record(path: Path, source_label: str) -> dict[str, object]:
    """Record the primary shapefile component and every sidecar consumed by GDAL."""
    record = _source_record(path, source_label)
    components = {}
    for component in sorted(path.parent.glob(f"{path.stem}.*")):
        components[component.name] = _source_record(component, f"{source_label} [{component.suffix.lstrip('.')}]")
    record["components"] = components
    return record


def render(args: argparse.Namespace) -> tuple[Path, Path]:
    for path in (args.pa_gpkg, args.old_land_wkb, args.aims_split):
        if not path.is_file():
            raise FileNotFoundError(path)
    if args.context_km <= 0 or args.quad_segs <= 0:
        raise ValueError("context-km and quad-segs must be positive")

    pas = gpd.read_file(args.pa_gpkg)
    required = {"pa_id", "NAME", "geometry"}
    missing = required.difference(pas.columns)
    if missing:
        raise ValueError(f"CAPAD geometry is missing columns: {sorted(missing)}")
    selected = pas[pas["pa_id"].astype(str).isin(PA_IDS)].copy()
    if set(selected["pa_id"].astype(str)) != set(PA_IDS):
        raise ValueError(f"CAPAD geometry is missing requested IDs: {sorted(set(PA_IDS) - set(selected.pa_id))}")
    selected = selected.set_index("pa_id").loc[list(PA_IDS)].reset_index().to_crs(CRS)

    old_land = wkb.loads(args.old_land_wkb.read_bytes())
    if old_land.is_empty:
        raise ValueError("Natural Earth land union is empty")
    aims = gpd.read_file(args.aims_split).to_crs(CRS)
    if aims.empty:
        raise ValueError("AIMS Split coastline is empty")
    aims_sindex = aims.sindex

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    panel_receipts: list[dict[str, object]] = []
    for ax, row in zip(axes, selected.itertuples(index=False)):
        pa = row.geometry
        context = pa.buffer(args.context_km * 1000.0, resolution=args.quad_segs)
        raw_1km = pa.buffer(1000.0, resolution=args.quad_segs).difference(pa)
        local_positions = aims_sindex.query(context, predicate="intersects")
        aims_local = _clip_union(aims.iloc[local_positions].geometry, context)
        old_local = old_land.intersection(context)
        xmin, ymin, xmax, ymax = context.bounds
        width, height = xmax - xmin, ymax - ymin
        margin = max(width, height) * 0.03
        bounds = (xmin - margin, xmax + margin, ymin - margin, ymax + margin)

        if not old_local.is_empty:
            gpd.GeoSeries([old_local], crs=CRS).plot(ax=ax, color="#E69F00", alpha=0.28, edgecolor="#B66A00", linewidth=0.5)
        if not aims_local.is_empty:
            gpd.GeoSeries([aims_local], crs=CRS).plot(ax=ax, color="#56B4E9", alpha=0.32, edgecolor="#0072B2", linewidth=0.6)
        gpd.GeoSeries([raw_1km], crs=CRS).plot(ax=ax, facecolor="none", edgecolor="#D55E00", linewidth=1.5, linestyle="--")
        gpd.GeoSeries([pa], crs=CRS).plot(ax=ax, facecolor="none", edgecolor="black", linewidth=1.5)
        ax.set_xlim(bounds[0], bounds[1])
        ax.set_ylim(bounds[2], bounds[3])
        ax.set_aspect("equal")
        ax.set_title(f"{NAMES[row.pa_id]}\n{row.pa_id}", fontsize=11)
        ax.set_xlabel("Easting (m)")
        if ax is axes[0]:
            ax.set_ylabel("Northing (m)")
        else:
            ax.set_ylabel("")
        ax.grid(alpha=0.18, linewidth=0.5)
        _add_scale_bar(ax, bounds)
        _add_north_arrow(ax, bounds)
        old_area = None if old_local.is_empty else old_local.area
        aims_area = None if aims_local.is_empty else aims_local.area
        label = (
            f"PA area: {_area_label(pa.area)}\n"
            f"raw 1 km support: {_area_label(raw_1km.area)}\n"
            f"AIMS land in window: {_area_label(aims_area)}\n"
            f"old NE land in window: {_area_label(old_area)}"
        )
        ax.text(0.02, 0.98, label, transform=ax.transAxes, ha="left", va="top", fontsize=8,
                bbox={"facecolor": "white", "alpha": 0.86, "edgecolor": "0.7", "pad": 4})
        if old_local.is_empty:
            ax.text(0.98, 0.04, "no old land in window", transform=ax.transAxes, ha="right", va="bottom",
                    fontsize=8, color="#8C510A", fontweight="bold")
        panel_receipts.append({
            "pa_id": row.pa_id,
            "name": NAMES[row.pa_id],
            "context_km": args.context_km,
            "pa_area_km2": pa.area / 1_000_000,
            "raw_1km_support_area_km2": raw_1km.area / 1_000_000,
            "old_ne_land_area_in_context_km2": None if old_local.is_empty else old_local.area / 1_000_000,
            "aims_land_area_in_context_km2": None if aims_local.is_empty else aims_local.area / 1_000_000,
            "aims_features_intersecting_context": int(len(local_positions)),
        })

    legend = [
        Patch(facecolor="none", edgecolor="black", linewidth=1.5, label="Accepted CAPAD boundary"),
        Patch(facecolor="none", edgecolor="#D55E00", linestyle="--", linewidth=1.5, label="Corrected raw 1 km support"),
        Patch(facecolor="#E69F00", edgecolor="#B66A00", alpha=0.28, label="Old Natural Earth 1:110m land"),
        Patch(facecolor="#56B4E9", edgecolor="#0072B2", alpha=0.32, label="AIMS Coast50K Split land"),
        Line2D([], [], color="black", linewidth=0, label="Panels: EPSG:3577; 5 km context"),
    ]
    fig.legend(handles=legend, loc="lower center", ncol=3, frameon=True, fontsize=9, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Spatial-support correction: coastal land-mask comparison", fontsize=14, y=1.02)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=200, bbox_inches="tight")
    plt.close(fig)

    receipt = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis_id": "spatial-correction-20260919",
        "purpose": "Bounded visual audit of corrected spatial support; not a manuscript figure or radiance result.",
        "parameters": {"crs": CRS, "context_km": args.context_km, "raw_buffer_km": 1.0, "quad_segs": args.quad_segs, "pa_ids": list(PA_IDS)},
        "inputs": {
            "accepted_pa_gpkg": _source_record(args.pa_gpkg, args.pa_source_label),
            "old_natural_earth_land_wkb": _source_record(args.old_land_wkb, args.old_land_source_label),
            "aims_split_shapefile": _shapefile_record(args.aims_split, args.aims_source_label),
        },
        "script": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        "output": {"path": str(args.output.resolve()), "sha256": sha256(args.output), "bytes": args.output.stat().st_size},
        "panels": panel_receipts,
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return args.output, args.receipt


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output, receipt = render(args)
    print(json.dumps({"output": str(output), "receipt": str(receipt)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

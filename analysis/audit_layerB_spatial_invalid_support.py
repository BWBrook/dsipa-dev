#!/usr/bin/env python3
"""Inventory invalid ALAN cells that could serve accepted Layer B locations.

The audit uses the archived CAPAD geometries and a spatial index to restrict
raster reads to blocks near the accepted PA-plus-10-km occurrence support. It
then checks raw nodata and negative values in those blocks. It does not read or
recreate ALA records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
import shapely
from pyproj import Transformer
from shapely.geometry import Polygon
from shapely.strtree import STRtree


def _sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk_size), b""):
            digest.update(block)
    return digest.hexdigest()


def _raster_support_inventory(path: Path, tree: STRtree, to_epsg3577, buffer_m: float):
    # The raster is nominally 500 m; half a cell diagonal makes the centre
    # distance test conservative for any occurrence coordinate in the cell.
    cell_margin_m = 0.5 * np.sqrt(2.0) * 500.0
    with rasterio.open(path) as dataset:
        distances: list[np.ndarray] = []
        raw_values: list[np.ndarray] = []
        nodata_flags: list[np.ndarray] = []
        lons: list[np.ndarray] = []
        lats: list[np.ndarray] = []
        candidate_blocks = 0
        for _, window in dataset.block_windows(1):
            left, bottom, right, top = rasterio.windows.bounds(window, dataset.transform)
            bx = np.array([left, right, right, left], dtype=float)
            by = np.array([bottom, bottom, top, top], dtype=float)
            block_x, block_y = to_epsg3577.transform(bx, by)
            block_geom = Polygon(zip(block_x, block_y)).buffer(buffer_m + 1000.0)
            if not tree.query(block_geom, predicate="intersects").size:
                continue
            candidate_blocks += 1
            raw = dataset.read(1, window=window, masked=False)
            finite = np.isfinite(raw)
            nodata = dataset.nodata
            nodata_mask = finite & (raw == nodata) if nodata is not None else np.zeros(raw.shape, dtype=bool)
            negative = finite & ~nodata_mask & (raw < 0)
            invalid = nodata_mask | negative
            if not invalid.any():
                continue
            rows, cols = np.where(invalid)
            rows = rows + int(window.row_off)
            cols = cols + int(window.col_off)
            xs, ys = rasterio.transform.xy(dataset.transform, rows, cols, offset="center")
            xs = np.asarray(xs, dtype=float)
            ys = np.asarray(ys, dtype=float)
            x3577, y3577 = to_epsg3577.transform(xs, ys)
            points = shapely.points(x3577, y3577)
            _, nearest = tree.query_nearest(points, return_distance=True)
            distances.append(np.asarray(nearest, dtype=float))
            raw_values.append(raw[invalid].astype(np.int64))
            nodata_flags.append(nodata_mask[invalid])
            lons.append(xs)
            lats.append(ys)
        if not distances:
            return {
                "year": path.name.split("_s_")[1][:4],
                "path": str(path),
                "sha256": _sha256(path),
                "scale": dataset.scales[0] if dataset.scales else None,
                "offset": dataset.offsets[0] if dataset.offsets else None,
                "candidate_blocks": candidate_blocks,
                "negative_cells_within_pa_plus_buffer": 0,
                "nodata_cells_within_pa_plus_buffer": 0,
                "negative_examples": [],
                "nodata_examples": [],
            }

        distance_arr = np.concatenate(distances)
        raw_arr = np.concatenate(raw_values)
        nodata_arr = np.concatenate(nodata_flags)
        lon_arr = np.concatenate(lons)
        lat_arr = np.concatenate(lats)
        possible = distance_arr <= (buffer_m + cell_margin_m)
        negative_arr = ~nodata_arr & (raw_arr < 0)
        negative_possible = possible & negative_arr
        nodata_possible = possible & ~negative_arr
        negative_examples = [
            {
                "lon": float(lon_arr[i]),
                "lat": float(lat_arr[i]),
                "raw": int(raw_arr[i]),
                "distance_to_pa_m": float(distance_arr[i]),
            }
            for i in np.flatnonzero(negative_possible)[:20]
        ]
        nodata_examples = [
            {
                "lon": float(lon_arr[i]),
                "lat": float(lat_arr[i]),
                "distance_to_pa_m": float(distance_arr[i]),
            }
            for i in np.flatnonzero(nodata_possible)[:20]
        ]
        return {
            "year": path.name.split("_s_")[1][:4],
            "path": str(path),
            "sha256": _sha256(path),
            "scale": dataset.scales[0] if dataset.scales else None,
            "offset": dataset.offsets[0] if dataset.offsets else None,
            "candidate_blocks": candidate_blocks,
            "negative_cells_within_pa_plus_buffer": int(negative_possible.sum()),
            "nodata_cells_within_pa_plus_buffer": int(nodata_possible.sum()),
            "negative_examples": negative_examples,
            "nodata_examples": nodata_examples,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--buffer-km", type=float, default=10.0)
    args = parser.parse_args()

    import geopandas as gpd

    geometry_path = args.repo_root / "data" / "processed" / "pa_geometries_v0_3_0.gpkg"
    geometries = gpd.read_file(geometry_path).to_crs("EPSG:3577")
    tree = STRtree(geometries.geometry.to_list())
    to_epsg3577 = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
    raster_dir = args.repo_root / "data" / "raw" / "nightlights_zenodo_v0_4"
    years = [
        _raster_support_inventory(path, tree, to_epsg3577, args.buffer_km * 1000.0)
        for path in sorted(raster_dir.glob("*.tif"))
    ]
    output = {
        "repository": str(args.repo_root),
        "geometry": {"path": str(geometry_path), "sha256": _sha256(geometry_path)},
        "support": {
            "crs": "EPSG:3577",
            "buffer_km": args.buffer_km,
            "distance_rule": "cell-centre distance to archived PA geometries <= buffer + half 500-m cell diagonal",
        },
        "years": years,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

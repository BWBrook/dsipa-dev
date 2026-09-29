#!/usr/bin/env python3
"""Verify local land-union equivalence of AIMS Full and Split polygons."""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union


CHECK_IDS = (
    "WA_39584",
    "WA_05225",
    "NSW_LHI",
    "CWTH_05",
    "CWTH_07",
    "CWTH_08",
    "CWTH_09",
    "CWTH_10",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", type=Path, required=True)
    parser.add_argument("--split", type=Path, required=True)
    parser.add_argument("--pa-gpkg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--buffer-m", type=float, default=5000.0)
    parser.add_argument("--quad-segs", type=int, default=128)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pas = gpd.read_file(args.pa_gpkg)
    pas = pas.loc[pas["pa_id"].isin(CHECK_IDS)].to_crs("EPSG:3577")
    missing = sorted(set(CHECK_IDS) - set(pas["pa_id"]))
    if missing:
        raise ValueError(f"Protected-area checks missing from input: {missing}")
    full_source = gpd.read_file(args.full)
    split_source = gpd.read_file(args.split)
    full_index = full_source.sindex
    split_index = split_source.sindex

    rows: list[dict[str, object]] = []
    for row in pas.itertuples():
        window = row.geometry.buffer(args.buffer_m, quad_segs=args.quad_segs)
        window_wgs = gpd.GeoSeries([window], crs="EPSG:3577").to_crs(
            "EPSG:4326"
        ).iloc[0]
        full_positions = full_index.query(window_wgs, predicate="intersects")
        split_positions = split_index.query(window_wgs, predicate="intersects")
        full_local = full_source.iloc[full_positions].to_crs("EPSG:3577")
        split_local = split_source.iloc[split_positions].to_crs("EPSG:3577")
        full_union = unary_union(
            full_local.geometry.intersection(window).to_numpy()
        )
        split_union = unary_union(
            split_local.geometry.intersection(window).to_numpy()
        )
        rows.append(
            {
                "pa_id": row.pa_id,
                "name": row.NAME,
                "full_features": len(full_local),
                "split_features": len(split_local),
                "full_area_m2": full_union.area,
                "split_area_m2": split_union.area,
                "absolute_area_difference_m2": abs(
                    full_union.area - split_union.area
                ),
                "symmetric_difference_m2": full_union.symmetric_difference(
                    split_union
                ).area,
            }
        )
    output = pd.DataFrame(rows).sort_values("pa_id")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()

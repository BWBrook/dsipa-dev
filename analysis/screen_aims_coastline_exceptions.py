#!/usr/bin/env python3
"""Screen CAPAD 5 km proximity to documented AIMS coastline exceptions."""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


# Approved-name coordinates are from Geoscience Australia's Composite
# Gazetteer. Lloyd and Olive also match coordinates in the AIMS v1-1 errata.
LOCATIONS = (
    (
        "Bribie Island/Sandstone Point bridge",
        153.12999893,
        -27.08678255,
        "GA Gazetteer: Sandstone Point",
    ),
    ("Swan River, WA", 115.73527778, -32.05527778, "GA Gazetteer: SWAN RIVER"),
    ("Collins Pool, WA", 123.73713, -18.45999, "GA Gazetteer: COLLINS POOL"),
    (
        "Brisbane Water, NSW",
        151.33448190,
        -33.48175443,
        "GA Gazetteer: Brisbane Water",
    ),
    (
        "Mooney Mooney Creek, NSW",
        151.25114910,
        -33.34842148,
        "GA Gazetteer: Mooney Mooney Creek",
    ),
    (
        "Parramatta River, NSW",
        151.10115630,
        -33.83175615,
        "GA Gazetteer: Parramatta River",
    ),
    (
        "Brisbane River, QLD",
        153.16495190,
        -27.37341545,
        "GA Gazetteer: Brisbane River",
    ),
    (
        "Lloyd Island, QLD",
        143.39969175,
        -12.76056562,
        "AIMS errata/GA Gazetteer",
    ),
    (
        "Olive River mouth, QLD",
        143.08693683,
        -12.15989648,
        "AIMS errata/GA Gazetteer",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pa-gpkg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--distance-m", type=float, default=5000.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    points = gpd.GeoDataFrame(
        [
            {
                "exception": name,
                "location_source": source,
                "geometry": Point(longitude, latitude),
            }
            for name, longitude, latitude, source in LOCATIONS
        ],
        crs="EPSG:4326",
    ).to_crs("EPSG:3577")
    pas = gpd.read_file(args.pa_gpkg).to_crs("EPSG:3577")
    rows: list[dict[str, object]] = []
    for point in points.itertuples():
        distances = pas.geometry.distance(point.geometry)
        nearby = pas.loc[
            distances <= args.distance_m, ["pa_id", "NAME", "STATE"]
        ].copy()
        if nearby.empty:
            rows.append(
                {
                    "exception": point.exception,
                    "location_source": point.location_source,
                    "pa_id": "",
                    "pa_name": "",
                    "state": "",
                    "distance_m": float(distances.min()),
                }
            )
            continue
        for index, pa in nearby.iterrows():
            rows.append(
                {
                    "exception": point.exception,
                    "location_source": point.location_source,
                    "pa_id": pa.pa_id,
                    "pa_name": pa.NAME,
                    "state": pa.STATE,
                    "distance_m": float(distances.loc[index]),
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output, index=False)


if __name__ == "__main__":
    main()

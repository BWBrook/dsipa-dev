"""Helpers to fetch CAPAD data from DCCEEW ArcGIS REST services."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable

import geopandas as gpd

CAPAD_MAPSERVER = "https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer"
CAPAD_PROTECTED_AREAS_LAYER = 0
CAPAD_MARINE_LAYER = 1


@dataclass(frozen=True)
class CapadQuery:
    layer: int = CAPAD_PROTECTED_AREAS_LAYER
    where: str = "1=1"
    out_fields: str = "*"
    out_sr: int = 4326
    chunk_size: int = 2000


def _fetch_json(url: str, timeout: int = 60) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "dsipa-nbs/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as resp:
        return json.load(resp)


def _query_url(params: dict) -> str:
    return CAPAD_MAPSERVER + f"/{params.pop('layer')}/query?" + urllib.parse.urlencode(params)


def fetch_service_metadata() -> dict:
    return _fetch_json(CAPAD_MAPSERVER + "?f=pjson")


def fetch_layer_metadata(layer: int) -> dict:
    return _fetch_json(f"{CAPAD_MAPSERVER}/{layer}?f=pjson")


def fetch_count(query: CapadQuery) -> int:
    params = {
        "layer": query.layer,
        "where": query.where,
        "returnCountOnly": "true",
        "f": "json",
    }
    data = _fetch_json(_query_url(params))
    return int(data.get("count", 0))


def iter_geojson_features(query: CapadQuery) -> Iterable[dict]:
    total = fetch_count(query)
    for offset in range(0, total, query.chunk_size):
        params = {
            "layer": query.layer,
            "where": query.where,
            "outFields": query.out_fields,
            "outSR": query.out_sr,
            "orderByFields": "OBJECTID",
            "resultOffset": offset,
            "resultRecordCount": query.chunk_size,
            "f": "geojson",
        }
        data = _fetch_json(_query_url(params))
        features = data.get("features", [])
        for feature in features:
            yield feature


def fetch_gdf(query: CapadQuery) -> gpd.GeoDataFrame:
    features = list(iter_geojson_features(query))
    if not features:
        return gpd.GeoDataFrame(columns=[], geometry=[], crs=f"EPSG:{query.out_sr}")
    gdf = gpd.GeoDataFrame.from_features(features, crs=f"EPSG:{query.out_sr}")
    return gdf

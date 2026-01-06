"""Helpers to fetch IBRA region data from DCCEEW ArcGIS REST services."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import geopandas as gpd

from dsipa.paths import find_repo_root

IBRA_FEATURESERVER = (
    "https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/IBRA7_Regions/FeatureServer"
)
IBRA_REGIONS_LAYER = 0
IBRA_OUT_FIELDS = "REG_CODE_7,REG_NAME_7,HECTARES"

IBRA_GPKG = "data/raw/ibra7_regions.gpkg"


@dataclass(frozen=True)
class IbraQuery:
    layer: int = IBRA_REGIONS_LAYER
    where: str = "1=1"
    out_fields: str = IBRA_OUT_FIELDS
    out_sr: int = 4326
    chunk_size: int = 2000


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fetch_json(url: str, timeout: int = 60) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "dsipa-nbs/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as resp:
        return json.load(resp)


def _query_url(params: dict) -> str:
    return IBRA_FEATURESERVER + f"/{params.pop('layer')}/query?" + urllib.parse.urlencode(params)


def fetch_service_metadata() -> dict:
    return _fetch_json(IBRA_FEATURESERVER + "?f=pjson")


def fetch_layer_metadata(layer: int) -> dict:
    return _fetch_json(f"{IBRA_FEATURESERVER}/{layer}?f=pjson")


def fetch_count(query: IbraQuery) -> int:
    params = {
        "layer": query.layer,
        "where": query.where,
        "returnCountOnly": "true",
        "f": "json",
    }
    data = _fetch_json(_query_url(params))
    return int(data.get("count", 0))


def iter_geojson_features(query: IbraQuery) -> Iterable[dict]:
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
        for feature in data.get("features", []):
            yield feature


def fetch_gdf(query: IbraQuery) -> gpd.GeoDataFrame:
    features = list(iter_geojson_features(query))
    if not features:
        return gpd.GeoDataFrame(columns=[], geometry=[], crs=f"EPSG:{query.out_sr}")
    return gpd.GeoDataFrame.from_features(features, crs=f"EPSG:{query.out_sr}")


def _hash_geometries(gdf: gpd.GeoDataFrame) -> str:
    import hashlib

    digest = hashlib.sha256()
    ordered = gdf.sort_values("REG_CODE_7")
    for _, row in ordered.iterrows():
        digest.update(str(row["REG_CODE_7"]).encode("utf-8"))
        geom = row.geometry
        if geom is not None:
            digest.update(geom.wkb)
    return digest.hexdigest()


def write_ibra_snapshot(root: Path, query: IbraQuery, gdf: gpd.GeoDataFrame) -> Path:
    snapshot_dir = root / "data" / "raw" / "ibra_snapshot"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_utc": _now_utc(),
        "service_metadata": fetch_service_metadata(),
        "layer_metadata": fetch_layer_metadata(query.layer),
        "query": {
            "layer": query.layer,
            "where": query.where,
            "out_fields": query.out_fields,
            "out_sr": query.out_sr,
            "chunk_size": query.chunk_size,
        },
        "feature_count": int(len(gdf)),
        "ibra_hash_sha256": _hash_geometries(gdf[["REG_CODE_7", "geometry"]].copy()),
    }
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    snapshot_path = snapshot_dir / f"ibra_snapshot_{stamp}.json"
    snapshot_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return snapshot_path


def process_ibra(root: Path | None = None) -> gpd.GeoDataFrame:
    query = IbraQuery(layer=IBRA_REGIONS_LAYER, out_sr=4326)
    gdf = fetch_gdf(query)
    if gdf.empty:
        raise RuntimeError("IBRA query returned no features.")

    if root is not None:
        write_ibra_snapshot(root, query, gdf)

    gdf = gdf.copy()
    if "REG_CODE_7" not in gdf.columns or "REG_NAME_7" not in gdf.columns:
        raise RuntimeError("IBRA features missing expected REG_CODE_7/REG_NAME_7 fields.")

    return gdf


def write_outputs(gdf: gpd.GeoDataFrame, root: Path) -> Path:
    out_path = root / IBRA_GPKG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(out_path, driver="GPKG")
    return out_path


def main() -> int:
    root = find_repo_root()
    gdf = process_ibra(root)
    write_outputs(gdf, root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

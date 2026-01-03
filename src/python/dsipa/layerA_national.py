"""National Layer A metric computation (WP0.9)."""

from __future__ import annotations

import argparse
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from shapely.geometry import GeometryCollection, Point
try:
    from shapely.errors import GEOSException
except Exception:  # pragma: no cover
    GEOSException = Exception
from shapely import wkb

from dsipa.landmask import download_landmask
from dsipa.manifest import build_manifest, write_manifest
from dsipa.nightlights import CORE_YEARS, download_year
from dsipa.paths import find_repo_root
from dsipa.schema import (
    EDGE_PROFILES_NATIONAL_CSV,
    PA_GEOMETRIES_GPKG,
    PA_BUFFER_VALIDITY_CSV,
    RADIANCE_BUFFERS_NATIONAL_CSV,
    SCHEMA_SLUG,
    SCHEMA_VERSION,
)
from dsipa.triad import CITY_POINTS, RING_BINS_KM

try:
    from shapely import make_valid
except ImportError:  # pragma: no cover
    from shapely.validation import make_valid  # type: ignore

BUFFER_DISTANCES_KM = (1.0, 5.0)
MIN_VALID_PIXELS = 10
BUFFER_TYPES = ("raw", "land", "land_unprotected")
PRIMARY_BUFFER_TYPE = "land_unprotected"
LANDMASK_DIR = "data/raw/ne_110m_land"
LAND_UNION_CACHE = "data/processed/cache/land_union_ne_110m.wkb"
PA_UNION_CACHE = f"data/processed/cache/pa_union_v{SCHEMA_SLUG}.wkb"
LAND_UNPROTECTED_CACHE = f"data/processed/cache/land_unprotected_union_v{SCHEMA_SLUG}.wkb"
BUFFER_QUAD_SEGS = 1
GEOM_SIMPLIFY_TOLERANCE_M = 500.0

REPORT_PATH = "analysis/reports/national_layerA_coverage_and_sanity.md"
PLOT_PATH = "analysis/reports/national_layerA_distributions.png"


@dataclass(frozen=True)
class RasterMeta:
    year: int
    path: Path
    nodata: float | None
    dtype: str
    scale: float | None
    offset: float | None


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _apply_scale(values: np.ndarray, scale: float | None, offset: float | None) -> np.ndarray:
    scale_value = 1.0 if scale is None else float(scale)
    offset_value = 0.0 if offset is None else float(offset)
    return values * scale_value + offset_value


def _stats_for_geom(
    dataset: rasterio.DatasetReader,
    geom,
    *,
    scale: float | None,
    offset: float | None,
    min_valid_pixels: int,
) -> dict[str, float]:
    if geom is None or geom.is_empty:
        return {
            "pixel_count": 0,
            "valid_pixel_count": 0,
            "valid_fraction": 0.0,
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
            "frac_gt0": np.nan,
            "p95": np.nan,
        }

    nodata = dataset.nodata
    try:
        data, _ = mask(dataset, [geom], crop=True, filled=True, nodata=nodata)
    except Exception:
        return {
            "pixel_count": 0,
            "valid_pixel_count": 0,
            "valid_fraction": 0.0,
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
            "frac_gt0": np.nan,
            "p95": np.nan,
        }
    band = data[0]

    mask_invalid = np.isnan(band)
    if nodata is not None:
        mask_invalid |= band == nodata
    mask_invalid |= band < 0

    pixel_count = int(band.size)
    valid = band[~mask_invalid].astype("float64")
    valid_count = int(valid.size)

    if valid_count < min_valid_pixels:
        return {
            "pixel_count": pixel_count,
            "valid_pixel_count": valid_count,
            "valid_fraction": float(valid_count / pixel_count) if pixel_count else 0.0,
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
            "frac_gt0": np.nan,
            "p95": np.nan,
        }

    valid = _apply_scale(valid, scale, offset)
    return {
        "pixel_count": pixel_count,
        "valid_pixel_count": valid_count,
        "valid_fraction": float(valid_count / pixel_count) if pixel_count else 0.0,
        "mean": float(np.mean(valid)),
        "median": float(np.median(valid)),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
        "std": float(np.std(valid)),
        "frac_gt0": float(np.mean(valid > 0)),
        "p95": float(np.quantile(valid, 0.95)),
    }


def _raster_meta(dataset: rasterio.DatasetReader, year: int, path: Path) -> RasterMeta:
    scale = dataset.scales[0] if dataset.scales else None
    offset = dataset.offsets[0] if dataset.offsets else None
    return RasterMeta(
        year=year,
        path=path,
        nodata=dataset.nodata,
        dtype=str(dataset.dtypes[0]),
        scale=scale,
        offset=offset,
    )


def _safe_geom(geom):
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        geom = make_valid(geom)
    return geom


def _safe_difference(a, b):
    if a is None or a.is_empty:
        return a
    if b is None or b.is_empty:
        return a
    try:
        return a.difference(b)
    except Exception:
        return make_valid(a).difference(make_valid(b))


def _safe_intersection(a, b):
    if a is None or a.is_empty:
        return a
    if b is None or b.is_empty:
        return b
    try:
        return a.intersection(b)
    except Exception:
        return make_valid(a).intersection(make_valid(b))


def _safe_intersection_series(series: gpd.GeoSeries, other) -> gpd.GeoSeries:
    try:
        return series.intersection(other)
    except GEOSException:
        return gpd.GeoSeries(
            [_safe_intersection(geom, other) for geom in series],
            index=series.index,
            crs=series.crs,
        )


def _chunk_records(records: list[dict], chunk_size: int) -> Iterable[list[dict]]:
    for i in range(0, len(records), chunk_size):
        yield records[i : i + chunk_size]


def _load_landmask_union(root: Path):
    cache_path = root / LAND_UNION_CACHE
    if cache_path.exists():
        return wkb.loads(cache_path.read_bytes())
    land_dir = root / LANDMASK_DIR
    land_path = download_landmask(land_dir)
    land_gdf = gpd.read_file(land_path)
    if land_gdf.empty:
        raise RuntimeError(f"Landmask data empty at {land_path}")
    land_gdf = land_gdf.to_crs("EPSG:3577")
    land_gdf["geometry"] = land_gdf.geometry.apply(_safe_geom)
    land_gdf = land_gdf[~land_gdf.geometry.is_empty]
    try:
        union_geom = land_gdf.geometry.union_all()
    except AttributeError:  # pragma: no cover
        union_geom = land_gdf.geometry.unary_union
    land_union = _safe_geom(union_geom)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(wkb.dumps(land_union))
    return land_union


def _load_pa_union(root: Path, pa_gdf: gpd.GeoDataFrame):
    cache_path = root / PA_UNION_CACHE
    if cache_path.exists():
        return wkb.loads(cache_path.read_bytes())
    try:
        union_geom = pa_gdf.geometry.union_all()
    except AttributeError:  # pragma: no cover
        union_geom = pa_gdf.geometry.unary_union
    union_geom = _safe_geom(union_geom)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(wkb.dumps(union_geom))
    return union_geom


def _load_land_unprotected_union(
    root: Path,
    land_union,
    pa_union,
):
    if land_union is None:
        return None
    if pa_union is None:
        return land_union
    cache_path = root / LAND_UNPROTECTED_CACHE
    if cache_path.exists():
        cached = wkb.loads(cache_path.read_bytes())
        return _safe_geom(cached)
    land_unprotected = _safe_difference(land_union, pa_union)
    land_unprotected = _safe_geom(land_unprotected)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(wkb.dumps(land_unprotected))
    return land_unprotected


def _compute_chunk(
    records: list[dict],
    *,
    raster_path: Path,
    scale: float | None,
    offset: float | None,
    min_valid_pixels: int,
) -> list[dict]:
    results: list[dict] = []
    with rasterio.open(raster_path) as dataset:
        for record in records:
            geom = wkb.loads(record["geometry"])
            stats = _stats_for_geom(
                dataset,
                geom,
                scale=scale,
                offset=offset,
                min_valid_pixels=min_valid_pixels,
            )
            out = {k: v for k, v in record.items() if k != "geometry"}
            out.update(
                {
                    "schema_version": SCHEMA_VERSION,
                    "scale_metadata": scale,
                    "offset_metadata": offset,
                }
            )
            out.update(stats)
            results.append(out)
    return results


def _compute_records(
    records: list[dict],
    *,
    raster_path: Path,
    scale: float | None,
    offset: float | None,
    min_valid_pixels: int,
    workers: int,
    chunk_size: int,
) -> list[dict]:
    if workers <= 1:
        return _compute_chunk(
            records,
            raster_path=raster_path,
            scale=scale,
            offset=offset,
            min_valid_pixels=min_valid_pixels,
        )

    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                _compute_chunk,
                chunk,
                raster_path=raster_path,
                scale=scale,
                offset=offset,
                min_valid_pixels=min_valid_pixels,
            )
            for chunk in _chunk_records(records, chunk_size)
        ]
        for future in as_completed(futures):
            results.extend(future.result())
    return results


def _build_city_gdf() -> gpd.GeoDataFrame:
    rows = [(name, Point(lon, lat)) for name, lon, lat in CITY_POINTS]
    return gpd.GeoDataFrame(rows, columns=["city", "geometry"], crs="EPSG:4326").to_crs("EPSG:3577")


def _attach_city_distance(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    gdf = gdf.to_crs("EPSG:3577").copy()
    gdf["centroid"] = gdf.geometry.centroid
    cities = _build_city_gdf()
    city_geoms = cities.geometry.to_list()
    city_names = cities["city"].to_list()
    nearest_city = []
    nearest_dist_km = []
    for geom in gdf["centroid"]:
        distances = [geom.distance(city_geom) for city_geom in city_geoms]
        idx = int(np.argmin(distances))
        nearest_city.append(city_names[idx])
        nearest_dist_km.append(distances[idx] / 1000.0)
    gdf["nearest_city"] = nearest_city
    gdf["distance_km"] = nearest_dist_km
    return gdf[["pa_id", "nearest_city", "distance_km"]]


def build_buffers(
    pa_gdf: gpd.GeoDataFrame,
    *,
    land_union,
    pa_union,
    land_unprotected_union=None,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    if land_unprotected_union is None:
        if land_union is None:
            land_unprotected_union = None
        elif pa_union is None:
            land_unprotected_union = land_union
        else:
            land_unprotected_union = _safe_difference(land_union, pa_union)

    base = pa_gdf[["pa_id", "geometry"]].copy()
    base["geometry"] = base.geometry.apply(_safe_geom).simplify(
        GEOM_SIMPLIFY_TOLERANCE_M, preserve_topology=True
    )
    base = base[~base.geometry.is_empty]

    buffer_frames: list[gpd.GeoDataFrame] = []
    validity_frames: list[pd.DataFrame] = []

    for dist_km in BUFFER_DISTANCES_KM:
        buffer_geom = base.geometry.buffer(dist_km * 1000.0, resolution=BUFFER_QUAD_SEGS)
        outside = buffer_geom.difference(base.geometry)
        valid_mask = ~outside.is_empty
        if not valid_mask.any():
            continue
        outside = outside[valid_mask]
        pa_ids = base.loc[valid_mask, "pa_id"].to_numpy()

        raw_area = outside.area.to_numpy()
        if land_union is not None:
            land_geom = _safe_intersection_series(outside, land_union)
            land_area = land_geom.area.to_numpy()
        else:
            land_geom = None
            land_area = np.zeros_like(raw_area)

        if land_unprotected_union is not None:
            land_unprotected = _safe_intersection_series(outside, land_unprotected_union)
            land_unprotected_area = land_unprotected.area.to_numpy()
        else:
            land_unprotected = land_geom
            land_unprotected_area = land_area

        overlap_area = np.maximum(land_area - land_unprotected_area, 0.0)
        effective_land_area = land_unprotected_area

        land_fraction = np.where(raw_area > 0, land_area / raw_area, 0.0)
        protected_overlap_fraction = np.where(raw_area > 0, overlap_area / raw_area, 0.0)
        land_fraction = np.clip(land_fraction, 0.0, 1.0)
        protected_overlap_fraction = np.clip(protected_overlap_fraction, 0.0, 1.0)

        validity_frames.append(
            pd.DataFrame(
                {
                    "pa_id": pa_ids,
                    "buffer_km": float(dist_km),
                    "buffer_area_km2": raw_area / 1_000_000.0,
                    "land_area_km2": land_area / 1_000_000.0,
                    "protected_overlap_km2": overlap_area / 1_000_000.0,
                    "effective_land_area_km2": effective_land_area / 1_000_000.0,
                    "land_fraction": land_fraction,
                    "protected_overlap_fraction": protected_overlap_fraction,
                }
            )
        )

        buffer_frames.append(
            gpd.GeoDataFrame(
                {
                    "pa_id": pa_ids,
                    "buffer_km": float(dist_km),
                    "buffer_type": "raw",
                    "geometry": outside,
                },
                crs=pa_gdf.crs,
            )
        )

        if land_geom is not None:
            land_mask = ~land_geom.is_empty
            if land_mask.any():
                buffer_frames.append(
                    gpd.GeoDataFrame(
                        {
                            "pa_id": pa_ids[land_mask],
                            "buffer_km": float(dist_km),
                            "buffer_type": "land",
                            "geometry": land_geom[land_mask],
                        },
                        crs=pa_gdf.crs,
                    )
                )
            if land_unprotected is not None:
                land_unprotected_mask = ~land_unprotected.is_empty
                if land_unprotected_mask.any():
                    buffer_frames.append(
                        gpd.GeoDataFrame(
                            {
                                "pa_id": pa_ids[land_unprotected_mask],
                                "buffer_km": float(dist_km),
                                "buffer_type": "land_unprotected",
                                "geometry": land_unprotected[land_unprotected_mask],
                            },
                            crs=pa_gdf.crs,
                        )
                    )

    buffers = (
        gpd.GeoDataFrame(pd.concat(buffer_frames, ignore_index=True), crs=pa_gdf.crs)
        if buffer_frames
        else gpd.GeoDataFrame(columns=["pa_id", "buffer_km", "buffer_type", "geometry"], crs=pa_gdf.crs)
    )
    validity = (
        pd.concat(validity_frames, ignore_index=True)
        if validity_frames
        else pd.DataFrame(
            columns=[
                "pa_id",
                "buffer_km",
                "buffer_area_km2",
                "land_area_km2",
                "protected_overlap_km2",
                "effective_land_area_km2",
                "land_fraction",
                "protected_overlap_fraction",
            ]
        )
    )

    return buffers, validity


def build_rings(pa_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    base = pa_gdf[["pa_id", "geometry"]].copy()
    base["geometry"] = base.geometry.apply(_safe_geom)
    base = base[~base.geometry.is_empty]
    area_km2 = base.geometry.area.to_numpy() / 1_000_000.0

    ring_frames: list[gpd.GeoDataFrame] = []
    for idx, (inner_km, outer_km) in enumerate(RING_BINS_KM):
        inner_threshold = np.pi * (inner_km**2)
        if inner_km == 0:
            inner_geom = base.geometry
        else:
            inner_geom = gpd.GeoSeries(
                [GeometryCollection()] * len(base), index=base.index, crs=pa_gdf.crs
            )
            inner_mask = area_km2 >= inner_threshold
            if inner_mask.any():
                inner_geom.loc[inner_mask] = base.geometry.loc[inner_mask].buffer(
                    -inner_km * 1000.0, resolution=BUFFER_QUAD_SEGS
                )

        ring_geom = inner_geom.copy()
        outer_threshold = np.pi * (outer_km**2)
        outer_mask = area_km2 >= outer_threshold
        if outer_mask.any():
            outer_geom = base.geometry.loc[outer_mask].buffer(
                -outer_km * 1000.0, resolution=BUFFER_QUAD_SEGS
            )
            ring_geom.loc[outer_mask] = inner_geom.loc[outer_mask].difference(outer_geom)

        ring_frames.append(
            gpd.GeoDataFrame(
                {
                    "pa_id": base["pa_id"].to_numpy(),
                    "ring_index": idx,
                    "ring_inner_km": float(inner_km),
                    "ring_outer_km": float(outer_km),
                    "geometry": ring_geom,
                },
                crs=pa_gdf.crs,
            )
        )

    return gpd.GeoDataFrame(pd.concat(ring_frames, ignore_index=True), crs=pa_gdf.crs)


def _load_pa_geoms(root: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)
    if gdf.empty:
        raise RuntimeError("PA geometry file is empty.")
    return gdf


def _filter_pas(
    gdf: gpd.GeoDataFrame,
    *,
    states: list[str] | None,
    pa_limit: int | None,
    sample: str,
    seed: int,
) -> gpd.GeoDataFrame:
    filtered = gdf.copy()
    if states:
        state_upper = [state.strip().upper() for state in states if state.strip()]
        if "STATE" not in filtered.columns:
            raise ValueError("STATE column missing from PA geometries; cannot filter by state.")
        filtered = filtered[filtered["STATE"].isin(state_upper)]
    if pa_limit is not None and pa_limit > 0 and len(filtered) > pa_limit:
        if sample == "largest":
            filtered = filtered.sort_values("area_km2", ascending=False).head(pa_limit)
        elif sample == "random":
            filtered = filtered.sample(n=pa_limit, random_state=seed)
        else:
            filtered = filtered.sort_values("pa_id").head(pa_limit)
    return filtered


def summarise_buffers(
    years: Iterable[int],
    pa_gdf: gpd.GeoDataFrame,
    raw_dir: Path,
    min_valid_pixels: int,
    *,
    workers: int,
    chunk_size: int,
    land_union=None,
    pa_union=None,
) -> tuple[pd.DataFrame, pd.DataFrame, list[RasterMeta]]:
    records: list[dict] = []
    meta_records: list[RasterMeta] = []

    years = list(years)
    inside = pa_gdf[["pa_id", "geometry"]].copy()
    if land_union is None:
        land_union = _load_landmask_union(find_repo_root())
    if pa_union is None:
        pa_union = _load_pa_union(find_repo_root(), pa_gdf)
    land_unprotected_union = _load_land_unprotected_union(find_repo_root(), land_union, pa_union)
    buffers, validity_df = build_buffers(
        pa_gdf,
        land_union=land_union,
        pa_union=pa_union,
        land_unprotected_union=land_unprotected_union,
    )

    sample_raster = download_year(years[0], raw_dir)
    with rasterio.open(sample_raster.path) as dataset:
        target_crs = dataset.crs

    inside_crs = inside.to_crs(target_crs)
    buffers_crs = buffers.to_crs(target_crs)

    inside_base = [
        {
            "pa_id": row["pa_id"],
            "zone": "inside",
            "buffer_km": np.nan,
            "buffer_type": "inside",
            "geometry": row.geometry.wkb,
        }
        for _, row in inside_crs.iterrows()
    ]
    buffer_base = [
        {
            "pa_id": row["pa_id"],
            "zone": "buffer",
            "buffer_km": float(row["buffer_km"]),
            "buffer_type": row["buffer_type"],
            "geometry": row.geometry.wkb,
        }
        for _, row in buffers_crs.iterrows()
    ]

    for year in years:
        raster = download_year(year, raw_dir)
        with rasterio.open(raster.path) as dataset:
            meta = _raster_meta(dataset, year, raster.path)
        meta_records.append(meta)

        year_records = [
            {**rec, "year": year} for rec in inside_base + buffer_base
        ]
        results = _compute_records(
            year_records,
            raster_path=raster.path,
            scale=meta.scale,
            offset=meta.offset,
            min_valid_pixels=min_valid_pixels,
            workers=workers,
            chunk_size=chunk_size,
        )
        records.extend(results)

    return pd.DataFrame(records), validity_df, meta_records


def summarise_rings(
    years: Iterable[int],
    pa_gdf: gpd.GeoDataFrame,
    raw_dir: Path,
    min_valid_pixels: int,
    *,
    workers: int,
    chunk_size: int,
) -> tuple[pd.DataFrame, list[RasterMeta]]:
    records: list[dict] = []
    meta_records: list[RasterMeta] = []

    years = list(years)
    rings = build_rings(pa_gdf)

    sample_raster = download_year(years[0], raw_dir)
    with rasterio.open(sample_raster.path) as dataset:
        target_crs = dataset.crs

    rings_crs = rings.to_crs(target_crs)
    rings_base = [
        {
            "pa_id": row["pa_id"],
            "ring_index": int(row["ring_index"]),
            "ring_inner_km": float(row["ring_inner_km"]),
            "ring_outer_km": float(row["ring_outer_km"]),
            "geometry": row.geometry.wkb,
        }
        for _, row in rings_crs.iterrows()
    ]

    for year in years:
        raster = download_year(year, raw_dir)
        with rasterio.open(raster.path) as dataset:
            meta = _raster_meta(dataset, year, raster.path)
        meta_records.append(meta)

        year_records = [{**rec, "year": year} for rec in rings_base]
        results = _compute_records(
            year_records,
            raster_path=raster.path,
            scale=meta.scale,
            offset=meta.offset,
            min_valid_pixels=min_valid_pixels,
            workers=workers,
            chunk_size=chunk_size,
        )
        records.extend(results)

    return pd.DataFrame(records), meta_records


def _anchor_summary(df_inside: pd.DataFrame, pa_meta: pd.DataFrame, years: Iterable[int]) -> list[str]:
    lines = ["## Anchor checks (inside mean)", ""]
    merged = df_inside.merge(pa_meta, on="pa_id", how="left")
    for year in years:
        subset = merged[merged["year"] == year]
        urban = subset[subset["distance_km"] <= 20.0]
        remote = subset[subset["distance_km"] >= 300.0]
        lines.append(f"Year {year}:")
        lines.append(
            f"- Urban-adjacent (<=20 km): n={len(urban)}, median mean={urban['mean'].median():.3f}"
        )
        lines.append(
            f"- Remote (>=300 km): n={len(remote)}, median mean={remote['mean'].median():.3f}"
        )
        city_summary = (
            subset.groupby("nearest_city")["mean"]
            .median()
            .sort_values(ascending=False)
            .head(3)
        )
        lines.append(
            "- Top city medians: "
            + ", ".join(f"{idx}={val:.3f}" for idx, val in city_summary.items())
        )
        lines.append("")
    return lines


def _inside_vs_buffer_check(df_buffers: pd.DataFrame) -> list[str]:
    lines = ["## Inside vs buffer sanity", ""]
    inside = df_buffers[df_buffers["zone"] == "inside"]
    buffer1 = df_buffers[
        (df_buffers["zone"] == "buffer")
        & (df_buffers["buffer_km"] == 1.0)
        & (df_buffers["buffer_type"] == PRIMARY_BUFFER_TYPE)
    ]
    merged = inside.merge(
        buffer1,
        on=["pa_id", "year"],
        suffixes=("_inside", "_buffer1"),
    )
    merged = merged.dropna(subset=["mean_inside", "mean_buffer1"])
    if merged.empty:
        lines.append("No comparable inside/buffer rows after filtering.")
        return lines
    frac = (merged["mean_buffer1"] > merged["mean_inside"]).mean()
    lines.append(
        f"Fraction with buffer1 mean > inside mean ({PRIMARY_BUFFER_TYPE}): {frac:.3f} (n={len(merged)})"
    )
    return lines


def _write_plot(df: pd.DataFrame, plot_path: Path) -> None:
    import matplotlib.pyplot as plt

    plot_path.parent.mkdir(parents=True, exist_ok=True)
    inside = df[df["zone"] == "inside"]
    years = [2013, 2018, 2024]
    fig, axes = plt.subplots(1, len(years), figsize=(12, 4), sharey=True)
    if len(years) == 1:
        axes = [axes]
    for ax, year in zip(axes, years):
        subset = inside[inside["year"] == year]
        values = subset["mean"].dropna()
        ax.hist(values, bins=40, color="#4C72B0", alpha=0.8)
        ax.set_title(str(year))
        ax.set_xlabel("Mean radiance (scaled)")
    axes[0].set_ylabel("PA count")
    fig.tight_layout()
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)


def _buffer_validity_summary(validity_df: pd.DataFrame) -> list[str]:
    if validity_df.empty:
        return ["## Buffer validity summary", "", "No buffer validity records available.", ""]
    summary = (
        validity_df.groupby("buffer_km")[
            ["land_fraction", "protected_overlap_fraction", "effective_land_area_km2"]
        ]
        .median()
        .reset_index()
    )
    low_land = (validity_df["land_fraction"] < 0.5).mean()
    high_overlap = (validity_df["protected_overlap_fraction"] > 0.25).mean()
    lines = [
        "## Buffer validity summary",
        "",
        summary.round(3).to_string(index=False),
        "",
        f"Fraction of buffers with land_fraction < 0.5: {low_land:.3f}",
        f"Fraction of buffers with protected_overlap_fraction > 0.25: {high_overlap:.3f}",
        "",
    ]
    return lines


def write_report(
    *,
    radiance_df: pd.DataFrame,
    ring_df: pd.DataFrame,
    meta_records: Iterable[RasterMeta],
    pa_meta: pd.DataFrame,
    report_path: Path,
    plot_path: Path,
    min_valid_pixels: int,
    buffer_validity: pd.DataFrame,
    subset_note: str | None = None,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    meta_by_year = {}
    for item in meta_records:
        meta_by_year.setdefault(item.year, item)
    meta_lines = [
        f"- {item.year}: dtype={item.dtype}, nodata={item.nodata}, scale={item.scale}, offset={item.offset}"
        for item in meta_by_year.values()
    ]

    coverage_df = radiance_df.copy()
    coverage_df["buffer_km"] = coverage_df["buffer_km"].fillna(-1)
    coverage = (
        coverage_df.assign(valid_ok=coverage_df["valid_pixel_count"] >= min_valid_pixels)
        .groupby(["year", "zone", "buffer_type", "buffer_km"])["valid_ok"]
        .mean()
        .reset_index()
    )

    ring_coverage = (
        ring_df.assign(valid_ok=ring_df["valid_pixel_count"] >= min_valid_pixels)
        .groupby(["year", "ring_index"])["valid_ok"]
        .mean()
        .reset_index()
    )

    lines = [
        "# National Layer A coverage and sanity report",
        "",
        f"Generated: {_now_utc()}",
        "",
        "## Raster metadata (per year)",
        *meta_lines,
        "",
    ]
    if subset_note:
        lines.extend(
            [
                "## Subset selection",
                "",
                subset_note,
                "",
            ]
        )

    lines.extend(
        [
        f"Minimum valid pixels per zone: {min_valid_pixels}",
        "",
        "## Coverage by zone (fraction with valid pixels)",
        "",
        "Note: buffer_km=-1 denotes inside-zone rows.",
        coverage.to_string(index=False),
        "",
        *_buffer_validity_summary(buffer_validity),
        "## Coverage by ring (fraction with valid pixels)",
        "",
        ring_coverage.to_string(index=False),
        "",
        ]
    )

    lines.extend(_anchor_summary(radiance_df[radiance_df["zone"] == "inside"], pa_meta, [2013, 2018, 2024]))
    lines.append("")
    lines.extend(_inside_vs_buffer_check(radiance_df))
    lines.append("")
    lines.append(f"Plot: {plot_path.name}")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_outputs(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def write_buffer_validity(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df_out = df.copy()
    df_out["schema_version"] = SCHEMA_VERSION
    df_out.to_csv(path, index=False)
    return path


def _resolve_output_path(root: Path, output_dir: str | None, default_path: str) -> Path:
    if output_dir is None:
        return root / default_path
    out_root = root / output_dir
    out_root.mkdir(parents=True, exist_ok=True)
    return out_root / Path(default_path).name


def write_artefact(
    *,
    report_path: Path,
    plot_path: Path,
    radiance_path: Path,
    ring_path: Path,
    buffer_validity_path: Path,
    root: Path,
) -> Path:
    artefact_dir = root / "artefacts" / "wp0_9_layerA_national"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(plot_path, artefact_dir / plot_path.name)
    shutil.copyfile(radiance_path, artefact_dir / radiance_path.name)
    shutil.copyfile(ring_path, artefact_dir / ring_path.name)
    shutil.copyfile(buffer_validity_path, artefact_dir / buffer_validity_path.name)

    manifest = build_manifest(
        run_id="wp0_9_layerA_national",
        wp="WP0.9",
        root=root,
        outputs=[
            report_path.name,
            plot_path.name,
            radiance_path.name,
            ring_path.name,
            buffer_validity_path.name,
        ],
        inputs=[PA_GEOMETRIES_GPKG, "data/raw/nightlights_zenodo_v0_4", LANDMASK_DIR],
        notes="WP0.9 national Layer A outputs",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.9 national Layer A artefact. Contains national tables, coverage report, and plot.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compute national Layer A metrics (WP0.9).")
    parser.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=list(CORE_YEARS),
        help="Years to process (default: 2013–2024).",
    )
    parser.add_argument(
        "--min-valid-pixels",
        type=int,
        default=MIN_VALID_PIXELS,
        help="Minimum valid pixels required to compute stats.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, min(4, os.cpu_count() or 1)),
        help="Number of worker processes for zonal stats.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=300,
        help="Records per worker chunk.",
    )
    parser.add_argument(
        "--buffers-only",
        action="store_true",
        help="Only compute inside/buffer summaries.",
    )
    parser.add_argument(
        "--rings-only",
        action="store_true",
        help="Only compute ring summaries.",
    )
    parser.add_argument(
        "--states",
        default=None,
        help="Comma-separated state codes to subset (e.g., TAS,NSW).",
    )
    parser.add_argument(
        "--pa-limit",
        type=int,
        default=None,
        help="Limit number of PAs for quick runs (applied after state filter).",
    )
    parser.add_argument(
        "--pa-sample",
        choices=["largest", "random", "first"],
        default="largest",
        help="Sampling strategy for --pa-limit (default: largest by area).",
    )
    parser.add_argument(
        "--pa-seed",
        type=int,
        default=42,
        help="Random seed for --pa-sample=random.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory for subset runs (writes filenames into this folder).",
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
    raw_dir = root / "data" / "raw" / "nightlights_zenodo_v0_4"

    pa_gdf_all = _load_pa_geoms(root)
    state_list = args.states.split(",") if args.states else None
    pa_gdf = _filter_pas(
        pa_gdf_all,
        states=state_list,
        pa_limit=args.pa_limit,
        sample=args.pa_sample,
        seed=args.pa_seed,
    )
    if pa_gdf.empty:
        raise RuntimeError("PA filter returned zero features.")
    pa_meta = _attach_city_distance(pa_gdf)
    subset_note = None
    if state_list or args.pa_limit:
        subset_note = (
            f"States={state_list or 'all'}; pa_limit={args.pa_limit or 'none'}; "
            f"sample={args.pa_sample}; seed={args.pa_seed}."
        )
    land_union = _load_landmask_union(root)
    pa_union = _load_pa_union(root, pa_gdf_all)

    if args.buffers_only and args.rings_only:
        raise SystemExit("Choose at most one of --buffers-only or --rings-only.")

    radiance_df = pd.DataFrame()
    ring_df = pd.DataFrame()
    buffer_validity_df = pd.DataFrame()
    meta_records: list[RasterMeta] = []

    if not args.rings_only:
        radiance_df, buffer_validity_df, meta_records = summarise_buffers(
            args.years,
            pa_gdf,
            raw_dir,
            args.min_valid_pixels,
            workers=args.workers,
            chunk_size=args.chunk_size,
            land_union=land_union,
            pa_union=pa_union,
        )
        radiance_path = write_outputs(
            radiance_df, _resolve_output_path(root, args.output_dir, RADIANCE_BUFFERS_NATIONAL_CSV)
        )
        buffer_validity_path = write_buffer_validity(
            buffer_validity_df, _resolve_output_path(root, args.output_dir, PA_BUFFER_VALIDITY_CSV)
        )
    else:
        radiance_path = None
        buffer_validity_path = None

    if not args.buffers_only:
        ring_df, ring_meta = summarise_rings(
            args.years,
            pa_gdf,
            raw_dir,
            args.min_valid_pixels,
            workers=args.workers,
            chunk_size=args.chunk_size,
        )
        meta_records.extend(ring_meta)
        ring_path = write_outputs(
            ring_df, _resolve_output_path(root, args.output_dir, EDGE_PROFILES_NATIONAL_CSV)
        )
    else:
        ring_path = None

    if not args.buffers_only and not args.rings_only:
        report_path = _resolve_output_path(root, args.output_dir, REPORT_PATH)
        plot_path = _resolve_output_path(root, args.output_dir, PLOT_PATH)
        _write_plot(radiance_df, plot_path)
        write_report(
            radiance_df=radiance_df,
            ring_df=ring_df,
            meta_records=meta_records,
            pa_meta=pa_meta,
            report_path=report_path,
            plot_path=plot_path,
            min_valid_pixels=args.min_valid_pixels,
            buffer_validity=buffer_validity_df,
            subset_note=subset_note,
        )

        if not args.skip_artefact:
            write_artefact(
                report_path=report_path,
                plot_path=plot_path,
                radiance_path=radiance_path,
                ring_path=ring_path,
                buffer_validity_path=buffer_validity_path,
                root=root,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

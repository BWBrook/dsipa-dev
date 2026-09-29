#!/usr/bin/env python3
"""Acquire and inspect the candidate AIMS Australian land polygon.

This utility is deliberately run-directory scoped.  It does not write to the
repository data tree or replace any accepted DSIPA input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile

import geopandas as gpd
import pyogrio
from shapely.ops import unary_union


SOURCE_URL = (
    "https://nextcloud.eatlas.org.au/s/DcGmpS3F5KZjgAG/download"
    "?path=%2FV1-1%2F&files=Full"
)
ARCHIVE_NAME = "AIMS_Australian_Coastline_50K_2024_v1-1_Full.zip"
EXPECTED_SHA256 = "cdbabe24373863c06eaa5a1e76643ea6aebfafe34abfcd0e188c05de1a60882f"
SHAPEFILE_NAME = "AU_NESP-MaC-3-17_AIMS_Aus-Coastline-50k_2024_V1-1.shp"
SPLIT_SOURCE_URL = (
    "https://nextcloud.eatlas.org.au/s/DcGmpS3F5KZjgAG/download"
    "?path=%2FV1-1%2F&files=Split"
)
SPLIT_ARCHIVE_NAME = "AIMS_Australian_Coastline_50K_2024_v1-1_Split.zip"
SPLIT_EXPECTED_SHA256 = (
    "c6046a756c8ac67f04ae99155265ee04b34d1dcbfa39fb1b0c479f6bb2b6a7cd"
)
SPLIT_SHAPEFILE_NAME = (
    "AU_NESP-MaC-3-17_AIMS_Aus-Coastline-50k_2024_V1-1_split.shp"
)
CHECK_IDS = (
    "WA_39584",  # Henderson, WA
    "WA_05225",  # Torndirrup, WA
    "NSW_LHI",  # Lord Howe Island
    "CWTH_05",  # Christmas Island
    "CWTH_07",  # Norfolk Island Botanic Gardens
    "CWTH_08",  # Norfolk Island (Mt Pitt)
    "CWTH_09",  # Phillip Island near Norfolk Island
    "CWTH_10",  # Pulu Keeling, Cocos (Keeling) Islands
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    destination = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            if destination not in target.parents and target != destination:
                raise ValueError(f"Unsafe archive member: {member.filename}")
        bundle.extractall(destination)


def acquire_archive(
    run_dir: Path,
    *,
    source_url: str,
    archive_name: str,
    expected_sha256: str,
    extract_directory: str,
    shapefile_name: str,
) -> Path:
    archive = run_dir / archive_name
    if not archive.exists():
        with urllib.request.urlopen(source_url, timeout=120) as response:
            with archive.open("wb") as output:
                shutil.copyfileobj(response, output)
    observed = sha256_file(archive)
    if observed != expected_sha256:
        raise ValueError(
            "AIMS archive SHA-256 mismatch: "
            f"expected {expected_sha256}, got {observed}"
        )
    extracted = run_dir / extract_directory
    if not extracted.exists():
        safe_extract(archive, extracted)
    matches = list(extracted.rglob(shapefile_name))
    if len(matches) != 1:
        raise ValueError(f"Expected one {shapefile_name}, found {len(matches)}")
    return matches[0]


def acquire(run_dir: Path) -> tuple[Path, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    full_path = acquire_archive(
        run_dir,
        source_url=SOURCE_URL,
        archive_name=ARCHIVE_NAME,
        expected_sha256=EXPECTED_SHA256,
        extract_directory="Full",
        shapefile_name=SHAPEFILE_NAME,
    )
    split_path = acquire_archive(
        run_dir,
        source_url=SPLIT_SOURCE_URL,
        archive_name=SPLIT_ARCHIVE_NAME,
        expected_sha256=SPLIT_EXPECTED_SHA256,
        extract_directory="Split",
        shapefile_name=SPLIT_SHAPEFILE_NAME,
    )
    (run_dir / "SHA256SUMS").write_text(
        f"{EXPECTED_SHA256}  {ARCHIVE_NAME}\n"
        f"{SPLIT_EXPECTED_SHA256}  {SPLIT_ARCHIVE_NAME}\n"
    )
    return full_path, split_path


def validate(coast_path: Path, pa_path: Path, run_dir: Path) -> None:
    coast_info = pyogrio.read_info(coast_path)
    coast_crs = coast_info["crs"]
    pas = gpd.read_file(pa_path)
    checks = pas.loc[pas["pa_id"].isin(CHECK_IDS)].copy()
    missing = sorted(set(CHECK_IDS) - set(checks["pa_id"]))
    if missing:
        raise ValueError(f"Protected-area checks missing from input: {missing}")

    # Equal-area geometry supports comparable overlap areas across mainland and
    # external-island checks.  Nearest distances are screening diagnostics only.
    equal_area = "EPSG:6933"
    checks_coast_crs = checks.to_crs(coast_crs)
    out = checks.drop(columns="geometry").copy()
    reserve_areas: list[float] = []
    intersection_areas: list[float] = []
    representative_on_land: list[bool] = []
    representative_distances: list[float] = []
    for reserve_source in checks_coast_crs.geometry:
        candidates = gpd.read_file(coast_path, bbox=tuple(reserve_source.bounds))
        reserve = gpd.GeoSeries([reserve_source], crs=coast_crs).to_crs(
            equal_area
        ).iloc[0]
        if len(candidates):
            candidates_ea = candidates.geometry.to_crs(
                equal_area
            )
            candidate_union = unary_union(
                candidates_ea.to_numpy()
            )
            intersection_area = reserve.intersection(candidate_union).area
        else:
            candidate_union = None
            intersection_area = 0.0
        representative = reserve.representative_point()
        if candidate_union is not None and representative.within(candidate_union):
            on_land = True
            distance = 0.0
        else:
            on_land = False
            distance = (
                representative.distance(candidate_union)
                if candidate_union
                else float("nan")
            )
        reserve_areas.append(reserve.area)
        intersection_areas.append(intersection_area)
        representative_on_land.append(on_land)
        representative_distances.append(distance)

    out["reserve_area_km2_recomputed"] = [x / 1_000_000 for x in reserve_areas]
    out["intersection_area_km2"] = [x / 1_000_000 for x in intersection_areas]
    out["land_overlap_fraction"] = [
        overlap / area for overlap, area in zip(intersection_areas, reserve_areas)
    ]
    out["representative_point_on_land"] = representative_on_land
    out["representative_point_distance_to_land_m"] = representative_distances
    out = out.sort_values("pa_id")
    out.to_csv(run_dir / "named_reserve_coverage.csv", index=False)

    summary = {
        "source_url": SPLIT_SOURCE_URL,
        "archive_sha256": SPLIT_EXPECTED_SHA256,
        "source_path": str(coast_path),
        "source_crs": str(coast_crs),
        "feature_count": int(coast_info["features"]),
        "geometry_type": str(coast_info["geometry_type"]),
        "bounds_source_crs": [float(value) for value in coast_info["total_bounds"]],
        "protected_area_source": str(pa_path),
        "check_ids": list(CHECK_IDS),
    }
    (run_dir / "validation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )


def screen_national_coverage(coast_path: Path, pa_path: Path, run_dir: Path) -> None:
    """List accepted non-Antarctic PAs with absent or suspect land coverage."""
    coast = gpd.read_file(coast_path)[["geometry"]]
    pas = gpd.read_file(pa_path)
    pas_source = pas.to_crs(coast.crs)
    representative_points = gpd.GeoDataFrame(
        pas_source.drop(columns="geometry"),
        geometry=pas_source.geometry.representative_point(),
        crs=coast.crs,
    )
    # Retain sub-Antarctic islands (e.g. Macquarie or Heard, if present) while
    # excluding CAPAD Antarctic Specially Protected/Managed Areas.
    non_antarctic = representative_points.geometry.y > -60
    pas_source = pas_source.loc[non_antarctic].copy()
    representative_points = representative_points.loc[non_antarctic].copy()

    intersecting = gpd.sjoin(
        pas_source[["pa_id", "geometry"]], coast, predicate="intersects", how="inner"
    )
    on_land = gpd.sjoin(
        representative_points[["pa_id", "geometry"]],
        coast,
        predicate="within",
        how="inner",
    )
    intersecting_ids = set(intersecting["pa_id"])
    on_land_ids = set(on_land["pa_id"])
    coverage = representative_points.drop(columns="geometry").copy()
    coverage["representative_longitude"] = representative_points.geometry.x
    coverage["representative_latitude"] = representative_points.geometry.y
    coverage["intersects_source_land"] = coverage["pa_id"].isin(intersecting_ids)
    coverage["representative_point_on_source_land"] = coverage["pa_id"].isin(
        on_land_ids
    )
    coverage = coverage.sort_values("pa_id")
    coverage.to_csv(run_dir / "national_pa_land_coverage_screen.csv", index=False)
    gaps = coverage.loc[
        ~coverage["intersects_source_land"]
        | ~coverage["representative_point_on_source_land"]
    ].copy()
    gaps.to_csv(run_dir / "coverage_gap_ids.csv", index=False)
    zero_overlap = coverage.loc[~coverage["intersects_source_land"]].copy()
    zero_overlap.to_csv(run_dir / "zero_land_overlap_ids.csv", index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--pa-gpkg", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _, split_path = acquire(args.run_dir)
    validate(split_path, args.pa_gpkg, args.run_dir)
    screen_national_coverage(split_path, args.pa_gpkg, args.run_dir)


if __name__ == "__main__":
    main()

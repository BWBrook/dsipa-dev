"""Smoke-test triad selection and QA harness (WP0.4)."""

from __future__ import annotations

import argparse
import json
import math
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point

from dsipa.capad import CapadQuery, fetch_gdf
from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root

try:
    from shapely import make_valid
except ImportError:  # pragma: no cover
    from shapely.validation import make_valid  # type: ignore

SCHEMA_VERSION = "0.1.0"
TARGET_CRS = "EPSG:3577"  # GDA94 / Australian Albers
BUFFER_DISTANCES_KM = [1, 5]
RING_BINS_KM = [(0, 1), (1, 5), (5, 10)]
MIN_AREA_KM2 = 5.0
URBAN_MAX_KM = 20.0
PERI_RANGE_KM = (50.0, 150.0)
PERI_TARGET_KM = 100.0
EXCLUDE_STATES = {"EXT"}

CAPAD_SOURCE_URL = "https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer"
CAPAD_LAYER = 0
CAPAD_WHERE = "NRS_PA='Y'"

CITY_POINTS = [
    ("Sydney", 151.2093, -33.8688),
    ("Melbourne", 144.9631, -37.8136),
    ("Brisbane", 153.0251, -27.4698),
    ("Perth", 115.8613, -31.9523),
    ("Adelaide", 138.6007, -34.9285),
    ("Canberra", 149.1300, -35.2809),
    ("Hobart", 147.3272, -42.8821),
    ("Darwin", 130.8456, -12.4634),
]


@dataclass(frozen=True)
class TriadPaths:
    triad_index_csv: Path
    triad_geoms_gpkg: Path
    triad_rings_csv: Path
    triad_buffers_gpkg: Path
    triad_definition_md: Path
    triad_qa_manifest: Path
    triad_maps_dir: Path


def _schema_slug() -> str:
    return SCHEMA_VERSION.replace(".", "_")


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fix_geometry(geom):
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        geom = make_valid(geom)
    return geom


def _build_city_gdf() -> gpd.GeoDataFrame:
    rows = [(name, Point(lon, lat)) for name, lon, lat in CITY_POINTS]
    gdf = gpd.GeoDataFrame(rows, columns=["city", "geometry"], crs="EPSG:4326")
    return gdf.to_crs(TARGET_CRS)


def fetch_capad_terrestrial() -> gpd.GeoDataFrame:
    query = CapadQuery(layer=CAPAD_LAYER, where=CAPAD_WHERE, out_sr=4326)
    gdf = fetch_gdf(query)
    if gdf.empty:
        raise RuntimeError("CAPAD query returned no features.")
    return gdf


def compute_metrics(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf["geometry"] = gdf["geometry"].apply(_fix_geometry)
    gdf = gdf[~gdf["geometry"].is_empty].copy()

    gdf = gdf.to_crs(TARGET_CRS)
    gdf["area_km2"] = gdf.geometry.area / 1_000_000.0
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
    return gdf


def select_triad(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    candidates = gdf[gdf["area_km2"] >= MIN_AREA_KM2].copy()
    if "STATE" in candidates.columns:
        candidates = candidates[~candidates["STATE"].isin(EXCLUDE_STATES)].copy()
    if len(candidates) < 3:
        raise RuntimeError("Not enough candidates after area filter for triad selection.")

    urban_candidates = candidates[candidates["distance_km"] <= URBAN_MAX_KM].copy()
    if urban_candidates.empty:
        raise RuntimeError("No urban-edge candidates found within URBAN_MAX_KM.")
    urban = urban_candidates.sort_values(
        by=["area_km2", "distance_km", "PA_ID"], ascending=[False, True, True]
    ).iloc[0]

    peri_candidates = candidates[
        (candidates["distance_km"] > PERI_RANGE_KM[0])
        & (candidates["distance_km"] <= PERI_RANGE_KM[1])
    ].copy()
    if peri_candidates.empty:
        raise RuntimeError("No peri-urban candidates found within PERI_RANGE_KM.")
    peri_candidates["distance_diff"] = (peri_candidates["distance_km"] - PERI_TARGET_KM).abs()
    peri = peri_candidates.sort_values(
        by=["distance_diff", "area_km2", "PA_ID"], ascending=[True, False, True]
    ).iloc[0]

    remaining = candidates[~candidates["PA_ID"].isin({urban["PA_ID"], peri["PA_ID"]})].copy()
    remote = remaining.sort_values(
        by=["distance_km", "area_km2", "PA_ID"], ascending=[False, False, True]
    ).iloc[0]

    rows = []
    for role, row in [("urban_edge", urban), ("peri_urban", peri), ("remote", remote)]:
        rows.append(
            {
                "schema_version": SCHEMA_VERSION,
                "triad_role": role,
                "pa_id": row.get("PA_ID"),
                "pa_pid": row.get("PA_PID"),
                "name": row.get("NAME"),
                "state": row.get("STATE"),
                "iucn": row.get("IUCN"),
                "area_km2": float(row.get("area_km2")),
                "distance_km": float(row.get("distance_km")),
                "nearest_city": row.get("nearest_city"),
            }
        )

    return pd.DataFrame(rows)


def triad_paths(root: Path) -> TriadPaths:
    schema_slug = _schema_slug()
    return TriadPaths(
        triad_index_csv=root / "data" / "processed" / f"smoke_test_triad_index_v{schema_slug}.csv",
        triad_geoms_gpkg=root / "data" / "processed" / f"smoke_test_triad_geoms_v{schema_slug}.gpkg",
        triad_rings_csv=root / "data" / "processed" / f"smoke_test_triad_rings_v{schema_slug}.csv",
        triad_buffers_gpkg=root / "data" / "processed" / f"smoke_test_triad_buffers_v{schema_slug}.gpkg",
        triad_definition_md=root / "analysis" / "reports" / "smoke_test_triad_definition.md",
        triad_qa_manifest=root / "analysis" / "reports" / "triad_qa_manifest.json",
        triad_maps_dir=root / "analysis" / "reports" / "triad_qa_maps",
    )


def write_triad_definition(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    display_df = df.copy()
    for col in ["area_km2", "distance_km"]:
        if col in display_df:
            display_df[col] = display_df[col].map(lambda v: f"{v:.2f}")

    headers = list(display_df.columns)
    rows = display_df.astype(str).values.tolist()
    table_lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        table_lines.append("| " + " | ".join(row) + " |")
    lines = [
        "# Smoke-test triad definition (WP0.4)",
        "",
        f"Generated: {_now_utc()}",
        "",
        "## Selection rule",
        "",
        "1) Fetch CAPAD 2024 protected areas (terrestrial; NRS_PA='Y').",
        f"2) Filter to area >= {MIN_AREA_KM2} km^2 and exclude STATE in {sorted(EXCLUDE_STATES)}.",
        "3) Compute distance from each PA centroid to nearest major city (8-city list).",
        "4) Select triad:",
        f"   - urban_edge: distance <= {URBAN_MAX_KM} km, choose largest area (tie-breaker distance, PA_ID)",
        f"   - peri_urban: distance in {PERI_RANGE_KM[0]}–{PERI_RANGE_KM[1]} km, choose closest to {PERI_TARGET_KM} km",
        "   - remote: maximum distance among remaining PAs (tie-breaker area, then PA_ID)",
        "",
        "## Selected protected areas",
        "",
        "\n".join(table_lines),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _safe_buffer(geom, distance_m: float):
    if geom is None or geom.is_empty:
        return geom
    buffered = geom.buffer(distance_m)
    if not buffered.is_valid:
        buffered = make_valid(buffered)
    return buffered


def build_buffers(gdf: gpd.GeoDataFrame, distances_km: Iterable[float]) -> gpd.GeoDataFrame:
    records = []
    for _, row in gdf.iterrows():
        base = row.geometry
        for dist_km in distances_km:
            buffer_geom = _safe_buffer(base, dist_km * 1000.0)
            outside = buffer_geom.difference(base)
            records.append(
                {
                    "pa_id": row["pa_id"],
                    "triad_role": row["triad_role"],
                    "buffer_km": dist_km,
                    "geometry": outside,
                }
            )
    return gpd.GeoDataFrame(records, crs=gdf.crs)


def build_rings(gdf: gpd.GeoDataFrame, ring_bins_km: Iterable[tuple[float, float]]) -> gpd.GeoDataFrame:
    records = []
    for _, row in gdf.iterrows():
        base = row.geometry
        for idx, (inner_km, outer_km) in enumerate(ring_bins_km):
            inner_geom = base if inner_km == 0 else _safe_buffer(base, -inner_km * 1000.0)
            if inner_geom is None or inner_geom.is_empty:
                ring_geom = inner_geom
            else:
                outer_geom = _safe_buffer(base, -outer_km * 1000.0)
                if outer_geom is None or outer_geom.is_empty:
                    ring_geom = inner_geom
                else:
                    ring_geom = inner_geom.difference(outer_geom)
            records.append(
                {
                    "pa_id": row["pa_id"],
                    "triad_role": row["triad_role"],
                    "ring_index": idx,
                    "ring_inner_km": inner_km,
                    "ring_outer_km": outer_km,
                    "geometry": ring_geom,
                }
            )
    return gpd.GeoDataFrame(records, crs=gdf.crs)


def _sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_qa_manifest(paths: TriadPaths, triad_df: pd.DataFrame) -> None:
    raw_capad = Path(find_repo_root()) / "data" / "raw" / "capad_2024_technical_spec.pdf"
    raw_vnl = Path(find_repo_root()) / "data" / "raw" / "vnl_v22_readme_20230707.pptx"

    manifest = {
        "generated_utc": _now_utc(),
        "schema_version": SCHEMA_VERSION,
        "capad": {
            "source": CAPAD_SOURCE_URL,
            "layer": CAPAD_LAYER,
            "where": CAPAD_WHERE,
            "metadata_files": {
                "capad_2024_technical_spec.pdf": _sha256(raw_capad) if raw_capad.exists() else None,
            },
        },
        "night_lights": {
            "metadata_files": {
                "vnl_v22_readme_20230707.pptx": _sha256(raw_vnl) if raw_vnl.exists() else None,
            }
        },
        "projection": TARGET_CRS,
        "buffer_distances_km": BUFFER_DISTANCES_KM,
        "ring_bins_km": RING_BINS_KM,
        "triad": triad_df.to_dict(orient="records"),
        "outputs": {
            "triad_index": str(paths.triad_index_csv),
            "triad_geoms": str(paths.triad_geoms_gpkg),
            "triad_rings_csv": str(paths.triad_rings_csv),
            "triad_buffers_gpkg": str(paths.triad_buffers_gpkg),
            "triad_maps_dir": str(paths.triad_maps_dir),
        },
    }
    paths.triad_qa_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _plot_maps(triad_gdf: gpd.GeoDataFrame, buffers: gpd.GeoDataFrame, rings: gpd.GeoDataFrame, paths: TriadPaths) -> None:
    import matplotlib.pyplot as plt

    if paths.triad_maps_dir.exists():
        shutil.rmtree(paths.triad_maps_dir)
    paths.triad_maps_dir.mkdir(parents=True, exist_ok=True)
    cities = _build_city_gdf().to_crs(triad_gdf.crs)

    for _, row in triad_gdf.iterrows():
        pa_id = row["pa_id"]
        role = row["triad_role"]
        geom = row.geometry

        fig, ax = plt.subplots(figsize=(6, 6))

        ring_sel = rings[rings["pa_id"] == pa_id]
        if not ring_sel.empty:
            ring_sel.plot(column="ring_index", ax=ax, cmap="Greens", alpha=0.5, legend=False)

        buffer_sel = buffers[buffers["pa_id"] == pa_id]
        if not buffer_sel.empty:
            buffer_sel.boundary.plot(ax=ax, color="orange", linewidth=1)

        gpd.GeoSeries([geom], crs=triad_gdf.crs).boundary.plot(ax=ax, color="black", linewidth=1.5)
        cities.plot(ax=ax, color="red", markersize=15)

        ax.set_title(f"{row['name']} ({role})")
        ax.set_axis_off()
        fig.tight_layout()

        out_path = paths.triad_maps_dir / f"{pa_id}_{role}.png"
        fig.savefig(out_path, dpi=150)
        plt.close(fig)

    readme = paths.triad_maps_dir / "README.md"
    readme.write_text(
        "# Triad QA maps\n\n"
        "Each PNG shows the PA boundary (black), inside rings (green fill), outside buffers (orange outline), and major cities (red points).\n",
        encoding="utf-8",
    )


def build_triad_outputs(root: Path) -> TriadPaths:
    paths = triad_paths(root)
    paths.triad_index_csv.parent.mkdir(parents=True, exist_ok=True)

    capad = fetch_capad_terrestrial()
    metrics = compute_metrics(capad)
    triad_df = select_triad(metrics)

    triad_df.to_csv(paths.triad_index_csv, index=False)
    write_triad_definition(triad_df, paths.triad_definition_md)

    triad_geoms = metrics[metrics["PA_ID"].isin(triad_df["pa_id"])].copy()
    triad_geoms = triad_geoms.drop(
        columns=["centroid", "area_km2", "distance_km", "nearest_city"], errors="ignore"
    )
    triad_geoms = triad_geoms.merge(triad_df, left_on="PA_ID", right_on="pa_id", how="inner")
    triad_geoms = triad_geoms.set_geometry("geometry")
    keep_cols = [
        "pa_id",
        "pa_pid",
        "name",
        "state",
        "iucn",
        "triad_role",
        "area_km2",
        "distance_km",
        "nearest_city",
        "geometry",
    ]
    triad_geoms = triad_geoms[keep_cols]
    triad_geoms.to_file(paths.triad_geoms_gpkg, driver="GPKG")

    buffers = build_buffers(triad_geoms, BUFFER_DISTANCES_KM)
    buffers.to_file(paths.triad_buffers_gpkg, driver="GPKG")

    rings = build_rings(triad_geoms, RING_BINS_KM)
    ring_summary = rings.copy()
    ring_summary["area_km2"] = ring_summary.geometry.area / 1_000_000.0
    ring_summary[[
        "pa_id",
        "triad_role",
        "ring_index",
        "ring_inner_km",
        "ring_outer_km",
        "area_km2",
    ]].to_csv(paths.triad_rings_csv, index=False)

    _plot_maps(triad_geoms, buffers, rings, paths)
    write_qa_manifest(paths, triad_df)

    return paths


def write_artefacts(paths: TriadPaths, root: Path) -> Path:
    artefact_dir = root / "artefacts" / "wp0_4_smoketest_triad"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(paths.triad_definition_md, artefact_dir / paths.triad_definition_md.name)
    shutil.copyfile(paths.triad_index_csv, artefact_dir / paths.triad_index_csv.name)
    shutil.copyfile(paths.triad_rings_csv, artefact_dir / paths.triad_rings_csv.name)
    shutil.copyfile(paths.triad_qa_manifest, artefact_dir / paths.triad_qa_manifest.name)

    maps_dest = artefact_dir / "triad_qa_maps"
    if maps_dest.exists():
        shutil.rmtree(maps_dest)
    shutil.copytree(paths.triad_maps_dir, maps_dest)

    manifest = build_manifest(
        run_id="wp0_4_smoketest_triad",
        wp="WP0.4",
        root=root,
        outputs=[
            paths.triad_definition_md.name,
            paths.triad_index_csv.name,
            paths.triad_rings_csv.name,
            paths.triad_qa_manifest.name,
            "triad_qa_maps/",
        ],
        notes="WP0.4 smoke-test triad outputs",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.4 smoke-test triad artefact. Contains triad definition, index, ring summary, QA manifest, and maps.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build smoke-test triad and QA outputs.")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    paths = build_triad_outputs(root)
    if not args.skip_artefact:
        write_artefacts(paths, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

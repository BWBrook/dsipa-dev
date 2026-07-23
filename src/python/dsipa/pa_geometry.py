"""Protected-area geometry processing (WP0.5)."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from dsipa.capad import CapadQuery, fetch_gdf, fetch_layer_metadata, fetch_service_metadata
from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import PA_GEOMETRIES_CSV, PA_GEOMETRIES_GPKG, SCHEMA_VERSION

try:
    from shapely import make_valid
except ImportError:  # pragma: no cover
    from shapely.validation import make_valid  # type: ignore

TARGET_CRS = "EPSG:3577"

CAPAD_LAYER = 0
CAPAD_WHERE = "NRS_PA='Y'"


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fix_geometry(geom):
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        geom = make_valid(geom)
    return geom


def _hash_geometries(gdf: gpd.GeoDataFrame) -> str:
    digest = hashlib.sha256()
    ordered = gdf.sort_values("PA_ID")
    for _, row in ordered.iterrows():
        digest.update(str(row["PA_ID"]).encode("utf-8"))
        geom = row.geometry
        if geom is not None:
            digest.update(geom.wkb)
    return digest.hexdigest()


def write_capad_snapshot(root: Path, query: CapadQuery, gdf: gpd.GeoDataFrame) -> Path:
    snapshot_dir = root / "data" / "raw" / "capad_snapshot"
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
        "pa_id_hash_sha256": _hash_geometries(gdf[["PA_ID", "geometry"]].copy()),
        "semantic_sha256": _hash_geometries(gdf[["PA_ID", "geometry"]].copy()),
    }
    snapshot_path = snapshot_dir / f"capad_snapshot_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    snapshot_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return snapshot_path


def process_capad(root: Path | None = None) -> gpd.GeoDataFrame:
    query = CapadQuery(layer=CAPAD_LAYER, where=CAPAD_WHERE, out_sr=4326)
    gdf = fetch_gdf(query)
    if gdf.empty:
        raise RuntimeError("CAPAD query returned no features.")

    if root is not None:
        write_capad_snapshot(root, query, gdf)

    gdf = gdf.copy()
    gdf["valid_original"] = gdf.geometry.is_valid
    gdf["geometry"] = gdf.geometry.apply(_fix_geometry)
    gdf["valid_fixed"] = gdf.geometry.is_valid
    gdf["geometry_empty"] = gdf.geometry.is_empty

    gdf["schema_version"] = SCHEMA_VERSION
    gdf["pa_id"] = gdf["PA_ID"]
    gdf["pa_pid"] = gdf["PA_PID"]

    qc_counts = {
        "input_total": int(len(gdf)),
        "invalid_original": int((~gdf["valid_original"]).sum()),
        "invalid_fixed": int((~gdf["valid_fixed"]).sum()),
        "empty_after_fix": int(gdf["geometry_empty"].sum()),
    }

    part_counts = gdf.groupby("pa_id").size().rename("part_count").reset_index()
    valid_original_all = gdf.groupby("pa_id")["valid_original"].all().rename("valid_original_all").reset_index()
    valid_fixed_all = gdf.groupby("pa_id")["valid_fixed"].all().rename("valid_fixed_all").reset_index()

    dissolve_fields = {
        "schema_version": "first",
        "pa_pid": "first",
        "NAME": "first",
        "STATE": "first",
        "IUCN": "first",
        "TYPE": "first",
        "TYPE_ABBR": "first",
        "NRS_PA": "first",
        "NRS_MPA": "first",
        "valid_original": "first",
        "valid_fixed": "first",
        "geometry_empty": "first",
    }
    dissolved = gdf.dissolve(by="pa_id", as_index=False, aggfunc=dissolve_fields)
    dissolved = dissolved.merge(part_counts, on="pa_id", how="left")
    dissolved = dissolved.merge(valid_original_all, on="pa_id", how="left")
    dissolved = dissolved.merge(valid_fixed_all, on="pa_id", how="left")

    dissolved = dissolved.to_crs(TARGET_CRS)
    dissolved["area_km2"] = dissolved.geometry.area / 1_000_000.0
    dissolved["perimeter_km"] = dissolved.geometry.length / 1000.0
    dissolved["compactness"] = (4 * np.pi * dissolved.geometry.area) / (dissolved.geometry.length ** 2)

    dissolved = dissolved.drop(columns=["PA_ID", "PA_PID"], errors="ignore")
    dissolved.attrs["qc_counts"] = qc_counts

    return dissolved


def write_outputs(gdf: gpd.GeoDataFrame, root: Path) -> dict[str, Path]:
    out_gpkg = root / PA_GEOMETRIES_GPKG
    out_csv = root / PA_GEOMETRIES_CSV

    gdf = gdf.sort_values("pa_id", kind="mergesort").reset_index(drop=True)
    gdf.to_file(out_gpkg, driver="GPKG")

    table_cols = [
        "schema_version",
        "pa_id",
        "pa_pid",
        "NAME",
        "STATE",
        "IUCN",
        "TYPE",
        "TYPE_ABBR",
        "NRS_PA",
        "NRS_MPA",
        "part_count",
        "valid_original_all",
        "valid_fixed_all",
        "area_km2",
        "perimeter_km",
        "compactness",
        "valid_original",
        "valid_fixed",
        "geometry_empty",
    ]
    gdf[table_cols].to_csv(out_csv, index=False)

    return {"gpkg": out_gpkg, "csv": out_csv}


def write_qc_report(gdf: gpd.GeoDataFrame, path: Path) -> None:
    qc_counts = gdf.attrs.get("qc_counts", {}) if hasattr(gdf, "attrs") else {}
    total_input = qc_counts.get("input_total", len(gdf))
    invalid_original = qc_counts.get("invalid_original", int((~gdf["valid_original"]).sum()))
    invalid_fixed = qc_counts.get("invalid_fixed", int((~gdf["valid_fixed"]).sum()))
    empty_geom = qc_counts.get("empty_after_fix", int(gdf["geometry_empty"].sum()))
    zero_area = int((gdf["area_km2"] <= 0).sum())
    min_area = float(gdf["area_km2"].min())

    summary = gdf[["area_km2", "perimeter_km", "compactness"]].describe().round(3)
    summary_text = summary.to_string()

    lines = [
        "# PA geometry QC report",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Total input features: {total_input}",
        f"Output features (dissolved): {len(gdf)}",
        f"Invalid geometries (original): {invalid_original}",
        f"Invalid geometries (after fix): {invalid_fixed}",
        f"Empty geometries (after fix): {empty_geom}",
        f"Zero-area geometries: {zero_area}",
        f"Min area_km2 (raw): {min_area:.10f}",
        f"Unique pa_id values: {gdf['pa_id'].nunique()}",
        "",
        "## Descriptor summary (km / unitless)",
        "",
        "```",
        summary_text,
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_artefact(outputs: dict[str, Path], qc_report: Path, root: Path) -> Path:
    artefact_dir = root / "artefacts" / "wp0_5_pa_geometry"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(qc_report, artefact_dir / qc_report.name)
    shutil.copyfile(outputs["csv"], artefact_dir / outputs["csv"].name)
    shutil.copyfile(outputs["gpkg"], artefact_dir / outputs["gpkg"].name)

    manifest = build_manifest(
        run_id="wp0_5_pa_geometry",
        wp="WP0.5",
        root=root,
        outputs=[qc_report.name, outputs["csv"].name, outputs["gpkg"].name],
        inputs=["CAPAD MapServer layer 0 (NRS_PA='Y')"],
        notes="WP0.5 protected-area geometry processing",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.5 geometry artefact. Contains QC report and processed geometry outputs.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process CAPAD geometries (WP0.5).")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    gdf = process_capad(root)
    outputs = write_outputs(gdf, root)

    qc_report = root / "analysis" / "reports" / "pa_geometry_qc.md"
    write_qc_report(gdf, qc_report)

    if not args.skip_artefact:
        write_artefact(outputs, qc_report, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

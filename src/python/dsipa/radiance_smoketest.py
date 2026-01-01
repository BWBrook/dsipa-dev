"""Radiance summarisation for smoke-test triad (WP0.6)."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask

from dsipa.manifest import build_manifest, write_manifest
from dsipa.nightlights import EXPECTED_MD5, download_year
from dsipa.paths import find_repo_root
from dsipa.schema import RADIANCE_BUFFERS_SMOKETEST_CSV, SCHEMA_VERSION
SMOKETEST_YEARS = [2013, 2018, 2024]

TRIAD_GEOMS = "data/processed/smoke_test_triad_geoms_v0_1_0.gpkg"
TRIAD_BUFFERS = "data/processed/smoke_test_triad_buffers_v0_1_0.gpkg"

OUTPUT_TABLE = RADIANCE_BUFFERS_SMOKETEST_CSV
SANITY_REPORT = "analysis/reports/smoketest_buffers_sanity.md"
SANITY_PLOT = "analysis/reports/smoketest_buffers_summary.png"


@dataclass(frozen=True)
class RasterMeta:
    year: int
    path: Path
    nodata: float | None
    dtype: str
    scale: float | None
    offset: float | None
    tags: dict[str, str]


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _load_geoms(path: Path, target_crs: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.empty:
        raise RuntimeError(f"No features found in {path}")
    return gdf.to_crs(target_crs)


def _stats_for_geom(dataset: rasterio.DatasetReader, geom) -> dict[str, float]:
    nodata = dataset.nodata
    data, _ = mask(dataset, [geom], crop=True, filled=True, nodata=nodata)
    band = data[0]

    mask_invalid = np.isnan(band)
    if nodata is not None:
        mask_invalid |= band == nodata
    mask_invalid |= band < 0

    pixel_count = int(band.size)
    valid = band[~mask_invalid]
    valid_count = int(valid.size)

    if valid_count == 0:
        return {
            "pixel_count": pixel_count,
            "valid_pixel_count": valid_count,
            "valid_fraction": 0.0,
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
        }

    return {
        "pixel_count": pixel_count,
        "valid_pixel_count": valid_count,
        "valid_fraction": float(valid_count / pixel_count),
        "mean": float(np.mean(valid)),
        "median": float(np.median(valid)),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
        "std": float(np.std(valid)),
    }


def _raster_meta(dataset: rasterio.DatasetReader, year: int, path: Path) -> RasterMeta:
    scale = None
    offset = None
    if dataset.scales:
        scale = dataset.scales[0]
    if dataset.offsets:
        offset = dataset.offsets[0]

    return RasterMeta(
        year=year,
        path=path,
        nodata=dataset.nodata,
        dtype=str(dataset.dtypes[0]),
        scale=scale,
        offset=offset,
        tags={k: str(v) for k, v in dataset.tags(1).items()},
    )


def summarise_year(
    year: int,
    triad: gpd.GeoDataFrame,
    buffers: gpd.GeoDataFrame,
    raster_path: Path,
) -> tuple[list[dict], RasterMeta]:
    records: list[dict] = []
    with rasterio.open(raster_path) as dataset:
        triad = triad.to_crs(dataset.crs)
        buffers = buffers.to_crs(dataset.crs)

        meta = _raster_meta(dataset, year, raster_path)

        for _, row in triad.iterrows():
            stats = _stats_for_geom(dataset, row.geometry)
            records.append(
                {
                    "schema_version": SCHEMA_VERSION,
                    "pa_id": row["pa_id"],
                    "triad_role": row["triad_role"],
                    "year": year,
                    "zone": "inside",
                    "buffer_km": np.nan,
                    "scale_metadata": meta.scale,
                    "offset_metadata": meta.offset,
                    **stats,
                }
            )

        for _, row in buffers.iterrows():
            stats = _stats_for_geom(dataset, row.geometry)
            records.append(
                {
                    "schema_version": SCHEMA_VERSION,
                    "pa_id": row["pa_id"],
                    "triad_role": row["triad_role"],
                    "year": year,
                    "zone": "buffer",
                    "buffer_km": float(row["buffer_km"]),
                    "scale_metadata": meta.scale,
                    "offset_metadata": meta.offset,
                    **stats,
                }
            )

    return records, meta


def write_sanity_report(
    df: pd.DataFrame,
    raster_meta: Iterable[RasterMeta],
    report_path: Path,
    plot_path: Path,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    meta_lines = []
    for meta in raster_meta:
        meta_lines.append(
            f"- {meta.year}: dtype={meta.dtype}, nodata={meta.nodata}, scale={meta.scale}, offset={meta.offset}"
        )

    low_pixels = df[df["valid_pixel_count"] < 10]
    anchor = (
        df[df["zone"] == "inside"]
        .pivot_table(index=["year"], columns=["triad_role"], values="mean")
        .reset_index()
    )

    lines = [
        "# Smoke-test radiance buffers sanity report",
        "",
        f"Generated: {_now_utc()}",
        "",
        "## Raster metadata (per year)",
        *meta_lines,
        "",
        "Note: Summary statistics are computed on raw stored values (no scale/offset applied).",
        "",
        "## Summary by zone",
        "",
        df.groupby(["year", "zone"])[["mean", "median", "valid_pixel_count"]].describe().round(3).to_string(),
        "",
        "## Anchor check (inside mean by triad role)",
        "",
        anchor.round(3).to_string(index=False),
        "",
        "## Low pixel-count warnings (<10)",
        "",
    ]

    if low_pixels.empty:
        lines.append("None")
    else:
        lines.append(low_pixels[["pa_id", "triad_role", "year", "zone", "buffer_km", "valid_pixel_count"]].to_string(index=False))

    lines.extend(
        [
            "",
            f"Plot: {plot_path.name}",
        ]
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_plot(df: pd.DataFrame, plot_path: Path) -> None:
    import matplotlib.pyplot as plt

    plot_path.parent.mkdir(parents=True, exist_ok=True)
    inside = df[df["zone"] == "inside"].copy()
    buffers = df[df["zone"] == "buffer"].copy()

    fig, axes = plt.subplots(1, len(SMOKETEST_YEARS), figsize=(12, 4), sharey=True)
    if len(SMOKETEST_YEARS) == 1:
        axes = [axes]

    for ax, year in zip(axes, SMOKETEST_YEARS):
        inside_year = inside[inside["year"] == year]
        buffer_year = buffers[buffers["year"] == year]

        roles = inside_year["triad_role"].tolist()
        x = np.arange(len(roles))
        width = 0.25

        inside_vals = inside_year["mean"].values
        buffer1_vals = (
            buffer_year[buffer_year["buffer_km"] == 1.0]
            .set_index("triad_role")
            .loc[roles]["mean"]
            .values
        )
        buffer5_vals = (
            buffer_year[buffer_year["buffer_km"] == 5.0]
            .set_index("triad_role")
            .loc[roles]["mean"]
            .values
        )

        ax.bar(x - width, inside_vals, width, label="inside")
        ax.bar(x, buffer1_vals, width, label="buffer 1km")
        ax.bar(x + width, buffer5_vals, width, label="buffer 5km")
        ax.set_title(str(year))
        ax.set_xticks(x)
        ax.set_xticklabels(roles, rotation=45, ha="right")

    axes[0].set_ylabel("Mean night-light value (scaled units)")
    axes[-1].legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.tight_layout()
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)


def write_outputs(df: pd.DataFrame, root: Path) -> Path:
    out_path = root / OUTPUT_TABLE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path


def write_artefact(
    report_path: Path,
    plot_path: Path,
    table_path: Path,
    root: Path,
) -> Path:
    artefact_dir = root / "artefacts" / "wp0_6_radiance_smoketest"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(plot_path, artefact_dir / plot_path.name)
    shutil.copyfile(table_path, artefact_dir / table_path.name)

    manifest = build_manifest(
        run_id="wp0_6_radiance_smoketest",
        wp="WP0.6",
        root=root,
        outputs=[report_path.name, plot_path.name, table_path.name],
        notes="WP0.6 smoke-test radiance summaries",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.6 smoke-test radiance artefact. Contains summary table, sanity report, and plot.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke-test radiance summarisation (WP0.6).")
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
    raster_files = [download_year(year, raw_dir) for year in SMOKETEST_YEARS]

    triad = _load_geoms(root / TRIAD_GEOMS, target_crs="EPSG:3577")
    buffers = _load_geoms(root / TRIAD_BUFFERS, target_crs="EPSG:3577")

    all_records: list[dict] = []
    meta_records: list[RasterMeta] = []
    for file in raster_files:
        records, meta = summarise_year(file.year, triad, buffers, file.path)
        all_records.extend(records)
        meta_records.append(meta)

    df = pd.DataFrame(all_records)
    table_path = write_outputs(df, root)

    report_path = root / SANITY_REPORT
    plot_path = root / SANITY_PLOT
    write_plot(df, plot_path)
    write_sanity_report(df, meta_records, report_path, plot_path)

    if not args.skip_artefact:
        write_artefact(report_path, plot_path, table_path, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

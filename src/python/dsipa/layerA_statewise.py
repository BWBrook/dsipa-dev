"""Statewise Layer A runner and merger (performance-friendly)."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd
import rasterio

from dsipa.layerA_national import (
    REPORT_PATH,
    PLOT_PATH,
    _resolve_output_path,
    _write_plot,
    write_report,
)
from dsipa.layerA_national import _attach_city_distance, _raster_meta
from dsipa.manifest import build_manifest, write_manifest
from dsipa.nightlights import CORE_YEARS, download_year
from dsipa.paths import find_repo_root
from dsipa.schema import (
    EDGE_PROFILES_NATIONAL_CSV,
    PA_BUFFER_VALIDITY_CSV,
    PA_GEOMETRIES_GPKG,
    RADIANCE_BUFFERS_NATIONAL_CSV,
)
from dsipa import layerA_national

DEFAULT_STATES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA", "JBT", "EXT"]


def _run_state(state: str, args: argparse.Namespace) -> None:
    output_dir = None
    if args.output_root:
        output_dir = str(Path(args.output_root) / state)
    argv = [
        "--states",
        state,
        "--min-valid-pixels",
        str(args.min_valid_pixels),
        "--workers",
        str(args.workers),
        "--chunk-size",
        str(args.chunk_size),
    ]
    if args.output_root:
        argv.extend(["--output-dir", output_dir])
    if args.buffers_only:
        argv.append("--buffers-only")
    if args.rings_only:
        argv.append("--rings-only")
    if args.skip_artefact:
        argv.append("--skip-artefact")
    if args.years:
        argv.extend(["--years", *[str(year) for year in args.years]])
    layerA_national.main(argv)


def _merge_tables(paths: list[Path], key_cols: list[str]) -> pd.DataFrame:
    frames = [pd.read_csv(path) for path in paths if path.exists()]
    if not frames:
        raise FileNotFoundError("No state outputs found to merge.")
    merged = pd.concat(frames, ignore_index=True)
    if merged.duplicated(subset=key_cols).any():
        dupes = merged[merged.duplicated(subset=key_cols, keep=False)][key_cols].head(5)
        raise RuntimeError(f"Duplicate keys found when merging state outputs: {dupes}")
    return merged


def merge_state_outputs(
    *,
    output_root: Path,
    states: list[str],
    output_dir: str | None,
    years: list[int],
    min_valid_pixels: int,
    buffers_only: bool,
    rings_only: bool,
) -> None:
    state_dirs = [output_root / state for state in states]
    radiance = None
    rings = None
    validity = None

    if not rings_only:
        radiance_paths = [d / Path(RADIANCE_BUFFERS_NATIONAL_CSV).name for d in state_dirs]
        validity_paths = [d / Path(PA_BUFFER_VALIDITY_CSV).name for d in state_dirs]
        radiance = _merge_tables(
            radiance_paths,
            ["pa_id", "year", "zone", "buffer_km", "buffer_type"],
        )
        validity = _merge_tables(
            validity_paths,
            ["pa_id", "buffer_km"],
        )
        for col in ["land_fraction", "protected_overlap_fraction"]:
            if col in validity.columns:
                validity[col] = validity[col].clip(lower=0.0, upper=1.0)

    if not buffers_only:
        ring_paths = [d / Path(EDGE_PROFILES_NATIONAL_CSV).name for d in state_dirs]
        rings = _merge_tables(
            ring_paths,
            ["pa_id", "year", "ring_index"],
        )

    root = find_repo_root()
    radiance_path = None
    ring_path = None
    validity_path = None

    if radiance is not None:
        radiance_path = _resolve_output_path(root, output_dir, RADIANCE_BUFFERS_NATIONAL_CSV)
        radiance.to_csv(radiance_path, index=False)
    if rings is not None:
        ring_path = _resolve_output_path(root, output_dir, EDGE_PROFILES_NATIONAL_CSV)
        rings.to_csv(ring_path, index=False)
    if validity is not None:
        validity_path = _resolve_output_path(root, output_dir, PA_BUFFER_VALIDITY_CSV)
        validity.to_csv(validity_path, index=False)

    report_path = None
    plot_path = None
    if radiance is not None and rings is not None and validity is not None:
        pa_gdf = layerA_national._load_pa_geoms(root)
        pa_meta = _attach_city_distance(pa_gdf)

        meta_records = []
        raw_dir = root / "data" / "raw" / "nightlights_zenodo_v0_4"
        for year in years:
            raster = download_year(year, raw_dir)
            with rasterio.open(raster.path) as dataset:
                meta_records.append(_raster_meta(dataset, year, raster.path))

        report_path = _resolve_output_path(root, output_dir, REPORT_PATH)
        plot_path = _resolve_output_path(root, output_dir, PLOT_PATH)
        _write_plot(radiance, plot_path)
        subset_note = f"Statewise merge: states={','.join(states)}."
        write_report(
            radiance_df=radiance,
            ring_df=rings,
            meta_records=meta_records,
            pa_meta=pa_meta,
            report_path=report_path,
            plot_path=plot_path,
            min_valid_pixels=min_valid_pixels,
            buffer_validity=validity,
            subset_note=subset_note,
        )

    artefact_dir = root / "artefacts" / "wp0_9_layerA_national_statewise"
    artefact_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for path in [radiance_path, ring_path, validity_path, report_path, plot_path]:
        if path is None:
            continue
        shutil.copyfile(path, artefact_dir / path.name)
        outputs.append(path.name)
    if outputs:
        manifest = build_manifest(
            run_id="wp0_9_layerA_national_statewise",
            wp="WP0.9",
            root=root,
            outputs=outputs,
            notes="Statewise merge of Layer A national outputs",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Layer A by state and merge outputs.")
    parser.add_argument("--states", default=",".join(DEFAULT_STATES), help="Comma-separated state codes.")
    parser.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=list(CORE_YEARS),
        help="Years to process (default: 2013–2024).",
    )
    parser.add_argument("--min-valid-pixels", type=int, default=10)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--chunk-size", type=int, default=300)
    parser.add_argument("--output-root", default="analysis/state_runs", help="Per-state output root.")
    parser.add_argument("--merge-only", action="store_true", help="Skip per-state runs; merge only.")
    parser.add_argument("--skip-artefact", action="store_true", help="Skip per-state artefacts.")
    parser.add_argument("--buffers-only", action="store_true", help="Only compute inside/buffer summaries.")
    parser.add_argument("--rings-only", action="store_true", help="Only compute ring summaries.")
    parser.add_argument("--output-dir", default=None, help="Merged output dir override.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    states = [state.strip().upper() for state in args.states.split(",") if state.strip()]
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    if not args.merge_only:
        for state in states:
            _run_state(state, args)

    merge_state_outputs(
        output_root=output_root,
        states=states,
        output_dir=args.output_dir,
        years=args.years,
        min_valid_pixels=args.min_valid_pixels,
        buffers_only=args.buffers_only,
        rings_only=args.rings_only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

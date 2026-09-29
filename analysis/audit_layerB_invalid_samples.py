#!/usr/bin/env python3
"""Bounded, read-only audit of archived Layer B exposure inputs.

The accepted remote checkout does not normally contain ALA row-level inputs or
the derived feature frames. This script records that availability explicitly,
and, when requested, scans only the archived night-light rasters for raw
invalid codes. It never writes beneath the inspected repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def _sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk_size), b""):
            digest.update(block)
    return digest.hexdigest()


def _candidate_feature_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for directory in (root / "data" / "processed", root / "artefacts", root / "analysis" / "reports"):
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix not in {".csv", ".gz", ".parquet", ".feather", ".npz"}:
                continue
            name = path.name.lower()
            if any(token in name for token in ("layerb", "feature", "model_input", "occurrence")):
                candidates.append(path)
    return sorted(set(candidates))


def _feature_counts(path: Path) -> dict[str, object]:
    """Count invalid values where an archived feature frame is available."""
    result: dict[str, object] = {"path": str(path), "sha256": _sha256(path)}
    if path.suffix not in {".csv", ".gz"}:
        result["status"] = "present_not_csv"
        return result

    import pandas as pd

    chunks = pd.read_csv(path, compression="gzip" if path.suffix == ".gz" else None, chunksize=100_000)
    total = raw_invalid = decoded_negative = decoded_nonfinite = 0
    has_alan = False
    raw_columns: list[str] = []
    for chunk in chunks:
        total += len(chunk)
        for column in ("raw_alan", "alan_raw", "stored_alan"):
            if column in chunk.columns:
                raw_columns.append(column)
                raw = pd.to_numeric(chunk[column], errors="coerce")
                raw_invalid += int((~np.isfinite(raw) | (raw < 0)).sum())
        if "alan" in chunk.columns:
            has_alan = True
            alan = pd.to_numeric(chunk["alan"], errors="coerce")
            decoded_negative += int((alan < 0).fillna(False).sum())
            decoded_nonfinite += int((~np.isfinite(alan)).sum())
    result.update(
        {
            "status": "scanned",
            "rows": total,
            "has_alan_column": has_alan,
            "raw_invalid_rows": raw_invalid,
            "raw_columns": sorted(set(raw_columns)),
            "decoded_negative_rows": decoded_negative,
            "decoded_nonfinite_rows": decoded_nonfinite,
        }
    )
    return result


def _raster_stats(path: Path) -> dict[str, object]:
    import rasterio

    stats = {
        "path": str(path),
        "sha256": _sha256(path),
        "bytes": path.stat().st_size,
    }
    with rasterio.open(path) as dataset:
        nodata = dataset.nodata
        counts = {"raw_nodata": 0, "raw_negative_non_nodata": 0, "raw_zero": 0, "raw_positive": 0, "raw_nonfinite": 0}
        for _, window in dataset.block_windows(1):
            raw = dataset.read(1, window=window, masked=False)
            finite = np.isfinite(raw)
            counts["raw_nonfinite"] += int((~finite).sum())
            if nodata is not None:
                nodata_mask = finite & (raw == nodata)
                counts["raw_nodata"] += int(nodata_mask.sum())
            else:
                nodata_mask = np.zeros(raw.shape, dtype=bool)
            valid = finite & ~nodata_mask
            counts["raw_negative_non_nodata"] += int((valid & (raw < 0)).sum())
            counts["raw_zero"] += int((valid & (raw == 0)).sum())
            counts["raw_positive"] += int((valid & (raw > 0)).sum())
        stats.update(
            {
                "status": "scanned",
                "shape": [dataset.height, dataset.width],
                "dtype": dataset.dtypes[0],
                "nodata": nodata,
                "scale": dataset.scales[0] if dataset.scales else None,
                "offset": dataset.offsets[0] if dataset.offsets else None,
                "counts": counts,
            }
        )
    return stats


def audit(root: Path, *, scan_rasters: bool, hash_rasters: bool) -> dict[str, object]:
    summary_candidates = [
        root / "data" / "processed" / "layerB_model_input_summary_v0_3_0.csv",
        root / "analysis" / "reports" / "layerB_modelling_report.md",
        root / "analysis" / "reports" / "final_release_manifest.md",
    ]
    available_summaries = [
        {"path": str(path), "sha256": _sha256(path), "bytes": path.stat().st_size}
        for path in summary_candidates
        if path.exists()
    ]
    feature_files = _candidate_feature_files(root)
    feature_results = [_feature_counts(path) for path in feature_files]
    result: dict[str, object] = {
        "repository": str(root),
        "feature_cache": {
            "files_found": len(feature_files),
            "files": feature_results,
            "scope_counts_reconstructable": any(item.get("has_alan_column", False) for item in feature_results),
        },
        "accepted_scope_counts": {
            "primary_dr368": "unknown_without_archived_row_level_or_feature_inputs",
            "shuffle_within_block": "unknown_without_archived_feature_inputs",
            "shuffle_within_ibra_year": "unknown_without_archived_feature_inputs",
            "sensitivity_all_providers": "unknown_without_archived_row_level_or_feature_inputs",
        },
        "summary_inputs": available_summaries,
        "raster_scan": {"requested": scan_rasters, "files": []},
    }

    if scan_rasters:
        raster_dir = root / "data" / "raw" / "nightlights_zenodo_v0_4"
        raster_paths = sorted(raster_dir.glob("*.tif")) if raster_dir.exists() else []
        if hash_rasters:
            result["raster_scan"]["files"] = [_raster_stats(path) for path in raster_paths]
        else:
            import rasterio

            files = []
            for path in raster_paths:
                with rasterio.open(path) as dataset:
                    files.append(
                        {
                            "path": str(path),
                            "bytes": path.stat().st_size,
                            "shape": [dataset.height, dataset.width],
                            "dtype": dataset.dtypes[0],
                            "nodata": dataset.nodata,
                            "scale": dataset.scales[0] if dataset.scales else None,
                            "offset": dataset.offsets[0] if dataset.offsets else None,
                        }
                    )
            result["raster_scan"]["files"] = files
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scan-rasters", action="store_true")
    parser.add_argument("--hash-rasters", action="store_true")
    args = parser.parse_args()
    output = audit(args.repo_root, scan_rasters=args.scan_rasters, hash_rasters=args.hash_rasters)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

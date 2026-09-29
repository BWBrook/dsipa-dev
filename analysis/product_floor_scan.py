#!/usr/bin/env python3
"""Complete the observed positive-pixel floor scan for 2014--2019.

Read-only follow-up to the frozen product-continuity audit. The fixed window is
the same accepted Australian audit rectangle; this script neither modifies nor
replaces prior audit outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import Window


YEARS = range(2014, 2020)
WINDOW = Window(66196, 23228, 17554, 8507)
EXPECTED_SHA256 = {
    2014: "12e24b91f3fef11117ac6bfb66142b1088541884602921128d3ddd44e3e40cbd",
    2015: "a673f35bd6240c6dc69e05550cdfcd46080a23364a12b91fe897312a308f712f",
    2016: "319ef2d91a2ff4733c61a555a81f05b483c9b47463b1f91f00bbc5385556ca45",
    2017: "6c767ca0d2c5b2c45c87fea60039bd232ed6a0114229ab31d9c2fa2238114c46",
    2018: "62fd7052dc69cadaf446d61ea135e8489b321be24cb4b3b4e26f689b81a3405a",
    2019: "9f84fedf65c5a1bdbda63295849d80f99c3b03a9a569e19b173026829c1760b3",
}


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raster-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc)
    start_clock = time.monotonic()
    rows: list[dict[str, object]] = []
    exceptions: list[dict[str, object]] = []
    inputs: dict[str, dict[str, object]] = {}
    expected_grid = None

    for year in YEARS:
        matches = list(args.raster_dir.glob(f"*_{year}0101_{year}1231_*.tif"))
        if len(matches) != 1:
            raise RuntimeError(f"Expected one raster for {year}, found {len(matches)}")
        path = matches[0]
        digest = sha256(path)
        if digest != EXPECTED_SHA256[year]:
            raise RuntimeError(f"SHA256 mismatch for {path.name}: {digest}")

        with rasterio.open(path) as dataset:
            grid = (dataset.shape, tuple(dataset.transform), dataset.crs.to_string())
            if expected_grid is None:
                expected_grid = grid
            elif grid != expected_grid:
                raise RuntimeError(f"Grid mismatch for {path.name}")

            scale = float(dataset.scales[0])
            offset = float(dataset.offsets[0])
            hist = np.zeros(65536, dtype=np.int64)
            row_end = int(WINDOW.row_off + WINDOW.height)
            for row_start in range(int(WINDOW.row_off), row_end, 512):
                block = Window(
                    WINDOW.col_off,
                    row_start,
                    WINDOW.width,
                    min(512, row_end - row_start),
                )
                values = dataset.read(1, window=block)
                hist += np.bincount(
                    values.ravel().astype(np.int32) + 32768,
                    minlength=65536,
                )

            stored_values = np.flatnonzero(hist) - 32768
            positive_values = stored_values[stored_values > 0]
            positive_counts = hist[positive_values + 32768]
            decoded_values = positive_values.astype(float) * scale + offset
            off_lattice = ~np.isclose(np.mod(decoded_values, 10.0), 0.0, atol=1e-9)
            gcd_stored = int(np.gcd.reduce(positive_values)) if len(positive_values) else None

            for stored, decoded, count in zip(
                positive_values[off_lattice],
                decoded_values[off_lattice],
                positive_counts[off_lattice],
                strict=True,
            ):
                exceptions.append(
                    {
                        "year": year,
                        "stored_value": int(stored),
                        "decoded_value": float(decoded),
                        "pixel_count": int(count),
                    }
                )

            positive_pixels = int(positive_counts.sum())
            off_lattice_pixels = int(positive_counts[off_lattice].sum())
            rows.append(
                {
                    "year": year,
                    "scale": scale,
                    "offset": offset,
                    "minimum_positive_stored": int(positive_values.min()),
                    "minimum_positive_decoded": float(decoded_values.min()),
                    "positive_unique_codes": int(len(positive_values)),
                    "positive_pixels": positive_pixels,
                    "zero_pixels": int(hist[32768]),
                    "negative_pixels_including_nodata": int(hist[:32768].sum()),
                    "gcd_positive_stored_codes": gcd_stored,
                    "off_10_lattice_unique_codes": int(off_lattice.sum()),
                    "off_10_lattice_pixels": off_lattice_pixels,
                    "off_10_lattice_fraction_positive": (
                        off_lattice_pixels / positive_pixels if positive_pixels else math.nan
                    ),
                }
            )
            inputs[str(year)] = {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": digest,
                "dtype": dataset.dtypes[0],
                "nodata": dataset.nodata,
            }
        print(f"complete {year}", flush=True)

    summary_path = args.output_dir / "product_floor_summary.csv"
    exception_path = args.output_dir / "product_floor_exceptions.csv"
    pd.DataFrame(rows).to_csv(summary_path, index=False)
    pd.DataFrame(
        exceptions,
        columns=["year", "stored_value", "decoded_value", "pixel_count"],
    ).to_csv(exception_path, index=False)

    finished = datetime.now(timezone.utc)
    manifest = {
        "purpose": "Read-only 2014-2019 observed positive-pixel floor follow-up",
        "host": socket.gethostname(),
        "started_utc": started.isoformat(),
        "finished_utc": finished.isoformat(),
        "runtime_seconds": time.monotonic() - start_clock,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "rasterio": rasterio.__version__,
        "window": [WINDOW.col_off, WINDOW.row_off, WINDOW.width, WINDOW.height],
        "window_pixels": int(WINDOW.width * WINDOW.height),
        "script_sha256": sha256(Path(__file__)),
        "inputs": inputs,
        "outputs_sha256": {
            summary_path.name: sha256(summary_path),
            exception_path.name: sha256(exception_path),
        },
        "interpretation_boundary": (
            "Observed stored values only; not a sensor detection threshold, "
            "calibrated physical-unit statement, or claim about polygon means."
        ),
    }
    (args.output_dir / "product_floor_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()

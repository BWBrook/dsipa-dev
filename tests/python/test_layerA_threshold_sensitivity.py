from __future__ import annotations

import pandas as pd

from dsipa.layerA_threshold_sensitivity import build_sensitivity, validate_sensitivity


def test_threshold_sensitivity_counts_nested_quadrants() -> None:
    rows = []
    for pa_id, inside_values, buffer_values in [
        ("a", [0, 0, 1, 1], [0, 0, 2, 2]),
        ("b", [2, 2, 1, 1], [1, 1, 0, 0]),
    ]:
        for year, inside, buffer in zip([2021, 2022, 2023, 2024], inside_values, buffer_values, strict=True):
            rows.append(
                {
                    "pa_id": pa_id,
                    "zone": "inside",
                    "year": year,
                    "valid_pixel_count": 10,
                    "mean": inside,
                }
            )
            rows.append(
                {
                    "pa_id": pa_id,
                    "zone": "buffer",
                    "buffer_km": 1.0,
                    "buffer_type": "land_unprotected",
                    "year": year,
                    "valid_pixel_count": 10,
                    "mean": buffer,
                }
            )
    df = pd.DataFrame(rows)

    summary = build_sensitivity(df, pixel_thresholds=(10,), year_thresholds=(4,))
    notes = validate_sensitivity(summary)
    row = summary.iloc[0]

    assert row["inside_trend_n"] == 2
    assert row["quadrant_n"] == 2
    assert row["q1_concurrent_brightening"] == 1
    assert row["q3_stable_non_detect"] == 1
    assert "Quadrant counts sum to each scenario denominator." in notes

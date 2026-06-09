from __future__ import annotations

import pandas as pd

from dsipa.layerA_tables import build_denominator_rows, render_report, validate_rows


def _row(rows: pd.DataFrame, key: str) -> pd.Series:
    return rows.set_index("key").loc[key]


def test_build_denominator_rows_tracks_nested_denominators() -> None:
    geoms = pd.DataFrame({"pa_id": ["pa1", "pa2", "pa3"]})
    radiance = pd.DataFrame(
        [
            {"pa_id": "pa1", "zone": "inside", "year": 2024, "valid_pixel_count": 10, "mean": 0.0},
            {"pa_id": "pa2", "zone": "inside", "year": 2024, "valid_pixel_count": 5, "mean": 1.0},
            {"pa_id": "pa3", "zone": "inside", "year": 2024, "valid_pixel_count": 12, "mean": 2.0},
            {
                "pa_id": "pa1",
                "zone": "buffer",
                "year": 2024,
                "buffer_km": 1.0,
                "buffer_type": "land_unprotected",
                "valid_pixel_count": 11,
                "mean": 0.5,
            },
            {
                "pa_id": "pa3",
                "zone": "buffer",
                "year": 2024,
                "buffer_km": 1.0,
                "buffer_type": "land_unprotected",
                "valid_pixel_count": 9,
                "mean": 3.0,
            },
        ]
    )
    edge_profiles = pd.DataFrame(
        [
            {"pa_id": "pa1", "year": 2024, "ring_index": 0, "ring_inner_km": 0, "ring_outer_km": 1, "valid_pixel_count": 10},
            {"pa_id": "pa1", "year": 2024, "ring_index": 1, "ring_inner_km": 1, "ring_outer_km": 5, "valid_pixel_count": 10},
            {"pa_id": "pa1", "year": 2024, "ring_index": 2, "ring_inner_km": 5, "ring_outer_km": 10, "valid_pixel_count": 10},
            {"pa_id": "pa3", "year": 2024, "ring_index": 0, "ring_inner_km": 0, "ring_outer_km": 1, "valid_pixel_count": 10},
            {"pa_id": "pa3", "year": 2024, "ring_index": 1, "ring_inner_km": 1, "ring_outer_km": 5, "valid_pixel_count": 0},
            {"pa_id": "pa3", "year": 2024, "ring_index": 2, "ring_inner_km": 5, "ring_outer_km": 10, "valid_pixel_count": 0},
        ]
    )
    buffer_validity = pd.DataFrame(
        [
            {"pa_id": "pa1", "buffer_km": 1.0, "land_fraction": 0.7, "protected_overlap_fraction": 0.1},
            {"pa_id": "pa2", "buffer_km": 1.0, "land_fraction": 0.4, "protected_overlap_fraction": 0.3},
            {"pa_id": "pa3", "buffer_km": 1.0, "land_fraction": 0.9, "protected_overlap_fraction": 0.2},
        ]
    )
    trends = pd.DataFrame(
        [
            {
                "pa_id": "pa1",
                "metric": "mean",
                "buffer_type": "land_unprotected",
                "n_years_inside": 8,
                "slope_inside": 0.0,
                "slope_buffer_1km": 1.0,
                "slope_buffer_5km": 0.0,
            },
            {
                "pa_id": "pa2",
                "metric": "mean",
                "buffer_type": "land_unprotected",
                "n_years_inside": 7,
                "slope_inside": 9.0,
                "slope_buffer_1km": 9.0,
                "slope_buffer_5km": 9.0,
            },
            {
                "pa_id": "pa3",
                "metric": "mean",
                "buffer_type": "land_unprotected",
                "n_years_inside": 8,
                "slope_inside": 2.0,
                "slope_buffer_1km": -1.0,
                "slope_buffer_5km": None,
            },
            {
                "pa_id": "pa3",
                "metric": "median",
                "buffer_type": "land_unprotected",
                "n_years_inside": 8,
                "slope_inside": 99.0,
                "slope_buffer_1km": 99.0,
                "slope_buffer_5km": 99.0,
            },
        ]
    )
    risk = pd.DataFrame(
        [
            {"pa_id": "pa1", "slope_inside": 0.0, "slope_buffer_1km": 1.0},
            {"pa_id": "pa3", "slope_inside": 2.0, "slope_buffer_1km": -1.0},
        ]
    )

    rows = build_denominator_rows(
        geoms=geoms,
        radiance=radiance,
        edge_profiles=edge_profiles,
        buffer_validity=buffer_validity,
        trends=trends,
        risk=risk,
    )
    notes = validate_rows(rows)

    assert _row(rows, "pa_universe")["n"] == 3
    assert _row(rows, "inside_2024_eligible")["n"] == 2
    assert _row(rows, "inside_2024_zero_mean")["n"] == 1
    assert _row(rows, "inside_trend_eligible")["n"] == 2
    assert _row(rows, "inside_trend_zero_slope")["n"] == 1
    assert _row(rows, "buffer1_2024_valid")["n"] == 1
    assert _row(rows, "retention_quadrant_eligible")["n"] == 2
    assert _row(rows, "quadrant_q2_internal_brightening")["n"] == 1
    assert _row(rows, "quadrant_q4_external_pressure")["n"] == 1
    assert _row(rows, "complete_rings_2024")["n"] == 1
    assert "Inside eligible + ineligible equals PA universe." in notes

    report = render_report(rows, notes)
    assert "| key | label | n | denominator_n | percent | selection_rule | notes |" in report
    assert "inside_2024_eligible" in report

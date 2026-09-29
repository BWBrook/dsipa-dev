from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[2] / "analysis"))

from audit_edge_followup import (  # noqa: E402
    area_terciles,
    annual_status_summary,
    matched_1205,
    ring_annual,
    ring_slopes,
)


def _edge() -> pd.DataFrame:
    rows = []
    histories = {
        "a": ([0] * 8, [0] * 8),
        "b": ([1] * 8, [1] * 8),
        "c": (list(range(8)), list(range(8))),
    }
    for pa_id, (near, band) in histories.items():
        for year, values in enumerate(zip(near, band), start=2013):
            rows.extend(
                [
                    {"pa_id": pa_id, "ring_inner_km": 0.0, "ring_outer_km": 1.0, "year": year, "valid_pixel_count": 10, "mean": values[0]},
                    {"pa_id": pa_id, "ring_inner_km": 1.0, "ring_outer_km": 5.0, "year": year, "valid_pixel_count": 10, "mean": values[1]},
                ]
            )
    return pd.DataFrame(rows)


def _trends() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"pa_id": pa_id, "metric": "mean", "buffer_type": "land_unprotected", "n_years_inside": 8, "slope_inside": slope, "slope_buffer_1km": 1.0}
            for pa_id, slope in [("a", 0.0), ("b", 0.2), ("c", 0.4)]
        ]
    )


def test_zero_slope_is_distinguished_from_all_zero_history() -> None:
    annual = ring_annual(_edge(), 1.0, 5.0)
    slopes = ring_slopes(annual, "ring_1_5km").set_index("pa_id")
    assert slopes.loc["a", "slope_ring_1_5km"] == 0
    assert slopes.loc["a", "all_annual_zero_ring_1_5km"]
    assert slopes.loc["b", "slope_ring_1_5km"] == 0
    assert not slopes.loc["b", "all_annual_zero_ring_1_5km"]
    assert slopes.loc["b", "any_annual_nonzero_ring_1_5km"]


def test_same_band_cohort_and_sign_fields_are_spatially_separate() -> None:
    matched, annual = matched_1205(_trends(), _edge())
    assert set(matched.pa_id) == {"a", "b", "c"}
    assert set(matched.ring_1_5km_sign) == {"zero", "positive"}
    assert set(matched.ring_0_1km_sign) == {"zero", "positive"}
    assert len(annual) == 24


def test_annual_summary_has_explicit_status_categories() -> None:
    annual = ring_annual(_edge(), 1.0, 5.0)
    summary = annual_status_summary(annual, "1--5 km")
    assert set(summary.status) == {"all_annual_zero", "has_positive_year"}
    assert int(summary.n.sum()) == 3


def test_tercile_boundary_ties_are_kept_in_lower_group() -> None:
    trends = pd.DataFrame(
        [{"pa_id": str(i), "metric": "mean", "buffer_type": "land_unprotected", "n_years_inside": 8, "slope_inside": float(value)} for i, value in enumerate([1, 1, 2, 3, 4, 5])]
    )
    geometries = pd.DataFrame({"pa_id": [str(i) for i in range(6)], "area_km2": [1] * 6})
    summary, meta = area_terciles(trends, geometries)
    assert int(summary.n.sum()) == 6
    assert meta["details"]["tie_rule"].startswith("Values equal")

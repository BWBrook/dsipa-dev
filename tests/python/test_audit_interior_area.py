from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[2] / "analysis"))

from audit_interior_area import (
    area_summary,
    matched_slopes,
    primary_paired_cohort,
    quadrant,
    ring_slopes,
    transition_table,
)


def _trends() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"pa_id": "a", "metric": "mean", "buffer_type": "land_unprotected", "n_years_inside": 8, "slope_inside": 1.0, "slope_buffer_1km": 1.0, "slope_buffer_5km": 1.0},
            {"pa_id": "b", "metric": "mean", "buffer_type": "land_unprotected", "n_years_inside": 8, "slope_inside": 1.0, "slope_buffer_1km": -1.0, "slope_buffer_5km": -1.0},
            {"pa_id": "c", "metric": "mean", "buffer_type": "land_unprotected", "n_years_inside": 8, "slope_inside": -1.0, "slope_buffer_1km": 1.0, "slope_buffer_5km": 1.0},
            {"pa_id": "d", "metric": "mean", "buffer_type": "land_unprotected", "n_years_inside": 7, "slope_inside": 2.0, "slope_buffer_1km": 2.0, "slope_buffer_5km": 2.0},
        ]
    )


def _edge() -> pd.DataFrame:
    rows = []
    for pa_id, values in {"a": list(range(8)), "b": list(range(7, -1, -1)), "c": [0] * 8}.items():
        for year, value in enumerate(values, start=2013):
            rows.append({"pa_id": pa_id, "ring_inner_km": 1.0, "ring_outer_km": 5.0, "year": year, "valid_pixel_count": 10, "mean": value})
    rows.append({"pa_id": "a", "ring_inner_km": 0.0, "ring_outer_km": 1.0, "year": 2013, "valid_pixel_count": 10, "mean": 99})
    rows.append({"pa_id": "b", "ring_inner_km": 1.0, "ring_outer_km": 5.0, "year": 2017, "valid_pixel_count": 9, "mean": 99})
    return pd.DataFrame(rows)


def test_quadrant_boundary_matches_main_convention() -> None:
    assert [quadrant(b, i) for b, i in [(1, 1), (-1, 1), (-1, -1), (1, 0)]] == ["Q1", "Q2", "Q3", "Q4"]


def test_ring_slopes_apply_pixel_and_year_thresholds() -> None:
    slopes = ring_slopes(_edge())
    assert set(slopes.pa_id) == {"a", "b", "c"}
    assert slopes.set_index("pa_id").loc["a", "slope_ring_1_5km"] == 1.0
    assert slopes.set_index("pa_id").loc["b", "slope_ring_1_5km"] == -1.0


def test_matched_cohort_keeps_original_pairing_and_excludes_missing_ring() -> None:
    matched = matched_slopes(_trends(), _edge())
    assert list(primary_paired_cohort(_trends()).pa_id) == ["a", "b", "c"]
    assert matched.ring_included.sum() == 3
    assert set(matched.original_quadrant) == {"Q1", "Q2", "Q4"}
    assert set(matched.ring_quadrant) == {"Q1", "Q3", "Q4"}


def test_transition_and_area_summary_preserve_denominators() -> None:
    trends = _trends()
    matched = matched_slopes(trends, _edge())
    geometry = pd.DataFrame({"pa_id": ["a", "b", "c", "d", "e"], "area_km2": [1, 2, 3, 4, 5]})
    transitions = transition_table(matched, geometry)
    assert int(transitions.n.sum()) == 3
    areas = area_summary(trends, geometry)
    assert int(areas.loc[areas.category == "all_geometry_ids", "n"].iat[0]) == 5
    assert int(areas.loc[areas.category == "ineligible", "n"].iat[0]) == 2
    assert int(areas.loc[areas.category == "eligible_positive", "n"].iat[0]) == 2

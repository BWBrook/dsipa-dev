from __future__ import annotations

import pandas as pd

from dsipa.layerA_buffer_sensitivity import build_sensitivity, validate_sensitivity


def test_buffer_validity_sensitivity_keeps_nested_quadrants() -> None:
    risk = pd.DataFrame(
        [
            {"pa_id": "a", "slope_inside": 1.0, "slope_buffer_1km": 2.0, "retention_index_1km": -1.0},
            {"pa_id": "b", "slope_inside": 1.0, "slope_buffer_1km": -1.0, "retention_index_1km": 2.0},
            {"pa_id": "c", "slope_inside": -1.0, "slope_buffer_1km": -2.0, "retention_index_1km": 1.0},
            {"pa_id": "d", "slope_inside": -1.0, "slope_buffer_1km": 1.0, "retention_index_1km": -2.0},
        ]
    )
    validity = pd.DataFrame(
        [
            {"pa_id": "a", "buffer_km": 1.0, "land_fraction": 0.9, "protected_overlap_fraction": 0.1},
            {"pa_id": "b", "buffer_km": 1.0, "land_fraction": 0.4, "protected_overlap_fraction": 0.1},
            {"pa_id": "c", "buffer_km": 1.0, "land_fraction": 0.8, "protected_overlap_fraction": 0.4},
            {"pa_id": "d", "buffer_km": 1.0, "land_fraction": 0.7, "protected_overlap_fraction": 0.2},
        ]
    )

    summary = build_sensitivity(risk, validity)
    notes = validate_sensitivity(summary)
    primary = summary[summary["scenario"] == "primary_retention_quadrant"].iloc[0]
    strict = summary[summary["scenario"] == "land_ge_0.50_and_overlap_le_0.25"].iloc[0]

    assert primary["n"] == 4
    assert primary["q1_concurrent_brightening"] == 1
    assert primary["q2_internal_brightening"] == 1
    assert primary["q3_stable_non_detect"] == 1
    assert primary["q4_external_pressure"] == 1
    assert strict["n"] == 2
    assert strict["q1_concurrent_brightening"] == 1
    assert strict["q4_external_pressure"] == 1
    assert "Quadrant counts sum to each scenario denominator." in notes

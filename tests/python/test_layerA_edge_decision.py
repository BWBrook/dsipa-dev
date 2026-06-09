from __future__ import annotations

import pandas as pd

from dsipa.layerA_edge_decision import build_edge_summary, validate_edge_summary


def test_edge_decision_flags_complete_ring_limitations() -> None:
    df = pd.DataFrame(
        [
            {"pa_id": "a", "year": 2024, "ring_index": 0, "ring_inner_km": 0, "ring_outer_km": 1, "valid_pixel_count": 10, "frac_gt0": 0.0, "mean": 0.0},
            {"pa_id": "a", "year": 2024, "ring_index": 1, "ring_inner_km": 1, "ring_outer_km": 5, "valid_pixel_count": 10, "frac_gt0": 0.0, "mean": 0.0},
            {"pa_id": "a", "year": 2024, "ring_index": 2, "ring_inner_km": 5, "ring_outer_km": 10, "valid_pixel_count": 10, "frac_gt0": 0.0, "mean": 0.0},
            {"pa_id": "b", "year": 2024, "ring_index": 0, "ring_inner_km": 0, "ring_outer_km": 1, "valid_pixel_count": 10, "frac_gt0": 0.2, "mean": 1.0},
            {"pa_id": "b", "year": 2024, "ring_index": 1, "ring_inner_km": 1, "ring_outer_km": 5, "valid_pixel_count": 0, "frac_gt0": 0.0, "mean": 0.0},
            {"pa_id": "b", "year": 2024, "ring_index": 2, "ring_inner_km": 5, "ring_outer_km": 10, "valid_pixel_count": 0, "frac_gt0": 0.0, "mean": 0.0},
        ]
    )

    summary = build_edge_summary(df)
    notes = validate_edge_summary(summary)

    assert summary.loc[summary["ring_index"] == 0, "valid_pa_n"].iloc[0] == 2
    assert summary.loc[summary["ring_index"] == 2, "valid_pa_n"].iloc[0] == 1
    assert summary["complete_pa_n"].iloc[0] == 1
    assert "Complete-ring median frac_gt0 is zero in all rings, so median profiles are not interpretable as absence of edge effect." in notes

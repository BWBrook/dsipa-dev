from __future__ import annotations

import pandas as pd

from dsipa.layerA_watchlists import (
    build_dominance_summary,
    build_watchlists,
    validate_dominance_summary,
    validate_watchlists,
)


def _risk_fixture() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "pa_id": "a",
                "name": "Alpha",
                "state": "WA",
                "area_km2": 10.0,
                "distance_km": 20.0,
                "slope_inside": 2.0,
                "slope_buffer_1km": 1.0,
                "slope_buffer_5km": 0.5,
                "retention_index_1km": 1.0,
                "retention_index_5km": 1.5,
                "rank_inside_brightening": 1,
                "rank_external_pressure_1km": pd.NA,
                "rank_internalisation_1km": 1,
            },
            {
                "pa_id": "b",
                "name": "Beta",
                "state": "NSW",
                "area_km2": 8.0,
                "distance_km": 40.0,
                "slope_inside": 1.0,
                "slope_buffer_1km": 2.0,
                "slope_buffer_5km": 1.0,
                "retention_index_1km": -1.0,
                "retention_index_5km": 0.0,
                "rank_inside_brightening": 2,
                "rank_external_pressure_1km": pd.NA,
                "rank_internalisation_1km": pd.NA,
            },
            {
                "pa_id": "c",
                "name": "Gamma",
                "state": "SA",
                "area_km2": 6.0,
                "distance_km": 60.0,
                "slope_inside": 0.0,
                "slope_buffer_1km": 0.7,
                "slope_buffer_5km": 0.3,
                "retention_index_1km": -0.7,
                "retention_index_5km": -0.3,
                "rank_inside_brightening": pd.NA,
                "rank_external_pressure_1km": 1,
                "rank_internalisation_1km": pd.NA,
            },
        ]
    )


def _bootstrap_fixture() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "pa_id": "a",
                "ibra_code": "SWA",
                "ibra_name": "Swan Coastal Plain",
                "slope_full": 2.0,
                "slope_median": 1.8,
                "slope_ci_low": 0.5,
                "slope_ci_high": 3.0,
                "prob_slope_gt0": 0.99,
                "n_boot": 300,
            },
            {
                "pa_id": "b",
                "ibra_code": "SYB",
                "ibra_name": "Sydney Basin",
                "slope_full": 1.0,
                "slope_median": 0.9,
                "slope_ci_low": -0.1,
                "slope_ci_high": 2.0,
                "prob_slope_gt0": 0.8,
                "n_boot": 300,
            },
            {
                "pa_id": "c",
                "ibra_code": "EYB",
                "ibra_name": "Eyre Yorke Block",
                "slope_full": 0.0,
                "slope_median": 0.0,
                "slope_ci_low": -0.2,
                "slope_ci_high": 0.2,
                "prob_slope_gt0": 0.2,
                "n_boot": 300,
            },
        ]
    )


def test_watchlists_join_uncertainty_and_preserve_category_rules() -> None:
    watchlists = build_watchlists(_risk_fixture(), _bootstrap_fixture(), top_n=2)
    notes = validate_watchlists(watchlists, top_n=2)

    assert set(watchlists["category_key"]) == {
        "inside_brightening",
        "external_pressure",
        "internalisation",
    }
    assert watchlists.loc[watchlists["pa_id"] == "a", "inside_prob_slope_gt0"].iloc[0] == 0.99
    assert "Category filters match the risk-ranking definitions." in notes


def test_dominance_summary_reports_pairwise_stability_counts() -> None:
    dominance = pd.DataFrame(
        [[0.5, 0.8], [0.2, 0.5]],
        index=["a", "b"],
        columns=["a", "b"],
    )

    summary = build_dominance_summary(dominance, _risk_fixture(), _bootstrap_fixture())
    notes = validate_dominance_summary(summary)

    assert summary.iloc[0]["pa_id"] == "a"
    assert summary.iloc[0]["dominance_gt_0_75_count"] == 1
    assert "Dominance matrix is square and bounded in [0,1]." in notes

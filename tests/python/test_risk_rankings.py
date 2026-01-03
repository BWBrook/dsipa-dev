from pathlib import Path

import pandas as pd
import pytest

from dsipa import schema as dschema


def test_risk_rankings_schema_and_ranks():
    if not Path(dschema.PA_RISK_RANKINGS_CSV).exists():
        pytest.skip("Risk rankings not present; regenerate via pipeline.")
    df = pd.read_csv(dschema.PA_RISK_RANKINGS_CSV)
    assert set(df.columns) == set(dschema.PA_RISK_RANKINGS_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    ranks = [
        "rank_inside_brightening",
        "rank_buffer_brightening_1km",
        "rank_internalisation_1km",
        "rank_external_pressure_1km",
    ]
    for col in ranks:
        if df[col].notna().any():
            assert df[col].dropna().min() >= 1

    inside_ranked = df["rank_inside_brightening"].notna()
    if inside_ranked.any():
        assert (df.loc[inside_ranked, "slope_inside"] > 0).all()

    buffer_ranked = df["rank_buffer_brightening_1km"].notna()
    if buffer_ranked.any():
        assert (df.loc[buffer_ranked, "slope_buffer_1km"] > 0).all()

    internal_ranked = df["rank_internalisation_1km"].notna()
    if internal_ranked.any():
        assert (df.loc[internal_ranked, "slope_inside"] > df.loc[internal_ranked, "slope_buffer_1km"]).all()
        assert (df.loc[internal_ranked, "slope_inside"] > 0).all()

    external_ranked = df["rank_external_pressure_1km"].notna()
    if external_ranked.any():
        assert (df.loc[external_ranked, "slope_buffer_1km"] > 0).all()
        assert (df.loc[external_ranked, "slope_inside"] <= 0).all()

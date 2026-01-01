import pandas as pd

from dsipa import schema as dschema


def test_risk_rankings_schema_and_ranks():
    df = pd.read_csv(dschema.PA_RISK_RANKINGS_CSV)
    assert set(df.columns) == set(dschema.PA_RISK_RANKINGS_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    assert df["rank_slope_inside"].min() >= 1
    assert df["rank_retention_1km"].min() >= 1

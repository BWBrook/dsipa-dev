from pathlib import Path

import pandas as pd

from dsipa import schema as dschema


def test_ibra_assignment_schema_if_present():
    path = Path(dschema.PA_IBRA_ASSIGNMENT_CSV)
    if not path.exists():
        return
    df = pd.read_csv(path)
    assert set(df.columns) == set(dschema.PA_IBRA_ASSIGNMENT_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    assert df["ibra_share"].dropna().between(0, 1).all()


def test_trend_bootstrap_summary_schema_if_present():
    path = Path(dschema.PA_TREND_BOOTSTRAP_SUMMARY_CSV)
    if not path.exists():
        return
    df = pd.read_csv(path)
    assert set(df.columns) == set(dschema.PA_TREND_BOOTSTRAP_SUMMARY_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    assert df["prob_slope_gt0"].dropna().between(0, 1).all()

import pandas as pd

from dsipa import schema as dschema


def test_trends_schema_and_retention():
    df = pd.read_csv(dschema.PA_TRENDS_CSV)
    assert set(df.columns) == set(dschema.PA_TRENDS_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    diff_1km = df["slope_inside"] - df["slope_buffer_1km"]
    diff_5km = df["slope_inside"] - df["slope_buffer_5km"]
    assert (diff_1km.fillna(0).round(6) == df["retention_index_1km"].fillna(0).round(6)).all()
    assert (diff_5km.fillna(0).round(6) == df["retention_index_5km"].fillna(0).round(6)).all()

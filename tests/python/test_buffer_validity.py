import pandas as pd

from dsipa import schema as dschema


def test_buffer_validity_schema_and_ranges():
    df = pd.read_csv(dschema.PA_BUFFER_VALIDITY_CSV)
    assert set(df.columns) == set(dschema.PA_BUFFER_VALIDITY_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    assert (df["land_fraction"].between(0, 1)).all()
    assert (df["protected_overlap_fraction"].between(0, 1)).all()
    assert (df["effective_land_area_km2"] <= df["land_area_km2"] + 1e-6).all()
    assert (df["land_area_km2"] <= df["buffer_area_km2"] + 1e-6).all()
    subset = df[df["buffer_km"] == 5.0]
    if not subset.empty:
        assert subset["land_fraction"].quantile(0.9) > 0.9

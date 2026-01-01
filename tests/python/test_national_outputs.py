import pandas as pd

from dsipa import schema as dschema


def test_national_radiance_schema_and_counts():
    df = pd.read_csv(dschema.RADIANCE_BUFFERS_NATIONAL_CSV)
    assert set(df.columns) == set(dschema.RADIANCE_BUFFERS_NATIONAL_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    n_pa = df["pa_id"].nunique()
    n_years = df["year"].nunique()
    inside = df[df["zone"] == "inside"]
    buffers = df[df["zone"] == "buffer"]
    assert len(inside) == n_pa * n_years
    buffer_distances = buffers["buffer_km"].unique().tolist()
    assert len(buffers) == n_pa * n_years * len(buffer_distances)
    assert (df["valid_fraction"] >= 0).all()
    assert (df["valid_fraction"] <= 1).all()


def test_national_edge_profiles_schema_and_counts():
    df = pd.read_csv(dschema.EDGE_PROFILES_NATIONAL_CSV)
    assert set(df.columns) == set(dschema.EDGE_PROFILES_NATIONAL_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    n_pa = df["pa_id"].nunique()
    n_years = df["year"].nunique()
    n_rings = df["ring_index"].nunique()
    assert len(df) == n_pa * n_years * n_rings
    assert (df["valid_fraction"] >= 0).all()
    assert (df["valid_fraction"] <= 1).all()

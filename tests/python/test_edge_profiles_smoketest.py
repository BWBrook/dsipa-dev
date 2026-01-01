import pandas as pd

from dsipa import schema as dschema

EDGE_TABLE = dschema.EDGE_PROFILES_SMOKETEST_CSV
EXPECTED_COLUMNS = set(dschema.EDGE_PROFILES_SMOKETEST_COLUMNS)

EXPECTED_RINGS = [(0.0, 1.0), (1.0, 5.0), (5.0, 10.0)]


def test_edge_profile_schema_and_rows():
    df = pd.read_csv(EDGE_TABLE)
    assert set(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 27
    assert set(df["year"]) == {2013, 2018, 2024}
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}


def test_edge_profile_ring_bins_ordered():
    df = pd.read_csv(EDGE_TABLE)
    for (pa_id, year), subset in df.groupby(["pa_id", "year"]):
        subset = subset.sort_values("ring_index")
        bins = list(zip(subset["ring_inner_km"], subset["ring_outer_km"]))
        assert bins == EXPECTED_RINGS


def test_edge_profile_valid_fraction_bounds():
    df = pd.read_csv(EDGE_TABLE)
    assert (df["valid_fraction"] >= 0).all()
    assert (df["valid_fraction"] <= 1).all()

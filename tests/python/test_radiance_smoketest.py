import pandas as pd

from dsipa import schema as dschema

RAD_TABLE = dschema.RADIANCE_BUFFERS_SMOKETEST_CSV
EXPECTED_COLUMNS = set(dschema.RADIANCE_BUFFERS_SMOKETEST_COLUMNS)


def test_radiance_smoketest_schema_and_rows():
    df = pd.read_csv(RAD_TABLE)
    assert set(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 27
    assert set(df["zone"]) == {"inside", "buffer"}
    assert set(df["year"]) == {2013, 2018, 2024}
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}


def test_radiance_smoketest_valid_counts():
    df = pd.read_csv(RAD_TABLE)
    assert (df["valid_pixel_count"] > 0).all()
    assert (df["valid_fraction"] > 0).all()
    assert (df["valid_fraction"] <= 1).all()


def test_radiance_smoketest_buffer_km_nan_for_inside():
    df = pd.read_csv(RAD_TABLE)
    inside = df[df["zone"] == "inside"]
    buffer = df[df["zone"] == "buffer"]
    assert inside["buffer_km"].isna().all()
    assert buffer["buffer_km"].notna().all()
    assert set(inside["buffer_type"]) == {"inside"}
    assert set(buffer["buffer_type"]) == {"raw"}

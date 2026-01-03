from pathlib import Path

import pandas as pd
import pytest

from dsipa import schema as dschema


def test_national_radiance_schema_and_counts():
    if not Path(dschema.RADIANCE_BUFFERS_NATIONAL_CSV).exists():
        pytest.skip("National radiance outputs not present; regenerate via pipeline.")
    df = pd.read_csv(dschema.RADIANCE_BUFFERS_NATIONAL_CSV)
    assert set(df.columns) == set(dschema.RADIANCE_BUFFERS_NATIONAL_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    n_pa = df["pa_id"].nunique()
    n_years = df["year"].nunique()
    inside = df[df["zone"] == "inside"]
    buffers = df[df["zone"] == "buffer"]
    assert len(inside) == n_pa * n_years
    assert set(inside["buffer_type"]) == {"inside"}
    buffer_distances = buffers["buffer_km"].unique().tolist()
    raw_buffers = buffers[buffers["buffer_type"] == "raw"]
    assert len(raw_buffers) == n_pa * n_years * len(buffer_distances)
    assert (df["valid_fraction"] >= 0).all()
    assert (df["valid_fraction"] <= 1).all()
    if "frac_gt0" in df.columns:
        assert (df["frac_gt0"].dropna() >= 0).all()
        assert (df["frac_gt0"].dropna() <= 1).all()
    if "p95" in df.columns:
        valid = df.dropna(subset=["p95", "median", "min"])
        assert (valid["p95"] >= valid["median"]).all()
        assert (valid["median"] >= valid["min"]).all()

    low_valid = df[df["valid_pixel_count"] < 10]
    if not low_valid.empty:
        assert low_valid["mean"].isna().all()
        assert low_valid["median"].isna().all()
        assert low_valid["frac_gt0"].isna().all()
        assert low_valid["p95"].isna().all()


def test_national_edge_profiles_schema_and_counts():
    if not Path(dschema.EDGE_PROFILES_NATIONAL_CSV).exists():
        pytest.skip("National edge profiles not present; regenerate via pipeline.")
    df = pd.read_csv(dschema.EDGE_PROFILES_NATIONAL_CSV)
    assert set(df.columns) == set(dschema.EDGE_PROFILES_NATIONAL_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}
    n_pa = df["pa_id"].nunique()
    n_years = df["year"].nunique()
    n_rings = df["ring_index"].nunique()
    assert len(df) == n_pa * n_years * n_rings
    assert (df["valid_fraction"] >= 0).all()
    assert (df["valid_fraction"] <= 1).all()
    if "frac_gt0" in df.columns:
        assert (df["frac_gt0"].dropna() >= 0).all()
        assert (df["frac_gt0"].dropna() <= 1).all()
    if "p95" in df.columns:
        valid = df.dropna(subset=["p95", "median", "min"])
        assert (valid["p95"] >= valid["median"]).all()
        assert (valid["median"] >= valid["min"]).all()

import pandas as pd

from dsipa import schema as dschema


def test_inside_valid_fraction_reasonable():
    df = pd.read_csv(dschema.RADIANCE_BUFFERS_NATIONAL_CSV)
    inside = df[df["zone"] == "inside"]
    frac_valid = (inside["valid_pixel_count"] >= 10).mean()
    assert 0.2 < frac_valid < 0.7


def test_scale_metadata_by_year():
    df = pd.read_csv(dschema.RADIANCE_BUFFERS_NATIONAL_CSV)
    inside = df[df["zone"] == "inside"]
    scale_by_year = inside.groupby("year")["scale_metadata"].median()
    if not scale_by_year.empty:
        early = scale_by_year[scale_by_year.index <= 2021].round(1)
        late = scale_by_year[scale_by_year.index >= 2022].round(1)
        assert (early == 1.0).all()
        assert (late == 10.0).all()


def test_ring_usability_low_fraction():
    df = pd.read_csv(dschema.EDGE_PROFILES_NATIONAL_CSV)
    valid = df[df["valid_pixel_count"] >= 10]
    if valid.empty:
        return
    n_rings = df["ring_index"].nunique()
    complete = valid.groupby(["pa_id", "year"])["ring_index"].nunique()
    frac_complete = (complete == n_rings).mean()
    assert frac_complete < 0.2

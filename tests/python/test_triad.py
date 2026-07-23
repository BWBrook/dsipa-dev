import geopandas as gpd
import pandas as pd
import pytest

from dsipa import schema as dschema
from dsipa.triad import build_buffers

TRIAD_INDEX = dschema.TRIAD_INDEX_CSV
TRIAD_GEOMS = dschema.TRIAD_GEOMS_GPKG
TRIAD_RINGS = dschema.TRIAD_RINGS_CSV
TRIAD_BUFFERS = dschema.TRIAD_BUFFERS_GPKG

EXPECTED_IDS = {"TAS_50483", "NSW_N0856", "QLD_0117LZI001"}
EXPECTED_ROLES = {"urban_edge", "peri_urban", "remote"}
EXPECTED_RING_BINS = [(0.0, 1.0), (1.0, 5.0), (5.0, 10.0)]
EXPECTED_BUFFER_KM = {1.0, 5.0}
OFFLINE_FIXTURE = "tests/fixtures/layerA_triad/triad_geometries.geojson"


@pytest.fixture
def offline_triad(monkeypatch):
    def network_forbidden(*_args, **_kwargs):
        raise AssertionError("Layer A triad QA attempted network access.")

    monkeypatch.setattr("urllib.request.urlretrieve", network_forbidden)
    monkeypatch.setattr("dsipa.capad.fetch_gdf", network_forbidden)
    return gpd.read_file(OFFLINE_FIXTURE).to_crs("EPSG:3577")


def test_triad_index_schema_and_ids():
    df = pd.read_csv(TRIAD_INDEX)
    assert len(df) == 3
    assert set(df["triad_role"]) == EXPECTED_ROLES
    assert set(df["pa_id"]) == EXPECTED_IDS
    assert set(df.columns) == set(dschema.TRIAD_INDEX_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}


def test_triad_geometries_valid_offline(offline_triad, tmp_path):
    fixture_path = tmp_path / "triad_geometries.gpkg"
    offline_triad.to_file(fixture_path, driver="GPKG")
    gdf = gpd.read_file(fixture_path)
    assert len(gdf) == 3
    assert set(gdf.columns) == set(dschema.TRIAD_GEOMS_COLUMNS)
    assert gdf.geometry.notna().all()
    assert (~gdf.geometry.is_empty).all()
    assert gdf.is_valid.all()


def test_triad_ring_bins_complete_and_ordered():
    df = pd.read_csv(TRIAD_RINGS)
    assert len(df) == 9
    assert set(df.columns) == set(dschema.TRIAD_RINGS_COLUMNS)
    for pa_id in EXPECTED_IDS:
        subset = df[df["pa_id"] == pa_id].sort_values("ring_index")
        assert list(zip(subset["ring_inner_km"], subset["ring_outer_km"])) == EXPECTED_RING_BINS


def test_triad_buffers_complete_offline(offline_triad, tmp_path):
    buffers = build_buffers(offline_triad, sorted(EXPECTED_BUFFER_KM))
    fixture_path = tmp_path / "triad_buffers.gpkg"
    buffers.to_file(fixture_path, driver="GPKG")
    gdf = gpd.read_file(fixture_path)
    assert len(gdf) == 6
    assert set(gdf.columns) == set(dschema.TRIAD_BUFFERS_COLUMNS)
    assert set(gdf["buffer_km"]) == EXPECTED_BUFFER_KM

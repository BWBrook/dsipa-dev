import geopandas as gpd
import pandas as pd

from dsipa import schema as dschema

TRIAD_INDEX = dschema.TRIAD_INDEX_CSV
TRIAD_GEOMS = dschema.TRIAD_GEOMS_GPKG
TRIAD_RINGS = dschema.TRIAD_RINGS_CSV
TRIAD_BUFFERS = dschema.TRIAD_BUFFERS_GPKG

EXPECTED_IDS = {"TAS_50483", "NSW_N0856", "QLD_0117LZI001"}
EXPECTED_ROLES = {"urban_edge", "peri_urban", "remote"}
EXPECTED_RING_BINS = [(0.0, 1.0), (1.0, 5.0), (5.0, 10.0)]
EXPECTED_BUFFER_KM = {1.0, 5.0}


def test_triad_index_schema_and_ids():
    df = pd.read_csv(TRIAD_INDEX)
    assert len(df) == 3
    assert set(df["triad_role"]) == EXPECTED_ROLES
    assert set(df["pa_id"]) == EXPECTED_IDS
    assert set(df.columns) == set(dschema.TRIAD_INDEX_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}


def test_triad_geometries_valid():
    gdf = gpd.read_file(TRIAD_GEOMS)
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


def test_triad_buffers_complete():
    gdf = gpd.read_file(TRIAD_BUFFERS)
    assert len(gdf) == 6
    assert set(gdf.columns) == set(dschema.TRIAD_BUFFERS_COLUMNS)
    assert set(gdf["buffer_km"]) == EXPECTED_BUFFER_KM

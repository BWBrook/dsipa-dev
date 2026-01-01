import pandas as pd
import geopandas as gpd

TRIAD_INDEX = "data/processed/smoke_test_triad_index_v0_1_0.csv"
TRIAD_GEOMS = "data/processed/smoke_test_triad_geoms_v0_1_0.gpkg"
TRIAD_RINGS = "data/processed/smoke_test_triad_rings_v0_1_0.csv"
TRIAD_BUFFERS = "data/processed/smoke_test_triad_buffers_v0_1_0.gpkg"

EXPECTED_IDS = {"TAS_50483", "NSW_N0856", "QLD_0117LZI001"}
EXPECTED_ROLES = {"urban_edge", "peri_urban", "remote"}
EXPECTED_RING_BINS = [(0.0, 1.0), (1.0, 5.0), (5.0, 10.0)]
EXPECTED_BUFFER_KM = {1.0, 5.0}


def test_triad_index_schema_and_ids():
    df = pd.read_csv(TRIAD_INDEX)
    assert len(df) == 3
    assert set(df["triad_role"]) == EXPECTED_ROLES
    assert set(df["pa_id"]) == EXPECTED_IDS
    required_cols = {"schema_version", "triad_role", "pa_id", "name", "state", "area_km2", "distance_km"}
    assert required_cols.issubset(df.columns)


def test_triad_geometries_valid():
    gdf = gpd.read_file(TRIAD_GEOMS)
    assert len(gdf) == 3
    assert gdf.geometry.notna().all()
    assert (~gdf.geometry.is_empty).all()
    assert gdf.is_valid.all()


def test_triad_ring_bins_complete_and_ordered():
    df = pd.read_csv(TRIAD_RINGS)
    assert len(df) == 9
    for pa_id in EXPECTED_IDS:
        subset = df[df["pa_id"] == pa_id].sort_values("ring_index")
        assert list(zip(subset["ring_inner_km"], subset["ring_outer_km"])) == EXPECTED_RING_BINS


def test_triad_buffers_complete():
    gdf = gpd.read_file(TRIAD_BUFFERS)
    assert len(gdf) == 6
    assert set(gdf["buffer_km"]) == EXPECTED_BUFFER_KM

from pathlib import Path

import pandas as pd
import pytest

from dsipa import schema as dschema

PA_GEOM_CSV = dschema.PA_GEOMETRIES_CSV
PA_GEOM_GPKG = dschema.PA_GEOMETRIES_GPKG
EXPECTED_COLUMNS = set(dschema.PA_GEOMETRIES_COLUMNS)


def test_pa_geometry_files_exist():
    assert Path(PA_GEOM_CSV).exists()
    if not Path(PA_GEOM_GPKG).exists():
        pytest.skip("PA geometry GPKG not present; regenerate via pipeline.")
    assert Path(PA_GEOM_GPKG).exists()


def test_pa_geometry_ids_and_areas():
    df = pd.read_csv(PA_GEOM_CSV)
    assert set(df.columns) == EXPECTED_COLUMNS
    assert df["pa_id"].is_unique
    assert (df["area_km2"] > 0).all()
    assert (~df["geometry_empty"]).all()
    assert df["valid_fixed_all"].all()
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}

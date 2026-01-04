from pathlib import Path

import pandas as pd
import pytest

from dsipa import schema as dschema


def test_layerB_summary_schema_if_present():
    if not Path(dschema.LAYERB_OCCURRENCE_SUMMARY_CSV).exists():
        pytest.skip("Layer B summary not present; run layerB_data pipeline.")
    df = pd.read_csv(dschema.LAYERB_OCCURRENCE_SUMMARY_CSV)
    assert set(df.columns) == set(dschema.LAYERB_OCCURRENCE_SUMMARY_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}

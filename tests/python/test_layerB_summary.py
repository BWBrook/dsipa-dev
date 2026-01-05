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


def test_layerB_model_input_summary_schema_if_present():
    if not Path(dschema.LAYERB_MODEL_INPUT_SUMMARY_CSV).exists():
        pytest.skip("Layer B model input summary not present; run layerB_model pipeline.")
    df = pd.read_csv(dschema.LAYERB_MODEL_INPUT_SUMMARY_CSV)
    assert set(df.columns) == set(dschema.LAYERB_MODEL_INPUT_SUMMARY_COLUMNS)
    assert set(df["schema_version"]) == {dschema.SCHEMA_VERSION}

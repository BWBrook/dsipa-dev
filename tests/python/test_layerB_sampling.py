import numpy as np
import pandas as pd
from rasterio.io import MemoryFile
from rasterio.transform import from_origin

from dsipa.layerB_model import (
    LOGISTIC_C,
    LOGISTIC_MAX_ITER,
    LOGISTIC_PENALTY,
    LOGISTIC_SOLVER,
    MODEL_FEATURES,
    _mean_fold_metrics,
    _sample_raster,
)


def test_sample_raster_masks_raw_invalid_before_scale_offset():
    """Raw nodata/negative codes are missing, while 0 and positive are valid."""
    profile = {
        "driver": "GTiff",
        "height": 1,
        "width": 4,
        "count": 1,
        "dtype": "int16",
        "crs": "EPSG:4326",
        "transform": from_origin(0, 4, 1, 1),
        "nodata": -32768,
    }
    with MemoryFile() as memory:
        with memory.open(**profile) as writer:
            writer.write(np.array([[0, 1, -1, -32768]], dtype=np.int16), 1)
            writer.scales = (10.0,)
            writer.offsets = (0.0,)
        with memory.open() as dataset:
            lons, lats = zip(
                dataset.xy(0, 0),
                dataset.xy(0, 1),
                dataset.xy(0, 2),
                dataset.xy(0, 3),
            )
            sampled = _sample_raster(dataset, np.array(lons), np.array(lats))

    np.testing.assert_allclose(sampled[:2], [0.0, 10.0])
    assert np.isnan(sampled[2])
    assert np.isnan(sampled[3])


def test_sample_raster_outside_support_is_missing():
    profile = {
        "driver": "GTiff",
        "height": 1,
        "width": 1,
        "count": 1,
        "dtype": "int16",
        "crs": "EPSG:4326",
        "transform": from_origin(0, 1, 1, 1),
        "nodata": -32768,
    }
    with MemoryFile() as memory:
        with memory.open(**profile) as writer:
            writer.write(np.array([[2]], dtype=np.int16), 1)
            writer.scales = (10.0,)
            writer.offsets = (0.0,)
        with memory.open() as dataset:
            inside = dataset.xy(0, 0)
            sampled = _sample_raster(
                dataset,
                np.array([inside[0], 100.0]),
                np.array([inside[1], 100.0]),
            )

    np.testing.assert_allclose(sampled[0], 20.0)
    assert np.isnan(sampled[1])


def test_layerB_model_contract_is_explicit():
    assert MODEL_FEATURES == ("any_light", "log1p_alan")
    assert (LOGISTIC_PENALTY, LOGISTIC_C, LOGISTIC_SOLVER, LOGISTIC_MAX_ITER) == (
        "l2",
        1.0,
        "liblinear",
        200,
    )


def test_mean_fold_metrics_is_arithmetic_mean():
    metrics = pd.DataFrame(
        {
            "run": ["primary", "primary", "primary"],
            "fold": [1, 2, 3],
            "auc": [0.4, 0.5, 0.6],
            "log_loss": [0.9, 0.7, 0.8],
        }
    )
    summary = _mean_fold_metrics(metrics)
    np.testing.assert_allclose(summary.loc["primary"], [0.5, 0.8])

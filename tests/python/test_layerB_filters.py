import pandas as pd
from pyproj import Transformer

from dsipa.layerB_data import apply_quality_filters, dedupe_occurrences


def _base_df():
    return pd.DataFrame(
        {
            "decimalLatitude": [-35.0, -35.0],
            "decimalLongitude": [149.0, 149.0],
            "coordinateUncertaintyInMeters": [500, 1500],
            "taxonRank": ["species", "species"],
            "occurrenceStatus": ["present", "present"],
            "establishmentMeans": ["", ""],
            "eventDate": ["2020-01-01", "2020-01-01"],
            "species": ["Test species", "Test species"],
        }
    )


def test_apply_quality_filters_uncertainty():
    df = _base_df()
    filtered = apply_quality_filters(df, uncertainty_m=1000)
    assert len(filtered) == 1
    assert filtered["coordinateUncertaintyInMeters"].iloc[0] <= 1000


def test_apply_quality_filters_captive_excluded():
    df = _base_df()
    df.loc[0, "establishmentMeans"] = "captive"
    filtered = apply_quality_filters(df, uncertainty_m=1000)
    assert len(filtered) == 0


def test_dedupe_occurrences_grid():
    df = _base_df().iloc[[0]].copy()
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "decimalLatitude": [-35.0],
                    "decimalLongitude": [149.0],
                    "coordinateUncertaintyInMeters": [500],
                    "taxonRank": ["species"],
                    "occurrenceStatus": ["present"],
                    "establishmentMeans": [""],
                    "eventDate": ["2020-01-01"],
                    "species": ["Test species"],
                }
            ),
            pd.DataFrame(
                {
                    "decimalLatitude": [-35.0],
                    "decimalLongitude": [149.0],
                    "coordinateUncertaintyInMeters": [500],
                    "taxonRank": ["species"],
                    "occurrenceStatus": ["present"],
                    "establishmentMeans": [""],
                    "eventDate": ["2020-01-02"],
                    "species": ["Test species"],
                }
            ),
        ],
        ignore_index=True,
    )

    filtered = apply_quality_filters(df, uncertainty_m=1000)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
    deduped = dedupe_occurrences(filtered, transformer, set())
    # Two unique dates should remain
    assert len(deduped) == 2

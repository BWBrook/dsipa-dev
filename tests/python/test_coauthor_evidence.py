"""Protect the distinction between zero Sen slopes, variation and missingness."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.trends import _theil_sen


def test_late_observed_brightening_can_have_zero_sen_slope():
    years = np.arange(2013, 2025)
    values = np.array([0.] * 9 + [1., 2., 3.])
    assert _theil_sen(years, values)[0] == 0
    assert np.ptp(values) > 0


def test_series_flags_do_not_treat_missing_years_as_zero():
    path = Path(__file__).parents[2] / "analysis/coauthor_evidence.py"
    spec = importlib.util.spec_from_file_location("coauthor_evidence", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    values = pd.DataFrame([
        [0.] * 9 + [1., 2., 3.],
        [np.nan] + [0.] * 8 + [1., 2., 3.],
        [0.] * 12,
        [2.] * 12,
    ], columns=range(2013, 2025))
    flags = module.describe_zero_series(values)
    assert flags.any_variation.tolist() == [True, True, False, False]
    assert flags.late_positive_complete.tolist() == [True, False, False, False]
    assert flags.all_observed_zero.tolist() == [False, False, True, False]
    assert flags.valid_years.tolist() == [12, 11, 12, 12]

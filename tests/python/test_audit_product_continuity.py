import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
spec=importlib.util.spec_from_file_location('audit',Path(__file__).resolve().parents[2]/'analysis/audit_product_continuity.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_hazards_exclude_missing_and_prior_positive():
    x=pd.DataFrame(0.,index=['event','never','missing','already'],columns=m.YEARS)
    x.loc['event',2022]=1
    x.loc['missing',2018]=np.nan;x.loc['missing',2022]=1
    x.loc['already',2013]=1
    h=m.hazards(x).set_index('year')
    assert h.loc[2022,'at_risk']==2
    assert h.loc[2022,'first_positive']==1
    assert h.loc[2023,'at_risk']==1  # reversion does not re-enter risk set
    assert h.loc[2022,'hazard']==.5

def test_empty_risk_set_has_no_rate():
    x=pd.DataFrame(1.,index=['one'],columns=m.YEARS);x[2013]=0
    h=m.hazards(x).set_index('year')
    assert h.loc[2014,'hazard']==1
    assert h.loc[2015,'at_risk']==0 and pd.isna(h.loc[2015,'hazard'])

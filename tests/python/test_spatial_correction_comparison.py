import importlib.util
from pathlib import Path
import pandas as pd


def module():
    path=Path(__file__).resolve().parents[2]/'analysis/synthesise_spatial_correction.py'
    spec=importlib.util.spec_from_file_location('spatial_synthesis',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def test_comparison_separates_common_cohort_from_support_changes(tmp_path):
    m=module()
    old=pd.DataFrame({'pa_id':['a','b','c','d'],'slope_inside':[1,1,0,0],
                      'slope_buffer_1km':[1,0,float('nan'),1],
                      'slope_buffer_5km':[1,0,float('nan'),1]}).set_index('pa_id')
    new=old.copy()
    new['slope_buffer_1km']=[-1,float('nan'),2,1]
    result=m.comparison(old,new,'check',tmp_path)
    assert result['old_paired']==3 and result['new_paired']==3
    assert result['common']==2 and result['gained']==1 and result['lost']==1
    assert result['category_changed_common']==1
    transitions=pd.read_csv(tmp_path/'check_category_transitions.csv',index_col=0)
    assert transitions.loc['Q1','Q2']==1
    assert transitions.loc['Q2','ineligible']==1
    assert transitions.loc['ineligible','Q4']==1

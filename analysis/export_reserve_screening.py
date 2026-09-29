#!/usr/bin/env python3
"""Export reserve-level results with explicit coastline-validation status."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import pandas as pd


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();r=a.root;d=r/'data/processed';o=r/'analysis/reports'
 paths=[d/'pa_geometries_v0_3_0.csv',d/'pa_trends_v0_3_0.csv',o/'spatial_known_coastline_exceptions.csv']
 g,t,e=[pd.read_csv(f,float_precision='round_trip') for f in paths]
 t=t[t.metric.eq('mean')&t.buffer_type.eq('land_unprotected')]
 x=g[['pa_id','NAME','STATE','area_km2']].merge(t[['pa_id','slope_inside','slope_buffer_1km','slope_buffer_5km']],on='pa_id',how='left',validate='one_to_one')
 x['analysis_id']='spatial-correction-20260919';x['inside_eligible']=x.slope_inside.notna();x['paired_eligible']=x.inside_eligible&x.slope_buffer_1km.notna()
 x['coastline_exception_proximity']=x.pa_id.isin(set(e.pa_id))
 x['provisional_surrounding_comparison']=x.paired_eligible&x.coastline_exception_proximity
 x['validation_status']=np.select([~x.inside_eligible,~x.paired_eligible,x.provisional_surrounding_comparison],['insufficient_inside_support','insufficient_surrounding_support','provisional_requires_local_coastline_validation'],default='eligible_satellite_screen_requires_local_interpretation')
 i=x.slope_inside;b=x.slope_buffer_1km
 x['category']=np.select([x.paired_eligible&(i>0)&(b>0),x.paired_eligible&(i>0)&(b<=0),x.paired_eligible&(i<=0)&(b<=0),x.paired_eligible&(i<=0)&(b>0)],['Q1','Q2','Q3','Q4'],default='unavailable')
 assert len(x)==11133 and x.pa_id.is_unique
 x.sort_values('pa_id').to_csv(o/'reserve_screening_results.csv',index=False)
 included=x[x.paired_eligible];excluded=included[~included.provisional_surrounding_comparison]
 result={'flag_definition':'Within 5 km of a documented source-exception reference point; proximity is not proof of a support error. Flagged surrounding results require local map validation.', 'screened_ids':int(x.coastline_exception_proximity.sum()),'paired_provisional_n':int(included.provisional_surrounding_comparison.sum()),'paired_provisional_ids':included.loc[included.provisional_surrounding_comparison,'pa_id'].tolist(),'all_paired':{'n':len(included),'categories':included.category.value_counts().sort_index().to_dict()},'excluding_provisional':{'n':len(excluded),'categories':excluded.category.value_counts().sort_index().to_dict()},'inputs':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (o/'coastline_exception_sensitivity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

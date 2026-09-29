#!/usr/bin/env python3
"""Compare archived and corrected interior eligibility without mixing cohorts."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from audit_interior_area import ring_slopes, primary_paired_cohort


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def compare(old,new,universe,label,out):
    x=old.reindex(universe).rename('old_slope').to_frame().join(new.reindex(universe).rename('new_slope'))
    def sign(v):
        return np.select([v.gt(0),v.lt(0),v.eq(0)],['positive','negative','zero'],default='unavailable')
    x['old_sign']=sign(x.old_slope);x['new_sign']=sign(x.new_slope)
    common=x.old_slope.notna()&x.new_slope.notna()
    result={'old_eligible':int(x.old_slope.notna().sum()),'new_eligible':int(x.new_slope.notna().sum()),
            'common':int(common.sum()),'gained':int((x.old_slope.isna()&x.new_slope.notna()).sum()),
            'lost':int((x.old_slope.notna()&x.new_slope.isna()).sum()),
            'sign_changed_common':int((x.loc[common,'old_sign']!=x.loc[common,'new_sign']).sum()),
            'max_abs_slope_change_common':float((x.loc[common,'old_slope']-x.loc[common,'new_slope']).abs().max())}
    x.rename_axis('pa_id').to_csv(out/f'interior_correction_{label}_reserve_changes.csv')
    pd.crosstab(x.old_sign,x.new_sign).to_csv(out/f'interior_correction_{label}_sign_transitions.csv')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--corrected',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    inputs={};edges=[];bands=[];paired=[]
    for label,root in [('baseline',a.baseline),('corrected',a.corrected)]:
        paths={n:root/'data/processed'/n for n in ['pa_edge_profiles_national_v0_3_0.csv','pa_trends_v0_3_0.csv']}
        inputs[label]={n:{'sha256':sha(f),'bytes':f.stat().st_size} for n,f in paths.items()}
        edge=pd.read_csv(paths['pa_edge_profiles_national_v0_3_0.csv'],float_precision='round_trip');edges.append(edge)
        bands.append(ring_slopes(edge).set_index('pa_id').slope_ring_1_5km)
        paired.append(primary_paired_cohort(pd.read_csv(paths['pa_trends_v0_3_0.csv'],float_precision='round_trip')).set_index('pa_id'))
    universe=sorted(set(edges[0].pa_id)|set(edges[1].pa_id))
    result={'inputs':inputs,'all_reserves':compare(*bands,universe,'all_reserves',a.output),
       'fixed_common_paired':compare(*bands,sorted(set(paired[0].index)&set(paired[1].index)),'fixed_common_paired',a.output),
       'joint_paired_and_band':compare(bands[0].reindex(paired[0].index),bands[1].reindex(paired[1].index),universe,'joint_paired_and_band',a.output)}
    for label,edge in zip(['baseline','corrected'],edges):
        grey=edge[edge.pa_id.eq('QLD_0239GRP001')&edge.ring_inner_km.eq(1)&edge.ring_outer_km.eq(5)]
        grey.to_csv(a.output/f'interior_correction_grey_peaks_{label}.csv',index=False)
        result.setdefault('grey_peaks',{})[label]={'valid_pixel_counts':sorted(grey.valid_pixel_count.unique().tolist()),'usable_years':int(grey['mean'].notna().sum())}
    result['script_sha256']=sha(Path(__file__))
    (a.output/'interior_correction_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

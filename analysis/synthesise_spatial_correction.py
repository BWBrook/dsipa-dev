#!/usr/bin/env python3
"""Regenerate dependent results and compare the three spatial-support variants."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np
import pandas as pd
from dsipa.trends import build_trends
from dsipa.vulnerability_model import build_risk_dataset, build_risk_rankings
from dsipa import layerA_tables, layerA_buffer_sensitivity, layerA_threshold_sensitivity, layerA_edge_decision
from dsipa.layerA_watchlists import build_watchlists, validate_watchlists, render_watchlist_report


def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def categories(t):
    eligible=t.slope_inside.notna()&t.slope_buffer_1km.notna()
    return pd.Series(np.select([
        eligible&t.slope_inside.gt(0)&t.slope_buffer_1km.gt(0),
        eligible&t.slope_inside.gt(0)&t.slope_buffer_1km.le(0),
        eligible&t.slope_inside.le(0)&t.slope_buffer_1km.le(0),
        eligible&t.slope_inside.le(0)&t.slope_buffer_1km.gt(0)],['Q1','Q2','Q3','Q4'],default='ineligible'),index=t.index)


def primary(t):
    return t[t.metric.eq('mean')&t.buffer_type.eq('land_unprotected')].set_index('pa_id')


def run_variant(root,baseline,edge_path):
    data=root/'data/processed';reports=root/'analysis/reports';reports.mkdir(parents=True,exist_ok=True)
    geometry=data/'pa_geometries_v0_3_0.gpkg'
    if not geometry.exists():shutil.copy2(baseline/'data/processed'/geometry.name,geometry)
    if not (data/edge_path.name).exists():shutil.copy2(edge_path,data/edge_path.name)
    annual=pd.read_csv(data/'pa_radiance_buffers_national_v0_3_0.csv')
    trends=build_trends(annual)
    trends.sort_values(['pa_id','buffer_type','metric']).to_csv(data/'pa_trends_v0_3_0.csv',index=False)
    original=pd.read_csv(baseline/'data/processed/pa_trends_v0_3_0.csv')
    inside_columns=['pa_id','metric','buffer_type','n_years_inside','slope_inside','intercept_inside']
    old=original[inside_columns].sort_values(['pa_id','metric','buffer_type']).reset_index(drop=True)
    new=trends[inside_columns].sort_values(['pa_id','metric','buffer_type']).reset_index(drop=True)
    pd.testing.assert_frame_equal(old,new,check_exact=False,rtol=1e-12,atol=1e-12)
    risk=build_risk_rankings(build_risk_dataset(root));risk.sort_values('pa_id').to_csv(data/'pa_risk_rankings_v0_3_0.csv',index=False)
    inputs=layerA_tables.load_inputs(root);rows=layerA_tables.build_denominator_rows(**inputs)
    layerA_tables.write_outputs(root,rows,layerA_tables.validate_rows(rows))
    v=inputs['buffer_validity']
    sensitivity=layerA_buffer_sensitivity.build_sensitivity(risk,v)
    layerA_buffer_sensitivity.write_outputs(root,sensitivity,layerA_buffer_sensitivity.validate_sensitivity(sensitivity))
    edge=layerA_edge_decision.build_edge_summary(inputs['edge_profiles'])
    layerA_edge_decision.write_outputs(root,edge,layerA_edge_decision.validate_edge_summary(edge))
    bootstrap=pd.read_csv(data/'pa_trend_bootstrap_summary_v0_3_0.csv')
    watch=build_watchlists(risk,bootstrap);notes=validate_watchlists(watch)
    watch.to_csv(reports/'layerA_watchlists_uncertainty.csv',index=False)
    (reports/'layerA_watchlists_uncertainty.md').write_text(render_watchlist_report(watch,notes,top_n=20))
    print(json.dumps(dict(stage='variant',root=str(root),inside=len(primary(trends)),paired=len(risk))),flush=True)
    return primary(trends), risk, rows


def comparison(before,after,label,reports):
    joined=before[['slope_inside','slope_buffer_1km','slope_buffer_5km']].join(
        after[['slope_buffer_1km','slope_buffer_5km']],how='outer',lsuffix='_old',rsuffix='_new')
    joined['old_category']=categories(before).reindex(joined.index).fillna('ineligible')
    joined['new_category']=categories(after).reindex(joined.index).fillna('ineligible')
    joined['old_eligible']=joined.old_category.ne('ineligible');joined['new_eligible']=joined.new_category.ne('ineligible')
    joined['delta_buffer_1km']=joined.slope_buffer_1km_new-joined.slope_buffer_1km_old
    joined['delta_buffer_5km']=joined.slope_buffer_5km_new-joined.slope_buffer_5km_old
    joined.reset_index().to_csv(reports/f'{label}_reserve_changes.csv',index=False)
    table=pd.crosstab(joined.old_category,joined.new_category).reindex(index=['Q1','Q2','Q3','Q4','ineligible'],columns=['Q1','Q2','Q3','Q4','ineligible'],fill_value=0).fillna(0).astype(int)
    table.to_csv(reports/f'{label}_category_transitions.csv')
    common=joined[joined.old_eligible&joined.new_eligible]
    result=dict(old_paired=int(joined.old_eligible.sum()),new_paired=int(joined.new_eligible.sum()),
                common=len(common),gained=int((~joined.old_eligible&joined.new_eligible).sum()),
                lost=int((joined.old_eligible&~joined.new_eligible).sum()),
                category_changed_common=int(common.old_category.ne(common.new_category).sum()),
                max_abs_slope_delta=float(common.delta_buffer_1km.abs().max()),
                median_abs_slope_delta=float(common.delta_buffer_1km.abs().median()),
                categories=joined.new_category.value_counts().to_dict())
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--run',type=Path,required=True)
    a=p.parse_args();reports=a.run/'analysis/reports';reports.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((a.run/'extraction_manifest.json').read_text())
    for relative,meta in manifest['output_files'].items():
        if sha(a.run/relative)!=meta['sha256']:raise ValueError(f'Extraction output changed: {relative}')
    edge=a.run/'data/processed/pa_edge_profiles_national_v0_3_0.csv'
    corrected,risk,rows=run_variant(a.run,a.baseline,edge)
    geometry,_,_=run_variant(a.run/'geometry_only',a.baseline,edge)
    old=primary(pd.read_csv(a.baseline/'data/processed/pa_trends_v0_3_0.csv'))
    summary={label:comparison(first,second,label,reports) for label,first,second in [
        ('baseline_to_geometry',old,geometry),('geometry_to_corrected',geometry,corrected),('baseline_to_corrected',old,corrected)]}
    summary['variants']={label:dict(paired=int(categories(t).ne('ineligible').sum()),
        quadrants={q:int(categories(t).eq(q).sum()) for q in ['Q1','Q2','Q3','Q4']})
        for label,t in [('Baseline',old),('Geometry-only',geometry),('Corrected',corrected)]}
    summary['unchanged_inside']=dict(n=len(corrected),positive=int(corrected.slope_inside.gt(0).sum()),
        negative=int(corrected.slope_inside.lt(0).sum()),zero=int(corrected.slope_inside.eq(0).sum()))
    (reports/'spatial_correction_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    thresholds=layerA_threshold_sensitivity.build_sensitivity(pd.read_csv(a.run/'data/processed/pa_radiance_buffers_national_v0_3_0.csv'))
    layerA_threshold_sensitivity.write_outputs(a.run,thresholds,layerA_threshold_sensitivity.validate_sensitivity(thresholds))
    files={p.name:dict(sha256=sha(p),bytes=p.stat().st_size) for p in (a.run/'data/processed').glob('*') if p.is_file()}
    result=dict(analysis_id='spatial-correction-20260919',files=files,
        extraction_manifest_sha256=sha(a.run/'extraction_manifest.json'),synthesis_script_sha256=sha(Path(__file__)))
    (a.run/'input_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()

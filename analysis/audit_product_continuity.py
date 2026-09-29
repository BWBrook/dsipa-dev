#!/usr/bin/env python3
"""Prospectively amended continuity diagnostics; never modifies accepted inputs."""
from __future__ import annotations
import argparse, hashlib, json, platform, sys, shutil
from contextlib import ExitStack
from pathlib import Path
import numpy as np
import pandas as pd

try:
    from analysis.input_contract import legacy_contract, load_manifest, resolve_contract, sha256
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from input_contract import legacy_contract, load_manifest, resolve_contract, sha256

YEARS = list(range(2013, 2025))

def hazards(wide, strata=None):
    """Complete-series first-positive fractions; no missing-as-zero convention."""
    wide = wide.reindex(columns=YEARS)
    eligible = wide.notna().all(axis=1) & wide[2013].eq(0)
    w = wide.loc[eligible]
    groups = pd.Series('all', index=w.index) if strata is None else strata.reindex(w.index)
    rows = []
    for group in groups.dropna().unique():
        x = w.loc[groups.eq(group)]
        for year in YEARS[1:]:
            at_risk = x.loc[:, 2013:year-1].eq(0).all(axis=1)
            events = at_risk & x[year].gt(0)
            n, k = int(at_risk.sum()), int(events.sum())
            rows.append(dict(stratum=group, year=year, at_risk=n, first_positive=k,
                             hazard=k/n if n else None))
    return pd.DataFrame(rows)

def annual_audit(data, out, paths=None):
    cols=['pa_id','zone','buffer_km','buffer_type','year','mean','max','frac_gt0','valid_pixel_count']
    radiance = (paths or {}).get('pa_radiance_buffers_national_v0_3_0.csv', data/'pa_radiance_buffers_national_v0_3_0.csv')
    a=pd.read_csv(radiance,usecols=cols)
    a=a[a.zone.eq('inside') | (a.zone.eq('buffer') & a.buffer_type.eq('land_unprotected'))].copy()
    a.loc[a.valid_pixel_count.lt(10),['mean','max','frac_gt0']]=np.nan
    a['zone_label']=np.where(a.zone.eq('inside'),'inside',a.buffer_km.map(lambda x:f'buffer_{x:g}km'))
    allh=[]; exclusions=[]; series=[]
    for label, frame in a.groupby('zone_label'):
        if frame.duplicated(['pa_id','year']).any():
            raise ValueError(f'Duplicate PA-year rows in {label}')
        if not frame.year.isin(YEARS).all():
            raise ValueError(f'Years outside 2013--2024 in {label}')
        if frame.valid_pixel_count.lt(0).any():
            raise ValueError(f'Negative valid pixel counts in {label}')
        w=frame.pivot(index='pa_id',columns='year',values='mean').reindex(columns=YEARS)
        h=hazards(w);h['zone']=label;allh.append(h)
        complete=w.notna().all(axis=1)
        exclusions.append(dict(zone=label,total_ids=len(w),complete_series=int(complete.sum()),
            complete_baseline_zero=int((complete&w[2013].eq(0)).sum()),incomplete=int((~complete).sum())))
        first=w.gt(0).idxmax(axis=1).where(w.gt(0).any(axis=1))
        detail=w.loc[complete].copy();detail.columns=[f'mean_{y}' for y in YEARS]
        detail['first_positive_year']=first;detail['zone']=label
        series.append(detail.reset_index())
    pd.concat(allh).to_csv(out/'product_hazards.csv',index=False)
    pd.DataFrame(exclusions).to_csv(out/'product_cohort_coverage.csv',index=False)
    s=pd.concat(series,ignore_index=True)
    s.to_csv(out/'product_annual_series.csv',index=False)
    f=s[s.first_positive_year.eq(2022)]
    signature=f.merge(a[a.year.eq(2022)][['pa_id','zone_label','max','frac_gt0','valid_pixel_count']],
         left_on=['pa_id','zone'],right_on=['pa_id','zone_label'],validate='one_to_one')
    signature['positive_2023']=signature.mean_2023.gt(0)
    signature['positive_2024']=signature.mean_2024.gt(0)
    signature.to_csv(out/'product_first_positive_2022.csv',index=False)
    return a,s

def raster_audit(data_dir,out,eligible,*,raw_dir=None,geometry_path=None):
    import rasterio, geopandas as gpd, shapely
    from rasterio.windows import from_bounds,Window
    from pyproj import Transformer
    raw=Path(raw_dir) if raw_dir is not None else data_dir.parent/'raw/nightlights_zenodo_v0_4'
    geometry_path=Path(geometry_path) if geometry_path is not None else data_dir/'pa_geometries_v0_3_0.gpkg'
    g=gpd.read_file(geometry_path)
    g=g[g.pa_id.isin(eligible)].copy()
    assert g.crs.to_epsg()==3577
    bounds=g.to_crs(4326).total_bounds
    bounds=[bounds[0]-1,bounds[1]-1,bounds[2]+1,bounds[3]+1]
    files={y:next(raw.glob(f'*_{y}0101_*.tif')) for y in YEARS}
    metadata=[]; histrows=[]; positives=[]
    transform=Transformer.from_crs(4326,3577,always_xy=True)
    with rasterio.open(files[2013]) as ref:
        win=from_bounds(*bounds,ref.transform).round_offsets().round_lengths()
        expected=(ref.shape,ref.transform,ref.crs)
    # Complete fixed rectangular window includes surrounding non-reserve land;
    # annual hazard denominators come exclusively from accepted PA summaries.
    for year,path in files.items():
        with rasterio.open(path) as d:
            assert (d.shape,d.transform,d.crs)==expected
            meta=dict(year=year,file=path.name,bytes=path.stat().st_size,scale=d.scales[0],
              offset=d.offsets[0],nodata=d.nodata,dtype=d.dtypes[0],tags=d.tags(),
              bounds_requested=bounds,window=[win.col_off,win.row_off,win.width,win.height])
            # SHA256 all input rasters; streamed once, preserved exact identities.
            meta['sha256']=sha(path)
            if year not in [2013,2020,2021,2022,2023,2024]:
                metadata.append(meta);continue
            hist=np.zeros(65536,dtype=np.int64)
            for row in range(int(win.row_off),int(win.row_off+win.height),512):
                w=Window(win.col_off,row,win.width,min(512,win.row_off+win.height-row))
                arr=d.read(1,window=w)
                hist+=np.bincount(arr.ravel().astype(np.int32)+32768,minlength=65536)
                if year==2013:
                    rr,cc=np.where(arr>0)
                    xx=d.transform.c+(cc+win.col_off+.5)*d.transform.a
                    yy=d.transform.f+(rr+row+.5)*d.transform.e
                    x,y=transform.transform(xx,yy)
                    positives.append(np.column_stack([x,y]))
            vals=np.flatnonzero(hist)-32768
            meta['minimum_positive_stored']=int(vals[vals>0].min()) if (vals>0).any() else None
            meta['positive_pixels']=int(hist[32769:].sum())
            meta['zero_pixels']=int(hist[32768])
            meta['negative_pixels_including_nodata']=int(hist[:32768].sum())
            for v in vals:
                histrows.append(dict(year=year,stored_value=int(v),scaled_value=float(v*d.scales[0]+d.offsets[0]),
                      pixel_count=int(hist[v+32768]),valid=bool(v>=0 and v!=d.nodata)))
            metadata.append(meta)
            print('raster complete',year,meta['positive_pixels'],flush=True)
    pd.DataFrame(histrows).to_csv(out/'product_raster_histograms.csv',index=False)
    transitions=[]
    with ExitStack() as stack:
        ds={y:stack.enter_context(rasterio.open(files[y])) for y in [2020,2021,2022,2023,2024]}
        counts={y:np.zeros(4,dtype=np.int64) for y in [2021,2022,2023,2024]}
        for row in range(int(win.row_off),int(win.row_off+win.height),512):
            w=Window(win.col_off,row,win.width,min(512,win.row_off+win.height-row))
            arrays={y:d.read(1,window=w) for y,d in ds.items()}
            valid=np.logical_and.reduce([x>=0 for x in arrays.values()])
            for year,c in counts.items():
                codes=(arrays[year-1][valid]>0).astype(np.int8)*2+(arrays[year][valid]>0)
                c+=np.bincount(codes,minlength=4)
        for year,c in counts.items():
            transitions.append(dict(from_year=year-1,to_year=year,zero_zero=int(c[0]),
                zero_positive=int(c[1]),positive_zero=int(c[2]),positive_positive=int(c[3]),
                common_valid_pixels=int(c.sum())))
    pd.DataFrame(transitions).to_csv(out/'product_pixel_transitions.csv',index=False)
    (out/'product_raster_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    points=shapely.points(np.concatenate(positives));del positives
    print('baseline points',len(points),'query polygons',len(g),flush=True)
    tree=shapely.STRtree(points)
    # all_matches=False avoids enormous overlap ties for lit reserves.
    pairs,dist=tree.query_nearest(g.geometry.to_numpy(),return_distance=True,all_matches=False)
    dists=np.full(len(g),np.nan);dists[pairs[0]]=dist/1000
    result=pd.DataFrame({'pa_id':g.pa_id.to_numpy(),'distance_2013_lit_cell_km':dists})
    result['stratum']=pd.cut(result.distance_2013_lit_cell_km,[-np.inf,2,20,np.inf],
       labels=['near_<2km','middle_2_to_20km','far_>20km'],right=True).astype(str)
    result.loc[result.distance_2013_lit_cell_km.eq(2),'stratum']='middle_2_to_20km'
    result.to_csv(out/'product_baseline_distances.csv',index=False)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--data-dir',type=Path)
    p.add_argument('--output',type=Path)
    p.add_argument('--output-dir',type=Path)
    p.add_argument('--input-manifest',type=Path)
    p.add_argument('--raw-dir',type=Path)
    p.add_argument('--existing-product-audit',type=Path)
    p.add_argument('--skip-raster',action='store_true')
    args=p.parse_args()
    data=args.data_dir or (args.root/'data/processed' if args.root else None)
    out=args.output_dir or args.output
    if data is None or out is None:
        p.error('one of --data-dir/--root and one of --output-dir/--output are required')
    base_names=['pa_radiance_buffers_national_v0_3_0.csv','pa_trends_v0_3_0.csv','pa_geometries_v0_3_0.csv']
    raster_mode=args.raw_dir is not None
    required=base_names.copy()
    existing_source=None
    if args.existing_product_audit:
        existing_source=Path(args.existing_product_audit)
        existing_source=existing_source/'product_baseline_distances.csv' if existing_source.is_dir() else existing_source
        if not existing_source.is_file():
            raise FileNotFoundError(f'Existing product audit lacks product_baseline_distances.csv: {existing_source}')
    if args.input_manifest is None:
        # Preserve the legacy product audit's requirement to identify the
        # source geometry package even when raster diagnostics are skipped.
        required.append('pa_geometries_v0_3_0.gpkg')
    if raster_mode:
        required.append('pa_geometries_v0_3_0.gpkg')
        required.extend(sorted(path.name for path in args.raw_dir.glob('*.tif')))
        if len(required)==len(base_names)+1:
            raise FileNotFoundError(f'No raster inputs found in {args.raw_dir}')
    expected={'pa_radiance_buffers_national_v0_3_0.csv':'63e95fb30b0bdebc6c74d23f08666ab9cfe0ef408d27744f12fbb029a8b92ec1'}
    if args.input_manifest is not None and raster_mode:
        overrides={name: args.raw_dir/name for name in required if name.endswith('.tif')}
        contract=load_manifest(args.input_manifest,data,required,path_overrides=overrides)
    elif args.input_manifest is not None and existing_source is not None:
        required_with_audit=required+['product_baseline_distances.csv']
        contract=load_manifest(args.input_manifest,data,required_with_audit,path_overrides={'product_baseline_distances.csv': existing_source})
    elif raster_mode and args.input_manifest is None:
        legacy_paths={name: (args.raw_dir/name if name.endswith('.tif') else data/name) for name in required}
        contract=legacy_contract(legacy_paths,expected)
    else:
        contract=resolve_contract(data,required,args.input_manifest,expected)
    paths=contract.files
    out.mkdir(parents=True,exist_ok=True)
    a,s=annual_audit(data,out,paths)
    t=pd.read_csv(paths['pa_trends_v0_3_0.csv']);t=t[t.metric.eq('mean')&t.buffer_type.eq('land_unprotected')]
    if t.pa_id.duplicated().any() or not t.n_years_inside.ge(8).all():
        raise ValueError('Primary trend invariants failed')
    if contract.mode=='legacy':
        assert len(t)==4426
    if existing_source is not None:
        d=pd.read_csv(existing_source)
        if not {'pa_id','stratum'}.issubset(d.columns) or d.pa_id.duplicated().any():
            raise ValueError('Existing product audit baseline distances are invalid')
        if set(d.pa_id)!=set(t.pa_id):
            raise ValueError('Existing product audit cohort does not match current trends')
        destination=out/'product_baseline_distances.csv'
        if existing_source.resolve()!=destination.resolve():
            shutil.copy2(existing_source,destination)
    elif args.skip_raster:
        d=pd.read_csv(out/'product_baseline_distances.csv')
    elif raster_mode:
        d=raster_audit(data,out,t.pa_id,raw_dir=args.raw_dir,geometry_path=paths['pa_geometries_v0_3_0.gpkg'])
    else:
        raise ValueError('Provide --raw-dir or --existing-product-audit (or legacy --skip-raster)')
    w=a[a.zone.eq('inside')].pivot(index='pa_id',columns='year',values='mean').reindex(t.pa_id)
    h=hazards(w,d.set_index('pa_id').stratum);h.to_csv(out/'product_distance_hazards.csv',index=False)
    inside=s[s.zone.eq('inside')].merge(d,on='pa_id',validate='one_to_one')
    inside.to_csv(out/'product_inside_distance_series.csv',index=False)
    support=a[a.zone.eq('inside')].groupby('pa_id').valid_pixel_count.agg(['min','max'])
    support['stable_valid_pixel_count']=support['min'].eq(support['max'])
    support.to_csv(out/'product_inside_support.csv')
    # Count stability cannot prove identical valid-pixel identities.
    stable_ids=support.index[support.stable_valid_pixel_count]
    hs=hazards(w.loc[w.index.intersection(stable_ids)],d.set_index('pa_id').stratum)
    hs.to_csv(out/'product_distance_hazards_stable_count.csv',index=False)
    geom=pd.read_csv(paths['pa_geometries_v0_3_0.csv'])
    context=inside.merge(geom[['pa_id','STATE','area_km2']],on='pa_id',validate='one_to_one')
    context.groupby(['stratum','first_positive_year','STATE'],dropna=False).agg(
        n=('pa_id','size'),median_area_km2=('area_km2','median')).reset_index().to_csv(
        out/'product_distance_state_context.csv',index=False)
    manifest=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
       input_sha256={name:sha256(path) for name,path in paths.items()},input_contract=contract.identity(),script_sha256=sha256(Path(__file__)),protocol='product_audit_protocol.md',
       interpretation='Descriptive compatibility diagnostics; no causal attribution or null calibration.')
    (out/'product_audit_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(h.to_string(index=False),flush=True)

if __name__=='__main__':main()

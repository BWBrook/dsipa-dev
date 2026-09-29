#!/usr/bin/env python3
"""Compare actual raster selections at two declared geometry precisions."""
import argparse
import json
from pathlib import Path
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from rasterio.features import geometry_mask
from dsipa.trends import _theil_sen
from dsipa.layerA_national import build_buffers, build_rings, _stats_for_geom

IDS = ['WA_37883','NSW_N1108','WA_09868','WA_07537','CWTH_IPA50',
       'QLD_0239GRP001','WA_47880','WA_47881','WA_27575','WA_39584',
       'ACT_03','NSW_N1142','WA_05225','NSW_LHI']


def pixels(ds, geom):
    if geom.is_empty:
        return np.empty((0,2), dtype=np.int64)
    a, t = mask(ds, [geom], crop=True, filled=False)
    r,c = np.where(geometry_mask([geom], out_shape=a[0].shape, transform=t, invert=True, all_touched=False))
    x,y = rasterio.transform.xy(t, r,c)
    rr,cc = rasterio.transform.rowcol(ds.transform, x,y)
    return np.column_stack((rr,cc))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    g=gpd.read_file(a.baseline/'data/processed/pa_geometries_v0_3_0.gpkg')
    sample=g.sort_values('pa_id').sample(n=36,random_state=20260919)
    edge=pd.read_csv(a.baseline/'data/processed/pa_edge_profiles_national_v0_3_0.csv',
                     usecols=['pa_id','year','ring_index','valid_pixel_count'])
    threshold=edge[(edge.year==2024)&(edge.ring_index==1)&edge.valid_pixel_count.between(9,11)]
    threshold=threshold.sort_values('pa_id').sample(n=min(24,len(threshold)),random_state=20260919)
    g=g[g.pa_id.isin(set(sample.pa_id)|set(IDS)|set(threshold.pa_id))]
    grids={}
    for year in range(2013,2025):
        path=next((a.baseline/'data/raw/nightlights_zenodo_v0_4').glob(f'*_{year}0101_*.tif'))
        with rasterio.open(path) as ds:
            grids[str(year)]=dict(crs=str(ds.crs),transform=list(ds.transform),width=ds.width,height=ds.height)
    (a.out/'raster_grids.json').write_text(json.dumps(grids,indent=2)+'\n')
    if len({json.dumps(v,sort_keys=True) for v in grids.values()})!=1:
        raise ValueError('Multiple annual raster grids: precision must be checked for each grid')
    rows=[]; annual_checks=[]
    raster=next((a.baseline/'data/raw/nightlights_zenodo_v0_4').glob('*_20240101_*.tif'))
    with rasterio.open(raster) as ds:
        for _,r in g.iterrows():
            one=g[g.pa_id.eq(r.pa_id)]
            variants={}
            for q in (128,256):
                rings=build_rings(one,quad_segs=q)
                buffers,_=build_buffers(one,land_union=None,pa_union=None,quad_segs=q)
                geoms=list(rings.geometry)+list(buffers.geometry)
                variants[q]=gpd.GeoSeries(geoms,crs=g.crs).to_crs(ds.crs)
            for i,label in enumerate(['ring0','ring1','ring2','buffer1_raw','buffer5_raw']):
                lo,hi=variants[128].iloc[i],variants[256].iloc[i]
                lp,hp=pixels(ds,lo),pixels(ds,hi)
                ls,hs=set(map(tuple,lp)),set(map(tuple,hp))
                sl=_stats_for_geom(ds,lo,scale=ds.scales[0],offset=ds.offsets[0],min_valid_pixels=10)
                sh=_stats_for_geom(ds,hi,scale=ds.scales[0],offset=ds.offsets[0],min_valid_pixels=10)
                rows.append(dict(pa_id=r.pa_id,name=r.NAME,support=label,n128=len(lp),n256=len(hp),
                                 pixel_symmetric_difference=len(ls^hs),mean128=sl['mean'],mean256=sh['mean'],
                                 valid128=sl['valid_pixel_count'],valid256=sh['valid_pixel_count']))
                if ls != hs:
                    annual={128:[],256:[]}
                    for year in range(2013,2025):
                        path=next((a.baseline/'data/raw/nightlights_zenodo_v0_4').glob(f'*_{year}0101_*.tif'))
                        with rasterio.open(path) as yearly:
                            for q,geom in [(128,lo),(256,hi)]:
                                stat=_stats_for_geom(yearly,geom,scale=yearly.scales[0],offset=yearly.offsets[0],min_valid_pixels=10)
                                annual[q].append(stat['mean'])
                    slopes={}
                    for q,values in annual.items():
                        valid=np.isfinite(values)
                        slopes[q]=_theil_sen(np.arange(2013,2025)[valid],np.array(values)[valid])[0] if valid.sum()>=8 else None
                    annual_checks.append(dict(pa_id=r.pa_id,support=label,annual=annual,slopes=slopes,
                                               changed_pixels=[[int(r),int(c)] for r,c in sorted(ls^hs)]))
            print(r.pa_id,flush=True)
    d=pd.DataFrame(rows);d.to_csv(a.out/'precision_128_256.csv',index=False)
    result=dict(seed=20260919,reserves=len(g),supports=len(d),changed_supports=int(d.pixel_symmetric_difference.gt(0).sum()),
                changed_eligibility=int(((d.valid128>=10)!=(d.valid256>=10)).sum()),
                maximum_pixel_difference=int(d.pixel_symmetric_difference.max()))
    (a.out/'changed_support_annual.json').write_text(json.dumps(annual_checks,indent=2)+'\n')
    (a.out/'precision_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()

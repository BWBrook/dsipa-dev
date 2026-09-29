#!/usr/bin/env python3
"""Isolated, resumable national support correction; never writes to the baseline.

The unchanged schema is distinguished by analysis_id and a fail-closed run
contract. Raw/land/unprotected surrounding and all interior supports are
re-extracted; accepted whole-reserve annual rows are retained exactly.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
from pathlib import Path
import shutil
import time
import traceback

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import shapely
from shapely.geometry import box

from dsipa import layerA_national as engine
from dsipa.schema import SCHEMA_VERSION

ANALYSIS_ID = 'spatial-correction-20260919'
EXPECTED = {
 'pa_geometries_v0_3_0.gpkg':'da843f551bf1863dc5d1930ecb657491f73d69827b25007a0c55c9019721d0e6',
 'pa_radiance_buffers_national_v0_3_0.csv':'63e95fb30b0bdebc6c74d23f08666ab9cfe0ef408d27744f12fbb029a8b92ec1',
 'pa_edge_profiles_national_v0_3_0.csv':'ddb9c9f5678f9da10b70754d3c9319ea30bfe7203d3c80c8f8f298ed2cf5783b',
}
# Public baseline bytes were independently shown to contain identical keyed
# observations, attributes and geometries; only these explicit aliases pass.
PUBLIC_EQUIVALENTS = {
 'pa_geometries_v0_3_0.gpkg':'6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9',
 'pa_radiance_buffers_national_v0_3_0.csv':'6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61',
 'pa_edge_profiles_national_v0_3_0.csv':'baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812',
}
G_PA = G_LAND = G_OLDLAND = G_OUT = None
G_RASTERS = {}
G_PATHS = {}
G_COAST_GAPS = set()


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def atomic_csv(frame,path):
    temp=path.with_suffix('.tmp')
    frame.to_csv(temp,index=False)
    temp.replace(path)


def local_union(frame,extent):
    positions=frame.sindex.query(extent,predicate='intersects')
    if len(positions)==0:
        return shapely.GeometryCollection()
    clipped=frame.geometry.iloc[positions].intersection(extent)
    return engine._polygonal_geom(shapely.union_all(clipped.to_numpy()))


def initialise_worker():
    global G_RASTERS
    G_RASTERS={year:rasterio.open(path) for year,path in G_PATHS.items()}


def one_reserve(index):
    one=G_PA.iloc[[index]][['pa_id','geometry']]
    pa_id=one.pa_id.iloc[0]
    geom=one.geometry.iloc[0]
    xmin,ymin,xmax,ymax=geom.bounds
    extent=box(xmin-5100,ymin-5100,xmax+5100,ymax+5100)
    land=local_union(G_LAND,extent)
    estate=local_union(G_PA,extent)
    oldland=engine._safe_intersection(G_OLDLAND,extent)
    buffers,validity=engine.build_buffers(one,land_union=land,pa_union=estate)
    oldbuffers,oldvalidity=engine.build_buffers(one,land_union=oldland,pa_union=estate)
    if pa_id in G_COAST_GAPS:
        # The land source has no overlap with this PA. Do not infer observed
        # terrestrial absence or accept its land-based surrounding comparison.
        buffers=buffers[buffers.buffer_type.eq('raw')]
    # Raw buffers are identical and re-used in both variants after extraction.
    oldbuffers=oldbuffers[oldbuffers.buffer_type.ne('raw')]
    rings=engine.build_rings(one)
    buffer_rows=[];edge_rows=[]
    area_rows=[]
    for variant,supports in [('corrected',buffers),('geometry_only',oldbuffers),('rings',rings)]:
        crs=next(iter(G_RASTERS.values())).crs
        projected=supports.to_crs(crs)
        for (_,row),(_,native) in zip(projected.iterrows(),supports.iterrows()):
            geom4326=row.geometry
            if variant=='rings':
                key=dict(pa_id=pa_id,ring_index=int(row.ring_index),
                         ring_inner_km=float(row.ring_inner_km),ring_outer_km=float(row.ring_outer_km))
            else:
                key=dict(pa_id=pa_id,zone='buffer',buffer_km=float(row.buffer_km),buffer_type=row.buffer_type,
                         variant=variant)
            area_rows.append(dict(**key,area_km2=native.geometry.area/1e6))
            for year,ds in G_RASTERS.items():
                try:
                    stats=engine._stats_for_geom(ds,geom4326,scale=ds.scales[0],offset=ds.offsets[0],min_valid_pixels=10)
                except Exception as error:
                    raise RuntimeError(f'Extraction failed: {key}, year={year}') from error
                result=dict(**key,year=year,schema_version=SCHEMA_VERSION,
                            scale_metadata=ds.scales[0],offset_metadata=ds.offsets[0],**stats)
                (edge_rows if variant=='rings' else buffer_rows).append(result)
    validity['variant']='corrected';oldvalidity['variant']='geometry_only'
    ds=next(iter(G_RASTERS.values()))
    inside_raster=one.to_crs(ds.crs).geometry.iloc[0].intersects(box(*ds.bounds))
    coverage=dict(pa_id=pa_id,coastline_support_excluded=pa_id in G_COAST_GAPS,inside_raster_footprint=inside_raster,coastline_inside_fraction=engine._safe_intersection(geom,land).area/geom.area,
                  geometry_area_km2=geom.area/1e6)
    return buffer_rows,edge_rows,pd.concat([validity,oldvalidity]).to_dict('records'),area_rows,[coverage]


def chunk(indices):
    number=indices[0]
    stem=G_OUT/'parts'/f'{number:06d}'
    done=stem.with_suffix('.done.json')
    suffixes=['buffers','rings','validity','areas','coverage']
    if done.exists():
        manifest=json.loads(done.read_text())
        if all(sha(G_OUT/'parts'/name)==digest for name,digest in manifest['sha256'].items()):
            return dict(chunk=number,reserves=len(indices),resumed=True)
        raise ValueError(f'Completed chunk changed: {number}')
    outputs=[[] for _ in suffixes]
    for index in indices:
        for target,rows in zip(outputs,one_reserve(index)):
            target.extend(rows)
    hashes={}
    for suffix,rows in zip(suffixes,outputs):
        path=stem.with_suffix('.'+suffix+'.csv')
        atomic_csv(pd.DataFrame(rows),path);hashes[path.name]=sha(path)
    done.write_text(json.dumps(dict(sha256=hashes,pa_ids=G_PA.iloc[indices].pa_id.tolist()),indent=2)+'\n')
    return dict(chunk=number,reserves=len(indices),resumed=False)


def assemble(baseline,out):
    destination=out/'data/processed';destination.mkdir(parents=True,exist_ok=True)
    def read_parts(suffix):
        return pd.concat([pd.read_csv(p,float_precision='round_trip') for p in sorted((out/'parts').glob(f'*.{suffix}.csv'))],ignore_index=True)
    original=pd.read_csv(baseline/'data/processed/pa_radiance_buffers_national_v0_3_0.csv',float_precision='round_trip')
    inside=original[original.zone.eq('inside')].copy()
    buffers=read_parts('buffers')
    new=buffers[buffers.variant.eq('corrected')].drop(columns='variant')
    old=buffers[buffers.variant.eq('geometry_only')].drop(columns='variant')
    old=pd.concat([old,new[new.buffer_type.eq('raw')]],ignore_index=True)
    for variant,frame in [('corrected',new),('geometry_only',old)]:
        folder=destination if variant=='corrected' else out/'geometry_only/data/processed'
        folder.mkdir(parents=True,exist_ok=True)
        frame=pd.concat([inside,frame],ignore_index=True).reindex(columns=original.columns)
        frame=frame.sort_values(['pa_id','zone','buffer_km','buffer_type','year'],na_position='first')
        path=folder/'pa_radiance_buffers_national_v0_3_0.csv';atomic_csv(frame,path)
        restored=pd.read_csv(path,float_precision='round_trip').loc[lambda d:d.zone.eq('inside')]
        pd.testing.assert_frame_equal(inside.sort_values(['pa_id','year']).reset_index(drop=True),
                                      restored.sort_values(['pa_id','year']).reset_index(drop=True))
    rings=read_parts('rings').sort_values(['pa_id','ring_index','year'])
    atomic_csv(rings,destination/'pa_edge_profiles_national_v0_3_0.csv')
    validity=read_parts('validity')
    validity['schema_version']=SCHEMA_VERSION
    for variant in ['corrected','geometry_only']:
        folder=destination if variant=='corrected' else out/'geometry_only/data/processed'
        atomic_csv(validity[validity.variant.eq(variant)].drop(columns='variant').sort_values(['pa_id','buffer_km']),
                   folder/'pa_buffer_validity_v0_3_0.csv')
    for suffix in ['areas','coverage']:
        atomic_csv(read_parts(suffix),out/f'support_{suffix}.csv')
    for name in ['pa_geometries_v0_3_0.csv','pa_ibra_assignment_v0_3_0.csv','pa_trend_bootstrap_summary_v0_3_0.csv']:
        for folder in [destination,out/'geometry_only/data/processed']:
            shutil.copy2(baseline/'data/processed'/name,folder/name)
    outputs={str(p.relative_to(out)):dict(sha256=sha(p),bytes=p.stat().st_size)
             for folder in [destination,out/'geometry_only/data/processed'] for p in sorted(folder.glob('*.csv'))}
    (out/'extraction_manifest.json').write_text(json.dumps(dict(analysis_id=ANALYSIS_ID,whole_reserve_rows_unchanged=True,
        whole_reserve_rows=len(inside),output_files=outputs),indent=2)+'\n')


def main():
    global G_PA,G_LAND,G_OLDLAND,G_OUT,G_PATHS,G_COAST_GAPS
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--coastline',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--coverage-screen',type=Path,required=True)
    p.add_argument('--workers',type=int,default=12)
    p.add_argument('--chunk-size',type=int,default=12)
    p.add_argument('--limit',type=int)
    p.add_argument('--pa-ids',help='Comma-separated pilot IDs; full estate is still excluded')
    a=p.parse_args();start=time.time()
    if a.out.resolve()==a.baseline.resolve() or a.baseline.resolve() in a.out.resolve().parents:
        raise ValueError('Correction output must be outside the accepted baseline')
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'parts').mkdir(exist_ok=True)
    inputs={}
    for name,expected in EXPECTED.items():
        path=a.baseline/'data/processed'/name;inputs[name]=sha(path)
        if inputs[name] not in {expected,PUBLIC_EQUIVALENTS[name]}:raise ValueError(f'Baseline identity mismatch: {name}')
    coast_files=sorted(a.coastline.parent.glob(a.coastline.stem+'.*'))
    contract=dict(analysis_id=ANALYSIS_ID,baseline_sha256=inputs,
                  coastline_sha256={p.name:sha(p) for p in coast_files},
                  engine_sha256=sha(engine.__file__),runner_sha256=sha(__file__),
                  coverage_screen_sha256=sha(a.coverage_screen),quad_segs=engine.BUFFER_QUAD_SEGS,limit=a.limit,pa_ids=a.pa_ids,chunk_size=a.chunk_size)
    cp=a.out/'run_contract.json'
    if cp.exists() and json.loads(cp.read_text())!=contract:
        raise ValueError('Run contract differs; use a new output directory')
    cp.write_text(json.dumps(contract,indent=2)+'\n')
    G_PA=gpd.read_file(a.baseline/'data/processed/pa_geometries_v0_3_0.gpkg').sort_values('pa_id').reset_index(drop=True)
    if G_PA.crs.to_epsg()!=3577:raise ValueError('CAPAD is not EPSG:3577')
    invalid_source=G_PA.loc[~G_PA.geometry.is_valid,['pa_id','geometry']]
    invalid_records=[dict(pa_id=row.pa_id,reason=shapely.is_valid_reason(row.geometry)) for row in invalid_source.itertuples()]
    G_PA['geometry']=G_PA.geometry.apply(engine._polygonal_geom)
    coverage=pd.read_csv(a.coverage_screen)
    if coverage.intersects_source_land.dtype!=bool:
        raise ValueError('Coverage flags must be boolean')
    G_COAST_GAPS=set(coverage.loc[~coverage.intersects_source_land,'pa_id'])
    if not G_COAST_GAPS.issubset(set(G_PA.pa_id)):
        raise ValueError('Coverage IDs missing from estate')
    shutil.copy2(a.coverage_screen,a.out/'coastline_coverage_screen.csv')
    G_LAND=gpd.read_file(a.coastline).to_crs(G_PA.crs)
    geometry_diagnostics=dict(pa_invalid_before_repair=invalid_records,pa_invalid=int((~G_PA.geometry.is_valid).sum()),
        coastline_invalid_before_repair=int((~G_LAND.geometry.is_valid).sum()),
        coastline_features=len(G_LAND),excluded_land_support_ids=sorted(G_COAST_GAPS))
    G_LAND['geometry']=G_LAND.geometry.apply(engine._polygonal_geom)
    (a.out/'geometry_diagnostics.json').write_text(json.dumps(geometry_diagnostics,indent=2)+'\n')
    # Build indices in the parent before Linux fork; workers share immutable geometry.
    G_PA.sindex;G_LAND.sindex
    cache=a.baseline/'data/processed/cache/land_union_ne_110m.wkb'
    if sha(cache)!='2eb7cea010a462e4d830ce779567d0d626b2355e4f444259616eae765be93b77':
        raise ValueError('Historical landmask cache identity mismatch')
    G_OLDLAND=shapely.from_wkb(cache.read_bytes());G_OUT=a.out
    G_PATHS={year:next((a.baseline/'data/raw/nightlights_zenodo_v0_4').glob(f'*_{year}0101_*.tif')) for year in range(2013,2025)}
    rasters={}
    for year,path in G_PATHS.items():
        with rasterio.open(path) as ds:
            rasters[str(year)]=dict(path=str(path),sha256=sha(path),crs=str(ds.crs),transform=list(ds.transform),
                                    width=ds.width,height=ds.height,scale=ds.scales[0],offset=ds.offsets[0],nodata=ds.nodata)
    (a.out/'raster_manifest.json').write_text(json.dumps(rasters,indent=2)+'\n')
    count=len(G_PA) if a.limit is None else min(a.limit,len(G_PA))
    indices=list(range(count))
    if a.pa_ids:
        requested=set(a.pa_ids.split(','))
        if not requested.issubset(set(G_PA.pa_id)):raise ValueError('Unknown pilot PA ID')
        indices=G_PA.index[G_PA.pa_id.isin(requested)].tolist();count=len(indices)
    chunks=[indices[i:i+a.chunk_size] for i in range(0,count,a.chunk_size)]
    print(json.dumps(dict(stage='extraction',reserves=count,workers=a.workers,elapsed=time.time()-start)),flush=True)
    with ProcessPoolExecutor(max_workers=a.workers,mp_context=multiprocessing.get_context('fork'),initializer=initialise_worker) as ex:
        jobs=[ex.submit(chunk,indices) for indices in chunks]
        try:
            for job in as_completed(jobs):
                print(json.dumps(dict(**job.result(),elapsed=time.time()-start)),flush=True)
        except BaseException:
            traceback.print_exc()
            for pending in jobs:
                pending.cancel()
            # This process owns only these extraction workers. Do not let a
            # failed support hide behind the executor's remaining work queue.
            for child in multiprocessing.active_children():
                child.terminate()
            raise
    if a.limit is None and not a.pa_ids:
        assemble(a.baseline,a.out)
    print(json.dumps(dict(stage='complete',elapsed=time.time()-start)),flush=True)

if __name__=='__main__':main()

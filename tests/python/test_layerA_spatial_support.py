"""Geometry regressions for the independently identified support errors."""
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon, box
from dsipa.layerA_national import BUFFER_QUAD_SEGS, build_buffers, build_rings


def frame(geom):
    return gpd.GeoDataFrame({'pa_id': ['test'], 'geometry': [geom]}, crs=3577)


def test_concave_inner_band_respects_distance():
    polygon = Polygon([(0,0),(10000,0),(10000,4000),(4000,4000),(4000,10000),(0,10000)])
    near = Point(3350,3350)
    far = Point(3200,3200)
    rings = build_rings(frame(polygon)).set_index('ring_index')
    assert near.distance(polygon.boundary) < 1000
    assert not rings.loc[1].geometry.covers(near)
    assert rings.loc[0].geometry.covers(near)
    assert far.distance(polygon.boundary) > 1000
    assert rings.loc[1].geometry.covers(far)
    assert rings.loc[0].geometry.intersection(rings.loc[1].geometry).area < 1e-6


def test_outside_buffer_keeps_narrow_boundary_features_and_excludes_estate():
    polygon = box(0,0,5000,5000).union(box(5000,2400,6000,2600))
    neighbour = box(5500,3000,6500,4000)
    buffers, validity = build_buffers(frame(polygon), land_union=box(-20000,-20000,20000,20000),
                                      pa_union=polygon.union(neighbour))
    row = buffers[(buffers.buffer_km == 1) & (buffers.buffer_type == 'land_unprotected')].iloc[0]
    assert row.geometry.intersection(polygon).area < 1e-6
    assert row.geometry.intersection(neighbour).area < 1e-6
    assert row.geometry.covers(Point(6950,2500))
    assert not row.geometry.covers(Point(5900,2500))
    assert (validity.effective_land_area_km2 <= validity.land_area_km2).all()


def test_arc_error_and_circle_area_converge():
    assert 10000 * (1 - np.cos(np.pi / (4 * BUFFER_QUAD_SEGS))) < .19
    polygon = box(0,0,10000,10000)
    buffers, _ = build_buffers(frame(polygon), land_union=None, pa_union=None)
    area = buffers.loc[buffers.buffer_km == 1].geometry.iloc[0].area
    expected = polygon.length * 1000 + np.pi * 1000**2
    assert abs(area / expected - 1) < 1e-5


def test_extraction_error_cannot_masquerade_as_ineligible(monkeypatch):
    import pytest
    from types import SimpleNamespace
    from dsipa import layerA_national as engine
    ds=SimpleNamespace(nodata=-999, bounds=(-2,-2,2,2))
    def fail(*args,**kwargs):
        raise OSError('unreadable raster block')
    monkeypatch.setattr(engine,'mask',fail)
    with pytest.raises(OSError,match='unreadable raster'):
        engine._stats_for_geom(ds,box(-1,-1,1,1),scale=1,offset=0,min_valid_pixels=10)
    result=engine._stats_for_geom(ds,box(10,10,20,20),scale=1,offset=0,min_valid_pixels=10)
    assert result['valid_pixel_count']==0
    assert np.isnan(result['mean'])


def test_mixed_overlay_collection_samples_only_polygon_support():
    import rasterio
    from rasterio.io import MemoryFile
    from rasterio.transform import from_origin
    from shapely.geometry import GeometryCollection, LineString
    from dsipa.layerA_national import _stats_for_geom, _polygonal_geom
    polygon=box(120.1,-10.4,120.4,-10.1)
    mixed=GeometryCollection([polygon,GeometryCollection([
        LineString([(120,-10.5),(120.5,-10.5)]),Point(120,-10)])])
    normalised=_polygonal_geom(mixed)
    assert normalised.equals(polygon)
    assert normalised.area==mixed.area
    with MemoryFile() as mem:
        with mem.open(driver='GTiff',height=5,width=5,count=1,dtype='int16',
                      crs='EPSG:4326',transform=from_origin(120,-10,.1,.1),nodata=-999) as ds:
            ds.write(np.full((1,5,5),10,dtype='int16'))
            expected=_stats_for_geom(ds,polygon,scale=10,offset=0,min_valid_pixels=1)
            actual=_stats_for_geom(ds,mixed,scale=10,offset=0,min_valid_pixels=1)
    assert actual==expected
    assert actual['valid_pixel_count']==9 and actual['mean']==100
    assert _polygonal_geom(LineString([(0,0),(1,1)])).is_empty


def test_nested_polygon_collection_preserves_disjoint_components():
    from shapely.geometry import GeometryCollection, LineString
    from dsipa.layerA_national import _polygonal_geom
    first=box(0,0,10,10);second=box(20,0,30,10)
    source=GeometryCollection([first,GeometryCollection([second])])
    result=_polygonal_geom(source)
    assert result.geom_type=='MultiPolygon' and result.is_valid
    assert result.area==source.area and result.bounds==source.bounds
    assert result.equals(first.union(second))
    assert _polygonal_geom(GeometryCollection([Point(0,0),LineString([(0,0),(1,1)])])).is_empty
    rings=build_rings(frame(first.union(second)))
    assert all(g.is_empty or (g.is_valid and g.geom_type in {'Polygon','MultiPolygon'}) for g in rings.geometry)


def test_legacy_entrypoint_cannot_silently_generate_current_results():
    from dsipa.layerA_national import main
    import pytest
    with pytest.raises(SystemExit, match="run_spatial_correction.py"):
        main([])


def test_nonareal_repair_remnants_cannot_gain_buffer_area():
    import geopandas as gpd
    from shapely.geometry import GeometryCollection, LineString, box
    from dsipa.layerA_national import build_buffers, build_rings
    polygon=box(0,0,5000,5000)
    mixed=GeometryCollection([polygon,LineString([(8000,0),(9000,0)])])
    a=gpd.GeoDataFrame({'pa_id':['test']},geometry=[polygon],crs=3577)
    b=gpd.GeoDataFrame({'pa_id':['test']},geometry=[mixed],crs=3577)
    land=box(-20000,-20000,30000,30000)
    for f in [a,b]:
        buffers,_=build_buffers(f,land_union=land,pa_union=f.geometry.iloc[0])
        if f is a:expected=buffers
        else:assert all(x.equals(y) for x,y in zip(expected.geometry,buffers.geometry))
    assert all(x.equals(y) for x,y in zip(build_rings(a).geometry,build_rings(b).geometry))

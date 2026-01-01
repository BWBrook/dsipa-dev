# Data inventory

Record every dataset placed under `data/raw/` and the derived products under `data/processed/`.

| Name | Source URL / DOI | Version / date fetched | License | Checksum (e.g., sha256) | Notes |
| --- | --- | --- | --- | --- | --- |
| CAPAD 2024 technical specifications (PDF) | https://www.dcceew.gov.au/sites/default/files/documents/capad-2024-tech-spec.pdf | CAPAD 2024; fetched 2026-01-01 | CC BY 4.0 | bdf7c15be087793dcfa27af38eb5dd56a66672ba3d8d88ba3ac2313456a51947 | Metadata file; spatial data accessed via DCCEEW CAPAD MapServer/FeatureServer. |
| CAPAD 2024 spatial data (ArcGIS REST service) | https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer | CAPAD 2024 (snapshot 2024-06-30) | CC BY 4.0 | N/A (service) | Primary protected-area geometry source; to be downloaded via REST in WP0.4+. |
| VIIRS DNB annual VNL v2.2 readme (PPTX) | https://eogdata.mines.edu/products/vnl/VNL_v22_readme_20230707.pptx | VNL v2.2 readme; fetched 2026-01-01 | Public domain (NOAA/EOG) | 40855418eba6d7543ecd4c8cc3d373e18c9cc6af6224a9e34f9047aef13763b1 | Metadata file describing VNL v2.2 products (superseded by Zenodo v0.4 source for this project). |
| VIIRS DNB annual VNL v2.2 GeoTIFFs | https://eogdata.mines.edu/products/vnl/ | VNL v2.2 annual series (2012–2024) | Public domain (NOAA/EOG) | N/A (not downloaded) | Superseded by Zenodo v0.4 (OpenGeoHub) due to auth gate. |
| Zenodo nightlights v0.4 record | https://doi.org/10.5281/zenodo.17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | N/A (record) | Annual VIIRS-based night-lights COGs; core years 2013–2024. |
| nightlights.average_viirs.v21_m_500m_s_20130101_20131231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | b60fb30a5039aff28e943179ec797f3f | Smoke-test year 2013. |
| nightlights.average_viirs.v21_m_500m_s_20180101_20181231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | b1818a74dd2bc41e7253a5df76533a9c | Smoke-test year 2018. |
| nightlights.average_viirs.v21_m_500m_s_20240101_20241231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 0b976892d40c2d0d99177c727289eaf2 | Smoke-test year 2024. |
| smoke_test_triad_index_v0_1_0.csv | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | b1c01a663ac194f228283017dbf297b8c07bb9d2cd2f4da4a921c0ede59bebd8 | Triad IDs + metadata for smoke-test slice. |
| smoke_test_triad_geoms_v0_1_0.gpkg | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | cd45da85947718eb6906279b9d930a120f32c67c03b19533ef4cc98df3430b44 | Triad geometries (EPSG:3577). |
| smoke_test_triad_buffers_v0_1_0.gpkg | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | 5bc567e130088e4c309dc028eaf03dd166bbbe7ea5f1377f281b243881e70967 | Outside buffers (1 km, 5 km). |
| smoke_test_triad_rings_v0_1_0.csv | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | fd4fd7c224f88781ed5bbb332e0a76c54a5d6217a4df7fec338b777815934b05 | Inside ring summary (0–1, 1–5, 5–10 km). |
| pa_geometries_v0_1_0.gpkg | src/python/dsipa/pa_geometry.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | 0a12f66fd59e0c3b7cb7d9f04c0eaa11557e21a8a2b66b82bb9367c29aec4c1f | Processed PA geometries (EPSG:3577) with validity + descriptors. |
| pa_geometries_v0_1_0.csv | src/python/dsipa/pa_geometry.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | e2e277e799b7a789094685731e1dbe3a70c1998b2f3a81661e87299091967676 | Tabular descriptors for processed PA geometries. |
| pa_radiance_buffers_smoketest_v0_1_0.csv | src/python/dsipa/radiance_smoketest.py | Generated 2026-01-01; schema v0.1.0 | Derived (Zenodo nightlights CC BY 4.0) | 99279752fd880a5493f46b189361605c7f24cfe09bc2766102f12c242b03c059 | Smoke-test radiance summaries (inside + buffers) for triad years. |
| pa_edge_profiles_smoketest_v0_1_0.csv | src/python/dsipa/ring_profiles_smoketest.py | Generated 2026-01-01; schema v0.1.0 | Derived (Zenodo nightlights CC BY 4.0) | efa04231e2912e13ad9d61805088a07baeb2f6b8c4e2124aa3cf3ea90d85bf47 | Smoke-test edge profile summaries (inside rings). |

Rules:
- Do not hand-edit files in `data/raw/`; recreate via scripts.
- Store scripts used for downloads/processing in `src/` or `analysis/` and reference them here.
- If data cannot be redistributed, keep it out of git and document the retrieval steps instead.

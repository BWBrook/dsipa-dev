# Data inventory

Record every dataset placed under `data/raw/` and the derived products under `data/processed/`.

| Name | Source URL / DOI | Version / date fetched | License | Checksum (algorithm noted) | Notes |
| --- | --- | --- | --- | --- | --- |
| CAPAD 2024 technical specifications (PDF) | https://www.dcceew.gov.au/sites/default/files/documents/capad-2024-tech-spec.pdf | CAPAD 2024; fetched 2026-01-01 | CC BY 4.0 | bdf7c15be087793dcfa27af38eb5dd56a66672ba3d8d88ba3ac2313456a51947 | Metadata file; spatial data accessed via DCCEEW CAPAD MapServer/FeatureServer. |
| CAPAD 2024 spatial data (ArcGIS REST service) | https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer | CAPAD 2024 (snapshot 2024-06-30) | CC BY 4.0 | N/A (service) | Primary protected-area geometry source; to be downloaded via REST in WP0.4+. |
| VIIRS DNB annual VNL v2.2 readme (PPTX) | https://eogdata.mines.edu/products/vnl/VNL_v22_readme_20230707.pptx | VNL v2.2 readme; fetched 2026-01-01 | Public domain (NOAA/EOG) | 40855418eba6d7543ecd4c8cc3d373e18c9cc6af6224a9e34f9047aef13763b1 | Metadata file describing VNL v2.2 products (superseded by Zenodo v0.4 source for this project). |
| VIIRS DNB annual VNL v2.2 GeoTIFFs | https://eogdata.mines.edu/products/vnl/ | VNL v2.2 annual series (2012–2024) | Public domain (NOAA/EOG) | N/A (not downloaded) | Superseded by Zenodo v0.4 (OpenGeoHub) due to auth gate. |
| Zenodo nightlights v0.4 record | https://doi.org/10.5281/zenodo.17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | N/A (record) | Annual VIIRS-based night-lights COGs; core years 2013–2024. |
| nightlights.average_viirs.v21_m_500m_s_20130101_20131231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | b60fb30a5039aff28e943179ec797f3f | Core year 2013 (smoke-test year). |
| nightlights.average_viirs.v21_m_500m_s_20140101_20141231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | c9505d985dbfef015e4f23f3d0172f32 | Core year 2014. |
| nightlights.average_viirs.v21_m_500m_s_20150101_20151231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 2dbb7b5930a218778636bea0eeb9afb1 | Core year 2015. |
| nightlights.average_viirs.v21_m_500m_s_20160101_20161231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | a75f58ecdffb7c62e6af2a0464139551 | Core year 2016. |
| nightlights.average_viirs.v21_m_500m_s_20170101_20171231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 380fcdc877f0213f023ee41372ff7894 | Core year 2017. |
| nightlights.average_viirs.v21_m_500m_s_20180101_20181231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | b1818a74dd2bc41e7253a5df76533a9c | Core year 2018 (smoke-test year). |
| nightlights.average_viirs.v21_m_500m_s_20190101_20191231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 88933a6aa669fa863a998b92f9d25c92 | Core year 2019. |
| nightlights.average_viirs.v21_m_500m_s_20200101_20201231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 2e2756b276a293dc4c2932c9ccb1f7e4 | Core year 2020. |
| nightlights.average_viirs.v21_m_500m_s_20210101_20211231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | f200a2292de85badfbadb557621cdd6b | Core year 2021. |
| nightlights.average_viirs.v21_m_500m_s_20220101_20221231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | d0952d107adfd943478f1635a2eb987e | Core year 2022 (GeoTIFF scale=10). |
| nightlights.average_viirs.v21_m_500m_s_20230101_20231231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 7108c72e049e2e718213816e3dad3ed2 | Core year 2023 (GeoTIFF scale=10). |
| nightlights.average_viirs.v21_m_500m_s_20240101_20241231_go_epsg4326_v20250904.tif | https://zenodo.org/records/17294744 | v0.4; accessed 2026-01-01 | CC BY 4.0 | 0b976892d40c2d0d99177c727289eaf2 | Core year 2024 (smoke-test year; GeoTIFF scale=10). |
| smoke_test_triad_index_v0_2_0.csv | src/python/dsipa/triad.py | Generated 2026-01-02; schema v0.2.0 | Derived (CAPAD CC BY 4.0) | 948ecdf4aadb73980071335134d80381ff47e8897095c6a9cfd687635b28f16f | Triad IDs + metadata for smoke-test slice. |
| smoke_test_triad_geoms_v0_2_0.gpkg | src/python/dsipa/triad.py | Generated 2026-01-02; schema v0.2.0 | Derived (CAPAD CC BY 4.0) | e54ed6adb9de333d1813af439172ea21060582491dcb02e410f0d9dff6559943 | Triad geometries (EPSG:3577). |
| smoke_test_triad_buffers_v0_2_0.gpkg | src/python/dsipa/triad.py | Generated 2026-01-02; schema v0.2.0 | Derived (CAPAD CC BY 4.0) | 3d096092e8137ffc1beed24afe332533d819fd537cf3e5389e94f9a014732e95 | Outside buffers (1 km, 5 km). |
| smoke_test_triad_rings_v0_2_0.csv | src/python/dsipa/triad.py | Generated 2026-01-02; schema v0.2.0 | Derived (CAPAD CC BY 4.0) | 15a0c5a4ca40f7ce8e1028a66b80edb4bca309747180804ed0c06cea1d814347 | Inside ring summary (0–1, 1–5, 5–10 km). |
| pa_geometries_v0_2_0.gpkg | src/python/dsipa/pa_geometry.py | Generated 2026-01-02; schema v0.2.0 | Derived (CAPAD CC BY 4.0) | 154571739d3215045ed6ed4d394381669dd40521f923de06993576a3178547f4 | Processed PA geometries (EPSG:3577) with validity + descriptors. |
| pa_geometries_v0_2_0.csv | src/python/dsipa/pa_geometry.py | Generated 2026-01-02; schema v0.2.0 | Derived (CAPAD CC BY 4.0) | 0883a0c0009d079fbe90b4d61f21919f11dd69023bc35a910169a85b569e82ce | Tabular descriptors for processed PA geometries. |
| pa_radiance_buffers_smoketest_v0_2_0.csv | src/python/dsipa/radiance_smoketest.py | Generated 2026-01-02; schema v0.2.0 | Derived (Zenodo nightlights CC BY 4.0) | a0e92162d5457b05974f22c09ba8c99718970d0ec57f12a85252947dc3c37897 | Smoke-test radiance summaries (inside + buffers) for triad years. |
| pa_edge_profiles_smoketest_v0_2_0.csv | src/python/dsipa/ring_profiles_smoketest.py | Generated 2026-01-02; schema v0.2.0 | Derived (Zenodo nightlights CC BY 4.0) | f4f2b9e05879e404d60b6bd9fd2c814e1e95cebc9ba65fcc7b482e57fcf80e0e | Smoke-test edge profile summaries (inside rings). |
| pa_radiance_buffers_national_v0_2_0.csv | src/python/dsipa/layerA_national.py | Generated 2026-01-02; schema v0.2.0 | Derived (Zenodo nightlights CC BY 4.0) | fee3c7d4f75539b6bac51cbf8742824eaf4f4368d756a9f750e92171d49baf01 | National radiance summaries (inside + buffers) for 2013–2024. |
| pa_edge_profiles_national_v0_2_0.csv | src/python/dsipa/layerA_national.py | Generated 2026-01-02; schema v0.2.0 | Derived (Zenodo nightlights CC BY 4.0) | 21bf4ec78005365fdd9a8dacf29543b8e83424ed9002f5d0b2cf848c925b7f60 | National edge profile summaries (inside rings) for 2013–2024. |
| pa_trends_v0_2_0.csv | src/python/dsipa/trends.py | Generated 2026-01-02; schema v0.2.0 | Derived (Zenodo nightlights CC BY 4.0) | 45b6592547111abecfa1340c5117a9abce09bfe1360b02fdb026e7878949cb29 | Trend estimates and retention indices (mean primary; median retained). |
| pa_risk_rankings_v0_2_0.csv | src/python/dsipa/vulnerability_model.py | Generated 2026-01-02; schema v0.2.0 | Derived (Zenodo nightlights CC BY 4.0) | c288682fbbcae9c91b3439091e52e41ee04e71d45ba634c6e6d057987fde74fb | Ranked PAs by brightening, retention, and combined risk score. |

Notes:
- Checksums default to sha256 unless otherwise stated. Nightlights GeoTIFF checksums are MD5 (32 hex characters), matching `src/python/dsipa/nightlights.py`.

Rules:
- Do not hand-edit files in `data/raw/`; recreate via scripts.
- Store scripts used for downloads/processing in `src/` or `analysis/` and reference them here.
- If data cannot be redistributed, keep it out of git and document the retrieval steps instead.

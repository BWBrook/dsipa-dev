# Data inventory

Record every dataset placed under `data/raw/` and the derived products under `data/processed/`.

| Name | Source URL / DOI | Version / date fetched | License | Checksum (e.g., sha256) | Notes |
| --- | --- | --- | --- | --- | --- |
| CAPAD 2024 technical specifications (PDF) | https://www.dcceew.gov.au/sites/default/files/documents/capad-2024-tech-spec.pdf | CAPAD 2024; fetched 2026-01-01 | CC BY 4.0 | bdf7c15be087793dcfa27af38eb5dd56a66672ba3d8d88ba3ac2313456a51947 | Metadata file; spatial data accessed via DCCEEW CAPAD MapServer/FeatureServer. |
| CAPAD 2024 spatial data (ArcGIS REST service) | https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer | CAPAD 2024 (snapshot 2024-06-30) | CC BY 4.0 | N/A (service) | Primary protected-area geometry source; to be downloaded via REST in WP0.4+. |
| VIIRS DNB annual VNL v2.2 readme (PPTX) | https://eogdata.mines.edu/products/vnl/VNL_v22_readme_20230707.pptx | VNL v2.2 readme; fetched 2026-01-01 | Public domain (NOAA/EOG) | 40855418eba6d7543ecd4c8cc3d373e18c9cc6af6224a9e34f9047aef13763b1 | Metadata file describing VNL v2.2 products. |
| VIIRS DNB annual VNL v2.2 GeoTIFFs | https://eogdata.mines.edu/products/vnl/ | VNL v2.2 annual series (2012–2024) | Public domain (NOAA/EOG) | N/A (not downloaded yet) | Planned night-lights source; annual global composites. |
| smoke_test_triad_index_v0_1_0.csv | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | b1c01a663ac194f228283017dbf297b8c07bb9d2cd2f4da4a921c0ede59bebd8 | Triad IDs + metadata for smoke-test slice. |
| smoke_test_triad_geoms_v0_1_0.gpkg | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | cd45da85947718eb6906279b9d930a120f32c67c03b19533ef4cc98df3430b44 | Triad geometries (EPSG:3577). |
| smoke_test_triad_buffers_v0_1_0.gpkg | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | 5bc567e130088e4c309dc028eaf03dd166bbbe7ea5f1377f281b243881e70967 | Outside buffers (1 km, 5 km). |
| smoke_test_triad_rings_v0_1_0.csv | src/python/dsipa/triad.py | Generated 2026-01-01; schema v0.1.0 | Derived (CAPAD CC BY 4.0) | fd4fd7c224f88781ed5bbb332e0a76c54a5d6217a4df7fec338b777815934b05 | Inside ring summary (0–1, 1–5, 5–10 km). |

Rules:
- Do not hand-edit files in `data/raw/`; recreate via scripts.
- Store scripts used for downloads/processing in `src/` or `analysis/` and reference them here.
- If data cannot be redistributed, keep it out of git and document the retrieval steps instead.

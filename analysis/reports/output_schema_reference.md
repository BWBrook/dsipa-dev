# Output schema reference

Generated: 2026-01-01 07:59 UTC

Schema version: 0.1.0

Migration policy: Any change to required columns or their meaning requires a schema_version bump and a full rerun. No automatic migration is provided.

## smoke_test_triad_index

File: `data/processed/smoke_test_triad_index_v0_1_0.csv`
Format: csv

Triad selection table (three protected areas).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for triad outputs. |
| triad_role | string | - | Triad role (urban_edge, peri_urban, remote). |
| pa_id | string | - | CAPAD PA_ID (stable protected-area identifier). |
| pa_pid | string | - | CAPAD PA_PID (persistent ID). |
| name | string | - | Protected area name. |
| state | string | - | State or territory code. |
| iucn | string | - | IUCN category (if available). |
| area_km2 | float | km2 | Area used for triad selection (EPSG:3577). |
| distance_km | float | km | Distance from PA centroid to nearest major city (EPSG:3577). |
| nearest_city | string | - | Nearest major city in the triad list. |

## smoke_test_triad_geoms

File: `data/processed/smoke_test_triad_geoms_v0_1_0.gpkg`
Format: gpkg

Triad geometries with attributes (EPSG:3577).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| pa_id | string | - | CAPAD PA_ID (stable protected-area identifier). |
| pa_pid | string | - | CAPAD PA_PID (persistent ID). |
| name | string | - | Protected area name. |
| state | string | - | State or territory code. |
| iucn | string | - | IUCN category (if available). |
| triad_role | string | - | Triad role (urban_edge, peri_urban, remote). |
| area_km2 | float | km2 | Area in EPSG:3577. |
| distance_km | float | km | Distance to nearest major city (EPSG:3577). |
| nearest_city | string | - | Nearest major city in the triad list. |
| geometry | geometry | EPSG:3577 | Protected-area geometry. |

## smoke_test_triad_rings

File: `data/processed/smoke_test_triad_rings_v0_1_0.csv`
Format: csv

Triad inside-ring summary table (area per ring).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| pa_id | string | - | CAPAD PA_ID. |
| triad_role | string | - | Triad role. |
| ring_index | int | - | Ring bin index (0..n-1). |
| ring_inner_km | float | km | Inner distance from boundary. |
| ring_outer_km | float | km | Outer distance from boundary. |
| area_km2 | float | km2 | Ring area in EPSG:3577. |

## smoke_test_triad_buffers

File: `data/processed/smoke_test_triad_buffers_v0_1_0.gpkg`
Format: gpkg

Triad outside buffers (difference between buffer and PA).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| pa_id | string | - | CAPAD PA_ID. |
| triad_role | string | - | Triad role. |
| buffer_km | float | km | Outside buffer distance. |
| geometry | geometry | EPSG:3577 | Buffer polygon geometry. |

## pa_geometries

File: `data/processed/pa_geometries_v0_1_0.csv`
Format: csv

Processed CAPAD geometries (dissolved by PA_ID).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for PA geometry outputs. |
| pa_id | string | - | CAPAD PA_ID (stable protected-area identifier). |
| pa_pid | string | - | CAPAD PA_PID (persistent ID). |
| NAME | string | - | Protected area name (CAPAD attribute). |
| STATE | string | - | State or territory code (CAPAD attribute). |
| IUCN | string | - | IUCN category (CAPAD attribute). |
| TYPE | string | - | Protected area type (CAPAD attribute). |
| TYPE_ABBR | string | - | Protected area type abbreviation. |
| NRS_PA | string | - | CAPAD terrestrial PA flag (Y/N). |
| NRS_MPA | string | - | CAPAD marine PA flag (Y/N). |
| part_count | int | - | Number of multipart geometries prior to dissolve. |
| valid_original_all | bool | - | All original parts were valid geometries. |
| valid_fixed_all | bool | - | All repaired parts are valid geometries. |
| area_km2 | float | km2 | Dissolved area in EPSG:3577. |
| perimeter_km | float | km | Dissolved perimeter in EPSG:3577. |
| compactness | float | - | Shape compactness (4*pi*area / perimeter^2). |
| valid_original | bool | - | Validity of representative geometry pre-fix. |
| valid_fixed | bool | - | Validity of representative geometry post-fix. |
| geometry_empty | bool | - | Representative geometry empty after fix. |

Notes:
- The GPKG output contains the same attributes plus geometry.

## pa_radiance_buffers_smoketest

File: `data/processed/pa_radiance_buffers_smoketest_v0_1_0.csv`
Format: csv

Smoke-test radiance summaries inside PAs and outside buffers.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for radiance outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| triad_role | string | - | Triad role. |
| year | int | year | Observation year. |
| zone | string | - | Zone label: inside or buffer. |
| buffer_km | float | km | Buffer distance for zone=buffer; NA for inside. |
| scale_metadata | float | - | Raster scale metadata (raw GeoTIFF). |
| offset_metadata | float | - | Raster offset metadata (raw GeoTIFF). |
| pixel_count | int | pixels | Total pixels sampled (incl. invalid). |
| valid_pixel_count | int | pixels | Valid pixels after masking. |
| valid_fraction | float | - | valid_pixel_count / pixel_count. |
| mean | float | raw | Mean of valid pixel values. |
| median | float | raw | Median of valid pixel values. |
| min | float | raw | Minimum valid pixel value. |
| max | float | raw | Maximum valid pixel value. |
| std | float | raw | Standard deviation of valid pixel values. |

Notes:
- Statistics are computed on raw stored raster values; scale/offset not applied.

## pa_edge_profiles_smoketest

File: `data/processed/pa_edge_profiles_smoketest_v0_1_0.csv`
Format: csv

Smoke-test inside ring (distance-to-edge) radiance profiles.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for edge profile outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| triad_role | string | - | Triad role. |
| year | int | year | Observation year. |
| ring_index | int | - | Ring bin index (0..n-1). |
| ring_inner_km | float | km | Inner distance from boundary. |
| ring_outer_km | float | km | Outer distance from boundary. |
| scale_metadata | float | - | Raster scale metadata (raw GeoTIFF). |
| offset_metadata | float | - | Raster offset metadata (raw GeoTIFF). |
| pixel_count | int | pixels | Total pixels sampled (incl. invalid). |
| valid_pixel_count | int | pixels | Valid pixels after masking. |
| valid_fraction | float | - | valid_pixel_count / pixel_count. |
| mean | float | raw | Mean of valid pixel values. |
| median | float | raw | Median of valid pixel values. |
| min | float | raw | Minimum valid pixel value. |
| max | float | raw | Maximum valid pixel value. |
| std | float | raw | Standard deviation of valid pixel values. |

Notes:
- Statistics are computed on raw stored raster values; scale/offset not applied.

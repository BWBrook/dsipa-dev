# Output schema reference

Generated: 2026-01-02 02:15 UTC

Schema version: 0.2.0

Migration policy: Any change to required columns or their meaning requires a schema_version bump and a full rerun. No automatic migration is provided.

## smoke_test_triad_index

File: `data/processed/smoke_test_triad_index_v0_2_0.csv`
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

File: `data/processed/smoke_test_triad_geoms_v0_2_0.gpkg`
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

File: `data/processed/smoke_test_triad_rings_v0_2_0.csv`
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

File: `data/processed/smoke_test_triad_buffers_v0_2_0.gpkg`
Format: gpkg

Triad outside buffers (difference between buffer and PA).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| pa_id | string | - | CAPAD PA_ID. |
| triad_role | string | - | Triad role. |
| buffer_km | float | km | Outside buffer distance. |
| geometry | geometry | EPSG:3577 | Buffer polygon geometry. |

## pa_geometries

File: `data/processed/pa_geometries_v0_2_0.csv`
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

File: `data/processed/pa_radiance_buffers_smoketest_v0_2_0.csv`
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
| scale_metadata | float | - | Raster scale metadata (GeoTIFF). |
| offset_metadata | float | - | Raster offset metadata (GeoTIFF). |
| pixel_count | int | pixels | Total pixels sampled (incl. invalid). |
| valid_pixel_count | int | pixels | Valid pixels after masking. |
| valid_fraction | float | - | valid_pixel_count / pixel_count. |
| mean | float | scaled | Mean of valid pixel values (scale/offset applied). |
| median | float | scaled | Median of valid pixel values (scale/offset applied). |
| min | float | scaled | Minimum valid pixel value (scale/offset applied). |
| max | float | scaled | Maximum valid pixel value (scale/offset applied). |
| std | float | scaled | Standard deviation of valid pixel values (scale/offset applied). |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_edge_profiles_smoketest

File: `data/processed/pa_edge_profiles_smoketest_v0_2_0.csv`
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
| scale_metadata | float | - | Raster scale metadata (GeoTIFF). |
| offset_metadata | float | - | Raster offset metadata (GeoTIFF). |
| pixel_count | int | pixels | Total pixels sampled (incl. invalid). |
| valid_pixel_count | int | pixels | Valid pixels after masking. |
| valid_fraction | float | - | valid_pixel_count / pixel_count. |
| mean | float | scaled | Mean of valid pixel values (scale/offset applied). |
| median | float | scaled | Median of valid pixel values (scale/offset applied). |
| min | float | scaled | Minimum valid pixel value (scale/offset applied). |
| max | float | scaled | Maximum valid pixel value (scale/offset applied). |
| std | float | scaled | Standard deviation of valid pixel values (scale/offset applied). |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_radiance_buffers_national

File: `data/processed/pa_radiance_buffers_national_v0_2_0.csv`
Format: csv

National radiance summaries inside PAs and outside buffers.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for radiance outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| year | int | year | Observation year. |
| zone | string | - | Zone label: inside or buffer. |
| buffer_km | float | km | Buffer distance for zone=buffer; NA for inside. |
| scale_metadata | float | - | Raster scale metadata (GeoTIFF). |
| offset_metadata | float | - | Raster offset metadata (GeoTIFF). |
| pixel_count | int | pixels | Total pixels sampled (incl. invalid). |
| valid_pixel_count | int | pixels | Valid pixels after masking. |
| valid_fraction | float | - | valid_pixel_count / pixel_count. |
| mean | float | scaled | Mean of valid pixel values (scale/offset applied). |
| median | float | scaled | Median of valid pixel values (scale/offset applied). |
| min | float | scaled | Minimum valid pixel value (scale/offset applied). |
| max | float | scaled | Maximum valid pixel value (scale/offset applied). |
| std | float | scaled | Standard deviation of valid pixel values (scale/offset applied). |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_edge_profiles_national

File: `data/processed/pa_edge_profiles_national_v0_2_0.csv`
Format: csv

National inside ring (distance-to-edge) radiance profiles.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for edge profile outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| year | int | year | Observation year. |
| ring_index | int | - | Ring bin index (0..n-1). |
| ring_inner_km | float | km | Inner distance from boundary. |
| ring_outer_km | float | km | Outer distance from boundary. |
| scale_metadata | float | - | Raster scale metadata (GeoTIFF). |
| offset_metadata | float | - | Raster offset metadata (GeoTIFF). |
| pixel_count | int | pixels | Total pixels sampled (incl. invalid). |
| valid_pixel_count | int | pixels | Valid pixels after masking. |
| valid_fraction | float | - | valid_pixel_count / pixel_count. |
| mean | float | scaled | Mean of valid pixel values (scale/offset applied). |
| median | float | scaled | Median of valid pixel values (scale/offset applied). |
| min | float | scaled | Minimum valid pixel value (scale/offset applied). |
| max | float | scaled | Maximum valid pixel value (scale/offset applied). |
| std | float | scaled | Standard deviation of valid pixel values (scale/offset applied). |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_trends

File: `data/processed/pa_trends_v0_2_0.csv`
Format: csv

Protected-area trend estimates and retention indices.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for trend outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| n_years_inside | int | years | Valid years used for inside trend. |
| slope_inside | float | scaled/year | Theil-Sen slope for inside metric. |
| intercept_inside | float | scaled | Theil-Sen intercept for inside metric. |
| n_years_buffer_1km | int | years | Valid years used for 1 km buffer trend. |
| slope_buffer_1km | float | scaled/year | Theil-Sen slope for 1 km buffer metric. |
| intercept_buffer_1km | float | scaled | Theil-Sen intercept for 1 km buffer metric. |
| n_years_buffer_5km | int | years | Valid years used for 5 km buffer trend. |
| slope_buffer_5km | float | scaled/year | Theil-Sen slope for 5 km buffer metric. |
| intercept_buffer_5km | float | scaled | Theil-Sen intercept for 5 km buffer metric. |
| method | string | - | Trend estimator name. |
| metric | string | - | Metric used for trends (mean or median). |
| retention_index_1km | float | scaled/year | Inside slope minus 1 km buffer slope. |
| retention_index_5km | float | scaled/year | Inside slope minus 5 km buffer slope. |

## pa_risk_rankings

File: `data/processed/pa_risk_rankings_v0_2_0.csv`
Format: csv

Ranked protected areas by brightening/retention metrics (mean trends).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for risk rankings. |
| pa_id | string | - | CAPAD PA_ID. |
| name | string | - | Protected area name. |
| state | string | - | State or territory code. |
| area_km2 | float | km2 | Protected area size. |
| distance_km | float | km | Distance to nearest major city. |
| slope_inside | float | scaled/year | Inside mean trend slope. |
| slope_buffer_1km | float | scaled/year | 1 km buffer mean trend slope. |
| slope_buffer_5km | float | scaled/year | 5 km buffer mean trend slope. |
| retention_index_1km | float | scaled/year | Inside minus 1 km buffer slope. |
| retention_index_5km | float | scaled/year | Inside minus 5 km buffer slope. |
| risk_score | float | - | Mean z-score of inside slope and retention indices. |
| rank_slope_inside | int | - | Rank by slope_inside (1=largest brightening). |
| rank_retention_1km | int | - | Rank by retention_index_1km (1=largest inside-outside contrast). |
| rank_retention_5km | int | - | Rank by retention_index_5km (1=largest inside-outside contrast). |
| rank_risk_score | int | - | Rank by combined risk score (1=highest risk). |

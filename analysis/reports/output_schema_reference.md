# Output schema reference

Generated: 2026-01-06 03:26 UTC

Schema version: 0.3.0

Migration policy: Any change to required columns or their meaning requires a schema_version bump and a full rerun. No automatic migration is provided.

## smoke_test_triad_index

File: `data/processed/smoke_test_triad_index_v0_3_0.csv`
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

File: `data/processed/smoke_test_triad_geoms_v0_3_0.gpkg`
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

File: `data/processed/smoke_test_triad_rings_v0_3_0.csv`
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

File: `data/processed/smoke_test_triad_buffers_v0_3_0.gpkg`
Format: gpkg

Triad outside buffers (difference between buffer and PA).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| pa_id | string | - | CAPAD PA_ID. |
| triad_role | string | - | Triad role. |
| buffer_km | float | km | Outside buffer distance. |
| geometry | geometry | EPSG:3577 | Buffer polygon geometry. |

## pa_geometries

File: `data/processed/pa_geometries_v0_3_0.csv`
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

File: `data/processed/pa_radiance_buffers_smoketest_v0_3_0.csv`
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
| buffer_type | string | - | Buffer variant: raw, land, land_unprotected (inside for zone=inside). |
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
| frac_gt0 | float | - | Fraction of valid pixels greater than 0. |
| p95 | float | scaled | 95th percentile of valid pixel values. |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_edge_profiles_smoketest

File: `data/processed/pa_edge_profiles_smoketest_v0_3_0.csv`
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
| frac_gt0 | float | - | Fraction of valid pixels greater than 0. |
| p95 | float | scaled | 95th percentile of valid pixel values. |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_radiance_buffers_national

File: `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
Format: csv

National radiance summaries inside PAs and outside buffers.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for radiance outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| year | int | year | Observation year. |
| zone | string | - | Zone label: inside or buffer. |
| buffer_km | float | km | Buffer distance for zone=buffer; NA for inside. |
| buffer_type | string | - | Buffer variant: raw, land, land_unprotected (inside for zone=inside). |
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
| frac_gt0 | float | - | Fraction of valid pixels greater than 0. |
| p95 | float | scaled | 95th percentile of valid pixel values. |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_buffer_validity

File: `data/processed/pa_buffer_validity_v0_3_0.csv`
Format: csv

Buffer validity descriptors (land fraction + protected overlap).

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for buffer validity outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| buffer_km | float | km | Buffer distance. |
| buffer_area_km2 | float | km2 | Raw buffer area (outside PA). |
| land_area_km2 | float | km2 | Land area within buffer. |
| protected_overlap_km2 | float | km2 | Overlap area with protected areas (land-masked). |
| effective_land_area_km2 | float | km2 | Land area excluding protected-overlap area. |
| land_fraction | float | - | Land area fraction of raw buffer. |
| protected_overlap_fraction | float | - | Protected overlap fraction of raw buffer (land-masked). |

## pa_edge_profiles_national

File: `data/processed/pa_edge_profiles_national_v0_3_0.csv`
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
| frac_gt0 | float | - | Fraction of valid pixels greater than 0. |
| p95 | float | scaled | 95th percentile of valid pixel values. |

Notes:
- Statistics are computed on scaled raster values; scale/offset metadata applied.

## pa_trends

File: `data/processed/pa_trends_v0_3_0.csv`
Format: csv

Protected-area trend estimates and retention indices.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for trend outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| buffer_type | string | - | Buffer variant used for outside trends (raw, land, land_unprotected). |
| metric | string | - | Metric used for trends. |
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
| retention_index_1km | float | scaled/year | Inside slope minus 1 km buffer slope. |
| retention_index_5km | float | scaled/year | Inside slope minus 5 km buffer slope. |

## pa_risk_rankings

File: `data/processed/pa_risk_rankings_v0_3_0.csv`
Format: csv

Ranked protected areas by brightening/retention categories.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for risk rankings. |
| pa_id | string | - | CAPAD PA_ID. |
| name | string | - | Protected area name. |
| state | string | - | State or territory code. |
| area_km2 | float | km2 | Protected area size. |
| distance_km | float | km | Distance to nearest major city. |
| buffer_type | string | - | Buffer variant used for outside trends (raw, land, land_unprotected). |
| metric | string | - | Metric used for trends. |
| slope_inside | float | scaled/year | Inside mean trend slope. |
| slope_buffer_1km | float | scaled/year | 1 km buffer mean trend slope. |
| slope_buffer_5km | float | scaled/year | 5 km buffer mean trend slope. |
| retention_index_1km | float | scaled/year | Inside minus 1 km buffer slope. |
| retention_index_5km | float | scaled/year | Inside minus 5 km buffer slope. |
| inside_brightening | bool | - | Inside slope > 0. |
| buffer_brightening_1km | bool | - | Buffer 1 km slope > 0. |
| internalisation_1km | bool | - | Inside slope > 0 and inside slope > buffer 1 km slope. |
| external_pressure_1km | bool | - | Buffer 1 km slope > 0 while inside slope <= 0. |
| rank_inside_brightening | int | - | Rank by inside brightening (1=largest). |
| rank_buffer_brightening_1km | int | - | Rank by buffer 1 km brightening. |
| rank_internalisation_1km | int | - | Rank by internalisation contrast. |
| rank_external_pressure_1km | int | - | Rank by external pressure. |

## pa_ibra_assignment

File: `data/processed/pa_ibra_assignment_v0_3_0.csv`
Format: csv

Dominant IBRA region assignment for each protected area.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for IBRA assignments. |
| pa_id | string | - | CAPAD PA_ID. |
| ibra_code | string | - | IBRA region code (REG_CODE_7). |
| ibra_name | string | - | IBRA region name. |
| ibra_area_km2 | float | km2 | PA area within dominant IBRA region. |
| pa_area_km2 | float | km2 | Total PA area (EPSG:3577). |
| ibra_share | float | fraction | Share of PA area in dominant IBRA region. |
| ibra_n | int | count | Number of IBRA regions intersecting PA. |

## pa_trend_bootstrap_summary

File: `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
Format: csv

Bootstrap uncertainty summaries for inside mean radiance trends.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for trend bootstrap outputs. |
| pa_id | string | - | CAPAD PA_ID. |
| ibra_code | string | - | Dominant IBRA region code. |
| ibra_name | string | - | Dominant IBRA region name. |
| ibra_share | float | fraction | Share of PA area in dominant IBRA region. |
| n_years | int | count | Number of valid years in the PA time series. |
| slope_full | float | scaled/yr | Theil-Sen slope on full time series. |
| slope_median | float | scaled/yr | Bootstrap median slope. |
| slope_ci_low | float | scaled/yr | Bootstrap 2.5th percentile slope. |
| slope_ci_high | float | scaled/yr | Bootstrap 97.5th percentile slope. |
| prob_slope_gt0 | float | fraction | Bootstrap P(slope > 0). |
| n_boot | int | count | Number of bootstrap draws contributing to PA. |
| method | string | - | Trend estimator (theil_sen). |
| bootstrap | string | - | Bootstrap design label. |
| block_len | int | years | Moving-block length (years). |
| n_boot_target | int | count | Requested bootstrap draws. |
| min_valid_pixels | int | pixels | Minimum valid pixels per year. |
| min_valid_years | int | count | Minimum valid years per PA. |

## layerB_occurrence_summary

File: `data/processed/layerB_occurrence_summary_v0_3_0.csv`
Format: csv

Layer B occurrence summary counts by taxon group and filter stage.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for Layer B summary. |
| group | string | - | Taxon group key (microbats, diurnal_birds, diurnal_reptiles). |
| label | string | - | Human-readable taxon group label. |
| raw_records | int | count | Raw records downloaded from ALA. |
| filtered_records | int | count | Records after quality filters. |
| dedup_records | int | count | Records after spatial/day deduplication. |
| unique_species | int | count | Unique species retained after filters. |

## layerB_ala_license_ledger

File: `data/processed/layerB_ala_license_ledger_v0_3_0.csv`
Format: csv

Layer B ALA license/provenance ledger joined to processed record counts.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for Layer B license ledger. |
| group | string | - | Taxon group key (microbats, diurnal_birds). |
| label | string | - | Human-readable taxon group label. |
| data_resource_uid | string | - | ALA data resource UID. |
| provider_name | string | - | Provider/resource name. |
| doi | string | - | DOI or citation identifier (if present). |
| citation | string | - | Citation text from ALA. |
| rights | string | - | Rights/license string from ALA. |
| more_information | string | - | More information URL. |
| download_records | int | count | Records in original ALA download. |
| processed_records | int | count | Records retained after filters/dedup. |
| processed_share | float | fraction | Share of processed records for group. |

## layerB_model_input_summary

File: `data/processed/layerB_model_input_summary_v0_3_0.csv`
Format: csv

Layer B model input summary for provider-matched and sensitivity runs.

| Column | Type | Units | Description |
| --- | --- | --- | --- |
| schema_version | string | - | Schema version for Layer B model input summary. |
| run | string | - | Run label (primary_dr368 or sensitivity_all). |
| group | string | - | Taxon group label (microbats or diurnal_birds). |
| n_records | int | count | Number of records in the model subset. |
| providers | string | - | Provider UID(s) included in the subset. |
| years_min | int | year | Earliest year in the subset. |
| years_max | int | year | Latest year in the subset. |
| inside_fraction | float | fraction | Share of records inside protected areas. |
| within_fraction | float | fraction | Share of records within buffer but outside. |
| zero_fraction | float | fraction | Share of records with ALAN = 0. |
| block_km | float | km | Spatial block size (km). |
| buffer_km | float | km | Buffer distance used for scope (km). |
| sample_rate | float | fraction | Random subsample rate applied to sensitivity runs. |

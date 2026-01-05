"""Output schema definitions for DSIPA-NBS."""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "0.3.0"
SCHEMA_SLUG = SCHEMA_VERSION.replace(".", "_")

TRIAD_INDEX_CSV = f"data/processed/smoke_test_triad_index_v{SCHEMA_SLUG}.csv"
TRIAD_GEOMS_GPKG = f"data/processed/smoke_test_triad_geoms_v{SCHEMA_SLUG}.gpkg"
TRIAD_RINGS_CSV = f"data/processed/smoke_test_triad_rings_v{SCHEMA_SLUG}.csv"
TRIAD_BUFFERS_GPKG = f"data/processed/smoke_test_triad_buffers_v{SCHEMA_SLUG}.gpkg"

PA_GEOMETRIES_CSV = f"data/processed/pa_geometries_v{SCHEMA_SLUG}.csv"
PA_GEOMETRIES_GPKG = f"data/processed/pa_geometries_v{SCHEMA_SLUG}.gpkg"

RADIANCE_BUFFERS_SMOKETEST_CSV = (
    f"data/processed/pa_radiance_buffers_smoketest_v{SCHEMA_SLUG}.csv"
)
EDGE_PROFILES_SMOKETEST_CSV = (
    f"data/processed/pa_edge_profiles_smoketest_v{SCHEMA_SLUG}.csv"
)
RADIANCE_BUFFERS_NATIONAL_CSV = (
    f"data/processed/pa_radiance_buffers_national_v{SCHEMA_SLUG}.csv"
)
PA_BUFFER_VALIDITY_CSV = (
    f"data/processed/pa_buffer_validity_v{SCHEMA_SLUG}.csv"
)
EDGE_PROFILES_NATIONAL_CSV = (
    f"data/processed/pa_edge_profiles_national_v{SCHEMA_SLUG}.csv"
)
PA_TRENDS_CSV = f"data/processed/pa_trends_v{SCHEMA_SLUG}.csv"
PA_RISK_RANKINGS_CSV = f"data/processed/pa_risk_rankings_v{SCHEMA_SLUG}.csv"
LAYERB_OCCURRENCE_SUMMARY_CSV = (
    f"data/processed/layerB_occurrence_summary_v{SCHEMA_SLUG}.csv"
)
LAYERB_ALA_LICENSE_LEDGER_CSV = (
    f"data/processed/layerB_ala_license_ledger_v{SCHEMA_SLUG}.csv"
)
LAYERB_MODEL_INPUT_SUMMARY_CSV = (
    f"data/processed/layerB_model_input_summary_v{SCHEMA_SLUG}.csv"
)


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    dtype: str
    units: str
    description: str


@dataclass(frozen=True)
class OutputSchema:
    key: str
    filename: str
    file_type: str
    description: str
    columns: tuple[ColumnSpec, ...]
    notes: tuple[str, ...] = ()

    @property
    def column_names(self) -> tuple[str, ...]:
        return tuple(col.name for col in self.columns)


TRIAD_INDEX_SCHEMA = OutputSchema(
    key="smoke_test_triad_index",
    filename=TRIAD_INDEX_CSV,
    file_type="csv",
    description="Triad selection table (three protected areas).",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for triad outputs."),
        ColumnSpec("triad_role", "string", "-", "Triad role (urban_edge, peri_urban, remote)."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID (stable protected-area identifier)."),
        ColumnSpec("pa_pid", "string", "-", "CAPAD PA_PID (persistent ID)."),
        ColumnSpec("name", "string", "-", "Protected area name."),
        ColumnSpec("state", "string", "-", "State or territory code."),
        ColumnSpec("iucn", "string", "-", "IUCN category (if available)."),
        ColumnSpec("area_km2", "float", "km2", "Area used for triad selection (EPSG:3577)."),
        ColumnSpec(
            "distance_km",
            "float",
            "km",
            "Distance from PA centroid to nearest major city (EPSG:3577).",
        ),
        ColumnSpec("nearest_city", "string", "-", "Nearest major city in the triad list."),
    ),
)

TRIAD_GEOMS_SCHEMA = OutputSchema(
    key="smoke_test_triad_geoms",
    filename=TRIAD_GEOMS_GPKG,
    file_type="gpkg",
    description="Triad geometries with attributes (EPSG:3577).",
    columns=(
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID (stable protected-area identifier)."),
        ColumnSpec("pa_pid", "string", "-", "CAPAD PA_PID (persistent ID)."),
        ColumnSpec("name", "string", "-", "Protected area name."),
        ColumnSpec("state", "string", "-", "State or territory code."),
        ColumnSpec("iucn", "string", "-", "IUCN category (if available)."),
        ColumnSpec("triad_role", "string", "-", "Triad role (urban_edge, peri_urban, remote)."),
        ColumnSpec("area_km2", "float", "km2", "Area in EPSG:3577."),
        ColumnSpec("distance_km", "float", "km", "Distance to nearest major city (EPSG:3577)."),
        ColumnSpec("nearest_city", "string", "-", "Nearest major city in the triad list."),
        ColumnSpec("geometry", "geometry", "EPSG:3577", "Protected-area geometry."),
    ),
)

TRIAD_RINGS_SCHEMA = OutputSchema(
    key="smoke_test_triad_rings",
    filename=TRIAD_RINGS_CSV,
    file_type="csv",
    description="Triad inside-ring summary table (area per ring).",
    columns=(
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("triad_role", "string", "-", "Triad role."),
        ColumnSpec("ring_index", "int", "-", "Ring bin index (0..n-1)."),
        ColumnSpec("ring_inner_km", "float", "km", "Inner distance from boundary."),
        ColumnSpec("ring_outer_km", "float", "km", "Outer distance from boundary."),
        ColumnSpec("area_km2", "float", "km2", "Ring area in EPSG:3577."),
    ),
)

TRIAD_BUFFERS_SCHEMA = OutputSchema(
    key="smoke_test_triad_buffers",
    filename=TRIAD_BUFFERS_GPKG,
    file_type="gpkg",
    description="Triad outside buffers (difference between buffer and PA).",
    columns=(
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("triad_role", "string", "-", "Triad role."),
        ColumnSpec("buffer_km", "float", "km", "Outside buffer distance."),
        ColumnSpec("geometry", "geometry", "EPSG:3577", "Buffer polygon geometry."),
    ),
)

PA_GEOMETRIES_SCHEMA = OutputSchema(
    key="pa_geometries",
    filename=PA_GEOMETRIES_CSV,
    file_type="csv",
    description="Processed CAPAD geometries (dissolved by PA_ID).",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for PA geometry outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID (stable protected-area identifier)."),
        ColumnSpec("pa_pid", "string", "-", "CAPAD PA_PID (persistent ID)."),
        ColumnSpec("NAME", "string", "-", "Protected area name (CAPAD attribute)."),
        ColumnSpec("STATE", "string", "-", "State or territory code (CAPAD attribute)."),
        ColumnSpec("IUCN", "string", "-", "IUCN category (CAPAD attribute)."),
        ColumnSpec("TYPE", "string", "-", "Protected area type (CAPAD attribute)."),
        ColumnSpec("TYPE_ABBR", "string", "-", "Protected area type abbreviation."),
        ColumnSpec("NRS_PA", "string", "-", "CAPAD terrestrial PA flag (Y/N)."),
        ColumnSpec("NRS_MPA", "string", "-", "CAPAD marine PA flag (Y/N)."),
        ColumnSpec(
            "part_count",
            "int",
            "-",
            "Number of multipart geometries prior to dissolve.",
        ),
        ColumnSpec(
            "valid_original_all",
            "bool",
            "-",
            "All original parts were valid geometries.",
        ),
        ColumnSpec(
            "valid_fixed_all",
            "bool",
            "-",
            "All repaired parts are valid geometries.",
        ),
        ColumnSpec("area_km2", "float", "km2", "Dissolved area in EPSG:3577."),
        ColumnSpec("perimeter_km", "float", "km", "Dissolved perimeter in EPSG:3577."),
        ColumnSpec(
            "compactness",
            "float",
            "-",
            "Shape compactness (4*pi*area / perimeter^2).",
        ),
        ColumnSpec("valid_original", "bool", "-", "Validity of representative geometry pre-fix."),
        ColumnSpec("valid_fixed", "bool", "-", "Validity of representative geometry post-fix."),
        ColumnSpec("geometry_empty", "bool", "-", "Representative geometry empty after fix."),
    ),
    notes=(
        "The GPKG output contains the same attributes plus geometry.",
    ),
)

RADIANCE_BUFFERS_SMOKETEST_SCHEMA = OutputSchema(
    key="pa_radiance_buffers_smoketest",
    filename=RADIANCE_BUFFERS_SMOKETEST_CSV,
    file_type="csv",
    description="Smoke-test radiance summaries inside PAs and outside buffers.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for radiance outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("triad_role", "string", "-", "Triad role."),
        ColumnSpec("year", "int", "year", "Observation year."),
        ColumnSpec("zone", "string", "-", "Zone label: inside or buffer."),
        ColumnSpec("buffer_km", "float", "km", "Buffer distance for zone=buffer; NA for inside."),
        ColumnSpec(
            "buffer_type",
            "string",
            "-",
            "Buffer variant: raw, land, land_unprotected (inside for zone=inside).",
        ),
        ColumnSpec("scale_metadata", "float", "-", "Raster scale metadata (GeoTIFF)."),
        ColumnSpec("offset_metadata", "float", "-", "Raster offset metadata (GeoTIFF)."),
        ColumnSpec("pixel_count", "int", "pixels", "Total pixels sampled (incl. invalid)."),
        ColumnSpec("valid_pixel_count", "int", "pixels", "Valid pixels after masking."),
        ColumnSpec("valid_fraction", "float", "-", "valid_pixel_count / pixel_count."),
        ColumnSpec("mean", "float", "scaled", "Mean of valid pixel values (scale/offset applied)."),
        ColumnSpec("median", "float", "scaled", "Median of valid pixel values (scale/offset applied)."),
        ColumnSpec("min", "float", "scaled", "Minimum valid pixel value (scale/offset applied)."),
        ColumnSpec("max", "float", "scaled", "Maximum valid pixel value (scale/offset applied)."),
        ColumnSpec("std", "float", "scaled", "Standard deviation of valid pixel values (scale/offset applied)."),
        ColumnSpec("frac_gt0", "float", "-", "Fraction of valid pixels greater than 0."),
        ColumnSpec("p95", "float", "scaled", "95th percentile of valid pixel values."),
    ),
    notes=(
        "Statistics are computed on scaled raster values; scale/offset metadata applied.",
    ),
)

EDGE_PROFILES_SMOKETEST_SCHEMA = OutputSchema(
    key="pa_edge_profiles_smoketest",
    filename=EDGE_PROFILES_SMOKETEST_CSV,
    file_type="csv",
    description="Smoke-test inside ring (distance-to-edge) radiance profiles.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for edge profile outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("triad_role", "string", "-", "Triad role."),
        ColumnSpec("year", "int", "year", "Observation year."),
        ColumnSpec("ring_index", "int", "-", "Ring bin index (0..n-1)."),
        ColumnSpec("ring_inner_km", "float", "km", "Inner distance from boundary."),
        ColumnSpec("ring_outer_km", "float", "km", "Outer distance from boundary."),
        ColumnSpec("scale_metadata", "float", "-", "Raster scale metadata (GeoTIFF)."),
        ColumnSpec("offset_metadata", "float", "-", "Raster offset metadata (GeoTIFF)."),
        ColumnSpec("pixel_count", "int", "pixels", "Total pixels sampled (incl. invalid)."),
        ColumnSpec("valid_pixel_count", "int", "pixels", "Valid pixels after masking."),
        ColumnSpec("valid_fraction", "float", "-", "valid_pixel_count / pixel_count."),
        ColumnSpec("mean", "float", "scaled", "Mean of valid pixel values (scale/offset applied)."),
        ColumnSpec("median", "float", "scaled", "Median of valid pixel values (scale/offset applied)."),
        ColumnSpec("min", "float", "scaled", "Minimum valid pixel value (scale/offset applied)."),
        ColumnSpec("max", "float", "scaled", "Maximum valid pixel value (scale/offset applied)."),
        ColumnSpec("std", "float", "scaled", "Standard deviation of valid pixel values (scale/offset applied)."),
        ColumnSpec("frac_gt0", "float", "-", "Fraction of valid pixels greater than 0."),
        ColumnSpec("p95", "float", "scaled", "95th percentile of valid pixel values."),
    ),
    notes=(
        "Statistics are computed on scaled raster values; scale/offset metadata applied.",
    ),
)

RADIANCE_BUFFERS_NATIONAL_SCHEMA = OutputSchema(
    key="pa_radiance_buffers_national",
    filename=RADIANCE_BUFFERS_NATIONAL_CSV,
    file_type="csv",
    description="National radiance summaries inside PAs and outside buffers.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for radiance outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("year", "int", "year", "Observation year."),
        ColumnSpec("zone", "string", "-", "Zone label: inside or buffer."),
        ColumnSpec("buffer_km", "float", "km", "Buffer distance for zone=buffer; NA for inside."),
        ColumnSpec(
            "buffer_type",
            "string",
            "-",
            "Buffer variant: raw, land, land_unprotected (inside for zone=inside).",
        ),
        ColumnSpec("scale_metadata", "float", "-", "Raster scale metadata (GeoTIFF)."),
        ColumnSpec("offset_metadata", "float", "-", "Raster offset metadata (GeoTIFF)."),
        ColumnSpec("pixel_count", "int", "pixels", "Total pixels sampled (incl. invalid)."),
        ColumnSpec("valid_pixel_count", "int", "pixels", "Valid pixels after masking."),
        ColumnSpec("valid_fraction", "float", "-", "valid_pixel_count / pixel_count."),
        ColumnSpec("mean", "float", "scaled", "Mean of valid pixel values (scale/offset applied)."),
        ColumnSpec("median", "float", "scaled", "Median of valid pixel values (scale/offset applied)."),
        ColumnSpec("min", "float", "scaled", "Minimum valid pixel value (scale/offset applied)."),
        ColumnSpec("max", "float", "scaled", "Maximum valid pixel value (scale/offset applied)."),
        ColumnSpec("std", "float", "scaled", "Standard deviation of valid pixel values (scale/offset applied)."),
        ColumnSpec("frac_gt0", "float", "-", "Fraction of valid pixels greater than 0."),
        ColumnSpec("p95", "float", "scaled", "95th percentile of valid pixel values."),
    ),
    notes=(
        "Statistics are computed on scaled raster values; scale/offset metadata applied.",
    ),
)

PA_BUFFER_VALIDITY_SCHEMA = OutputSchema(
    key="pa_buffer_validity",
    filename=PA_BUFFER_VALIDITY_CSV,
    file_type="csv",
    description="Buffer validity descriptors (land fraction + protected overlap).",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for buffer validity outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("buffer_km", "float", "km", "Buffer distance."),
        ColumnSpec("buffer_area_km2", "float", "km2", "Raw buffer area (outside PA)."),
        ColumnSpec("land_area_km2", "float", "km2", "Land area within buffer."),
        ColumnSpec(
            "protected_overlap_km2",
            "float",
            "km2",
            "Overlap area with protected areas (land-masked).",
        ),
        ColumnSpec(
            "effective_land_area_km2",
            "float",
            "km2",
            "Land area excluding protected-overlap area.",
        ),
        ColumnSpec("land_fraction", "float", "-", "Land area fraction of raw buffer."),
        ColumnSpec(
            "protected_overlap_fraction",
            "float",
            "-",
            "Protected overlap fraction of raw buffer (land-masked).",
        ),
    ),
)

EDGE_PROFILES_NATIONAL_SCHEMA = OutputSchema(
    key="pa_edge_profiles_national",
    filename=EDGE_PROFILES_NATIONAL_CSV,
    file_type="csv",
    description="National inside ring (distance-to-edge) radiance profiles.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for edge profile outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("year", "int", "year", "Observation year."),
        ColumnSpec("ring_index", "int", "-", "Ring bin index (0..n-1)."),
        ColumnSpec("ring_inner_km", "float", "km", "Inner distance from boundary."),
        ColumnSpec("ring_outer_km", "float", "km", "Outer distance from boundary."),
        ColumnSpec("scale_metadata", "float", "-", "Raster scale metadata (GeoTIFF)."),
        ColumnSpec("offset_metadata", "float", "-", "Raster offset metadata (GeoTIFF)."),
        ColumnSpec("pixel_count", "int", "pixels", "Total pixels sampled (incl. invalid)."),
        ColumnSpec("valid_pixel_count", "int", "pixels", "Valid pixels after masking."),
        ColumnSpec("valid_fraction", "float", "-", "valid_pixel_count / pixel_count."),
        ColumnSpec("mean", "float", "scaled", "Mean of valid pixel values (scale/offset applied)."),
        ColumnSpec("median", "float", "scaled", "Median of valid pixel values (scale/offset applied)."),
        ColumnSpec("min", "float", "scaled", "Minimum valid pixel value (scale/offset applied)."),
        ColumnSpec("max", "float", "scaled", "Maximum valid pixel value (scale/offset applied)."),
        ColumnSpec("std", "float", "scaled", "Standard deviation of valid pixel values (scale/offset applied)."),
        ColumnSpec("frac_gt0", "float", "-", "Fraction of valid pixels greater than 0."),
        ColumnSpec("p95", "float", "scaled", "95th percentile of valid pixel values."),
    ),
    notes=(
        "Statistics are computed on scaled raster values; scale/offset metadata applied.",
    ),
)

PA_TRENDS_SCHEMA = OutputSchema(
    key="pa_trends",
    filename=PA_TRENDS_CSV,
    file_type="csv",
    description="Protected-area trend estimates and retention indices.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for trend outputs."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec(
            "buffer_type",
            "string",
            "-",
            "Buffer variant used for outside trends (raw, land, land_unprotected).",
        ),
        ColumnSpec("metric", "string", "-", "Metric used for trends."),
        ColumnSpec("n_years_inside", "int", "years", "Valid years used for inside trend."),
        ColumnSpec("slope_inside", "float", "scaled/year", "Theil-Sen slope for inside metric."),
        ColumnSpec("intercept_inside", "float", "scaled", "Theil-Sen intercept for inside metric."),
        ColumnSpec("n_years_buffer_1km", "int", "years", "Valid years used for 1 km buffer trend."),
        ColumnSpec("slope_buffer_1km", "float", "scaled/year", "Theil-Sen slope for 1 km buffer metric."),
        ColumnSpec("intercept_buffer_1km", "float", "scaled", "Theil-Sen intercept for 1 km buffer metric."),
        ColumnSpec("n_years_buffer_5km", "int", "years", "Valid years used for 5 km buffer trend."),
        ColumnSpec("slope_buffer_5km", "float", "scaled/year", "Theil-Sen slope for 5 km buffer metric."),
        ColumnSpec("intercept_buffer_5km", "float", "scaled", "Theil-Sen intercept for 5 km buffer metric."),
        ColumnSpec("method", "string", "-", "Trend estimator name."),
        ColumnSpec("retention_index_1km", "float", "scaled/year", "Inside slope minus 1 km buffer slope."),
        ColumnSpec("retention_index_5km", "float", "scaled/year", "Inside slope minus 5 km buffer slope."),
    ),
)

PA_RISK_RANKINGS_SCHEMA = OutputSchema(
    key="pa_risk_rankings",
    filename=PA_RISK_RANKINGS_CSV,
    file_type="csv",
    description="Ranked protected areas by brightening/retention categories.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for risk rankings."),
        ColumnSpec("pa_id", "string", "-", "CAPAD PA_ID."),
        ColumnSpec("name", "string", "-", "Protected area name."),
        ColumnSpec("state", "string", "-", "State or territory code."),
        ColumnSpec("area_km2", "float", "km2", "Protected area size."),
        ColumnSpec("distance_km", "float", "km", "Distance to nearest major city."),
        ColumnSpec(
            "buffer_type",
            "string",
            "-",
            "Buffer variant used for outside trends (raw, land, land_unprotected).",
        ),
        ColumnSpec("metric", "string", "-", "Metric used for trends."),
        ColumnSpec("slope_inside", "float", "scaled/year", "Inside mean trend slope."),
        ColumnSpec("slope_buffer_1km", "float", "scaled/year", "1 km buffer mean trend slope."),
        ColumnSpec("slope_buffer_5km", "float", "scaled/year", "5 km buffer mean trend slope."),
        ColumnSpec("retention_index_1km", "float", "scaled/year", "Inside minus 1 km buffer slope."),
        ColumnSpec("retention_index_5km", "float", "scaled/year", "Inside minus 5 km buffer slope."),
        ColumnSpec("inside_brightening", "bool", "-", "Inside slope > 0."),
        ColumnSpec("buffer_brightening_1km", "bool", "-", "Buffer 1 km slope > 0."),
        ColumnSpec(
            "internalisation_1km",
            "bool",
            "-",
            "Inside slope > 0 and inside slope > buffer 1 km slope.",
        ),
        ColumnSpec(
            "external_pressure_1km",
            "bool",
            "-",
            "Buffer 1 km slope > 0 while inside slope <= 0.",
        ),
        ColumnSpec("rank_inside_brightening", "int", "-", "Rank by inside brightening (1=largest)."),
        ColumnSpec("rank_buffer_brightening_1km", "int", "-", "Rank by buffer 1 km brightening."),
        ColumnSpec("rank_internalisation_1km", "int", "-", "Rank by internalisation contrast."),
        ColumnSpec("rank_external_pressure_1km", "int", "-", "Rank by external pressure."),
    ),
)

LAYERB_OCCURRENCE_SUMMARY_SCHEMA = OutputSchema(
    key="layerB_occurrence_summary",
    filename=LAYERB_OCCURRENCE_SUMMARY_CSV,
    file_type="csv",
    description="Layer B occurrence summary counts by taxon group and filter stage.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for Layer B summary."),
        ColumnSpec("group", "string", "-", "Taxon group key (microbats, diurnal_birds, diurnal_reptiles)."),
        ColumnSpec("label", "string", "-", "Human-readable taxon group label."),
        ColumnSpec("raw_records", "int", "count", "Raw records downloaded from ALA."),
        ColumnSpec("filtered_records", "int", "count", "Records after quality filters."),
        ColumnSpec("dedup_records", "int", "count", "Records after spatial/day deduplication."),
        ColumnSpec("unique_species", "int", "count", "Unique species retained after filters."),
    ),
)

LAYERB_ALA_LICENSE_LEDGER_SCHEMA = OutputSchema(
    key="layerB_ala_license_ledger",
    filename=LAYERB_ALA_LICENSE_LEDGER_CSV,
    file_type="csv",
    description="Layer B ALA license/provenance ledger joined to processed record counts.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for Layer B license ledger."),
        ColumnSpec("group", "string", "-", "Taxon group key (microbats, diurnal_birds)."),
        ColumnSpec("label", "string", "-", "Human-readable taxon group label."),
        ColumnSpec("data_resource_uid", "string", "-", "ALA data resource UID."),
        ColumnSpec("provider_name", "string", "-", "Provider/resource name."),
        ColumnSpec("doi", "string", "-", "DOI or citation identifier (if present)."),
        ColumnSpec("citation", "string", "-", "Citation text from ALA."),
        ColumnSpec("rights", "string", "-", "Rights/license string from ALA."),
        ColumnSpec("more_information", "string", "-", "More information URL."),
        ColumnSpec("download_records", "int", "count", "Records in original ALA download."),
        ColumnSpec("processed_records", "int", "count", "Records retained after filters/dedup."),
        ColumnSpec("processed_share", "float", "fraction", "Share of processed records for group."),
    ),
)

LAYERB_MODEL_INPUT_SUMMARY_SCHEMA = OutputSchema(
    key="layerB_model_input_summary",
    filename=LAYERB_MODEL_INPUT_SUMMARY_CSV,
    file_type="csv",
    description="Layer B model input summary for provider-matched and sensitivity runs.",
    columns=(
        ColumnSpec("schema_version", "string", "-", "Schema version for Layer B model input summary."),
        ColumnSpec("run", "string", "-", "Run label (primary_dr368 or sensitivity_all)."),
        ColumnSpec("group", "string", "-", "Taxon group label (microbats or diurnal_birds)."),
        ColumnSpec("n_records", "int", "count", "Number of records in the model subset."),
        ColumnSpec("providers", "string", "-", "Provider UID(s) included in the subset."),
        ColumnSpec("years_min", "int", "year", "Earliest year in the subset."),
        ColumnSpec("years_max", "int", "year", "Latest year in the subset."),
        ColumnSpec("inside_fraction", "float", "fraction", "Share of records inside protected areas."),
        ColumnSpec("within_fraction", "float", "fraction", "Share of records within buffer but outside."),
        ColumnSpec("zero_fraction", "float", "fraction", "Share of records with ALAN = 0."),
        ColumnSpec("block_km", "float", "km", "Spatial block size (km)."),
        ColumnSpec("buffer_km", "float", "km", "Buffer distance used for scope (km)."),
        ColumnSpec("sample_rate", "float", "fraction", "Random subsample rate applied to sensitivity runs."),
    ),
)

OUTPUT_SCHEMAS = (
    TRIAD_INDEX_SCHEMA,
    TRIAD_GEOMS_SCHEMA,
    TRIAD_RINGS_SCHEMA,
    TRIAD_BUFFERS_SCHEMA,
    PA_GEOMETRIES_SCHEMA,
    RADIANCE_BUFFERS_SMOKETEST_SCHEMA,
    EDGE_PROFILES_SMOKETEST_SCHEMA,
    RADIANCE_BUFFERS_NATIONAL_SCHEMA,
    PA_BUFFER_VALIDITY_SCHEMA,
    EDGE_PROFILES_NATIONAL_SCHEMA,
    PA_TRENDS_SCHEMA,
    PA_RISK_RANKINGS_SCHEMA,
    LAYERB_OCCURRENCE_SUMMARY_SCHEMA,
    LAYERB_ALA_LICENSE_LEDGER_SCHEMA,
    LAYERB_MODEL_INPUT_SUMMARY_SCHEMA,
)

OUTPUT_SCHEMAS_BY_KEY = {schema.key: schema for schema in OUTPUT_SCHEMAS}

TRIAD_INDEX_COLUMNS = TRIAD_INDEX_SCHEMA.column_names
TRIAD_GEOMS_COLUMNS = TRIAD_GEOMS_SCHEMA.column_names
TRIAD_RINGS_COLUMNS = TRIAD_RINGS_SCHEMA.column_names
TRIAD_BUFFERS_COLUMNS = TRIAD_BUFFERS_SCHEMA.column_names
PA_GEOMETRIES_COLUMNS = PA_GEOMETRIES_SCHEMA.column_names
RADIANCE_BUFFERS_SMOKETEST_COLUMNS = RADIANCE_BUFFERS_SMOKETEST_SCHEMA.column_names
EDGE_PROFILES_SMOKETEST_COLUMNS = EDGE_PROFILES_SMOKETEST_SCHEMA.column_names
RADIANCE_BUFFERS_NATIONAL_COLUMNS = RADIANCE_BUFFERS_NATIONAL_SCHEMA.column_names
PA_BUFFER_VALIDITY_COLUMNS = PA_BUFFER_VALIDITY_SCHEMA.column_names
EDGE_PROFILES_NATIONAL_COLUMNS = EDGE_PROFILES_NATIONAL_SCHEMA.column_names
PA_TRENDS_COLUMNS = PA_TRENDS_SCHEMA.column_names
PA_RISK_RANKINGS_COLUMNS = PA_RISK_RANKINGS_SCHEMA.column_names
LAYERB_OCCURRENCE_SUMMARY_COLUMNS = LAYERB_OCCURRENCE_SUMMARY_SCHEMA.column_names
LAYERB_MODEL_INPUT_SUMMARY_COLUMNS = LAYERB_MODEL_INPUT_SUMMARY_SCHEMA.column_names

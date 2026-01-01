"""Output schema definitions for DSIPA-NBS."""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "0.1.0"
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
        ColumnSpec("scale_metadata", "float", "-", "Raster scale metadata (raw GeoTIFF)."),
        ColumnSpec("offset_metadata", "float", "-", "Raster offset metadata (raw GeoTIFF)."),
        ColumnSpec("pixel_count", "int", "pixels", "Total pixels sampled (incl. invalid)."),
        ColumnSpec("valid_pixel_count", "int", "pixels", "Valid pixels after masking."),
        ColumnSpec("valid_fraction", "float", "-", "valid_pixel_count / pixel_count."),
        ColumnSpec("mean", "float", "raw", "Mean of valid pixel values."),
        ColumnSpec("median", "float", "raw", "Median of valid pixel values."),
        ColumnSpec("min", "float", "raw", "Minimum valid pixel value."),
        ColumnSpec("max", "float", "raw", "Maximum valid pixel value."),
        ColumnSpec("std", "float", "raw", "Standard deviation of valid pixel values."),
    ),
    notes=(
        "Statistics are computed on raw stored raster values; scale/offset not applied.",
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
        ColumnSpec("scale_metadata", "float", "-", "Raster scale metadata (raw GeoTIFF)."),
        ColumnSpec("offset_metadata", "float", "-", "Raster offset metadata (raw GeoTIFF)."),
        ColumnSpec("pixel_count", "int", "pixels", "Total pixels sampled (incl. invalid)."),
        ColumnSpec("valid_pixel_count", "int", "pixels", "Valid pixels after masking."),
        ColumnSpec("valid_fraction", "float", "-", "valid_pixel_count / pixel_count."),
        ColumnSpec("mean", "float", "raw", "Mean of valid pixel values."),
        ColumnSpec("median", "float", "raw", "Median of valid pixel values."),
        ColumnSpec("min", "float", "raw", "Minimum valid pixel value."),
        ColumnSpec("max", "float", "raw", "Maximum valid pixel value."),
        ColumnSpec("std", "float", "raw", "Standard deviation of valid pixel values."),
    ),
    notes=(
        "Statistics are computed on raw stored raster values; scale/offset not applied.",
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
)

OUTPUT_SCHEMAS_BY_KEY = {schema.key: schema for schema in OUTPUT_SCHEMAS}

TRIAD_INDEX_COLUMNS = TRIAD_INDEX_SCHEMA.column_names
TRIAD_GEOMS_COLUMNS = TRIAD_GEOMS_SCHEMA.column_names
TRIAD_RINGS_COLUMNS = TRIAD_RINGS_SCHEMA.column_names
TRIAD_BUFFERS_COLUMNS = TRIAD_BUFFERS_SCHEMA.column_names
PA_GEOMETRIES_COLUMNS = PA_GEOMETRIES_SCHEMA.column_names
RADIANCE_BUFFERS_SMOKETEST_COLUMNS = RADIANCE_BUFFERS_SMOKETEST_SCHEMA.column_names
EDGE_PROFILES_SMOKETEST_COLUMNS = EDGE_PROFILES_SMOKETEST_SCHEMA.column_names

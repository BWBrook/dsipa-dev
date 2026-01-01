# Data inventory (Layer A)

Generated: 2026-01-01 07:33 UTC

## Protected areas — CAPAD 2024 (DCCEEW)

- Snapshot date: 30 June 2024 (CAPAD 2024 compilation).
- Access: GIS data via DCCEEW ArcGIS REST services (CAPAD MapServer/FeatureServer).
- License: CC-BY (Creative Commons Attribution).
- Coverage: terrestrial + marine in a single layer; Sea Country IPAs included in marine reporting.
- Planned inclusion rule (Layer A core): terrestrial protected areas only (filter on NRS_PA flag).
- Known caveats: interim protected areas included; attributes are contributed by multiple jurisdictions.

Source URLs:
- https://www.dcceew.gov.au/environment/land/nrs/science/capad/2024
- https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer

## Night lights — VIIRS annual average (Zenodo v0.4, Hengl/OpenGeoHub)

- Provider: OpenGeoHub (Hengl et al.), Zenodo record v0.4.
- Coverage: annual global time series (2000–2024). VIIRS-based years start 2012; core analysis uses 2013–2024.
- Resolution/CRS: 500 m (COG) in EPSG:4326.
- Variable: annual average VIIRS composite (`nightlights.average_viirs.v21_*`).
- Scaling: record notes values scaled from 0–200 to 0–2000; scale factor to be confirmed in WP0.6 and recorded.
- Smoke-test years (WP0.6): 2013, 2018, 2024.
- Known caveats: 2012 is partial-year for VIIRS; exclude from trends.

Source URLs:
- https://doi.org/10.5281/zenodo.17294744
- https://zenodo.org/records/17294744

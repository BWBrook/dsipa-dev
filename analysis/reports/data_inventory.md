# Data inventory (Layer A)

Generated: 2026-01-01 04:40 UTC

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

## Night lights — VIIRS DNB annual VNL v2.2 (EOG)

- Provider: Earth Observation Group (Colorado School of Mines).
- Coverage: annual near-global time series (2012–2024), 75N–65S.
- Resolution/CRS: 15 arc-second (~500 m) in EPSG:4326.
- Units: nW/cm^2/sr (radiance).
- Bands: average, median, median-masked, plus coverage statistics.
- Planned band (Layer A core): median-masked radiance to reduce transient outliers.
- Known caveats: background is zeroed via data-range thresholds; annual composites built from monthly cloud-free grids.

Source URLs:
- https://eogdata.mines.edu/products/vnl/
- https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_ANNUAL_V22

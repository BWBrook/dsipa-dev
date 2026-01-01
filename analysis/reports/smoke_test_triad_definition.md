# Smoke-test triad definition (WP0.4)

Generated: 2026-01-01 05:03 UTC

## Selection rule

1) Fetch CAPAD 2024 protected areas (terrestrial; NRS_PA='Y').
2) Filter to area >= 5.0 km^2 and exclude STATE in ['EXT'].
3) Compute distance from each PA centroid to nearest major city (8-city list).
4) Select triad:
   - urban_edge: distance <= 20.0 km, choose largest area (tie-breaker distance, PA_ID)
   - peri_urban: distance in 50.0–150.0 km, choose closest to 100.0 km
   - remote: maximum distance among remaining PAs (tie-breaker area, then PA_ID)

## Selected protected areas

| schema_version | triad_role | pa_id | pa_pid | name | state | iucn | area_km2 | distance_km | nearest_city |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1.0 | urban_edge | TAS_50483 | TAS_50483 | Wellington Park | TAS | II | 180.25 | 15.75 | Hobart |
| 0.1.0 | peri_urban | NSW_N0856 | NSW_N0856 | Coornartha | NSW | Ia | 11.84 | 100.08 | Canberra |
| 0.1.0 | remote | QLD_0117LZI001 | QLD_0117LZI001 | Lizard Island | QLD | II | 9.37 | 1620.46 | Darwin |

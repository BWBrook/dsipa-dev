# Layer A buffer-validity sensitivity

Generated: 2026-09-19 05:50 UTC

Primary retention/quadrant analyses use 1 km `land_unprotected` buffer trends. This sensitivity checks whether headline quadrant counts are stable when conditioning on stricter raw-buffer land fraction and protected-overlap criteria.

## Scenario summary

| scenario | n | retained_fraction | q1_concurrent_brightening | q2_internal_brightening | q3_stable_non_detect | q4_external_pressure | q1_fraction | q4_fraction | median_inside_slope | median_buffer_slope | median_retention_index_1km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| primary_retention_quadrant | 4,253 | 1.000 | 347 | 70 | 3,587 | 249 | 0.082 | 0.059 | 0.000 | 0.000 | 0.000 |
| has_1km_buffer_validity | 4,253 | 1.000 | 347 | 70 | 3,587 | 249 | 0.082 | 0.059 | 0.000 | 0.000 | 0.000 |
| land_fraction_ge_0.50 | 4,127 | 0.970 | 327 | 60 | 3,510 | 230 | 0.079 | 0.056 | 0.000 | 0.000 | 0.000 |
| protected_overlap_le_0.25 | 3,336 | 0.784 | 309 | 55 | 2,759 | 213 | 0.093 | 0.064 | 0.000 | 0.000 | 0.000 |
| land_ge_0.50_and_overlap_le_0.25 | 3,216 | 0.756 | 289 | 45 | 2,687 | 195 | 0.090 | 0.061 | 0.000 | 0.000 | 0.000 |

## Validation notes

- All scenario counts are nested within the primary retention/quadrant denominator.
- Quadrant counts sum to each scenario denominator.

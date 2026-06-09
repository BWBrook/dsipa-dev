# Layer A buffer-validity sensitivity

Generated: 2026-05-25 03:35 UTC

Primary retention/quadrant analyses use 1 km `land_unprotected` buffer trends. This sensitivity checks whether headline quadrant counts are stable when conditioning on stricter raw-buffer land fraction and protected-overlap criteria.

## Scenario summary

| scenario | n | retained_fraction | q1_concurrent_brightening | q2_internal_brightening | q3_stable_non_detect | q4_external_pressure | q1_fraction | q4_fraction | median_inside_slope | median_buffer_slope | median_retention_index_1km |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| primary_retention_quadrant | 3,858 | 1.000 | 305 | 55 | 3,308 | 190 | 0.079 | 0.049 | 0.000 | 0.000 | 0.000 |
| has_1km_buffer_validity | 3,858 | 1.000 | 305 | 55 | 3,308 | 190 | 0.079 | 0.049 | 0.000 | 0.000 | 0.000 |
| land_fraction_ge_0.50 | 3,785 | 0.981 | 295 | 45 | 3,263 | 182 | 0.078 | 0.048 | 0.000 | 0.000 | 0.000 |
| protected_overlap_le_0.25 | 2,919 | 0.757 | 252 | 36 | 2,477 | 154 | 0.086 | 0.053 | 0.000 | 0.000 | 0.000 |
| land_ge_0.50_and_overlap_le_0.25 | 2,847 | 0.738 | 242 | 26 | 2,433 | 146 | 0.085 | 0.051 | 0.000 | 0.000 | 0.000 |

## Validation notes

- All scenario counts are nested within the primary retention/quadrant denominator.
- Quadrant counts sum to each scenario denominator.

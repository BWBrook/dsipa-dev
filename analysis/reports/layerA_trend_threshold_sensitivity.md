# Layer A trend-threshold sensitivity

Generated: 2026-05-25 03:57 UTC

Sensitivity grid for primary Layer A trend rules. Slopes use Theil-Sen on inside `mean` radiance and 1 km `land_unprotected` buffer `mean` radiance.

## Scenario summary

| min_valid_pixels | min_valid_years | inside_trend_n | inside_zero_slope_fraction | inside_positive_slope_n | inside_positive_slope_fraction | quadrant_n | q1_concurrent_brightening | q2_internal_brightening | q3_stable_non_detect | q4_external_pressure | q1_fraction | q4_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5.000 | 6.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 3858.000 | 305.000 | 55.000 | 3308.000 | 190.000 | 0.079 | 0.049 |
| 5.000 | 8.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 3858.000 | 305.000 | 55.000 | 3308.000 | 190.000 | 0.079 | 0.049 |
| 5.000 | 10.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 3858.000 | 305.000 | 55.000 | 3308.000 | 190.000 | 0.079 | 0.049 |
| 10.000 | 6.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 3858.000 | 305.000 | 55.000 | 3308.000 | 190.000 | 0.079 | 0.049 |
| 10.000 | 8.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 3858.000 | 305.000 | 55.000 | 3308.000 | 190.000 | 0.079 | 0.049 |
| 10.000 | 10.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 3858.000 | 305.000 | 55.000 | 3308.000 | 190.000 | 0.079 | 0.049 |
| 20.000 | 6.000 | 3371.000 | 0.888 | 353.000 | 0.105 | 2872.000 | 252.000 | 46.000 | 2434.000 | 140.000 | 0.088 | 0.049 |
| 20.000 | 8.000 | 3371.000 | 0.888 | 353.000 | 0.105 | 2872.000 | 252.000 | 46.000 | 2434.000 | 140.000 | 0.088 | 0.049 |
| 20.000 | 10.000 | 3371.000 | 0.888 | 353.000 | 0.105 | 2872.000 | 252.000 | 46.000 | 2434.000 | 140.000 | 0.088 | 0.049 |
| 50.000 | 6.000 | 2194.000 | 0.878 | 251.000 | 0.114 | 1767.000 | 168.000 | 35.000 | 1466.000 | 98.000 | 0.095 | 0.055 |
| 50.000 | 8.000 | 2194.000 | 0.878 | 251.000 | 0.114 | 1767.000 | 168.000 | 35.000 | 1466.000 | 98.000 | 0.095 | 0.055 |
| 50.000 | 10.000 | 2194.000 | 0.878 | 251.000 | 0.114 | 1767.000 | 168.000 | 35.000 | 1466.000 | 98.000 | 0.095 | 0.055 |

## Primary rule cross-check

Primary rule (`>=10` valid pixels, `>=8` valid years): inside trend n=4,426, zero-slope fraction=0.897, positive-slope n=420, quadrant n=3,858.

## Validation notes

- Quadrant counts sum to each scenario denominator.
- Quadrant denominators are nested within inside trend denominators.
- Inside zero + positive slope counts do not exceed inside trend denominators.

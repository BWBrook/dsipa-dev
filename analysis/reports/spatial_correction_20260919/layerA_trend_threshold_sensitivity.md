# Layer A trend-threshold sensitivity

Generated: 2026-09-19 05:52 UTC

Sensitivity grid for primary Layer A trend rules. Slopes use Theil-Sen on inside `mean` radiance and 1 km `land_unprotected` buffer `mean` radiance.

## Scenario summary

| min_valid_pixels | min_valid_years | inside_trend_n | inside_zero_slope_fraction | inside_positive_slope_n | inside_positive_slope_fraction | quadrant_n | q1_concurrent_brightening | q2_internal_brightening | q3_stable_non_detect | q4_external_pressure | q1_fraction | q4_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5.000 | 6.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 4253.000 | 347.000 | 70.000 | 3587.000 | 249.000 | 0.082 | 0.059 |
| 5.000 | 8.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 4253.000 | 347.000 | 70.000 | 3587.000 | 249.000 | 0.082 | 0.059 |
| 5.000 | 10.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 4253.000 | 347.000 | 70.000 | 3587.000 | 249.000 | 0.082 | 0.059 |
| 10.000 | 6.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 4253.000 | 347.000 | 70.000 | 3587.000 | 249.000 | 0.082 | 0.059 |
| 10.000 | 8.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 4253.000 | 347.000 | 70.000 | 3587.000 | 249.000 | 0.082 | 0.059 |
| 10.000 | 10.000 | 4426.000 | 0.897 | 420.000 | 0.095 | 4253.000 | 347.000 | 70.000 | 3587.000 | 249.000 | 0.082 | 0.059 |
| 20.000 | 6.000 | 3371.000 | 0.888 | 353.000 | 0.105 | 3188.000 | 289.000 | 60.000 | 2652.000 | 187.000 | 0.091 | 0.059 |
| 20.000 | 8.000 | 3371.000 | 0.888 | 353.000 | 0.105 | 3188.000 | 289.000 | 60.000 | 2652.000 | 187.000 | 0.091 | 0.059 |
| 20.000 | 10.000 | 3371.000 | 0.888 | 353.000 | 0.105 | 3188.000 | 289.000 | 60.000 | 2652.000 | 187.000 | 0.091 | 0.059 |
| 50.000 | 6.000 | 2194.000 | 0.878 | 251.000 | 0.114 | 2015.000 | 199.000 | 47.000 | 1635.000 | 134.000 | 0.099 | 0.067 |
| 50.000 | 8.000 | 2194.000 | 0.878 | 251.000 | 0.114 | 2015.000 | 199.000 | 47.000 | 1635.000 | 134.000 | 0.099 | 0.067 |
| 50.000 | 10.000 | 2194.000 | 0.878 | 251.000 | 0.114 | 2015.000 | 199.000 | 47.000 | 1635.000 | 134.000 | 0.099 | 0.067 |

## Primary rule cross-check

Primary rule (`>=10` valid pixels, `>=8` valid years): inside trend n=4,426, zero-slope fraction=0.897, positive-slope n=420, quadrant n=4,253.

## Validation notes

- Quadrant counts sum to each scenario denominator.
- Quadrant denominators are nested within inside trend denominators.
- Inside zero + positive slope counts do not exceed inside trend denominators.

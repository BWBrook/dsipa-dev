# Kosciuszko output-floor audit

Completed: 2026-10-19T14:35:54.832933+11:00

**Decision:** retain the high-value pixel table, but reject the proposed statement that masking cannot explain those values. The arithmetic is correct; that inference does not follow from it.

## Independent numerical replay

The cache's internal array hashes all pass. Common-valid, centre-selected inside support contains 39,721 cells: 642 increased, 30 decreased and 39,049 were unchanged. There are no endpoint-only valid inside cells. Direct sums replay the accepted annual mean multiplied by count within 1e-8: 1,220 in 2019 and 26,970 in 2024.

Let delta = decoded_2024 - decoded_2019. The denominator is **26,110**, the sum of strictly positive deltas across **642** cells. Negative deltas sum to -360 and net change is 25,750. The following thresholds refer to the **2024 value**, are nested, and include only cells with delta > 0. They are unweighted endpoint cell sums, not the manuscript's area-weighted OLS contributions.

| Minimum 2024 value | Brightened cells | Sum of positive differences | Share of all positive differences | Recorded zero in 2019 |
|---:|---:|---:|---:|---:|
| 10 | 642 | 26,110 | 100.0000% | 632 |
| 50 | 102 | 19,530 | 74.7989% | 102 |
| 100 | 64 | 16,910 | 64.7645% | 64 |
| 200 | 37 | 13,300 | 50.9383% | 37 |

All 64 cells at or above 100 were zero in the 2019 product. The median 2024 value among brightened cells is 10; 448 cells end at 10 and supply 4,480/26,110 = 17.16% of positive change. There are 184 positive differences larger than 10, supplying 21,530/26,110 = 82.46%. Maxima are 40 and 610 **inside the park**. The entire rectangular cache has a 2019 maximum of 120, so avoid describing 40 as the maximum of the entire window.

## What the calculation establishes

The increase is not confined to the smallest positive output value. An explanation restricted to one-bin endpoint changes cannot reproduce the 184 differences larger than 10. This is a conditional statement about bounded rounding error, not a general statement about the full product pipeline. The mere observation of a ten-unit lattice does not identify the exact upstream rounding rule or its complete history.

## Why it does not exclude masking

EOG describes background classification using 3 x 3 data range and cloud-free coverage. The original V2 method derives a per-cell threshold using multiyear information. Its output band is an average with background cells masked; the threshold statistic is not simply the final encoded cell average. See the [official EOG methods and band definitions](https://eogdata.mines.edu/products/vnl/) and [Elvidge et al. (2021)](https://doi.org/10.3390/rs13050922).

It follows that the smallest retained encoded value supplies no general upper bound on the threshold statistic or on an average discarded by the mask. A recorded zero can mean masking of a nonzero pre-mask value. The cached arrays do not retain that discarded value or the upstream mask diagnostics. The original method's attempt to keep thresholds constant across years is relevant evidence, but does not turn the output floor into such a bound or verify every transformation in the retained cross-version series.

## Explicit counterexample and discriminating test

Write Y = M Q(A), where A is a pre-mask average, Q is the encoding, and M is a binary retention mask. Let Q(A) be 610 for a target cell and 10 for an always-retained reference cell in both periods. Changing only the target mask from 0 to 1 produces [0, 10] -> [610, 10]: a 610-unit rise, the same ten-unit lattice, and the same smallest positive value. The script checks this exactly. A generic texture rule M = 1[D >= T], with fixed D = [1, 3] and T changing from 2 to 0.5, provides one implementation.

These arbitrary mask-statistic units are not calibrated product or physical radiance units. This toy is not the EOG algorithm, does not claim that EOG changed thresholds independently each year, and is not evidence that masking caused the park's rise. It refutes the categorical logical claim that masking cannot reveal a large value while the output floor stays fixed.

A discriminating test would compare the corresponding native pre-mask values and masks at the 64 high-value cells. Low pre-mask values in 2019 and high values in 2024 would reject the unchanged-input mask-only example; high 2019 values suppressed by its mask would support it. Consistent source identity and processing would be needed to test broader product effects. That extraction is outside this bounded audit and has not been run.

## Recommended manuscript wording

> The documented 2022 source change cannot by itself explain the rise already visible in 2021. The endpoint increase also extends well above the smallest positive encoded value: 64 of the 642 cells that brightened between 2019 and 2024 reached at least 100 product units, contributing 64.8% of summed positive pixel differences; the 2024 maximum within the park was 610. This establishes that the increase is not confined to the ten-unit output floor, but does not exclude masking or other processing effects.

Keep the table in Supporting Information if useful. Label its denominator explicitly. Do not replace the existing processing qualification with 'Nor can changes in masking or quantisation'.

## Reproducibility and scope

Run `uv run python analysis/reports/kosciuszko_floor_audit_20261019.py` from the repository root. The calculation imports no existing audit function and performs no network reads. JSON records input and reviewed-reference SHA-256 hashes, all verified array hashes, the cached source metadata, exact denominators, software versions and the executable counterexample. Primary methodology pages were consulted separately on 19 October 2026; direct article retrieval was rate limited, while publisher-indexed text and the EOG page were available.

- Cache SHA-256: `d76bd2dd874d111af9710be7269e2e0300db3b126e6ad140acdcefd71030cdc1`
- Script SHA-256: `d842a69b2d5d3da4bfa0d83304e104002d2e46f3fe1b818ab682a7ca8d8fc59e`
- JSON receipt SHA-256: `135f499c2c2f61096145b6789f649c195cc42b1e3e383958836679fde90ab423`
- No remote rasters, native EOG masks or unmasked averages were acquired. This is an offline replay and inference check, not satellite-product validation.

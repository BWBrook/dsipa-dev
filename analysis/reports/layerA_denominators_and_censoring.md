# Layer A denominators and censoring

Generated: 2026-05-25 03:06 UTC

Release reconciliation: 2026-07-24 from the independently accepted Goal 011
archive candidate and Goal 012 reference contract.

Primary settings:

- Baseline year: 2024
- Minimum valid pixels: 10
- Minimum valid years: 8
- Primary metric: `mean`
- Primary buffer type: `land_unprotected`

## Denominator table

| key | label | n | denominator_n | percent | selection_rule | notes |
| --- | --- | --- | --- | --- | --- | --- |
| pa_universe | Protected-area universe | 11,133 | 11,133 | 100.0% | Dissolved CAPAD PA_ID universe. | Base denominator for Layer A. |
| inside_2024_eligible | Inside baseline eligible (2024) | 4,426 | 11,133 | 39.8% | Inside PA, 2024, valid pixels >= 10. | Eligible for stable baseline inside radiance mapping. |
| inside_2024_ineligible | Inside baseline ineligible (2024) | 6,707 | 11,133 | 60.2% | Inside PA, 2024, valid pixels < 10. | Ineligible under the minimum-pixel rule, not necessarily missing source data. |
| inside_2024_zero_mean | Inside baseline zero mean (2024) | 3,844 | 4,426 | 86.9% | Eligible inside baseline rows with mean radiance == 0. | Primary baseline floor/censoring indicator. |
| inside_trend_eligible | Inside trend eligible | 4,426 | 11,133 | 39.8% | Primary metric=mean, buffer=land_unprotected, inside valid years >= 8. | Eligible for primary inside Theil-Sen trend estimates. |
| inside_trend_zero_slope | Inside trend exactly zero slope | 3,969 | 4,426 | 89.7% | Primary inside trend slope == 0. | Primary trend floor/censoring indicator. |
| inside_trend_positive_slope | Inside trend positive slope | 420 | 4,426 | 9.5% | Primary inside trend slope > 0. | Non-zero brightening subset for primary trends. |
| buffer1_2024_valid | 1 km unprotected-land buffer valid (2024) | 9,695 | 11,133 | 87.1% | Buffer 1 km, land_unprotected, 2024, valid pixels >= 10. | Baseline buffer availability for external-pressure context. |
| buffer1_trend_eligible | 1 km unprotected-land buffer trend eligible | 3,858 | 4,426 | 87.2% | Primary trend rows with non-missing 1 km buffer slope. | Buffer trend availability among inside-trend-eligible PAs. |
| buffer5_trend_eligible | 5 km unprotected-land buffer trend eligible | 3,992 | 4,426 | 90.2% | Primary trend rows with non-missing 5 km buffer slope. | Wider-buffer trend availability among inside-trend-eligible PAs. |
| buffer1_land_ge50 | 1 km buffer land fraction >= 0.5 | 10,221 | 11,133 | 91.8% | Buffer validity table, 1 km raw buffer land fraction >= 0.5. | Candidate stricter-valid-buffer sensitivity condition. |
| buffer1_overlap_le25 | 1 km buffer protected overlap <= 0.25 | 9,171 | 11,133 | 82.4% | Buffer validity table, 1 km protected-overlap fraction <= 0.25. | Candidate stricter-valid-buffer sensitivity condition. |
| retention_quadrant_eligible | Retention/quadrant eligible | 3,858 | 4,426 | 87.2% | Primary inside trend plus non-missing 1 km buffer trend and covariates. | Denominator for retention quadrant and category-safe risk rankings. |
| quadrant_q1_concurrent_brightening | Q1 concurrent inside and buffer brightening | 305 | 3,858 | 7.9% | Buffer slope > 0 and inside slope > 0. | Concurrent brightening subset. |
| quadrant_q2_internal_brightening | Q2 internal brightening with stable/non-detect buffer | 55 | 3,858 | 1.4% | Buffer slope <= 0 and inside slope > 0. | Internal brightening subset. |
| quadrant_q3_stable_or_non_detect | Q3 stable/non-detect inside and buffer | 3,308 | 3,858 | 85.7% | Buffer slope <= 0 and inside slope <= 0. | Stable or non-detect subset under primary thresholds. |
| quadrant_q4_external_pressure | Q4 external pressure without inside brightening | 190 | 3,858 | 4.9% | Buffer slope > 0 and inside slope <= 0. | External-pressure subset under primary thresholds. |
| ring0_2024_valid | Inside ring 0 valid (0-1 km) | 4,425 | 11,133 | 39.7% | Inside ring 0, 2024, valid pixels >= 10. | Ring feasibility denominator for edge/penetration analysis. |
| ring1_2024_valid | Inside ring 1 valid (1-5 km) | 1,432 | 11,133 | 12.9% | Inside ring 1, 2024, valid pixels >= 10. | Ring feasibility denominator for the conditional edge diagnostic. |
| ring2_2024_valid | Inside ring 2 valid (5-10 km) | 383 | 11,133 | 3.4% | Inside ring 2, 2024, valid pixels >= 10. | Ring feasibility denominator for edge/penetration analysis. |
| complete_rings_2024 | Complete ring set (2024) | 383 | 11,133 | 3.4% | All 3 inside rings have valid pixels >= 10 in 2024. | Conditional denominator for complete-ring edge profile summaries. |

## Validation notes

- PA universe is positive.
- Inside eligible + ineligible equals PA universe.
- Inside trend and retention denominators are nested correctly.
- All counts are <= their stated denominators.

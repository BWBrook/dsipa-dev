**Table 1. Feasibility, censoring, and denominators for the DSIPA Layer A audit.**

| label | n | denominator_n | percent | selection_rule | notes |
| --- | --- | --- | --- | --- | --- |
| Protected-area universe | 11,133 | 11,133 | 100.0% | Dissolved CAPAD PA_ID universe. | Base denominator for Layer A. |
| Inside baseline eligible (2024) | 4,426 | 11,133 | 39.8% | Inside PA, 2024, valid pixels >= 10. | Eligible for stable baseline inside radiance mapping. |
| Inside baseline ineligible (2024) | 6,707 | 11,133 | 60.2% | Inside PA, 2024, valid pixels < 10. | Ineligible under the minimum-pixel rule, not necessarily missing source data. |
| Inside baseline zero mean (2024) | 3,844 | 4,426 | 86.9% | Eligible inside baseline rows with mean radiance == 0. | Primary baseline floor/censoring indicator. |
| Inside trend eligible | 4,426 | 11,133 | 39.8% | Primary metric=mean, buffer=land_unprotected, inside valid years >= 8. | Eligible for primary inside Theil-Sen trend estimates. |
| Inside trend exactly zero slope | 3,969 | 4,426 | 89.7% | Primary inside trend slope == 0. | Primary trend floor/censoring indicator. |
| Inside trend positive slope | 420 | 4,426 | 9.5% | Primary inside trend slope > 0. | Non-zero brightening subset for primary trends. |
| Retention/quadrant eligible | 3,858 | 4,426 | 87.2% | Primary inside trend plus non-missing 1 km buffer trend and covariates. | Denominator for retention quadrant and category-safe risk rankings. |
| Q1 concurrent inside and buffer brightening | 305 | 3,858 | 7.9% | Buffer slope > 0 and inside slope > 0. | Concurrent brightening subset. |
| Q2 internal brightening with stable/non-detect buffer | 55 | 3,858 | 1.4% | Buffer slope <= 0 and inside slope > 0. | Internal brightening subset. |
| Q3 stable/non-detect inside and buffer | 3,308 | 3,858 | 85.7% | Buffer slope <= 0 and inside slope <= 0. | Stable or non-detect subset under primary thresholds. |
| Q4 external pressure without inside brightening | 190 | 3,858 | 4.9% | Buffer slope > 0 and inside slope <= 0. | External-pressure subset under primary thresholds. |
| Inside ring 0 valid (0-1 km) | 4,425 | 11,133 | 39.7% | Inside ring 0, 2024, valid pixels >= 10. | Ring feasibility denominator for edge/penetration analysis. |
| Inside ring 1 valid (1-5 km) | 1,427 | 11,133 | 12.8% | Inside ring 1, 2024, valid pixels >= 10. | Ring feasibility denominator for edge/penetration analysis. |
| Inside ring 2 valid (5-10 km) | 383 | 11,133 | 3.4% | Inside ring 2, 2024, valid pixels >= 10. | Ring feasibility denominator for edge/penetration analysis. |
| Complete ring set (2024) | 383 | 11,133 | 3.4% | All 3 inside rings have valid pixels >= 10 in 2024. | Conditional denominator for complete-ring edge profile summaries. |

Counts use the `v0.3.0` processed Layer A evidence. Percentages are relative to the stated denominator, so rows intentionally mix PA-universe, trend-eligible, retention-eligible, and ring-complete denominators.

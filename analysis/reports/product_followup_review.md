# Post-review product and spatial-support follow-up — 18 September 2026

This exploratory follow-up responds to Fable correspondence messages 207–208,
after inspection of the September 17 results. It does not amend the frozen
September 17 protocol retrospectively or replace accepted national outputs.

## Calendar patterns and persistence

The absence of a spike in 2022 does not resolve product continuity. All three
complete-series zone cohorts show synchronous rises in first-positive fractions
in 2017 and 2023. In the inside cohort, 2024 remains slightly above 2023; calling
2023 a pulse denotes its rise relative to earlier years, not a local maximum in
every series. Similarly, 2022 is not a strict local minimum inside: 14/3,864
versus 13/3,877 in 2021. Buffer fractions and common-support pixel transitions
show a clearer 2022 dip and 2023 rebound. Zero-to-positive transitions rise from
28,035 to 57,328, while positive-to-zero transitions fall from 21,520 to 12,031.
A processing explanation involving the mixed-sensor 2022 composite is plausible
but unidentified; regional environmental or observational changes remain possible.

`audit_pulse_followup.py` reproduces the 64/78 first detections in 2023–2024 and
writes onset-year persistence for all three cohorts. Next-year positive fractions
are 67.9–69.9% for 2017 first detections, 64.5–70.6% for 2023 and 71.4–84.0% for
2022. These do not identify a processing or environmental cause. The 2024 onset
cohort has no following year and is left missing, not assigned zero persistence.
No independent trials, causal tests or multiplicity-adjusted pulse tests are
claimed. The new S8 uses separate zero-based distance panels with explicit scales.

## Interpretation and verification boundaries

Individual-pixel minimum positive values must be distinguished from zonal means,
which can fall below that minimum. A zero Sen slope must be distinguished from
an all-zero annual series. Coding, upstream masking and source measurement cannot
be assigned separate shares of the observed zero mass with these data. No physical
unit conversion is made without a reproducible source-to-derivative mapping.

The floor scan now confirms a minimum positive decoded value of 10 in every
2013–2024 audit window. Five higher-valued off-lattice pixels (one in 2013, four
in 2019) do not affect this conclusion. See `product_floor_followup.md` and
its hashed inputs/outputs. The same-cohort 0–1 km extension is recorded in
`edge_followup/`, with a separate reproducibility manifest. No Black Marble or EOG data acquisition is required
for the product-descriptive interpretation retained here. Stronger environmental
attribution would require independent evidence.

## Matched bands and area magnitude

The fixed cohort contains 1,205 reserves with 12 valid years in each inward
band. Of 119 positive whole-reserve slopes, 109 remain positive at 0–1 km and
32 at 1–5 km; 79 are positive only in the outer band (the deeper slope is zero).
This supports outer-ring concentration of the measured trend within this selected
cohort, but is not independent corroboration because the outer ring contributes
to the whole-reserve mean. Source location and optical spillover remain unidentified.

Fable's Q1-loss numbers reproduce: 68 zero band slopes, median polygon area
112.6 km², median whole-reserve slope 0.0132 versus 0.1473 for the 23 Q1 retainers.
However, only 54 of the 68 have all-zero deeper-band histories. Fourteen have
positive annual observations with a zero median pairwise slope. The Q2 losses
number 19: 18 zero slopes and one negative, with 17 all-zero histories. The phrase
‘the loss is floor censoring’ is therefore too categorical.

The 420 positive whole-reserve slopes divide into 140 per tercile (no boundary
ties). The lowest tercile contributes 99.147% of positive-class summed polygon
area. The 68 Q1 losses alone contribute 8.947% of that area; they do not carry
the national area result on their own. The 37.6% eligible-area share is a
whole-polygon sign classification dominated by very small reserve-mean slopes,
not the area illuminated, changing or experiencing substantial change.

Independent review reproduced the cohort/sign counts and area joins. It caught
a transient source/output mismatch during script finalisation; the final run
and matching local/remote source SHA-256 are now recorded in the edge manifest. Supporting Table S5 is generated
from the preserved result tables, not manually entered summaries.

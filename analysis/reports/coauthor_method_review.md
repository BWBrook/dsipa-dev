# Scientific review of the RSEC co-author revision

Date: 2026-09-12. Independent methods review accepted the corrected interpretation
and the revised central claims after small textual/citation repairs.

## Accepted interpretation

The protected-area unit, annual source layers, pixel/year eligibility, Sen
estimator and primary category counts remain unchanged. The secondary evidence
is interpreted according to the implemented algorithm: each area has marginal
temporal pairs/block resampling percentiles, not spatial confidence intervals.
No formal category confidence or joint ordering follows from these marginals.
The former dominance matrix is excluded from the active manuscript.

The zero-slope diagnostic checks the observed annual series, with complete-year
requirements for the late-positive pattern. Its exact partition is 3,786 all
zero + 3 constant non-zero + 180 varying = 3,969; 78 varying series satisfy the
late-positive definition. All 3,969 have 12 valid years. Missing values are
preserved rather than reinterpreted as zero. Four input hashes and the primary
counts are checked by `analysis/coauthor_evidence.py`.

The four displayed reserves are illustrative selections, not a statistical
sample. Henderson's buffer endpoint increase (53 to 75) coexists with a decline
and recovery and a Sen slope of -0.0625. Black Mountain explicitly demonstrates
that Q3 contains negative slopes. Source attribution and biological response
are not inferred from these trajectories.

## Repairs accepted during review

- The abstract specifies at least one positive annual mean in 2022-2024.
- Temporal-increase studies are distinguished from Garrett's skyglow evidence.
- Presence-only bias citations accompany that limitation; repeated standardised
  surveys are presented as a recommendation.
- Selected high-magnitude values are not described as high conservation value.
- The Hengl/OpenGeoHub v0.4 derivative is cited alongside Elvidge's source
  methodology. Values remain in metadata-adjusted scaled product units.

## Reproduction boundary

The descriptive calculation and figure rendering use the preserved Goal 012
outputs on deep-server under tmux. No raster extraction, national trend refit,
new uncertainty simulation, biodiversity model run or public deposit is required.
Historical schemas, payloads and prior interpretation records remain available
for provenance. The present manuscript and this review supersede older claims
of spatially calibrated uncertainty and absence of change from zero Sen slopes.

# 133 - RSEC manuscript consolidation

Date: 2026-07-24

Goal 013 consolidated the accepted DSIPA evidence into an Original Research
manuscript targeted to *Remote Sensing in Ecology and Conservation*.

## Scientific outcome

- Exact title adopted:
  **Detectable change in dark-sky integrity across Australia’s protected
  areas**.
- Layer A is the primary contribution: a detectability-aware assessment of
  inside and surrounding unprotected-land radiance change.
- Eligibility remains explicit: 4,426 of 11,133 protected areas support the
  primary inside result.
- Management output is categorical screening, not numerical priority ranking.
- Interior-band inference is conditional on spatial support.
- Current manuscript surfaces use the accepted ring-1 evidence:
  1,432/11,133 (12.9%).
- Layer B is a compact test of microbat-versus-passerine occurrence-record
  discrimination. Its weak out-of-block performance and uncontrolled
  taxon-specific observation processes prevent biological-response inference.
- ALAN shuffles are interpreted as null benchmarks; attenuation after shuffling
  does not identify the source of the original association.

## Manuscript and validation outcome

- Abstract: 235 words.
- IMRAD main text: 4,609 words.
- IMRAD plus Data accessibility: 4,683 words.
- Keywords: 5.
- Main displays: 4 figures and 1 table.
- Supporting displays: 7 figures and 2 tables.
- `git diff --check`: passed.
- `make ms-check`: passed, including 61 tests, manuscript lint, reference
  audit with zero unknown keys, author metadata checks, and build check.
- `make ms-build`: passed.
- Built PDF and DOCX were inspected; one focused scientific repair was applied
  and the affected checks/build were repeated successfully.

## Boundaries and residuals

No new analysis, data processing, modelling, figure generation, code/test
change, citation addition, release-manifest repair, archive/DOI action,
packaging, submission, commit, or push occurred.

Two production-provenance issues remain for a later release goal:

1. pre-Goal-012 local Layer A report copies still carry historical
   1,427/12.8% text even though the accepted Goal 012 reference contract and
   manuscript use 1,432/12.9%; and
2. the Makedoc build manifest records the Makedoc checkout Git SHA rather than
   the DSIPA action-repo SHA.

These do not alter Goal 013 manuscript claims, but they must be resolved or
explicitly handled before final archive/submission packaging.

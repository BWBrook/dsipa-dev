# 144 — Spatial review correction (19 September 2026)

Barry authorised the parent's recommended remedies after the fresh independent
Astra/max review. Scope: correct spatial supports and coastal land masking;
quantify national impacts; regenerate affected results and manuscript; fix and
audit Layer B sampling; prepare a coherent private reproducibility candidate.
Accepted Goal 012 inputs and previous reading/evidence bundles remain immutable.
Public release, submission, commit and push are outside this authorisation.

## Initial work

- Parent owns spatial engine, correction protocol and integration.
- Independent source-selection agent evaluates coastline resolution, coverage,
  dates and licensing, with particular attention to external islands.
- Layer B agent fixes invalid raw sampling and measures its effect before refits.
- Read-only reconciliation agent compares public and accepted input semantics.
- Heavy computation uses isolated deep-server scratch and persistent tmux jobs.

No corrected national result has yet been obtained or interpreted.

## Preflight and extraction

- Replaced simplified, one-segment geometry with unsimplified repaired CAPAD and
  q128 arcs. Five geometry/error regressions initially passed; an additional
  nested-polygon collection regression was then added.
- 73-reserve, 365-support q128/q256 pilot: three one-cell 5 km raw-buffer
  differences; no tested inward-band or 1 km difference and no eligibility/sign
  change. Twelve raster grids are identical. Detailed protocol is prospective
  relative to national corrected results.
- AIMS Coast50K2024 v1-1 Split source selected and validated. Eight named local
  unions match Full exactly; six non-Antarctic zero-overlap IDs excluded only
  from land-dependent surrounding comparisons. Explicit hashes/screens preserved.
- First national attempt (`national/`) correctly raised an extraction error for
  Wilinggin: a GeometryCollection reached Rasterio's transformed window path.
  Error had been hidden by the old blanket exception handler. Polygonal
  normalization preserves area while removing zero-area overlay remnants and
  reconstructing Polygon/MultiPolygon containers. The partial attempt is kept
  but contributes no accepted corrected result.
- Full clean restart: deep-server tmux `dsipa-spatial-national-v2-20260919`,
  output `/data/codex/scratch/dsipa-spatial-correction-20260919/national_v2`,
  20 workers. Code snapshot and input/run contracts retained. No raster masking
  exception can silently become ineligibility.
- Pilot Henderson surrounding slope becomes positive with the corrected land
  source. Its old Q2 narrative must be revised, retaining the case transparently.

## Parallel follow-ups

Layer B sampler repaired and tested; methods clarified for species-level
cell/date deduplication, L2 penalty and arithmetic fold metrics. Original ALA
rows have not been located. A domain-wide raster scan narrows possible invalid
samples to ten cells in Western Australia (2013, 2019, 2021), with none in
2022–2024; actual record hits remain unknown. Barry was asked about backups and,
if unavailable, preference between removing optional numerical Layer B results
(recommended) and fresh acquisition/refit. Core spatial work continues.

Manifest-validated audit orchestration and dynamic figure/table cohort handling
are implemented. Numerical regeneration, manuscript completion, private release
packaging and final independent acceptance review remain pending extraction.

## Candidate scope and public-input route

The optional Layer B numerical section is omitted from the active candidate,
using Barry's existing discretion over its extent and the stated recommendation
after the unanswered backup/preference request. This is a submission-scope
choice, not a claim that its old coefficients are demonstrably wrong. Historical
results, code, review notes and previous bundles are retained. Active SI now has
three methods sections, five tables and three figures.

All nine public processed baseline payloads passed pinned identities. Complete
annual/edge keyed equality and all geometry attributes/topology were checked;
a parent probe additionally found zero per-key raw WKB differences after loading
the accepted and public GPKGs. The historical land cache was rebuilt from its
pinned public archive with identical SHA-256. An eight-reserve corrected public
input pilot includes Henderson, Torndirrup, Lord Howe, Grey Peaks and Wilinggin.

## Corrected spatial results — 19 September 2026

The completed clean national v2 extraction covers all 11,133 reserves. Whole
observations/slopes are exactly unchanged. Corrected paired coverage is 4,253
(Q1 347; Q2 70; Q3 3,587; Q4 249). Geometry and coastline effects are separated
in spatial_correction_summary.json. The matched deeper-band cohort changes
from 1,205 to 1,341; among common paired eligible reserves no interior slope
sign changes. The change is principally eligibility/support selection, not a
reversal of common-reserve trends. Whole-positive/deeper-positive counts are
150/42. Henderson changes from historical Q2 to Q1 and remains a transparent
example of spatial-support sensitivity.

AIMS 50K is a substantial improvement but not local ground truth. Nineteen
reserves overlap a proximity screen around source-listed exceptions; nine
are paired comparisons and explicitly provisional in reserve_screening_results.csv.
Excluding those nine gives 4,244 paired, Q1=341, Q2=70, Q3=3,585, Q4=248.
Swan River and Brisbane Water are newly eligible Q1 cases near these exceptions.
Maps do not delimit actual mapping error; local validation remains necessary.

The observed pixel floor and 2017/2023 synchrony remain material limitations.
Corrected spatial screening does not identify biological effects or establish
encroachment causally. The upper two positive-slope terciles still cover 0.32%
of eligible summed polygon area; their empirical cutoff is not ecological.

Optional numerical Layer B is omitted from the active candidate because the
original occurrence downloads are unavailable for verifying a nodata-sampling
repair. This uses the authorised discretion over this secondary section and
preserves historical outputs; it is not evidence that old coefficients are wrong.

## Final candidate verification

Independent acceptance checks verified all 928 national chunks and 4,640 part
hashes, 133,596 unchanged whole-reserve annual rows, all 4,253 paired SciPy
Theil–Sen recalculations (maximum difference 1.42e-14), and the original-versus-
amended validity fields. Full repository tests pass: 154. Wheel and sdist build.
A clean curated directory reproduces all 20 audit CSVs byte-for-byte, the table
source, all five main/forest figures and the product-audit figure. The edge
renderer had joined an already relative path twice, leaving the old 383-reserve
asset canonical; the corrected 369-reserve output is now canonical and the
renderer path is fixed. Its reproduced bytes are identical after the correction.

The Git-free archive exposed a manuscript wrapper/provenance assumption.
Archives now use their FILE_MANIFEST identity and verify all listed file hashes;
normal repository builds retain Git provenance. No commit identity is invented.
The archive's submission check passes. Final SI QA caught a split dagger note;
its placement is being corrected before the final bundle is sealed.

## Tranche completed

Independent acceptance verdict: APPROVE the corrected private candidate; no
open scientific, numerical or artefact blocker. Main/SI PDFs have 21/14 pages;
Word conversions have 27/17 pages after a targeted Table 1 note-spacing repair.
All four surfaces passed structural/visual QA. Both profiles build from the
253-file Git-free curated package and yield identical PDF layout text. The
package has 38 focused passing tests; the full repository has 154 passing tests.
Twenty audit CSVs and all seven active figures reproduce exactly. Current
reading bundle: build/final_read/spatial_20260919/; complete private source and
evidence: artefacts/spatial_candidate_20260919/. ZIP identities are recorded in
analysis/reports/spatial_candidate_seal_20260919.json. Previous baselines and
bundles remain preserved. No commit, push, public deposit or submission made.
Barry's full edit, declarations and eventual release decisions remain next.

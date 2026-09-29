# RSEC co-author revision, 2026-09-12

Status: completed for private co-author review. Barry authorised all five orientation priorities and
confirmed Remote Sensing in Ecology and Conservation as the target.

## Scope and decisions

- Lead with remote sensing for conservation: eligibility, annual radiance,
  full-window trend screening, and named reserve examples.
- Preserve accepted primary inputs, annual summaries, slopes and sign counts.
  Distinguish zero Sen slopes from unchanging observed series, and non-positive
  slopes from stable conditions.
- Assess the existing per-reserve bootstrap as marginal temporal sensitivity;
  remove claims of shared spatial uncertainty and matched-replicate dominance.
  Obtain independent scientific review before accepting this interpretation.
- Compress the biodiversity comparison in the main text and move detailed
  methods/results and its coefficient figure to Supporting Information.
- Rebuild figures from preserved evidence, repair map/quadrant communication,
  and add named annual trajectories with explicit illustrative selection.
- Build and visually inspect editable main/SI reading files with local makedoc.

No public release, submission, author-metadata invention, or routine national
rerun is included. Any remote computation uses deep-server and tmux; source
and accepted data are preserved. Parent owns manuscript/build/docs integration;
bounded agents review methods and implement specified figure changes.

## Validation and outcome

All five priorities are implemented. The primary data identities, slopes and
sign counts are preserved. Independently reviewed interpretation now distinguishes
zero slopes from unchanging series and marginal temporal sensitivity from
calibrated or joint uncertainty. The new descriptive diagnostic confirms 180
varying zero-slope series, including 78 with the specified late-positive pattern.
The main fourth figure shows Neerabup, Henderson, Black Mountain and Bungonia;
Layer B details and the association figure are in SI. The dominance figure is
excluded from the active manuscript. Twenty-four cited records were checked and
inherited bibliographic errors corrected.

Descriptive checks and six figure renders completed in tmux on deep-server,
using an isolated source checkout and preserved accepted data. Final image/source
hashes match the remote render manifest. No national extraction, trend refit,
new bootstrap simulation or biological model fit was required.

Verification: 111 Python tests passed, seven large-input local tests skipped;
sdist and wheel built; both makedoc profile checks and fresh builds passed.
All embedded image hashes and document output hashes were reconciled. The local
wrapper now forces fresh builds, avoiding stale embedded images. A4 Word page
geometry, compact editable tables, coherent SI caption placement and page-break
normalization were added reproducibly without modifying shared makedoc source.

Visual review covered both complete PDFs and LibreOffice-rendered DOCX files,
then rechecked affected pages after pagination fixes. Main PDF: 19 pages;
main Word rendering: 25. SI PDF: 14; SI Word rendering: 16. No clipping,
orphan caption page or empty break-only page remains. LibreOffice emitted an
`Unknown IO error` while producing valid QA PDFs; Microsoft Word rendering was
not tested. Conservative source count: 3,297 words, including the 224-word abstract.

Private bundle: `build/final_read/coauthor_20260912/`; portable ZIP:
`build/final_read/dsipa_rsec_coauthor_20260912.zip`. It contains main/SI PDF and
DOCX, the reading guide and companion data. Canonical provenance and source
snapshot: `artefacts/rsec_coauthor_20260912/`. Detailed check record:
`analysis/reports/coauthor_validation.md`.

Author/declaration fields and pre-submission decisions remain visible for Barry
and co-authors. Nothing was submitted, deposited, messaged, committed or pushed.

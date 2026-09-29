# RSEC co-author revision validation, 12 September 2026

## Scientific evidence

- Preserved accepted Goal 012 annual radiance, geometry, trend and paired-risk
  input hashes. The descriptive diagnostic fails closed if these identities or
  the primary count invariants change.
- Confirmed 4,426 inside-eligible areas, 3,969 zero inside slopes and the paired
  sign counts 305 / 55 / 3,308 / 190 (3,858 total).
- Among all 3,969 zero-slope series, confirmed 12 valid years each: 3,786 all
  zero, three constant positive, 180 varying. The explicitly defined late-positive
  subset has 78 members. Missing values remain missing.
- Checked all 96 zone-year values for four named examples and the stated
  full-period slopes. Examples are illustrative, not representative selections.
- Reconciled all 60 Table S1 rows against accepted risk/resampling outputs at
  full precision (tolerance 1e-12 before display rounding). Table S2 values and
  Figure S3 coefficients/AUCs agree with the preserved model report.
- Independent methods review accepted the marginal temporal-resampling
  interpretation and the resulting claim limits. See `coauthor_method_review.md`.
- Checked the 24 cited records (22 journal articles and two datasets) against
  DOI metadata; repaired inherited title, author, year and DOI errors. See
  `coauthor_reference_audit.md` and `coauthor_reference_metadata.json`.

## Execution and provenance

Descriptive checks and revised figure rendering ran on deep-server in persistent
`tmux` sessions. The accepted data checkout was preserved; rendering used an
isolated source checkout. The six final figure hashes and four rendering-source
hashes reconcile to `render_manifest.json`, which records all input hashes and
actual software versions. A final title-only trajectory render used the same
inputs and refreshed that manifest. No raster extraction, national trend refit,
new bootstrap simulation or biological model fit was performed.

The private artefact folder is `artefacts/rsec_coauthor_20260912/`, containing
source snapshot/hashes, remote and local manifests, evidence, package builds,
figures, reading files and check logs. The portable private reading ZIP is
`build/final_read/dsipa_rsec_coauthor_20260912.zip`.

## Final build and visual checks

- `uv run python -m pytest -rs`: 111 passed, seven skipped because large
  national inputs are absent locally. This is not a new full national replay.
- `uv build`: Python sdist and wheel produced successfully.
- Main and SI `make ms-check` and `make ms-build`: passed, run sequentially.
  Builds force fresh source/image rendering because upstream incremental
  dependencies did not detect embedded-image replacements.
- All four main and seven SI embedded DOCX image hashes match their final PNG
  sources. Both PDF/DOCX output hashes match their build manifests after local
  Word normalization.
- The main PDF has 19 A4 pages; SI has 14. SI Word renders to 16 A4 pages in
  LibreOffice; main Word renders to 25 A4 pages, with no blank pages.
- Full visual review covered text, tables, references, captions and figures in
  both native PDFs and LibreOffice-rendered DOCX files. Subsequent pagination
  repairs were checked on the affected pages. Tables retain repeat headers,
  single-spaced cells and unsplit rows; body text remains double-spaced. SI
  captions accompany their figures, and empty Word page-break pages are removed.
- LibreOffice reported `Unknown IO error` while producing valid PDFs for QA.
  Rendered files and DOCX ZIP contents were inspected successfully; this check
  uses LibreOffice rather than Microsoft Word's rendering engine.
- Conservative manuscript count: 3,297 source words including abstract, complete
  body, headings and current declarations; abstract alone 224. Main has four
  figures and one table; SI seven figures and two tables.

## Scope remaining for people

This is a private co-author version. Author identity/order, affiliations,
contributions, acknowledgements, conflict/ethics/AI wording, public-code route
and final all-author approval remain explicit human fields or decisions.
No public archive, preprint deposit, journal submission, collaborator message,
commit or push was made during this revision. Journal production exports remain
a later task after scientific/editorial comments.

# Stage 4B Closeout: Release and data availability readiness

Status: complete, pending DSIPA orchestrator review.

Date: 2026-06-23

## Repo state recorded

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch at start: `main`
- HEAD at start: `530e843`
- Starting status: `## main...origin/main` plus the untracked Goal 007 packet.
- Repo-local `AGENTS.md`: present and read.
- Packet read: `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md` under
  `docs/goals/007-stage4B-release-data-availability-readiness/`.

## Work completed

- Created `analysis/reports/final_release_manifest.md` as the Stage 4B release
  decision surface.
- Updated `data/README.md` to remove the stale implication that large derived
  outputs have already been archived, to point to the Stage 4B manifest, and to
  document the verified current/evidence checksum semantics for the Layer B
  licence ledger.
- Updated `README.md` to say large outputs are classified for release readiness
  and that archive upload/DOI minting remain pending.
- Updated only the manuscript Data and code availability section to reference
  the Stage 4B manifest and to keep raw and row-level ALA occurrence tables out
  of the manuscript package by default.
- Added DEC-039 for the Stage 4B release/data policy.
- Updated critique-matrix rows B01, B11, R02, R05, and R09.
- Updated `docs/stage_overview.md` to mark Stage 4B readiness as prepared and
  keep Stage 4C unstarted.
- Created `docs/log/127_stage4B_release_data_availability.md`.

## Manifest classifications

- `tracked`: source docs, manuscript source, manuscript figures, small reports,
  smoke-test fixtures, and derived Layer B summaries/ledger tables.
- `archived-proposed`: large paper-critical Layer A national outputs and
  support files, including `pa_radiance_buffers_national_v0_3_0.csv`,
  `pa_edge_profiles_national_v0_3_0.csv`, `pa_buffer_validity_v0_3_0.csv`,
  `pa_trends_v0_3_0.csv`, `pa_risk_rankings_v0_3_0.csv`, PA geometry outputs,
  IBRA assignments, and bootstrap summaries.
- `restricted`: raw ALA downloads and row-level processed Layer B occurrence
  tables.
- `excluded`: deferred Squamata control and `docs/ref_doi.txt` as a DOI
  authority.
- `regenerated`: build outputs, `artefacts/`, state-run folders, and manuscript
  build products.

## Matrix status changes

- B01: `release-gate` to `done` for mixed-licence release-surface handling.
- B11: `release-gate` to `done` for raw/row-level ALA redistribution policy.
- R09: `open` to `done` after recording that the current checkout byte
  SHA-256 matches the evidence reconciliation SHA-256 after CRLF-to-LF
  normalization.
- R02: remains `release-gate`; the manifest classifies archive-proposed files,
  but no external archive or DOI exists.
- R05: remains `release-gate`; large ignored files are classified, but final
  archive scope and publication are Stage 4C decisions.
- R04 and R08 were not changed because Goal 007 did not address the uv warning
  or the broader per-stage validation doctrine beyond this closeout.

## Decisions still required

- Barry/orchestrator must decide final archive scope for `archived-proposed`
  files.
- Barry/orchestrator must choose the external archive record and authorize DOI
  minting before publication wording cites a final DOI.
- Any exception that would redistribute raw ALA downloads or row-level processed
  ALA occurrence tables needs explicit later approval and a recorded permission
  basis.
- Stage 4C should refresh evidence reconciliation/audit on the final clean
  release state.

## Validation

Commands run:

- `git status --short --branch`: completed; showed the expected Goal 007 edit
  footprint only, with the Goal 007 packet still untracked.
- `git diff --check`: passed.
- `test -f analysis/reports/final_release_manifest.md`
  `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
  `docs/log/127_stage4B_release_data_availability.md`: passed.
- `make ms-check`: passed because the manuscript Data and code availability
  section changed. The check reported tool/config validation passed, 61 tests
  OK, manuscript lint passed, reference audit passed with 4 non-fatal unused
  bibliography keys, author metadata checks passed, and build check passed.
- Release/archive scan over `data/README.md`, `README.md`,
  `manuscript/text/manuscript_draft.md`, `docs/decisions.md`,
  `docs/stage1_critique_resolution_matrix.md`, and
  `analysis/reports/final_release_manifest.md`: reviewed. Remaining Zenodo
  hits are source-record/helper references or superseded historical decisions;
  no current wording says the DSIPA external archive/DOI has already been
  published.
- ALA licence/redistribution scan: reviewed. Raw ALA and row-level processed
  occurrence data are restricted/excluded by default; derived Layer B summaries
  remain the manuscript-facing surface.
- Checksum convention scan: reviewed. `data/README.md`,
  `analysis/reports/evidence_reconciliation.md`, and
  `analysis/reports/final_release_manifest.md` now state that the Layer B
  licence ledger current checkout byte SHA-256 matches the evidence
  reconciliation SHA-256 after CRLF-to-LF normalization.

## Review iteration: licence-ledger checksum correction

Reviewer evidence showed that the previous Goal 007 wording incorrectly
preserved an older conflicting value as the current raw byte identity for
`data/processed/layerB_ala_license_ledger_v0_3_0.csv`. The current checkout
byte SHA-256 is
`a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`, and the
CRLF-normalized SHA-256 is the same. The evidence reconciliation JSON records
that same value for both `sha256` and `expected_sha256`, with
`normalize_crlf: true`.

Revised files:

- `data/README.md`
- `analysis/reports/final_release_manifest.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
- `docs/log/127_stage4B_release_data_availability.md`

Iteration validation:

- `shasum -a 256 data/processed/layerB_ala_license_ledger_v0_3_0.csv`: current
  checkout byte hash is
  `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`.
- `perl -0777 -pe 's/\r\n/\n/g' data/processed/layerB_ala_license_ledger_v0_3_0.csv | shasum -a 256`:
  normalized hash is
  `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`.
- `jq -r '.files[] | select(.path|test("layerB_ala_license_ledger"))' analysis/reports/evidence_reconciliation.json`:
  `sha256` and `expected_sha256` are both
  `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`, with
  `normalize_crlf: true`.
- `file data/processed/layerB_ala_license_ledger_v0_3_0.csv`: CSV text.
- CR scan: no CR line ending was found in the current checkout file.
- `git diff --check`: passed.
- Goal 007 file-presence checks: passed.
- `rg` scan: the older conflicting checksum prefix no longer appears in the
  release-facing Goal 007 surfaces; `a751d630` remains documented in `data/README.md`,
  `analysis/reports/final_release_manifest.md`, the closeout, and the evidence
  reconciliation report.
- `make ms-check` was not rerun in this review iteration because the manuscript
  was unchanged after the previous pass.
- Core filename/checksum scan: reviewed. Layer A national files, raw ALA zips,
  and row-level processed Layer B occurrence tables are present in the manifest
  with classifications and checksums matching the evidence reconciliation.
- Classification vocabulary scan: reviewed. `tracked`, `archived-proposed`,
  `regenerated`, `excluded`, `restricted`, and Barry/orchestrator decision
  language are present in the manifest.

No full pytest, package build, release packaging, data pipeline, ALA download,
remote compute, archive upload, DOI tooling, commit, push, merge, or PR command
was run.

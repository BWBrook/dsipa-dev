# 127 Stage 4B release/data availability readiness

Date: 2026-06-23

Goal: Execute Goal 007 as a planning/readiness-only release and data
availability pass. This log records the repo-local state, release-surface
classification, and validation evidence without running data processing,
archive upload, DOI minting, release packaging, remote compute, or manuscript
builds beyond the authorized manuscript check.

## Starting state

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch/status at start: `## main...origin/main` with the untracked Goal 007
  packet.
- HEAD at start: `530e843`
- Packet read: `docs/goals/007-stage4B-release-data-availability-readiness/Goal.md`,
  `Plan.md`, `Runbook.md`, and `Log.md`.
- Repo-local `AGENTS.md` was present and read.

## Scope respected

- No data processing, ALA downloads, model runs, remote compute, release
  packaging, archive tooling, DOI tooling, commits, pushes, or PR work.
- No generated science artefacts or existing evidence reconciliation reports
  were modified.
- Manuscript edits were limited to `## 6. Data and code availability`.

## Outputs

- Created `analysis/reports/final_release_manifest.md`.
- Updated `data/README.md`, `README.md`, and the manuscript data/code
  availability wording to state that archive upload and DOI minting remain
  pending.
- Added DEC-039 to `docs/decisions.md`.
- Updated matrix rows B01, B11, R02, R05, and R09.
- Updated `docs/stage_overview.md` to reflect Stage 4B readiness and the
  unstarted Stage 4C boundary.

## Classification summary

- `tracked`: repository docs, manuscript source, manuscript figures, small
  evidence reports, smoke-test fixtures, and derived Layer B summary/ledger
  tables.
- `archived-proposed`: large paper-critical Layer A national tables and
  geometry/uncertainty support files.
- `restricted`: raw ALA downloads and row-level processed Layer B occurrence
  tables.
- `excluded`: deferred Squamata control and `docs/ref_doi.txt` as a DOI
  authority.
- `regenerated`: build outputs, `artefacts/`, state-run folders, and manuscript
  build products.

Validation evidence is recorded in the Goal 007 closeout memo.

## Review iteration: licence-ledger checksum correction

- Corrected the Stage 4B release-facing checksum wording for
  `data/processed/layerB_ala_license_ledger_v0_3_0.csv`.
- The current checkout byte SHA-256 is
  `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`.
- CRLF-to-LF normalization yields the same SHA-256, matching
  `analysis/reports/evidence_reconciliation.json` where `normalize_crlf` is
  `true`.
- Removed the previous unsubstantiated current/raw-byte wording from
  `data/README.md` and `analysis/reports/final_release_manifest.md`.
- `make ms-check` was not rerun for this iteration because the manuscript was
  unchanged after the previous pass.

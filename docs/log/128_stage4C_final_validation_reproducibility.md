# Stage 4C final validation and reproducibility audit

Date: 2026-06-23
Agent: `nightlight`
Goal packet:
`docs/goals/008-stage4C-final-validation-reproducibility-audit/`

## Scope

Executed the Stage 4C local validation and reproducibility-audit supplement
only. No data processing, ALA downloads, model runs, remote compute,
manuscript science edits, source/test edits, release packaging, archive upload,
DOI tooling, commit, push, merge, or PR work was performed.

## Starting state

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD: `9082f4f`
- Remote-tracking HEAD: `origin/main` at `9082f4f`
- Starting status: `## main...origin/main` plus the untracked Goal 008 packet.
- Packet read: `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md`.

## Validation run

- `make ms-check`: passed.
- `make test`: passed, `40 passed, 9 skipped in 1.56s`.
- `make build`: passed, produced package artefacts under `/tmp/dsipa-build`.
- Local evidence reconciliation to `/tmp`: command passed, but evidence status
  was not release-clean: 28/38 files present, 27 verified, 10 missing required
  large/restricted ignored files, and one tracked figure checksum mismatch
  against the older evidence snapshot.
- Manual claim/denominator/release/reference/manifest scans were run and
  classified in `analysis/reports/stage4C_final_validation_report.md`.
- Final post-edit gates passed: `git diff --check`, Stage 4C file-presence
  checks, targeted old-checksum-prefix scan over current release-facing
  surfaces, and targeted `a751d630` checksum documentation scan.

## Review iteration: manifest checksum consistency

- Reviewer supplied a manifest-vs-evidence checksum comparison that found two
  inherited mismatches in `analysis/reports/final_release_manifest.md` for
  `pa_geometries_v0_3_0` CSV/GPKG rows.
- Corrected those two manifest checksums to match
  `analysis/reports/evidence_reconciliation.json`.
- Reran the manifest-vs-evidence checksum comparison after correction; every
  compared row was `OK`.
- `git diff --check`, Stage 4C file-presence checks, and targeted checksum
  presence/absence scans passed.
- Did not rerun `make ms-check`, `make test`, or `make build` because no
  executable or manuscript surface changed.

## Outputs

- Created `analysis/reports/stage4C_final_validation_report.md`.
- Created `analysis/reports/final_reproducibility_audit_supplement.md`.
- Created `docs/goals/008-stage4C-final-validation-reproducibility-audit/Stage4C_Closeout.md`.
- Updated `analysis/reports/final_release_manifest.md` with current checkout
  metadata and Stage 4C evidence caveats.
- Updated `docs/stage1_critique_resolution_matrix.md` for R01, R02, R04, R05,
  R08, R09, and M03.
- Updated `docs/stage_overview.md` with the Goal 008 validation status.
- Updated the Goal 008 log.

## Recommendation

No-move to archive, DOI minting, release packaging, GitHub release, or
publication submission from this checkout.

The manuscript/check/test/build surface is locally green, but final release
requires an authorized archive/DOI decision, availability of the large ignored
outputs or an explicit regeneration/exclusion decision, and a refreshed
evidence reconciliation for the current tracked baseline figure hash.

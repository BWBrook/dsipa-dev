# Stage 4E Option B Zenodo Archive Staging Closeout

Status: blocked before archive staging.

Generated: 2026-06-23 UTC by `nightlight` for Goal 010.

## Starting State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch/remote: `main...origin/main`
- HEAD: `b1c1539`
- Remote-tracking HEAD: `origin/main` at `b1c1539`
- Starting status: `## main...origin/main` plus untracked
  `docs/goals/010-optionB-zenodo-archive-staging/`
- Repo-local `AGENTS.md` was read.
- Goal packet read: `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md`.

## Work Completed

- Confirmed the approved release decision recorded in the Goal 010 packet:
  Option B Layer A archive scope, Zenodo-style DOI route, and no raw/row-level
  ALA redistribution exception.
- Inventoried the nine approved Layer A payload files locally.
- Ran narrow DSIPA-owned remote checks on `deep-server-ts` for the exact nine
  approved filenames under the documented evidence-store and DSIPA checkout
  paths.
- Created blocked/partial release surfaces:
  - `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.md`
  - `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.json`
  - `analysis/reports/zenodo_optionB_metadata_2026-06-23.md`
  - `analysis/reports/zenodo_release_checklist_2026-06-23.md`
- Created this closeout memo.
- Created `docs/log/130_optionB_zenodo_archive_staging.md`.
- Updated this goal log.
- Recorded DEC-040 in `docs/decisions.md`.
- Updated `docs/stage_overview.md` narrowly to show that Goal 010 is blocked,
  not release-complete.

No archive upload, DOI minting/reservation, GitHub release, tag, PR, commit,
push, package build, manuscript build, source/test edit, generated figure edit,
data processing, model run, full pipeline run, ALA download, compression, large
payload upload, or publication submission was performed.

## Blocker

The approved Option B payload is incomplete in the current checkout and in the
checked DSIPA-owned remote evidence-store paths.

Local inventory found:

- present and SHA-256 verified:
  `data/processed/pa_geometries_v0_3_0.csv`
- missing:
  - `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
  - `data/processed/pa_edge_profiles_national_v0_3_0.csv`
  - `data/processed/pa_buffer_validity_v0_3_0.csv`
  - `data/processed/pa_trends_v0_3_0.csv`
  - `data/processed/pa_risk_rankings_v0_3_0.csv`
  - `data/processed/pa_geometries_v0_3_0.gpkg`
  - `data/processed/pa_ibra_assignment_v0_3_0.csv`
  - `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`

Narrow remote searches found only:

- `deep-server-ts:/data/codex/repos/dsipa-dev-mac-sync/data/processed/pa_geometries_v0_3_0.csv`

The older evidence reconciliation report verifies that all nine files existed
and matched checksums in the 2026-05-14 evidence snapshot, but the retained
remote artefact directory contains the reports, not the missing large payload
files, and the current remote scratch checkout no longer has the eight missing
files.

## ALA Exclusion Confirmation

The four explicitly excluded raw/row-level ALA files were absent locally and
were not staged, copied, compressed, uploaded, or included in the Option B
payload:

- `data/raw/ala_occurrences/microbats_20260104T020628Z.zip`
- `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`

## Validation

- Local payload inventory: completed; 1/9 files present.
- Local checksum verification: completed for
  `data/processed/pa_geometries_v0_3_0.csv`; SHA-256 matched
  `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b`.
- Narrow remote evidence-store checks: completed; only the geometry CSV was
  found.
- Manifest JSON validation: passed with 9 payload rows, 8 blocked-missing
  rows, 1 verified-local-only row, 4 excluded ALA rows, and expected
  checksums/sizes matching `analysis/reports/evidence_reconciliation.json`.
- `git diff --check`: passed.
- Required file-presence checks: passed for the manifest, metadata, checklist,
  closeout, goal log, and stage log files.
- Targeted `rg` release/archive scan: 996 hits reviewed as expected historical,
  decision, manifest, and blocked-status language.
- Targeted `rg` raw/row-level ALA scan: 260 hits reviewed as expected policy,
  exclusion, and historical context language.
- Targeted `rg` Option B payload scan: 231 hits reviewed as expected payload
  inventory/checksum/context language.
- Targeted `rg` baseline-figure/evidence scan: 120 hits reviewed as expected
  evidence-snapshot and current checksum context.
- Final `git status --short --branch`: `## main...origin/main` with modified
  `docs/decisions.md`, modified `docs/stage_overview.md`, untracked Goal 010
  packet outputs, and untracked Goal 010 report/log files.

`make ms-check`, `make test`, `make build`, evidence reconciliation, pipeline
commands, and package/release commands were not run because this blocked
iteration changed only documentation/report surfaces and did not change
manuscript, executable, data, figure, or build surfaces.

## Recommendation

Do not open the later external-upload/DOI-mint goal yet. Goal 010 is blocked
until the eight missing approved Layer A payload files are recovered from a
concrete source or a separate explicitly authorized data/regeneration goal
creates and accepts a replacement payload. Keep raw/row-level ALA data
restricted/excluded by default.

# 130 Option B Zenodo archive staging

- Date/time (UTC): 2026-06-23 14:09 UTC
- Agent/environment: `nightlight` in `/Users/bwbrook/papers/dsipa-dev`
- Scope: execute Goal 010 Option B Zenodo-style archive staging, with no
  external archive upload, DOI minting/reservation, GitHub release,
  publication submission, new science, data processing, model run, figure
  regeneration, or ALA download.

## Starting State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Git state: `## main...origin/main` plus untracked
  `docs/goals/010-optionB-zenodo-archive-staging/`
- HEAD: `b1c1539`
- Remote-tracking HEAD: `origin/main` at `b1c1539`
- Read `AGENTS.md`.
- Read Goal 010 `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md`.

## Actions

- Confirmed the approved decision state: Option B Layer A archive payload,
  Zenodo-style DOI route, and no raw/row-level ALA redistribution exception.
- Checked local availability for the nine approved Layer A files.
- Checked local absence of the four explicitly excluded raw/row-level ALA
  files.
- Performed narrow DSIPA-owned remote searches on `deep-server-ts` for the
  exact nine approved filenames under:
  - `/data/codex/artifacts/dsipa/20260514T072832Z-evidence6`
  - `/data/codex/scratch/dsipa/20260514T072832Z-evidence6`
  - `/data/codex/repos/dsipa-dev-mac-sync`
  - `/data/codex/artifacts/dsipa`
  - `/data/codex/scratch/dsipa`
  - `/data/codex/repos`
- Wrote blocked release surfaces:
  - `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.md`
  - `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.json`
  - `analysis/reports/zenodo_optionB_metadata_2026-06-23.md`
  - `analysis/reports/zenodo_release_checklist_2026-06-23.md`
  - `docs/goals/010-optionB-zenodo-archive-staging/Stage4E_Closeout.md`
- Recorded DEC-040 and updated the stage overview narrowly.

## Outcome

Goal 010 is blocked before archive staging.

Only one approved Option B payload file is present and checksum-verified:

- `data/processed/pa_geometries_v0_3_0.csv`
  (`781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b`)

The other eight approved Layer A payload files are absent locally and absent
from the checked DSIPA-owned remote paths. No local archive staging directory
was created.

The four raw/row-level ALA files remain absent locally and were not staged,
copied, compressed, uploaded, or included.

## Validation

- Manifest JSON validation: passed against
  `analysis/reports/evidence_reconciliation.json`; 9 payload rows, 8
  blocked-missing rows, 1 verified-local-only row, and 4 excluded ALA rows.
- `git diff --check`: passed.
- Required file-presence checks: passed.
- Targeted `rg` scans:
  - release/archive/DOI/checksum/staging language: 996 hits, reviewed as
    expected blocked-status and historical/context language.
  - raw/row-level ALA policy language: 260 hits, reviewed as expected
    restricted/excluded policy and context language.
  - approved Option B payload filenames: 231 hits, reviewed as expected
    inventory/checksum/context language.
  - baseline-figure/evidence language: 120 hits, reviewed as expected current
    checksum and evidence-snapshot context.
- Final `git status --short --branch`: `## main...origin/main` with modified
  `docs/decisions.md`, modified `docs/stage_overview.md`, untracked Goal 010
  packet outputs, and untracked Goal 010 report/log files.

`make ms-check`, `make test`, `make build`, evidence reconciliation, pipeline
commands, package/release commands, and manuscript builds were not run because
this blocked iteration changed only documentation/report surfaces and did not
change manuscript, executable, data, figure, or build surfaces.

## Recommendation

Do not proceed to external archive upload, DOI minting/reservation, GitHub
release, release packaging, or publication submission. The later
external-upload/DOI-mint goal is not ready until the missing Layer A payload
files are recovered from a concrete source or regenerated under a separate,
explicitly authorized goal.

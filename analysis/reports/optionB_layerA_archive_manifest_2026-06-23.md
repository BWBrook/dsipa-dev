# Option B Layer A Archive Manifest

Status: blocked staging manifest. This report does not publish an archive, mint
or reserve a DOI, create a GitHub release, compress files, upload files, or
authorize publication submission.

Generated: 2026-06-23 UTC by `nightlight` for Goal 010.

## Executor State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch/status at start: `## main...origin/main` plus untracked
  `docs/goals/010-optionB-zenodo-archive-staging/`
- HEAD: `b1c1539`
- Remote-tracking HEAD: `origin/main` at `b1c1539`
- Goal packet read:
  `docs/goals/010-optionB-zenodo-archive-staging/{Goal.md,Plan.md,Runbook.md,Log.md}`
- Repo-local `AGENTS.md` was present and read.

## Decision Scope

Barry/orchestrator approved the Goal 009 recommended path:

- Option B archive scope: source/manuscript via git plus an external archive
  for the nine Layer A outputs listed below.
- Zenodo-style DOI route.
- No raw or row-level ALA redistribution exception.

This Goal 010 pass stopped before any external archive upload, DOI
minting/reservation, GitHub release, publication submission, release packaging,
data processing, model run, figure regeneration, or ALA download.

## Recovery And Staging Status

No archive staging directory was created, because the approved payload is
incomplete. The local checkout and the narrow DSIPA-owned remote evidence-store
checks found only one of the nine approved files:

- `data/processed/pa_geometries_v0_3_0.csv`

The following remote DSIPA paths were checked for exactly the approved Option B
filenames:

- `deep-server-ts:/data/codex/artifacts/dsipa/20260514T072832Z-evidence6`
- `deep-server-ts:/data/codex/scratch/dsipa/20260514T072832Z-evidence6`
- `deep-server-ts:/data/codex/repos/dsipa-dev-mac-sync`
- fallback exact-name search under:
  - `deep-server-ts:/data/codex/artifacts/dsipa`
  - `deep-server-ts:/data/codex/scratch/dsipa`
  - `deep-server-ts:/data/codex/repos`

The broader fallback search still found only:

- `deep-server-ts:/data/codex/repos/dsipa-dev-mac-sync/data/processed/pa_geometries_v0_3_0.csv`

## Approved Payload Inventory

| Archive status | Path | Expected bytes | Expected SHA-256 | Checked source status |
| --- | --- | ---: | --- | --- |
| blocked-missing | `data/processed/pa_radiance_buffers_national_v0_3_0.csv` | 96268937 | `493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e` | Absent locally; absent from checked DSIPA remote paths. |
| blocked-missing | `data/processed/pa_edge_profiles_national_v0_3_0.csv` | 25252979 | `9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888` | Absent locally; absent from checked DSIPA remote paths. |
| blocked-missing | `data/processed/pa_buffer_validity_v0_3_0.csv` | 2561064 | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | Absent locally; absent from checked DSIPA remote paths. |
| blocked-missing | `data/processed/pa_trends_v0_3_0.csv` | 5187168 | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | Absent locally; absent from checked DSIPA remote paths. |
| blocked-missing | `data/processed/pa_risk_rankings_v0_3_0.csv` | 600663 | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | Absent locally; absent from checked DSIPA remote paths. |
| verified-local-only | `data/processed/pa_geometries_v0_3_0.csv` | 1768417 | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | Present locally and in the checked DSIPA remote checkout; checksum verified locally. |
| blocked-missing | `data/processed/pa_geometries_v0_3_0.gpkg` | 132571136 | `0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11` | Absent locally; absent from checked DSIPA remote paths. |
| blocked-missing | `data/processed/pa_ibra_assignment_v0_3_0.csv` | 987075 | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | Absent locally; absent from checked DSIPA remote paths. |
| blocked-missing | `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv` | 582886 | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | Absent locally; absent from checked DSIPA remote paths. |

The expected bytes and checksums are taken from
`analysis/reports/evidence_reconciliation.json` and match the Goal 010
runbook. That evidence snapshot proves a prior verified state, but it does not
provide a current file source for the missing eight payload files.

## ALA Exclusion Confirmation

The following restricted/excluded raw or row-level ALA files were absent
locally and were not staged, copied, compressed, uploaded, or included in the
Option B payload:

- `data/raw/ala_occurrences/microbats_20260104T020628Z.zip`
- `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`

The release-facing rule remains: raw ALA downloads and row-level processed ALA
occurrence tables are restricted/excluded by default and require a separate
permission decision before redistribution.

## Baseline Figure Evidence Supplement

Goal 010 does not modify evidence reconciliation code or generated figures. The
current accepted baseline figure checksum is retained as a release supplement:

- `manuscript/figures/fig_layerA_baseline_map.png`
- Current tracked SHA-256:
  `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`
- Older evidence snapshot SHA-256:
  `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`

The difference remains classified as evidence-snapshot staleness from accepted
Stage 2 figure work, not current local figure drift.

## Recommendation

Do not proceed to external archive upload, DOI minting/reservation, GitHub
release, or publication submission. The later external-upload/DOI-mint goal is
not ready until the eight missing approved Layer A payload files are recovered
from a concrete source or a separate, explicitly authorized regeneration goal
produces a new accepted payload and evidence snapshot.

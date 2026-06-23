# Final Release Manifest (Stage 4B readiness)

Status: readiness manifest only. This file does not publish an archive, mint a
DOI, move large files, or package a release.

Generated: 2026-06-23 by `nightlight` for Goal 007.
Stage 4C validation update: 2026-06-23 by `nightlight` for Goal 008.
Stage 4D decision-packet update: see
`docs/release_blocker_decision_packet.md` for the recommended release-blocker
decision path. This pointer does not authorize archive upload, DOI minting,
release packaging, or publication submission.

Current local checkout after accepted Goal 007:

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD: `9082f4f`
- Remote-tracking HEAD: `origin/main` at `9082f4f`
- Goal 008 starting status: `## main...origin/main` plus the untracked Goal
  008 packet.

## Purpose

This manifest gives the Stage 4 release/data-availability decision surface
before any archive upload, DOI minting, final release packaging, or final
validation release work. It classifies the paper-relevant repo, data, report,
figure, and occurrence evidence surfaces using the Goal 007 vocabulary:
`tracked`, `archived-proposed`, `regenerated`, `excluded`, and `restricted`.

## Classification vocabulary

- `tracked`: version-controlled in this repository and intended to ship through
  the source/manuscript repository path.
- `archived-proposed`: not tracked in git, paper-relevant, and proposed for a
  later external archive after explicit Barry/orchestrator decision and final
  validation.
- `regenerated`: not intended for direct archival as a primary release object;
  recreated by the documented pipeline or build commands.
- `excluded`: not part of the release surface.
- `restricted`: not redistributed by default because licence/provider terms or
  row-level occurrence sensitivity require an explicit later decision.

## Evidence sources

- `data/README.md`: source provenance and current checksum inventory.
- `analysis/reports/evidence_reconciliation.md` and `.json`: 38/38 expected
  evidence files verified with zero checksum mismatches in the deep-server
  reconciliation snapshot generated 2026-05-14.
- `analysis/reports/stage4C_final_validation_report.md` and
  `analysis/reports/final_reproducibility_audit_supplement.md`: current local
  Stage 4C validation at `9082f4f`, including the `/tmp` evidence check.
- `analysis/reports/reproducibility_audit.md`: pre-final reproducibility audit
  and large-file caveat.
- `analysis/reports/zenodo_release_checklist_2026-01-04.md`: pre-final large
  Layer A archive checklist.
- `analysis/reports/layerB_ala_license_ledger.md`: provider licence mix for
  Layer B ALA downloads.
- `docs/stage4_manuscript_release_plan.md`: accepted Stage 4B scope.

The evidence reconciliation snapshot was generated on `deep-server` at git
commit `f73156272104ed16b0506617fc423e5c6478f50e` with `dirty=true`. It is a
verified evidence snapshot, not a final clean release audit.

The Stage 4C local evidence check at `9082f4f` did not overwrite the
repository evidence snapshot. It wrote only to `/tmp` and found 28 of 38
required files present, 27 checksum-verified files, 10 missing large ignored
outputs, and one tracked figure checksum mismatch against the older snapshot.
The mismatched file was `manuscript/figures/fig_layerA_baseline_map.png`:
current tracked checkout SHA-256
`ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`, older
snapshot expected SHA-256
`e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`.
`git log` shows the tracked figure changed in accepted Stage 2 commit
`896131a`, so this is evidence-snapshot staleness rather than a local dirty
figure. Final archive or DOI work must refresh the evidence manifest against
the current tracked figure set.

## Release posture

- No external archive or DOI is published from this checkout.
- `docs/ref_doi.txt` is a citation scaffold only; it is not a final archive DOI
  decision.
- Large Layer A national outputs are archive candidates, not already archived
  by this Stage 4B goal.
- Raw ALA downloads and row-level processed ALA occurrence tables are
  restricted/excluded by default. They must not be redistributed in the release
  package unless a later explicit Barry/orchestrator decision records the
  permission basis.
- Manuscript-facing Layer B evidence remains derived summaries, reports, and
  figures.

## Tracked repo/manuscript surface

| Classification | Surface | Release handling |
| --- | --- | --- |
| tracked | `README.md`, `data/README.md`, `docs/decisions.md`, `docs/stage1_critique_resolution_matrix.md`, `docs/stage_overview.md` | Source and governance documentation. |
| tracked | `manuscript/text/manuscript_draft.md` | Manuscript source, including data/code availability wording. |
| tracked | `manuscript/figures/*.png` | Paper figures are tracked. Stage 4C found the current tracked baseline-map checksum differs from the older evidence snapshot and must be refreshed before final release packaging. |
| tracked | `analysis/reports/*.md`, `analysis/reports/*.json`, selected small CSV/PNG report artefacts | Review and evidence reports that are small enough for git. |
| tracked | `data/processed/layerB_occurrence_summary_v0_3_0.csv` | Derived Layer B summary counts; no row-level occurrence records. |
| tracked | `data/processed/layerB_ala_license_ledger_v0_3_0.csv` | Provider licence/provenance ledger; mixed ALA provider terms retained. |
| tracked | `data/processed/layerB_model_input_summary_v0_3_0.csv` | Derived model-input summary; no row-level records. |
| tracked | `data/processed/layerB_ibra_summary_v0_3_0.csv` | Derived IBRA summary; no row-level records. |
| tracked | smoke-test fixtures under `data/processed/*smoketest*` and `smoke_test_triad*` | Lightweight regression fixtures, not national release payloads. |

## Archived-proposed large Layer A outputs

These files are not tracked in git. They are paper-relevant, checksum-verified
in the 2026-05-14 evidence reconciliation snapshot, and proposed for a later
external archive after an explicit archive/DOI decision.

| Classification | Path | Evidence checksum | Release rationale |
| --- | --- | --- | --- |
| archived-proposed | `data/processed/pa_radiance_buffers_national_v0_3_0.csv` | `493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e` | Core Layer A inside/buffer annual radiance table. |
| archived-proposed | `data/processed/pa_edge_profiles_national_v0_3_0.csv` | `9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888` | Core Layer A boundary-to-interior ring table. |
| archived-proposed | `data/processed/pa_buffer_validity_v0_3_0.csv` | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | Buffer land/overlap validity descriptors used to interpret outside-buffer pressure. |
| archived-proposed | `data/processed/pa_trends_v0_3_0.csv` | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | Trend estimates and retention/quadrant metrics. |
| archived-proposed | `data/processed/pa_risk_rankings_v0_3_0.csv` | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | Category-safe watchlists and rankings. |
| archived-proposed | `data/processed/pa_geometries_v0_3_0.csv` | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | Protected-area descriptors supporting denominators and joins. |
| archived-proposed | `data/processed/pa_geometries_v0_3_0.gpkg` | `0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11` | Processed protected-area geometry layer; large binary context file. |
| archived-proposed | `data/processed/pa_ibra_assignment_v0_3_0.csv` | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | Dominant IBRA assignments used for uncertainty summaries. |
| archived-proposed | `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv` | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | IBRA-clustered trend-uncertainty summaries. |

## Layer B ALA occurrence release policy

| Classification | Path or surface | Evidence checksum | Release rationale |
| --- | --- | --- | --- |
| restricted | `data/raw/ala_occurrences/microbats_20260104T020628Z.zip` | `f0272a2ae9a53fbe53530367cdb9ac2458122889c86264f1e623f06d7074b86a` | Raw ALA provider bundle with mixed licences; not redistributed by default. |
| restricted | `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip` | `0277111ae02416ccdd7b4975a22c05030da89ccca634a1345e86828ea3de7c10` | Raw ALA provider bundle with mixed licences; not redistributed by default. |
| restricted | `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz` | `19e87ebda5e61cd0eb08a2824f85d63fe5dfc870527cd0ac9f21c00e38f1c007` | Row-level processed occurrence table; excluded from default release package. |
| restricted | `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz` | `b4de14ec88af0a34c82553078d3a8c9b01c664413fde0262fe050fefed6e12ba` | Row-level processed occurrence table; excluded from default release package. |
| tracked | `data/processed/layerB_occurrence_summary_v0_3_0.csv` | `ec7746a882675b4955b7d455cddae2f9851bde55d16900cf6b32979346f77474` | Derived summary counts; suitable for repo release. |
| tracked | `data/processed/layerB_ala_license_ledger_v0_3_0.csv` | `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0` | Provider licence/provenance ledger. This is the current checkout byte SHA-256; evidence reconciliation reports the same value after CRLF-to-LF normalization. |
| tracked | `data/processed/layerB_model_input_summary_v0_3_0.csv` | `f42e9fea29dea812f54e4e9a02fafa3c7d6382e499d20e31b267b84be9346575` | Derived model subset summary. |
| tracked | `data/processed/layerB_ibra_summary_v0_3_0.csv` | `ed117aadd0c700c8dd0c7180714112fd212567f4b1ec56d0c8464f2e77d00a0d` | Derived IBRA exposure/count summary. |
| excluded | Squamata/diurnal reptile ALA control | N/A | Deferred after ALA 500 errors; not part of this manuscript release surface. |

## Regenerated/excluded surfaces

| Classification | Surface | Release handling |
| --- | --- | --- |
| regenerated | `artefacts/` and `analysis/state_runs/` | Recreated by the documented pipeline; not a primary Stage 4B release payload unless a later archive-scope decision expands the package. |
| regenerated | package build outputs such as `dist/` and `build/` | Recreated by release tooling; not committed or archived by this goal. |
| regenerated | manuscript build outputs | Recreated by the manuscript build path; this goal only updates source availability wording. |
| excluded | `docs/ref_doi.txt` as a DOI authority | Citation scaffold only until a final external archive DOI exists. |

## Checksum convention

- Checksums in `data/README.md` default to SHA-256 unless otherwise stated.
- Nightlights GeoTIFF entries use the source MD5 convention recorded by the
  nightlights workflow.
- `layerB_ala_license_ledger_v0_3_0.csv` currently has byte SHA-256
  `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`.
  `analysis/reports/evidence_reconciliation.md` and `.json` compute the
  ledger checksum after CRLF-to-LF normalization and report the same value
  (`normalize_crlf: true`), so no separate current raw-file checksum is
  recorded here.

## Decisions still required

- Barry/orchestrator decision: approve the final archive scope for
  `archived-proposed` files.
- Barry/orchestrator decision: choose the external repository/record and mint a
  final DOI before publication wording cites one.
- Barry/orchestrator decision: decide whether any raw ALA or row-level
  processed occurrence data can be redistributed. The default here is
  restricted/excluded.
- Stage 4C/final release work: refresh the evidence reconciliation/audit on the
  final clean release state and update availability wording with the real DOI.
- Stage 4C follow-up: refresh the current figure checksum evidence for
  `manuscript/figures/fig_layerA_baseline_map.png` before archive, DOI, or
  publication packaging.
- Stage 4D decision path: review `docs/release_blocker_decision_packet.md` and
  record Barry/orchestrator decisions before any release-execution goal.

## Readiness assessment

Stage 4B remains ready for orchestrator review as a release/data-availability
decision surface. Goal 008 adds a no-move recommendation for archive, DOI,
release packaging, and publication submission until the current evidence
snapshot is refreshed and the required large-output/archive decisions are
recorded. Goal 009 adds a recommended decision path but does not authorize
release movement.

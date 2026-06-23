# Stage 4C Final Validation Report

Status: complete as a validation decision surface; no-move for archive, DOI,
release packaging, or publication submission.

Generated: 2026-06-23 by `nightlight` for Goal 008.

## Scope

This report records the authorized Stage 4C local validation only. It does not
run data processing, ALA downloads, model runs, remote compute, release
packaging, archive upload, DOI tooling, GitHub release tooling, or publication
submission tooling.

## Starting state

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD: `9082f4f`
- Remote-tracking HEAD: `origin/main` at `9082f4f`
- Starting status: `## main...origin/main` plus the untracked Goal 008 packet.
- Goal packet present: `docs/goals/008-stage4C-final-validation-reproducibility-audit/`
  with `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md`.

## Command validation

| Gate | Command | Result |
| --- | --- | --- |
| Manuscript/checks | `make ms-check` | PASS. Manuscript lint/build checks passed; makedoc tests passed; reference audit reported 30 bibliography keys, 26 cited keys, 0 unknown keys, and 4 unused non-fatal keys (`bara2023`, `elvidge2017`, `roman2018`, `sung2022`). |
| Python tests | `make test` | PASS. `40 passed, 9 skipped in 1.56s`. Skips are expected for absent large ignored national outputs and instruct regeneration via pipeline. |
| Package build | `make build` | PASS. Built sdist and wheel under `/tmp/dsipa-build`: `dsipa_nbs-0.1.0.tar.gz` and `dsipa_nbs-0.1.0-py3-none-any.whl`. The build also created ignored local `build/` and `src/python/dsipa_nbs.egg-info/` working files. |
| Evidence reconciliation | `uv run python -m dsipa.evidence_reconciliation --output-md /tmp/dsipa_stage4c_evidence_reconciliation.md --output-json /tmp/dsipa_stage4c_evidence_reconciliation.json --audit-md /tmp/dsipa_stage4c_reproducibility_audit.md --write-audit` | PASS as a command, but not release-clean as evidence. The `/tmp` report found 38 expected required files, 28 present, 27 checksum-verified, 10 missing required files, and 1 checksum mismatch. |
| Initial whitespace check | `git diff --check` | PASS before Stage 4C report edits. A final pass was also run after edits. |

No `uv` `VIRTUAL_ENV` mismatch warning was reproduced in the authorized command
set, so no README troubleshooting update was required for R04.

## Evidence reconciliation classification

The local Stage 4C evidence check wrote only to `/tmp` and left the repository
evidence reports unchanged. It classified the current checkout as
`main` at `9082f4ff6c906ba554e4e6a86b126fb9f175fe7c` with `dirty=True`
because the Goal 008 packet and this validation work are uncommitted.

Missing required files in the local checkout:

- `data/processed/pa_geometries_v0_3_0.gpkg`
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `data/processed/pa_trends_v0_3_0.csv`
- `data/processed/pa_risk_rankings_v0_3_0.csv`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`

These are large ignored or restricted/release-gated outputs. Their absence is
consistent with the Stage 4B manifest, but it blocks a complete local
release-clean evidence proof.

Checksum mismatch:

- `manuscript/figures/fig_layerA_baseline_map.png`
  - Current tracked checkout SHA-256:
    `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`
  - Older evidence snapshot expected SHA-256:
    `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`

The figure is not locally dirty. `git log` shows it changed in accepted Stage 2
commit `896131a`, so this is stale evidence-snapshot metadata rather than an
uncontrolled local figure edit. It still blocks final release packaging until
the evidence manifest is refreshed against the current tracked figure.

The Layer B licence ledger checksum remains correct for the current checkout:
`a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`.
The evidence JSON also records this value with `normalize_crlf: true`.

## Manual scan classifications

| Scan | Command summary | Lines | Classification |
| --- | --- | ---: | --- |
| Claim discipline | `rg` over manuscript text and docs for causal/population/national-biodiversity/provider-bounded/presence-only/falsification terms | 194 | PASS. Manuscript hits are explicit limitations, conservative Layer B framing, or citation/context statements. Historical goal/planning hits include old scan commands and constraints. No paper-facing causal, population-trend, population-decline, or national biodiversity response claim was found. |
| Denominators and censoring | `rg` over manuscript text for denominator, eligibility, censoring, ring, provider-matched, AUC, log-loss, and redistribution terms | 54 | PASS. Manuscript/table/figure hits are expected denominator and feasibility statements. They preserve `n = 11,133`, `4,426`, `3,858`, ring-complete `n = 383`, provider-matched `50,281` per class, AUC/log-loss, and raw/row-level redistribution limits. |
| Release/data availability | `rg` over manuscript text, docs, `data/README.md`, and `analysis/reports` for release, licence, archive, DOI, checksum, and redistribution terms | 689 | PASS with release-gate caveats. Current paper-facing wording says no external archive DOI has been minted and raw/row-level ALA occurrence data are not redistributed by default. Large output/archive/DOI decisions remain open. |
| References | `rg` over manuscript text, `references/refs.yaml`, and `docs/ref_doi.txt` for DOI/citation/TODO patterns | 82 | PASS. Manuscript hits are bracket citations plus one numeric table value; reference YAML and the parked DOI scaffold explain DOI hits. Separate TODO/FIXME/citation-needed scan returned no hits. |
| Manifest consistency | `rg` over the manifest, evidence reports, `data/README.md`, and Stage 4B closeout for commit/checksum/classification terms | 80 | PASS after narrow manifest update for checkout metadata. A review-iteration checksum comparison then found two inherited manifest row mismatches for `pa_geometries_v0_3_0` outputs; those rows now match `analysis/reports/evidence_reconciliation.json`. The old conflicting Layer B licence-ledger checksum prefix appears only in the Goal 008 packet instructions, not as a current release-facing checksum. |

Final post-edit gates passed: `git diff --check`, required Stage 4C file
presence checks, a targeted scan confirming the old conflicting checksum prefix
is absent from current release-facing surfaces, and a targeted scan confirming
`a751d630...` remains documented.

## Review iteration: manifest checksum consistency

A reviewer-supplied manifest-vs-evidence checksum comparison found two
inherited manifest mismatches in the archived-proposed PA geometry rows.
`analysis/reports/final_release_manifest.md` was corrected to the evidence JSON
values:

- `data/processed/pa_geometries_v0_3_0.csv`:
  `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b`
- `data/processed/pa_geometries_v0_3_0.gpkg`:
  `0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11`

The post-correction manifest-vs-evidence comparison reports every compared
manifest/evidence row as `OK`. `make ms-check`, `make test`, and `make build`
were not rerun in this iteration because no executable or manuscript surface
changed.

## Matrix updates

Stage 4C updates the critique-resolution matrix as follows:

- R01: `release-gate` to `done`, because this report and the reproducibility
  supplement record the accepted checkout, command set, dirty/output state, and
  remaining blockers.
- R04: `open` to `done`, because the `uv` warning did not reproduce in the
  authorized validation commands.
- R08: `open` to `done`, because Stage 4C records tests/build plus domain,
  release, reference, and manifest scan classifications.
- M03: `open` to `done`, because `make ms-check` found zero unknown
  bibliography keys and the raw DOI list remains a parked scaffold outside the
  paper text.
- R02 and R05 remain `release-gate` because no archive, DOI, large-file staging,
  or release package has been authorized or completed.

## Recommendation

No-move for archive, DOI minting, release packaging, GitHub release, or
publication submission from this checkout.

Move is acceptable only for orchestrator review of the decision surface and for
human scientific/manuscript judgment if the remaining blockers are treated as
release-gate, not as new science requirements.

Required before publication/release:

1. Decide final archive scope for `archived-proposed` large Layer A files.
2. Decide external archive/DOI policy and update data/code availability wording
   only after the real archive DOI exists.
3. Refresh evidence reconciliation against the current tracked figure set,
   including `fig_layerA_baseline_map.png`.
4. Stage or otherwise verify large ignored outputs under an authorized
   release/archive goal without redistributing restricted raw or row-level ALA
   data by default.

# Stage 4C Closeout

Status: complete as a validation and reproducibility-audit supplement; blocked
for release/archive movement.

Generated: 2026-06-23 by `nightlight` for Goal 008.

## Starting state

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD: `9082f4f`
- Remote-tracking HEAD: `origin/main` at `9082f4f`
- Starting status: `## main...origin/main` plus the untracked Goal 008 packet.
- Repo-local `AGENTS.md` was read.
- Goal packet read: `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md`.

## Work completed

- Created `analysis/reports/stage4C_final_validation_report.md`.
- Created `analysis/reports/final_reproducibility_audit_supplement.md`.
- Created `docs/log/128_stage4C_final_validation_reproducibility.md`.
- Updated `analysis/reports/final_release_manifest.md` with current checkout
  metadata and Stage 4C evidence caveats.
- Updated `docs/stage1_critique_resolution_matrix.md`:
  - R01 to `done`.
  - R04 to `done`.
  - R08 to `done`.
  - M03 to `done`.
  - R02 and R05 remain `release-gate`.
  - R09 remains `done` with the Stage 4C checksum confirmation.
- Updated `docs/stage_overview.md` with the Goal 008 no-move release
  recommendation.
- Updated the Goal 008 packet log.

No manuscript science text, source code, tests, generated data, generated
figures, release packages, archive files, DOI files, commits, pushes, merges,
or PRs were created.

## Validation evidence

| Gate | Result |
| --- | --- |
| `make ms-check` | Passed. Manuscript checks and makedoc tests passed. Reference audit: 30 bibliography keys, 26 cited keys, 0 unknown keys, 4 unused non-fatal keys. |
| `make test` | Passed. `40 passed, 9 skipped in 1.56s`; skips are expected absent large ignored national outputs. |
| `make build` | Passed. Built sdist and wheel in `/tmp/dsipa-build`; ignored local `build/` and `src/python/dsipa_nbs.egg-info/` were created by the authorized build. |
| Local evidence reconciliation to `/tmp` | Command passed, but evidence status is not release-clean: 28/38 required files present, 27 verified, 10 missing required large/restricted ignored files, and 1 checksum mismatch. |
| Manual scans | Claim discipline, denominator/censoring, release/data availability, reference, and manifest consistency scans were run and classified in the Stage 4C report. |
| Checksum correction carry-forward | Current Layer B licence ledger SHA-256 remains `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`; the old conflicting checksum prefix appears only in the Goal 008 packet instructions, not as a current release-facing checksum. |
| Final post-edit gates | `git diff --check` passed; all expected Stage 4C output files were present; targeted checksum scans confirmed the old conflicting checksum prefix is absent from current release-facing surfaces and `a751d630...` remains documented. |
| Review iteration checksum comparison | Corrected two inherited manifest checksum mismatches for `pa_geometries_v0_3_0` CSV/GPKG rows; the post-correction manifest-vs-evidence comparison reports every compared row as `OK`. |

## Blockers and recommendation

No-move for archive, DOI minting, release packaging, GitHub release, or
publication submission.

Remaining blockers:

- Ten required large/restricted ignored evidence files are absent from the
  local checkout. This is expected under the Stage 4B release policy, but it
  prevents a complete local release-clean proof.
- `manuscript/figures/fig_layerA_baseline_map.png` is tracked and not dirty,
  but its current SHA-256
  `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`
  differs from the older evidence snapshot expected SHA-256
  `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`.
  The difference traces to accepted Stage 2 figure work in commit `896131a`,
  so it requires evidence-refresh, not manuscript or figure rewriting.
- R02 remains open as a release gate: no external archive or DOI exists.
- R05 remains open as a release gate: large ignored outputs need an approved
  archive/regeneration/exclusion decision; raw and row-level ALA data remain
  restricted/excluded by default.

The current checkout is suitable for orchestrator review of the decision
surface and for manuscript/science judgment with the release gates visible. It
is not suitable for final release, archive, DOI, or publication submission.

Review iteration note: `make ms-check`, `make test`, and `make build` were not
rerun because only documentation/report checksum rows changed; no manuscript,
source, test, data, or figure surface was edited.

Final `git status --short --branch`:

```text
## main...origin/main
 M analysis/reports/final_release_manifest.md
 M docs/stage1_critique_resolution_matrix.md
 M docs/stage_overview.md
?? analysis/reports/final_reproducibility_audit_supplement.md
?? analysis/reports/stage4C_final_validation_report.md
?? docs/goals/008-stage4C-final-validation-reproducibility-audit/
?? docs/log/128_stage4C_final_validation_reproducibility.md
```

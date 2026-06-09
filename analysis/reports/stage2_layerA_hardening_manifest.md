# Stage 2 Layer A hardening manifest

Generated: 2026-05-25 05:13 UTC

## Scope

This manifest records the Stage 2 Layer A hardening package. The canonical local artefact folder is:

`artefacts/stage2_layerA_hardening/`

The `artefacts/` tree is intentionally git-ignored, so this tracked report is the repo-visible pointer to the package contents and validation status.

## Git state

- Branch: `main`
- Stage 2 baseline commit: `dab3ddb55d04cfbfd39deb35c5e9ed3274f5447e`
- Worktree: expected dirty Stage 1/2 changes plus generated Stage 2 reports; no unrelated changes were reverted.

## Packaged outputs

The package contains the following Stage 2 evidence, manuscript, governance, and checksum artefacts:

- `README.md`
- `fig_layerA_baseline_map.png`
- `fig_layerA_baseline_map_stage2_a02.sha256`
- `layerA_anchors_buffer_stage2.sha256`
- `layerA_buffer_validity_sensitivity.csv`
- `layerA_buffer_validity_sensitivity.md`
- `layerA_denominators_and_censoring.csv`
- `layerA_denominators_and_censoring.md`
- `layerA_dominance_summary.csv`
- `layerA_dominance_summary.md`
- `layerA_edge_profile_decision.csv`
- `layerA_edge_profile_decision.md`
- `layerA_sanity_dashboard.md`
- `layerA_sensitivity_mean_vs_median.png`
- `layerA_table1_candidate.md`
- `layerA_tables_stage2_denominators.sha256`
- `layerA_threshold_edge_stage2.sha256`
- `layerA_trend_threshold_sensitivity.csv`
- `layerA_trend_threshold_sensitivity.md`
- `layerA_watchlists_stage2.sha256`
- `layerA_watchlists_uncertainty.csv`
- `layerA_watchlists_uncertainty.md`
- `figures.md`
- `supplementary_figures.md`
- `tables.md`
- `supplementary_tables.md`
- `stage1_critique_resolution_matrix.md`
- `stage2_layerA_hardening_manifest.md`
- `stage2_layerA_hardening_plan.md`
- `stage_overview.md`
- `121_stage2_layerA_hardening.md`
- `interpretation_notes.md`
- `decisions.md`
- `SHA256SUMS`

`sha256sum -c SHA256SUMS` passed from inside `artefacts/stage2_layerA_hardening/`.

## Remote tmux runs

- `20260525T024610Z-stage2-a02-figure`: regenerated baseline figure after ineligible/missing label fix.
- `20260525T030528Z-stage2-denominators`: generated denominator/censoring report and Table 1 source.
- `20260525T033352Z-stage2-anchors-buffer`: regenerated sanity dashboard and buffer-validity sensitivity.
- `20260525T035530Z-stage2-threshold-edge`: generated trend-threshold sensitivity and edge-profile decision report.
- `20260525T044118Z-stage2-watchlists`: generated uncertainty-aware watchlists, dominance summary, and Table S1.
- `20260525T050953Z-stage2-validation`: final remote validation/build run.

Remote run roots follow the Stage 0 harness convention:

- Logs: `/data/codex/scratch/dsipa/<RUN_ID>/`
- Durable copied artefacts: `/data/codex/artifacts/dsipa/<RUN_ID>/`

## Domain sanity closeout

- Denominators are explicit: PA universe `n=11,133`, 2024 inside eligibility `n=4,426`, retention/quadrant denominator `n=3,858`, complete-ring subset `n=383`.
- Censoring/floor mass is central: 2024 inside eligible zero mean is 86.9%; primary inside trend zero-slope fraction is 89.7%.
- Bright/dark anchors now behave as expected: urban-adjacent eligible PAs have 2024 inside p95 much higher than remote eligible PAs.
- Buffer-validity sensitivity preserves the quadrant interpretation under stricter filters.
- Trend-threshold sensitivity preserves the primary interpretation across valid-year thresholds and stricter valid-pixel thresholds.
- Edge profiles are retained only as feasibility-limited diagnostics, not a definitive edge-effect test.
- Table S1 is populated with category-safe, uncertainty-aware watchlists; all 60 rows have inside-slope bootstrap uncertainty.
- Dominance heatmap now has a simplified companion summary, supporting triage without precise rank overclaiming.

## Validation closeout

- Local `git diff --check` passed.
- Local targeted Stage 2 tests: 8 passed, 2 skipped for locally absent ignored national outputs.
- Local full pytest smoke: 34 passed, 9 skipped for locally absent ignored national outputs.
- Local build: `uv build --out-dir /tmp/dsipa-build-stage2` succeeded.
- Remote deep-server validation run `20260525T050953Z-stage2-validation` passed 10 targeted tests, 41 full tests, and built wheel/sdist artefacts.
- Remote build checksums:
  - `51b5e2a895a15f5ab7bad0dbe180d611f9e710ad8e0546c21d37ccddb06d5ac8` — `dsipa_nbs-0.1.0-py3-none-any.whl`
  - `6f4ae032061a485cc6ab3b6556c4a994bc4b8367f67b011b3fca1c9c50d23eb0` — `dsipa_nbs-0.1.0.tar.gz`

## Gate recommendation

Stage 2 passed its exit gate for the current evidence state and is ready for user signoff. The recommended next step after signoff is Stage 3 planning for Layer B reconciliation.

## Known caveats carried forward

- Stage 2 hardens Layer A only; Layer B remains for Stage 3.
- Stage 2 reports inside-slope bootstrap uncertainty in Table S1; buffer and retention uncertainty remain point-estimate fields.
- Release archive/DOI and large ignored data-output packaging remain Stage 4 release gates.
- Stage 4 still needs manuscript-level prose synthesis from the hardened evidence package.

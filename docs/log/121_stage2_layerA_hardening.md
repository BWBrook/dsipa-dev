# 121 Stage 2 Layer A hardening

Date: 2026-05-25

## Scope

Opened Stage 2 after user acceptance of the Stage 1 critique-resolution matrix. The purpose of Stage 2 is to harden the primary Layer A protected-area ALAN result before any Layer B reconciliation or manuscript rewrite.

## Baseline

- DSIPA checkout: `main` at `dab3ddb`.
- Stage 1: accepted by the user on 2026-05-25.
- Evidence snapshot: deep-server reconciliation reports 38/38 expected files present and checksum verified.
- Current worktree: expected stage-planning documentation changes are uncommitted.

## Changes

- Marked Stage 1 as accepted in `docs/stage1_critique_resolution_matrix.md`.
- Added `docs/stage2_layerA_hardening_plan.md`.
- Updated `docs/stage_overview.md` so Stage 1 is complete and Stage 2 is active.
- Started S2.3 by updating `src/python/dsipa/figures_layerA.py` so the baseline eligibility panel reports `ineligible` rather than `missing`.
- Regenerated `manuscript/figures/fig_layerA_baseline_map.png` on deep-server under tmux run `20260525T024610Z-stage2-a02-figure` and copied it back locally.
- Added `src/python/dsipa/layerA_tables.py` plus `tests/python/test_layerA_tables.py` to generate denominator/censoring reports from processed Layer A evidence.
- Generated and copied back:
  - `analysis/reports/layerA_denominators_and_censoring.md`
  - `analysis/reports/layerA_denominators_and_censoring.csv`
  - `analysis/reports/layerA_table1_candidate.md`
  - `analysis/reports/layerA_tables_stage2_denominators.sha256`
- Replaced the placeholder in `manuscript/text/tables.md` with validated Table 1 values.
- Marked A02 and A14 as `done` in `docs/stage1_critique_resolution_matrix.md`.
- Updated `src/python/dsipa/layerA_sanity.py` to replace the old median-by-distance anchor framing with explicit bright/dark context anchors.
- Added `src/python/dsipa/layerA_buffer_sensitivity.py` plus `tests/python/test_layerA_buffer_sensitivity.py`.
- Regenerated and copied back from deep-server tmux run `20260525T033352Z-stage2-anchors-buffer`:
  - `analysis/reports/layerA_sanity_dashboard.md`
  - `analysis/reports/layerA_sensitivity_mean_vs_median.png`
  - `analysis/reports/layerA_buffer_validity_sensitivity.md`
  - `analysis/reports/layerA_buffer_validity_sensitivity.csv`
  - `analysis/reports/layerA_anchors_buffer_stage2.sha256`
- Marked A04, A05, A06, and A11 as `done` in `docs/stage1_critique_resolution_matrix.md`.
- Added `src/python/dsipa/layerA_threshold_sensitivity.py` plus `tests/python/test_layerA_threshold_sensitivity.py`.
- Added `src/python/dsipa/layerA_edge_decision.py` plus `tests/python/test_layerA_edge_decision.py`.
- Generated and copied back from deep-server tmux run `20260525T035530Z-stage2-threshold-edge`:
  - `analysis/reports/layerA_trend_threshold_sensitivity.md`
  - `analysis/reports/layerA_trend_threshold_sensitivity.csv`
  - `analysis/reports/layerA_edge_profile_decision.md`
  - `analysis/reports/layerA_edge_profile_decision.csv`
  - `analysis/reports/layerA_threshold_edge_stage2.sha256`
- Updated the supplementary edge-profile caption to state that median `frac_gt0` is zero under floor domination and that the conditional non-zero share is diagnostic only.
- Recorded the fixed-ring/adaptive-ring decision as `DEC-035` in `docs/decisions.md`.
- Marked A07, A08, and A09 as `done` in `docs/stage1_critique_resolution_matrix.md`.
- Added `src/python/dsipa/layerA_watchlists.py` plus `tests/python/test_layerA_watchlists.py`.
- Generated and copied back from deep-server tmux run `20260525T044118Z-stage2-watchlists`:
  - `analysis/reports/layerA_watchlists_uncertainty.md`
  - `analysis/reports/layerA_watchlists_uncertainty.csv`
  - `analysis/reports/layerA_dominance_summary.md`
  - `analysis/reports/layerA_dominance_summary.csv`
  - `analysis/reports/layerA_watchlists_stage2.sha256`
  - `manuscript/text/supplementary_tables.md`
- Replaced the Table S1 placeholder with category-safe, uncertainty-aware Layer A watchlists.
- Added a simplified dominance summary as the companion to the dominance heatmap.
- Marked A10, A12, and A13 as `done` in `docs/stage1_critique_resolution_matrix.md`.

## Initial Stage 2 priorities

- Fix terminology for minimum-pixel ineligibility versus true missingness.
- Build a generated denominator/censoring table for Table 1.
- Replace weak city-median anchors with defensible bright/dark sanity checks.
- Add valid-buffer and trend-threshold sensitivities.
- Decide the edge/penetration figure treatment.
- Integrate uncertainty into risk/watchlist tables.

## Validation

- `git diff --check` passed after the current Stage 2 planning and A02 source edits.
- `uv run python -m py_compile src/python/dsipa/figures_layerA.py` passed.
- `rg -n "missing|ineligible|Eligibility" src/python/dsipa/figures_layerA.py manuscript/text/figures.md manuscript/text/supplementary_figures.md docs/stage2_layerA_hardening_plan.md` confirms current paper-facing figure captions do not use stale "missing" language for the baseline eligibility panel.
- Attempted `uv run python -m dsipa.figures_layerA --skip-edge --skip-artefact` to regenerate the baseline figure, but local ignored evidence files are absent:
  - `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
  - `data/processed/pa_geometries_v0_3_0.gpkg`
- No Layer A figure output was changed by that failed local regeneration attempt.
- Remote tmux run `20260525T024610Z-stage2-a02-figure` completed and produced baseline figure SHA-256 `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`.
- Local visual inspection of the copied baseline figure confirmed the title now reads `eligible=4426, ineligible=6707`.
- `uv run pytest tests/python/test_layerA_tables.py -q` passed locally.
- `uv run python -m py_compile src/python/dsipa/layerA_tables.py tests/python/test_layerA_tables.py` passed locally.
- Remote tmux run `20260525T030528Z-stage2-denominators` completed:
  - `uv run python -m pytest tests/python/test_layerA_tables.py -q` passed on deep-server.
  - `uv run python -m dsipa.layerA_tables` generated the denominator/censoring outputs.
  - Generated SHA-256 values match `analysis/reports/layerA_tables_stage2_denominators.sha256`.
- Earlier remote denominator attempts exposed two useful environment issues and were superseded:
  - `uv run pytest` could not spawn the `pytest` console script, so the portable command is `uv run python -m pytest`.
  - `pandas.to_markdown()` required optional `tabulate`, so the report generator now uses an internal Markdown renderer.
- `uv run pytest tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_tables.py -q` passed locally.
- `uv run python -m py_compile src/python/dsipa/layerA_sanity.py src/python/dsipa/layerA_buffer_sensitivity.py tests/python/test_layerA_buffer_sensitivity.py` passed locally.
- Remote tmux run `20260525T033352Z-stage2-anchors-buffer` completed:
  - `uv run python -m pytest tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_tables.py -q` passed on deep-server.
  - `uv run python -m dsipa.layerA_sanity --skip-artefact` regenerated the sanity dashboard.
  - `uv run python -m dsipa.layerA_buffer_sensitivity` generated buffer-validity sensitivity outputs.
  - Generated SHA-256 values match `analysis/reports/layerA_anchors_buffer_stage2.sha256`.
- Anchor sanity checks now show urban-adjacent inside PAs have mean p95 112.769 versus 0.167 for remote inside PAs, and the top non-zero inside PA median mean is 41.630, both supporting the bright/dark sanity contrast.
- Buffer-validity sensitivity retains similar Q1/Q4 fractions under stricter filters:
  - primary n=3,858, Q1=7.9%, Q4=4.9%;
  - land fraction >=0.5 and protected overlap <=0.25 n=2,847, Q1=8.5%, Q4=5.1%.
- `uv run pytest tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_tables.py -q` passed locally.
- `uv run python -m py_compile src/python/dsipa/layerA_threshold_sensitivity.py src/python/dsipa/layerA_edge_decision.py tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py` passed locally.
- Remote tmux run `20260525T035530Z-stage2-threshold-edge` completed:
  - `uv run python -m pytest tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_tables.py -q` passed on deep-server.
  - `uv run python -m dsipa.layerA_threshold_sensitivity` generated trend-threshold sensitivity outputs.
  - `uv run python -m dsipa.layerA_edge_decision` generated the edge/penetration decision outputs.
  - Generated SHA-256 values match `analysis/reports/layerA_threshold_edge_stage2.sha256`.
- Trend-threshold sensitivity supports retaining the primary rule:
  - primary rule n=4,426 inside trends, zero-slope fraction=89.7%, positive-slope n=420, quadrant n=3,858, Q1=7.9%, Q4=4.9%;
  - stricter `>=50` valid pixels gives n=2,194 inside trends, zero-slope fraction=87.8%, positive-slope n=251, quadrant n=1,767, Q1=9.5%, Q4=5.5%;
  - changing minimum valid years from 6 to 10 does not change counts in the current complete annual evidence snapshot.
- Edge decision report supports retaining the existing 0-1, 1-5, and 5-10 km rings only as a feasibility-limited diagnostic:
  - complete-ring n=383 (3.4% of the PA universe);
  - complete-ring median `frac_gt0` is zero in all rings;
  - conditional non-zero share declines from 18.0% in the 0-1 km ring to 3.7% in the 5-10 km ring.
- Final S2.6/S2.7 hygiene checks passed:
  - `sha256sum -c analysis/reports/layerA_threshold_edge_stage2.sha256`
  - `git diff --check`
- `uv run pytest tests/python/test_layerA_watchlists.py -q` passed locally.
- `uv run python -m py_compile src/python/dsipa/layerA_watchlists.py tests/python/test_layerA_watchlists.py` passed locally.
- Remote tmux run `20260525T044118Z-stage2-watchlists` completed:
  - `uv run python -m pytest tests/python/test_layerA_watchlists.py tests/python/test_risk_rankings.py tests/python/test_trend_uncertainty.py -q` passed on deep-server.
  - `uv run python -m dsipa.layerA_watchlists` generated the watchlist, dominance, and Table S1 outputs.
  - Generated SHA-256 values match `analysis/reports/layerA_watchlists_stage2.sha256`.
- S2.8 local closeout checks passed:
  - `uv run pytest tests/python/test_layerA_watchlists.py tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_tables.py -q`
  - `sha256sum -c analysis/reports/layerA_watchlists_stage2.sha256`
  - `git diff --check`
- Watchlist validation shows all 60 rows have inside-slope bootstrap uncertainty, with category filters matching the risk-ranking definitions.
- The dominance summary shows only the two strongest top brighteners have mean pairwise dominance >0.90 against the other heatmap PAs; mid-rank dominance drops quickly, reinforcing that the lists should be read as uncertainty-aware triage rather than precise rank order.
- Added the canonical ignored artefact folder `artefacts/stage2_layerA_hardening/` plus a repo-visible manifest at `analysis/reports/stage2_layerA_hardening_manifest.md`.
- The artefact folder contains 32 packaged Stage 2 files plus `README.md` and `SHA256SUMS`; `sha256sum -c SHA256SUMS` passed from inside the folder.
- Copied final remote validation build checksums and resource snapshot back to:
  - `analysis/reports/stage2_validation_build.sha256`
  - `analysis/reports/stage2_validation_resource_snapshot.txt`
- Closed A01 and A03 as `done` in `docs/stage1_critique_resolution_matrix.md` after confirming Table 1, Layer A captions, and interpretation notes now explicitly carry denominators, eligibility, zero/floor mass, non-zero subset sizes, and conditional ring/watchlist caveats.
- R03/R07/R08 Stage 2 obligations are satisfied by the tmux run records, package manifest, artefact folder, domain sanity notes, and validation bundle. They remain recurring governance expectations for Stage 3/4 where applicable.
- Updated `docs/stage_overview.md` and `docs/stage2_layerA_hardening_plan.md` to mark Stage 2 as closeout-ready, awaiting user signoff.
- S2.9 validation bundle:
  - Local `git diff --check` passed.
  - Local targeted validation passed: `uv run pytest tests/python/test_trends.py tests/python/test_risk_rankings.py tests/python/test_trend_uncertainty.py tests/python/test_layerA_tables.py tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py tests/python/test_layerA_watchlists.py -q` returned 8 passed, 2 skipped for locally absent ignored national outputs.
  - Local full test smoke passed: `uv run pytest -rs` returned 34 passed, 9 skipped for locally absent ignored national outputs.
  - Local package build passed: `uv build --out-dir /tmp/dsipa-build-stage2`.
  - Remote deep-server tmux validation run `20260525T050953Z-stage2-validation` returned 10/10 targeted tests passed, 41/41 full tests passed, and a successful wheel/sdist build.
  - Remote build checksums:
    - `51b5e2a895a15f5ab7bad0dbe180d611f9e710ad8e0546c21d37ccddb06d5ac8` for `dsipa_nbs-0.1.0-py3-none-any.whl`
    - `6f4ae032061a485cc6ab3b6556c4a994bc4b8367f67b011b3fca1c9c50d23eb0` for `dsipa_nbs-0.1.0.tar.gz`

## Gate status

Stage 2 exit gate passed for the current evidence state. A01-A14 are resolved as `done`, Table 1 and Table S1 are populated from validated evidence, regenerated Layer A figure/table/caption artefacts are packaged, result-review notes are updated, and both local and deep-server validation/build gates passed. Stage 2 is ready for user signoff.

## Proposed next action

If the user accepts Stage 2, proceed to Stage 3 planning: write the detailed Layer B reconciliation plan before doing new Layer B work.

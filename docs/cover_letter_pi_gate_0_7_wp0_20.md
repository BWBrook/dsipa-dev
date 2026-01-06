# PI Cover Letter — Gate 0.7.2 (WP0.15b → WP0.20 package)

Date: 2026-01-06

## Purpose
This package consolidates all work since the last formal PI review (WP0.15b acceptance) through WP0.20. It includes Layer‑B QC hardening, modelling + falsification, manuscript/reproducibility artefacts, Layer‑A bootstrap uncertainty, and the new IBRA‑stratified Layer‑B robustness checks.

## What changed since the last PI review (by WP)
### WP0.15b — Layer‑B QC hardening
- Provider licence ledger derived from `citation.csv` and joined to processed counts.
- Extended QC (coordinate sanity, uncertainty quantiles, provider concentration, clustering, dedup loss).
- Scope coverage + ALAN exposure diagnostics at occurrence locations.

### WP0.16 — Layer‑B modelling + falsification
- Provider‑matched primary analysis (dr368) with two‑part ALAN covariates and spatial blocking.
- Falsification by within‑block ALAN shuffle; full multi‑provider sensitivity run.
- Effect figure + model‑input summary output.

### WP0.17–WP0.18 — Manuscript skeleton + reproducibility audit
- Draft manuscript scaffold with linked artefacts.
- One‑command pipeline + reproducibility audit + schema reference.

### WP0.19 — Layer‑A trend uncertainty
- IBRA‑clustered bootstrap for inside‑PA slopes; forest plot + dominance heatmap.
- DEC‑032 logged (bootstrap design).

### WP0.20 — Layer‑B IBRA robustness (new in this package)
- IBRA‑stratified occurrence summary (counts + ALAN quantiles by IBRA × group × stratum).
- Falsification by shuffling ALAN within IBRA×year.
- IBRA heterogeneity check for log1p(ALAN) intensity term (regions with ≥500 records per class).

## Key artefacts in this ZIP
### Layer‑B QC (WP0.15b)
- `analysis/reports/layerB_ala_license_ledger.md`
- `data/processed/layerB_ala_license_ledger_v0_3_0.csv`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_exposure_qc.json`
- `analysis/reports/layerB_gonogo.md` + `docs/layerB_gonogo.json`

### Layer‑B modelling (WP0.16 + WP0.20 updates)
- `analysis/reports/layerB_modelling_report.md`
- `data/processed/layerB_model_input_summary_v0_3_0.csv`
- `manuscript/figures/fig_layerB_alan_effects.png` (now includes IBRA‑shuffle falsification)
- `manuscript/figures/fig_layerB_ibra_intensity_forest.png`
- `analysis/reports/layerB_ibra_summary.md`
- `data/processed/layerB_ibra_summary_v0_3_0.csv`
- `analysis/reports/layerB_ibra_effects.csv`

### Layer‑A uncertainty (WP0.19)
- `analysis/reports/pa_trend_uncertainty.md`
- `analysis/reports/pa_trend_dominance_matrix.csv`
- `manuscript/figures/fig_layerA_trend_uncertainty_forest.png`
- `manuscript/figures/fig_layerA_trend_dominance.png`

### Manuscript + reproducibility (WP0.17–WP0.18)
- `manuscript/text/manuscript_draft.md`
- `analysis/run_full_pipeline.sh`
- `analysis/build_final_release.py`
- `analysis/reports/reproducibility_audit.md`
- `analysis/reports/figure_inventory.md`
- `analysis/reports/output_schema_reference.md`

### Governance/context
- `docs/decisions.md` (DEC‑032, DEC‑033)
- `docs/interpretation_notes.md`
- `docs/roadmap.md`
- `docs/log/101_layerB_qc_hardening.md`
- `docs/log/102_layerB_modelling.md`
- `docs/log/103_layerA_figure_polish.md`
- `docs/log/104_manuscript_skeleton.md`
- `docs/log/105_reproducibility_audit.md`
- `docs/log/106_layerA_trend_uncertainty.md`
- `docs/log/107_layerB_ibra_robustness.md`
- `data/README.md`

## Summary highlights (new since last review)
- **IBRA falsification**: ALAN shuffle within IBRA×year collapses the log1p(ALAN) coefficient toward zero (AUC ≈ 0.517), while the any_light term remains small but non‑zero; consistent with residual sampling structure rather than strong ecological signal.
- **IBRA heterogeneity**: 11 IBRA regions meet the ≥500‑per‑class threshold; most show a negative intensity term, but a few flip sign, reinforcing a cautious interpretation.
- **IBRA coverage**: IBRA summary is now explicit and quantified by stratum, enabling reviewers to see coverage and censoring at bioregional scale.

## Validation done
- Tests: `uv run pytest`
- Build: `uv run python -m build --sdist --wheel`

## Packaging note
- ZIP excludes files >10 MB to respect bandwidth constraints.
- Large raw rasters and national tables remain excluded; regenerate via pipeline scripts.

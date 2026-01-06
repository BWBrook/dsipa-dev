# PI Cover Letter — Gate 0.7.1 (WP0.15b → WP0.19 package)

Date: 2026-01-06

## Purpose
This package consolidates **all work since the last formal PI review** (WP0.15b acceptance) through WP0.19. It includes Layer‑B QC hardening, Layer‑B modelling outputs, manuscript + reproducibility artefacts, and the new Layer‑A IBRA‑bootstrap uncertainty module.

## What changed since the last PI review (by WP)
### WP0.15b — Layer‑B QC hardening
- Licence/provenance ledger derived from ALA `citation.csv` and joined to processed counts.
- Extended QC: coordinate sanity, uncertainty quantiles, provider concentration, clustering, dedup loss.
- Scope coverage (inside PA / within 10 km) and ALAN exposure QC at occurrence locations.
- Updated go/no‑go and mixed‑licence statements.

### WP0.16 — Layer‑B modelling + falsification
- Provider‑matched primary analysis (dr368) + full multi‑provider sensitivity.
- Two‑part ALAN covariates and spatial blocking with falsification (ALAN shuffle).
- Model input summary + effect figure + exposure/occurrence figures.

### WP0.17–WP0.18 — Manuscript skeleton + reproducibility audit
- Draft manuscript scaffold with linked artefacts.
- One‑command pipeline script + reproducibility audit + schema reference update.

### WP0.19 — Layer‑A trend uncertainty
- Added IBRA7 fetch + snapshot and IBRA‑clustered moving‑block bootstrap for inside slopes.
- New uncertainty outputs + forest plot + dominance heatmap.
- DEC‑032 logged for bootstrap design choices.

## Key artefacts in this ZIP
### Layer‑B QC (WP0.15b)
- `analysis/reports/layerB_ala_license_ledger.md`
- `data/processed/layerB_ala_license_ledger_v0_3_0.csv`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_exposure_qc.json`
- `analysis/reports/layerB_gonogo.md` + `docs/layerB_gonogo.json`

### Layer‑B modelling (WP0.16)
- `analysis/reports/layerB_modelling_report.md`
- `data/processed/layerB_model_input_summary_v0_3_0.csv`
- `manuscript/figures/fig_layerB_alan_effects.png`
- `manuscript/figures/fig_layerB_exposure_summary.png`
- `manuscript/figures/fig_layerB_occurrence_counts.png`
- `manuscript/figures/fig_layerB_occurrence_density.png`

### Manuscript + reproducibility (WP0.17–WP0.18)
- `manuscript/text/manuscript_draft.md`
- `analysis/run_full_pipeline.sh`
- `analysis/build_final_release.py`
- `analysis/reports/reproducibility_audit.md`
- `analysis/reports/figure_inventory.md`
- `analysis/reports/output_schema_reference.md`

### Layer‑A uncertainty (WP0.19)
- `analysis/reports/pa_trend_uncertainty.md`
- `analysis/reports/pa_trend_dominance_matrix.csv`
- `manuscript/figures/fig_layerA_trend_uncertainty_forest.png`
- `manuscript/figures/fig_layerA_trend_dominance.png`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
- `data/raw/ibra_snapshot/ibra_snapshot_20260106.json`

### Governance/context
- `docs/decisions.md` (DEC‑032)
- `docs/interpretation_notes.md` (FIG9/FIG10)
- `docs/roadmap.md`
- `docs/log/101_layerB_qc_hardening.md`
- `docs/log/102_layerB_modelling.md`
- `docs/log/103_layerA_figure_polish.md`
- `docs/log/104_manuscript_skeleton.md`
- `docs/log/105_reproducibility_audit.md`
- `docs/log/106_layerA_trend_uncertainty.md`
- `data/README.md`

## Summary highlights (new since last review)
- **Layer‑B**: Provider‑matched primary inference is now fully executed with falsification; effects are modest and framed conservatively.
- **Uncertainty**: IBRA‑clustered bootstrap CIs show that only a small subset of top PAs separate cleanly; mid‑rank ordering overlaps heavily.
- **Reproducibility**: One‑command pipeline + audit are in place, with schema + figure inventory updated.

## Validation done
- Full tests: `uv run pytest`
- Build: `uv run python -m build --sdist --wheel`

## Packaging note
- ZIP excludes files >10 MB to respect bandwidth constraints.
- Large raw rasters and national tables remain excluded; regenerate via pipeline scripts.

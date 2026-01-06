# Log 107 — Layer B IBRA robustness (WP0.20)

Date: 2026-01-06

Summary:
- Added IBRA‑stratified Layer B summaries (counts + ALAN quantiles by IBRA × group × stratum).
- Implemented IBRA×year ALAN shuffle falsification and IBRA heterogeneity check for the log1p(ALAN) coefficient.
- Updated Layer B effects figure to include IBRA shuffle series and added a heterogeneity forest plot.

Key outputs:
- `data/processed/layerB_ibra_summary_v0_3_0.csv`
- `analysis/reports/layerB_ibra_summary.md`
- `analysis/reports/layerB_ibra_effects.csv`
- `manuscript/figures/fig_layerB_ibra_intensity_forest.png`
- Updated `analysis/reports/layerB_modelling_report.md`
- Updated `manuscript/figures/fig_layerB_alan_effects.png`

Notes:
- IBRA summary uses inside/within_10km scope and year‑specific ALAN sampling, aligned with primary modelling.
- Heterogeneity check is descriptive only (regions with ≥500 records per class; GroupKFold by block).

Next:
- Refresh schema reference + figure inventory.
- Update interpretation notes and reproducibility audit.
- Build WP0.20 artefact folder after clean commit.

Tests:
- `uv run pytest`

Build:
- `uv run python -m build --sdist --wheel`

Artefacts:
- `artefacts/wp0_20_layerB_ibra_robustness/` created (MANIFEST.json shows dirty tree; rerun after commit for clean manifest).

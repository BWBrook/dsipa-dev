# PI Cover Letter — Gate 0.5.1 Review (Layer A metric correction)

Date: 2026-01-02

## Purpose
This note orients the Gate 0.5.1 review. It summarizes the metric corrections, revised outputs, and where to look for evidence that the Layer A story is now publishable.

## What changed since Gate 0.5
- **Trends pivoted to mean radiance** as primary (median retained as robustness).
- **Risk/retention outputs** replace the OLS “vulnerability coefficients” story.
- **Figures revised** to handle missingness and use aggregate edge profiles with valid coverage.
- **Sanity checks stratified** by PA area quartiles and city-distance bands.
- **Schema bumped to v0.2.0**; processed outputs migrated to v0.2.0 filenames.

## Key artefacts to review
- **Trends (mean primary)**:
  - `data/processed/pa_trends_v0_2_0.csv`
  - `analysis/reports/trends_methods_and_sanity.md`
  - `analysis/reports/trends_yearly_means.png`
  - `manuscript/figures/fig_layerA_trend_distribution.png`
  - `artefacts/wp0_11b_trends_mean/`
- **Risk/retention outputs**:
  - `data/processed/pa_risk_rankings_v0_2_0.csv`
  - `analysis/reports/risk_rankings_and_quadrants.md`
  - `manuscript/figures/fig_layerA_retention_quadrant.png`
  - `artefacts/wp0_12b_risk_retention/`
- **Sanity suite upgrade**:
  - `analysis/reports/layerA_sanity_dashboard.md`
  - `artefacts/wp0_10b_layerA_sanity/`
- **Figure set revisions**:
  - `manuscript/figures/fig_layerA_baseline_map.png`
  - `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`
  - `manuscript/figures/fig_layerA_trend_distribution.png`
  - `manuscript/figures/fig_layerA_retention_quadrant.png`
  - `analysis/reports/figure_inventory.md`
  - `artefacts/wp0_13b_layerA_figures/`

## Notes on interpretability
- **Mean-trend slopes** now show a visible non-zero tail; median trends remain mostly zero (documented in `analysis/reports/trends_methods_and_sanity.md`).
- **Aggregate edge profiles** restrict to PAs with complete ring coverage; n is reported.
- **Baseline map** shows missing PAs in grey to avoid misinterpreting missing as zero.

## What I need from you
- Confirm that the revised Layer A story is acceptable for manuscript drafting.
- Decide whether the risk/retention table should be trimmed further (top 20 vs 50).
- Green-light (or decline) the move to Layer B data acquisition (WP0.15).

## Validation done
- Tests: `uv run pytest` (21 passed)
- Build: `uv run python -m build` (sdist + wheel)

## Packaging note
- The review ZIP includes the processed PA geometries GPKG (`data/processed/pa_geometries_v0_2_0.gpkg`) as requested.
- Large rasters under `data/raw/nightlights_zenodo_v0_4/` remain excluded.

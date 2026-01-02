# 090 Layer A metric correction + figure polish (Milestone 0.5.1)

Date: 2026-01-02

## Summary
- Added Milestone 0.5.1 WPs (0.10b–0.13b) and paused Layer B acquisition pending PI gate.
- Upgraded sanity dashboard with stratified inside-vs-buffer checks (area quartiles + city-distance bands).
- Recomputed trends using **mean** radiance as primary metric; median retained as robustness.
- Replaced OLS vulnerability model with risk/retention rankings + quadrant plot.
- Revised figure set: baseline map handles missingness; edge profiles use aggregate + example; trend distribution reflects mean slopes.
- Bumped schema to v0.2.0 and migrated processed outputs to v0.2.0 filenames.

## Outputs & artefacts
- `analysis/reports/layerA_sanity_dashboard.md`, `artefacts/wp0_10b_layerA_sanity/`
- `data/processed/pa_trends_v0_2_0.csv`, `analysis/reports/trends_methods_and_sanity.md`, `analysis/reports/trends_yearly_means.png`, `artefacts/wp0_11b_trends_mean/`
- `data/processed/pa_risk_rankings_v0_2_0.csv`, `analysis/reports/risk_rankings_and_quadrants.md`, `manuscript/figures/fig_layerA_retention_quadrant.png`, `artefacts/wp0_12b_risk_retention/`
- `manuscript/figures/fig_layerA_baseline_map.png`, `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`, `manuscript/figures/fig_layerA_trend_distribution.png`, `artefacts/wp0_13b_layerA_figures/`

## Notes
- Mean-trend slopes still include a high fraction of zeros, but the non-zero tail is now visible and interpretable.
- Aggregate edge profiles are restricted to PAs with complete ring coverage; example PA chosen deterministically.

## Tests and builds
- Tests: `uv run pytest` (21 passed)
- Build: `uv run python -m build` (sdist + wheel)

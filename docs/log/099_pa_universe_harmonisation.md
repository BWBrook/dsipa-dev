# 099 PA universe harmonisation (JBT/EXT)

Date: 2026-01-04

## Summary
- Added JBT + EXT to default state list for statewise runs.
- Ran statewise Layer A for JBT/EXT and merged with existing states.
- Regenerated national Layer A reports/figures so denominators align (11133 across geometry/radiance/rings).

## Outputs & artefacts
- `analysis/state_runs/JBT/*`, `analysis/state_runs/EXT/*`
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `data/processed/pa_trends_v0_3_0.csv`
- `data/processed/pa_risk_rankings_v0_3_0.csv`
- `analysis/reports/national_layerA_coverage_and_sanity.md`
- `analysis/reports/layerA_sanity_dashboard.md`
- `analysis/reports/trends_methods_and_sanity.md`
- `analysis/reports/risk_rankings_and_quadrants.md`
- `manuscript/figures/fig_layerA_baseline_map.png`

## Sanity notes
- PA counts now match across core tables:
  - `pa_geometries`: 11,133
  - `pa_radiance_buffers`: 11,133
  - `pa_edge_profiles`: 11,133

## Tests
- `uv run pytest`

# 095 Layer A buffer validity + censoring-aware metrics (Milestone 0.5.2 prep)

Date: 2026-01-02

## Summary
- Added buffer validity descriptors (raw vs land vs land_unprotected) using Natural Earth landmask.
- Introduced censoring-aware exposure metrics (frac_gt0, p95) for inside/buffer/ring summaries and trends.
- Bumped schema to v0.3.0 and updated downstream tables/plots to include buffer_type + new metrics.
- Added cached geometry unions + statewise runner to manage national runtime.

## Outputs & artefacts
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`, `analysis/reports/national_layerA_coverage_and_sanity.md`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `analysis/reports/schema_reference_v0_3_0.md`

## Notes
- Buffer validity tables now track land fraction, protected overlap, and effective land area for each buffer.
- Censoring-aware metrics are intended to reduce zero-floor dominance at 500 m resolution.

## Tests and builds
- Tests: `uv run pytest`
- Build: `uv run python -m build`

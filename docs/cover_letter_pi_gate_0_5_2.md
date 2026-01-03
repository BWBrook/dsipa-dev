# PI Cover Letter — Gate 0.5.2 Review (Layer A validity + censoring)

Date: 2026-01-03

## Purpose
This note orients the Gate 0.5.2 review. It summarizes the validity/censoring fixes and points to the evidence needed to decide whether Layer A is now defensible enough to revisit Layer B.

## What changed since Gate 0.5.1
- **Buffer validity decomposition**: raw vs land vs land_unprotected buffers, with land_fraction and protected-overlap diagnostics.
- **Censoring-aware exposure metrics**: added `frac_gt0` and `p95` to inside/buffer summaries + trends.
- **Category-safe risk/retention outputs**: separate ranked lists for inside brightening, buffer brightening, internalisation, and external pressure.
- **Figure revisions**: baseline map now shows eligibility vs radiance; edge figure now shows ring feasibility + conditional profile.
- **Schema bumped to v0.3.0** with updated outputs and schema reference.

## Key artefacts to review
- **Buffer validity + national tables**:
  - `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
  - `data/processed/pa_buffer_validity_v0_3_0.csv`
  - `data/processed/pa_edge_profiles_national_v0_3_0.csv`
  - `analysis/reports/national_layerA_coverage_and_sanity.md`
  - `analysis/reports/output_schema_reference.md`
- **Sanity suite (censoring + stratified invariants)**:
  - `analysis/reports/layerA_sanity_dashboard.md`
  - `artefacts/wp0_10c_layerA_sanity/`
- **Trends + censoring-aware metrics**:
  - `data/processed/pa_trends_v0_3_0.csv`
  - `analysis/reports/trends_methods_and_sanity.md`
  - `analysis/reports/trends_yearly_means.png`
  - `manuscript/figures/fig_layerA_trend_distribution.png`
  - `artefacts/wp0_11c_trends_censoring/`
- **Risk/retention (category-safe)**:
  - `data/processed/pa_risk_rankings_v0_3_0.csv`
  - `analysis/reports/risk_rankings_and_quadrants.md`
  - `manuscript/figures/fig_layerA_retention_quadrant.png`
  - `artefacts/wp0_12c_risk_retention/`
- **Figure set revision**:
  - `manuscript/figures/fig_layerA_baseline_map.png`
  - `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`
  - `analysis/reports/figure_inventory.md`
  - `artefacts/wp0_13c_layerA_figures/`

## Notes on interpretability
- Eligibility remains limited (4,422/11,112 PAs with >=10 valid pixels in 2024; zero-mass ≈ 86.9% among eligible).
- Ring feasibility is low (complete rings ≈ 3.4% in 2024), so edge profiles are explicitly conditional.
- The buffer validity tables allow us to quantify how much “outside” is land vs protected overlap; retention narratives now use `land_unprotected`.

## What I need from you
- Confirm whether the Layer A story is now sufficiently defensible to re-open Layer B.
- Any guidance on how aggressively to de-emphasize the ring/penetration story given low feasibility.

## Validation done
- Tests: `uv run pytest` (25 passed)
- Build: `uv run python -m build` (sdist + wheel)

## Packaging note
- The review ZIP includes `data/processed/pa_geometries_v0_3_0.gpkg` and all updated artefacts.
- Large rasters under `data/raw/nightlights_zenodo_v0_4/` and the per‑state caches under `analysis/state_runs/` are excluded to keep the archive manageable.

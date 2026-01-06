# PI Cover Letter — Gate 0.7.1 (WP0.19 Layer A trend uncertainty)

Date: 2026-01-06

## Purpose
This note summarises the IBRA‑clustered bootstrap added to quantify uncertainty on Layer‑A inside‑PA slopes before further synthesis.

## What changed since the last PI package
- Added IBRA7 region fetch + snapshot for bioregional clustering (`src/python/dsipa/ibra.py`).
- Implemented IBRA‑clustered moving‑block bootstrap for inside mean‑radiance slopes (`src/python/dsipa/trend_uncertainty.py`).
- Generated new uncertainty outputs + figures (forest plot + dominance heatmap).
- Updated schema reference, data inventory, roadmap, and interpretation notes to document WP0.19.

## Key artefacts to review
- `analysis/reports/pa_trend_uncertainty.md`
- `analysis/reports/pa_trend_dominance_matrix.csv`
- `manuscript/figures/fig_layerA_trend_uncertainty_forest.png`
- `manuscript/figures/fig_layerA_trend_dominance.png`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
- `docs/decisions.md` (DEC‑032)
- `docs/interpretation_notes.md` (FIG9/FIG10 entries)

## Summary highlights
- IBRA coverage: 11,098 / 11,133 PAs assigned (missing 35, likely external territories/offshore).
- Multi‑IBRA overlap fraction: ~8.3%; dominant IBRA share median = 1.00.
- Bootstrap summaries for 4,426 PAs (39.9%), aligned with inside eligibility + min‑year thresholds.
- Dominance heatmap shows clear separation for only a small subset; mid‑rank slopes overlap heavily (as expected with spatial+temporal resampling).

## Decisions logged
- DEC‑032: Use IBRA regions as spatial resampling clusters with moving‑block length = 3 years and n_boot = 300.

## Validation done
- Tests: `uv run pytest tests/python/test_trend_uncertainty.py`

## Packaging note
- Review ZIP excludes files >10 MB to respect bandwidth constraints.
- Large national tables and raw rasters remain excluded; use pipeline to regenerate.

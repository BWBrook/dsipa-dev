# Log 106 — Layer A trend uncertainty (IBRA bootstrap)

Date: 2026-01-06

Summary:
- Added IBRA7 regions fetcher and snapshot (ArcGIS REST service) for bioregional clustering.
- Implemented IBRA-clustered moving-block bootstrap for inside mean-radiance slopes (block_len=3, n_boot=300, seed=42).
- Generated new outputs + artefact folder:
  - `data/processed/pa_ibra_assignment_v0_3_0.csv`
  - `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
  - `analysis/reports/pa_trend_uncertainty.md`
  - `analysis/reports/pa_trend_dominance_matrix.csv`
  - `manuscript/figures/fig_layerA_trend_uncertainty_forest.png`
  - `manuscript/figures/fig_layerA_trend_dominance.png`
  - `artefacts/wp0_19_layerA_trend_uncertainty/`

Observations:
- IBRA assignment covers 11,098 PAs; ~35 PAs are outside IBRA coverage (likely external territories/offshore), noted for interpretation.
- Multi-IBRA overlaps are modest (~8.3% of PAs; dominant share median = 1.00).
- Bootstrap summaries available for 4,426 PAs (39.9%), consistent with inside eligibility and min-year thresholds.

Next:
- Update schema reference + tests, data inventory, interpretation notes, reproducibility audit, and roadmap checkboxes.

Tests:
- `uv run pytest tests/python/test_trend_uncertainty.py`

# 065_layerA_sanity log

- Date/time (UTC): 2026-01-01 09:59 UTC
- Objectives: run Layer A sanity dashboard with anchors, invariants, and sensitivity checks (WP0.10).
- Actions taken:
  - Generated `analysis/reports/layerA_sanity_dashboard.md`.
  - Produced mean-vs-median sensitivity plot.
  - Wrote canonical artefact folder.
- Outputs:
  - `analysis/reports/layerA_sanity_dashboard.md`
  - `analysis/reports/layerA_sensitivity_mean_vs_median.png`
  - `artefacts/wp0_10_layerA_sanity/`
- Diagnostics / sanity checks:
  - Invariants pass; mean/median strongly correlated (r ~0.94).
  - Only ~40% of inside zones meet 10-pixel threshold; ~20% meet 50-pixel threshold.
  - Ring missingness remains substantial for outer bins.
- Next steps:
  - Proceed to trend estimation (WP0.11).

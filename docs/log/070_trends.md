# 070_trends log

- Date/time (UTC): 2026-01-01 09:59 UTC
- Objectives: compute trends and retention indices (WP0.11).
- Actions taken:
  - Implemented Theil-Sen trend estimation on median radiance.
  - Generated trend table, methods/sanity report, and trend distribution figure.
  - Wrote canonical artefact folder.
- Outputs:
  - `data/processed/pa_trends_v0_1_0.csv`
  - `analysis/reports/trends_methods_and_sanity.md`
  - `manuscript/figures/fig_layerA_trend_distribution.png`
  - `artefacts/wp0_11_trends/`
- Diagnostics / sanity checks:
  - Mean inside median radiance increases steadily from 2013–2024.
  - ~4,426 PAs meet the minimum valid-year threshold for trends.
- Next steps:
  - Run vulnerability model (WP0.12).

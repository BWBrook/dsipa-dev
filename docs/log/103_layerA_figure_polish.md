# 103 Layer A figure polish (post-WP0.16)

Date: 2026-01-05

## Summary
- Adjusted Layer A figure aesthetics per manuscript feedback.
  - Baseline map panels now share identical bounds/aspect; legend/colorbar reduced.
  - Edge-profile panel now plots share of PAs with any light (frac_gt0 > 0) to avoid flat median line.
  - Retention quadrant uses lighter colormap with boxed labels for readability.
  - Trend distribution x-axis clipped to 1st–99th percentiles (left panel) with clipping noted in title.
 - Added Layer B figures for exposure summary, occurrence counts (year/state), and spatial density.

## Outputs regenerated
- `manuscript/figures/fig_layerA_baseline_map.png`
- `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`
- `manuscript/figures/fig_layerA_retention_quadrant.png`
- `manuscript/figures/fig_layerA_trend_distribution.png`
- `manuscript/figures/fig_layerB_exposure_summary.png`
- `manuscript/figures/fig_layerB_occurrence_counts.png`
- `manuscript/figures/fig_layerB_occurrence_density.png`
- `analysis/reports/figure_inventory.md`

## Commands
- `uv run python -m dsipa.figures_layerA --skip-artefact`
- `uv run python -m dsipa.trends --skip-artefact`
- `uv run python -m dsipa.vulnerability_model --skip-artefact`
- `uv run python -m dsipa.figures_layerB`
- `uv run python -m dsipa.figure_inventory`

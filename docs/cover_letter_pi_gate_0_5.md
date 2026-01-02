# PI Cover Letter — Gate 0.5 Review (Layer A complete; Layer B decision)

Date: 2026-01-02

## Purpose
This note provides a short primer for the Gate 0.5 review so you can quickly orient to what is complete, what evidence exists, and what is next.

## What is complete
- **Layer A (national)**: WP0.9–WP0.13 delivered national tables, sanity suite, robust trends, vulnerability model, and paper-ready figures.
- **Layer B decision**: WP0.14 is complete; go/no-go criteria, focal taxa, negative controls, and bias strategy are formalised.

## Key deliverables to review
- **National tables**: `data/processed/pa_radiance_buffers_national_v0_1_0.csv`, `data/processed/pa_edge_profiles_national_v0_1_0.csv`, `data/processed/pa_trends_v0_1_0.csv`, `data/processed/pa_risk_rankings_v0_1_0.csv`.
- **Core reports**: `analysis/reports/national_layerA_coverage_and_sanity.md`, `analysis/reports/layerA_sanity_dashboard.md`, `analysis/reports/trends_methods_and_sanity.md`, `analysis/reports/vulnerability_model_report.md`.
- **Figures**: `manuscript/figures/fig_layerA_baseline_map.png`, `manuscript/figures/fig_layerA_edge_profiles_examples.png`, `manuscript/figures/fig_layerA_trend_distribution.png`, `manuscript/figures/fig_layerA_vulnerability_coefficients.png`.
- **Layer B decision**: `analysis/reports/layerB_gonogo.md` (generated from `docs/layerB_gonogo.json`).

## Key decisions (most relevant)
- **Night-lights source**: Zenodo DOI 10.5281/zenodo.17294744 (annual VIIRS averages), with metadata-based scaling (scale=10 for 2022–2024). See DEC-003.
- **Trend estimation**: Theil-Sen on median radiance; require >=8 valid years. See DEC-007.
- **Layer B go/no-go**: Conditional-go with microbats as focal taxa; diurnal birds + diurnal reptiles as negative controls; target-group background + spatial blocking + falsification checks. See DEC-009 and `docs/layerB_gonogo.json`.
- **Micro-area handling**: Keep `min_valid_pixels=10` for baseline; treat area <0.01 km2 and median valid pixels <10 as sensitivity-only filters. See DEC-011.

## Validation done
- Unit tests: `uv run pytest` (all tests passing).
- Build artefacts: `uv run python -m build` (sdist + wheel).
- Sanity review: coverage, anchors, and distributions checked in the reports above.

## Artefacts
Canonical artefact folders with manifests:
- `artefacts/wp0_9_layerA_national/`
- `artefacts/wp0_10_layerA_sanity/`
- `artefacts/wp0_11_trends/`
- `artefacts/wp0_12_vulnerability_model/`
- `artefacts/wp0_13_layerA_figures/`
- `artefacts/wp0_14_layerB_gonogo/`

## Next step (pending PI direction)
- **WP0.15**: Acquire ALA occurrence data for the Layer B focal taxa and negative controls, apply filters, and record provenance.
- **WP0.16**: Bias-controlled modelling + falsification checks, only if go/no-go criteria are met.

## Notes
- Large rasters remain in `data/raw/nightlights_zenodo_v0_4/` and are excluded from the review zip.
- All decisions and logs are traceable under `docs/decisions.md` and `docs/log/`.

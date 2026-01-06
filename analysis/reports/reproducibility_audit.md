# Reproducibility audit (WP0.18)

Generated: 2026-01-06

## Repo state
- Git commit: `e6ff0d8e967332f393a5296d9f33e9d404693360`
- Working tree: dirty (WP0.17/WP0.18 docs + WP0.19 trend-uncertainty updates pending commit)

## One-command full rerun
Full pipeline script (Layer A + Layer B + tests + build):

```bash
analysis/run_full_pipeline.sh
```

Key environment variables:
- `DSIPA_REPO_ROOT` (optional): redirect outputs to a clean directory.
- `DSIPA_WORKERS` (optional): number of workers for statewise Layer A (default 6).
- `DSIPA_STATES` (optional): comma-separated state list (default includes ACT, NSW, NT, QLD, SA, TAS, VIC, WA, JBT, EXT).
- `ALA_DOWNLOAD_EMAIL` + `ALA_DOWNLOAD_REASON` (required for Layer B downloads), or set `DSIPA_SKIP_LAYERB=1` to skip Layer B.

## Expected runtime class (order-of-magnitude)
- Layer A national statewise run (buffers + rings, 2013–2024): **~1–3 days** on 6 cores with cached unions and local nightlights.
- Layer A trend/vulnerability/figures: **minutes to ~1 hour**.
- Layer A trend uncertainty (IBRA bootstrap): **~5–10 minutes** (n_boot=300).
- Layer B downloads + QC: **minutes** (network-bound).
- Layer B modelling (provider-matched + sensitivity): **~1 hour**.
- Tests + build: **<5 minutes**.

## Verification checklist
If rerunning the pipeline, verify outputs using checksums (small, tracked artefacts):

```
sha256sum \
  manuscript/figures/fig_layerA_baseline_map.png \
  manuscript/figures/fig_layerA_trend_distribution.png \
  manuscript/figures/fig_layerA_retention_quadrant.png \
  manuscript/figures/fig_layerA_edge_profiles_aggregate.png \
  manuscript/figures/fig_layerA_trend_uncertainty_forest.png \
  manuscript/figures/fig_layerA_trend_dominance.png \
  manuscript/figures/fig_layerB_alan_effects.png \
  manuscript/figures/fig_layerB_exposure_summary.png \
  manuscript/figures/fig_layerB_occurrence_counts.png \
  manuscript/figures/fig_layerB_occurrence_density.png \
  analysis/reports/pa_trend_uncertainty.md \
  analysis/reports/pa_trend_dominance_matrix.csv \
  analysis/reports/layerB_modelling_report.md \
  analysis/reports/figure_inventory.md \
  analysis/reports/risk_rankings_and_quadrants.md \
  analysis/reports/trends_methods_and_sanity.md \
  data/processed/layerB_model_input_summary_v0_3_0.csv \
  analysis/reports/output_schema_reference.md
```

Expected hashes (sha256):
- `manuscript/figures/fig_layerA_baseline_map.png`: `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`
- `manuscript/figures/fig_layerA_trend_distribution.png`: `8b662196b40609c6978bf191c59e708478f1942bc1734a80ac7f360b25dec97e`
- `manuscript/figures/fig_layerA_retention_quadrant.png`: `f80cfd0e40874e9a34e2b4bd6c4a16adfc20302ed759cd1ab4f8d782a0827df2`
- `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`: `e098405d6c03c53d97dc53c3b1a43ed04bd33c4a56bdd9fd2fac43904fc6339e`
- `manuscript/figures/fig_layerA_trend_uncertainty_forest.png`: `9a2fca733e46f401c32c0606d50d54d1089e4f24f83fd86d71bd38f638a67f26`
- `manuscript/figures/fig_layerA_trend_dominance.png`: `de53c292ddd22278e16da374c0166ced7f37ce2510fa5ad410ec325711eeee1d`
- `manuscript/figures/fig_layerB_alan_effects.png`: `f923b99b722975d0095d766a8dd953ae4df13fca1b80b0a1f95dfd0a75c5410c`
- `manuscript/figures/fig_layerB_exposure_summary.png`: `c5fa067e759fe0f3dcb5b837ef5b888c7636f65723c14335f74f9069b48c028e`
- `manuscript/figures/fig_layerB_occurrence_counts.png`: `fefd4a827ac5af543a2f184624dbfe385591c185748550aefcbad909f5ed3025`
- `manuscript/figures/fig_layerB_occurrence_density.png`: `e15d7ce82a6748f5be23c63c873406240c85b1df9dc0ce36039102fb40c43c16`
- `analysis/reports/pa_trend_uncertainty.md`: `8b0822635086a2eb804467105c84963fc3b79d9a882ceb5dec8d8f001da8ad06`
- `analysis/reports/pa_trend_dominance_matrix.csv`: `ce322c5110ad47336c001b521322f64c745c016e8af93909df8aa3f9e603cfb8`
- `analysis/reports/layerB_modelling_report.md`: `eb8e629d9455835bf41d2652126e278d0bcf6e87d63ec84caafc97899f404c1d`
- `analysis/reports/figure_inventory.md`: `68e73ae9a73a82de5126c8fe142c8f9464c6deda05b13d6c869fc56424ca68a8`
- `analysis/reports/risk_rankings_and_quadrants.md`: `271a6a8580bfcd072ad42b44b9382346dcb74ca9225b68d5ea1eb3d04f2ca316`
- `analysis/reports/trends_methods_and_sanity.md`: `6934a40b182750a74ba4c04cb242f1f67967a55f723b64177d410c2303084d2f`
- `data/processed/layerB_model_input_summary_v0_3_0.csv`: `f42e9fea29dea812f54e4e9a02fafa3c7d6382e499d20e31b267b84be9346575`
- `analysis/reports/output_schema_reference.md`: `eea1b6b019a67aebe12a6596a74e64202fefa0f4a4b7230a7cb3186d9634812f`

For large, untracked national tables (Layer A), verify via summary stats and row counts reported in:
- `analysis/reports/national_layerA_coverage_and_sanity.md`
- `analysis/reports/trends_methods_and_sanity.md`

## Tests and builds
- `uv run pytest`
- `uv run python -m build --sdist --wheel`

## Schema versioning
- Current schema version: `v0.3.0`.
- Output schema reference: `analysis/reports/output_schema_reference.md`.

## Final release artefact
- Folder: `artefacts/final_release_20260105/`
- Manifest records current git state (dirty due to uncommitted WP0.17/WP0.18 docs); a clean manifest requires committing those files.

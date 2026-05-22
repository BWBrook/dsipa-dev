# Reproducibility audit

Generated: 2026-05-14 07:28 UTC

## Repo state
- Git commit: `f73156272104ed16b0506617fc423e5c6478f50e`
- Branch: `main`
- Working tree: dirty
- Evidence host: `deep-server`

## Evidence reconciliation
- Report: `analysis/reports/evidence_reconciliation.md`
- JSON: `analysis/reports/evidence_reconciliation.json`
- Expected files: 38
- Present files: 38
- Checksum-verified files: 38
- Missing required files: 0
- Checksum mismatches: 0
- Artefact manifests found: 28

## One-command full rerun
Full pipeline script (Layer A + Layer B + tests + build):

```bash
analysis/run_full_pipeline.sh
```

Key environment variables:
- `DSIPA_REPO_ROOT` (optional): redirect outputs to a clean directory.
- `DSIPA_WORKERS` (optional): number of workers for statewise Layer A.
- `DSIPA_STATES` (optional): comma-separated state list.
- `ALA_DOWNLOAD_EMAIL` + `ALA_DOWNLOAD_REASON` (required for Layer B downloads), or set `DSIPA_SKIP_LAYERB=1` to skip Layer B.

## Expected runtime class
- Layer A national statewise run (buffers + rings, 2013-2024): multi-hour to multi-day, depending on cache state and worker count.
- Layer A trend/vulnerability/figures: minutes to about 1 hour.
- Layer A trend uncertainty (IBRA bootstrap): about 5-10 minutes at n_boot=300.
- Layer B downloads + QC: minutes, usually network-bound.
- Layer B modelling + IBRA summary/falsification: about 1-2 hours.
- Tests + build: under 5 minutes on the control plane.

## Deep-server harness
Use tmux for remote runs so laptop sleep/shutdown does not interrupt work:

```bash
analysis/deep_server_tmux_run.sh --mode evidence
analysis/deep_server_tmux_run.sh --mode full --workers 12
```

Default remote run roots:
- `/home/bwbrook/papers/dsipa-dev` for the current evidence snapshot.
- `/data/codex/scratch/dsipa/<RUN_ID>` for logs and run-local files.
- `/data/codex/artifacts/dsipa/<RUN_ID>` for durable copied artefacts.

## Verification checklist
Verify the reconciled evidence snapshot with pinned SHA-256 values:

```bash
sha256sum data/processed/pa_geometries_v0_3_0.csv \
  data/processed/pa_geometries_v0_3_0.gpkg \
  data/processed/pa_radiance_buffers_national_v0_3_0.csv \
  data/processed/pa_edge_profiles_national_v0_3_0.csv \
  data/processed/pa_buffer_validity_v0_3_0.csv \
  data/processed/pa_trends_v0_3_0.csv \
  data/processed/pa_risk_rankings_v0_3_0.csv \
  data/processed/pa_ibra_assignment_v0_3_0.csv \
  data/processed/pa_trend_bootstrap_summary_v0_3_0.csv \
  data/processed/layerB_occurrence_summary_v0_3_0.csv \
  data/processed/layerB_ala_license_ledger_v0_3_0.csv \
  data/processed/layerB_model_input_summary_v0_3_0.csv \
  data/processed/layerB_ibra_summary_v0_3_0.csv \
  data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz \
  data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz \
  analysis/reports/national_layerA_coverage_and_sanity.md \
  analysis/reports/trends_methods_and_sanity.md \
  analysis/reports/risk_rankings_and_quadrants.md \
  analysis/reports/pa_trend_uncertainty.md \
  analysis/reports/pa_trend_dominance_matrix.csv \
  analysis/reports/layerB_modelling_report.md \
  analysis/reports/layerB_qc_extended.md \
  analysis/reports/layerB_scope_coverage.md \
  analysis/reports/layerB_ibra_summary.md \
  analysis/reports/layerB_ibra_effects.csv \
  analysis/reports/figure_inventory.md \
  analysis/reports/output_schema_reference.md \
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
  manuscript/figures/fig_layerB_ibra_intensity_forest.png
```

Expected hashes (sha256):
- `data/processed/pa_geometries_v0_3_0.csv`: `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b`
- `data/processed/pa_geometries_v0_3_0.gpkg`: `0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11`
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`: `493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`: `9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888`
- `data/processed/pa_buffer_validity_v0_3_0.csv`: `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25`
- `data/processed/pa_trends_v0_3_0.csv`: `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f`
- `data/processed/pa_risk_rankings_v0_3_0.csv`: `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`: `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`: `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920`
- `data/processed/layerB_occurrence_summary_v0_3_0.csv`: `ec7746a882675b4955b7d455cddae2f9851bde55d16900cf6b32979346f77474`
- `data/processed/layerB_ala_license_ledger_v0_3_0.csv`: `a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0`
- `data/processed/layerB_model_input_summary_v0_3_0.csv`: `f42e9fea29dea812f54e4e9a02fafa3c7d6382e499d20e31b267b84be9346575`
- `data/processed/layerB_ibra_summary_v0_3_0.csv`: `ed117aadd0c700c8dd0c7180714112fd212567f4b1ec56d0c8464f2e77d00a0d`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`: `19e87ebda5e61cd0eb08a2824f85d63fe5dfc870527cd0ac9f21c00e38f1c007`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`: `b4de14ec88af0a34c82553078d3a8c9b01c664413fde0262fe050fefed6e12ba`
- `analysis/reports/national_layerA_coverage_and_sanity.md`: `1f9e23239f88750c4ee1b63b46632af7822a30a6ecd577f7a8c0c0ebb5cffcd9`
- `analysis/reports/trends_methods_and_sanity.md`: `6934a40b182750a74ba4c04cb242f1f67967a55f723b64177d410c2303084d2f`
- `analysis/reports/risk_rankings_and_quadrants.md`: `271a6a8580bfcd072ad42b44b9382346dcb74ca9225b68d5ea1eb3d04f2ca316`
- `analysis/reports/pa_trend_uncertainty.md`: `8b0822635086a2eb804467105c84963fc3b79d9a882ceb5dec8d8f001da8ad06`
- `analysis/reports/pa_trend_dominance_matrix.csv`: `ce322c5110ad47336c001b521322f64c745c016e8af93909df8aa3f9e603cfb8`
- `analysis/reports/layerB_modelling_report.md`: `77381d7108b18146dd28ff194b9e31dcf45908e6dc355d83908ebb1cde8cc63a`
- `analysis/reports/layerB_qc_extended.md`: `1673e75bf596f31bda178ac0908bd1dfa258d75b0d9da98451e98b6eae7e2fbb`
- `analysis/reports/layerB_scope_coverage.md`: `62e0f8beaea79cd3186cd39a978bade5c3998d46e4b693a19efa77a95a0a1c3a`
- `analysis/reports/layerB_ibra_summary.md`: `e09e152899605583cd7c3ce16b1a778bc5a107583d0e719609fd37c2e2d50b57`
- `analysis/reports/layerB_ibra_effects.csv`: `2b9b14e678cb8e3819e50f26845a130ab2e4444dc0bedcf041f61a572d7454b1`
- `analysis/reports/figure_inventory.md`: `4748110e45e40fda53129fb8370754ad64adf8e4fb7b344db9e45321370ebc1d`
- `analysis/reports/output_schema_reference.md`: `7d2b00aa0a74b4b738424fce6ae4288cd6f15362007733a1349e5c97b8d79c8f`
- `manuscript/figures/fig_layerA_baseline_map.png`: `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`
- `manuscript/figures/fig_layerA_trend_distribution.png`: `8b662196b40609c6978bf191c59e708478f1942bc1734a80ac7f360b25dec97e`
- `manuscript/figures/fig_layerA_retention_quadrant.png`: `f80cfd0e40874e9a34e2b4bd6c4a16adfc20302ed759cd1ab4f8d782a0827df2`
- `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`: `e098405d6c03c53d97dc53c3b1a43ed04bd33c4a56bdd9fd2fac43904fc6339e`
- `manuscript/figures/fig_layerA_trend_uncertainty_forest.png`: `9a2fca733e46f401c32c0606d50d54d1089e4f24f83fd86d71bd38f638a67f26`
- `manuscript/figures/fig_layerA_trend_dominance.png`: `de53c292ddd22278e16da374c0166ced7f37ce2510fa5ad410ec325711eeee1d`
- `manuscript/figures/fig_layerB_alan_effects.png`: `6a01c40b070aaaae71387963a0b0326ef4ee32336ead43b21f2c7af2f85f58f8`
- `manuscript/figures/fig_layerB_exposure_summary.png`: `c5fa067e759fe0f3dcb5b837ef5b888c7636f65723c14335f74f9069b48c028e`
- `manuscript/figures/fig_layerB_occurrence_counts.png`: `fefd4a827ac5af543a2f184624dbfe385591c185748550aefcbad909f5ed3025`
- `manuscript/figures/fig_layerB_occurrence_density.png`: `e15d7ce82a6748f5be23c63c873406240c85b1df9dc0ce36039102fb40c43c16`
- `manuscript/figures/fig_layerB_ibra_intensity_forest.png`: `eb80460408620d61e144b572d9dd9d89e4a15aa143003d85e37ca922c99eda40`

Checksum notes:
- `data/processed/layerB_ala_license_ledger_v0_3_0.csv`: Checksum is computed after CRLF-to-LF normalization because ALA citation fields contain embedded line endings that vary across checkouts.

## Tests and builds
- `uv run pytest`
- `uv build`

## Schema versioning
- Current schema version: `v0.3.0`.
- Output schema reference: `analysis/reports/output_schema_reference.md`.

## Release caveat
Large derived tables and raw occurrence downloads remain outside git. Before paper release, upload the required large files and a checksum manifest to the external archive, then record the DOI/access date in `data/README.md`.

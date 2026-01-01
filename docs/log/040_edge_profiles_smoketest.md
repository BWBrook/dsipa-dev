# 040_edge_profiles_smoketest log

- Date/time (UTC): 2026-01-01 07:50 UTC
- Objectives: compute smoke-test distance-to-edge ring radiance profiles.
- Actions taken:
  - Generated ring geometries from triad PAs (EPSG:3577) and reprojected for raster sampling.
  - Computed ring-level radiance stats for 2013/2018/2024.
  - Produced edge profile plot + report and canonical artefact folder.
- Outputs:
  - `data/processed/pa_edge_profiles_smoketest_v0_1_0.csv`
  - `analysis/reports/smoketest_edge_profiles.md`
  - `analysis/reports/smoketest_edge_profiles.png`
  - `artefacts/wp0_7_edge_profiles_smoketest/`
- Diagnostics / sanity checks:
  - Ring bins ordered and complete (0–1, 1–5, 5–10 km).
  - Ring index 2 has zero valid pixels for all triad PAs; likely due to small PA sizes (documented in report).
  - `uv run pytest` (14 passed).
  - `uv run python -m build` (sdist + wheel).
- Next steps:
  - Proceed to WP0.8 structured outputs + schema_version + regression tests.

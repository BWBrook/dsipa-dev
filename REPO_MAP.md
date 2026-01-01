# Repo map (snapshot)

Generated: 2026-01-01 08:00:51 UTC
Root: /home/bwbrook/git/dsipa-dev
Depth: 3

```
├── analysis/
│   ├── notebooks/
│   │   └── .gitkeep
│   └── reports/
│       ├── triad_qa_maps/
│       │   ├── NSW_N0856_peri_urban.png
│       │   ├── QLD_0117LZI001_remote.png
│       │   ├── README.md
│       │   └── TAS_50483_urban_edge.png
│       ├── .gitkeep
│       ├── data_inventory.md
│       ├── output_schema_reference.md
│       ├── pa_geometry_qc.md
│       ├── smoke_test_triad_definition.md
│       ├── smoketest_buffers_sanity.md
│       ├── smoketest_buffers_summary.png
│       ├── smoketest_edge_profiles.md
│       ├── smoketest_edge_profiles.png
│       └── triad_qa_manifest.json
├── artefacts/
│   ├── wp0_1_bootstrap/
│   │   ├── MANIFEST.json
│   │   ├── placeholder.txt
│   │   └── README.txt
│   ├── wp0_3_data_sources/
│   │   ├── data_inventory.md
│   │   ├── MANIFEST.json
│   │   └── README.txt
│   ├── wp0_4_smoketest_triad/
│   │   ├── triad_qa_maps/
│   │   │   ├── NSW_N0856_peri_urban.png
│   │   │   ├── QLD_0117LZI001_remote.png
│   │   │   ├── README.md
│   │   │   └── TAS_50483_urban_edge.png
│   │   ├── MANIFEST.json
│   │   ├── README.txt
│   │   ├── smoke_test_triad_definition.md
│   │   ├── smoke_test_triad_index_v0_1_0.csv
│   │   ├── smoke_test_triad_rings_v0_1_0.csv
│   │   └── triad_qa_manifest.json
│   ├── wp0_5_pa_geometry/
│   │   ├── MANIFEST.json
│   │   ├── pa_geometries_v0_1_0.csv
│   │   ├── pa_geometries_v0_1_0.gpkg
│   │   ├── pa_geometry_qc.md
│   │   └── README.txt
│   ├── wp0_6_radiance_smoketest/
│   │   ├── MANIFEST.json
│   │   ├── pa_radiance_buffers_smoketest_v0_1_0.csv
│   │   ├── README.txt
│   │   ├── smoketest_buffers_sanity.md
│   │   └── smoketest_buffers_summary.png
│   ├── wp0_7_edge_profiles_smoketest/
│   │   ├── MANIFEST.json
│   │   ├── pa_edge_profiles_smoketest_v0_1_0.csv
│   │   ├── README.txt
│   │   ├── smoketest_edge_profiles.md
│   │   └── smoketest_edge_profiles.png
│   └── wp0_8_schema_reference/
│       ├── MANIFEST.json
│       ├── output_schema_reference.md
│       └── README.txt
├── data/
│   ├── processed/
│   │   ├── .gitkeep
│   │   ├── pa_edge_profiles_smoketest_v0_1_0.csv
│   │   ├── pa_geometries_v0_1_0.csv
│   │   ├── pa_geometries_v0_1_0.gpkg
│   │   ├── pa_radiance_buffers_smoketest_v0_1_0.csv
│   │   ├── smoke_test_triad_buffers_v0_1_0.gpkg
│   │   ├── smoke_test_triad_geoms_v0_1_0.gpkg
│   │   ├── smoke_test_triad_index_v0_1_0.csv
│   │   └── smoke_test_triad_rings_v0_1_0.csv
│   ├── raw/
│   │   ├── nightlights_zenodo_v0_4/
│   │   │   ├── nightlights.average_viirs.v21_m_500m_s_20130101_20131231_go_epsg4326_v20250904.tif
│   │   │   ├── nightlights.average_viirs.v21_m_500m_s_20180101_20181231_go_epsg4326_v20250904.tif
│   │   │   └── nightlights.average_viirs.v21_m_500m_s_20240101_20241231_go_epsg4326_v20250904.tif
│   │   ├── .gitkeep
│   │   ├── capad_2024_technical_spec.pdf
│   │   └── vnl_v22_readme_20230707.pptx
│   └── README.md
├── docs/
│   ├── log/
│   │   ├── 000_bootstrap.md
│   │   ├── 010_data_acquisition.md
│   │   ├── 015_smoketest_triad.md
│   │   ├── 020_exploratory_analysis.md
│   │   ├── 025_pa_geometry.md
│   │   ├── 030_radiance_smoketest.md
│   │   ├── 035_radiance_buffers_smoketest.md
│   │   ├── 040_edge_profiles_smoketest.md
│   │   └── 045_output_schema.md
│   ├── collaboration_protocol.md
│   ├── decisions.md
│   ├── interpretation_notes.md
│   ├── plan.md
│   ├── questions_for_human.md
│   ├── roadmap.md
│   └── workflow.md
├── manuscript/
│   ├── figures/
│   │   └── .gitkeep
│   └── text/
│       └── .gitkeep
├── src/
│   ├── python/
│   │   ├── dsipa/
│   │   │   ├── __init__.py
│   │   │   ├── capad.py
│   │   │   ├── data_inventory.py
│   │   │   ├── manifest.py
│   │   │   ├── nightlights.py
│   │   │   ├── pa_geometry.py
│   │   │   ├── paths.py
│   │   │   ├── radiance_smoketest.py
│   │   │   ├── ring_profiles_smoketest.py
│   │   │   ├── run.py
│   │   │   ├── schema.py
│   │   │   ├── schema_reference.py
│   │   │   └── triad.py
│   │   └── .gitkeep
│   └── r/
│       └── .gitkeep
├── tests/
│   ├── python/
│   │   ├── .gitkeep
│   │   ├── test_edge_profiles_smoketest.py
│   │   ├── test_manifest.py
│   │   ├── test_pa_geometry.py
│   │   ├── test_radiance_smoketest.py
│   │   ├── test_run.py
│   │   └── test_triad.py
│   └── r/
│       └── .gitkeep
├── .gitignore
├── AGENTS.md
├── LICENSE
├── pi_blocker_bundle_2026-01-01.zip
├── pyproject.toml
├── README.md
├── REPO_MAP.md
└── uv.lock
```

Notes:
- Excludes `.git`, `.venv`, `dist`, `build`, `.pytest_cache`, `__pycache__`, and `*.egg-info`.
- This is a point-in-time snapshot; update as structure changes.

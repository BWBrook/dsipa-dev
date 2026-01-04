# Zenodo release checklist

Generated: 2026-01-04 UTC
Schema version: 0.3.0

## Checklist
- [ ] Confirm national outputs are regenerated for schema v0.3.0.
- [ ] Verify outputs are derived from a clean commit (record commit hash in Zenodo description).
- [ ] Run unit tests and record results.
- [ ] Generate canonical artefacts for WP0.10c–WP0.13c (optional but recommended).
- [ ] Upload required national tables + geometry outputs to Zenodo.
- [ ] Copy SHA256 checksums into the Zenodo record description or an attached manifest.
- [ ] Add repository URL + commit hash, and link to this checklist in Zenodo metadata.
- [ ] After DOI is minted, update data/README.md with the Zenodo DOI and access date.

## Required files

| Path | Status | Size (MB) | SHA256 |
| --- | --- | --- | --- |
| data/processed/pa_radiance_buffers_national_v0_3_0.csv | present | 92 | 493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e |
| data/processed/pa_edge_profiles_national_v0_3_0.csv | present | 25 | 9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888 |
| data/processed/pa_buffer_validity_v0_3_0.csv | present | 3 | 407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25 |
| data/processed/pa_trends_v0_3_0.csv | present | 5 | d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f |
| data/processed/pa_risk_rankings_v0_3_0.csv | present | 1 | 554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a |

## Optional/context files

| Path | Status | Size (MB) | SHA256 |
| --- | --- | --- | --- |
| data/processed/pa_geometries_v0_3_0.gpkg | present | 127 | 0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11 |
| data/processed/pa_geometries_v0_3_0.csv | present | 2 | 781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b |
| artefacts/wp0_10c_layerA_sanity | dir | 1 | - |
| artefacts/wp0_11c_trends_censoring | dir | 6 | - |
| artefacts/wp0_12c_risk_retention | dir | 1 | - |
| artefacts/wp0_13c_layerA_figures | dir | 1 | - |


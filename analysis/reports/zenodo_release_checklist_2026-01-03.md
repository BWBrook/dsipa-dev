# Zenodo release checklist

Generated: 2026-01-03 UTC
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
| data/processed/pa_radiance_buffers_national_v0_3_0.csv | present | 92 | 33f354c6447c3108d69f4461a727eae7f52cc6b023ce47f37bc6459fff1cb9df |
| data/processed/pa_edge_profiles_national_v0_3_0.csv | present | 25 | 4af7830beab5a286371aabf38d344dac4fa216b9ae0b4252c19db74ab2ccb8b5 |
| data/processed/pa_buffer_validity_v0_3_0.csv | present | 3 | 1e7f8d152a2f59f5c0c57b5b9acd310ac04eb11faec4e011018567094807ac8a |
| data/processed/pa_trends_v0_3_0.csv | present | 5 | 000ae620f537e3d3e70abf2d76f0f9da7f9ec27c804588940651812a23b6259f |
| data/processed/pa_risk_rankings_v0_3_0.csv | present | 1 | 9ac0a201a1b9d1d199e6a68e977032ccceac45b62ee4a29a1cd58c3c38f47624 |

## Optional/context files

| Path | Status | Size (MB) | SHA256 |
| --- | --- | --- | --- |
| data/processed/pa_geometries_v0_3_0.gpkg | present | 127 | 0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11 |
| data/processed/pa_geometries_v0_3_0.csv | present | 2 | 781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b |
| artefacts/wp0_10c_layerA_sanity | dir | 1 | - |
| artefacts/wp0_11c_trends_censoring | dir | 6 | - |
| artefacts/wp0_12c_risk_retention | dir | 1 | - |
| artefacts/wp0_13c_layerA_figures | dir | 1 | - |


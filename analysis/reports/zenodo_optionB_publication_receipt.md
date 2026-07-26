# Zenodo Option B Publication Receipt

Status: pass. Publication, public metadata, full public-download byte/checksum
verification, and focused RSEC validation/builds are complete. Exact-path Git
closeout remains.

Verified: 2026-07-26.

## Public Record

- Record: <https://zenodo.org/records/21524637>
- DOI: <https://doi.org/10.5281/zenodo.21524637>
- DOI resolution: pass; resolves to the public record above
- Public API status: `published`
- Publication date: `2026-07-26`
- Resource type: Dataset
- Version: `0.3.0`
- Title: Australian protected-area dark-sky integrity outputs, 2013-2024
- Access: open; no embargo
- Licence: Creative Commons Attribution 4.0 International (`CC BY 4.0`)
- Rights holder: University of Tasmania
- Copyright: `Copyright (C) 2026 University of Tasmania.`
- Funding, contributors, community: none

Creator:

- `Brook, Barry W.`
- ORCID: `0000-0002-2491-1517`
- Affiliation: School of Natural Sciences, University of Tasmania, Hobart,
  Tasmania, Australia
- Creator count: one

Keywords:

1. artificial light at night
2. protected areas
3. VIIRS
4. Australia
5. remote sensing
6. dark-sky integrity

Related identifier:

- `10.5281/zenodo.17294744`
- Relation: `isDerivedFrom`
- Resource type: Dataset

## Canonical Citation

> Brook, B. W. (2026). Australian protected-area dark-sky integrity outputs,
> 2013-2024 (Version 0.3.0) [Dataset]. Zenodo.
> https://doi.org/10.5281/zenodo.21524637

## Published File Inventory

The public page displays exactly 12 flat files and 265.8 MB. The nine payload
files total exactly `265,783,139` bytes; all 12 files total `265,798,999`
bytes. Every public server MD5 below matches the corresponding current local
staging file (12/12).

| File | Role | Bytes | Public server MD5 |
| --- | --- | ---: | --- |
| `README.md` | companion | 3,130 | `f15f51b8a29dd3a72e173dd95641fc8e` |
| `SHA256SUMS` | companion | 1,025 | `0a04012a3d7ed43f4ff66ce26b6f4875` |
| `manifest.json` | companion | 11,705 | `fa9336e01fb4928160276b216a7b7649` |
| `pa_buffer_validity_v0_3_0.csv` | payload | 2,561,064 | `d9d183ff2d6defd77384435558211480` |
| `pa_edge_profiles_national_v0_3_0.csv` | payload | 25,255,793 | `04537ef868cb5fe4ccb366a908722faf` |
| `pa_geometries_v0_3_0.csv` | payload | 1,768,417 | `ab311e72a4e1e9a3008a7981f915be1d` |
| `pa_geometries_v0_3_0.gpkg` | payload | 132,571,136 | `bc2fe3b60cd5c2316ff77e64f1135eda` |
| `pa_ibra_assignment_v0_3_0.csv` | payload | 987,075 | `5d6e53bc0d1c937d89548782e1a6e6dd` |
| `pa_radiance_buffers_national_v0_3_0.csv` | payload | 96,268,937 | `3919f413eb387d0e0e519315b66252da` |
| `pa_risk_rankings_v0_3_0.csv` | payload | 600,663 | `a1c747592c5919f63df03762c94d5b95` |
| `pa_trend_bootstrap_summary_v0_3_0.csv` | payload | 582,886 | `03970533cc5c0fdac3531e1f13a146a4` |
| `pa_trends_v0_3_0.csv` | payload | 5,187,168 | `d2de7a6be4603269b9dac61bb404184f` |

The deposit contains processed Layer A outputs only. It contains zero raw or
row-level Atlas of Living Australia files, zero Layer B files, and zero
unlisted files. The source GitHub repository remains private and is local
provenance only; this receipt does not represent the source code as public.

## Verification State

Verified from the public DOI, record page, API metadata, and server checksum
inventory:

- DOI resolution and public availability: pass
- public API status `published`: pass
- public record metadata and canonical citation: pass
- exact flat inventory and file-size totals: pass
- public server MD5 versus local staging: 12/12 pass
- deposit-boundary exclusions: pass

Verified from the full public re-acquisition:

- 12 files downloaded, totalling `265,798,999` bytes
- public API sizes and server MD5 values: 12/12 pass
- downloaded files byte-identical to flat staging: 12/12 pass
- downloaded `SHA256SUMS`: 11/11 pass
- nine payloads SHA-256-, size-, and byte-identical to the frozen candidate:
  9/9 pass
- downloaded manifest JSON: valid
- public metadata assertions: 24/24 pass
- excluded files: zero raw ALA, zero row-level ALA, zero Layer B, and zero
  unlisted

Ignored evidence:
`artefacts/goal015_zenodo_evidence/public_verification_2026-07-26.json`.
The public-download portion of Gate D is complete. The receipt JSON parses, 13
focused tests pass, and draft, submission, and supplementary `ms-check` and
`ms-build` all pass after one focused dataset-citation repair. The generated
main and SI assets passed focused text/visual inspection. Exact-path Git
commit/push and remote reconciliation are the only remaining orchestrator-owned
Goal 015 closeout actions.

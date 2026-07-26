# Zenodo Option B Metadata

Status: published Zenodo Dataset record. DOI resolution, public record/API
state, metadata, 12-file inventory, and server-MD5 equality with local staging
are verified. Full public-download byte and SHA-256 verification also passes.

Prepared: 2026-07-26 for Goal 015.

## Confirmed Record Metadata

- Resource type: Dataset
- Title: Australian protected-area dark-sky integrity outputs, 2013-2024
- Creator: `Brook, Barry W.` (exact final preview match)
- ORCID: `0000-0002-2491-1517`
- Creator count: sole creator
- Affiliation: School of Natural Sciences, University of Tasmania, Hobart,
  Tasmania, Australia
- Version: `0.3.0`
- Publication date: `2026-07-26`
- Language: English
- Access: open/public
- Embargo: none
- Licence: Creative Commons Attribution 4.0 International (`CC BY 4.0`)
- Rights holder: University of Tasmania
- Copyright: `Copyright (C) 2026 University of Tasmania.`
- Contributors: none
- Zenodo community: none
- Funding: none associated with a specific grant

Barry confirmed on 2026-07-24 that the dataset falls under the applicable
University of Tasmania policy and that he has authority or approval to release
it under CC BY 4.0. Publication later proceeded through the separate Goal 015
Gate C authority.

## Description

This dataset contains nine processed national Layer A outputs supporting a
detectability-aware assessment of artificial light at night inside and around
Australian protected areas for 2013-2024. It includes annual inside/buffer
radiance summaries, interior-ring profiles, buffer-validity descriptors,
trends, categorical screening output, protected-area descriptors/geometries,
IBRA assignments, and trend-bootstrap summaries.

Six files reproduce historical hashes exactly. Three are accepted non-exact:
the radiance CSV has no detected primary scientific drift but lacks direct
historical row-level proof; the edge-profile CSV contains an accepted bounded
threshold-sensitive difference, with current ring-1 feasibility
`1,432/12.9%`; and the GPKG has accepted within-run semantic identity but lacks
direct historical feature-level proof. All accepted primary scientific
headlines match.

The legacy file `pa_risk_rankings_v0_3_0.csv` contains categorical screening
output, not a priority ranking.

The deposit contains processed Layer A outputs only. Raw Atlas of Living
Australia downloads, row-level ALA occurrence data, Layer B biodiversity
payloads, and every unlisted file are excluded.

## Files And Checksums

- File presentation: 12 flat, individually downloadable files; no ZIP
- Payload files: 9
- Companion files: `README.md`, `manifest.json`, and `SHA256SUMS`
- Total payload bytes: `265,783,139`
- Historical-hash classification: six exact, three accepted non-exact
- Local deposit staging:
  `artefacts/optionB_layerA_zenodo_deposit_staging_2026-07-24/`
- Local verification evidence:
  `artefacts/goal015_zenodo_evidence/local_staging_verification.json`
- `SHA256SUMS`: 11 entries covering every other staging file
- Frozen accepted candidate:
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`

The nine staged payloads match the candidate byte sizes and SHA-256 values
9/9. The candidate remained unchanged after staging.

## Provenance And Attribution

- Accepted source run:
  `20260723T062202Z-goal011-layerA-preservation`
- Analysis schema: `0.3.0`
- Period: 2013-2024
- CAPAD 2024 and IBRA 7.1: Australian Government Department of Climate
  Change, Energy, the Environment and Water; CC BY 4.0
- OpenGeoHub/Zenodo VIIRS night-lights v0.4:
  <https://doi.org/10.5281/zenodo.17294744>; CC BY 4.0
- Natural Earth land mask: public domain
- Related input identifier: `10.5281/zenodo.17294744` as `IsDerivedFrom`
- Related manuscript DOI: none until one exists

The private GitHub repository URL is local provenance only. It must not be
entered as public metadata, a public access link, an alternate public
identifier, or a substitute for the Zenodo data record while the repository
remains private.

## Keywords

- artificial light at night
- protected areas
- VIIRS
- Australia
- remote sensing
- dark-sky integrity

## Citation And External State

Current public state verified on 2026-07-26:

- Public record: <https://zenodo.org/records/21524637>
- DOI: <https://doi.org/10.5281/zenodo.21524637>; resolves to the public
  record.
- Public API state: `published`.
- Resource type/version/publication date: Dataset; `0.3.0`; `2026-07-26`.
- Access/licence: open, no embargo; CC BY 4.0.
- Public presentation: exactly 12 flat files, displayed as 265.8 MB.
- Source repository: remains private and is not represented as public code or
  as a public access route.

Canonical APA citation:

> Brook, B. W. (2026). Australian protected-area dark-sky integrity outputs,
> 2013-2024 (Version 0.3.0) [Dataset]. Zenodo.
> https://doi.org/10.5281/zenodo.21524637

The initial concurrent upload returned Zenodo 502/504 errors. Incomplete
placeholders were removed and only the five failed files were retried: four
smaller files completed together and the 132.57 MB GPKG completed alone. The
final preview showed all 12 files with server checksums and sizes. This is
operational evidence, not a dataset caveat.

## Publication And Server File Evidence

All Zenodo-computed MD5 values matched the local staged-file MD5 values exactly
(12/12):

| File | Local/server bytes | Local MD5 = server MD5 |
| --- | ---: | --- |
| `README.md` | 3,130 | `f15f51b8a29dd3a72e173dd95641fc8e` |
| `SHA256SUMS` | 1,025 | `0a04012a3d7ed43f4ff66ce26b6f4875` |
| `manifest.json` | 11,705 | `fa9336e01fb4928160276b216a7b7649` |
| `pa_buffer_validity_v0_3_0.csv` | 2,561,064 | `d9d183ff2d6defd77384435558211480` |
| `pa_edge_profiles_national_v0_3_0.csv` | 25,255,793 | `04537ef868cb5fe4ccb366a908722faf` |
| `pa_geometries_v0_3_0.csv` | 1,768,417 | `ab311e72a4e1e9a3008a7981f915be1d` |
| `pa_geometries_v0_3_0.gpkg` | 132,571,136 | `bc2fe3b60cd5c2316ff77e64f1135eda` |
| `pa_ibra_assignment_v0_3_0.csv` | 987,075 | `5d6e53bc0d1c937d89548782e1a6e6dd` |
| `pa_radiance_buffers_national_v0_3_0.csv` | 96,268,937 | `3919f413eb387d0e0e519315b66252da` |
| `pa_risk_rankings_v0_3_0.csv` | 600,663 | `a1c747592c5919f63df03762c94d5b95` |
| `pa_trend_bootstrap_summary_v0_3_0.csv` | 582,886 | `03970533cc5c0fdac3531e1f13a146a4` |
| `pa_trends_v0_3_0.csv` | 5,187,168 | `d2de7a6be4603269b9dac61bb404184f` |

The public deposit boundary remains strict: zero raw or row-level Atlas of
Living Australia files, zero Layer B payloads, and no unlisted files. The
exact local pre-upload evidence remains 9/9 candidate payload SHA-256 matches,
with `SHA256SUMS` verifying 11/11 other staging files. Candidate identity
remains 12/12 unchanged. The public server MD5 inventory matches current local
staging 12/12. Full public re-acquisition downloaded 12 files totalling
`265,798,999` bytes and proved 12/12 byte identity with staging, 11/11
downloaded `SHA256SUMS` entries, and 9/9 payload SHA-256, size, and byte
identity with the frozen candidate. Public metadata assertions pass 24/24;
the downloaded manifest is valid; and raw ALA, row-level ALA, Layer B, and
unlisted-file exclusions remain zero.

The companion-only repair was uploaded and re-previewed successfully. The
repaired remote and local companions have `manifest.json` size 11,705 bytes,
SHA-256 `787c56fba9226444e77dd97f6f8351743ed0d1b77284217c7b8d8109f4469192`,
MD5 `fa9336e01fb4928160276b216a7b7649`; and `SHA256SUMS` size 1,025 bytes,
SHA-256 `2317be0fe88b1c6792fd9dda89aa6a7607bfd09e2747166596312449990ff260`,
MD5 `0a04012a3d7ed43f4ff66ce26b6f4875`. All 12 published server MD5 values
match the current local flat staging exactly. The superseded companion hashes
are historical chronology only, not current evidence.

The published remote manifest states: `Publication-ready flat Zenodo deposit
manifest; the Zenodo landing page is canonical for record and DOI state.` Its
stable external-state policy is present and the stale pre-deposit false claims
are absent.

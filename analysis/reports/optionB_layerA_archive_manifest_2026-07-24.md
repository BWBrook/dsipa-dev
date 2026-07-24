# Option B Layer A Archive Manifest

Status: **local candidate verified; external actions blocked**.

Generated: 2026-07-24 for Goal 014.

This report does not create a Zenodo draft, upload files, reserve or mint a
DOI, create a Git tag/release, log into or submit to Wiley, authorize a fee,
agree to open-access terms, commit, or push.

## Recovery Identity

- Read-only source:
  `deep-server-ts:/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation/payload/`
- Goal 011 run: `20260723T062202Z-goal011-layerA-preservation`
- Accepted source commit:
  `7f46a00f74c32881034f0129728b3d80eedd2442`
- Local ignored destination:
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`
- Recovery time: `2026-07-24T00:03:59Z`
- Recovery method: rsync with explicit directory entries and an exact
  nine-file include allowlist, with all other paths excluded.

The read-only source listing contained exactly the nine approved files and
reported total size `265,783,139` bytes. The local candidate independently
matched every Goal 011 byte size and SHA-256.

## Candidate Inventory

| Path | Bytes | Goal 011 SHA-256 | Goal 011 classification |
| --- | ---: | --- | --- |
| `data/processed/pa_radiance_buffers_national_v0_3_0.csv` | 96,268,937 | `6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61` | `byte_different_no_detected_primary_drift_historical_rows_unproven` |
| `data/processed/pa_edge_profiles_national_v0_3_0.csv` | 25,255,793 | `baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812` | `bounded_secondary_threshold_sensitive_drift` |
| `data/processed/pa_buffer_validity_v0_3_0.csv` | 2,561,064 | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | `exact` |
| `data/processed/pa_trends_v0_3_0.csv` | 5,187,168 | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | `exact` |
| `data/processed/pa_risk_rankings_v0_3_0.csv` | 600,663 | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | `exact` |
| `data/processed/pa_geometries_v0_3_0.csv` | 1,768,417 | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | `exact` |
| `data/processed/pa_geometries_v0_3_0.gpkg` | 132,571,136 | `6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9` | `byte_different_within_run_semantics_exact_historical_features_unproven` |
| `data/processed/pa_ibra_assignment_v0_3_0.csv` | 987,075 | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | `exact` |
| `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv` | 582,886 | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | `exact` |

Payload count: **9**. Payload total: **265,783,139 bytes**. Exact historical
hashes: **6**. Accepted non-exact files: **3**.

## Reconciliation

- Radiance: no detected primary scientific drift; direct historical row-level
  equality is unproven.
- Edge profiles: the independently accepted bounded difference changes
  ring-1 feasibility from historical `1,427` to current `1,432/12.9%`.
  Complete-ring n remains `383`, and all primary headlines match.
- Geometry GPKG: within-run columns, attributes, CRS, and WKB semantics match;
  direct historical feature-level equality is unproven.
- `pa_risk_rankings_v0_3_0.csv` is categorical screening output under a legacy
  filename, not a priority ranking.

Goal 012 reference-contract classifications are preserved separately in the
JSON companion and candidate `manifest.json`; they describe canonical ordering
or container semantics and do not replace the exact Goal 011 classifications
above.

## Candidate Companions

The only non-payload files are:

| File | SHA-256 |
| --- | --- |
| `README.md` | `cbf3227cbe378c1321441242c33e30fe6a1c3e6f8b4a3d57867e1b228f021532` |
| `manifest.json` | `ed727510d48350050bf37de0ef8cbbb123b56686f86e6ce1d9694be38a97be1a` |
| `SHA256SUMS` | `1ea60510554f327e125031fab9a87c33ec130b893ecedbfd43cf6c8d8d4ce3ff` |

## ALA Exclusion

Because the candidate matches an exact nine-file Layer A allowlist and every
file matches its accepted Goal 011 hash, it contains zero raw ALA downloads,
zero row-level processed ALA occurrence tables, and zero Layer B payloads.
No ALA file was copied, staged, compressed, or uploaded.

## External State

- Zenodo draft/upload: none.
- DOI reserved/minted: none.
- Git tag/release: none.
- Wiley login/submission: none.
- Fee or OA agreement: none.
- Goal 014 commit/push: none.

Machine-readable companion:
`analysis/reports/optionB_layerA_archive_manifest_2026-07-24.json`.

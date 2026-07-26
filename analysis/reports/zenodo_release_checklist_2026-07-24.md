# Zenodo Release Checklist: Option B

Status: published on 2026-07-26. DOI resolution, public record/API metadata,
12-file inventory, server/local staging MD5 equality, and full public-download
byte/SHA verification are verified. Focused RSEC tests and all three profile
checks/builds passed. Tracked reconciliation is ready for exact-path Git
closeout.

Updated: 2026-07-26.

| Gate | Status | Evidence |
| --- | --- | --- |
| Option B/no-ALA-exception decision | pass | DEC-040 and Goals 009-014. |
| Frozen candidate identity | pass | Exact accepted candidate retained unchanged. |
| Candidate inventory | pass | Nine payloads plus three companions; 12 files total. |
| Candidate payload bytes | pass | `265,783,139`. |
| Candidate hashes and sizes | pass | 9/9 independently verified. |
| Six exact/three non-exact classifications | pass | Goal 011 classifications preserved in the staging manifest. |
| Risk-ranking interpretation | pass | Legacy filename is categorical screening, not a priority ranking. |
| Raw/row-level ALA exclusion | pass | Zero such payloads in the exact allowlist and staging view. |
| Layer B exclusion | pass | Zero Layer B payloads in the exact allowlist and staging view. |
| Creator/ORCID/affiliation | pass - final preview match | `Brook, Barry W.` exactly matches the confirmed creator; `0000-0002-2491-1517`; sole creator; exact affiliation. |
| Rights holder/release authority | pass - Barry confirmed | University of Tasmania; authority or approval to release under CC BY 4.0 confirmed. |
| Resource type/title/version/language | pass - Barry confirmed | Dataset; confirmed title; `0.3.0`; English. |
| Access/licence/embargo | pass - Barry confirmed | Open/public; CC BY 4.0; no embargo. |
| Funding/contributors/community | pass - Barry confirmed | No specific grant; no contributors; no community. |
| Publication date | pass | Public API publication date is `2026-07-26`. |
| Keywords | pass - Barry confirmed | Six confirmed terms recorded in metadata and manifest. |
| Related input DOI | pass | `10.5281/zenodo.17294744` is recorded as `IsDerivedFrom` with resource type Dataset. |
| Private source-repository boundary | pass | URL retained as local provenance only; not public Zenodo metadata/access. |
| Flat staging presentation | pass | Exactly 12 unique root-level files; no ZIP; zero nested files. |
| Candidate-to-staging payload identity | pass | 9/9 byte-size and SHA-256 matches. |
| Staging checksums | pass | `SHA256SUMS` covers and verifies all 11 other files. |
| Staging manifest JSON | pass | JSON parses; payload metadata/mapping/classification/exclusion assertions pass; repaired external-state policy is current. |
| Final remote manifest preview | pass | Repaired manifest is 11,705 bytes; preview contains the publication-ready canonical-landing-page status and stable external-state policy; stale false claims are absent. |
| Local verification evidence | pass | `artefacts/goal015_zenodo_evidence/local_staging_verification.json`. |
| Candidate immutability after staging | pass | All 12 candidate hashes, including all three companions, unchanged. |
| Barry draft authorization | pass | `authorise draft` received 2026-07-24 and accepted as Gate B authority. |
| Zenodo draft history | pass | One verified draft was saved, uploaded, repaired once, and re-previewed before publication. |
| Upload and preview verification | pass | Exactly 12 flat files shown; preview total 265.8 MB; final preview showed server checksums and sizes after retrying five failed placeholders and re-previewing repaired companions. |
| Server/local file MD5 equality | pass | All 12 Zenodo-computed MD5 values equal local staged-file MD5 values (12/12); see metadata report and ignored evidence JSON. |
| Published DOI and public record | pass | <https://doi.org/10.5281/zenodo.21524637> resolves to <https://zenodo.org/records/21524637>; public API status is `published`. |
| Public metadata | pass | Exact title, sole creator, ORCID, affiliation, date, version, type, open/no-embargo access, CC BY 4.0, rights/copyright, six keywords, no funding/contributors/community, and related input DOI match the confirmed contract. |
| Public file presentation | pass | Public page shows exactly 12 flat files and 265.8 MB; server MD5 inventory matches local staging 12/12. |
| Public download verification | pass | 12 files/`265,798,999` bytes; 12/12 API sizes, server MD5 values, and staging byte identity; downloaded `SHA256SUMS` 11/11; payload SHA-256/size/byte identity 9/9; metadata 24/24; valid manifest; zero raw ALA, row-level ALA, Layer B, or unlisted files. |
| Manuscript citation insertion | pass - prepared | Actual public DOI/citation and the private-source/public-data distinction are reconciled only in the authorized tracked surfaces. |
| RSEC rebuild/test | pass | Receipt JSON parses; 13 focused tests pass; draft, submission, and supplementary `ms-check`/`ms-build` all pass after one focused dataset-citation repair. |
| Commit/push | pending orchestrator closeout | Not performed; exact-path commit/push and remote reconciliation are the remaining orchestrator-owned Goal 015 actions. |
| Release/tag work | incomplete | No tag or release is authorized or created by draft work. |
| Publication | pass | The verified Goal 015 draft was published once through Gate C on 2026-07-26. |

## Exact Local Surfaces

Frozen accepted candidate:

```text
artefacts/optionB_layerA_archive_candidate_2026-07-24/
```

Deposit-ready flat staging:

```text
artefacts/optionB_layerA_zenodo_deposit_staging_2026-07-24/
```

Machine-readable local verification:

```text
artefacts/goal015_zenodo_evidence/local_staging_verification.json
```

The flat staging contains exactly the nine accepted payload basenames plus
deposit-specific `README.md`, `manifest.json`, and `SHA256SUMS`. Use this
staging view for the authorized draft; never mutate or upload from a modified
copy of the frozen candidate.

## Gate D Closeout And Next Action

Publication, DOI resolution, public record/API inspection, canonical citation
capture, metadata review, the 12/12 server-MD5 comparison, and full public
re-acquisition are complete. The tracked reconciliation is prepared without
exposing the private source repository. Focused RSEC validation and all
draft/submission/supplementary checks and builds passed. Gate D remains open
only for exact-path Git commit/push and remote reconciliation.

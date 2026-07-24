# Final Release Manifest

Status: local RSEC release candidate for orchestrator review. This manifest
does not create or publish an archive, reserve or mint a DOI, create a Git
release, submit to Wiley, authorize fees, or agree to open-access terms.

Reconciled: 2026-07-24 for Goal 014.

## Current Identity

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- Candidate baseline HEAD and `origin/main`:
  `f5788ea4ad62237a95bf323930ec477107e7c2f3`
- Accepted manuscript: Goal 013 RSEC consolidation
- Accepted Layer A contract:
  `settings/layerA_reference_contract_v0_3_0.json`
- Accepted archive source: Goal 011 run
  `20260723T062202Z-goal011-layerA-preservation`
- Local ignored candidate:
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`

The current working tree contains the bounded Goal 014 implementation and has
not been committed or pushed. Exact final Git state is recorded in the Goal
014 closeout.

## Decision History

- Goal 010 records Barry/orchestrator approval of Option B through a
  Zenodo-style DOI route with no raw or row-level ALA redistribution
  exception. Goal 010 remains a blocked historical staging record because its
  eight missing files were not available at that time.
- Goal 011 regenerated all nine outputs. Independent review accepted the
  payload as a scientifically concordant but non-exact archive candidate.
- Goal 012 hardened clean-checkout execution and froze the current Layer A
  contract, including ring-1 `1,432/12.9%` and historical reconciliation
  `1,427` versus `1,432`.
- Goal 013 consolidated the evidence into the accepted RSEC manuscript.
- Goal 014 recovered and checksum-proved the exact Goal 011 payload locally.
  It does not authorize external movement.

## Classification Vocabulary

- `tracked`: version-controlled source, manuscript, figure, report, and compact
  derived evidence intended for the repository release surface.
- `archive-candidate`: an ignored, paper-relevant Layer A payload accepted for
  later archive review but not uploaded or assigned a DOI.
- `regenerated`: build/run outputs recreated by documented commands rather
  than primary archive objects.
- `excluded`: outside this release surface.
- `restricted`: not redistributed because provider/licence or row-level
  occurrence conditions require separate authorization.

## Option B Layer A Archive Candidate

The candidate contains exactly nine payload files and totals `265,783,139`
bytes. Candidate companions are limited to `README.md`, `manifest.json`, and
`SHA256SUMS`.

| Classification | Path | Bytes | Goal 011 SHA-256 | Reconciliation |
| --- | --- | ---: | --- | --- |
| archive-candidate | `data/processed/pa_radiance_buffers_national_v0_3_0.csv` | 96,268,937 | `6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61` | Byte-different; no detected primary drift; historical row equality unproven. |
| archive-candidate | `data/processed/pa_edge_profiles_national_v0_3_0.csv` | 25,255,793 | `baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812` | Accepted bounded secondary threshold-sensitive difference; current ring-1 `1,432/12.9%`. |
| archive-candidate | `data/processed/pa_buffer_validity_v0_3_0.csv` | 2,561,064 | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | Exact historical hash. |
| archive-candidate | `data/processed/pa_trends_v0_3_0.csv` | 5,187,168 | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | Exact historical hash. |
| archive-candidate | `data/processed/pa_risk_rankings_v0_3_0.csv` | 600,663 | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | Exact historical hash; categorical screening output under a legacy filename, not a priority ranking. |
| archive-candidate | `data/processed/pa_geometries_v0_3_0.csv` | 1,768,417 | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | Exact historical hash. |
| archive-candidate | `data/processed/pa_geometries_v0_3_0.gpkg` | 132,571,136 | `6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9` | Byte-different container; within-run attributes, CRS, and WKB match; historical feature equality unproven. |
| archive-candidate | `data/processed/pa_ibra_assignment_v0_3_0.csv` | 987,075 | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | Exact historical hash. |
| archive-candidate | `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv` | 582,886 | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | Exact historical hash. |

Six files match their historical SHA-256 exactly. The radiance, edge, and GPKG
limitations are part of the accepted release evidence and must not be
described as exact reproduction.

Machine- and human-readable evidence:

- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.json`
- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.md`
- `artefacts/optionB_layerA_archive_candidate_2026-07-24/manifest.json`
- `artefacts/optionB_layerA_archive_candidate_2026-07-24/SHA256SUMS`

## Tracked Repository And Manuscript Surface

The tracked release surface includes source and tests, `README.md`,
`data/README.md`, governance and workflow records, manuscript Markdown,
references, author metadata, generated manuscript figures, compact derived
Layer B summaries/licence ledgers, accepted analysis reports, and Goal 014
RSEC submission drafts.

Manuscript title:

> Detectable change in dark-sky integrity across Australia’s protected areas

Article type: **Original Research**.

The combined `draft` remains the working source assembly. The `submission`
profile builds main text only, while `supplementary` builds Supporting
Information separately. The main PDF/DOCX use visible placeholder author
metadata; the authoritative SI asset is PDF. The autogenerated SI DOCX is
diagnostic and non-submittable. All external submission fields remain visibly
pending Barry confirmation.

## Layer B ALA Policy

The following remain restricted/excluded and are absent from the Option B
candidate:

- `data/raw/ala_occurrences/microbats_20260104T020628Z.zip`
- `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`
- any other raw ALA download or row-level processed ALA occurrence table.

Mixed provider terms are documented in
`analysis/reports/layerB_ala_license_ledger.md`. No blanket ALA licence or
redistribution permission is claimed. Manuscript-facing Layer B evidence
remains derived summaries, reports, figures, and provenance ledgers.

## Provenance And Regenerated Outputs

DSIPA manuscript build manifests retain upstream Makedoc's top-level `git`
field as build-tool identity and add `repository_provenance.source` for the
DSIPA repository plus `repository_provenance.build_tool` for Makedoc. Each
records SHA, branch, and dirty state.

Build outputs under `build/`, distributions, temporary test outputs, and
general `artefacts/` content remain ignored/regenerated unless explicitly
identified as the local Option B candidate above.

## Official Requirements Checked

Checked 2026-07-24:

- <https://help.zenodo.org/docs/deposit/create-new-upload/>
- <https://help.zenodo.org/docs/deposit/about-records/>
- <https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/>
- <https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/author-guidelines>

The Zenodo material distinguishes draft, metadata/files, reserved DOI, and
published record states; this checkout remains before the draft stage. The
RSEC guidance supports the prepared Original Research, word/abstract/keyword,
double-spacing, continuous-line-numbering, main/SI, cover-letter, declaration,
data-accessibility, and count surfaces. It also identifies fee, open-access,
sole-submission, author/contribution, conflict, AI, and correspondence actions
that remain human-owned.

## Human And External Gates

Barry must confirm:

- creators, author order, ORCIDs, affiliations, and CRediT contributions;
- archive rights/licence and journal licence decision;
- archive date/version and publication date;
- funding and grant numbers;
- conflicts of interest;
- AI-use statement;
- all-author approval, sole-submission status, and accountability;
- corresponding-author full address and contact details;
- final DOI and repository URL after an authorized external action; and
- authorization for any Zenodo, Git release, Wiley, fee, or OA action.

Current external state:

- Zenodo draft/upload: none;
- DOI reserved/minted: none;
- Git tag/release: none;
- Wiley login/submission: none;
- fee/OA agreement: none;
- commit/push for Goal 014: none.

The candidate is ready only for local orchestrator review.

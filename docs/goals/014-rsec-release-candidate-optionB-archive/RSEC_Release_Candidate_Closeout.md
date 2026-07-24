# Goal 014 RSEC Release Candidate Closeout

Date: 2026-07-24

Status: **COMPLETE; local Option B/RSEC candidate ready for orchestrator
review, with human and external actions still blocked and no commit or push**.

## Conclusion

Goal 014 assembled and verified the accepted Goal 011 Option B Layer A payload,
reconciled the active release surface to the Goal 012 contract, added distinct
DSIPA-source and Makedoc-tool provenance, and produced separate RSEC main and
Supporting Information candidates.

The candidate remains local. No archive record, DOI, Git release, Wiley
submission, fee, licence, or open-access action exists.

Exact title:

> Detectable change in dark-sky integrity across Australia’s protected areas

Article type: **Original Research**.

## Starting And Final Git State

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- Start/final HEAD:
  `f5788ea4ad62237a95bf323930ec477107e7c2f3`
- Start/final `origin/main`:
  `f5788ea4ad62237a95bf323930ec477107e7c2f3`
- Starting status: only the authorized untracked Goal 014 packet.
- Final status: exactly the 34 authorized tracked paths listed below, plus the
  ignored archive candidate and normal build outputs.
- Commit: none.
- Push: none.

## Exact Tracked Footprint

Release and documentation:

- `analysis/reports/layerA_denominators_and_censoring.md`
- `analysis/reports/layerA_table1_candidate.md`
- `analysis/reports/final_release_manifest.md`
- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.md`
- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.json`
- `analysis/reports/zenodo_optionB_metadata_2026-07-24.md`
- `analysis/reports/zenodo_release_checklist_2026-07-24.md`
- `data/README.md`
- `docs/decisions.md`
- `docs/stage_overview.md`

Makedoc provenance and profiles:

- `analysis/annotate_makedoc_manifest.py`
- `analysis/makedoc.sh`
- `analysis/render_rsec_pdf_layout.py`
- `settings/build.yaml`
- `tests/python/test_makedoc_provenance.py`
- `tests/python/test_rsec_submission_contract.py`

RSEC assets:

- `manuscript/submission/rsec/README.md`
- `manuscript/submission/rsec/submission_checklist.md`
- `manuscript/submission/rsec/submission_metadata.md`
- `manuscript/submission/rsec/submission_counts.md`
- `manuscript/submission/rsec/cover_letter_draft.md`
- `manuscript/submission/rsec/declarations_draft.md`
- `manuscript/submission/rsec/submission_authors.yaml`
- `manuscript/submission/rsec/supplementary_frontmatter.md`
- `manuscript/submission/rsec/supplementary_table_end.md`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/supplementary_tables.md`

Goal and chronology:

- `docs/goals/014-rsec-release-candidate-optionB-archive/Goal.md`
- `docs/goals/014-rsec-release-candidate-optionB-archive/Plan.md`
- `docs/goals/014-rsec-release-candidate-optionB-archive/Runbook.md`
- `docs/goals/014-rsec-release-candidate-optionB-archive/Log.md`
- `docs/goals/014-rsec-release-candidate-optionB-archive/RSEC_Release_Candidate_Closeout.md`
- `docs/log/134_rsec_release_candidate.md`

No raw data, `data/processed/`, manuscript science/table content, references,
figure captions, figure paths/images, working author metadata, upstream
Makedoc, or unrelated file changed. The accepted-manuscript source edits are
three Markdown table delimiter rows and seven figure-width attributes;
headers, cells, values, labels, captions, prose, order, alignments, and image
files are unchanged.

## Archive Recovery

- Read-only source:
  `deep-server-ts:/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation/payload/`
- Recovery: explicit nine-file rsync include allowlist.
- Local ignored candidate:
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`
- Payload files: 9.
- Candidate companion files: `README.md`, `manifest.json`, `SHA256SUMS`.
- Candidate files total: 12.
- Payload total: `265,783,139` bytes.
- Checksum result: 9/9 `OK`.
- Historical exact/non-exact: 6/3.
- Raw or row-level ALA files: 0.
- Layer B payload files: 0.
- Unlisted payload files: 0.

### Payload Inventory

| Path | Bytes | SHA-256 | Historical status | Goal 011 classification | Goal 012 contract classification |
| --- | ---: | --- | --- | --- | --- |
| `data/processed/pa_radiance_buffers_national_v0_3_0.csv` | 96,268,937 | `6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61` | accepted non-exact | `byte_different_no_detected_primary_drift_historical_rows_unproven` | `canonical_ordering_change_semantically_exact` |
| `data/processed/pa_edge_profiles_national_v0_3_0.csv` | 25,255,793 | `baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812` | accepted non-exact | `bounded_secondary_threshold_sensitive_drift` | `canonical_ordering_change_semantically_exact` |
| `data/processed/pa_buffer_validity_v0_3_0.csv` | 2,561,064 | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | exact | `exact` | `canonical_ordering_change_semantically_exact` |
| `data/processed/pa_trends_v0_3_0.csv` | 5,187,168 | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | exact | `exact` | `exact` |
| `data/processed/pa_risk_rankings_v0_3_0.csv` | 600,663 | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | exact | `exact` | `exact` |
| `data/processed/pa_geometries_v0_3_0.csv` | 1,768,417 | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | exact | `exact` | `exact` |
| `data/processed/pa_geometries_v0_3_0.gpkg` | 132,571,136 | `6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9` | accepted non-exact | `byte_different_within_run_semantics_exact_historical_features_unproven` | `container_metadata_may_differ_semantics_exact` |
| `data/processed/pa_ibra_assignment_v0_3_0.csv` | 987,075 | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | exact | `exact` | `exact` |
| `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv` | 582,886 | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | exact | `exact` | `exact` |

Companion hashes:

| File | SHA-256 |
| --- | --- |
| `README.md` | `cbf3227cbe378c1321441242c33e30fe6a1c3e6f8b4a3d57867e1b228f021532` |
| `manifest.json` | `ed727510d48350050bf37de0ef8cbbb123b56686f86e6ce1d9694be38a97be1a` |
| `SHA256SUMS` | `1ea60510554f327e125031fab9a87c33ec130b893ecedbfd43cf6c8d8d4ce3ff` |

The legacy `pa_risk_rankings` filename is retained for provenance. Its content
is categorical screening, not a competitive management priority order.

## Release Reconciliation

- Current active ring-1 evidence is `1,432/11,133` or `12.9%`.
- The two primary active reports contain no `1,427` or `12.8%`.
- Three `1,427` hits remain only in explicit historical Goal 011/012
  reconciliation statements.
- Goal 010 remains a blocked historical staging record.
- Goal 011 remains the accepted payload identity.
- Goal 012 remains the current semantic/reference contract.
- No report claims that an archive, DOI, tag, release, or submission exists.

## Dual Provenance

The wrapper now annotates only successful `check` and `all` results. It
refreshes provenance even when upstream Makedoc leaves an existing manifest
unchanged, preserves upstream failure codes, performs no post-failure
annotation, and fails closed if a successful build has no manifest.

Focused TDD result:

```text
.....                                                                    [100%]
5 passed
```

All three final manifests passed JSON and `jq` assertions:

- upstream top-level `git` and `repository_provenance.build_tool`:
  - SHA `3a52e7059fb069c854b49d8f0a1991aface33d75`;
  - branch `main`;
  - dirty `false`;
- `repository_provenance.source`:
  - SHA `f5788ea4ad62237a95bf323930ec477107e7c2f3`;
  - branch `main`;
  - dirty `true`.

The dirty source state is expected because this is an uncommitted local
candidate. Upstream Makedoc remained clean; no upstream file changed.

## RSEC Candidate

Profile contract:

- `draft`: unchanged combined assembly, 1.5 spacing, continuous line numbers,
  `build/draft/dsipa_draft`;
- `submission`: main only, double spacing, continuous line numbers,
  visible placeholder author metadata, `build/submission/dsipa_rsec_main`;
- `supplementary`: Supporting Information only, PDF-authoritative with
  continuous line numbers, portrait frontmatter/captions/figures and compact
  landscape tables, `build/supplementary/dsipa_rsec_supplementary`.

Counts:

- abstract: 235 words;
- IMRAD: 4,609 words;
- IMRAD plus Data accessibility: 4,683 words;
- keywords: 5;
- main figures/tables: 4/1;
- SI figures/tables: 7/2;
- proposed running title: 34 characters.

Build products:

| Profile/product | Size | SHA-256 | Pages |
| --- | ---: | --- | ---: |
| `build/draft/dsipa_draft.pdf` | 1,171,210 | `9770563b24117f663f2f3304bcb6f1cac91f4bc9869a4ad76baf7138e14ded39` | 35 |
| `build/draft/dsipa_draft.docx` | 1,065,060 | `edc6dce43577137b954494a757b6a7c055c57c49cc4742efd81013a28687992d` | n/a |
| `build/submission/dsipa_rsec_main.pdf` | 492,100 | `b5fbba8bea3c133190c04b31a1d09cac2ed73d429034aa337b9400575c8d90aa` | 27 |
| `build/submission/dsipa_rsec_main.docx` | 421,351 | `1fe797ff04cc46d3d20a40ed23e88116aec53575569cfa07791b0d251ee0ee5e` | n/a |
| `build/supplementary/dsipa_rsec_supplementary.pdf` | 723,378 | `28e4c88a4361f1415c2415a551258bb85241e6bcc1c6a7b57c2c4b952ed0f112` | 14 |
| `build/supplementary/dsipa_rsec_supplementary.docx` (diagnostic only) | 655,550 | `0e2e61a2cf5d59a0cdbc6bb0eb0bf27c04394b159c4cbf3a18340e1c6a92c374` | n/a |

Build-manifest sizes and SHA-256 values are deliberately omitted: each
successful DSIPA annotation refreshes `annotated_at_utc`, so those byte hashes
are timestamp-dependent. Their current JSON structure and dual provenance are
validated directly instead.

Main/SI separation passed. The main contains the exact title and Abstract and
contains no SI source content, assets, or display definitions; legitimate
cross-references to Figs S1-S7 and Tables S1-S2 remain. The authoritative SI
PDF contains the exact title, Supporting Information, Tables S1-S2, and Figs
S1-S7, with no main Abstract, Introduction, Table 1 content/assets/definition,
or main-figure assets.

OOXML inspection records 1.5/double spacing as line values 360/480/480 and
continuous line numbering in all three generated profiles. This structural
fact does not make the SI DOCX a submission asset.

## Validation

Final prescribed commands:

| Command | Result |
| --- | --- |
| `uv run --locked pytest tests/python/test_makedoc_provenance.py tests/python/test_rsec_submission_contract.py -q` | pass, 13 tests |
| `make test` | pass, 83 passed and 9 expected missing-local-output skips |
| `make PROFILE=draft ms-check` | pass, including 61 Makedoc tests and zero unknown citations |
| `make PROFILE=draft ms-build` | pass |
| `make PROFILE=submission ms-check` | pass, including 61 Makedoc tests and zero unknown citations |
| `make PROFILE=submission ms-build` | pass |
| `make PROFILE=supplementary ms-check` | pass, including 61 Makedoc tests and zero unknown citations |
| `make PROFILE=supplementary ms-build` | pass |
| `git diff --check` | pass |
| `bash -n analysis/makedoc.sh` | pass |
| `python3 -m py_compile analysis/annotate_makedoc_manifest.py analysis/render_rsec_pdf_layout.py` | pass |

Additional gates:

- all five generated candidate/build JSON files pass
  `python3 -m json.tool`;
- candidate allowlist, total bytes, hashes, classifications, and ALA exclusion
  pass;
- DSIPA/Makedoc identity and profile assertions pass 3/3;
- title, type, word, abstract, keyword, citation, and display gates pass;
- all 14 final SI pages pass native-resolution visual review, including full
  visible `Fig. S1.`-`Fig. S7.` labels and legible plots;
- final main PDF and LibreOffice-rendered DOCX first pages visibly contain
  placeholders without overlap and contain no Barry/UTas assertion;
- final main Table 1 passes complete native-resolution review in the PDF
  (pages 17-19) and 36-page LibreOffice DOCX rendering (pages 23-27), without
  collisions, clipped headers, ambiguous cells, or vertical fragmentation;
- DOCX ZIP integrity passes 3/3;
- 16 XML/relationship parts per DOCX pass `xmllint`;
- LibreOffice opens/exports the final main and diagnostic SI DOCX files;
- precise tracked-footprint and ignored-candidate checks pass.

Pandoc cannot re-import any of the three generated DOCX files:

```text
exit 63
couldn't parse docx file: DocxError
```

ZIP integrity, XML validation, and LibreOffice open/export establish container
openability only. They do not override visual QA: the main DOCX is readable,
while the 32-page LibreOffice rendering of SI DOCX has severe table
fragmentation and is explicitly diagnostic/non-submittable.

## Focused Repair

Independent review rejected the initial candidate for two material defects:
the SI PDF/DOCX were unreadable, and the main PDF/DOCX asserted unconfirmed
Barry W. Brook/University of Tasmania authorship.

The bounded repair abandoned custom OOXML postprocessing. The working
`manuscript/authors.yaml` remains unchanged, while a submission-only YAML
renders visible placeholders for author names/order, affiliations, ORCIDs,
corresponding author, full address, and contact details.

The SI contract is PDF-authoritative. A deterministic DSIPA-owned layout
extender delegates to upstream Makedoc, adds `pdflscape` only for the
supplementary profile, is a byte-for-byte no-op for other profiles, avoids
duplicate package injection, and propagates upstream failure without replacing
output. Tests cover those behaviors.

Tables S1-S2 are scoped to pages 2-5 in landscape with footnote-size compact
spacing; figures return to portrait on page 6. The SI table layout uses two
approved Markdown delimiter rows assigning reviewed width vectors:

- S1: `10, 6, 13, 13, 4, 4, 7, 7, 8, 8, 10, 10%`;
- S2: `12, 17, 5, 5, 6, 6, 6, 6, 7, 7, 4, 5, 14%`.

Pandoc table ASTs normalized to remove only `colspec` had identical SHA-256
`77628867bdff41861f16f6e4476be8017006d817a221d62b9823e634ac4b3de0`
before and after. Thus captions, headers, cells, values, order, alignments,
labels, and prose are identical.

The final SI is 14 A4 pages: page 1 portrait, pages 2-5 rotated landscape,
and pages 6-14 portrait. Native-resolution inspection found no collision,
clipping, one-word table fragmentation, overlap, missing/blank figure, or
masked figure label.

A final full-resolution production review also repaired main Table 1 and the
SI figure-label clearance. Table 1 now uses the shared PDF/DOCX width vector
`22, 10, 16, 11, 23, 18%`. Its Pandoc Table AST, normalized to omit only
`colspec`, had identical SHA-256
`5878534ee812462312c7e07e53908a7756b0a7f75500817ac2168b5462511ed0`
before and after. SI figures S1-S5 and S7 use `width=85%`; S6 uses the targeted
`width=80%` fallback. The SI figure source, normalized to omit only width
values, had identical SHA-256
`47e5b13e0b930d8d542ba09bcb9d0367defefc926a7ed3f81fd4c9240a9e7887`
before and after, and all seven referenced image-file hashes remained
unchanged.

## Human Decisions Still Required

- author names/order, ORCIDs, affiliations, and CRediT roles;
- corresponding author and full address/contact details;
- archive creators, rights holder, and licence;
- version/date and final accepted release commit;
- funding and grant numbers;
- conflict-of-interest statement;
- AI-use statement;
- all-author approval and accountability;
- sole-submission/not-published confirmation;
- ethics/consent applicability;
- data/archive DOI and public URL after authorization;
- cover image decision and rights;
- publication fee and open-access choices;
- final archive and Wiley authorization.

Every such field remains visibly marked `[BARRY CONFIRM]` or
`[PENDING EXTERNAL ACTION]`.

## Blocked External Actions

Not performed:

- Zenodo draft or upload;
- DOI reservation, registration, or minting;
- Git tag or release;
- Wiley login or submission;
- fee payment or authorization;
- open-access or publication licence agreement;
- commit or push.

## Residual Limitations And Recommendation

1. The accepted radiance, edge-profile, and GPKG payloads remain non-exact
   under their explicit Goal 011/012 classifications.
2. Pandoc re-import fails for all three generated DOCX files. Main DOCX opens
   readably in LibreOffice; SI DOCX opens but is not production-readable and
   must not be submitted. The authoritative SI asset is PDF.
3. Human-owned identity, declarations, rights, licence, fee, OA, DOI/URL, and
   authorization decisions remain deliberately unresolved.
4. No public identifier or immutable public release exists.

Accept Goal 014 as the verified local release candidate. The next tranche is a
human decision and authorization pass, followed by a separately authorized
external archive/submission goal.

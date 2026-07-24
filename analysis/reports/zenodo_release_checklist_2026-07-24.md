# Zenodo Release Checklist: Option B

Status: local release-candidate checklist. External actions remain blocked.

Prepared: 2026-07-24 for Goal 014.

| Gate | Status | Evidence |
| --- | --- | --- |
| Option B/no-ALA-exception decision | pass | DEC-040 and Goal 010 history. |
| Goal 011 archive source identity | pass | Exact read-only source path and run id recorded. |
| Exact nine-file source allowlist | pass | Read-only rsync listing showed exactly nine files. |
| Exact payload bytes | pass | `265,783,139` bytes at source and destination. |
| Goal 011 hashes and sizes | pass | 9/9 independently matched after recovery. |
| Candidate companions only | pass | `README.md`, `manifest.json`, and `SHA256SUMS`; 12 files total. |
| Raw/row-level ALA exclusion | pass | Exact Layer A allowlist and hashes; zero ALA/Layer B payload files. |
| Six exact/three non-exact classifications | pass | Goal 011 classifications and Goal 012 contract classifications preserved. |
| Risk-ranking interpretation | pass | Legacy filename explicitly classified as categorical screening, not priority. |
| Active ring-1 release value | pass | Active reports use `1,432/12.9%`; `1,427` is historical reconciliation only. |
| Candidate manifest JSON | pass | JSON validates; paths, hashes, sizes, classes, source, and external state recorded. |
| Dual DSIPA/Makedoc provenance | pass | Focused tests pass; all three manifests preserve clean Makedoc `git` identity and record the distinct dirty DSIPA source identity. |
| RSEC main/SI profiles and assets | pass | Draft/main/SI checks and builds pass; final PDF/DOCX separation, counts, spacing, numbering, and displays are verified. |
| Creator/ORCID/affiliation/contribution | blocked on Barry | No human identity field is inferred. |
| Rights and archive licence | blocked on Barry | No combined-candidate licence is asserted. |
| Date/version/funding/conflict/AI/sole submission | blocked on Barry | Required human confirmations remain marked. |
| Correspondence address and DOI/URL | blocked on Barry/later external state | No address or identifier invented. |
| Zenodo draft or upload | blocked/not performed | No account or external record accessed. |
| DOI reservation or minting | blocked/not performed | No DOI action authorized. |
| External upload goal ready | no | Requires successful final local verification plus Barry/orchestrator authorization and all human fields. |

## Exact Candidate

```text
artefacts/optionB_layerA_archive_candidate_2026-07-24/
```

Use the candidate's `SHA256SUMS` only after re-verifying it in the later
authorized external-action goal. Do not substitute Goal 012 reserializations
or pre-Goal 011 historical hashes.

## Official Sources

Retrieved 2026-07-24:

- <https://help.zenodo.org/docs/deposit/create-new-upload/>
- <https://help.zenodo.org/docs/deposit/about-records/>
- <https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/>

No external action followed source checking.

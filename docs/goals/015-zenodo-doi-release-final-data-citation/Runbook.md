# Runbook: Goal 015 Zenodo DOI Release And Final Data Citation

Run future execution commands from `/Users/bwbrook/papers/dsipa-dev`. Packet
creation itself performs none of the Gate B-D commands below.

## Gate A: Packet Baseline And Footprint

The packet-authoring baseline is:

```bash
pwd
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git status --short --branch
```

Required:

```text
pwd = /Users/bwbrook/papers/dsipa-dev
branch = main
HEAD = origin/main = 37ccb4e0f33bc921a09baa06d908f2b8ce284d87
status before packet creation = ## main...origin/main
```

Gate A may create only:

```text
docs/goals/015-zenodo-doi-release-final-data-citation/Goal.md
docs/goals/015-zenodo-doi-release-final-data-citation/Plan.md
docs/goals/015-zenodo-doi-release-final-data-citation/Runbook.md
docs/goals/015-zenodo-doi-release-final-data-citation/Log.md
docs/goals/015-zenodo-doi-release-final-data-citation/Release_Confirmation_Sheet.md
```

Gate A verification is limited to:

```bash
git diff --check
git status --short --branch
git diff --name-only
git ls-files --others --exclude-standard
```

Do not run checksum, build, test, packaging, network, browser, commit, push, or
Zenodo commands in Gate A.

## Gate B Authorization Check

Before any Gate B command, re-read:

- `AGENTS.md`;
- all five Goal 015 files;
- Barry's exact confirmation response;
- Goal 014 packet and closeout;
- `analysis/reports/zenodo_optionB_metadata_2026-07-24.md`;
- `analysis/reports/zenodo_release_checklist_2026-07-24.md`;
- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.{md,json}`;
- `analysis/reports/final_release_manifest.md`;
- `data/README.md`; and
- the official sources listed below.

`analysis/zenodo_release_checklist.sh` encodes a stale pre-Goal-014 file set
and can overwrite the current dated checklist. Do not run it unmodified. The
frozen nine-payload allowlist and 12-file presentation in this packet are the
release contract. Treat both dated Goal 014 archive-manifest files as immutable
historical evidence: read and compare them, but never edit them.

Require all of the following before proceeding:

```text
creator/ORCID/affiliation/creator count confirmed
rights holder confirmed
release authority or approval under selected licence confirmed
funding/grant state confirmed
remaining metadata defaults approved or amended
Barry's instruction contains: authorize draft
```

Record only the substantive confirmation, never login or account material.
If any field is missing or ambiguous, remain at Gate A.

## Official Sources To Recheck

Record retrieval date and any changed guidance:

- Zenodo create upload:
  <https://help.zenodo.org/docs/deposit/create-new-upload/>
- Zenodo records and publication:
  <https://help.zenodo.org/docs/deposit/about-records/>
- Zenodo DOI reservation:
  <https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/>
- Zenodo licences:
  <https://help.zenodo.org/docs/deposit/describe-records/licenses/>
- Zenodo file management:
  <https://help.zenodo.org/docs/deposit/manage-files/>
- Creative Commons Attribution 4.0:
  <https://creativecommons.org/licenses/by/4.0/>
- Natural Earth terms:
  <https://www.naturalearthdata.com/about/terms-of-use/>
- CAPAD 2024 technical specification:
  <https://www.dcceew.gov.au/sites/default/files/documents/capad-2024-tech-spec.pdf>
- UTas Research Data Management Procedure:
  <https://www.utas.edu.au/__data/assets/pdf_file/0007/1551769/Research-Data-Management-Procedure.pdf>
- UTas Intellectual Property Policy:
  <https://www.utas.edu.au/__data/assets/pdf_file/0007/1457746/4.3-Intellectual-Property-Policy.pdf>

Official guidance checked 2026-07-24 says a licence is required and defaults to
CC BY 4.0; drafts may be populated and previewed before publication; a DOI is
registered on publication and may be reserved earlier; and multiple files may
be uploaded. The file guidance does not document directory-path preservation
and recommends considering ZIP for 20 or more files. Recheck rather than
assuming this remains current.

## Controlled Git Start

Record the exact state:

```bash
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git status --short --branch
git log --oneline --decorate -5
git merge-base --is-ancestor \
  37ccb4e0f33bc921a09baa06d908f2b8ce284d87 HEAD
```

The only acceptable tracked change at Gate B start is the accepted Goal 015
packet if it has not yet been committed. If the packet has been committed, the
worktree must be clean and the intervening commit must contain only the
accepted packet. Stop for every other difference.

## Frozen Candidate Verification

Set:

```bash
CANDIDATE=artefacts/optionB_layerA_archive_candidate_2026-07-24
```

Expected 12-file inventory:

```text
README.md
SHA256SUMS
data/processed/pa_buffer_validity_v0_3_0.csv
data/processed/pa_edge_profiles_national_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.gpkg
data/processed/pa_ibra_assignment_v0_3_0.csv
data/processed/pa_radiance_buffers_national_v0_3_0.csv
data/processed/pa_risk_rankings_v0_3_0.csv
data/processed/pa_trend_bootstrap_summary_v0_3_0.csv
data/processed/pa_trends_v0_3_0.csv
manifest.json
```

Create the expected list in `/tmp`, compare it with a sorted `find`, and remove
the temporary file afterward. Do not write inside the candidate.

Run the candidate's checksum file from its own root:

```bash
(
  cd "$CANDIDATE"
  shasum -a 256 -c SHA256SUMS
)
```

Require exactly nine `OK` results. Prove payload count and total bytes:

```bash
test "$(awk 'NF {n++} END {print n+0}' "$CANDIDATE/SHA256SUMS")" -eq 9

while IFS= read -r rel; do
  stat -f '%z' "$CANDIDATE/$rel"
done < <(awk 'NF {print $2}' "$CANDIDATE/SHA256SUMS") |
  awk '{total += $1} END {
    print total
    exit total != 265783139
  }'
```

Validate the structured manifest:

```bash
python3 -m json.tool "$CANDIDATE/manifest.json" >/dev/null
jq -e '
  .candidate.payload_count == 9 and
  .candidate.payload_total_size_bytes == 265783139 and
  (.candidate.additional_files == ["README.md","manifest.json","SHA256SUMS"]) and
  (.payload | length) == 9 and
  ([.payload[].historical_hash_exact] | map(select(. == true)) | length) == 6 and
  ([.payload[].historical_hash_exact] | map(select(. == false)) | length) == 3 and
  .exclusions.raw_ala_downloads == true and
  .exclusions.row_level_ala_occurrence_tables == true and
  .exclusions.layer_b_payloads == true and
  .exclusions.unlisted_files == true
' "$CANDIDATE/manifest.json"
```

Compare every `manifest.json` path, size, and SHA-256 with `SHA256SUMS` and the
actual file. Confirm that the categorical-screening interpretation and all
three non-exact limitations match Goal 014. Search the exact inventory for
`ala`, `occurrence`, and Layer B names, then manually confirm any textual hit
belongs only to exclusion/provenance prose and not a payload.

Any mismatch is an immediate stop. Do not repair by regeneration, conversion,
normalization, or substitution. The entire accepted candidate is immutable:
do not add, remove, rename, or edit its `README.md`, `manifest.json`,
`SHA256SUMS`, directory paths, or any payload. All deposit-facing changes
belong in the separate ignored staging view.

## File-Presentation Decision

Official Zenodo guidance does not promise preservation of nested directory
paths. The approved default is therefore 12 flat, individually downloadable
files in a separate ignored staging view. Create:

```text
artefacts/optionB_layerA_zenodo_deposit_staging_2026-07-24/
```

Requirements:

- copy each of the nine payloads to its unique basename without transforming
  bytes;
- independently verify every copied SHA-256 and size against the candidate;
- create deposit-specific `README.md`, `manifest.json`, and `SHA256SUMS`;
- record both each original `data/processed/...` path and its deposited flat
  filename in the manifest;
- retain the six-exact/three-accepted-non-exact classifications and all
  exclusions;
- make `SHA256SUMS` address the flat deposited filenames; and
- keep all 12 staged files in one ignored directory.

The nine current payload basenames are unique, but prove uniqueness before
copying:

```bash
awk 'NF {print $2}' "$CANDIDATE/SHA256SUMS" |
  awk -F/ '{print $NF}' |
  LC_ALL=C sort |
  uniq -d
```

The command must print nothing. Use ordinary byte-preserving file copy, then
hash the destination. Generate or transform JSON only with a structured JSON
tool and validate it with `python3 -m json.tool` plus `jq`. Never edit or
reserialize a CSV or GPKG. Re-prove that no candidate file or path changed
after staging.

### Documented packaging exception

Do not use ZIP by default: 12 files are below Zenodo's 20-or-more-file
guidance. Packaging is permitted only if the live service imposes a documented
functional constraint that flat direct upload cannot satisfy. Record the
reason, archive format, member names, uncompressed payload sizes, and member
hashes; prove that extraction yields all nine accepted payload hashes. Return
to Barry before upload because packaging changes the approved individually
downloadable presentation.

Record the exact 12 flat files shown in the draft. Do not upload the accepted
candidate companions directly and do not edit the accepted candidate to
accommodate the service.

## Final Deposit Metadata

Use Barry's confirmed sheet, not remembered chat text. Required defaults unless
amended:

```text
resource type = Dataset
title = Australian protected-area dark-sky integrity outputs, 2013-2024
creator = Brook, Barry W.
ORCID = 0000-0002-2491-1517
affiliation = School of Natural Sciences, University of Tasmania, Hobart,
              Tasmania, Australia
version = 0.3.0
publication date = actual date first made public
access = open/public, no embargo
licence = Creative Commons Attribution 4.0 International
community = none
contributors = none unless Barry adds one
funding = blank unless Barry supplies exact metadata
related input identifier = 10.5281/zenodo.17294744 as IsDerivedFrom,
                           if Zenodo supports that relation
related manuscript DOI = none until one exists
```

The private GitHub repository URL remains in local provenance only while the
repository is private. Do not enter it in Zenodo as a public access link,
public related identifier, alternate public identifier, or DOI. Public code
exposure is later scope. Do not change repository visibility.

The description must state:

- nine processed national Layer A outputs for 2013-2024;
- detectability-aware protected-area dark-sky analysis;
- six exact and three accepted non-exact files with their limitations;
- all accepted primary headlines match;
- the legacy risk-rankings filename is categorical screening only; and
- no raw/row-level ALA or Layer B payload is included.

Include source attribution for:

- CAPAD 2024 and IBRA 7.1, DCCEEW, CC BY 4.0;
- OpenGeoHub/Zenodo VIIRS night-lights v0.4, source DOI
  `10.5281/zenodo.17294744`, CC BY 4.0; and
- Natural Earth land mask, public domain.

Use `University of Tasmania` as rights holder only after Barry's exact
confirmation that the dataset falls under the applicable policy and he has
authority or approval to release it under CC BY 4.0. This runbook is not legal
advice. Stop if the confirmation is unavailable or inconsistent.

## Draft Creation, Upload, And Evidence

Zenodo login or 2FA may require Barry. Keep credentials and account details in
the live authenticated session only. Do not store them in environment files,
shell history, screenshots, packet files, Git, or logs.

After login:

1. create one new upload draft;
2. populate all confirmed metadata;
3. upload exactly the chosen 12 logical files;
4. reserve a DOI only if needed for pre-publication citation;
5. preview and re-open the draft;
6. compare every visible file and metadata field with the local evidence; and
7. do not use the publication control.

Store redacted screenshots or metadata exports only under:

```text
artefacts/goal015_zenodo_evidence/
```

Redact credentials, tokens, cookies, account identifiers, email, and 2FA
material. Report the draft URL or identifier to Barry in the live task when
needed for inspection, but do not commit private account-state identifiers.

For remote identity proof, download all nine draft payloads through the
authenticated draft interface into an ignored evidence subdirectory. Compute
SHA-256 locally and compare all nine with the accepted candidate. Also verify:

```text
logical files = 12
payload files = 9
payload bytes = 265783139
payload SHA-256 matches = 9/9
companions = README.md, manifest.json, SHA256SUMS
raw/row-level ALA payloads = 0
Layer B payloads = 0
```

Show Barry a compact table of draft filename, byte size, SHA-256 or companion
role, plus the exact metadata and a preview screenshot/export. Gate B ends
here. Do not publish.

## Gate C Publication Authority

After showing the complete draft evidence, wait for a new Barry message.

The new instruction must:

- contain the literal word `publish`;
- identify or unambiguously refer to the verified Goal 015 Zenodo draft; and
- arrive after Gate B evidence was presented.

These do not authorize publication:

```text
authorize draft
proceed
approved
looks good
silence
successful upload
successful DOI reservation
```

Immediately before publication, re-open the draft and recheck:

```text
12 exact logical files and 9/9 payload identity
Dataset type and exact title
confirmed creator, ORCID, affiliation, and creator count
confirmed rights holder and release authority
CC BY 4.0 licence
open/public access and no embargo
version 0.3.0
publication date is the actual public date
six keywords
description and limitation wording
CAPAD, IBRA, OpenGeoHub/VIIRS, and Natural Earth attribution
funding/community/contributor/related-identifier state
OpenGeoHub input DOI is IsDerivedFrom if that relation is supported
private GitHub source URL is absent from public access/identifier fields
```

If the state matches the evidence and the separate authority exists, publish
once. Capture the success confirmation. If Zenodo errors or the record state is
ambiguous, stop and inspect; do not click repeatedly and do not create a
replacement record.

## Gate D Public Verification

Use an unauthenticated session where possible to prove the record is genuinely
public.

1. Resolve the public DOI and record URL.
2. Inspect the public landing page and metadata export.
3. Verify all 12 public files are downloadable.
4. Download all public files to a new ignored evidence subdirectory.
5. Compare all nine payload SHA-256 values and byte sizes with the accepted
   candidate.
6. Validate the downloaded manifest and checksum companion.
7. Verify the public citation and metadata fields listed in Gate C.

Prefer full 9/9 public-download verification because the payload total is
about 266 MB and is feasible. If the service prevents full verification,
record the exact limitation, verify every server-reported file checksum plus a
documented download sample, and stop for orchestrator judgment before citation
reconciliation.

Do not treat DOI resolution alone, a successful authenticated view, or a
publication success banner as complete public verification.

## Tracked Reconciliation

Use the actual public record, not placeholders or inferred citation syntax.
Capture the canonical Zenodo citation and then narrowly update:

```text
analysis/reports/zenodo_optionB_metadata_2026-07-24.md
analysis/reports/zenodo_release_checklist_2026-07-24.md
analysis/reports/zenodo_optionB_publication_receipt.md
analysis/reports/zenodo_optionB_publication_receipt.json
analysis/reports/final_release_manifest.md
README.md
data/README.md
docs/decisions.md
docs/stage_overview.md
manuscript/text/manuscript_draft.md
manuscript/submission/rsec/declarations_draft.md
manuscript/submission/rsec/submission_metadata.md
manuscript/submission/rsec/submission_checklist.md
manuscript/submission/rsec/submission_counts.md
manuscript/submission/rsec/cover_letter_draft.md
docs/goals/015-zenodo-doi-release-final-data-citation/Log.md
docs/log/135_zenodo_doi_release.md
```

Do not edit the accepted Goal 014 historical evidence:

```text
analysis/reports/optionB_layerA_archive_manifest_2026-07-24.md
analysis/reports/optionB_layerA_archive_manifest_2026-07-24.json
```

Create the publication receipts from independently verified public evidence.
They must record the actual DOI and record URL, publication date, all 12 public
files with sizes and checksums, and the verified public metadata.

Only update the manuscript's `## Data accessibility` section and the named
RSEC data DOI, source-provenance, and archive-rights fields. Preserve the
raw/row-level ALA exclusion and exact-reacquisition limitation. Explicitly
distinguish:

```text
public data = the verified Zenodo Dataset record
source code = private GitHub repository retained as local provenance only
```

In `README.md`, change only the release/data-accessibility paragraph. In
`submission_counts.md`, recompute and change only the Data accessibility
inclusive count if the final wording changes it; preserve the counting method
and all unrelated counts.

Update `manuscript/authors.yaml` or
`manuscript/submission/rsec/submission_authors.yaml` only if Barry supplied the
exact identity fields and requested their use. Do not infer journal authorship
or contributions from Zenodo creator metadata.

Do not edit science, references, tables, captions, figures, code, tests,
configuration, raw data, or processed data.

## Focused Tests And RSEC Rebuild

After tracked reconciliation:

```bash
uv run --locked pytest \
  tests/python/test_makedoc_provenance.py \
  tests/python/test_rsec_submission_contract.py -q

make PROFILE=draft ms-check
make PROFILE=draft ms-build
make PROFILE=submission ms-check
make PROFILE=submission ms-build
make PROFILE=supplementary ms-check
make PROFILE=supplementary ms-build

git diff --check
git status --short --branch
git diff --name-only
git diff --stat
```

Validate every changed JSON file with `python3 -m json.tool`. Inspect the
generated DSIPA/Makedoc provenance and the main Data accessibility rendering
in PDF and DOCX. Confirm the supplementary PDF remains authoritative and no
new citation, placeholder, layout, or main/SI separation failure appears.

Run one focused repair only if a material defect is found, then repeat only the
checks affected by the repair plus the final acceptance set. Do not enter
repeated wording or layout polish loops.

## Orchestrator Review, Commit, And Push

Before staging, provide:

- exact public record and DOI-resolution evidence;
- public 12-file inventory and 9/9 payload hash/byte proof;
- metadata, rights, licence, attribution, and citation proof;
- exact changed paths and diff summary;
- focused tests and RSEC build results;
- remaining assumptions or limitations; and
- branch, HEAD, upstream, and status.

Commit and push only after explicit orchestrator acceptance within Goal 015.
Stage exact paths individually; never use `git add .`, `git add -A`, or a
directory-wide sweep. Then:

```bash
git diff --cached --check
git diff --cached --name-status
git diff --cached
git commit -m "Publish DSIPA Zenodo dataset citation"
git fetch --prune origin
git status --short --branch
git log --oneline --decorate -3
git push origin main
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
git status --short --branch
```

If `origin/main` moved unexpectedly, stop. Do not merge, rebase, force-push,
reset, or absorb unrelated work. Final acceptance requires matching local,
upstream, tracking, and remote identities plus a clean worktree.

No Git tag/release, repository-visibility change, Wiley login/submission,
payment, fee commitment, open-access agreement, or journal licence action is
permitted.

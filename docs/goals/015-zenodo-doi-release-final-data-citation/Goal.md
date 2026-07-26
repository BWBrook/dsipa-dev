# Goal 015: Zenodo DOI Release And Final Data Citation

## Objective

Publish one Zenodo Dataset record for the accepted Option B Layer A archive
candidate, then reconcile the actual public DOI, record URL, publication date,
version, licence, and data citation across the tracked DSIPA release and RSEC
surfaces. Independently verify the public record and downloaded payloads,
rebuild the targeted RSEC outputs, obtain orchestrator acceptance, and only
then commit and push the exact accepted footprint.

This goal is phase-gated. Gates A and B completed the confirmed local packet,
draft, upload, DOI reservation, repair, and final preview. Gate C then
published the verified draft on 2026-07-26. Gate D verifies the resolving
public DOI, `published` API state, exact public metadata (24/24 assertions),
12-file/`265,798,999`-byte flat inventory, 12/12 server-MD5 and staging byte
identity, 11/11 downloaded checksum entries, and 9/9 payload SHA-256, size,
and byte identity. Tracked citation reconciliation is prepared; focused
validation/build, acceptance, commit, and push remain open.

## Current State

- Action repo: `/Users/bwbrook/papers/dsipa-dev`
- Required packet-authoring branch: `main`
- Required packet-authoring HEAD and `origin/main`:
  `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`
- Required status before packet creation: clean (`## main...origin/main`)
- Accepted predecessor: Goal 014, committed and pushed
- Repository URL: <https://github.com/BWBrook/dsipa-dev>
- Repository visibility verified 2026-07-24: **private**
- Manuscript target: *Remote Sensing in Ecology and Conservation*
- Accepted manuscript title:
  **Detectable change in dark-sky integrity across Australia’s protected
  areas**
- Accepted archive route: Option B, Zenodo-style DOI, with no ALA
  redistribution exception
- Current external state (2026-07-26): Zenodo Dataset version `0.3.0` is
  public at <https://zenodo.org/records/21524637>; DOI
  <https://doi.org/10.5281/zenodo.21524637> resolves to it; public API status
  is `published`; the page shows exactly 12 flat files and 265.8 MB; public
  server MD5 values and downloaded bytes match local staging 12/12, downloaded
  `SHA256SUMS` passes 11/11, and all nine payloads match the frozen candidate
  by SHA-256, size, and bytes. The GitHub source repository remains private.

At the start of every later gate, record `pwd`, branch, HEAD, `origin/main`,
status, and the accepted Goal 015 packet state. The tracked history must
descend from the release baseline above and contain no unrelated change. Stop
before mutation if the worktree or upstream state cannot be explained exactly.
Do not reset, clean, overwrite, or absorb another person's work.

## Frozen Archive Identity

The accepted candidate is:

```text
artefacts/optionB_layerA_archive_candidate_2026-07-24/
```

Its data payload is exactly these nine files:

```text
data/processed/pa_radiance_buffers_national_v0_3_0.csv
data/processed/pa_edge_profiles_national_v0_3_0.csv
data/processed/pa_buffer_validity_v0_3_0.csv
data/processed/pa_trends_v0_3_0.csv
data/processed/pa_risk_rankings_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.gpkg
data/processed/pa_ibra_assignment_v0_3_0.csv
data/processed/pa_trend_bootstrap_summary_v0_3_0.csv
```

The nine payload files total exactly `265,783,139` bytes and have 9/9 accepted
Goal 011 SHA-256 checksums. Six are exact historical-hash matches. The accepted
non-exact radiance, edge-profile, and GPKG limitations must remain explicit:

- radiance is byte-different with no detected primary scientific drift, while
  direct historical row-level equality is unproven;
- edge profiles contain the accepted bounded threshold-sensitive difference,
  with current ring-1 feasibility `1,432/12.9%`; and
- the GPKG is byte-different with accepted within-run semantic identity, while
  direct historical feature-level equality is unproven.

`pa_risk_rankings_v0_3_0.csv` is categorical screening output under a legacy
filename. It is not a priority ranking.

The candidate contains the nine payloads plus only `README.md`,
`manifest.json`, and `SHA256SUMS`, for 12 logical deposit files. Raw ALA
downloads, row-level ALA occurrence data, Layer B payloads, and every unlisted
file are excluded.

The entire accepted Goal 014 candidate is frozen. Never add, remove, rename,
edit, regenerate, substitute, reserialize, normalize, recompress, or overwrite
any candidate path, including `README.md`, `manifest.json`, `SHA256SUMS`, or
any of the nine payload files. Stop on any path, count, byte-size, checksum,
classification, source-identity, ALA-exclusion, or Layer B-exclusion mismatch.
All Zenodo-facing presentation or metadata changes belong only in the separate
ignored deposit-staging view.

## Metadata And Rights Contract

Recommended deposit defaults are recorded in
`Release_Confirmation_Sheet.md`. Barry must approve or amend them before Gate
B. In particular:

- public ORCID evidence suggests Barry W. Brook is
  `0000-0002-2491-1517`, but Barry must confirm it;
- the repository MIT licence covers software and does not license the derived
  data archive;
- CAPAD 2024 and IBRA 7.1 are documented as CC BY 4.0;
- the actual OpenGeoHub/Zenodo VIIRS v0.4 inputs are CC BY 4.0;
- Natural Earth data are officially public domain; and
- CC BY 4.0 is therefore the recommended combined-archive licence, with
  explicit CAPAD, IBRA, OpenGeoHub/VIIRS, and Natural Earth provenance and
  attribution.

Current University of Tasmania policy indicates that the University
presumptively owns research data created by an employee in the course of
employment and that the Data Owner controls publication and licensing. The
recommended rights-holder text is therefore `University of Tasmania`, not
Barry personally, but this is not a legal determination. Gate B remains
blocked until Barry confirms both that this dataset falls under the applicable
policy and that he has the authority or approval to release it under CC BY
4.0. Stop if he cannot confirm that authority or supplies a materially
different rights position.

The GitHub repository is private. Its URL remains local provenance only while
the repository is private and must not be entered in Zenodo as a public access
link, public related identifier, alternate public identifier, or substitute
for the public Zenodo data record. Public code exposure is later scope. This
goal does not authorize a repository-visibility change.

## Hard Gates

### Gate A: Packet And Barry Confirmation Only

Authorized now:

- create the five Goal 015 packet files;
- present the compact confirmation sheet to Barry; and
- record Barry's later response in the live task before any next gate.

No Zenodo access, login, draft, upload, DOI reservation, DOI registration,
publication, packaging, checksum recalculation, candidate edit, build, test,
commit, push, or other external action is authorized in Gate A.

Gate A completion does not authorize Gate B. Gate B requires Barry to approve
or amend all required metadata and rights fields and explicitly write
`authorize draft`.

### Gate B: Authorized Draft, Upload, And Optional DOI Reservation

Gate B opens only after Barry:

1. confirms or corrects the creator, ORCID, affiliation, and sole-creator
   default;
2. confirms the exact rights-holder wording and his authority or approval to
   release under the selected licence;
3. supplies funding/grant metadata or explicitly confirms none;
4. approves or amends the remaining confirmation-sheet defaults; and
5. explicitly writes `authorize draft`.

That instruction authorizes only:

- fresh local revalidation of the frozen candidate;
- a deliberate, evidenced Zenodo file-presentation choice;
- preparation of deposit-specific metadata/provenance and, when needed, an
  ignored staging view;
- Zenodo account access, draft creation, upload of the 12 logical files, and
  draft inspection; and
- DOI reservation if needed to prepare the exact pre-publication data
  citation.

Official Zenodo guidance confirms multiple-file upload but does not document
preservation of directory paths. Do not assume nested paths survive. The
approved default is therefore a flat, direct-upload staging view with 12
individually downloadable files: the nine unique payload basenames preserved
byte-for-byte plus deposit-specific `README.md`, `manifest.json`, and
`SHA256SUMS` that map the flat names back to the accepted relative paths.
Create that view under ignored `artefacts/`; never flatten or otherwise change
the accepted candidate. Twelve files are below Zenodo's 20-or-more-file ZIP
recommendation. A ZIP or other packaging choice is permitted only if the live
service imposes a documented functional constraint and the alternative proves
payload identity and usable metadata.

After upload, independently download and SHA-256 verify all nine draft
payloads when feasible, prove the 12-file presentation, and show Barry the
exact draft files, metadata, creator, rights holder, licence, access, version,
date, description, attribution, and reserved DOI if one was requested.

**Do not publish in Gate B.** `authorize draft`, `proceed`, metadata approval,
silence, account login, upload success, or DOI reservation is never publication
authority.

Zenodo login, identity confirmation, and two-factor authentication may require
Barry's direct interaction. No password, recovery code, API token, session
cookie, account identifier, or other credential may be recorded in the
repository, packet, logs, screenshots, or task response.

### Gate C: Separate Explicit Publication Instruction

Gate C opens only after:

- the complete Gate B evidence has been shown to Barry;
- every draft mismatch has been resolved with at most one focused repair;
- Barry has inspected the final draft state; and
- Barry sends a new, separate instruction that explicitly contains the word
  `publish` and unambiguously refers to the verified Goal 015 Zenodo draft.

Never interpret `proceed`, `approved`, `looks good`, silence, a confirmation
sheet response, draft authorization, DOI reservation, or any earlier message
as publication authority.

Immediately before publication, re-open and re-check the exact draft files and
metadata. If they still match the accepted evidence, publish once. Stop after
any Zenodo error, ambiguity, or unexpected record state; do not create a
replacement record or repeat publication blindly.

### Gate D: Public Verification, Citation Reconciliation, And Git Closeout

Gate D starts only after Zenodo confirms successful publication. Then:

1. independently verify DOI resolution and the public record;
2. verify public file names, count, accessibility, payload bytes, and all nine
   payload SHA-256 values by full download when feasible;
3. verify the public creator, ORCID, affiliation, title, description, date,
   version, access, licence, rights holder, keywords, source attribution, and
   related identifiers;
4. capture the canonical Zenodo citation and public URL;
5. update only the authorized tracked release, Zenodo, data-accessibility,
   citation, confirmed-author, goal, and chronology surfaces;
6. keep the public Zenodo dataset distinct from the still-private GitHub source
   repository;
7. run focused tests and rebuild the targeted RSEC draft, submission, and
   supplementary outputs;
8. perform one focused repair pass only if a material defect is found;
9. obtain orchestrator review and acceptance; and
10. stage exact paths, commit, and push `main` only after that acceptance.

Commit and push are authorized within Gate D only after all public verification,
build, test, footprint, and orchestrator-acceptance checks pass. No tag,
GitHub release, GitHub visibility change, Wiley login or submission, journal
fee, open-access agreement, or journal licence action is authorized.

## Permitted Mutation Boundary

### Gate A now

Only:

```text
docs/goals/015-zenodo-doi-release-final-data-citation/Goal.md
docs/goals/015-zenodo-doi-release-final-data-citation/Plan.md
docs/goals/015-zenodo-doi-release-final-data-citation/Runbook.md
docs/goals/015-zenodo-doi-release-final-data-citation/Log.md
docs/goals/015-zenodo-doi-release-final-data-citation/Release_Confirmation_Sheet.md
```

### Gate B ignored working evidence

- `artefacts/optionB_layerA_zenodo_deposit_staging_2026-07-24/`
- `artefacts/goal015_zenodo_evidence/`

The accepted Goal 014 candidate is immutable in full. No candidate file or path
may be added, removed, renamed, or amended, including `README.md`,
`manifest.json`, `SHA256SUMS`, and all nine payloads. If a verified Zenodo
requirement cannot be represented in the separate ignored staging view, stop
and return the constraint to Barry; do not change the candidate.

### Gates B-D tracked release and citation surfaces

- `analysis/reports/zenodo_optionB_metadata_2026-07-24.md`
- `analysis/reports/zenodo_release_checklist_2026-07-24.md`
- `analysis/reports/zenodo_optionB_publication_receipt.md`
- `analysis/reports/zenodo_optionB_publication_receipt.json`
- `analysis/reports/final_release_manifest.md`
- `README.md`, release/data-accessibility paragraph only
- `data/README.md`
- `docs/decisions.md`
- `docs/stage_overview.md`
- `manuscript/text/manuscript_draft.md`, Data accessibility section only
- `manuscript/submission/rsec/declarations_draft.md`, Data Accessibility and
  archive-rights fields only
- `manuscript/submission/rsec/submission_metadata.md`, data DOI, source
  provenance, and archive-rights fields only
- `manuscript/submission/rsec/submission_checklist.md`, data-accessibility and
  archive-licence rows only
- `manuscript/submission/rsec/submission_counts.md`, Data accessibility count
  only if the final wording changes it
- `manuscript/submission/rsec/cover_letter_draft.md`, data DOI and
  source-provenance placeholder only
- `manuscript/authors.yaml` and
  `manuscript/submission/rsec/submission_authors.yaml`, only for exact
  identity fields Barry has expressly confirmed
- the five Goal 015 files listed above
- `docs/log/135_zenodo_doi_release.md` as the single chronology log

The accepted Goal 014 dated archive manifests are immutable historical
evidence and must not be edited:

```text
analysis/reports/optionB_layerA_archive_manifest_2026-07-24.md
analysis/reports/optionB_layerA_archive_manifest_2026-07-24.json
```

The two new publication receipts must record the actual public DOI, record URL,
publication date, exact public file evidence, and verified public metadata.

No manuscript Results, Methods, Discussion, references, tables, captions,
figures, scientific claims, analysis, code, tests, configuration, raw data,
processed data, or unrelated documentation may change.

## Acceptance Criteria

- Gate A has exactly the five-file packet footprint and no external action.
- Barry's confirmation is explicit, complete, and recorded before Gate B.
- Rights-holder wording and release authority are confirmed; uncertainty
  blocks release.
- Candidate identity passes exact 12-file inventory, nine-payload allowlist,
  `265,783,139` payload bytes, 9/9 SHA-256 checks, six exact/three accepted
  non-exact classifications, categorical-screening wording, and ALA/Layer B
  exclusion.
- The file-presentation decision is deliberate and proved; nested paths are
  not assumed, and flat staging does not mutate any payload byte.
- The Zenodo draft evidence shows the exact 12 logical files and all confirmed
  metadata. All 12 server-computed MD5 values equal the local staged-file MD5
  values, including the repaired companions. Full remote-download SHA-256
  verification remains a later public verification item. The final preview
  displays `Brook, Barry W.` exactly, matching the required creator; ORCID,
  sole-creator status, and exact affiliation are correct. The preview-labelled
  date is normalized to `2026-07-26` while the record remains unpublished.
- Gate B ends without publication.
- Gate C has a separate, unambiguous Barry instruction containing `publish`.
- The public DOI resolves and the public record is independently inspected.
- All nine public payloads pass full downloaded SHA-256 verification when
  feasible; file count, payload bytes, companions, metadata, access, licence,
  creator, attribution, date, and version match.
- Final tracked DOI/data-citation text uses the actual public record and does
  not imply the private GitHub repository is public.
- The accepted Goal 014 candidate and dated archive manifests remain unchanged,
  and the actual public DOI/date/file/metadata evidence is captured in the new
  Markdown and JSON publication receipts.
- Focused RSEC contract tests and draft/submission/supplementary checks and
  builds pass with current DSIPA/Makedoc provenance.
- `git diff --check`, exact changed-footprint review, staged-diff review, and
  final clean-status checks pass.
- Orchestrator acceptance precedes exact-path commit and push; local HEAD,
  upstream, `origin/main`, and remote `main` reconcile afterward.
- One core pass plus at most one focused material repair is used. Stop rather
  than enter repeated polish loops.

## Stop Conditions

Stop and report exact evidence on:

- any baseline, upstream, candidate path, count, size, checksum,
  classification, ALA, or Layer B mismatch;
- any unconfirmed creator, ORCID, affiliation, contributor, rights holder,
  release authority, licence, funding, access, version, or date;
- any unexpected Zenodo file transformation, missing file, duplicate record,
  metadata drift, login/2FA boundary, publication ambiguity, or service error;
- any request to record credentials or expose the private GitHub repository;
- any attempt to treat draft authorization as publication authority;
- any science, code, data, Wiley, GitHub release, fee, or OA scope expansion;
  or
- any material validation failure that remains after one focused repair.

## Non-Goals

No new science, analysis, data regeneration, serialization, raw or row-level
ALA redistribution, Layer B publication, repository visibility change, Git
tag/release, Wiley submission, journal fee, open-access agreement, journal
licence choice, or broad cleanup/refactor is part of Goal 015.

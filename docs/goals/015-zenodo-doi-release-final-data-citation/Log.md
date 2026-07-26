# Log: Goal 015 Zenodo DOI Release And Final Data Citation

## 2026-07-24 - Gate A Packet Creation

### Observed baseline

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD:
  `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`
- `origin/main`:
  `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`
- Starting status: clean (`## main...origin/main`)
- Goal 014: accepted, committed, and pushed

### Accepted starting evidence

- Option B with no ALA redistribution exception remains the selected route.
- The ignored candidate is
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`.
- It contains nine Layer A payloads plus `README.md`, `manifest.json`, and
  `SHA256SUMS`.
- The entire candidate, including all paths and all 12 files, is immutable;
  every deposit-facing change belongs in a separate ignored flat staging view.
- Accepted payload total: `265,783,139` bytes.
- Accepted payload hashes: 9/9.
- Classification: six exact historical-hash matches and three accepted
  non-exact files.
- The legacy risk-rankings file is categorical screening output, not a
  priority ranking.
- Raw/row-level ALA and Layer B payloads are excluded.
- At Gate A packet creation, no Zenodo draft, upload, reserved DOI, minted DOI,
  or published record existed; this was superseded by the later Gate B draft
  session recorded below.
- The GitHub source repository is private; Goal 015 does not authorize a
  visibility change, and its URL remains local provenance only while private.

### Rights and metadata evidence

- The repository MIT licence is software-only for this release decision.
- CAPAD 2024 and IBRA 7.1 are documented CC BY 4.0.
- OpenGeoHub/Zenodo VIIRS v0.4 is documented CC BY 4.0.
- Natural Earth data are officially public domain.
- CC BY 4.0 is the recommended derived-archive licence, subject to confirmed
  institutional authority and explicit source attribution.
- Current UTas policy makes `University of Tasmania` the presumptive data
  rights-holder wording, subject to Barry confirming applicability and his
  authority or approval to release under CC BY 4.0.
- Public ORCID evidence suggests `0000-0002-2491-1517` for Barry W. Brook;
  Barry must confirm it.

### Gate status

| Gate | Status | Evidence or blocker |
| --- | --- | --- |
| A: packet and confirmation | prepared | Exactly five packet files authorized; confirmation still required. |
| B: draft/upload/reservation | blocked | Requires complete Barry metadata/rights confirmation and literal `authorize draft`. |
| C: publication | blocked | Requires accepted Gate B evidence and a later separate instruction containing `publish`. |
| D: public verification/citation/Git | blocked | Requires successful authorized publication and independent public verification. |

### Actions not performed

No candidate edit, checksum recalculation, packaging, data processing, build,
test, commit, push, authenticated Zenodo account/deposit action, draft, upload,
DOI action, publication, external mutation, Git tag/release, GitHub visibility
change, Wiley action, fee, or open-access agreement occurred during packet
creation.

Official public Zenodo, Natural Earth, Creative Commons, DCCEEW, and UTas
documentation was checked, together with a read-only GitHub visibility query.
Those checks were public/read-only and made no authenticated Zenodo deposit or
other external mutation.

## Future Execution Logging Contract

Append a dated checkpoint after each gate. Each checkpoint must separate:

1. observed facts and exact evidence;
2. Barry-provided metadata and authorization;
3. executor inference or recommendation;
4. files or external state changed;
5. validation commands and results;
6. stop conditions, residual uncertainty, and repair count; and
7. exact Git state.

### Gate B checkpoint must record

- Barry's confirmation and `authorize draft` authority;
- rights-holder and release-authority wording;
- candidate 12-file inventory, 9/9 hashes, payload bytes, classifications, and
  exclusions;
- approved flat file-presentation mapping, or the documented live-service
  constraint returned to Barry before any packaging exception;
- exact draft metadata/files evidence and remote 9/9 payload verification;
- whether a DOI was reserved; and
- an explicit statement that publication did not occur.

Do not record credentials, tokens, cookies, account identifiers, email, 2FA
material, or other private authentication state.

## 2026-07-24 - Gate B Authorization And Local Staging

### Barry-confirmed facts and authority

- Barry approved all recommended confirmation-sheet defaults.
- Creator: `Brook, Barry W.`, sole creator.
- ORCID: `0000-0002-2491-1517`.
- Affiliation: School of Natural Sciences, University of Tasmania, Hobart,
  Tasmania, Australia.
- Rights holder: University of Tasmania.
- Barry confirmed that the dataset falls under the applicable University of
  Tasmania policy and that he has authority or approval to release it under
  CC BY 4.0.
- Funding: none associated with a specific grant.
- Barry wrote `authorise draft`; this was accepted as the unambiguous British
  English equivalent of the Gate B phrase `authorize draft`.
- This authority covers draft creation, upload, inspection, and optional DOI
  reservation only. It does not authorize publication.

### Observed Git baseline

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD and `origin/main`:
  `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`
- Gate B starting status: only the five untracked Goal 015 packet files;
  no unrelated tracked or untracked change.

### Observed candidate evidence

- Frozen candidate:
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`.
- Exact inventory: nine payload files plus `README.md`, `manifest.json`, and
  `SHA256SUMS`.
- Candidate checksums: 9/9 payloads `OK`.
- Payload total: `265,783,139` bytes.
- Classification: six historical-hash exact and three accepted non-exact.
- The radiance, edge-profile, and GPKG limitations remain explicit.
- `pa_risk_rankings_v0_3_0.csv` remains categorical screening output, not a
  priority ranking.
- Exact payload-path scans found zero raw/row-level ALA and zero Layer B
  payloads.
- Before/after SHA-256 comparisons proved that all 12 candidate files,
  including all three candidate companions, remained unchanged.

### Local staging created

- Flat ignored staging:
  `artefacts/optionB_layerA_zenodo_deposit_staging_2026-07-24/`.
- Exactly 12 unique root-level files and zero nested files.
- Nine payloads copied byte-for-byte to unique basenames.
- Candidate-to-staging payload comparison: 9/9 byte sizes and SHA-256 values
  match.
- Staged payload total: `265,783,139` bytes.
- Deposit-specific companions: publication-ready `README.md`, structured
  `manifest.json`, and `SHA256SUMS`.
- `SHA256SUMS`: 11/11 other staging files verified.
- SHA-256 of staging `SHA256SUMS`:
  `056720a6c50063b88288d373131d36ec9964fafdd0fc889d072cf9114fefd354`.
- Machine-readable verification:
  `artefacts/goal015_zenodo_evidence/local_staging_verification.json`.

### Metadata decision

- Dataset title:
  `Australian protected-area dark-sky integrity outputs, 2013-2024`.
- Version: `0.3.0`; language: English.
- Publication date remains a policy field: use the actual date the record is
  first made public.
- Access is open/public with no embargo; licence is CC BY 4.0.
- Contributors and community: none.
- Six confirmed keywords are recorded.
- OpenGeoHub DOI `10.5281/zenodo.17294744` is prepared as `IsDerivedFrom` if
  the live interface supports that relation.
- No manuscript DOI exists.
- The private GitHub URL remains local provenance only and is not represented
  as public metadata or access.

### Validation and external state

- Candidate inventory/checksum/manifest assertions: pass.
- Flat staging count, uniqueness, root-level layout, and payload byte total:
  pass.
- Candidate-to-staging payload comparisons: 9/9 pass.
- Staging `SHA256SUMS`: 11/11 pass.
- Staging manifest and local evidence JSON parse and `jq` assertions: pass.
- ALA/occurrence/Layer B payload filename scans: zero matches.
- Candidate immutability comparison: pass.
- Focused repair count: zero.
- At this local-staging checkpoint, before the later authenticated draft
  session, no network, browser, Zenodo account, draft, upload, DOI reservation,
  DOI registration, publication, build, test, commit, push, tag, release,
  repository-visibility change, or Wiley action had occurred.

At this local-staging checkpoint the deposit was ready for orchestrator-
controlled Zenodo draft work. The later draft session is recorded below; at
that checkpoint Gate C remained closed pending companion repair, Barry's review
of the complete verified draft, and a later, separate instruction explicitly
containing `publish`.

## 2026-07-24 - Gate B Zenodo Draft, Upload, Reservation, And Preview

### Observed draft evidence

- Draft URL: <https://zenodo.org/uploads/21524637>.
- Draft saved without validation errors and remained in draft state.
- Preview banner was visible. The Publish control became enabled but was not
  clicked.
- Reserved DOI: `10.5281/zenodo.21524637`. It is reserved for the draft but is
  unregistered until publication and is not yet a public DOI.
- Initial provisional draft publication-date field/preview: `2026-07-24`;
  superseded by the `2026-07-26` normalization recorded below. Any actual
  publication date must still be the date the record is first made public.
- The exact evidence is mirrored in ignored
  `artefacts/goal015_zenodo_evidence/zenodo_draft_21524637.json`.

### Confirmed draft metadata

- Dataset; title `Australian protected-area dark-sky integrity outputs,
  2013-2024`; version `0.3.0`; English; publisher Zenodo.
- Sole creator `Brook, Barry W.` (displayed `Brook, Barry`), ORCID
  `0000-0002-2491-1517`, exact affiliation `School of Natural Sciences,
  University of Tasmania, Hobart, Tasmania, Australia`.
- Open/public access, no embargo; CC BY 4.0; copyright `Copyright (C) 2026
  University of Tasmania.`; rights holder University of Tasmania.
- Funding, contributors, and community: none.
- Keywords exactly: artificial light at night; protected areas; VIIRS;
  Australia; remote sensing; dark-sky integrity.
- Related work: `10.5281/zenodo.17294744`, `Is derived from`, DOI scheme,
  Dataset resource type.
- Description retains the nine processed Layer A outputs, six exact/three
  accepted non-exact reproduction status, categorical-screening interpretation,
  and exclusion of raw/row-level ALA, Layer B, and unlisted files.

### Draft files and upload recovery

- Preview showed exactly 12 flat files and 265.8 MB total. All 12 Zenodo
  server-computed MD5 values matched local staged-file MD5 values exactly;
  the complete file/size/hash table is in
  `analysis/reports/zenodo_optionB_metadata_2026-07-24.md` and the ignored
  JSON evidence file.
- The initial concurrent upload returned 502/504 errors. Incomplete
  placeholders were removed; only the five failed files were retried, with
  four smaller files together and the 132.57 MB GPKG alone. The final preview
  showed all 12 files with server checksums and sizes. This is operational
  evidence, not a dataset caveat.
- No raw or row-level ALA files, Layer B payloads, or unlisted files are in the
  deposit boundary. Local pre-upload evidence remains 9/9 candidate payload
  SHA-256 matches and `SHA256SUMS` verifies the other 11 files.

### Gate status and caveat

- Draft creation, upload, DOI reservation, companion repair, and preview
  inspection are complete. Technical and metadata Gate B evidence is complete.
- The repaired remote and local `manifest.json` are 11,705 bytes with SHA-256
  `787c56fba9226444e77dd97f6f8351743ed0d1b77284217c7b8d8109f4469192` and MD5
  `fa9336e01fb4928160276b216a7b7649`; repaired `SHA256SUMS` is 1,025 bytes
  with SHA-256 `2317be0fe88b1c6792fd9dda89aa6a7607bfd09e2747166596312449990ff260`
  and MD5 `0a04012a3d7ed43f4ff66ce26b6f4875`.
- All 12 final preview MD5 values match current local flat staging exactly;
  `SHA256SUMS` verifies 11/11, payload identity is 9/9, candidate identity is
  unchanged 12/12, and exclusions remain zero raw/row-level ALA and zero
  Layer B. The final remote manifest contains the publication-ready canonical
  landing-page status and stable external-state policy; stale false claims are
  absent.
- Publication, DOI registration/resolution, public download verification,
  manuscript citation insertion, RSEC rebuild/test, commit, push, and
  release/tag work remain incomplete. Publication requires a later, separate
  instruction containing the word `publish`.

### Final metadata review: creator-name mismatch resolved

- An earlier preview displayed `Brook, Barry` because ORCID autocomplete
  populated given names as `Barry`; the confirmed/required creator was
  `Brook, Barry W.`. ORCID `0000-0002-2491-1517`, sole-creator status, and exact
  affiliation were correct throughout.
- On 2026-07-26 the authenticated draft was corrected to given names `Barry W.`
  and re-previewed. The final preview now displays `Brook, Barry W.` exactly.
- The draft publication-date field was normalized to `2026-07-26`; the preview
  label `Published July 26, 2026 | Version 0.3.0` is not an actual publication
  event, and the record remains unpublished.
- Technical and metadata Gate B evidence is complete. Publication, DOI
  registration/resolution, public download verification, manuscript citation
  insertion, RSEC rebuild/test, commit, push, and release/tag work remain
  incomplete. Gate C remains closed until Barry sees the final evidence and
  sends a later, separate instruction containing `publish`.

### Gate C checkpoint must record

- the later, separate publication instruction and why it satisfies the gate;
- final pre-publication recheck evidence;
- publication action and service outcome; and
- any ambiguity or error that caused an immediate stop.

### Gate D checkpoint must record

- public DOI resolution and record evidence;
- the Markdown and JSON Zenodo publication receipts containing the actual
  public DOI/date/file/metadata evidence;
- public 12-file inventory, all feasible download hashes, payload bytes, and
  metadata/licence/creator/attribution verification;
- exact tracked DOI/data-citation changes;
- private-source/public-data distinction;
- focused tests, RSEC checks/builds, and generated provenance;
- one focused repair, if any;
- orchestrator review and acceptance;
- exact staged footprint, commit, push, and remote reconciliation; and
- material residual limitations and highest-value next action.

Also append one concise chronology entry to
`docs/log/135_zenodo_doi_release.md` during Gate D. Do not create additional
chronology logs for this goal.

## 2026-07-26 - Gate C Publication And Preliminary Gate D Reconciliation

### Gate C and publication

- The orchestrator confirmed that the separate Goal 015 Gate C publication
  authority had been satisfied for the verified draft.
- The draft was published once. Zenodo now reports the record as `published`
  with publication date `2026-07-26`.
- Public record: <https://zenodo.org/records/21524637>
- Resolving DOI: <https://doi.org/10.5281/zenodo.21524637>
- No replacement record, Git tag/release, repository-visibility change, Wiley
  action, fee, open-access agreement, or journal licence action occurred.

### Preliminary public evidence

- Public metadata matches the confirmed contract: Dataset; version `0.3.0`;
  exact title; sole creator `Brook, Barry W.`; ORCID
  `0000-0002-2491-1517`; exact University of Tasmania affiliation; open access
  with no embargo; CC BY 4.0; University of Tasmania rights holder; exact
  copyright; six keywords; no funding, contributors, or community; and
  `10.5281/zenodo.17294744` as `isDerivedFrom` a Dataset.
- The canonical APA citation is:
  `Brook, B. W. (2026). Australian protected-area dark-sky integrity outputs,
  2013-2024 (Version 0.3.0) [Dataset]. Zenodo.
  https://doi.org/10.5281/zenodo.21524637`.
- The public page shows exactly 12 flat files and 265.8 MB. All 12 public
  server MD5 values match the current local flat staging.
- The deposit remains nine processed Layer A payloads plus three companions:
  zero raw/row-level ALA, zero Layer B, and zero unlisted files. The GitHub
  source repository remains private and is not represented as public code.

### Public verification, tracked reconciliation, and remaining Gate D work

- Baseline at reconciliation start: repository
  `/Users/bwbrook/papers/dsipa-dev`, branch `main`, HEAD and `origin/main`
  `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`.
- The already modified Gate B metadata/checklist and untracked five-file Goal
  015 packet were preserved and extended in place. Only the Gate D-authorized
  release, data-accessibility, archive-rights, goal-status, and chronology
  surfaces were changed.
- The manuscript Data accessibility wording preserves the exact accepted
  counts: 4,609 IMRAD words and 4,685 words including Data accessibility.
- Full public re-acquisition downloaded 12 files totalling `265,798,999` bytes.
  API sizes and server MD5 values match 12/12; downloaded files are
  byte-identical to flat staging 12/12; downloaded `SHA256SUMS` passes 11/11;
  and all nine payloads match the frozen candidate by SHA-256, size, and bytes.
  The downloaded manifest is valid, public metadata assertions pass 24/24, and
  exclusions remain zero raw ALA, zero row-level ALA, zero Layer B, and zero
  unlisted files.
- The initial local-resolver failure, later Cloudflare DNS-over-HTTPS A-record
  response, and successful pinned host/SNI route are retained as transport
  chronology, not a dataset limitation. The positive ignored receipt is
  `artefacts/goal015_zenodo_evidence/public_verification_2026-07-26.json`.
- Focused RSEC validation and all draft/submission/supplementary checks and
  builds passed at the final Gate D checkpoint below. Exact-path staging,
  commit, push, and remote reconciliation remain orchestrator-owned.

## 2026-07-26 - Final Gate D Validation Checkpoint

- `analysis/reports/zenodo_optionB_publication_receipt.json` parses; the focused
  RSEC pytest selection passes 13 tests.
- The `draft`, `submission`, and `supplementary` profiles all pass both
  `ms-check` and `ms-build`. Each profile check ran 61 Makedoc tests;
  manuscript lint, reference audit, and author injection passed. The main
  profiles report 31 bibliography keys, 25 cited keys, zero unknown keys, and
  six non-fatal unused keys; supplementary reports zero cited and zero unknown.
- The first draft check exposed a manual author-year dataset citation. One
  focused, orchestrator-authorized material repair replaced it with
  `@brook2026dsipa` and added one CSL-YAML dataset record in
  `references/refs.yaml`. This narrow repair was required by Makedoc lint and
  proper dataset citation; it is not a bibliography expansion or scientific
  change. The explicit DOI and all private-source, ALA, and Layer B boundaries
  are preserved. The full validation matrix passed on rerun.
- The four documented count commands were rerun after that repair: abstract
  235, IMRAD 4,609, IMRAD plus Data accessibility 4,685, and five keywords.
  The current submission count, metadata, checklist, and Goal 015 log surfaces
  were reconciled to the verified 4,685 value.
- Generated outputs: draft PDF 36 pages/`1,171,965` bytes and DOCX
  `1,065,264`; submission PDF 27 pages/`492,527` and DOCX `421,505`;
  authoritative SI PDF 14 pages/`723,377`, with diagnostic SI DOCX `655,550`.
  Focused visual/text inspection passed for the submission front page, Data
  accessibility/DOI/reference rendering, SI front page, and wide table; no
  overlap or clipping defect was found.
- Build manifests record DSIPA source provenance at baseline HEAD
  `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`, branch `main`, dirty as expected,
  and clean Makedoc
  `3a52e7059fb069c854b49d8f0a1991aface33d75` on `main`.
- `git diff --check` passes. Public verification and focused validation/builds
  are complete. Git commit/push has not occurred; exact-path Git closeout and
  subsequent remote reconciliation are the only remaining orchestrator-owned
  Goal 015 actions.
- Human/Wiley, Git tag/release, and repository-visibility gates remain
  unchanged.

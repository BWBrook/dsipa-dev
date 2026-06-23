# Release Blocker Decision Packet

Status: decision packet only. This document does not authorize archive upload,
DOI minting, release packaging, GitHub release, publication submission, remote
compute, data reruns, figure regeneration, or large-file movement.

Generated: 2026-06-23 by `nightlight` for Goal 009.

## Executive Recommendation

Recommended path: approve a later, separate release-execution goal that pairs
the tracked source/manuscript repository with an external archive for the
`archived-proposed` large Layer A outputs, plus a checksum manifest and a
refreshed evidence reconciliation for the current tracked figure set.

Keep raw ALA downloads and row-level processed ALA occurrence tables
restricted/excluded by default. Do not redistribute them unless Barry and the
orchestrator later record a specific permission basis and publication need.

No-move remains in force for archive upload, DOI minting, release packaging,
GitHub release, and publication submission until Barry/orchestrator approve the
archive scope and a future release-execution goal verifies the payload.

## Current Evidence State

Goal 009 starts from the accepted Goal 008 checkout:

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD: `91cd628`
- Remote-tracking HEAD: `origin/main` at `91cd628`
- Starting status: `## main...origin/main` plus the untracked Goal 009 packet.

Goal 008 was command-green for the local manuscript/test/build surfaces:

- `make ms-check`: passed.
- `make test`: passed, `40 passed, 9 skipped`.
- `make build`: passed, producing package artefacts under `/tmp/dsipa-build`.

Goal 008 also correctly found that the checkout was not release-clean. The
local evidence reconciliation at `9082f4f` wrote only to `/tmp` and reported 38
required expected files, 28 present, 27 checksum-verified, 10 missing required
files, and one checksum mismatch against the older evidence snapshot.

The 10 missing local files were:

- `data/processed/pa_geometries_v0_3_0.gpkg`
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `data/processed/pa_trends_v0_3_0.csv`
- `data/processed/pa_risk_rankings_v0_3_0.csv`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`

The first eight are large Layer A release/archive candidates. The final two
are row-level Layer B occurrence tables and should remain restricted/excluded
by default.

The tracked baseline figure checksum mismatch is evidence-snapshot staleness,
not figure drift:

- Current tracked `manuscript/figures/fig_layerA_baseline_map.png` SHA-256:
  `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`
- Older evidence snapshot expected SHA-256:
  `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`
- Stage 4C traced the change to accepted Stage 2 figure work in commit
  `896131a`.

The older deep-server evidence snapshot remains useful but not final:

- `analysis/reports/evidence_reconciliation.md` was generated at
  `f73156272104ed16b0506617fc423e5c6478f50e` with `dirty=true`.
- It verified 38/38 expected files, but predates accepted Stage 2 figure and
  Stage 4 release-state updates.
- Goal 008 review corrected inherited checksum mismatches in
  `analysis/reports/final_release_manifest.md`; the manifest now matches
  `analysis/reports/evidence_reconciliation.json` for compared rows.

## Decision Table

| Owner | Decision needed | Recommended option | Alternatives | Risks and trade-offs |
| --- | --- | --- | --- | --- |
| Barry | Approve final archive scope. | Archive tracked source/manuscript through the repo and archive the `archived-proposed` large Layer A outputs externally with checksums. | Source/manuscript-only release; broader reproducibility bundle. | Source-only is faster but weakens reproducibility. A broader bundle adds operational and licensing risk. |
| Barry | Choose archive/DOI route. | Use the existing Zenodo-oriented path unless Barry prefers an institutional repository. | Institutional archive; no DOI until later. | Zenodo is already scaffolded by the checklist. Institutional route may fit local policy but needs fresh process work. No DOI weakens publication data availability. |
| Barry | Decide whether raw ALA or row-level processed ALA data can be shared. | No sharing by default; keep raw ALA downloads and row-level processed occurrence tables restricted/excluded. | Explicit permission route for selected ALA material. | Sharing without permissions creates legal/licensing risk. Permission work may delay release and is not necessary for the current manuscript claims. |
| Orchestrator | Authorize the next goal type. | Open a release-execution goal only after Barry approves archive scope and route. | Split into an archive-scope confirmation goal and a later execution goal. | A single execution goal is efficient if decisions are clear; a split goal is safer if Barry changes scope. |
| Future release-execution goal | Verify payload and refresh evidence. | Verify `archived-proposed` Layer A files, current tracked figure checksums, and checksum manifest before any DOI/publication wording changes. | Re-run pipelines; source-only release. | Verification is lower risk than rerun. Pipeline reruns introduce new science/artefact drift and should be avoided unless verification fails. |

## Archive-Scope Options

### Option A: Minimum Source/Manuscript-Only Release

Content:

- tracked repository source;
- manuscript text and tracked figures;
- small tracked reports and derived Layer B summaries.

Pros:

- fastest;
- avoids large-file movement;
- avoids archive upload and DOI work.

Cons:

- leaves R02 and R05 effectively unresolved;
- paper-facing data availability would need to say users must regenerate or
  request large outputs;
- weaker reproducibility story for Layer A national results.

Recommendation: not preferred unless publication timing forces a minimal
submission package and Barry accepts the reproducibility limitation.

### Option B: Recommended Source/Manuscript Plus Layer A Archive

Content:

- tracked repository/manuscript source through git/GitHub;
- external archive containing the `archived-proposed` large Layer A national
  outputs:
  - `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
  - `data/processed/pa_edge_profiles_national_v0_3_0.csv`
  - `data/processed/pa_buffer_validity_v0_3_0.csv`
  - `data/processed/pa_trends_v0_3_0.csv`
  - `data/processed/pa_risk_rankings_v0_3_0.csv`
  - `data/processed/pa_geometries_v0_3_0.csv`
  - `data/processed/pa_geometries_v0_3_0.gpkg`
  - `data/processed/pa_ibra_assignment_v0_3_0.csv`
  - `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
- SHA-256 manifest matching `analysis/reports/final_release_manifest.md`;
- refreshed evidence reconciliation that records the current tracked baseline
  figure checksum.

Pros:

- directly supports the primary Layer A contribution;
- uses checksums and archive surfaces already present in the repo;
- avoids redistributing raw/row-level ALA data.

Cons:

- requires authorized large-file staging/upload and DOI minting later;
- requires final evidence refresh before publication wording cites the DOI.

Recommendation: preferred.

### Option C: Full Reproducibility Bundle With Restricted-Data Exclusions

Content:

- Option B contents;
- additional regenerated artefact folders or state-run outputs if Barry wants a
  broader provenance bundle;
- explicit exclusions for raw ALA downloads and row-level processed ALA
  occurrence tables unless permissions are resolved.

Pros:

- strongest reproducibility posture;
- may help future reviewers inspect intermediate outputs.

Cons:

- larger, noisier, and more operationally fragile;
- increases archive curation burden;
- can blur which files are required for paper claims.

Recommendation: reserve for a later expansion only if Barry or a journal
requires it.

### Option D: Raw/Row-Level ALA Redistribution Exception

Content:

- raw ALA downloads or row-level processed Layer B occurrence tables.

Recommendation: reject by default. Only reconsider under a separate permission
and licensing goal that records provider terms and a publication need.

## DOI And Archive Route Recommendation

Existing repo evidence supports a Zenodo-style route:

- `analysis/reports/zenodo_release_checklist_2026-01-04.md` already lists the
  core national Layer A outputs and checksum-manifest steps.
- `data/README.md` already records source provenance and states that archive
  upload/DOI minting remain pending.
- `analysis/reports/final_release_manifest.md` already classifies
  `archived-proposed`, `restricted`, `excluded`, `tracked`, and `regenerated`
  surfaces.

Recommended route: use Zenodo or an equivalent DOI-minting research-data
archive for the Option B Layer A archive payload. If Barry has institutional
policy reasons to prefer a University of Tasmania or journal-linked repository,
that route is acceptable, but it should use the same payload and checksum
manifest.

No DOI may be cited in the manuscript, `data/README.md`, release manifest, or
publication materials until the archive record exists and the DOI has actually
been minted.

## Evidence-Refresh Plan For A Future Goal

A future release-execution goal should:

1. Record starting `pwd`, branch, HEAD, remote-tracking HEAD, and status.
2. Confirm Barry/orchestrator archive-scope and archive-route decisions.
3. Verify the current tracked baseline figure checksum:
   `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`.
4. Verify the `archived-proposed` Layer A outputs against
   `analysis/reports/final_release_manifest.md` and
   `analysis/reports/evidence_reconciliation.json`.
5. Generate or refresh a release checksum manifest for the archive payload.
6. Refresh evidence reconciliation or produce a final supplement from the
   accepted release state, including the current tracked figure hash.
7. Keep raw ALA downloads and row-level processed ALA occurrence tables out of
   the release package unless a separate permission decision says otherwise.
8. Update data/code availability wording only after the real DOI exists.

## Release-Execution Goal Outline

Prerequisites:

- Barry approves archive scope.
- Barry or the orchestrator chooses the archive/DOI route.
- Orchestrator authorizes large-file staging/upload and any remote or archive
  tooling needed.
- The source tree has an accepted release candidate commit.
- The future packet explicitly authorizes any commands that move, package,
  upload, mint, or publish.

Actions that should be considered in the later goal, if explicitly authorized:

- local and/or remote file-presence checks for the archive payload;
- SHA-256 verification for the `archived-proposed` Layer A outputs;
- checksum manifest generation for the archive payload;
- evidence reconciliation refresh or final supplement from the accepted release
  state;
- archive upload and DOI minting;
- data/code availability update with the real DOI;
- final `git diff --check`, manifest consistency scans, and release closeout.

Non-goals that should remain blocked even in the release-execution goal unless
separately authorized:

- new Layer A or Layer B science;
- pipeline reruns or figure regeneration as a convenience;
- ALA downloads or occurrence reprocessing;
- raw ALA or row-level processed ALA redistribution without a recorded
  permission basis;
- publication submission before the archive DOI and release state are final.

Stop conditions:

- any archived-proposed checksum mismatch that cannot be explained by an
  accepted evidence refresh;
- absence of required large files after the authorized retrieval/staging path;
- any pressure to cite a DOI before it exists;
- any requirement to redistribute restricted ALA material without explicit
  permission;
- any need for new science, manuscript rewriting, or figure/data regeneration.

## Risk Classification

| Risk class | Current risk | Recommended control |
| --- | --- | --- |
| Scientific | Release payload could drift from accepted evidence if files are rerun rather than verified. | Prefer checksum verification and evidence refresh over rerun; rerun only if verification fails and a new science goal authorizes it. |
| Legal/licensing | Raw ALA downloads and row-level occurrence tables have mixed provider terms. | Keep restricted/excluded by default; include only derived summaries and ledger/report surfaces. |
| Reproducibility | Source-only release would not carry large Layer A outputs supporting the main paper results. | Archive `archived-proposed` Layer A outputs with checksums. |
| Operational | Large-file staging/upload can create accidental payload drift. | Use a later release-execution packet with explicit file list, checksums, and stop conditions. |
| Publication process | Manuscript could cite an archive DOI before it exists. | Keep no-move until DOI is minted; update wording only after DOI creation. |

## Decisions For Barry

1. Approve the recommended Option B archive scope, or choose source-only /
   broader bundle.
2. Choose the archive route: Zenodo-style DOI archive, institutional archive,
   or deferred DOI.
3. Confirm that raw ALA downloads and row-level processed ALA occurrence tables
   remain excluded from the default release.
4. Decide whether publication timing requires a source-only interim submission
   despite weaker reproducibility.

## Recommended Next Goal

Open a narrowly scoped release-execution goal only after Barry/orchestrator
decisions are recorded. The goal should be titled along the lines of:

`Goal 010: Release Archive Execution And Evidence Refresh`

It should be authorized to verify and stage the approved Layer A archive
payload, refresh the evidence/checksum surface, mint or record the DOI if
approved, update data/code availability with the real DOI, and then stop. It
should not perform new science, pipeline reruns, ALA downloads, manuscript
rewriting, or restricted-data redistribution by default.

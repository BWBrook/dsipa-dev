# Plan: Goal 010 Option B Zenodo Archive Staging

## Purpose

Turn Barry's approved release decision into a verified, reviewable,
Zenodo-ready archive-staging package without performing any external upload,
DOI minting, or publication submission.

## Steps

1. Confirm current state.
   - Record `pwd`, branch/status, short HEAD, remote-tracking HEAD if
     available, Goal 010 packet presence, and local payload presence/absence.

2. Reconstruct the approved decision.
   - Read the Goal 010 packet and required context.
   - Treat Option B scope, Zenodo-style DOI route, and no ALA exception as
     decided.

3. Inventory the approved payload.
   - Check all nine approved Layer A files.
   - If files are missing locally, search only documented DSIPA project
     evidence locations.
   - Recover/copy missing approved files only if they can be matched to the
     pinned release checksums.

4. Build the archive evidence surface.
   - Compute sizes and SHA-256 checksums.
   - Create a human-readable archive manifest.
   - Create a machine-readable companion manifest.
   - Record source/recovery location and local staging location for every file.
   - Record explicit raw/row-level ALA exclusions.

5. Prepare Zenodo-style metadata.
   - Draft title, description, creators/contributors where safely inferable,
     keywords, provenance/licence notes, related identifiers, file-list
     wording, and checksum-manifest wording.
   - State clearly that the DOI is pending and must not be cited until minted.

6. Refresh release evidence/documentation.
   - Record Barry's decision in `docs/decisions.md`.
   - Update release-facing docs only where needed to distinguish "approved and
     staged/verified" from "uploaded/minted".
   - Address the accepted current baseline-figure checksum through a narrow
     release evidence supplement or a justified evidence-reconciliation update.

7. Validate.
   - Run `git diff --check`.
   - Run file-presence and checksum checks for Goal 010 deliverables.
   - Run script/Python tests only if the corresponding files changed.
   - Run targeted release-policy scans and classify hits.

8. Close out and wake the orchestrator.
   - Write `Stage4E_Closeout.md`.
   - Update Goal 010 log and stage log.
   - Send a wake-up that includes manifest paths, staging location, checksum
     status, ALA-exclusion status, and readiness for the later external
     upload/DOI-mint goal.

## Non-Goals

- No archive upload.
- No DOI minting or reservation.
- No final DOI citation.
- No GitHub release, publication submission, commit, push, merge, PR, or tag.
- No new science, data processing, modelling, figure regeneration, ALA
  downloads, full pipeline rerun, or remote compute run.
- No raw ALA or row-level processed ALA redistribution.

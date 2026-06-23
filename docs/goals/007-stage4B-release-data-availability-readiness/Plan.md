# Plan: Goal 007 Stage 4B Release Readiness

## Purpose

This plan turns the accepted Stage 4B recommendation into a local
release-readiness audit and decision surface. The output should make the
project safer to publish later without doing the publication step now.

## Steps

1. Confirm current state.
   - Record `pwd`, branch/status, short HEAD, and Goal 007 packet presence.

2. Reconstruct the release contract.
   - Read the Goal 007 packet and required files.
   - Extract the open Stage 4B items: B01, B11, R01, R02, R05, R09, and any
     relevant R04/R08 notes.

3. Audit existing release wording.
   - Check `data/README.md`, README, manuscript data availability,
     reproducibility audit, evidence reconciliation, Zenodo checklists, and
     decisions.
   - Identify stale "already archived" wording versus archive-pending wording.

4. Build the release manifest.
   - Classify artefacts as tracked, archived-proposed, regenerated, excluded,
     or restricted.
   - Include large Layer A outputs, tracked figures/reports, small derived
     Layer B summaries, raw ALA downloads, and row-level processed ALA tables.
   - Record checksum and provenance sources.

5. Align data availability.
   - Update `data/README.md` and any needed README/manuscript data-availability
     wording.
   - Avoid final DOI or archive claims.

6. Record policy.
   - Add a decision note if needed.
   - Update Stage 1 matrix statuses only where justified.
   - Keep Barry-level decisions explicit.

7. Validate.
   - Run `git diff --check`.
   - Run file-existence checks.
   - Run `make ms-check` only if manuscript data availability changed.
   - Run and classify release/licence/checksum scans.

8. Close out.
   - Write `docs/log/127_stage4B_release_data_availability.md`.
   - Write `Stage4B_Closeout.md`.
   - Append `Log.md`.
   - Wake the DSIPA orchestrator and stop.

## Non-Goals

- No archive upload or DOI minting.
- No release packaging or GitHub release.
- No data reruns, data processing, ALA downloads, modelling, or remote compute.
- No moving/copying/compressing large ignored outputs.
- No raw ALA or row-level processed ALA redistribution decision unless
  explicitly authorized later.
- No package builds, full pytest, or final publication tooling.
- No commit or push.

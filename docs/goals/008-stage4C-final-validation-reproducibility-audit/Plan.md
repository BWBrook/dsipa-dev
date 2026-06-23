# Plan: Goal 008 Stage 4C Final Validation

## Purpose

This plan turns the accepted Stage 4C contract into a local validation and
reproducibility-audit pass. The output should tell the DSIPA orchestrator what
is proven, what is blocked by publication decisions, and what the next move
should be.

## Steps

1. Confirm current state.
   - Record `pwd`, branch/status, short HEAD, remote-tracking HEAD if
     available, and Goal 008 packet presence.

2. Reconstruct the Stage 4C contract.
   - Read the Goal 008 packet and required files.
   - Identify open or release-gate rows: R01, R02, R04, R05, R08, M03, and any
     Stage 4 exit-gate row touched by validation.

3. Run command validation.
   - Run `git diff --check`, `make ms-check`, `make test`, and `make build`.
   - Run the evidence-reconciliation command to `/tmp` if possible.
   - Capture exact pass/fail/skip outcomes.

4. Run manual scans.
   - Claim discipline.
   - Caption/table denominator discipline.
   - Release/licence/checksum discipline.
   - Reference hygiene.
   - Release-manifest consistency.
   - Classify every material hit.

5. Write the validation report.
   - Include command evidence, scan classifications, blocker table, and
     move/no-move recommendation.

6. Write the reproducibility supplement.
   - Record current commit, clean/dirty state, relation to the pre-final audit,
     large-output assumptions, and expected compute class for future full rerun.

7. Update governance surfaces.
   - Update the matrix only where validation justifies it.
   - Update stage overview only if Stage 4C status should be recorded.
   - Apply only narrow factual provenance corrections to the release manifest
     if validation proves they are needed.

8. Close out.
   - Write the Stage 4C log and closeout.
   - Append this goal log.
   - Wake the DSIPA orchestrator and stop.

## Non-Goals

- No new science, data reruns, ALA downloads, modelling, or figure regeneration.
- No manuscript rewrite or source/test edits.
- No remote compute, SSH probing, deep-server sync, or readiness probe.
- No release packaging, archive upload, DOI minting, GitHub release, or
  publication tooling.
- No large-file movement.
- No commit or push.

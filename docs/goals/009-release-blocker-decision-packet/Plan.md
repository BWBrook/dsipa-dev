# Plan: Goal 009 Release Blocker Decision Packet

## Purpose

This plan turns the Goal 008 no-move release finding into a concise decision
packet. The output should let the DSIPA orchestrator and Barry choose the next
release path without asking them to excavate evidence reports.

## Steps

1. Confirm current state.
   - Record `pwd`, branch/status, short HEAD, remote-tracking HEAD if
     available, and Goal 009 packet presence.

2. Reconstruct the blockers.
   - Read the Goal 009 packet and required files.
   - Extract the large ignored output blocker, baseline-figure checksum
     blocker, archive/DOI blocker, and raw/row-level ALA redistribution
     blocker.

3. Build the decision model.
   - Separate decisions from validation tasks.
   - Assign likely owners: orchestrator, Barry, or future release-execution
     goal.
   - Define recommended option plus alternatives.

4. Draft archive-scope recommendation.
   - Source/manuscript-only option.
   - Recommended archive-proposed large Layer A option.
   - Full reproducibility bundle option with explicit restricted-data
     exclusions.
   - Default no raw/row-level ALA redistribution.

5. Draft evidence-refresh recommendation.
   - Current baseline-map checksum issue.
   - Required evidence reconciliation refresh.
   - Required large-output checksum verification.
   - Future validation prerequisites.

6. Write deliverables.
   - `docs/release_blocker_decision_packet.md`
   - Goal closeout memo.
   - Stage log.
   - Goal log update.
   - Optional narrow status/pointer updates if justified.

7. Validate the packet.
   - Run `git diff --check`.
   - Run required file-presence checks.
   - Run targeted consistency scans from `Goal.md` and classify hits.

8. Wake the orchestrator and stop.

## Non-Goals

- No archive upload, DOI minting, release packaging, GitHub release, or
  publication submission.
- No data reruns, data processing, ALA downloads, modelling, or figure
  regeneration.
- No remote compute, SSH/Tailscale probes, deep-server sync, or readiness
  checks.
- No source/test/manuscript/figure/generated-data edits.
- No large-file movement.
- No commit or push.

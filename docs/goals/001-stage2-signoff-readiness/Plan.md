# Plan: Goal 001 Stage 2 Signoff Readiness Audit

## Purpose

This plan gives `nightlight` a practical route through the audit without
turning it into implementation or new science work.

## Steps

1. Confirm current state.
   - Record `pwd`, branch, short HEAD, and status.
   - Confirm the Goal 001 packet is present.

2. Reconstruct the Stage 2 contract.
   - Read the required files from `Goal.md`.
   - Extract the Stage 2 exit criteria and A01-A14 expectations.

3. Inspect evidence rather than trusting summaries.
   - Check the matrix status for A01-A14.
   - Inspect Table 1, Table S1, interpretation notes, and Stage 2 manifest.
   - Check whether Table S2 remains a Stage 3/4 item.

4. Run the validation ladder.
   - Run cheap hygiene checks first.
   - Run checksum checks for locally present artefacts.
   - Run targeted Stage 2 tests.
   - Run package build.
   - Run `make ms-check`.
   - Classify any skips or failures.

5. Write the review memo.
   - Use a pass/caveat/fail structure.
   - Include exact evidence paths and command outcomes.
   - State whether Stage 2 should be accepted.
   - State whether Stage 3 planning is the right next goal.

6. Update `Log.md`.
   - Append a concise chronological record of what was checked and what
     happened.

7. Wake the orchestrator.
   - Send the required short wake-up to thread
     `019eabf0-9051-7ce2-a0b6-d93b966d1562`, or state that thread tools were
     unavailable.

## Non-Goals

- Do not perform Stage 3 planning.
- Do not fix Stage 2 issues if found; identify them and recommend a narrow
  follow-up goal.
- Do not modify project source, manuscript text, generated figures, generated
  tables, or stage-status docs.

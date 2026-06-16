# Plan: Goal 002 Stage 3 Layer B Reconciliation Plan

## Purpose

This plan gives `nightlight` a route through Stage 3 planning without drifting
into Layer B implementation. The intended output is an executor-ready Stage 3
plan and a short readiness memo for orchestrator review.

## Steps

1. Confirm current state.
   - Record `pwd`, branch, short HEAD, and status.
   - Confirm the Goal 002 packet is present.

2. Reconstruct the Stage 3 contract.
   - Read the required files from `Goal.md`.
   - Extract B01-B12 plus any related reproducibility and manuscript claim
     discipline items that affect Stage 3.

3. Audit current Layer B evidence.
   - Identify which reports already support each item.
   - Identify which manuscript/table/data-availability surfaces still need
     integration later.
   - Identify which items are really Stage 4 release gates.

4. Decide the implementation shape.
   - Recommend one Stage 3 implementation goal or a split into smaller goals.
   - Keep the recommendation practical: fewer goals if the work is mostly
     integration, more only if a true science/compute branch exists.

5. Write the canonical plan.
   - Use a B01-B12 reconciliation matrix.
   - Include deliverables, validation gates, non-goals, and escalation rules.
   - Make Table S2 and claim-discipline requirements concrete.

6. Write the readiness memo.
   - State whether the plan is executor-ready.
   - State the recommended next implementation goal.
   - State whether any Barry-level decision is needed now.

7. Update the stage overview if appropriate.
   - Mark Stage 2 accepted and Stage 3 plan written/pending review.
   - Do not mark Stage 3 complete.

8. Validate the planning artefacts.
   - Run the hygiene and targeted text checks in `Goal.md`.
   - Classify results; do not “fix” paper-facing findings during this goal.

9. Update `Log.md`.
   - Append a concise chronological record of reading, decisions, edits, and
     validation.

10. Wake the orchestrator.
   - Send the required short wake-up to thread
     `019eabf0-9051-7ce2-a0b6-d93b966d1562`, or state that thread tools were
     unavailable.

## Non-Goals

- Do not implement Stage 3.
- Do not edit manuscript text, tables, captions, figures, code, tests, or
  generated science artefacts.
- Do not run modelling, ALA downloads, remote compute, full test suites,
  manuscript builds, package builds, release packaging, or archive checks.
- Do not contact Barry or Chief.

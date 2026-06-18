# Plan: Goal 005 Stage 4 Manuscript And Release Planning

## Purpose

This plan gives `nightlight` a direct route to a Stage 4 execution map without
starting the rewrite or the release package. The output should be a practical
plan that the DSIPA orchestrator can accept, modify, or use immediately for the
next goal packet.

## Steps

1. Confirm current state.
   - Record `pwd`, branch, short HEAD, and status.
   - Confirm the Goal 005 packet is present.

2. Reconstruct accepted evidence.
   - Read the required Stage 2 and Stage 3 closeouts.
   - Confirm Stage 3 is accepted and Stage 4 planning is the next stage.

3. Build the Stage 4 issue map.
   - Start from the Stage 1 critique-resolution matrix.
   - Classify B01, B11, R01, R02, R04, R05, R06, R07, R08, R09, and M01-M05.
   - Keep the classification tied to evidence, validation, and escalation
     boundaries.

4. Audit manuscript surfaces at planning level only.
   - Identify which manuscript sections, tables, captions, and supplement
     surfaces need rewrite or verification.
   - Preserve the accepted Layer A/Layer B scientific stance.
   - Do not edit manuscript files.

5. Audit release and reproducibility surfaces at planning level only.
   - Identify archive/DOI, release manifest, checksum, raw ALA redistribution,
     clean-state audit, data availability, `uv` warning, and stale governance
     text risks.
   - Do not edit release, data, or reproducibility files.

6. Design the Stage 4 goal sequence.
   - Decide whether Stage 4 should split into manuscript synthesis,
     release/data-availability readiness, and final validation goals.
   - For each proposed goal, specify objective, allowed surfaces, non-goals,
     validation, stop conditions, and escalation points.

7. Define the validation ladder.
   - Specify when manuscript checks, package/build checks, release manifest
     checks, checksum reconciliation, claim scans, and reproducibility audits
     should run.
   - Distinguish planning validation from later implementation validation.

8. Write the planning artefacts.
   - `docs/stage4_manuscript_release_plan.md`
   - `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
   - `docs/log/125_stage4_manuscript_release_plan.md`
   - `docs/goals/005-stage4-manuscript-release-plan/Log.md`

9. Optionally update the stage overview.
   - Only record that the Stage 4 plan has been written or is pending review.
   - Do not mark Stage 4 complete.

10. Validate and close out.
    - Run the required `git diff --check`, file-existence checks, and targeted
      `rg` planning scans.
    - Record exact outcomes.
    - Wake the DSIPA orchestrator with the plan and readiness memo paths.

## Non-Goals

- Do not rewrite the manuscript.
- Do not update tables, captions, figures, or generated artefacts.
- Do not create release manifests, archives, DOI deposits, or publication
  packages.
- Do not run remote compute.
- Do not run data processing, ALA downloads, model runs, manuscript builds, or
  package builds.
- Do not commit or push.

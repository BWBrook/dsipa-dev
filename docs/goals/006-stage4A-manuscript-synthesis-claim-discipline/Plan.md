# Plan: Goal 006 Stage 4A Manuscript Synthesis

## Purpose

This plan turns the accepted Stage 4A recommendation into an execution route.
The output should be a manuscript-facing rewrite that is more decisive about
Layer A, clearer about Layer B limits, and easier to validate.

## Steps

1. Confirm current state.
   - Record `pwd`, branch/status, short HEAD, and Goal 006 packet presence.

2. Reconstruct the evidence contract.
   - Read the Goal 006 packet and required files.
   - Extract the accepted Layer A numbers, Layer B posture, and Stage 4A
     non-goals.

3. Make a pre-edit claim map.
   - Identify manuscript sections that need stronger synthesis.
   - Identify claims that need tighter caveats.
   - Identify table/caption notes that need denominator or selection-rule text.

4. Rewrite manuscript-facing surfaces.
   - Prioritize Abstract, Results, Discussion, limitations, tables, captions,
     supplementary captions, and table notes.
   - Keep data availability and release/archive commitments out of Stage 4A.

5. Cross-check values.
   - Verify core Layer A and Layer B numbers against accepted reports and the
     Stage 4 plan.
   - Do not change values unless the source reports prove a mismatch.

6. Update governance and interpretation.
   - Add a Stage 4A interpretation entry.
   - Update matrix rows for M01, M02, M04, and manuscript-facing M05 only when
     justified.
   - Add narrow plan/roadmap redirects only if necessary.

7. Validate.
   - Run `git diff --check`.
   - Run `make ms-check`.
   - Run and classify claim, caption/table, and source-value scans.

8. Close out.
   - Write `docs/log/126_stage4A_manuscript_synthesis.md`.
   - Write `Stage4A_Closeout.md`.
   - Append `Log.md`.
   - Wake the DSIPA orchestrator and stop.

## Non-Goals

- No new analyses, model runs, ALA downloads, or data processing.
- No figure regeneration.
- No release manifest, archive/DOI, or data availability policy work.
- No remote compute.
- No package builds, full pytest, release packaging, or publication tooling.
- No commit or push.

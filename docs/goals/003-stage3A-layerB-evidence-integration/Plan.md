# Plan: Goal 003 Stage 3A Layer B Evidence Integration

## Purpose

This plan gives `nightlight` a route through the Layer B manuscript-facing
integration pass without turning it into new modelling or a broad manuscript
rewrite.

## Steps

1. Confirm current state.
   - Record `pwd`, branch, short HEAD, and status.
   - Confirm the Goal 003 packet is present.

2. Reconstruct the Stage 3A contract.
   - Read the required files from `Goal.md`.
   - Extract the Stage 3A subset of B01-B12 from the accepted Stage 3 plan.

3. Cross-check source values before editing.
   - Pull the Table S2 values from `analysis/reports/layerB_modelling_report.md`.
   - Pull scope/zero-mass support from the QC reports if needed.
   - Keep a cross-check note for the closeout memo.

4. Fill Table S2.
   - Replace the placeholder in `manuscript/text/supplementary_tables.md`.
   - Keep it compact enough for a supplementary table.
   - Preserve the weak/falsification-limited interpretation in the table notes.

5. Tighten Layer B claims.
   - Inspect Layer B sections in `manuscript/text/manuscript_draft.md`,
     `figures.md`, and `supplementary_figures.md`.
   - Edit only where needed to remove ambiguity or overclaiming.
   - Do not rewrite unrelated Layer A or broad Discussion prose.

6. Handle licensing and data-availability language.
   - Verify paper-facing wording says ALA licences are mixed.
   - Verify raw ALA occurrence redistribution is not promised.
   - Add narrow wording only if the current text is insufficient.

7. Record rationale and status.
   - Record B04/B07/B09 no-run rationales.
   - Record B01-B09/B11/B12 as resolved, deferred, or Stage 4-bounded.
   - Leave B10 to Stage 3B.

8. Validate.
   - Run the required commands from `Goal.md`.
   - Classify targeted scan hits instead of treating them as automatic failures.

9. Close out.
   - Write `docs/log/123_stage3A_layerB_evidence_integration.md`.
   - Write `Stage3A_Closeout.md`.
   - Append `Log.md`.

10. Wake the orchestrator.
   - Send the required short wake-up to thread
     `019eabf0-9051-7ce2-a0b6-d93b966d1562`, or state that thread tools were
     unavailable.

## Non-Goals

- Do not run ALA downloads.
- Do not run Layer B modelling or regenerate figures/tables from raw data.
- Do not edit source code or tests.
- Do not implement B10.
- Do not do release packaging, archive/DOI work, remote compute, or a broad
  Stage 4 manuscript rewrite.

# Plan: Goal 004 Stage 3B ALA Ingest Guardrail

## Purpose

This plan gives `nightlight` a direct route through B10 without live data
access. The work should produce durable local test coverage and the smallest
possible code change, if any.

## Steps

1. Confirm current state.
   - Record `pwd`, branch, short HEAD, and status.
   - Confirm the Goal 004 packet is present.

2. Reconstruct the contract.
   - Read the required files from `Goal.md`.
   - Confirm B10 is the only remaining Stage 3 item.

3. Inspect current ingest validation.
   - Review `MIN_DATA_BYTES`, `MIN_DATA_ROWS`, `_select_data_csv`,
     `_validate_download_zip`, `_is_valid_zip`, `find_valid_zips`, and
     `iter_csv_chunks_from_zip`.

4. Write tests first.
   - Create synthetic zips in pytest `tmp_path`.
   - Cover invalid no-CSV, tiny CSV, too-few-rows, malformed payload, valid
     payload, and filtering behavior.
   - Prefer no binary fixtures in git.

5. Run the new test before source edits.
   - If it passes, keep source code unchanged and record that existing guards
     were sufficient once tested.
   - If it fails, patch the smallest needed source behavior and rerun.

6. Update governance docs.
   - Mark B10 resolved in `docs/stage1_critique_resolution_matrix.md`.
   - Write `docs/log/124_stage3B_ala_ingest_guardrail.md`.

7. Validate.
   - Run the required commands from `Goal.md`.
   - Classify optional Layer B summary skips if they occur.

8. Close out.
   - Write `Stage3B_Closeout.md`.
   - Append `Log.md`.
   - Recommend whether Stage 3 can close and Stage 4 planning can begin.

9. Wake the orchestrator.
   - Send the required short wake-up to thread
     `019eabf0-9051-7ce2-a0b6-d93b966d1562`, or state that thread tools were
     unavailable.

## Non-Goals

- Do not call ALA.
- Do not process occurrence data.
- Do not run Layer B models.
- Do not edit manuscript text, figures, or tables.
- Do not run remote compute, release packaging, archive/DOI work, or Stage 4
  planning.

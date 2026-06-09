# 120 Stage 1 critique resolution

Date: 2026-05-23

## Scope

Opened Stage 1 after user acceptance of the Stage 0 baseline. The purpose of this session was to convert the agreed science/evidence critiques into a traceable queue before starting any new Layer A or Layer B science work.

## Baseline

- DSIPA checkout: `main` at `dab3ddb`.
- Stage 0: accepted by the user.
- Evidence snapshot: deep-server reconciliation reports 38/38 expected files present and checksum verified.
- Known nuance: reconciliation/reproducibility reports were generated before the Stage 0 commit and record `f731562...` plus dirty state. This is now tracked as a release-manifest issue rather than a Stage 0 blocker.

## Changes

- Added `docs/stage1_critique_resolution_plan.md`.
- Added `docs/stage1_critique_resolution_matrix.md`.
- Updated `docs/stage_overview.md` to point Stage 1 at the detailed plan.

## Review notes

- The Gate 0.15 audit remains useful, but several Layer B "NO-GO" blockers were later improved by WP0.15b-WP0.20 artefacts. Stage 1 therefore distinguishes `open`, `verify`, `release-gate`, and `superseded` items rather than treating the old audit as a flat to-do list.
- Layer A remains the immediate Stage 2 priority: denominators, floor/censoring, valid-buffer interpretation, bright/dark anchors, ring feasibility, trend sensitivity, and watchlist uncertainty.
- Layer B remains queued for Stage 3: provider-matched conservative framing, licensing/data availability, control design, falsification interpretation, and model-summary table integration.
- Release hygiene remains queued for Stage 4: clean release audit, external archive/DOI, checksum convention clarity, and final manuscript availability statements.

## Validation

- `git diff --check` passed.
- `git status --short --branch` showed only the expected Stage 1 document changes.

## Gate status

Stage 1 was accepted by the user on 2026-05-25.

## Proposed next action

Write the detailed Stage 2 Layer A science-hardening plan, then begin resolving the Stage 2 Layer A items from `docs/stage1_critique_resolution_matrix.md`.

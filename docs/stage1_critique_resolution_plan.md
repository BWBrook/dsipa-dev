# Stage 1 critique-resolution plan

Status: complete, accepted by the user on 2026-05-25.

## Baseline

- DSIPA baseline: `main` at `dab3ddb` (`Add baseline stage plan and evidence harness`).
- Stage 0 status: accepted by the user on 2026-05-23.
- Evidence snapshot: `deep-server` evidence run `20260514T072832Z-evidence6`, reconciled as 38/38 expected files present and checksum verified.
- Known nuance: the reconciliation and reproducibility reports record the pre-Stage-0-commit state (`f731562...`, dirty tree) because they were generated before the Stage 0 baseline commit. Stage 1 treats that as an evidence/release-manifest issue to resolve before final publication claims, not as a reason to reopen Stage 0.

## Objective

Convert every agreed critique into a traceable resolution queue with:

- a stable critique ID;
- severity and current status;
- source evidence;
- required code, data, report, figure, table, or manuscript action;
- a concrete validation gate;
- owner/signoff responsibility;
- a target stage for execution.

This stage is a control surface: it prevents us from strengthening the manuscript by prose alone and prevents later science work from drifting away from the critique set we agreed to fix.

## Non-goals

- Do not run new national analyses or simulations in Stage 1.
- Do not rewrite the manuscript narrative in Stage 1, except for planning references if required.
- Do not write detailed Stage 2, Stage 3, or Stage 4 plans yet.
- Do not treat older audit findings as still open when later artefacts clearly supersede them; mark them as `verify` or `superseded` and record the required follow-through.

## Source inventory and precedence

Primary critique/evidence sources:

- `docs/cover_letters/codex_repo_review_v20260104_gate0_15.md`
- `docs/cover_letter_pi_gate_0_7_wp0_20.md`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/reproducibility_audit.md`
- `analysis/reports/national_layerA_coverage_and_sanity.md`
- `analysis/reports/layerA_sanity_dashboard.md`
- `analysis/reports/risk_rankings_and_quadrants.md`
- `analysis/reports/pa_trend_uncertainty.md`
- `analysis/reports/layerB_modelling_report.md`
- `analysis/reports/layerB_qc_extended.md`
- `docs/interpretation_notes.md`
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_tables.md`

Precedence rules:

1. Current generated evidence beats older review prose when they conflict.
2. The Gate 0.15 audit remains authoritative for risks unless a later artefact both implements the fix and records the validation.
3. Later Layer B QC/modelling artefacts supersede the old "not ready for modelling" verdict, but not the need to integrate the resulting caveats into manuscript claims.
4. Release-facing reproducibility claims require a clean committed evidence/manifest refresh, even if the Stage 0 evidence snapshot is checksum-verified.

## Stage 1 work packages

### S1.1 Critique source inventory

Extract critique items from the Gate 0.15 audit, later PI package, interpretation notes, evidence reports, and manuscript placeholders.

Acceptance:

- Sources are named in this plan.
- The matrix records the source abbreviation for each critique.
- Obsolete or superseded findings are not silently dropped.

### S1.2 Critique-resolution matrix

Create `docs/stage1_critique_resolution_matrix.md` as the single queue of record.

Acceptance:

- Each item has a stable ID, severity, status, target stage, required resolution, owner/signoff rule, and validation gate.
- Items are grouped by Layer A, Layer B, reproducibility/governance, and manuscript synthesis.
- At least one concrete validation gate is attached to every item.

### S1.3 Evidence reconciliation within the matrix

Classify each item as:

- `open`: requires new work before the relevant claim can be used.
- `verify`: likely addressed by existing artefacts, but needs manuscript/report integration or independent confirmation.
- `release-gate`: not blocking Stage 2 science, but blocking final publication/release.
- `superseded`: historical critique retained for traceability; no action unless it reappears.

Acceptance:

- Old Gate 0.15 Layer B blockers are split into implemented-but-verify items versus genuinely open items.
- Release-manifest issues are not confused with scientific result validity.

### S1.4 Stage targeting

Assign execution stages:

- Stage 2: Layer A hardening and primary-result tables/figures.
- Stage 3: Layer B reconciliation and conservative signal framing.
- Stage 4: evidence-led manuscript rewrite, final availability statements, and release package.

Acceptance:

- No Stage 2 item depends on a detailed Stage 3 or Stage 4 plan.
- Stage 2 priority items are explicit enough to write the Stage 2 detailed plan after Stage 1 signoff.

### S1.5 Closeout and gate report

End Stage 1 with a short gate report and a move/no-move recommendation.

Acceptance:

- Stage 1 plan exists.
- Stage 1 matrix exists.
- `docs/stage_overview.md` points to this plan.
- `docs/log/120_stage1_critique_resolution.md` records the work.
- Lightweight document validation passes.

## Stage 1 exit gate

Stage 1 can be accepted only when all of the following are true:

- Every agreed critique is represented in the matrix or explicitly marked `superseded`.
- Every non-superseded item has a target stage and validation gate.
- Layer A items are separated from Layer B and release/manuscript items.
- Existing evidence that partially resolves a critique is named, not assumed.
- No new science or manuscript strengthening has been started ahead of the matrix signoff.
- The user accepts the matrix as the queue of record for Stages 2-4.

## Stage 1 closeout packet

The closeout packet should report:

- created/updated files;
- validation commands run;
- current worktree status;
- Stage 1 gate status;
- the proposed next action, expected to be "write the detailed Stage 2 Layer A hardening plan" if the gate is accepted.

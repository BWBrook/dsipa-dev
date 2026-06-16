# Runbook: Goal 002 Stage 3 Layer B Reconciliation Plan

## Working Directory

```bash
cd /Users/bwbrook/papers/dsipa-dev
```

## Required Starting Checks

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/002-stage3-layerB-reconciliation-plan/Goal.md
```

## Suggested Reading Order

```text
AGENTS.md
README.md
docs/stage_overview.md
docs/stage1_critique_resolution_matrix.md
docs/decisions.md
docs/log/100_layerB_data_acquisition.md
docs/log/101_layerB_qc_hardening.md
docs/log/102_layerB_modelling.md
docs/log/107_layerB_ibra_robustness.md
analysis/reports/layerB_gonogo.md
analysis/reports/layerB_data_qc.md
analysis/reports/layerB_ala_license_ledger.md
analysis/reports/layerB_qc_extended.md
analysis/reports/layerB_scope_coverage.md
analysis/reports/layerB_exposure_qc.md
analysis/reports/layerB_modelling_report.md
analysis/reports/layerB_ibra_summary.md
analysis/reports/layerB_ibra_effects.csv
analysis/reports/evidence_reconciliation.md
docs/interpretation_notes.md
manuscript/text/manuscript_draft.md
manuscript/text/supplementary_tables.md
data/README.md
tests/python/
```

## Planning Artefact Shape

Use this structure for `docs/stage3_layerB_reconciliation_plan.md`:

```md
# Stage 3 Layer B Reconciliation Plan

## Summary Recommendation

## Current Layer B State

## Stage 3 Objective

## B01-B12 Reconciliation Matrix

## Recommended Execution Structure

## Table S2 Completion Plan

## Claim Discipline And Licensing Checks

## Validation Bundle For Implementation

## Stage 4 Boundaries

## Escalation Points

## Exit Gate
```

Use this structure for
`docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`:

```md
# Stage 3 Planning Readiness

## Summary Recommendation

## Current State

## Plan Readiness Audit

## Recommended Next Goal

## Validation Results

## Decisions Or Blockers
```

## Validation Commands

Run from the repo root.

```bash
git status --short --branch
git diff --check
test -f docs/stage3_layerB_reconciliation_plan.md
test -f docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md
```

Targeted text checks:

```bash
rg -n "CC-BY|CC BY|Creative Commons|ALA" manuscript/text docs data/README.md
rg -n "causal|population decline|population trend|national biodiversity|negative controls|falsification|provider-matched|Layer B" manuscript/text docs/interpretation_notes.md docs/stage3_layerB_reconciliation_plan.md
```

Record and interpret these `rg` outputs. They are inspection aids, not
automatic failures.

## Wake-Up

After the plan, memo, and log are complete, send the orchestrator a short
wake-up:

```text
Goal 002 complete. Plan: /Users/bwbrook/papers/dsipa-dev/docs/stage3_layerB_reconciliation_plan.md; readiness memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md
```

Use thread id:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

If thread tools are unavailable, state that in the final response and stop.

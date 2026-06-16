# Runbook: Goal 003 Stage 3A Layer B Evidence Integration

## Working Directory

```bash
cd /Users/bwbrook/papers/dsipa-dev
```

## Required Starting Checks

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/003-stage3A-layerB-evidence-integration/Goal.md
```

## Suggested Reading Order

```text
AGENTS.md
README.md
docs/stage3_layerB_reconciliation_plan.md
docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md
docs/stage1_critique_resolution_matrix.md
docs/decisions.md
docs/interpretation_notes.md
docs/log/100_layerB_data_acquisition.md
docs/log/101_layerB_qc_hardening.md
docs/log/102_layerB_modelling.md
docs/log/107_layerB_ibra_robustness.md
analysis/reports/layerB_data_qc.md
analysis/reports/layerB_ala_license_ledger.md
analysis/reports/layerB_qc_extended.md
analysis/reports/layerB_scope_coverage.md
analysis/reports/layerB_exposure_qc.md
analysis/reports/layerB_modelling_report.md
analysis/reports/layerB_ibra_summary.md
analysis/reports/layerB_ibra_effects.csv
analysis/reports/evidence_reconciliation.md
manuscript/text/manuscript_draft.md
manuscript/text/figures.md
manuscript/text/supplementary_figures.md
manuscript/text/supplementary_tables.md
data/README.md
```

## Table S2 Source Anchors

Use `analysis/reports/layerB_modelling_report.md`.

Known values from the accepted Stage 3 plan:

| Design | n per class | AUC | Log loss | any_light mean | log1p_alan mean | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Primary dr368 | 50,281 | 0.545 | 0.689 | 1.316 | -0.354 | Weak provider-matched association; not causal. |
| Block shuffle | 50,281 | 0.505 | 0.695 | 0.202 | -0.027 | Near-null performance after block shuffle. |
| IBRA-year shuffle | 50,281 | 0.517 | 0.695 | 0.163 | -0.001 | Near-null performance after coarse bioregion-year shuffle. |
| Full sensitivity | 56,883 | 0.557 | 0.700 | 0.732 | -0.332 | Descriptive only because provider/state confounding returns. |

Preserve more precision if the table format permits it, but do not imply
ranking precision or stronger inference than the model supports.

## Closeout Memo Shape

Use this structure for
`docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`:

```md
# Stage 3A Closeout

## Summary Recommendation

## Current State

## Files Changed

## Table S2 Source Cross-Check

## B01-B09/B11/B12 Resolution State

## Claim And Licence Review

## Validation Results

## Residual Risks

## Recommendation For Next Goal
```

## Validation Commands

Run from the repo root.

```bash
git status --short --branch
git diff --check
make ms-check
```

Targeted review scans:

```bash
rg -n "population decline|population trend|causal impact|national biodiversity response|national biodiversity signal" manuscript/text docs/interpretation_notes.md
rg -n "negative controls|diurnal reptiles|Squamata|provider-matched|falsification|Layer B" manuscript/text docs/interpretation_notes.md
rg -n "CC-BY|CC BY|Creative Commons|raw ALA|redistribut|mixed" manuscript/text docs data/README.md
```

## Wake-Up

After the closeout and log are complete, send the orchestrator a short
wake-up:

```text
Goal 003 complete. Closeout memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md
```

Use thread id:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

If thread tools are unavailable, state that in the final response and stop.

# Runbook: Goal 001 Stage 2 Signoff Readiness Audit

## Working Directory

```bash
cd /Users/bwbrook/papers/dsipa-dev
```

## Required Starting Checks

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/001-stage2-signoff-readiness/Goal.md
```

## Suggested Reading Order

```text
AGENTS.md
README.md
docs/stage_overview.md
docs/stage2_layerA_hardening_plan.md
docs/stage1_critique_resolution_matrix.md
docs/log/121_stage2_layerA_hardening.md
docs/log/122_macos_readiness_makedoc.md
analysis/reports/stage2_layerA_hardening_manifest.md
docs/interpretation_notes.md
manuscript/text/tables.md
manuscript/text/supplementary_tables.md
```

## Validation Commands

Run from the repo root unless noted.

```bash
git status --short --branch
git diff --check
```

If present:

```bash
cd artefacts/stage2_layerA_hardening
sha256sum -c SHA256SUMS
cd /Users/bwbrook/papers/dsipa-dev
```

Then:

```bash
sha256sum -c analysis/reports/layerA_tables_stage2_denominators.sha256
sha256sum -c analysis/reports/layerA_anchors_buffer_stage2.sha256
sha256sum -c analysis/reports/layerA_threshold_edge_stage2.sha256
sha256sum -c analysis/reports/layerA_watchlists_stage2.sha256
```

```bash
uv run python -m pytest tests/python/test_trends.py tests/python/test_risk_rankings.py tests/python/test_trend_uncertainty.py tests/python/test_layerA_tables.py tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py tests/python/test_layerA_watchlists.py -q
```

```bash
uv build --out-dir /tmp/dsipa-build-goal001
```

```bash
make ms-check
```

## Memo Shape

Use this structure for
`docs/goals/001-stage2-signoff-readiness/Stage2_Signoff_Readiness.md`:

```md
# Stage 2 Signoff Readiness

## Summary Recommendation

## Current State

## Stage 2 Exit-Gate Audit

## A01-A14 Audit

## Evidence And Artefact Checks

## Validation Results

## Residual Risks

## Recommendation For Next Goal
```

## Wake-Up

After the memo and log are complete, send the orchestrator a short wake-up:

```text
Goal 001 complete. Review memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/001-stage2-signoff-readiness/Stage2_Signoff_Readiness.md
```

Use thread id:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

If thread tools are unavailable, state that in the final response and stop.

# Stage 3 Planning Readiness

## Summary Recommendation

Goal 002 is ready for orchestrator review. The recommended next move is to
authorize a narrow Stage 3A implementation goal for Layer B evidence
integration, Table S2 completion, and claim/licence discipline, followed by a
separate Stage 3B code/test goal for the ALA ingest guardrail.

The planning recommendation is not to run new Layer B modelling by default.
Existing evidence supports retaining Layer B only as a weak, conservative,
provider-bounded secondary occurrence signal test.

## Current State

Stage 2 has been accepted for purposes of moving to Stage 3 planning. Goal 002
has produced the Stage 3 planning surface at:

- `docs/stage3_layerB_reconciliation_plan.md`

Layer B evidence currently supports:

- A primary NSW BioNet dr368 provider-matched model with 50,281 records per
  class.
- Weak primary discrimination, with AUC about 0.545.
- Near-null falsification performance under block shuffle and IBRA-by-year
  shuffle.
- Descriptive full multi-provider sensitivity only.
- Descriptive IBRA heterogeneity only.
- Strong provider/state concentration that prevents national biodiversity
  inference.
- Mixed ALA occurrence licences that require careful data-availability language.

## Plan Readiness Audit

The plan includes all required sections from the Goal 002 runbook:

- Summary recommendation.
- Current Layer B state.
- Stage 3 objective.
- B01-B12 reconciliation matrix.
- Recommended execution structure.
- Table S2 completion plan.
- Claim discipline and licensing checks.
- Validation bundle for implementation.
- Stage 4 boundaries.
- Escalation points.
- Exit gate.

The plan classifies all B01-B12 items:

- Stage 3A evidence/text integration: B01, B02, B03, B04, B05, B06, B07, B08,
  B09, B11 boundary note, B12.
- Stage 3B code/test guardrail: B10.
- Stage 4 release/archive boundary: B01 release mechanics and B11.
- No new modelling by default: B04, B07, B09.

## Recommended Next Goal

Recommended next goal: Stage 3A Layer B evidence integration and claim
discipline.

Suggested executor outcome:

> Reconcile existing Layer B evidence into the manuscript-facing surfaces
> without new analyses. Fill Table S2, tighten Layer B claims, add licensing and
> data-availability caveats, document no-run rationales for B04/B07/B09, and
> stop with validation evidence and a move/no-move recommendation for Stage 4.

Recommended follow-on goal: Stage 3B ALA ingest guardrail test.

Suggested executor outcome:

> Add a local synthetic-fixture test and minimal code guard so ALA ingest rejects
> implausibly tiny or malformed zip payloads. Do not run live ALA downloads or
> data processing.

## Validation Results

Completed on 2026-06-16:

- `git status --short --branch`:
  - `## main...origin/main`
  - ` M docs/stage_overview.md`
  - `?? docs/goals/002-stage3-layerB-reconciliation-plan/`
  - `?? docs/stage3_layerB_reconciliation_plan.md`
- `git diff --check`: pass.
- `test -f docs/stage3_layerB_reconciliation_plan.md`: pass.
- `test -f docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`:
  pass.
- Required heading audit for the Stage 3 plan and readiness memo: pass.
- Targeted licence/provenance scan completed:
  `rg -n "CC-BY|CC BY|Creative Commons|ALA" manuscript/text docs data/README.md`.
- Targeted claim-discipline scan completed:
  `rg -n "causal|population decline|population trend|national biodiversity|negative controls|falsification|provider-matched|Layer B" manuscript/text docs/interpretation_notes.md docs/stage3_layerB_reconciliation_plan.md`.

The targeted scans are intentionally review-heavy. They surfaced expected hits
in the new plan, current cautious manuscript Layer B passages, `data/README.md`
licence/provenance entries, and older review-cover-letter warnings. No
out-of-scope edits were made during Goal 002.

## Decisions Or Blockers

No blocker prevents Stage 3 implementation planning.

Orchestrator decision needed before work proceeds:

- Accept the split Stage 3A/Stage 3B structure, or direct a single combined
  Stage 3 implementation goal.
- Confirm that no new Layer B modelling is required unless Stage 3A exposes a
  specific unsupported claim.
- Confirm that Stage 4, not Stage 3, owns release packaging, DOI/archive policy,
  and final manuscript rewrite.

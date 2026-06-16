# Goal 001: Stage 2 Signoff Readiness Audit

## Objective

Produce an evidence-backed Stage 2 signoff readiness memo that lets the DSIPA
orchestrator decide whether to recommend Barry sign off Stage 2 Layer A
hardening and authorize a later Stage 3 Layer B reconciliation planning goal.

This goal is complete when the memo either:

- recommends Stage 2 signoff with clear supporting evidence;
- recommends Stage 2 signoff with narrow caveats that do not block Stage 3
  planning; or
- identifies specific blockers that must be fixed before signoff.

## Why This Matters

Repo-local records say Stage 2 Layer A hardening is closeout-ready. Before the
project moves to Stage 3, the orchestrator needs a current, independent review
surface rather than relying only on previous closeout notes.

This goal supports a management decision, not a new science result.

## Operating Mode

Review/audit with evidence-packaging validation.

## Review Surface

Create:

- `docs/goals/001-stage2-signoff-readiness/Stage2_Signoff_Readiness.md`
- updates to `docs/goals/001-stage2-signoff-readiness/Log.md`

The memo is the primary review surface. It should be concise but decisive.

## Scope

In scope:

- inspect the current action repo state;
- inspect Stage 2 exit criteria and closeout evidence;
- check A01-A14 status in the Stage 1 critique-resolution matrix;
- inspect Table 1, Table S1, figure/caption references, interpretation notes,
  and Stage 2 artefact manifests;
- verify existing Stage 2 checksums/artefacts where present locally;
- run the validation ladder in this packet;
- classify skips, missing ignored artefacts, or validation failures;
- recommend whether Stage 2 is ready for Barry signoff.

Out of scope:

- do not plan Stage 3 in detail;
- do not start new Layer B work;
- do not rerun ALA downloads, national raster processing, remote compute, or
  data-processing pipelines;
- do not rewrite the manuscript;
- do not alter generated science artefacts;
- do not mark Stage 2 as signed off;
- do not edit `docs/stage_overview.md` or close stage gates;
- do not commit, push, merge, or open pull requests.

## Read First

- `AGENTS.md` - repo-local authority and scientific guardrails.
- `README.md` - current repo/run surface.
- `docs/stage_overview.md` - stage ladder and signoff rule.
- `docs/stage2_layerA_hardening_plan.md` - Stage 2 objective, exit gate, and
  validation bundle.
- `docs/stage1_critique_resolution_matrix.md` - A01-A14 and Layer B/Stage 3
  residuals.
- `docs/log/121_stage2_layerA_hardening.md` - Stage 2 closeout evidence.
- `docs/log/122_macos_readiness_makedoc.md` - Mac readiness and manuscript
  build context.
- `analysis/reports/stage2_layerA_hardening_manifest.md` - repo-visible Stage 2
  artefact manifest.
- `docs/interpretation_notes.md` - result-review notes and residual worries.
- `manuscript/text/tables.md` and `manuscript/text/supplementary_tables.md` -
  Table 1 and Table S1/S2 state.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this goal packet is present

The orchestrator created this goal packet before delegation. Treat these files
as the authorized starting instructions, not as unexpected dirty state.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, or open a PR.
- `nightlight` may edit only files inside
  `docs/goals/001-stage2-signoff-readiness/`.
- The DSIPA orchestrator will review the result and decide whether to commit
  accepted goal artefacts later.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not run remote compute.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not regenerate national Layer A outputs or Layer B datasets.
- Temporary build outputs may go under `/tmp`.
- If an ignored Stage 2 artefact folder is absent locally, report that clearly
  and classify whether it blocks signoff review.

## Required Work

1. Audit Stage 2 exit-gate evidence against the stated exit criteria.
2. Audit A01-A14 status and check that each item is resolved, superseded, or
   explicitly deferred with a reason.
3. Inspect Table 1 and Table S1 readiness; note that Table S2 belongs to Stage
   3/4 unless already complete.
4. Inspect figure/caption and interpretation-note evidence enough to judge
   whether Stage 2 claims are traceable.
5. Run the validation ladder below.
6. Write the signoff readiness memo with a clear recommendation.

## Validation Gates

Run, unless a command is impossible in the current environment:

```bash
git status --short --branch
git diff --check
```

If the Stage 2 artefact folder exists:

```bash
cd artefacts/stage2_layerA_hardening
sha256sum -c SHA256SUMS
```

From the repo root, check the Stage 2 report checksums that are present:

```bash
sha256sum -c analysis/reports/layerA_tables_stage2_denominators.sha256
sha256sum -c analysis/reports/layerA_anchors_buffer_stage2.sha256
sha256sum -c analysis/reports/layerA_threshold_edge_stage2.sha256
sha256sum -c analysis/reports/layerA_watchlists_stage2.sha256
```

Run the targeted Stage 2 test bundle:

```bash
uv run python -m pytest tests/python/test_trends.py tests/python/test_risk_rankings.py tests/python/test_trend_uncertainty.py tests/python/test_layerA_tables.py tests/python/test_layerA_buffer_sensitivity.py tests/python/test_layerA_threshold_sensitivity.py tests/python/test_layerA_edge_decision.py tests/python/test_layerA_watchlists.py -q
```

Run a package build to prove the current checkout still builds:

```bash
uv build --out-dir /tmp/dsipa-build-goal001
```

Run manuscript/build sanity:

```bash
make ms-check
```

Classify validation as:

- current and passing;
- passing with expected skips;
- inconclusive because ignored artefacts are absent;
- failed and blocking; or
- failed but only relevant to a later packaging/release stage.

Do not silently ignore failures.

## Deliverables

- `docs/goals/001-stage2-signoff-readiness/Stage2_Signoff_Readiness.md`
- updated `docs/goals/001-stage2-signoff-readiness/Log.md`
- final response to the DSIPA orchestrator summarizing:
  - changed files;
  - validation commands and outcomes;
  - current git status;
  - signoff recommendation;
  - residual risks;
  - whether Stage 3 planning should be the next goal.

## Decision Authority

`nightlight` may decide:

- how to organize the memo;
- whether a validation failure is Stage 2-blocking, Stage 3-relevant, or a
  later release concern, provided the reasoning is explicit;
- whether existing evidence is sufficient for signoff or needs a narrow repair.

`nightlight` must pause or report blocked before:

- changing scientific assumptions;
- changing stage status;
- editing files outside this goal folder;
- running remote compute or data-processing pipelines;
- making publication/archive policy decisions;
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 001 is complete or blocked and point
to the memo path. If thread tools are unavailable at runtime, state that in the
final response and stop.

## Stop Conditions

Stop when one of these is true:

- the memo is written, the log is updated, and validation is classified;
- a blocker prevents the audit from being completed;
- completing the audit would require out-of-scope work.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- signoff recommendation;
- blockers or residual risks;
- whether a narrow fix goal is needed before Stage 2 signoff;
- whether Stage 3 planning is ready to be the next goal.

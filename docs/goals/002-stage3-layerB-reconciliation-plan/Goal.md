# Goal 002: Stage 3 Layer B Reconciliation Plan

## Objective

Produce a canonical Stage 3 plan that lets the DSIPA orchestrator decide how to
resolve the remaining Layer B critique items before any implementation begins.

This goal is complete when the repository contains a clear, evidence-linked
Stage 3 Layer B reconciliation plan that:

- maps every Layer B critique item B01-B12 to a concrete resolution path;
- separates Stage 3 implementation work from Stage 4 manuscript/release work;
- states whether Stage 3 should be one implementation goal or split into
  smaller goals;
- identifies any decisions that genuinely need Barry rather than orchestrator
  discretion; and
- preserves the conservative interpretation of Layer B as secondary,
  bias-aware, and falsification-limited unless the evidence justifies a
  narrower demotion.

## Why This Matters

Goal 001 accepted Stage 2 Layer A hardening as signoff-ready. Barry has now
authorized the DSIPA orchestrator to proceed into Goal 002. The next risk is
not an obvious missing run; it is Layer B claim discipline. The project needs a
sharp plan before editing manuscript text, filling Table S2, adding guardrail
tests, or deciding whether any new sensitivity run is justified.

This is a planning and reconciliation goal, not a Layer B implementation goal.

## Operating Mode

Planning, evidence reconciliation, and claim-risk triage.

## Authorized Review Surface

Create or update:

- `docs/stage3_layerB_reconciliation_plan.md`
- `docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`
- `docs/goals/002-stage3-layerB-reconciliation-plan/Log.md`

You may also update:

- `docs/stage_overview.md`

Only update `docs/stage_overview.md` to reflect that Stage 2 has been accepted
and that the Stage 3 plan has been written. Do not mark Stage 3 complete.

## Scope

In scope:

- inspect the current action repo state;
- inspect B01-B12 in the Stage 1 critique-resolution matrix;
- inspect the existing Layer B decisions, logs, reports, manuscript sections,
  supplementary table placeholder, data-availability/provenance surfaces, and
  relevant tests;
- classify each B01-B12 item as:
  - Stage 3 implementation required;
  - Stage 3 decision/no-run rationale required;
  - already evidenced but needing integration;
  - Stage 4 release/manuscript gate; or
  - superseded by current evidence;
- propose a concrete Stage 3 validation bundle;
- decide whether Stage 3 should be executed as one goal or split into smaller
  implementation goals;
- identify high-impact scientific or publication decisions that should be
  escalated to the orchestrator and, only if genuinely necessary, Barry.

Out of scope:

- do not edit manuscript prose, tables, captions, figures, or generated
  science artefacts;
- do not run Layer B modelling, ALA downloads, remote compute, data
  processing, release packaging, archive/DOI preparation, or manuscript builds;
- do not implement sentinel-download tests;
- do not fill Table S2;
- do not rewrite Layer B interpretation notes;
- do not change `docs/decisions.md` unless you are explicitly blocked without
  a decision record;
- do not commit, push, merge, or open pull requests;
- do not contact Barry or Chief.

## Read First

- `AGENTS.md` - repo-local scientific and workflow guardrails.
- `README.md` - current repo/run surface and Layer B commands.
- `docs/stage_overview.md` - staged workflow and stage status.
- `docs/stage1_critique_resolution_matrix.md` - B01-B12 and related
  governance items.
- `docs/decisions.md` - current Layer B decisions DEC-009 and DEC-025 through
  DEC-033.
- `docs/log/100_layerB_data_acquisition.md`
- `docs/log/101_layerB_qc_hardening.md`
- `docs/log/102_layerB_modelling.md`
- `docs/log/107_layerB_ibra_robustness.md`
- `analysis/reports/layerB_gonogo.md`
- `analysis/reports/layerB_data_qc.md`
- `analysis/reports/layerB_ala_license_ledger.md`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_modelling_report.md`
- `analysis/reports/layerB_ibra_summary.md`
- `analysis/reports/layerB_ibra_effects.csv`
- `analysis/reports/evidence_reconciliation.md`
- `docs/interpretation_notes.md`
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/supplementary_tables.md`
- `data/README.md`
- relevant Layer B tests under `tests/python/`

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this Goal 002 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 001. Treat files under
`docs/goals/002-stage3-layerB-reconciliation-plan/` as authorized working
instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, or open a PR.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  002 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not use remote compute.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not regenerate Layer B data, reports, figures, artefacts, or manuscript
  outputs.
- Temporary scratch output should not be necessary; if you create any, keep it
  outside the repo or remove it before completion.

## Required Work

1. Reconstruct the Layer B evidence state from the required reading.
2. Build a B01-B12 reconciliation table with current evidence, residual risk,
   proposed Stage 3 action, validation gate, and stage boundary.
3. Decide whether B04, B07, and B09 require new sensitivity work or a no-run
   rationale. Be conservative: do not propose new runs unless they materially
   change manuscript defensibility.
4. Decide how B10 should be implemented in a later goal as a sentinel/tiny ALA
   download guardrail test, without writing that test now.
5. Specify how Table S2 should be filled later, including required rows,
   columns, source reports, and cross-checks.
6. Specify the claim-discipline checks needed to keep Layer B secondary,
   associational, provider-bounded, and falsification-limited.
7. Write `docs/stage3_layerB_reconciliation_plan.md`.
8. Write `Stage3_Planning_Readiness.md` summarizing whether the Stage 3 plan is
   executor-ready and what the next implementation goal should be.
9. Append `Log.md`.
10. If appropriate, update `docs/stage_overview.md` to show Stage 2 accepted
    and Stage 3 plan written/pending review.

## Validation Gates

Run these from the repo root:

```bash
git status --short --branch
git diff --check
test -f docs/stage3_layerB_reconciliation_plan.md
test -f docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md
```

Run targeted text checks and record what they show:

```bash
rg -n "CC-BY|CC BY|Creative Commons|ALA" manuscript/text docs data/README.md
rg -n "causal|population decline|population trend|national biodiversity|negative controls|falsification|provider-matched|Layer B" manuscript/text docs/interpretation_notes.md docs/stage3_layerB_reconciliation_plan.md
```

These `rg` commands are not pass/fail tests by themselves. Use them to verify
that the plan identifies the right claim and licensing risks. Do not edit
paper-facing text during this goal.

Do not run full validation suites, package builds, manuscript builds, data
pipelines, or remote commands for this planning goal.

## Deliverables

- `docs/stage3_layerB_reconciliation_plan.md`
- `docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`
- updated `docs/goals/002-stage3-layerB-reconciliation-plan/Log.md`
- optional, tightly scoped update to `docs/stage_overview.md`
- final response to the DSIPA orchestrator summarizing:
  - changed files;
  - validation commands and outcomes;
  - current git status;
  - recommended Stage 3 execution structure;
  - any decisions needing orchestrator or Barry input;
  - whether the next goal should begin implementation.

## Decision Authority

`nightlight` may decide:

- the plan structure;
- how to group B01-B12 into one or more implementation goals;
- whether a critique item is Stage 3 implementation, Stage 3 decision, or
  Stage 4 release/manuscript work, provided the reasoning is explicit;
- whether existing evidence supports a no-run rationale for B04, B07, or B09.

`nightlight` must pause or report blocked before:

- changing scientific assumptions;
- changing Layer B analysis outputs;
- running new models, downloads, remote compute, or data-processing pipelines;
- changing publication/archive policy;
- making a material decision to remove Layer B from the paper;
- editing outside the authorized review surface;
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 002 is complete or blocked and point
to the Stage 3 plan and readiness memo paths. If thread tools are unavailable
at runtime, state that in the final response and stop.

## Stop Conditions

Stop when one of these is true:

- the Stage 3 plan is written, the readiness memo is written, the log is
  updated, and validation is classified;
- a blocker prevents a defensible Stage 3 plan from being written;
- completing the work would require out-of-scope implementation, compute,
  data processing, manuscript rewriting, or publication policy decisions.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- recommended Stage 3 execution structure;
- whether any narrow pre-implementation fix is needed;
- what the next goal should be if the orchestrator accepts this plan.

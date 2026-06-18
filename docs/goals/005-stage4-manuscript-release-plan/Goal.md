# Goal 005: Stage 4 Manuscript And Release Plan

## Objective

Produce a canonical Stage 4 plan that lets the DSIPA orchestrator decide how to
move from the accepted Stage 2/3 evidence package into manuscript rewriting,
release/archive readiness, and final validation without conflating those tasks.

This goal is complete when the repository contains an evidence-linked,
executor-ready Stage 4 plan that:

- maps every open Stage 4 and release-gate item in the Stage 1
  critique-resolution matrix to a concrete resolution path;
- separates manuscript synthesis, release/data-availability work, and final
  validation into sensible follow-on goals;
- identifies which claims, tables, captions, and availability statements are
  ready for rewrite from existing evidence;
- identifies which publication or archive decisions genuinely require
  orchestrator or Barry input;
- defines the validation ladder for Stage 4, including manuscript checks,
  claim-discipline scans, release manifest checks, and reproducibility checks;
  and
- does not start the manuscript rewrite, release packaging, DOI/archive work,
  data processing, remote compute, or final publication work.

## Why This Matters

Stage 3 is now accepted. Layer A has been hardened and Layer B has been
retained only as a conservative, provider-bounded, presence-only secondary
signal test. The next project risk is not an obvious missing model; it is
letting the final manuscript and release surface drift away from the evidence
and constraints already established.

Stage 4 must therefore be planned as an evidence-led rewrite and release
readiness stage. It should make the paper more decisive, but only where the
evidence is already strong. It should also keep data licensing, large-output
archive policy, checksum conventions, and reproducibility audit evidence
visible before any publication-facing package is assembled.

This is a planning goal, not a manuscript-editing or release-packaging goal.

## Operating Mode

Planning, release-risk triage, manuscript-surface audit, and validation design.

## Authorized Review Surface

Create or update:

- `docs/stage4_manuscript_release_plan.md`
- `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
- `docs/goals/005-stage4-manuscript-release-plan/Log.md`
- `docs/log/125_stage4_manuscript_release_plan.md`

You may also update:

- `docs/stage_overview.md`

Only update `docs/stage_overview.md` to reflect that Stage 3 has been accepted
and that a Stage 4 detailed plan has been written or is pending review. Do not
mark Stage 4 complete.

Do not edit manuscript text, tables, captions, data inventories, release
manifests, build scripts, source code, tests, figures, or generated artefacts
during this goal.

## Scope

In scope:

- inspect the current action repo state;
- inspect the accepted Stage 2 and Stage 3 closeout surfaces;
- inspect the Stage 1 critique-resolution matrix, especially B01, B11, R01,
  R02, R04, R05, R06, R07, R08, R09, and M01-M05;
- inspect manuscript text, tables, captions, supplementary tables/figures, and
  current evidence reports only to classify Stage 4 work;
- inspect release and reproducibility surfaces, including data availability,
  `docs/ref_doi.txt`, Zenodo/release checklist material, evidence
  reconciliation, and reproducibility audit reports;
- decide the recommended Stage 4 goal sequence and boundaries;
- specify manuscript claim-discipline checks that preserve the accepted Layer A
  and Layer B scientific stance;
- specify release/data-availability checks that avoid raw ALA redistribution
  unless permissions are explicitly resolved;
- specify how stale plan/roadmap language should be handled without erasing
  project history;
- identify decisions that the orchestrator can make versus decisions that need
  Barry because they involve publication, archive/DOI, or strategic trade-offs;
  and
- write a readiness memo that recommends the next implementation goal.

Out of scope:

- do not rewrite manuscript prose, tables, captions, abstract, title, or
  availability statements;
- do not create or modify release manifests, archive packages, DOI deposits, or
  publication bundles;
- do not run data pipelines, figure regeneration, Layer A analyses, Layer B
  analyses, ALA downloads, or remote compute;
- do not run manuscript builds or package builds unless the orchestrator later
  authorizes a scope change;
- do not edit `data/README.md`, `docs/ref_doi.txt`, `docs/roadmap.md`,
  `docs/plan.md`, `docs/decisions.md`, `analysis/reports/*`, `manuscript/*`,
  source files, tests, or generated artefacts;
- do not commit, push, merge, or open pull requests;
- do not contact Barry or Chief.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/stage_overview.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/goals/001-stage2-signoff-readiness/Stage2_Signoff_Readiness.md`
- `docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`
- `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
- `docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md`
- `docs/stage2_layerA_hardening_plan.md`
- `docs/stage3_layerB_reconciliation_plan.md`
- `docs/interpretation_notes.md`
- `docs/decisions.md`
- `docs/workflow.md`
- `docs/plan.md`
- `docs/roadmap.md`
- `data/README.md`
- `docs/ref_doi.txt`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/reproducibility_audit.md`
- `analysis/reports/data_inventory.md`
- `analysis/reports/figure_inventory.md`
- `analysis/reports/zenodo_release_checklist_2026-01-03.md`
- `analysis/reports/zenodo_release_checklist_2026-01-04.md`
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/references.md`

If additional files are clearly needed to classify a Stage 4 planning item,
read them. Do not read outside `/Users/bwbrook/papers/dsipa-dev`.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this Goal 005 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 004 at commit `b78a302`. Treat files under
`docs/goals/005-stage4-manuscript-release-plan/` as authorized working
instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, or open a PR.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  005 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not use remote compute.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not run data-processing pipelines, ALA downloads, manuscript builds,
  package builds, archive packaging, or DOI publication tooling.
- Temporary scratch output should not be necessary; if you create any, keep it
  outside the repo or remove it before completion.

## Required Work

1. Reconstruct the accepted Stage 2/3 evidence state from the required reading.
2. Build a Stage 4 issue map from the Stage 1 critique-resolution matrix. At
   minimum classify B01, B11, R01, R02, R04, R05, R06, R07, R08, R09, and
   M01-M05 by required Stage 4 action, evidence source, validation gate, and
   escalation boundary.
3. Audit the manuscript surfaces at planning level only. Identify which
   Results, Discussion, table, caption, supplement, and availability surfaces
   are ready for evidence-led rewrite and which need release-policy decisions
   first.
4. Audit release and reproducibility surfaces at planning level only. Identify
   current risks around external archive/DOI policy, large ignored outputs,
   raw ALA redistribution, checksum conventions, stale pre-commit audit
   references, `uv` warning documentation, and stale roadmap/plan language.
5. Recommend a Stage 4 goal sequence. At minimum consider whether Stage 4
   should split into:
   - Stage 4A manuscript synthesis and claim/caption/table discipline;
   - Stage 4B data availability, release manifest, archive/DOI, and checksum
     policy readiness; and
   - Stage 4C final manuscript/build/reproducibility audit.
6. For each recommended follow-on goal, specify:
   - objective;
   - allowed review surface;
   - non-goals;
   - required evidence inputs;
   - validation commands and manual checks;
   - stop conditions;
   - escalation points; and
   - expected deliverables.
7. Define a Stage 4 claim-discipline scan strategy for causal, population
   decline, population trend, national biodiversity, Layer B, denominator,
   censoring, and licensing language.
8. Define the final validation ladder, including when to run `make ms-check`,
   package/build checks, release manifest checks, checksum checks, and any
   clean-state reproducibility audit.
9. Write `docs/stage4_manuscript_release_plan.md`.
10. Write `Stage4_Planning_Readiness.md` summarizing whether the Stage 4 plan
    is executor-ready and what the next implementation goal should be.
11. Write `docs/log/125_stage4_manuscript_release_plan.md`.
12. Append `Log.md`.
13. If appropriate, update `docs/stage_overview.md` to show Stage 4 plan
    written/pending review, without marking Stage 4 complete.

## Validation Gates

Run these from the repo root:

```bash
git status --short --branch
git diff --check
test -f docs/stage4_manuscript_release_plan.md
test -f docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md
test -f docs/log/125_stage4_manuscript_release_plan.md
```

Run targeted text checks and record what they show:

```bash
rg -n "release-gate|Stage 4|B01|B11|R01|R02|R04|R05|R06|R07|R08|R09|M01|M02|M03|M04|M05" docs/stage1_critique_resolution_matrix.md docs/stage4_manuscript_release_plan.md
rg -n "population decline|population trend|causal|national biodiversity|provider-bounded|presence-only|falsification|mixed|raw ALA|redistribut|CC-BY|Creative Commons" manuscript/text docs data/README.md docs/stage4_manuscript_release_plan.md
rg -n "doi|archive|Zenodo|checksum|release manifest|uv|VIRTUAL_ENV|reproducibility" docs analysis/reports data/README.md docs/stage4_manuscript_release_plan.md
```

These `rg` commands are not pass/fail tests by themselves. Use them to verify
that the plan identifies the right manuscript, claim, release, and
reproducibility risks. Do not edit the matched surfaces during this goal unless
they are in the authorized review surface.

Do not run full validation suites, package builds, manuscript builds, data
pipelines, release packaging, DOI/archive commands, or remote commands for this
planning goal.

## Deliverables

- `docs/stage4_manuscript_release_plan.md`
- `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
- `docs/log/125_stage4_manuscript_release_plan.md`
- updated `docs/goals/005-stage4-manuscript-release-plan/Log.md`
- optional, tightly scoped update to `docs/stage_overview.md`
- final response to the DSIPA orchestrator summarizing:
  - changed files;
  - validation commands and outcomes;
  - current git status;
  - recommended Stage 4 execution structure;
  - any decisions needing orchestrator or Barry input;
  - whether the next goal should begin implementation.

## Decision Authority

`nightlight` may decide:

- the plan structure;
- how to group Stage 4 work into follow-on goals;
- whether a critique item is manuscript synthesis, release/readiness work,
  final validation, or a Barry-level decision;
- which existing evidence surfaces are most important for each follow-on goal;
  and
- whether stale governance text should be handled in the first Stage 4
  implementation goal or a later cleanup goal.

`nightlight` must pause or report blocked before:

- changing scientific assumptions;
- editing manuscript text, tables, captions, figures, data inventories, release
  files, source code, tests, or generated artefacts;
- running new models, downloads, remote compute, data-processing pipelines,
  manuscript builds, package builds, or release/DOI tooling;
- making publication/archive policy decisions;
- proposing raw ALA occurrence redistribution;
- deciding to remove Layer B from the paper;
- editing outside the authorized review surface; or
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 005 is complete or blocked and point
to the Stage 4 plan and readiness memo paths. If thread tools are unavailable
at runtime, state that in the final response and stop.

## Stop Conditions

Stop when one of these is true:

- the Stage 4 plan is written, validation is classified, the readiness memo is
  written, and the log is updated;
- a blocker prevents a defensible Stage 4 plan;
- completing the work would require out-of-scope manuscript editing, release
  packaging, archive/DOI work, data processing, remote compute, or publication
  decisions.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- recommended Stage 4 goal sequence;
- decisions or blockers requiring orchestrator or Barry input;
- residual risks; and
- whether the next implementation goal is ready to delegate.

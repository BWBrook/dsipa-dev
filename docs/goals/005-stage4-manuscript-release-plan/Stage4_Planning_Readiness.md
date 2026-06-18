# Stage 4 Planning Readiness

Date: 2026-06-18

## Readiness Verdict

Goal 005 is ready for DSIPA orchestrator review. The Stage 4 plan is
executor-ready as a planning surface and recommends a three-goal sequence:

1. Stage 4A manuscript synthesis and claim discipline.
2. Stage 4B release/data-availability/archive/DOI readiness.
3. Stage 4C final manuscript/build/reproducibility validation.

This goal did not start the rewrite, release packaging, archive publication,
data processing, remote compute, manuscript builds, package builds, or final
publication tooling.

## Current State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Starting branch/status: `## main...origin/main` with the untracked Goal 005
  packet directory.
- Starting short HEAD: `b78a302`
- Goal 005 packet present: yes.
- Repo-local `AGENTS.md` and the full Goal 005 packet were read.
- All Goal 005 read-first files were read.

## Changed Files

- `docs/stage4_manuscript_release_plan.md`
- `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
- `docs/goals/005-stage4-manuscript-release-plan/Log.md`
- `docs/log/125_stage4_manuscript_release_plan.md`
- `docs/stage_overview.md`

The `docs/stage_overview.md` edit is deliberately narrow: it records that the
Stage 4 detailed plan has been written and is pending orchestrator review. It
does not mark Stage 4 complete.

## Planning Coverage

The plan maps the required Stage 4 and release-gate items:

- B01 and B11: ALA mixed-licence and raw-redistribution release gates.
- R01, R02, R04, R05, R06, R07, R08, and R09: reproducibility, archive/DOI,
  checksum, governance, and validation risks.
- M01-M05: manuscript synthesis, caption/table discipline, references, claim
  discipline, and table traceability.

The plan also defines:

- manuscript surfaces ready for evidence-led rewrite;
- surfaces needing release-policy decisions first;
- the Stage 4A/4B/4C goal sequence;
- validation commands and manual checks for each follow-on goal;
- a claim-discipline and licensing scan strategy;
- stale governance handling; and
- orchestrator versus Barry escalation points.

## Validation Results

- `git status --short --branch` completed. Status showed `main...origin/main`,
  modified `docs/stage_overview.md`, and untracked Goal 005 planning artefacts.
- `git diff --check` passed.
- File-existence gates passed for:
  - `docs/stage4_manuscript_release_plan.md`
  - `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
  - `docs/log/125_stage4_manuscript_release_plan.md`
- Matrix/plan scan passed:
  `rg -n "release-gate|Stage 4|B01|B11|R01|R02|R04|R05|R06|R07|R08|R09|M01|M02|M03|M04|M05" docs/stage1_critique_resolution_matrix.md docs/stage4_manuscript_release_plan.md`
  found the required Stage 4 IDs in the matrix and new plan.
- Claim/licensing scan completed:
  `rg -n "population decline|population trend|causal|national biodiversity|provider-bounded|presence-only|falsification|mixed|raw ALA|redistribut|CC-BY|Creative Commons" manuscript/text docs data/README.md docs/stage4_manuscript_release_plan.md`.
  Hits were expected cautionary/governance hits in the manuscript, Stage 3
  closeouts/plans, data README, and the new Stage 4 scan strategy.
- Release/reproducibility scan completed:
  `rg -n "doi|archive|Zenodo|checksum|release manifest|uv|VIRTUAL_ENV|reproducibility" docs analysis/reports data/README.md docs/stage4_manuscript_release_plan.md`.
  Hits confirm the plan identifies archive/DOI, checksum, release-manifest,
  `uv`, and reproducibility risks already present in the repo records.

## Recommended Next Goal

Recommended next implementation goal: Stage 4A manuscript synthesis and claim
discipline.

Suggested executor outcome:

> Rewrite the manuscript-facing narrative from the accepted Stage 2/3 evidence
> package, preserving Layer A as the primary result and Layer B as a weak,
> provider-bounded, presence-only falsification exercise. Update Results,
> Discussion, captions, tables, interpretation notes, and matrix statuses as
> authorized. Do not do release packaging, archive/DOI work, new science, ALA
> downloads, remote compute, manuscript build publication tooling, commits,
> pushes, merges, or PRs.

Stage 4B should follow only after Stage 4A is accepted, because final data
availability and release-manifest wording should reflect the accepted
manuscript state.

## Decisions Needed

Orchestrator decisions:

- Accept, modify, or reject the proposed 4A/4B/4C split.
- Decide whether Stage 4A may run `make ms-check` after manuscript edits.
- Decide how narrowly to update stale `docs/plan.md` and `docs/roadmap.md`
  status language during Stage 4.

Barry decisions, later:

- Whether and when to publish an external archive/DOI.
- Final archive scope for large ignored outputs.
- Any exception to the default no-raw-ALA/no-row-level-ALA redistribution rule.
- Strategic title/abstract/journal-framing choices if the orchestrator wants a
  stronger publication positioning decision.

## Blockers

No blocker prevents orchestrator review of this Stage 4 plan.

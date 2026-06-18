# Stage 4 Manuscript And Release Plan

Date: 2026-06-18

## Scope

Goal 005 produced the Stage 4 manuscript/release planning surface only. It did
not rewrite manuscript prose, tables, captions, or availability statements; did
not edit release manifests or data inventories; did not run pipelines,
manuscript builds, package builds, archive/DOI tooling, ALA downloads, remote
compute, or model runs.

## Starting State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch/status: `## main...origin/main` with untracked
  `docs/goals/005-stage4-manuscript-release-plan/`
- Short HEAD: `b78a302`
- Goal 005 packet present: yes
- Repo-local `AGENTS.md` was read.

## Reading Completed

Read the Goal 005 packet plus the required Stage 2/3 closeouts, Stage 1 matrix,
Stage 2/3 plans, interpretation notes, decisions, workflow, plan, roadmap, data
inventory, DOI seed file, evidence/reproducibility reports, Zenodo checklists,
and manuscript text/table/caption/reference surfaces.

## Planning Findings

- Stage 2 and Stage 3 are accepted for Stage 4 planning purposes.
- The remaining Stage 4 risks are not missing science by default; they are
  manuscript synthesis, release policy, data availability, checksum convention,
  stale governance text, and final validation risks.
- B01/B11 and R02/R05 are the highest-stakes release gates because they involve
  ALA redistribution and archive/DOI scope.
- M01/M02/M04/M05 should be resolved in a manuscript-focused Stage 4A goal.
- R01/R02/R05/R09 should be resolved in a release-focused Stage 4B goal.
- Final builds, manuscript checks, package checks, and clean-state
  reproducibility audit belong in Stage 4C after the manuscript and release
  surfaces have settled.

## Deliverables

- `docs/stage4_manuscript_release_plan.md`
- `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
- `docs/log/125_stage4_manuscript_release_plan.md`
- updated `docs/goals/005-stage4-manuscript-release-plan/Log.md`
- narrowly updated `docs/stage_overview.md`

## Validation

- `git status --short --branch` completed. Status showed `main...origin/main`,
  modified `docs/stage_overview.md`, and untracked Goal 005 planning artefacts.
- `git diff --check` passed.
- File-existence gates passed:
  - `test -f docs/stage4_manuscript_release_plan.md`
  - `test -f docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
  - `test -f docs/log/125_stage4_manuscript_release_plan.md`
- Matrix/plan scan passed. The required Stage 4 IDs B01, B11, R01, R02, R04,
  R05, R06, R07, R08, R09, and M01-M05 appear in the matrix and Stage 4 plan.
- Claim/licensing scan completed. Hits were expected cautionary/governance hits
  in manuscript text, Stage 3/4 docs, and data README; no matched surface was
  edited outside the authorized planning review surface.
- Release/reproducibility scan completed. Hits confirm the plan identifies
  archive/DOI, Zenodo, checksum, release-manifest, `uv`, and reproducibility
  risks.

## Recommendation

Recommend orchestrator review and, if accepted, a Stage 4A manuscript synthesis
and claim-discipline goal next. Stage 4B release/data-availability readiness and
Stage 4C final validation should remain separate follow-on goals.

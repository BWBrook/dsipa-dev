# Runbook: Goal 005 Stage 4 Manuscript And Release Plan

## Start

From `/Users/bwbrook/papers/dsipa-dev`:

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/005-stage4-manuscript-release-plan/Goal.md
```

Record the results in the goal log.

## Required Reading Checklist

Read the files listed in `Goal.md` before writing the Stage 4 plan. If a file
is absent, record that explicitly and continue only if the missing file is not
blocking.

Pay particular attention to:

- Stage 1 matrix statuses and targets.
- Stage 2/3 closeout recommendations and residual risks.
- Manuscript tables/captions that are placeholders or need evidence trace.
- Release/readiness notes involving DOI, archive, raw ALA redistribution,
  checksums, and clean-state reproducibility.
- Repo-local workflow rules for result review and artefact review.

## Planning Output Requirements

`docs/stage4_manuscript_release_plan.md` should include:

- summary recommendation;
- current accepted evidence state;
- Stage 4 objective and non-goals;
- issue map for Stage 4 and release-gate matrix items;
- manuscript synthesis plan;
- release/data-availability/reproducibility plan;
- recommended Stage 4 goal sequence;
- validation ladder;
- claim-discipline and licensing scan strategy;
- escalation points;
- exit gate.

`Stage4_Planning_Readiness.md` should include:

- whether the plan is ready for orchestrator review;
- changed files;
- validation results;
- recommended next goal;
- decisions or blockers.

`docs/log/125_stage4_manuscript_release_plan.md` should record the planning
session compactly.

## Validation

Run:

```bash
git status --short --branch
git diff --check
test -f docs/stage4_manuscript_release_plan.md
test -f docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md
test -f docs/log/125_stage4_manuscript_release_plan.md
```

Run and classify:

```bash
rg -n "release-gate|Stage 4|B01|B11|R01|R02|R04|R05|R06|R07|R08|R09|M01|M02|M03|M04|M05" docs/stage1_critique_resolution_matrix.md docs/stage4_manuscript_release_plan.md
rg -n "population decline|population trend|causal|national biodiversity|provider-bounded|presence-only|falsification|mixed|raw ALA|redistribut|CC-BY|Creative Commons" manuscript/text docs data/README.md docs/stage4_manuscript_release_plan.md
rg -n "doi|archive|Zenodo|checksum|release manifest|uv|VIRTUAL_ENV|reproducibility" docs analysis/reports data/README.md docs/stage4_manuscript_release_plan.md
```

The `rg` commands are review scans, not automatic failures. Summarize the
classes of hits and how the plan addresses them.

## Wake-Up

When complete or blocked, send a short wake-up to the DSIPA orchestrator thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

Use this shape:

```text
Goal 005 complete.

Stage 4 plan: /Users/bwbrook/papers/dsipa-dev/docs/stage4_manuscript_release_plan.md
Readiness memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md
```

If blocked, replace `complete` with `blocked` and point to the blocker note.

## Stop

Stop after the wake-up. Do not keep working into Stage 4 implementation without
a new goal packet.

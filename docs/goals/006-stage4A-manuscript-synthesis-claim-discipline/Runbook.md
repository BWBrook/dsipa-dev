# Runbook: Goal 006 Stage 4A Manuscript Synthesis

## Start

From `/Users/bwbrook/papers/dsipa-dev`:

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Goal.md
```

Record the results in the goal log.

## Execution Checklist

- Read `AGENTS.md` and the full Goal 006 packet.
- Read every required source listed in `Goal.md`.
- Build a pre-edit claim map.
- Rewrite manuscript-facing surfaces only.
- Cross-check core numbers before changing them.
- Keep release/archive/data-availability policy out of this goal.
- Run validation.
- Write the closeout and log.
- Wake the orchestrator.

## Core Values To Protect

Layer A:

- protected-area universe: n = 11,133;
- inside baseline/trend eligibility: n = 4,426;
- 2024 zero inside mean radiance: 3,844 of 4,426, 86.9 percent;
- zero inside slopes: 3,969 of 4,426, 89.7 percent;
- positive inside slopes: 420 eligible protected areas;
- 1 km unprotected-land buffer retention denominator: n = 3,858;
- retention quadrants: Q1 = 305, Q2 = 55, Q3 = 3,308, Q4 = 190;
- complete interior-ring profiles: n = 383.

Layer B:

- primary provider-matched design: 50,281 microbat and 50,281 passerine
  records;
- primary AUC about 0.545 and log loss about 0.689;
- block-shuffle AUC about 0.505;
- IBRA x year shuffle AUC about 0.517;
- full multi-provider sensitivity AUC about 0.557;
- interpretation: weak, provider-bounded, presence-only, associational, and
  falsification-limited.

## Validation

Run:

```bash
git status --short --branch
git diff --check
make ms-check
```

Run and classify:

```bash
rg -n "population decline|population trend|causal impact|causal|national biodiversity response|national biodiversity signal|national biodiversity" manuscript/text docs/interpretation_notes.md
rg -n "provider-bounded|presence-only|falsification|provider-matched|weak discrimination|AUC|log loss|raw ALA|redistribut|mixed" manuscript/text docs/interpretation_notes.md
rg -n "n =|eligible|ineligible|minimum-pixel|valid-pixel|zero|censor|floor|complete ring|selection rule|triage|uncertainty" manuscript/text
rg -n "11,133|4,426|3,844|86.9|3,969|89.7|420|3,858|305|55|3,308|190|383" manuscript/text docs/stage4_manuscript_release_plan.md analysis/reports
rg -n "50,281|0.545|0.689|0.505|0.517|0.557|provider-matched|multi-provider|mixed" manuscript/text docs/stage4_manuscript_release_plan.md analysis/reports
```

Do not treat `rg` output as automatically passing or failing. Classify hits
manually in the closeout.

## Wake-Up

When complete or blocked, send a short wake-up to:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

Use this shape:

```text
Goal 006 complete.

Closeout memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Stage4A_Closeout.md
```

If blocked, replace `complete` with `blocked` and point to the blocker note.

## Stop

Stop after the wake-up. Do not start Stage 4B without a new goal packet.

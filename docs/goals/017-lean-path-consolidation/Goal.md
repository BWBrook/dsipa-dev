# Goal 017: Lean-Path Consolidation

Status: implementation complete; pending orchestrator acceptance.

## Objective

Reduce active engineering burden while preserving accepted science. Fix the
Layer B pipeline/artefact-state contradiction, simplify high-value active
paths, remove only demonstrably obsolete code, and establish proportional
fast/release gates.

Principle: rigour at the scientific decision boundary; proportional
engineering everywhere else.

## Starting Gate

Before implementation:

- read repo-local `AGENTS.md`;
- record `pwd`, branch, full HEAD, `origin/main`, short status, and recent
  history;
- require `main`, HEAD/origin
  `00e43f0d2a127c62eadd14fd8bb9eb5ef38fa9c5`, and a clean tree except this
  newly persisted Goal 017 packet.

Stop and wake the DSIPA orchestrator for divergence or unrelated changes. Never
reset, clean, stash, or overwrite.

## Frozen Contract

Do not change scientific/schema/output-row/figure/manuscript/DOI/licensing
surfaces. Frozen items include:

- Layer A primary and Layer B compact/provider-bounded/presence-only,
  bias-limited, non-causal framing;
- 2013-2024 and all CAPAD/IBRA/VIIRS, spatial, threshold, estimator, seed,
  control, provider, and inclusion definitions;
- schema v0.3.0, stable keys, nine accepted Layer A files, reference identities
  and headlines;
- all results, tables, figures, manuscript claims, interpretations, and
  screening-not-ranking framing;
- DOI `10.5281/zenodo.21524637`;
- no raw/row-level ALA redistribution and existing release boundaries.

Any required change to those surfaces stops the goal.

## Required Outcomes

- Create `Lean_Path_Consolidation_Closeout.md`.
- Fix the Layer B clean-tree contradiction by rejecting unexplained dirtiness
  before mutation, allowing expected generated outputs through artefact
  creation, centralising duplicated Git-state rules, retaining only justified
  override behaviour, and making the canonical invocation coherent.
- Prove the Layer B fix with deterministic temporary-repository or fixture
  tests, without ALA/network/national data.
- Simplify active Layer B paths where it materially improves
  readability/testability, using plain functions/modules and existing
  dependencies.
- Reduce duplication among canonical runner, Layer B artefacts, and current
  expected-output/release-manifest surfaces only where one source safely
  replaces repeated active lists.
- Investigate caller-free candidates and delete only with repository-wide
  evidence that no active test, manuscript, reproduction, or release path needs
  them.
- Document truthful fast and release gates using existing tooling.

## Boundaries

Work only in `/Users/bwbrook/papers/dsipa-dev`. Do not read
`/Users/bwbrook/chief_of_staff` or `/Users/bwbrook/work/goal_composer`; do not
contact Barry or Chief. Wake only DSIPA orchestrator thread
`019eabf0-9051-7ce2-a0b6-d93b966d1562`.

Do not run national/remote compute, ALA acquisition, real-data modelling,
figure/manuscript regeneration, packaging, Zenodo/GitHub/Wiley/public actions,
or external service actions. Do not commit, push, tag, release, publish, upload,
submit, change visibility, or contact external services.

Permitted writes: active Layer B modules or small shared helpers,
`analysis/run_full_pipeline.sh`, narrowly justified active orchestration or
manifest scripts, `Makefile`, corresponding tests/small synthetic fixtures,
truthful README/workflow docs, this Goal 017 packet/closeout/one log/narrow
stage pointer, and deletions proven within scope.

Do not edit manuscript, scientific settings/reference contracts, data,
generated reports, figures, receipts, DOI metadata, dependencies/lockfiles, or
unrelated modules.

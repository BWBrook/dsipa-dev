# Runbook

## Start

```bash
pwd
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git log --oneline -5 --decorate
```

Required state: `main`, HEAD and `origin/main` both
`00e43f0d2a127c62eadd14fd8bb9eb5ef38fa9c5`, clean except the newly persisted
Goal 017 packet.

## Audit

Use `rg`/`rg --files` to find callers for:

- `src/python/dsipa/radiance_smoketest.py`
- `src/python/dsipa/ring_profiles_smoketest.py`
- `src/python/dsipa/data_inventory.py`
- `src/python/dsipa/layerB_gonogo.py`
- `analysis/build_final_release.py`
- superseded Zenodo/checklist helpers or obsolete CLI modes

Delete only with repository-wide caller evidence. Defer when ambiguous.

## Implementation Rules

- Reject unexplained dirtiness before artefact mutation.
- Allow expected generated outputs through artefact creation.
- Centralise duplicated Git-state policy.
- Keep CLI entry points thin.
- Do not add frameworks, registries, compatibility layers, dependency
  injection, or configurable workflow engines.
- Keep Layer A stable except for tiny caller-proven low-risk helpers.

## Validation

Run only decision-relevant local gates:

```bash
git diff --check
make test
uv build --out-dir /tmp/dsipa-goal017-build
```

Also run targeted fast tests, shell syntax checks, runner-contract tests,
caller-evidence scans, and frozen-surface checks needed for Goal 017. Do not
run manuscript, national, remote, model, release, DOI, GitHub, Zenodo, Wiley,
or public-action gates.

## Closeout

`Lean_Path_Consolidation_Closeout.md` must record:

- start/final git state and footprint;
- retained active path;
- caller-backed retain/simplify/delete/defer disposition for every
  changed/deleted surface;
- deletion/flag/mode caller evidence;
- fast/full/build/shell/frozen-surface validation;
- before/after complexity inventory;
- one focused self-review;
- material residual/deferred candidates;
- readiness for orchestrator review.

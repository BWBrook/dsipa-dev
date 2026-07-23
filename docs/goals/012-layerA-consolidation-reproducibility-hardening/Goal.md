# Goal 012: Layer A Consolidation And Reproducibility Hardening

## Objective

Harden and simplify the accepted DSIPA Layer A execution path without changing
its science. Make clean-checkout QA offline and deterministic, make statewise
serialization and geometry-union cache reuse deterministic, consolidate
accepted input/output identities into one machine-readable reference contract,
and prove the result with exactly one clean national Layer A regression run on
`deep-server`.

This is a bounded reproducibility and orchestration goal. It is not a new
analysis, scientific revision, or broad architecture rewrite.

## Starting State

- Action repo: `/Users/bwbrook/papers/dsipa-dev`
- Required branch: `main`
- Required HEAD and `origin/main`:
  `1b39dcc1403a40c3962f04c922bb612c41f83a8f`
- Required starting status: clean (`## main...origin/main`)
- Accepted comparison payload:
  `/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation`
- Accepted schema: `v0.3.0`
- Accepted period: 2013-2024

Stop before mutation if the branch, HEAD, `origin/main`, or clean status
differs. Never reset, clean, or reconcile unexpected work.

## Frozen Scientific Contract

The following are immutable in Goal 012:

- Zenodo/OpenGeoHub v0.4 annual VIIRS composites for 2013-2024;
- CAPAD and IBRA source definitions;
- buffer distances, ring definitions, minimum valid-pixel and valid-year
  thresholds;
- estimators, bootstrap settings, ranking categories, and inclusion rules;
- schema `v0.3.0`, output column sets, and the nine approved filenames;
- primary Layer A claims and accepted headline values; and
- the complete Layer B boundary.

The accepted primary headline values are:

- protected-area universe: 11,133;
- eligible baseline/trend subset: 4,426;
- 2024 zero inside mean: 3,844/4,426;
- exact-zero inside slopes: 3,969/4,426;
- positive inside slopes: 420/4,426;
- retention denominator: 3,858;
- quadrants: Q1=305, Q2=55, Q3=3,308, Q4=190; and
- complete rings: 383.

Any primary-value change is scientific drift and stops the goal.

## Required Outcomes

### 1. Offline Clean-Checkout QA

Full pytest must pass from a true fresh checkout or `git archive` without
ignored local artefacts and without network access.

The two real triad geometry and buffer checks must run and pass; they must not
be skipped. The implementation may use provenance-verified tracked fixtures or
deterministic temporary fixtures. Pytest must not fetch CAPAD or depend on
repository-local ignored GPKGs.

### 2. Deterministic Statewise Serialization

Preserve all values and schemas while producing stable canonical key order for
state-level and merged outputs. Use a stable sort with an explicit null policy.

Canonical keys:

- radiance buffers:
  `pa_id,year,zone,buffer_km,buffer_type`;
- edge profiles:
  `pa_id,year,ring_index`; and
- buffer validity:
  `pa_id,buffer_km`.

Goal 011's accepted payload contains 1,941 ordering descents in the
900,768-row radiance CSV and 845 in the 400,788-row edge CSV. Goal 012 must
reduce both to zero without changing row counts, key sets, columns, or values.

### 3. Single Layer A Reference Contract

Create exactly one machine-readable reference contract at:

```text
settings/layerA_reference_contract_v0_3_0.json
```

It must contain:

- contract and analysis-schema versions;
- frozen period, states, thresholds, buffers, rings, and required filenames;
- accepted CAPAD, IBRA, Natural Earth, and VIIRS identities;
- archive-candidate output classifications and hashes;
- stable keys and expected row/key constraints;
- frozen primary headline values;
- the accepted 1,432/12.9% ring-1 value; and
- an explicit historical reconciliation record for 1,427 versus 1,432.

Code, tests, and release validation must consume this contract rather than
copying release hashes or headline values into multiple modules.

### 4. Fail-Closed Input And Output Validation

Canonical execution must stop before expensive national computation unless:

- CAPAD has 14,403 raw features and semantic hash
  `148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf`;
- IBRA has 89 features and semantic hash
  `3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332`;
- Natural Earth archive size is 69,700 bytes and SHA-256 is
  `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`;
  and
- all 12 annual VIIRS files pass the existing code-pinned MD5 values.

Post-run validation must verify all nine files, schemas, stable keys, row/key
constraints, output classifications, and frozen headlines against the same
reference contract.

### 5. Fingerprinted Geometry-Union Caches

Add a small cache-sidecar contract for the existing PA, land, and
land-unprotected union caches. Fingerprints must include only the relevant
accepted input identities, schema/cache-contract version, and algorithm
identity needed to detect stale reuse.

- PA-union cache: CAPAD identity.
- Land-union cache: Natural Earth identity.
- Land-unprotected cache: CAPAD plus Natural Earth identities.

A missing, malformed, or mismatched fingerprint invalidates and rebuilds the
cache. Do not redesign the cache system or introduce a general cache
framework.

### 6. Narrow Runner Hardening

The canonical runner must:

- locate the repository root from its own path and run from that root;
- check the dev environment and required triad-fixture path before work;
- expose an explicit Layer A remote mode that propagates
  `DSIPA_SKIP_LAYERB=1`, workers, and the ten-code state list;
- suppress redundant per-state artefact emission while preserving the merged
  national artefact;
- run input validation before expensive national computation;
- run output validation before QA/build; and
- run accepted report-only modules in dependency order:
  `layerA_tables`, `layerA_buffer_sensitivity`,
  `layerA_threshold_sensitivity`, `layerA_edge_decision`, and
  `layerA_watchlists`.

Canonical surfaces must regenerate to 1,432 and 12.9%. The old 1,427 value may
remain only in explicit historical reconciliation.

### 7. Exactly One National Regression Run

After all local and clean-checkout gates pass, run exactly one clean national
Layer A regression on `deep-server` with:

```text
DSIPA_SKIP_LAYERB=1
DSIPA_WORKERS=12
DSIPA_STATES=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT
```

Use the accepted Goal 011 payload as the comparison baseline. Preserve the
exact base commit, uncommitted implementation overlay and hashes, command,
environment, package versions, host/resources, logs, terminal status, source
diff/inventory, nine outputs, checksums, semantic comparison, ordering proof,
headline comparison, tests, build result, and canonical reports under one
unique DSIPA artefact path.

Byte changes caused only by stable ordering or GPKG container metadata are
acceptable only with explicit semantic proof. Any primary-value drift stops
the goal.

## Permitted Implementation Scope

Implementation writes must remain within these file families:

- `settings/layerA_reference_contract_v0_3_0.json`;
- `Makefile`;
- `analysis/run_full_pipeline.sh`;
- `analysis/deep_server_tmux_run.sh`;
- `src/python/dsipa/triad.py`;
- `src/python/dsipa/pa_geometry.py`;
- `src/python/dsipa/ibra.py`;
- `src/python/dsipa/landmask.py`;
- `src/python/dsipa/layerA_national.py`;
- `src/python/dsipa/layerA_statewise.py`;
- one new `src/python/dsipa/layerA_reproducibility.py`;
- directly corresponding `tests/python/test_*.py` files;
- optional text-based fixtures only under `tests/fixtures/layerA_triad/`;
- these accepted report surfaces:
  `national_layerA_coverage_and_sanity.md`,
  `layerA_sanity_dashboard.md`,
  `layerA_denominators_and_censoring.{csv,md}`,
  `layerA_edge_profile_decision.{csv,md}`, and
  `layerA_table1_candidate.md`;
- this Goal 012 packet plus
  `LayerA_Consolidation_Closeout.md`;
- `docs/log/132_layerA_consolidation_reproducibility_hardening.md`; and
- one narrow `docs/stage_overview.md` update.

Do not edit Layer B modules, manuscript files, generated national payloads
locally, schemas, dependencies, or unrelated documentation.

## Acceptance Criteria

- Starting and final Git evidence is exact; the diff is limited to the
  permitted footprint.
- Targeted unit and contract tests pass.
- True fresh-checkout/archive pytest passes offline with both real triad
  geometry/buffer checks executed, not skipped.
- Full pytest and wheel/sdist build pass.
- Shell syntax and runner-contract tests pass.
- Positive and mismatch tests prove fail-closed input, reference-contract, and
  cache-fingerprint behaviour.
- State and merged output tests prove zero stable-key ordering descents.
- Exactly one clean remote national Layer A run reaches a terminal state with
  complete preserved evidence.
- All nine outputs reconcile semantically with Goal 011; allowable byte
  differences are explained.
- All frozen headlines match exactly.
- Canonical reports show 1,432/12.9%; 1,427 remains only in historical
  reconciliation.
- `LayerA_Consolidation_Closeout.md` records the complete evidence and
  residual risks.
- An independent orchestrator review accepts the evidence.
- No commit or push occurs until explicitly requested after review.

## Non-Goals

No Layer B reacquisition or modelling, 2025 VIIRS, new science, manuscript
rewrite, DOI upload or minting, Zenodo publication, submission, dependency
upgrade, schema redesign, broad architecture rewrite, monolithic
`layerA_national` split, `dsipa-run` repurposing, byte-identical GPKG chase,
style-only cleanup, or local editing of generated national payloads.

## Stop Rules

Stop and report without improvising if:

- the local baseline or permitted footprint drifts;
- accepted inputs or the Goal 011 comparison payload are unavailable;
- any accepted input identity mismatches;
- tests or build still fail after one focused repair;
- a primary headline changes;
- the remote artefact or checksum record is incomplete;
- a methodological change becomes necessary or ambiguous;
- a second national regression would be required; or
- work expands beyond the bounded 80/20 scope.

On completion or blockage, send the orchestrator a short wake-up containing
status and the Goal 012 closeout path.

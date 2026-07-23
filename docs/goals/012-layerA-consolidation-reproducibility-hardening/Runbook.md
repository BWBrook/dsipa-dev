# Runbook: Goal 012 Layer A Consolidation And Reproducibility Hardening

Run local commands from `/Users/bwbrook/papers/dsipa-dev`.

## Local Baseline Gate

```bash
pwd
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git status --short --branch
```

Required:

```text
branch = main
HEAD = origin/main = 1b39dcc1403a40c3962f04c922bb612c41f83a8f
status = ## main...origin/main
```

Stop without mutation for any difference.

## Frozen Runtime Contract

```text
schema = 0.3.0
years = 2013-2024
workers = 12
states = ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT
skip_layerB = 1
```

Reference contract:

```text
settings/layerA_reference_contract_v0_3_0.json
```

Accepted comparison payload:

```text
/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation
```

## Contract Validation

The reference-contract loader must fail on:

- missing or malformed JSON;
- wrong contract or analysis-schema version;
- incomplete 2013-2024 VIIRS coverage;
- duplicate or missing approved outputs;
- missing stable keys or frozen headlines;
- internally inconsistent classifications/hashes; or
- missing historical 1,427 versus accepted 1,432 reconciliation.

Test the positive contract and one mutation for each failure class. Do not
duplicate contract hashes in test source; derive mutations from the loaded
contract.

## Offline Triad QA

A fresh checkout/archive must not contain or require ignored repository-local
triad GPKGs. Tests may create deterministic temporary files or use explicitly
tracked, provenance-verified fixtures.

Required proof:

```text
pytest network calls to CAPAD = 0
triad geometry check = passed, not skipped
triad buffer check = passed, not skipped
fresh checkout status after pytest = clean
```

Do not satisfy this gate by weakening, deleting, or skipping the existing
geometry/buffer assertions.

## Accepted Input Gate

Canonical execution must verify:

```text
CAPAD feature_count = 14403
CAPAD semantic_sha256 = 148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf
IBRA feature_count = 89
IBRA semantic_sha256 = 3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332
Natural Earth size_bytes = 69700
Natural Earth sha256 = 1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de
VIIRS years = 2013-2024
VIIRS MD5 = existing code-pinned EXPECTED_MD5 values
```

Mismatch exits non-zero before statewise national computation. The canonical
path has no permissive override.

## Cache Fingerprint Contract

Use compact JSON sidecars adjacent to the existing cache files. Each sidecar
must record cache-contract version, relevant accepted input fingerprints,
algorithm identity, cache path, and cache-file checksum.

On load:

1. require cache and sidecar;
2. validate sidecar schema;
3. compare relevant current input fingerprints;
4. compare cache-file checksum; and
5. rebuild on any missing or mismatched state.

Test valid reuse plus missing, malformed, CAPAD-mismatch, Natural
Earth-mismatch, and cache-file-mismatch cases. Do not introduce a general cache
registry.

## Stable Serialization Contract

Sort with a stable algorithm and explicit null placement immediately before
writing state and merged tables:

```text
radiance: pa_id,year,zone,buffer_km,buffer_type
edge: pa_id,year,ring_index
validity: pa_id,buffer_km
```

Tests must:

- feed shuffled state tables and reversed state lists;
- verify identical ordered output across repetitions;
- verify zero adjacent stable-key descents;
- verify row count, key set, column order, dtypes/values, and schema are
  unchanged; and
- verify only the merged national artefact is emitted.

Accepted baseline counts:

```text
radiance rows = 900768; Goal 011 descents = 1941
edge rows = 400788; Goal 011 descents = 845
Goal 012 canonical descents = 0 for both
```

## Runner Contract

Required step order:

1. self-locate root and enter it;
2. verify `uv`, dev dependencies, and fixture strategy;
3. generate CAPAD and IBRA inputs;
4. run fail-closed accepted-input validation;
5. run statewise Layer A and deterministic merge;
6. run sanity, trends, uncertainty, vulnerability, and Layer A figures;
7. run report-only modules in this order:
   `layerA_tables`, `layerA_buffer_sensitivity`,
   `layerA_threshold_sensitivity`, `layerA_edge_decision`,
   `layerA_watchlists`;
8. run figure inventory and schema reference;
9. run fail-closed nine-output/reference validation;
10. run full pytest; and
11. build wheel and sdist.

Add an explicit `layerA` mode to the remote harness. A local dry-run or
contract test must prove the frozen environment and command without SSH.

Validation:

```bash
bash -n analysis/run_full_pipeline.sh
bash -n analysis/deep_server_tmux_run.sh
```

## Local Test Ladder

Run the narrowest relevant tests first, then:

```bash
uv run pytest -rs
uv run python -m build --sdist --wheel
git diff --check
git status --short --branch
```

Fresh-checkout proof must use a temporary directory created from committed
files only. Disable network for pytest, run the full suite, capture skip
reasons, and prove the two triad geometry/buffer tests executed.

Do not proceed to the national run while any local gate is red.

## Single Remote Regression

The executor may run exactly one national Layer A regression after local gates
pass.

Create an isolated remote sibling from baseline HEAD. Because commit/push is
not authorized, overlay only the permitted local implementation files and
preserve:

- base commit and tree;
- local and remote overlay path lists;
- binary-capable diff where applicable;
- SHA-256 for each overlaid file;
- deterministic tracked-tree inventory after overlay; and
- remote `git status --short`.

Run through the new explicit Layer A mode with a unique run id. Preserve under
`/data/codex/artifacts/dsipa/<run-id>/`:

- exact command and environment;
- source identity/diff and clean baseline proof;
- resource and package snapshots;
- terminal status and complete log;
- input-gate and cache-fingerprint evidence;
- nine outputs and checksums;
- ordering metrics;
- semantic and headline reconciliation;
- canonical reports;
- pytest and build logs; and
- an artefact-level checksum index.

Do not start a second national run. If the first fails after the one permitted
local repair pass, close Goal 012 as blocked with exact evidence.

## Nine-Output Reconciliation

For each approved output:

1. verify presence, size, schema, rows, columns, keys, and SHA-256;
2. compare to the Goal 011 archive candidate;
3. prove exact value equality after canonical key sort for CSVs;
4. use attribute/CRS/geometry semantic comparison for GPKG;
5. classify byte changes as ordering, container metadata, substantive drift,
   or unexplained; and
6. stop for any unexplained value or primary-headline difference.

The six Goal 011 exact-hash outputs may change bytes only if deterministic
ordering affects them; semantic equality must still be exact.

## Canonical Report Gate

Regenerate reports through accepted report modules, not manual value edits.

Required scan:

```text
canonical current ring-1 = 1432 / 12.9%
historical reconciliation = 1427 versus 1432
```

Search all current release surfaces. Any unexplained current-use `1,427` or
`12.8%` blocks acceptance; historical logs and explicit reconciliation are
allowed.

## Final Review And Publication Boundary

Write a compact closeout with:

- exact start/final Git evidence;
- changed footprint;
- local/fresh-checkout/remote validation;
- nine-output reconciliation;
- frozen-headline table;
- canonical report scan;
- residual limitations; and
- final recommendation.

Closeout path:

```text
docs/goals/012-layerA-consolidation-reproducibility-hardening/LayerA_Consolidation_Closeout.md
```

Request independent orchestrator review. Do not stage, commit, or push until
the orchestrator explicitly requests publication.

Send a short wake-up containing:

```text
Goal 012 status: COMPLETE or BLOCKED
Closeout: <repo-relative-path>
```

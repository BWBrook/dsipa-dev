# Runbook: Goal 011 Layer A Preservation Reproduction

Run local commands from `/Users/bwbrook/papers/dsipa-dev`.

## Local Gate

```bash
pwd
git branch --show-current
git rev-parse HEAD
git status --short --branch
git rev-parse origin/main
test -f AGENTS.md
```

Expected accepted commit:

```text
7f46a00f74c32881034f0129728b3d80eedd2442
```

## Read-Only Remote Preflight

Use `ssh -o BatchMode=yes -o ConnectTimeout=8 deep-server-ts` to record:

- hostname and route;
- CPU, RAM, and `/data` capacity;
- `uv`, Python, `tmux`, git, and operating-system versions;
- DSIPA checkout locations, HEADs, branches, remotes, and status;
- required nightlights, CAPAD/geometry, Natural Earth/cache, and IBRA inputs.

Do not modify a remote checkout during preflight.

The initial 2026-07-23 preflight was preserved as provisional Phase 1 run
`20260723T060854Z-goal011-layerA-preservation-blocked`. An independent
provenance audit subsequently authorized controlled reacquisition under the
gate below. The Phase 1 record is not the final Goal 011 outcome.

## Exact Source Materialization

Create a fresh sibling by streaming the accepted local tree:

```bash
git archive 7f46a00f74c32881034f0129728b3d80eedd2442 |
  ssh deep-server-ts 'tar -x -C <fresh-remote-sibling>'
```

Record:

- accepted commit:
  `7f46a00f74c32881034f0129728b3d80eedd2442`;
- accepted tree object from local `git rev-parse
  7f46a00f74c32881034f0129728b3d80eedd2442^{tree}`:
  `c82ebdda83c987d2e1dcc79fb2dba2759f9d7739`;
- accepted archive entry count: 354;
- streamed archive SHA-256;
- a deterministic post-extraction tracked-tree inventory/hash; and
- the source/transfer command and time.

Do not read from or modify the dirty remote checkout to construct this tree.

## Fail-Closed Acquisition Gate

Use the unchanged modules/helpers in the isolated source tree and stop before
the expensive pipeline unless all hard pins pass:

```text
CAPAD feature_count = 14403
CAPAD pa_id_hash_sha256 = 148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf
IBRA feature_count = 89
IBRA ibra_hash_sha256 = 3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332
Zenodo v0.4 years = 2013-2024
Zenodo file MD5s = code-pinned EXPECTED_MD5 values
```

Acquire Natural Earth 110m land only through the unchanged official-S3 helper.
Require the tracked release marker, archive size 69,700 bytes, and SHA-256
`1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`.
This input is version-reacquirable but not historically byte-pinned; that
limitation must remain explicit even if all regenerated science matches.

## Required Pipeline Environment

```bash
export DSIPA_SKIP_LAYERB=1
export DSIPA_WORKERS=12
export DSIPA_STATES=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT
analysis/run_full_pipeline.sh
```

Launch through `analysis/deep_server_tmux_run.sh --mode custom` against the
isolated remote checkout, with a unique `--run-id` and `--session`, for
example:

```bash
analysis/deep_server_tmux_run.sh \
  --mode custom \
  --command 'DSIPA_SKIP_LAYERB=1 DSIPA_WORKERS=12 DSIPA_STATES=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT analysis/run_full_pipeline.sh'
```

Do not use harness `full` mode for Goal 011: it does not propagate the local
`DSIPA_SKIP_LAYERB` value into `run_remote.sh`.

## Approved Output Payload

```text
data/processed/pa_radiance_buffers_national_v0_3_0.csv
data/processed/pa_edge_profiles_national_v0_3_0.csv
data/processed/pa_buffer_validity_v0_3_0.csv
data/processed/pa_trends_v0_3_0.csv
data/processed/pa_risk_rankings_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.gpkg
data/processed/pa_ibra_assignment_v0_3_0.csv
data/processed/pa_trend_bootstrap_summary_v0_3_0.csv
```

Historical hashes are pinned in `data/README.md`,
`analysis/reports/reproducibility_audit.md`, and
`analysis/reports/evidence_reconciliation.json`.

## Terminal Outcome Check

The run is terminal when the tmux session has exited and the log plus recorded
exit status show success or a precise failure. Do not infer success solely
from a missing tmux session.

Goal 011 terminal controlled run:

```text
run id: 20260723T062202Z-goal011-layerA-preservation
remote repo: /data/codex/repos/dsipa-dev-goal011-20260723T062202Z
remote artefact: /data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation
remote scratch: /data/codex/scratch/dsipa/20260723T062202Z-goal011-layerA-preservation
pipeline status: failed
pipeline exit code: 1
```

National computation, trends, uncertainty, vulnerability, and figure
generation completed. The terminal failure occurred in QA because the clean
archive did not contain two ignored triad GPKG fixtures. The bounded repair
ran `dsipa.triad --skip-artefact`, then full pytest passed 49 tests and the
sdist/wheel build completed.

## Reconciliation

For all nine files:

1. verify presence, size, and SHA-256;
2. compare historical hash;
3. compare schema, row count, stable keys, numeric values, and categories when
   bytes differ;
4. recompute accepted headline values from regenerated data;
5. compare generated reports/figures to accepted evidence where relevant.

Classify each file as exact, byte-different with unresolved historical
row/feature equality, bounded secondary scientific drift, or missing/failed.
Do not force non-identical files into a representation-only category.

Goal 011 found:

- six exact files: buffer validity, trends, risk rankings, geometry CSV, IBRA
  assignment, and bootstrap summary;
- a byte-different radiance CSV with unchanged primary downstream
  hashes/headlines, but no historical payload for row-level proof;
- bounded secondary edge-profile drift: 1-5 km valid PA count 1,432 versus
  1,427, while complete-ring n remains 383; and
- a byte-different GPKG whose pipeline and input-gate copies are identical in
  attributes and geometry WKB, but whose historical payload is unavailable
  for direct feature comparison.

## Required Validation

```bash
python3 -m json.tool analysis/reports/layerA_preservation_manifest_2026-07-23.json
git diff --check
git status --short --branch
```

Also verify remote file presence/checksums, inspect raw pipeline pytest/build
results, and report targeted invariant counts.

## Forbidden Actions

Do not edit source, tests, scientific configuration, schema, methods,
thresholds, manuscript, or generated accepted science to force a match. Do not
run Layer B, redownload inputs, publish externally, commit, or push.

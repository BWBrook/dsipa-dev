# Goal 011: Layer A Preservation Reproduction

## Objective

Determine whether the accepted DSIPA Layer A analysis can be reproduced
unchanged from repository commit
`7f46a00f74c32881034f0129728b3d80eedd2442`, regenerate the nine approved
2013-2024 national Layer A outputs in an isolated `deep-server` run, and
produce a precise hash and scientific reconciliation record.

This is a preservation run, not a refactor or a new scientific analysis.

## Starting State

- Action repo: `/Users/bwbrook/papers/dsipa-dev`
- Accepted branch/commit at dispatch: `main` at
  `7f46a00f74c32881034f0129728b3d80eedd2442`
- Accepted source: Zenodo/OpenGeoHub nightlights v0.4, 2013-2024
- Output schema: `v0.3.0`
- Goal 010 recovery result: one of nine approved Layer A payloads was present;
  eight require regeneration.

Stop rather than silently using another commit if local `main` has
legitimately advanced before execution begins.

## Required Result

1. A terminal isolated remote run, whether successful or evidence-backed
   blocked/failed.
2. Exact source, input, environment, command, host, run, and git identity.
3. All nine approved Layer A outputs preserved under
   `/data/codex/artifacts/dsipa/<run-id>/`, or an exact cause for each missing
   output.
4. A machine-readable output manifest with paths, sizes, and SHA-256 values.
5. Structured comparison with the historical pinned hashes, schemas, row
   counts, keys, numeric values, categories, reports, figures, and accepted
   scientific headline values.
6. Existing pipeline tests/build results and targeted scientific invariants.
7. A closeout that distinguishes byte/representation drift from scientific
   drift and does not infer equivalence from tests alone.

## Accepted Scientific Headline Values

- Protected-area universe: 11,133
- Eligible baseline/trend subset: 4,426
- 2024 zero inside mean: 3,844/4,426
- Exact-zero inside slopes: 3,969/4,426
- Positive inside slopes: 420/4,426
- Retention denominator: 3,858
- Quadrants: Q1=305, Q2=55, Q3=3,308, Q4=190
- Complete rings: n=383

Any material difference in these values stops publication-readiness claims.
Diagnose and report drift without changing methods or manuscript.

## Scope And Mutation Boundary

Local writes are limited to Goal 011 documentation, logs, and compact
reconciliation reports in `/Users/bwbrook/papers/dsipa-dev`.

Remote writes are limited to DSIPA-owned paths:

- `/data/codex/repos`
- `/data/codex/scratch/dsipa`
- `/data/codex/artifacts/dsipa`

The legacy checkout `/home/bwbrook/papers/dsipa-dev` may be inspected
read-only. Do not clean, reset, or mutate a dirty remote checkout.

An isolated sibling checkout/run root may be created at the accepted commit.
Immutable required inputs may be copied or linked into it with provenance and
checksums recorded.

## Required Execution

- Materialize the exact accepted source tree into a fresh remote sibling by
  streaming local `git archive
  7f46a00f74c32881034f0129728b3d80eedd2442`; record the commit, tree,
  archive, and transfer provenance. The accepted source tree is
  `c82ebdda83c987d2e1dcc79fb2dba2759f9d7739` (354 archive entries). Do not
  use or modify the dirty remote checkout.
- Controlled input reacquisition is authorized only behind this fail-closed
  gate:
  - CAPAD 2024: require raw feature count 14,403 and semantic
    `pa_id_hash_sha256`
    `148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf`;
  - IBRA 7.1: require feature count 89 and semantic `ibra_hash_sha256`
    `3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332`;
  - Zenodo/OpenGeoHub v0.4: require all 12 annual files to pass the unchanged
    downloader's code-pinned MD5 values;
  - Natural Earth 110m land: use the documented official S3 URL, require the
    tracked version marker, require current archive size 69,700 bytes and
    SHA-256
    `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`,
    and classify it as version-reacquirable but not historically-byte-pinned.
- Stop before the expensive Layer A run if any fail-closed input check fails.
- Run `analysis/run_full_pipeline.sh` unchanged through the existing tmux
  harness in `custom` mode so the Layer B skip flag is propagated, with:
  - `DSIPA_SKIP_LAYERB=1`
  - `DSIPA_WORKERS=12`
  - `DSIPA_STATES=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT`
- Use `analysis/deep_server_tmux_run.sh --mode custom --command ...` and a
  unique Goal 011 run identifier. The harness `full` mode does not propagate
  `DSIPA_SKIP_LAYERB` into its remote run environment.
- Preserve logs, resource snapshot, package/environment versions, exact
  command, git status/HEAD, input provenance/checksums, output
  checksums/sizes, test/build results, and the nine approved outputs.
- Do not publish or upload externally.

## Acceptance Criteria

- The remote run is terminal, not merely queued.
- Exact source/input/run identity is recorded.
- The nine approved files are regenerated and preserved, or every absence has
  a precise cause.
- Reconciliation covers hashes and the accepted scientific quantities.
- Tests/build and targeted invariants are reported with raw results.
- The local diff is limited to Goal 011 documentation and compact reports.

## Non-Goals

No refactoring, redundancy cleanup, dependency updates, source edits, schema
changes, estimator or threshold changes, new science, manuscript rewriting,
title/journal changes, 2025 VIIRS work, Layer B work, archive upload, DOI
minting, GitHub release, tag, PR, commit, or push.

## Stop Rules

- Stop before mutation if local overlapping work is dirty.
- Never reset or clean user state.
- The original bounded search found the accepted files absent. Its
  `blocked_preflight` artefact is the provisional Phase 1 record, not the final
  Goal 011 outcome. Controlled reacquisition is now authorized only under the
  exact fail-closed gate above; do not substitute other sources.
- Diagnose one failed run and repair only environmental/orchestration issues
  that do not alter source or science.
- Two consecutive attempts without material new evidence end the goal as
  blocked.
- Perform one focused self-review and repair pass after the core result. Stop
  when additional work is only polish.

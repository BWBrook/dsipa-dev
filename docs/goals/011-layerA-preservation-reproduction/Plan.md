# Plan: Goal 011 Layer A Preservation Reproduction

## Purpose

Reproduce the accepted Layer A analysis unchanged at its accepted commit,
preserve the regenerated nine-file payload remotely, and distinguish
representation drift from scientific drift.

## Steps

1. Confirm local identity and contract.
   - Record `pwd`, branch, HEAD, status, `origin/main`, and repo-local
     `AGENTS.md`.
   - Stop for overlapping dirt or a legitimate advance from the accepted
     commit.

2. Preflight `deep-server-ts` read-only.
   - Verify route, host, resources, `uv`, Python, `tmux`, `/data` capacity,
     relevant DSIPA checkouts, their identity/status, and required input
     availability.
   - Do not clean or reset any checkout.

3. Establish isolated execution state.
   - Stream the exact source tree from local `git archive
     7f46a00f74c32881034f0129728b3d80eedd2442` into a fresh remote sibling.
   - Record source commit/tree/archive identity without using the dirty remote
     checkout.
   - Reacquire CAPAD 2024, IBRA 7.1, Zenodo v0.4 nightlights, and Natural Earth
     110m land only from the source locations encoded by the unchanged code.
   - Fail closed unless CAPAD count/hash, IBRA count/hash, and all 12
     nightlight MD5s match their accepted pins.
   - Record the full Natural Earth archive SHA-256 and size and carry its
     version-reacquirable but not historically-byte-pinned limitation.

4. Run the accepted pipeline.
   - Use a unique Goal 011 run id and the existing tmux harness.
   - Set `DSIPA_SKIP_LAYERB=1`, workers to 12, and the complete ten-code state
     list.
   - Monitor until terminal completion; observation timeouts are not worker
     deadlines.
   - Treat the earlier `blocked_preflight` record as provisional Phase 1
     evidence; the controlled run receives a new run id.

5. Preserve the evidence payload.
   - Copy all nine approved Layer A outputs plus run logs, environment and
     resource snapshots, exact command, tests/build results, reports, and
     figures needed for reconciliation to the run artefact directory.
   - Write and validate a machine-readable manifest.

6. Reconcile.
   - Compare SHA-256 values with the historical evidence snapshot.
   - For non-identical files, compare schemas, row counts, keys, categories,
     and numeric values.
   - Recompute and compare the accepted scientific headline values.
   - Treat any material scientific difference as a preservation concern.

7. Close out and validate.
   - Write the Goal 011 reconciliation report, closeout, goal log, and stage
     log.
   - Run JSON validation, file-presence/checksum checks, `git diff --check`,
     pipeline test/build review, and targeted scientific invariants.
   - Perform one focused self-review/repair pass, then return control without
     committing or pushing.

## 80/20 Stop Rule

Deliver the complete preservation evidence and one focused repair pass. Do not
spend further cycles on cosmetic differences unless they conceal scientific
drift, a validation defect, or missing required evidence.

## Completion Record

All seven steps were completed on 2026-07-23. The terminal controlled run is
`20260723T062202Z-goal011-layerA-preservation`; its remote artefact is
`/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation`.
The pipeline itself ended `failed` with exit code 1 at QA because a clean
source archive omitted two ignored triad fixtures. A bounded validation repair
generated the fixtures without editing source, after which all 49 tests passed
and both package distributions built.

All nine approved outputs were preserved. Six match their historical hashes
exactly. All accepted primary scientific headline values match, while the
edge-profile output has a bounded secondary threshold-sensitive difference.
The historical radiance and GPKG payloads remain unavailable for direct
row/feature comparison, so Goal 011 is a concordant but non-exact
reproduction.

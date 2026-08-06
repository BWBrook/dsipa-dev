# Goal 017: Lean-Path Consolidation Closeout

## Conclusion

Goal 017 is ready for orchestrator review. The bounded consolidation fixes the
Layer B clean-tree contradiction, removes duplicated Git-state rules and two
superseded release helpers, and establishes truthful fast/release gates without
changing scientific outputs or claims. No commit or push was made.

## Repository state

- Start and final branch: `main`.
- HEAD and `origin/main`: `00e43f0d2a127c62eadd14fd8bb9eb5ef38fa9c5`.
- The final dirty state contains only the inherited Goal 017 work and its
  completed tests/docs; no generated data, reports, figures, build outputs, or
  unrelated files were added.

## Lean product promise and active flow

DSIPA's active product remains one canonical Layer A analysis plus a compact,
bias-limited Layer B diagnostic and the evidence needed to support the paper.
The retained Layer B execution flow is:

```text
clean-start gate -> Layer B data -> QC/licensing -> modelling -> figures
                 -> expected-path artefacts and manifests
```

Direct Layer B commands require a fully clean tree before any network, data, or
model work. The canonical full runner performs one clean-start gate, then uses
`--allow-dirty` only for the three explicit intra-pipeline Layer B handoffs.

## Dispositions

### Retain

- Layer A code, schemas, contracts, tests, data identities, and manuscript
  surfaces unchanged.
- `DSIPA_SKIP_LAYERB`, `--skip-artefact`, `--artefact-only`, and
  `--allow-dirty`; each has a current bounded workflow.
- `radiance_smoketest.py`, `ring_profiles_smoketest.py`, and
  `data_inventory.py`; deletion evidence was not strong enough for this goal.
- `layerB_gonogo.py`; it has current scientific configuration, decision, and
  test consumers.
- Existing RSEC and scientific tests.

### Simplify

- Replaced four private Git probes and three duplicated enforcement pairs with
  one `dsipa.git_state` implementation.
- Git enforcement now fails closed when status cannot be inspected and uses
  `git status --no-renames` so an expected destination cannot hide a deleted
  source path.
- Manifests distinguish expected generated changes from unexplained dirt and
  store expected paths relative to the repository.
- Added `make fast` for imports plus targeted deterministic fixture/domain
  tests; `make test`, build, output/manuscript checks, and remote evidence runs
  remain decision-relevant release gates.

### Delete

- `analysis/build_final_release.py` (79 lines): superseded by the accepted
  release manifest and Goal 014/015 archive/DOI workflow; no live caller.
- `analysis/zenodo_release_checklist.sh` (105 lines): encoded the superseded
  pre-release checklist and had no live caller after DOI publication.

Historical goals, reports, cover letters, and DOI receipts were preserved.

### Defer

- Splitting the large Layer B modules and broader helper extraction.
- Further smoke/inventory candidate deletion.
- A general mid-run external-edit snapshot or monitoring framework.
- Any national, ALA, model, manuscript, release, or remote execution.

## Complexity before and after

Before, Layer B data, QC, and modelling each carried its own Git probe and
clean-tree guard, while manifest collection had a fourth probe with different
failure semantics. After, those seven duplicated functions are gone and one
shared helper owns the rule. Two obsolete executable scripts (184 lines total)
are removed. The active Layer B modules grow slightly to name their upstream
and own-output boundaries explicitly; line count was not treated as the goal.

## Protected invariants

The diff is empty for `manuscript/`, `data/`, `settings/`, `analysis/reports/`,
`pyproject.toml`, `uv.lock`, `schema.py`, and `layerA_reproducibility.py`.
Accordingly, no accepted result, row/schema identity, figure, claim, reference
contract, dependency, DOI/licensing receipt, or Layer A scientific definition
changed. No real data, ALA, remote, national, model, manuscript, or release run
was performed.

## Verification

- Focused red/green guard, manifest, entry-point, and runner tests: 18 passed.
- `make fast`: 57 passed.
- `make test`: 97 passed, 9 skipped because national/geometry/ranking outputs
  are not present locally; the skips were reported rather than treated as
  exercised evidence.
- `bash -n analysis/run_full_pipeline.sh`: passed.
- `uv build` to a temporary output directory: sdist and wheel built.
- `git diff --check`: passed.
- Protected-surface diff: empty.

## Focused review and stopping point

One focused review checked imports, direct-entry ordering, upstream versus
stage-owned paths, rename handling, fail-closed behavior, manifest path
portability, runner handoff confinement, deleted-script callers, build churn,
and protected surfaces. No further material defect was found.

The remaining risk is bounded: a user can explicitly bypass direct guards with
`--allow-dirty`, and the canonical runner does not detect an unrelated edit
introduced after its clean-start gate. That is accepted for this private,
single-user research workflow; adding continuous snapshot enforcement would be
disproportionate. Real-data Layer B execution remains to be exercised only when
a later scientific goal makes it decision-relevant.

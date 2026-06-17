# Runbook: Goal 004 Stage 3B ALA Ingest Guardrail

## Working Directory

```bash
cd /Users/bwbrook/papers/dsipa-dev
```

## Required Starting Checks

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/004-stage3B-ala-ingest-guardrail/Goal.md
```

## Suggested Reading Order

```text
AGENTS.md
README.md
docs/stage3_layerB_reconciliation_plan.md
docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md
docs/stage1_critique_resolution_matrix.md
docs/log/123_stage3A_layerB_evidence_integration.md
src/python/dsipa/layerB_data.py
tests/python/test_layerB_filters.py
tests/python/test_layerB_summary.py
tests/python/test_layerB_gonogo.py
```

## Suggested Test Targets

The test file will likely need helpers that create zip files under `tmp_path`.
Useful cases:

- malformed path with non-zip bytes;
- zip with `notes.txt` only;
- zip with `data.csv` smaller than `MIN_DATA_BYTES`;
- zip with `data.csv` at least `MIN_DATA_BYTES` but fewer than
  `MIN_DATA_ROWS`;
- zip with `data.csv` at least `MIN_DATA_BYTES` and at least `MIN_DATA_ROWS`;
- `find_valid_zips(tmp_path, key)` returns only the valid candidate for the
  requested key.

Direct tests of `_validate_download_zip` are acceptable because the goal is a
specific guardrail around the private ingest validator. Also include at least
one public-helper test through `find_valid_zips`.

## Validation Commands

Run from the repo root.

```bash
git status --short --branch
git diff --check
uv run python -m pytest tests/python/test_layerB_download_guardrail.py tests/python/test_layerB_filters.py tests/python/test_layerB_summary.py tests/python/test_layerB_gonogo.py -q
uv build --out-dir /tmp/dsipa-build-goal004
```

## Closeout Memo Shape

Use this structure for
`docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md`:

```md
# Stage 3B Closeout

## Summary Recommendation

## Current State

## Files Changed

## Guardrail Coverage

## Validation Results

## B10 And Stage 3 State

## Residual Risks

## Recommendation For Next Goal
```

## Wake-Up

After the closeout and log are complete, send the orchestrator a short
wake-up:

```text
Goal 004 complete. Closeout memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md
```

Use thread id:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

If thread tools are unavailable, state that in the final response and stop.

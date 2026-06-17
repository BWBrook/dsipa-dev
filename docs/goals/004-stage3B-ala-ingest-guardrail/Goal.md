# Goal 004: Stage 3B ALA Ingest Guardrail

## Objective

Close the remaining Stage 3 Layer B item B10 by adding a local synthetic-fixture
guardrail test for implausibly tiny, malformed, or sentinel ALA download zip
payloads.

This goal is complete when the Layer B ingest path is covered by targeted tests
that prove invalid ALA download payloads cannot silently enter the processing
pipeline, and when the closeout clearly says whether Stage 3 is ready to close
or needs a narrow follow-up.

## Why This Matters

Earlier Layer B work deferred Squamata after repeated ALA download failures.
The Stage 3 plan retained B10 as a small but important robustness guard:
download failures or service sentinels should fail loudly rather than being
treated as valid occurrence data. Goal 003 completed the manuscript-facing Layer
B integration, leaving this code/test item as the only remaining Stage 3 task.

This is a local test and minimal-guard goal, not a data-acquisition goal.

## Operating Mode

Test-first code guardrail. Add synthetic fixtures, run targeted tests, patch
only if the tests expose a real gap.

## Authorized Review Surface

You may create or update only these files unless blocked:

- `tests/python/test_layerB_download_guardrail.py`
- `src/python/dsipa/layerB_data.py`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/log/124_stage3B_ala_ingest_guardrail.md`
- `docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md`
- `docs/goals/004-stage3B-ala-ingest-guardrail/Log.md`

Only edit `src/python/dsipa/layerB_data.py` if a test-first pass demonstrates
that the existing validation is insufficient. If the current implementation
already rejects the invalid synthetic payloads, keep the code unchanged and
record that Stage 3B was a test coverage hardening goal.

Do not update `docs/stage_overview.md`; the DSIPA orchestrator will update
stage status after review and acceptance.

## Scope

In scope:

- add synthetic local zip fixtures inside tests, generated in test temp
  directories;
- test that tiny or malformed ALA-like zip payloads are rejected;
- test that zips without usable CSV payloads are rejected;
- test that zips with too-small `data.csv` or too few rows are rejected;
- test that a minimally valid local zip is accepted;
- test that `find_valid_zips` filters invalid zips and keeps valid zips;
- patch `src/python/dsipa/layerB_data.py` only if the tests expose a real
  guardrail gap;
- update B10 in `docs/stage1_critique_resolution_matrix.md`;
- write the Stage 3B log and closeout memo.

Out of scope:

- do not run live ALA downloads or HTTP calls;
- do not use Barry's ALA credentials or environment variables;
- do not process raw or filtered occurrence data;
- do not run Layer B modelling;
- do not run remote compute;
- do not edit manuscript text, figures, tables, or interpretation notes;
- do not perform release packaging, archive/DOI work, or Stage 4 planning;
- do not change Layer A;
- do not commit, push, merge, or open pull requests;
- do not contact Barry or Chief.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/stage3_layerB_reconciliation_plan.md`
- `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/log/123_stage3A_layerB_evidence_integration.md`
- `src/python/dsipa/layerB_data.py`
- `tests/python/test_layerB_filters.py`
- `tests/python/test_layerB_summary.py`
- `tests/python/test_layerB_gonogo.py`

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this Goal 004 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 003 at commit `f905172`. Treat files under
`docs/goals/004-stage3B-ala-ingest-guardrail/` as authorized working
instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, or open a PR.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  004 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Generate test fixtures in pytest temp directories only.
- Do not add binary zip fixtures to the repo.
- Do not use network access for ALA.
- Do not run remote compute.
- Do not run data-processing pipelines.
- Temporary build outputs may go under `/tmp`.

## Required Work

1. Reconstruct the Stage 3B contract from the accepted Stage 3 plan and Goal
   003 closeout.
2. Inspect the existing Layer B ingest guard functions in
   `src/python/dsipa/layerB_data.py`.
3. Add targeted tests in `tests/python/test_layerB_download_guardrail.py`.
4. Use synthetic zip files created at test runtime to cover, at minimum:
   - a malformed/non-zip payload;
   - a zip with no CSV files;
   - a zip with a too-small `data.csv`;
   - a zip with a large-enough `data.csv` but too few rows;
   - a minimally valid `data.csv`;
   - `find_valid_zips` filtering invalid candidates.
5. Run the new guardrail test before patching. If it already passes against
   existing code, do not patch the source.
6. If a test fails because the guardrail is insufficient, make the smallest
   source patch needed and rerun the targeted tests.
7. Update B10 in `docs/stage1_critique_resolution_matrix.md`.
8. Write `docs/log/124_stage3B_ala_ingest_guardrail.md`.
9. Write `Stage3B_Closeout.md` with a clear recommendation on whether Stage 3
   is ready to close.

## Validation Gates

Run from the repo root:

```bash
git status --short --branch
git diff --check
uv run python -m pytest tests/python/test_layerB_download_guardrail.py tests/python/test_layerB_filters.py tests/python/test_layerB_summary.py tests/python/test_layerB_gonogo.py -q
uv build --out-dir /tmp/dsipa-build-goal004
```

If `tests/python/test_layerB_summary.py` skips checks because optional ignored
Layer B summaries are absent, classify those skips explicitly. They are not
blocking for this guardrail goal.

Do not run full test suites, manuscript builds, live ALA downloads, data
pipelines, or remote commands unless the goal becomes blocked and the
orchestrator authorizes a scope change.

## Deliverables

- `tests/python/test_layerB_download_guardrail.py`
- minimal `src/python/dsipa/layerB_data.py` patch only if needed
- updated B10 row in `docs/stage1_critique_resolution_matrix.md`
- Stage 3B log:
  `docs/log/124_stage3B_ala_ingest_guardrail.md`
- Closeout memo:
  `docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md`
- updated `docs/goals/004-stage3B-ala-ingest-guardrail/Log.md`
- final response to the DSIPA orchestrator summarizing:
  - changed files;
  - whether source code changed or tests alone were sufficient;
  - validation commands and exact outcomes;
  - B10 resolution state;
  - current git status;
  - whether Stage 3 is ready to close;
  - whether any Barry-level decision is needed.

## Decision Authority

`nightlight` may decide:

- exact test helper structure;
- whether to test private validation helpers directly or through public helpers
  such as `find_valid_zips` and `iter_csv_chunks_from_zip`;
- whether source code needs a minimal patch after tests are written.

`nightlight` must pause or report blocked before:

- using live ALA services;
- running data processing or modelling;
- changing download semantics beyond rejecting invalid payloads;
- editing outside the authorized review surface;
- changing Stage 4 release/archive policy;
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 004 is complete or blocked and point
to the closeout memo path. If thread tools are unavailable at runtime, state
that in the final response and stop.

## Stop Conditions

Stop when one of these is true:

- Stage 3B guardrail coverage is complete, validation is classified, the
  closeout memo is written, and the log is updated;
- a blocker prevents test coverage or a necessary minimal guard patch;
- completing the work would require out-of-scope live ALA access, data
  processing, remote compute, release packaging, or publication decisions.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- whether existing code was sufficient or source patching was required;
- B10 state;
- blockers or residual risks;
- whether Stage 3 is ready to close or needs a narrow follow-up.

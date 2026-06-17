# Stage 3B ALA Ingest Guardrail

Date: 2026-06-17

## Scope

Goal 004 closed the B10 ALA ingest guardrail item using local synthetic zip
fixtures only. The work stayed inside the authorized Stage 3B review surface
and did not run live ALA calls, use ALA credentials, process occurrence data,
run Layer B modelling, edit manuscript files, or perform release/archive work.

## Starting State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch/HEAD: `main` at `f905172`
- Initial `git status --short --branch`: `## main...origin/main` plus the
  untracked Goal 004 packet directory.
- Repo-local `AGENTS.md` was available and followed.

## Source Inspection

`src/python/dsipa/layerB_data.py` already routes downloaded and discovered ALA
zip files through `_validate_download_zip()` and `_select_data_csv()`.
Existing guards reject non-zip payloads, archives without CSV files, selected
CSV files below `MIN_DATA_BYTES`, and selected CSV files with fewer than
`MIN_DATA_ROWS`.

No source-code change was required.

## Guardrail Coverage Added

Added `tests/python/test_layerB_download_guardrail.py` with runtime-generated
synthetic fixtures that cover:

- malformed `.zip` byte payloads;
- archives with no CSV file;
- tiny `data.csv` sentinel-like payloads;
- oversized header-only `data.csv` payloads with too few rows;
- a minimal valid `data.csv`;
- `find_valid_zips()` filtering invalid candidates while preserving valid
  key-matched downloads.

The tests create all zip payloads under `tmp_path`; no binary zip fixtures were
added to the repository.

## Validation

- `uv run python -m pytest tests/python/test_layerB_download_guardrail.py -q`
  passed: 6 tests.
- `uv run python -m pytest tests/python/test_layerB_download_guardrail.py tests/python/test_layerB_filters.py tests/python/test_layerB_summary.py tests/python/test_layerB_gonogo.py -q`
  passed: 15 tests.
- `uv build --out-dir /tmp/dsipa-build-goal004` passed and produced:
  - `/tmp/dsipa-build-goal004/dsipa_nbs-0.1.0.tar.gz`
  - `/tmp/dsipa-build-goal004/dsipa_nbs-0.1.0-py3-none-any.whl`
- `git diff --check` passed after document updates.

## B10 State

B10 is now marked `done` in `docs/stage1_critique_resolution_matrix.md` with
Stage 3B provenance. The closure is test-first and local-only: it verifies that
bad ALA download artefacts are rejected before ingestion, without exercising
network, credential, data-processing, or modelling paths.

## Recommendation

Stage 3B can be accepted as complete. With B10 closed and earlier Stage 3A
items already integrated, the orchestrator has a defensible basis to close
Stage 3 when it independently reviews the diff and validation evidence.

# 045_output_schema log

- Date/time (UTC): 2026-01-01 07:59 UTC
- Objectives: lock smoke-test output schema with versioning and regression tests.
- Actions taken:
  - Added centralized schema definitions and output file constants.
  - Generated `analysis/reports/output_schema_reference.md` and WP0.8 artefact folder.
  - Updated tests to enforce schema columns and schema_version values across triad, PA geometry, radiance buffers, and edge profiles.
  - Recorded schema policy decision (DEC-008).
  - Added interpretation notes for smoke-test radiance buffers and edge profiles.
- Outputs:
  - `analysis/reports/output_schema_reference.md`
  - `artefacts/wp0_8_schema_reference/`
  - `src/python/dsipa/schema.py`
  - `src/python/dsipa/schema_reference.py`
- Diagnostics / sanity checks:
  - Schema tests updated to fail on missing/renamed columns.
  - (Run) `uv run pytest` and `uv run python -m build`.
- Next steps:
  - Proceed to WP0.9 national run (Layer A metric tables).

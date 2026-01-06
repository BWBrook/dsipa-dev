# 105 Reproducibility audit (WP0.18)

Date: 2026-01-05

## Summary
- Added one-command full pipeline script: `analysis/run_full_pipeline.sh`.
- Wrote reproducibility audit report: `analysis/reports/reproducibility_audit.md`.
- Built final release artefact pack: `artefacts/final_release_20260105/`.

## Checks
- Tests: `uv run pytest` (pass).
- Build: `uv run python -m build --sdist --wheel` (pass).

## Notes
- Final artefact manifest reflects current git status; clean manifest requires committing pending WP0.17 updates.

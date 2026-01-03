# 098 Repo hygiene: keep national outputs out of git

Date: 2026-01-03

## Summary
- Added gitignore patterns for national-scale derived tables under `data/processed/`.
- Removed tracked national outputs (radiance buffers, edge profiles, buffer validity, trends, risk rankings) from git history going forward.
- Updated tests to skip when national outputs are absent; smoke-test fixtures remain in-repo.

## Rationale
National outputs are large and reproducible; tracking them in git bloats the repo and triggers snapshot warnings. They will be archived via Zenodo for paper release.

## Notes
- Smoke-test outputs and small CSV fixtures remain tracked for regression tests.
- Large GPKG outputs in `data/processed/` remain ignored by default and are regenerated as needed.

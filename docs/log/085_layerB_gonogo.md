# 085 Layer B go/no-go decision (WP0.14)

Date: 2026-01-02

## Summary
- Defined Layer B go/no-go criteria, focal taxa, negative controls, and bias strategy in `docs/layerB_gonogo.json`.
- Added `dsipa.layerB_gonogo` report generator and tests; produced the WP0.14 decision report and artefact.
- Recorded decisions DEC-009 (Layer B go/no-go) and DEC-011 (micro-area PA handling).

## Micro-area screening (context for DEC-011)
Using `data/processed/pa_geometries_v0_1_0.csv` and inside-zone valid pixel counts:
- Area < 0.01 km2: 218 PAs (1.96% of 11,133).
- Median valid pixels < 10: 6,707 PAs (60.24%); <25: 8,087 (72.64%).
- Area < 0.01 km2 and median valid pixels < 10: 218 PAs.
Decision: keep `min_valid_pixels=10` for baseline continuity and avoid discarding most PAs; treat area < 0.01 km2 and median valid pixels < 10 as sensitivity-only filters in later modelling.

## Artefacts
- `artefacts/wp0_14_layerB_gonogo/` (decision report + config + manifest).

## Tests and builds
- Tests: `uv run pytest` (21 passed)
- Build: `uv run python -m build` (sdist + wheel)

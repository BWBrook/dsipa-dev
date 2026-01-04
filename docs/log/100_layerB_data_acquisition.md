# 100 Layer B data acquisition (WP0.15) — in progress

Date: 2026-01-04

## Summary
- Implemented `dsipa.layerB_data` pipeline for ALA downloads, quality filters, deduplication, and QC reporting.
- Added Layer B summary schema + tests for filter logic and summary schema.
- Added gitignore rules for Layer B raw/processed outputs and documented planned data locations.

## Blocker
- ALA downloads require a contact email + reasonTypeId. Awaiting human input (see `docs/questions_for_human.md` Q-002).

## Planned outputs (once downloads run)
- `data/raw/ala_occurrences/*` (ignored; raw ALA downloads + metadata JSON)
- `data/processed/layerB/*` (ignored; filtered occurrence tables)
- `data/processed/layerB_occurrence_summary_v0_3_0.csv`
- `analysis/reports/layerB_data_qc.md`
- `artefacts/wp0_15_layerB_data/`

## Tests
- `uv run pytest`

## Update (2026-01-04)
- Received ALA email + reason (“research”) and added automatic reason-id resolution.
- Switched ALA downloads to `occurrences/download` (index/download returns 500), added column-normalisation for ALA headers, and download retries.
- Downloads succeeded for microbats (`microbats_20260104T020628Z.zip`) and diurnal birds (`diurnal_birds_20260104T020701Z.zip`).
- Added safer download selection (latest valid zip by default; optional `--use-all-downloads`).

## Blocker (current)
- ALA download service is returning 500 errors for diurnal reptiles (and currently fails for any new download request); need service recovery before completing WP0.15 processing/QC.

## Update (2026-01-04, later)
- Processed microbats + diurnal birds downloads (skipping reptiles) and generated `layerB_occurrence_summary_v0_3_0.csv` + `analysis/reports/layerB_data_qc.md`.
- Summary counts: microbats raw 108,695 → filtered 107,907 → dedup 63,716 (59 spp); passerines raw 2,845,757 → filtered 2,834,940 → dedup 2,378,378 (348 spp).
- Artefact created: `artefacts/wp0_15_layerB_data/` with manifest + QC outputs.
- DEC-026: Proceed with microbats + passerines only until ALA download service recovers for Squamata.
- Built sdist + wheel via `uv run python -m build`.
- Prepared PI review ZIP: `analysis/pi_review_wp0_15_20260104.zip` (excludes files >10 MB and large raw/processed caches).

# PI Cover Letter — Gate 0.6 (WP0.15 Layer B data acquisition)

Date: 2026-01-04

## Purpose
This note orients the WP0.15 review gate. It summarises Layer B occurrence acquisition, filters, QC outputs, and the current limitation on diurnal reptiles.

## What changed since Gate 0.5.3
- Implemented `dsipa.layerB_data` pipeline for ALA downloads, quality filters, 1 km grid/day deduplication, and QC summaries.
- Acquired and processed ALA occurrences for microbats (treatment) and diurnal passerines (primary negative control).
- Recorded provenance + checksums in `data/README.md`, added summary schema to the output reference.
- Documented a deferral of the diurnal reptile control due to ALA download service 500 errors (DEC-026).

## Key artefacts to review
- `analysis/reports/layerB_data_qc.md` (counts by year/state; filter summary)
- `data/processed/layerB_occurrence_summary_v0_3_0.csv` (summary table)
- `artefacts/wp0_15_layerB_data/` (QC outputs + manifest)
- `analysis/reports/output_schema_reference.md` (Layer B summary schema)
- `data/README.md` (ALA provenance + checksums)
- `docs/log/100_layerB_data_acquisition.md` (chronology + decisions)

## Notes / caveats
- ALA `occurrences/download` repeatedly returned HTTP 500 for Squamata queries on 2026-01-04; diurnal reptiles are deferred (DEC-026).
- Raw ALA downloads and filtered occurrence tables are kept in `data/raw/ala_occurrences/` and `data/processed/layerB/` but excluded from the review ZIP due to size; checksums are recorded.

## What I need from you
- Confirm it is acceptable to proceed with WP0.16 using microbats + passerines only, or provide an alternative path for the reptile control.

## Validation done
- Tests: `uv run pytest tests/python/test_layerB_filters.py tests/python/test_layerB_summary.py`
- Build: `uv run python -m build`

## Packaging note
- Review ZIP excludes files >10 MB to respect bandwidth constraints.

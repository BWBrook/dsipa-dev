# 010_data_acquisition log

- Date/time (UTC): 2026-01-01 04:39 UTC
- Objectives for this phase: Select CAPAD + night-lights sources; download metadata; record provenance/checksums.
- Actions taken:
  - Confirmed CAPAD 2024 source and ArcGIS REST service endpoints; downloaded technical specification PDF.
  - Confirmed VIIRS DNB annual VNL v2.2 source; downloaded readme metadata.
  - Generated `analysis/reports/data_inventory.md` and canonical artefact folder for WP0.3.
  - Updated `data/README.md` with provenance entries and checksums.
- Data sources & checksums recorded in `data/README.md` (Y/N): Y
- Issues/blockers (add questions to `docs/questions_for_human.md` if needed):
  - None.
- Decisions (if irreversible, also log in `docs/decisions.md`):
  - DEC-002: CAPAD 2024 via DCCEEW REST; terrestrial-only for core Layer A.
  - DEC-003: VIIRS DNB annual VNL v2.2, median-masked radiance band.
- Tests/builds:
  - `uv run pytest` (2 passed).
  - `uv run python -m build` (sdist + wheel).
- Sanity verdict: pass (metadata downloads and inventory report align with chosen sources).
- Next steps:
  - Begin WP0.4 smoke-test triad definition and input preparation.

---

## 2026-01-01 update — Night-lights source switch

- Switched night-lights source to Zenodo v0.4 (OpenGeoHub/Hengl) DOI 10.5281/zenodo.17294744 due to EOG auth gate.
- Updated data inventory and provenance records to reflect Zenodo source and smoke-test years (2013, 2018, 2024).

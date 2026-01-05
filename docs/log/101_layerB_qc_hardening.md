# 101 Layer B QC hardening (WP0.15b) — in progress

Date: 2026-01-04

## Summary
- Added WP0.15b to roadmap to address licensing + QC hardening before modelling.
- Implemented `dsipa.layerB_qc` for license ledger, extended QC, scope coverage, and exposure diagnostics.

## Planned outputs
- `data/processed/layerB_ala_license_ledger_v0_3_0.csv`
- `analysis/reports/layerB_ala_license_ledger.md`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `artefacts/wp0_15b_layerB_qc/`

## Notes
- Diurnal reptiles still deferred pending ALA download stability.
- Manifest canonicality will be re-run on a clean HEAD once code + docs are committed.

## Update (2026-01-04)
- Generated license ledger and reports:
  - `data/processed/layerB_ala_license_ledger_v0_3_0.csv`
  - `analysis/reports/layerB_ala_license_ledger.md`
- Extended QC: `analysis/reports/layerB_qc_extended.md`
  - Microbats dominated by NSW BioNet (dr368) at 88.8% of processed records.
  - Provider top-10 share is ~100% for microbats, ~99.7% for passerines.
  - Dedup loss fraction: microbats 0.41; passerines 0.16.
- Scope coverage: `analysis/reports/layerB_scope_coverage.md`
  - ~89% of microbat and ~90% of passerine records fall inside PA or within 10 km buffers.
- Exposure QC: `analysis/reports/layerB_exposure_qc.md` (+ JSON)
  - Zero-mass is high inside PAs (microbats ~0.89; passerines ~0.84), lower within 10 km buffers.
- Decisions recorded:
  - DEC-027 (mixed licences; ledger required)
  - DEC-028 (provider-matched NSW BioNet primary analysis)
- Added PI cover letter: `docs/cover_letter_pi_gate_0_6_wp0_15b.md`
- Prepared PI review ZIP: `analysis/pi_review_wp0_15b_20260104.zip` (excludes files >10 MB and large raw/processed caches).
- Note: `artefacts/wp0_15b_layerB_qc/MANIFEST.json` still reports dirty tree; canonical clean-manifest rerun pending commit.
- Added `--allow-dirty` enforcement to Layer B artefact generation scripts to prevent accidental dirty manifests.
- Added `--artefact-only` flags to WP0.15 and WP0.15b scripts to enable clean-manifest rebuilds without reprocessing.
- Built sdist + wheel via `uv run python -m build`.
- PI review (2026-01-05): WP0.15b accepted; GO for WP0.16 under provider‑matched primary (dr368) with multi‑provider sensitivity only.
- Regenerated WP0.15 + WP0.15b artefacts on clean HEAD (`dirty=false`, commit matches).
- Updated PI review ZIP (post‑GO edits): `analysis/pi_review_wp0_15b_20260105.zip`.

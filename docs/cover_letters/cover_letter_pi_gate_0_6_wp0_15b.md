# PI Cover Letter — Gate 0.6 (WP0.15b Layer B QC hardening)

Date: 2026-01-04

## Purpose
This note orients the WP0.15b review. It summarises the licensing ledger, expanded QC, scope coverage, and exposure diagnostics required before WP0.16.

## What changed since the WP0.15 gate
- Built an ALA licence/provenance ledger from `citation.csv` and joined it to processed record counts.
- Expanded QC beyond year/state to include coordinate sanity, uncertainty quantiles, provider concentration, spatial clustering, and dedup loss.
- Quantified scope coverage (inside PA / within 10 km / outside).
- Attached ALAN exposure at occurrence locations and reported missingness + zero‑mass + quantiles by scope.
- Updated the go/no‑go document to reflect mixed licences and provider‑matched controls.

## Key artefacts to review
- `analysis/reports/layerB_ala_license_ledger.md`
- `data/processed/layerB_ala_license_ledger_v0_3_0.csv`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_exposure_qc.json` (machine‑readable)
- `analysis/reports/layerB_gonogo.md` / `docs/layerB_gonogo.json`
- `artefacts/wp0_15b_layerB_qc/`

## Summary highlights (from QC)
- Microbats are highly provider‑skewed: NSW BioNet (dr368) ≈ 88.8% of processed records.
- Dedup loss fraction: microbats ≈ 0.41; passerines ≈ 0.16.
- Scope coverage: ~89% of microbats and ~90% of passerines are inside PAs or within 10 km buffers.
- ALAN exposure zero‑mass remains high inside PAs (microbats ≈ 0.89; passerines ≈ 0.84), lower within 10 km buffers.

## Decisions logged
- DEC‑027: ALA downloads are mixed‑licence; no blanket CC‑BY claim.
- DEC‑028: Primary analysis will be provider‑matched (NSW BioNet) with full‑dataset sensitivity.

## Validation done
- Tests: `uv run pytest tests/python/test_layerB_filters.py tests/python/test_layerB_summary.py`

## Packaging note
- Review ZIP excludes files >10 MB to respect bandwidth constraints.
- Canonical manifest rerun with `dirty=false` is pending a clean commit (see WP0.15b acceptance).

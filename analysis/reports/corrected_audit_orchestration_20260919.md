# Corrected audit orchestration plumbing (19 September 2026)

The four bounded manuscript audits now accept an explicit `--input-manifest`.
The manifest must contain an `analysis_id` and a `files` mapping with exact
`sha256` and `bytes` values for every required input.  Inputs are resolved
under `--data-dir`, hashed before reading, and rejected on missing files,
size mismatches, or digest mismatches.  Every JSON audit summary records the
manifest path, digest, and `analysis_id`.

Legacy invocations retain the Goal 012 defaults and historical cohort/sign
checks.  Explicit manifest mode keeps structural invariants (unique PA-year
rows, 2013--2024 years, minimum pixel/year support, and unique primary PA
rows) but derives cohort sizes, sign counts, area summaries, and coauthor
categories from the supplied data.  The edge follow-up keeps the historical
`matched_1205` import alias while using a cohort-size-independent implementation.

`analysis/run_manuscript_audits.py` is the single entry point:

```text
python analysis/run_manuscript_audits.py \
  --data-dir DATA_DIR \
  --input-manifest INPUT_MANIFEST.json \
  --output-dir OUTPUT_DIR \
  --existing-product-audit VALIDATED_PRODUCT_AUDIT_DIR
```

Use `--raw-dir RAW_RASTER_DIR` instead when raster diagnostics are authorised;
the product audit then requires the raster files and their manifest entries.
When `--existing-product-audit` is used, its
`product_baseline_distances.csv` is also validated against the manifest.
No corrected national rerun was launched in this plumbing tranche.

Verification performed on 19 September 2026:

- Python bytecode compilation passed for the shared contract, four audits,
  and orchestration CLI.
- Focused legacy unit tests passed: 12 tests in the four audit test modules.
- Full corrected-data execution remains pending the parent’s corrected spatial
  outputs and manifest.

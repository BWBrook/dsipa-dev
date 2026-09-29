# Corrected spatial analysis: private reproduction route

This route produces the 19 September 2026 corrected candidate. The existing
Goal 012 runner and `settings/layerA_reference_contract_v0_3_0.json` identify the
historical baseline; its surrounding and inward-band results are superseded.
Do not overwrite that baseline or previous reading bundles.

## Inputs and environment

Use Python 3.12 with the repository `uv.lock` (`uv sync --extra dev`). The executed
remote environment is recorded separately in the candidate runtime manifest.
Run raster extraction on a compute server in a persistent tmux session.

Download all nine processed files from Zenodo dataset 21524637 into one source
directory. Their expected SHA-256 identities are in the historical reference
contract. Obtain the twelve 2013–2024 rasters from night-lights record 17294744;
the contract contains their upstream MD5 values. The coastline acquisition
script records the AIMS Coast50K2024 v1-1 archive URL, checksum and licence.
Natural Earth's pinned `ne_110m_land.zip` is required only to reproduce the
historical-mask sensitivity, not to define the corrected primary comparison.

Prepare a new baseline, with paths supplied explicitly:

```bash
uv run python analysis/prepare_public_spatial_baseline.py \
  --public-dir /path/to/zenodo21524637 \
  --raster-dir /path/to/nightlights_zenodo_v0_4 \
  --natural-earth-dir /path/to/ne_110m_land \
  --output-dir /path/to/new-public-baseline
```

This validates every public processed file and all twelve raster identities,
copies the processed inputs, links the immutable large source trees, rebuilds
the historical land union and verifies its exact hash. `--copy-large-inputs`
makes the baseline self-contained. The source directories remain unchanged.

Acquire and screen national coverage with `analysis/acquire_corrected_coastline.py`
(`--run-dir` and `--pa-gpkg`). Separately run
`analysis/screen_aims_coastline_exceptions.py` (`--pa-gpkg` and `--output`)
for proximity to known source errors. Their `--help` documents these paths. The private evidence packet retains the resulting national
coverage screen and all source hashes. Six zero-overlap identifiers are excluded
only from land-dependent comparisons; fourteen Antarctic records fall outside
the raster footprint. Neither condition is encoded as observed zero radiance.

## Extraction and dependent analyses

Use a new output directory outside the baseline:

```bash
uv run python analysis/run_spatial_correction.py \
  --baseline /path/to/new-public-baseline \
  --coastline /path/to/AU_NESP-MaC-3-17_AIMS_Aus-Coastline-50k_2024_V1-1_split.shp \
  --coverage-screen /path/to/national_pa_land_coverage_screen.csv \
  --out /path/to/corrected-run --workers 20 --chunk-size 12
uv run python analysis/synthesise_spatial_correction.py \
  --baseline /path/to/new-public-baseline --run /path/to/corrected-run
```

The extraction records exact code/input hashes, checks resumed chunks and
propagates raster failures. Its completion manifest verifies keyed equality of
all retained whole-reserve annual fields. Synthesis compares the historical,
geometry-only and corrected-land variants, recomputes surrounding categories,
checks inside trends, and generates an explicit corrected input manifest.
The failed first national attempt is not an input to this candidate.

Run `analysis/run_manuscript_audits.py` with `--data-dir`, `--input-manifest` and
`--output-dir`. Product continuity accepts either `--raw-dir` (fresh raster
diagnostics) or `--existing-product-audit` (validated 2013-distance evidence).
Every reused file must be listed with SHA-256 and byte count in the manifest.
For raw mode, include the twelve raster identities. Reusing the fixed inside
2013 distances is justified by unchanged reserve geometry and raster inputs;
the corrected surrounding annual hazards are always recomputed.

Run `analysis/compare_spatial_interior_correction.py` with explicit `--baseline`,
`--corrected` and `--output` paths to produce the old–corrected band comparison.
Run `analysis/export_reserve_screening.py --root /path/to/candidate` after placing
the known-exception screen at `analysis/reports/spatial_known_coastline_exceptions.csv`.
The reserve-level export retains provisional flags; this step is required for
the candidate tables.

The audit produces `coauthor_evidence`, `product_continuity`, `interior_area` and
`edge_followup` directories. For the manuscript layout, copy the first two into
`analysis/reports/`, the third into `analysis/reports/interior_area_audit/`, and
the fourth into `analysis/reports/edge_followup/`. Include the generated example
series and spatial correction summary in the rendering input manifest.

```bash
uv run python analysis/render_coauthor_figures.py \
  --data-root /path/to/corrected-run --output-root /path/to/candidate \
  --input-manifest /path/to/render-input-manifest.json \
  --spatial-correction --omit-layer-b
uv run python analysis/render_product_audit.py --root /path/to/candidate
uv run python analysis/build_coauthor_tables.py --root /path/to/candidate \
  --spatial-correction --omit-layer-b
```

The candidate root must contain the corresponding reports and manuscript
source directories. Figure/table construction reads corrected cohorts; it does
not reinstate historical denominators. Main prose and captions are reviewed
against these receipts. Numerical Layer B is deliberately absent from the active
candidate; its historical code, reports and prior bundles are retained.

Build PDF and editable Word documents through `$HOME/work/makedoc`:

```bash
make ms-check PROFILE=submission
make ms-build PROFILE=submission
make ms-check PROFILE=supplementary
make ms-build PROFILE=supplementary
```

## Scope of verification

Complete keyed comparison established equality of all accepted/public annual
and interior-band input values and geometry attributes; loaded per-reserve WKB
also matched exactly. An independent eight-reserve run from the published
baseline checks the corrected annual results, including coastal examples and
Wilinggin's polygon-collection case. This is a targeted reproduction check,
not a second national extraction. National results have their own immutable
input/output receipts and separately checked cohort comparisons.

This is a private candidate. The public dataset still contains the earlier
baseline. Publishing corrected data, software or a submission requires Barry's
separate authorisation.

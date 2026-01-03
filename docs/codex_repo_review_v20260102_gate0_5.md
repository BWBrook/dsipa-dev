# Codex External Repository Review — Gate 0.5 (DSIPA‑NBS)

**Reviewer role:** skeptical external auditor (methods + engineering).  
**Repo:** `/home/bwbrook/git/dsipa-dev`  
**Audit date:** 2026‑01‑02  
**Repo commit (at audit):** `37801e8be70e9ea0079b571943f0d3a66fd7dc19` (working tree clean at audit time)

This review is evidence-driven and assumes nothing is correct until checked. I did **not** refactor, “clean up”, or change analysis logic; I only inspected code, tables, reports, and figures, and ran targeted reproducibility checks.

> Important context: The repository content reflects **Milestone 0.5.1 corrections** (mean-trend pivot + risk/retention outputs). Some Gate 0.5 paths mentioned in `docs/cover_letter_pi_gate_0_5.md` and in this audit prompt are now **superseded** or live only under `artefacts/`.

---

## Executive summary (max 12 lines)

- **Readiness for Layer B:** **NO‑GO (for now)** — Layer A floor/selection + buffer validity issues would contaminate Layer B.
- **Critical #1:** Severe floor/zero inflation → many metrics effectively dead; trends/risk apply to **4426/11133 (39.8%)** PAs.
- **Critical #2:** Penetration rings usable for only **369/11133 (3.3%)** PAs; aggregate edge profile is ~0 (weak encroachment evidence).
- **Critical #3:** Buffers/rings ignore ocean + other‑PA overlap → “outside” often not a development proxy; retention indices can be biased.
- **Critical #4:** Run manifests are incomplete (no data checksums/most deps) and many artefacts were built from `git.dirty: true`.
- **Critical #5:** Smoke-tests are brittle/broken in-place (hardcoded `v0_1_0` triad paths in smoketest modules).
- **Strength #1:** Strong roadmap/decision/log discipline (traceable work packages and choices).
- **Strength #2:** Data inventory is unusually thorough; processed outputs have sha256 checksums.
- **Strength #3:** Scale metadata discontinuity (2022–2024 scale=10) was detected, handled, and reported.
- **Strength #4:** Schema discipline exists (explicit `schema_version`, schema reference doc, schema-based tests).
- **Strength #5:** Tests are fast and the package builds cleanly (sdist+wheel).

---

## Reproducibility checks performed

### Commands run (with outcomes)

- `uv run pytest` → **PASS** (21 tests) in **~2.3 s** (real).  
- `uv run python -m build` → **PASS** (sdist + wheel) in **~11.2 s** (real).  

Smoke-tests requested by the audit prompt:
- `uv run python -m dsipa.radiance_smoketest --skip-artefact` → **FAIL** (looks for `data/processed/smoke_test_triad_geoms_v0_1_0.gpkg`, which does not exist).  
  - Root cause: `src/python/dsipa/radiance_smoketest.py:25-26` hardcode `v0_1_0` triad filenames.  
- `uv run python -m dsipa.ring_profiles_smoketest --skip-artefact` → **FAIL** for the same reason (`src/python/dsipa/ring_profiles_smoketest.py:25`).  

To still evaluate scientific/engineering behaviour without editing repo files, I executed the smoke-tests in an isolated temp root via `DSIPA_REPO_ROOT`, using symlinks so the `v0_1_0` paths resolved:
- `env DSIPA_REPO_ROOT=/tmp/dsipa_audit_smoke_cz6SYm uv run python -m dsipa.radiance_smoketest --skip-artefact` → **PASS** in **~2.2 s**.  
- `env DSIPA_REPO_ROOT=/tmp/dsipa_audit_smoke_cz6SYm uv run python -m dsipa.ring_profiles_smoketest --skip-artefact` → **PASS** in **~3.1 s**.  

Minimal “light” end-to-end regeneration from intermediates (as required):
- `env DSIPA_REPO_ROOT=/tmp/dsipa_audit_trends_XZHNKx uv run python -m dsipa.trends --skip-artefact` → **PASS** in **~14.8 s**.  
  - Inputs: symlinked `data/processed/pa_radiance_buffers_national_v0_2_0.csv`  
  - Outputs: regenerated `data/processed/pa_trends_v0_2_0.csv`, `analysis/reports/trends_methods_and_sanity.md`, `analysis/reports/trends_yearly_means.png`, and `manuscript/figures/fig_layerA_trend_distribution.png` inside the temp root.

Additional “light” regeneration (useful corroboration):
- `env DSIPA_REPO_ROOT=/tmp/dsipa_audit_figures_wTNYx2 uv run python -m dsipa.figures_layerA --skip-artefact` → **PASS** in **~12.2 s**.  
  - Inputs: symlinked `data/processed/pa_radiance_buffers_national_v0_2_0.csv`, `data/processed/pa_edge_profiles_national_v0_2_0.csv`, `data/processed/pa_geometries_v0_2_0.gpkg`  
  - Outputs: regenerated `manuscript/figures/fig_layerA_baseline_map.png` and `manuscript/figures/fig_layerA_edge_profiles_aggregate.png` inside the temp root.

### Notes / reproducibility friction observed

- `uv` repeatedly prints: `VIRTUAL_ENV=... does not match the project environment path .venv`. This is cosmetic but will annoy reviewers/users running this in varied shells.  
- Canonical artefact `MANIFEST.json` files often report `git.dirty: true` (e.g., `artefacts/wp0_11b_trends_mean/MANIFEST.json`, `artefacts/wp0_13b_layerA_figures/MANIFEST.json`). If these are supposed to support a PI/journal audit trail, you should aim to generate “paper figures” only from a **clean** commit and record the commit hash.

---

## Data provenance audit

### What is good

- Night-lights source is **DOI-pinned**: `10.5281/zenodo.17294744` (see `data/README.md` + `analysis/reports/data_inventory.md`).  
- Year range is explicit and consistent in code: `2013–2024` (`src/python/dsipa/nightlights.py:31` `CORE_YEARS`).  
- Checksums exist for every downloaded nightlights raster **year** (MD5) and for key derived tables (sha256) in `data/README.md`. I spot-verified:  
  - 2013 and 2024 GeoTIFF MD5 match `EXPECTED_MD5` in `src/python/dsipa/nightlights.py`.  
  - sha256 of `data/processed/pa_trends_v0_2_0.csv` and `data/processed/pa_radiance_buffers_national_v0_2_0.csv` match `data/README.md`.
- CAPAD inclusion rule (terrestrial only) is explicit in code: `NRS_PA='Y'` (`src/python/dsipa/pa_geometry.py:28`) and in decisions (`DEC-002`).

### Provenance gaps that would annoy a journal reviewer

1. **Checksum algorithm ambiguity in `data/README.md`:** the column header says “Checksum (e.g., sha256)” but the nightlights entries are clearly **MD5** (32 hex characters). That’s not a nit: provenance tables must state algorithm unambiguously.  
   - Code uses MD5 intentionally (`src/python/dsipa/nightlights.py:43+`). That’s fine, but document it as **MD5** or migrate to sha256 consistently.

2. **CAPAD “raw” is not frozen.** `data/README.md` points to an ArcGIS REST service with “N/A (service)” checksum. If the service changes, you cannot reproduce geometries.  
   - You do have `data/processed/pa_geometries_v0_2_0.gpkg` and a QC report, but that is not the same as freezing the raw input.  
   - Minimal defensible step for publication: record the ArcGIS REST service metadata (service `currentVersion`, layer `editingInfo`/`lastEditDate` if available, full query parameters) and export the retrieved features (or their hashes) to a raw snapshot.

3. **License hygiene for Zenodo v0.4 dataset:** the repo states CC BY 4.0; ensure the manuscript methods explicitly cite the dataset and satisfies attribution requirements (this is not present yet in manuscript skeleton because WP0.17 is not done).

### Data integrity checks (quick)

- GeoTIFF metadata discontinuity: `scale_metadata` is **1.0** for 2013–2021 and **10.0** for 2022–2024 (verified via rasterio). This is captured in `analysis/reports/national_layerA_coverage_and_sanity.md` and in the output tables (`scale_metadata` column).
- Derived tables in `data/processed/` match schema version `0.2.0` and tests assert the column sets.

---

## Scientific validity audit (Layer A)

### Metric engine (inside/buffers/rings): logic & failure modes

**Core code paths:**
- CAPAD geometry processing: `src/python/dsipa/pa_geometry.py` (`process_capad`, around `:43+`).  
- National metrics: `src/python/dsipa/layerA_national.py`  
  - Zonal stats: `_stats_for_geom` (`:65+`)  
  - Buffers: `build_buffers` (`:264+`)  
  - Rings: `build_rings` (`:283+`)

#### CRS & distance handling

- You compute buffers/rings in **EPSG:3577** (Australian Albers; decision `DEC-004`), then reproject to the raster CRS (EPSG:4326) for extraction.  
  - For distance-based operations, a projected CRS with meters is necessary; **but EPSG:3577 is equal-area, not equidistant**. For 1–10 km rings this may be acceptable, but it is an **assumption** and should be justified quantitatively (max distance distortion across Australia) or replaced with a distance-appropriate CRS strategy.

#### Pixel weighting / geographic grid bias

- Extraction is done against rasters in EPSG:4326 (geographic). Metrics are computed as unweighted mean/median across selected pixels.  
  - Because pixel area varies with latitude in geographic coordinates, the mean is not strictly an area-weighted average. This introduces a **systematic latitudinal bias** for any metric interpreted “per unit area”.
  - If you want “mean radiance over the polygon area”, you should either reproject the raster to an equal-area grid or area-weight pixels. If you want “mean of pixel values”, then you must state that explicitly (and accept the bias).

#### Missingness handling

- National metrics treat `valid_pixel_count < min_valid_pixels` as **missing** (NaN means/medians), not as zero (`src/python/dsipa/layerA_national.py:_stats_for_geom`). This is the correct direction: it prevents silently converting “no data / too few pixels” into “dark”.  
- However, the consequences are enormous and must be front-and-center:
  - **Only 39.8% (4426/11133) of PAs** meet `min_valid_pixels=10` *for inside zones* (and because the mask is constant across years, this selection is effectively all-or-nothing across 2013–2024).
  - Buffers have ~99.9% validity at the same threshold (because they are larger).
  - Rings: only **3.3% (369/11133)** of PAs have valid pixels in the 5–10 km ring.

This is not a minor caveat: it means most analyses are about “larger PAs (or those with geometry that overlaps enough pixels)”, not “Australian protected areas” as a whole. Any paper claims must reflect that.

#### Buffer contamination (conceptual validity)

This is the biggest *conceptual* failure mode in Layer A right now:

- Outside buffers are computed as `buffer(PA) - PA` for each PA independently (`build_buffers`). They are **not** controlled for:
  - ocean/water fraction (coastal PAs),
  - overlap with other protected areas,
  - adjacency of multi-PA complexes (buffer zone still “protected” land),
  - other confounders like large uninhabited regions adjacent to PAs.

Therefore, “outside buffer” is often **not a proxy for development pressure**. This can flip or dilute inside-vs-outside contrasts and directly contaminates:
- inside-vs-outside sanity statements,
- retention indices (inside slope minus buffer slope),
- risk rankings that use retention indices.

If the paper intends to interpret buffers as “encroachment pressure”, you need at minimum a sensitivity analysis controlling for (i) ocean mask and (ii) “outside but also inside any protected area” mask.

---

### Trends: scaling, quantization risks, robustness

**Core code path:** `src/python/dsipa/trends.py` (`_theil_sen` at `:28`, `_compute_trends` at `:45`).

#### Scale/offset handling across years

- Scale metadata differs by year: 2022–2024 have `scale_metadata=10.0`, earlier years `1.0`.  
- Extraction code multiplies raw pixel values by `scale_metadata` before computing mean/median (e.g., `src/python/dsipa/layerA_national.py:_apply_scale` and smoketests).  
- This is plausibly correct (the yearly mean series does not show an artificial step at 2022), **but** note:
  - Raster band tags are empty (`tags n 0`); the only evidence is GDAL’s `scales` property.
  - A journal reviewer will want a short justification showing the data provider’s documentation supports this scale interpretation.

#### Quantization / “dead metric” risk (high priority)

This repo is dominated by exact zeros at multiple stages. Quantitatively (computed directly from `data/processed/*v0_2_0.csv`):

- Total dissolved terrestrial PAs: **11133** (`data/processed/pa_geometries_v0_2_0.csv`).
- Inside-zone validity (>=10 pixels) is **4426 PAs** (39.8%) in every year 2013–2024.
- Among those 4426 PAs (complete-case, 12 years each):
  - **96.5%** have **inside median == 0 for all years**.  
  - **85.5%** have **inside mean == 0 for all years**.  
  - **89.7%** have **inside mean slope == 0** (Theil–Sen).  
  - **98.7%** have **inside median slope == 0** (Theil–Sen).

Interpretation: for most PAs even in the “valid pixels” subset, you are at the floor of this nightlights product; mean and median trends cannot detect change because the underlying per-pixel values are exactly zero in every year.

This is not only a statistical issue; it is a *remote sensing measurement limitation* (left-censoring / floor effect). Proceeding to Layer B using these metrics as exposure variables would produce a high risk of:
- spurious “no effect” results (because exposure is constant zero), or
- confounding where only urban-adjacent PAs carry signal and everything else is indistinguishable.

**Minimal fix (recommendation, not implementation):**
- Introduce at least one non-floor-sensitive exposure metric alongside mean/median, e.g.:
  - fraction of pixels above a small threshold (e.g., >0, >1, >5; calibrated),
  - a high quantile (p90/p95) inside and in buffers,
  - or total radiance sum (with area normalization).
- Treat zeros as censored in trend modelling or explicitly restrict trend claims to the non-zero subset with transparent counts.

#### Robustness / uncertainty

- Trend estimation produces point estimates only. No uncertainty intervals, no bootstrap, no sensitivity to year subset.  
- Outliers are large (e.g., inside slope min ≈ ‑8.4 and buffer slope min ≈ ‑29.5 in `analysis/reports/trends_methods_and_sanity.md`). Without uncertainty and diagnostics, these are impossible to interpret as real-world change vs artefact.

---

### Results narrative: what the current figures genuinely support

What the current artefacts support **with high confidence**:
- A subset of Australian terrestrial protected areas (especially large ones near major cities) have non-zero VIIRS-derived annual average nightlights; many remote/large areas are at (or near) the product floor (0).  
- The 2022–2024 scale metadata discontinuity is real and is being applied; the national mean series does not show an obvious artificial step.

What the current artefacts support **only weakly / conditionally**:
- “Encroachment / edge effects” as a national generalization. The penetration profile analysis is currently dominated by censoring and selection (n=369). The aggregate curve is basically 0, and the single example PA shown does not exemplify the claimed mechanism.
- “Trends in protected areas” for Australia broadly. Trends are computed for 4426/11133 PAs (39.8%) and are overwhelmingly exactly zero even there. Trend claims must be framed as “detectable change above the product floor in the subset of PAs with sufficient pixel support”.

What is **not defensible yet** as a paper-claim:
- Any ranking or “top risk PAs” story without uncertainty and without addressing buffer validity (ocean/protected overlap) and outlier artefacts.

---

## Artefact-by-artefact critique

For each artefact: **What it shows** (what it actually shows), **Red flags**, **Fixes** (recommendations).

### Figure: `manuscript/figures/fig_layerA_baseline_map.png`

**What it shows**
- A national choropleth of **inside‑PA mean radiance in 2024**, with missing PAs colored grey.
- Colormap uses `magma` with `vmin=0` and `vmax` clipped to the 99th percentile.

**Red flags**
- “Missing” here is primarily “<10 valid pixels”, not “no raster coverage”. Without stating that, grey can be misread as a data gap rather than a design choice.  
- Visual separation between *true zero* (black) and *near zero* is weak, and the map is dominated by floor effects.  
- No indication of sample size or selection: this map implicitly suggests nationwide coverage, but only ~40% of PAs meet the inside threshold (and many plotted non-missing values are exactly 0).

**Fixes**
- Add a caption line that explicitly states: “Grey = fewer than 10 valid pixels inside the PA at 500 m resolution; not a missing-tile artefact.”  
- Consider adding an inset histogram or annotation: fraction of PAs at exactly 0, fraction missing, and the pixel threshold used.  
- Consider a diverging/stepped colormap that separates 0 from >0 (e.g., binary “zero vs non-zero” overlay), or show log1p scale for non-zero values (with an explicit “zero mass” label).

---

### Figure: `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`

**What it shows**
- Left panel: “Aggregate profile (n=369)” — median and IQR of **mean radiance** across PAs with complete ring coverage in 2024.  
- Right panel: one “Example PA” time series across ring midpoints (0.5, 3, 7.5 km) for 2013/2018/2024.

**Red flags**
- **Selection bias is extreme:** n=369 is **3.3%** of all PAs, heavily biased toward large PAs (small PAs cannot have 5–10 km interior rings).  
- The aggregate median profile appears effectively **0 at all distances** (driven by zero inflation), which does **not** strongly support an encroachment narrative as presented.  
- The example PA shown (selected as largest with complete rings) has radiance increasing inward, which is **counter to the expected “edge brighter” story**. That might be real for that PA, but it is a poor exemplar if your narrative is encroachment from outside.
- The figure does not show how many of the n=369 have non-zero values; the IQR band can hide that most values are identical zeros.

**Fixes**
- Report (on-plot) the fraction of ring rows with mean==0 in the n=369 subset.  
- Choose example PA(s) using an explicit, defensible rule aligned to the hypothesis, e.g., high (ring0 − ring2) or high buffer–inside contrast, *not* largest area.  
- Consider plotting conditional on non-zero (e.g., show median among PAs with any ring>0) alongside the unconditional profile, with sample sizes.  
- Consider revising ring definitions (adaptive bins by PA size) so that “penetration” is not restricted to 3% of PAs.

---

### Figure: `manuscript/figures/fig_layerA_trend_distribution.png`

**What it shows**
- Two histograms of inside slopes (Theil–Sen on mean radiance): (i) all inside slopes, (ii) non-zero inside slopes only.

**Red flags**
- The second panel conditions on non-zero slopes but does not annotate that **~89.7%** are exactly zero; readers may overinterpret the non-zero distribution.  
- Histogram ranges are set by extreme outliers, compressing the bulk near zero.
- Slopes are shown without uncertainty. Given the floor effects, a lot of “non-zero” slopes could be driven by a few bright pixels or preprocessing changes rather than real encroachment.

**Fixes**
- Put the zero-mass fraction directly into the title/annotation (e.g., “Non-zero subset: n=457 / 4426”).  
- Add a zoomed inset around 0, or use log-count y-axis, so the near-zero structure is visible.  
- Add a robustness panel: e.g., compare slopes from mean vs p95 vs lit-pixel fraction, or show slope vs baseline radiance (to demonstrate censoring).

---

### Figure: `manuscript/figures/fig_layerA_retention_quadrant.png`

**What it shows**
- Scatter of buffer 1 km slope vs inside slope (mean radiance), with quadrants defined by 0 lines.

**Red flags**
- Axes are dominated by extreme outliers (buffer slope as low as ~‑30), compressing the main cloud near (0,0).  
- Without density contours or a clipped view, this is visually “mostly a blob”, and the viewer cannot see structure for the majority.  
- The plot does not state the selection: it is **n=4426** PAs (complete-case inside pixels), not all 11133.

**Fixes**
- Add density contours or hexbin, and optionally a clipped panel (e.g., x∈[‑2,2], y∈[‑2,2]) plus a separate outlier panel.  
- Add on-plot counts per quadrant and the fraction of exact zeros.  
- Consider using retention index directly (inside−buffer) vs inside slope (more interpretable) or using partial pooling/uncertainty.

---

### Figure (Gate 0.5 legacy): `artefacts/wp0_13_layerA_figures/fig_layerA_edge_profiles_examples.png`

**What it shows**
- Three triad PAs ring profiles for 2013/2018/2024.

**Red flags**
- Two panels effectively have only a single x-point (because rings are missing), making this **debug-quality**, not paper-quality.  
- This figure can mislead by implying a “penetration profile” is generally available, when the ring completeness problem is the dominant reality.

**Fixes**
- Keep this only as an internal QC artefact. If used in a paper, replace with (i) an example with complete rings and non-zero radiance, and (ii) an explicit missingness/coverage panel.

---

### Figure (Gate 0.5 legacy): `artefacts/wp0_12_vulnerability_model/fig_layerA_vulnerability_coefficients.png`

**What it shows**
- Standardized OLS coefficients for predictors of inside brightening (median-based slope at that time).

**Red flags**
- The model has **near-zero explanatory power** (`R2 ~ 0.006`; see report below) and is vulnerable to collinearity (log_area, log_perimeter, compactness are geometrically linked).  
- Without out-of-sample validation and uncertainty, coefficients are not scientifically defensible as “drivers”.

**Fixes**
- Do not use as a main result. If any model is retained, require:
  - explicit response definition robust to floor effects,
  - collinearity diagnostics,
  - out-of-sample validation (spatially blocked CV),
  - and clear interpretation limits.

---

### Report: `analysis/reports/national_layerA_coverage_and_sanity.md`

**What it shows**
- Per-year raster scale/offset metadata.
- Coverage fractions by zone and ring.
- Anchor checks (urban vs remote) and an inside vs buffer summary.

**Red flags**
- “Top city medians” are reported as 0 for multiple cities/years; this statistic is not clearly meaningful as written (it’s a median over *all* PAs assigned to each nearest city, not restricted to an “urban” band).  
- Inside-vs-buffer sanity line reports only the unconditional fraction (`0.153`) which is severely depressed by the mass of zeros; this can mislead into thinking buffers are usually not brighter than inside.

**Fixes**
- Report inside-vs-buffer contrasts conditional on non-zero, e.g.:
  - among pairs where inside>0 or buffer>0, buffer>inside is ~0.91 (computed; see Appendix).  
- Clarify what “missingness” means here (pixel threshold), and separate: (i) coverage due to pixel threshold vs (ii) true raster nodata.

---

### Report: `analysis/reports/layerA_sanity_dashboard.md`

**What it shows**
- Basic invariants, anchor checks, mean-vs-median correlation, pixel threshold sensitivity, ring missingness counts, stratified inside-vs-buffer medians.

**Red flags**
- Stratified tables are dominated by zeros; many strata report exactly 0 for both inside and buffer, which can create a false impression that “most strata are stable” rather than “the metric is censored”.  
- Ring missingness section reports counts of below-threshold rows, but does not translate this into “fraction of PAs with usable penetration metrics”, which is what a reviewer will care about.

**Fixes**
- Add explicit “floor-effect” diagnostics to the dashboard: fraction of inside mean==0 by distance band and by area quartile.  
- Report sample sizes for each stratum and the fraction excluded by pixel threshold.

---

### Report: `analysis/reports/trends_methods_and_sanity.md`

**What it shows**
- Theil–Sen trend summaries for mean and median metrics; fraction of exactly-zero slopes; yearly mean/median series.

**Red flags**
- Trend sample size is **n=4426** (because of inside pixel threshold), but this is not stated as a fraction of all PAs (39.8%).  
- The apparent “no step change at 2022” is reassuring, but it is not a proof that scale metadata was correctly interpreted. (You should cite the data provider’s documentation.)

**Fixes**
- Add a prominent “coverage” header: trends apply to 4426/11133 PAs with ≥10 pixels inside for all years.  
- Add at least one additional trend metric less sensitive to floor effects and compare.

---

### Report (Gate 0.5 legacy): `artefacts/wp0_12_vulnerability_model/vulnerability_model_report.md`

**What it shows**
- OLS model definition and coefficients; `R2` ~0.006–0.007.

**Red flags**
- This is not a defensible scientific result as-is. It is an exploratory regression with negligible explanatory power.

**Fixes**
- Remove from main narrative (already superseded), and if modelling is revived, treat it as a rigorously validated module with uncertainty and bias controls.

---

### Report: `analysis/reports/risk_rankings_and_quadrants.md` and table `data/processed/pa_risk_rankings_v0_2_0.csv`

**What it shows**
- Top 20 rankings by inside slope, by retention index (1 km), and by combined z-score risk score.  
- Quadrant plot is referenced (`manuscript/figures/fig_layerA_retention_quadrant.png`).

**Red flags**
- The combined `risk_score` can rank **strongly negative inside slopes** highly if the buffer slope is even more negative (large positive retention). Example: Murujuga (WA_2803) ranks #3 by risk score with inside slope ‑8.42 but retention +21.07. This is a conceptual mismatch if “risk” is interpreted as “brightening risk”.  
- No uncertainty or diagnostic flags for extreme slopes; rankings can be driven by outliers/artefacts.  
- Again: applies to 4426/11133 PAs; many PAs are excluded entirely.

**Fixes**
- Split outputs into clearly labeled components:
  - “Inside brightening” (requires slope_inside > 0),
  - “Relative retention/encroachment” (retention indices),
  - “Outlier/artefact flags” (extreme slopes, low baseline, etc).  
- Add robust uncertainty (bootstrap or jackknife) and rank stability checks before claiming “top risk PAs”.

---

### Table: `data/processed/pa_geometries_v0_2_0.csv` (+ `data/processed/pa_geometries_v0_2_0.gpkg`)

**What it shows**
- Dissolved CAPAD geometries by `PA_ID` (`pa_id`), with geometry validity flags and basic shape descriptors (area, perimeter, compactness) in EPSG:3577.

**Red flags**
- CAPAD provenance is not frozen (REST service). This processed file is acting as a de facto “frozen dataset” without an explicit raw snapshot.  
- The geometry QC report reports a minimum area on the order of ~5e‑6 km² (a few m²). Such micro-polygons are effectively incompatible with 500 m rasters and dominate missingness; they should be treated explicitly as “below resolution”.

**Fixes**
- Document “below raster resolution” as a formal category and ensure no downstream analysis implicitly treats these as “dark” rather than “unmeasurable”.  
- Add a provenance record for the raw CAPAD extraction that produced this file (query + timestamp + service metadata).

---

### Table: `data/processed/pa_radiance_buffers_national_v0_2_0.csv`

**What it shows**
- Per-PA, per-year inside and buffer (1 km, 5 km) zonal stats (mean/median/min/max/std) plus `valid_pixel_count` and `scale_metadata`.

**Red flags**
- “Coverage” is dominated by the `min_valid_pixels` threshold, not true raster nodata. Many PAs have computed mean==0/median==0 across all years → heavy censoring.  
- Buffers likely include ocean and other protected areas; interpreting buffer stats as “development pressure” is unsafe without controls.

**Fixes**
- Add explicit columns capturing buffer composition (ocean fraction, overlap with other PAs) or provide sensitivity tables with those areas excluded.  
- Add additional exposure metrics less floor-sensitive (lit-pixel fraction, p95).

---

### Table: `data/processed/pa_edge_profiles_national_v0_2_0.csv`

**What it shows**
- Per-PA, per-year, per-ring zonal stats for three inside rings (0–1, 1–5, 5–10 km from boundary).

**Red flags**
- Only 3.3% of PAs have valid pixels in ring 2 at the current settings; penetration metrics are not broadly applicable.  
- For valid rows, mean is still zero ~90% of the time → penetration signal is heavily censored.

**Fixes**
- Redesign rings (adaptive widths) or provide penetration metrics that apply broadly (e.g., only 0–1 km ring + interior “core” defined as farthest X% of distance transform).  
- Report penetration results as conditional on non-zero or above-threshold values, with sample sizes.

---

### Table: `data/processed/pa_trends_v0_2_0.csv`

**What it shows**
- Theil–Sen slopes/intercepts for inside and buffers, for both `metric=mean` and `metric=median`, plus retention indices.

**Red flags**
- All trend rows have `n_years_inside==12` (for the included PAs), meaning `MIN_VALID_YEARS=8` is not functionally selecting “partially observed” PAs; it’s selecting a full-coverage subset defined by pixel threshold.  
- Slope distributions are dominated by exact zeros and a few outliers; uncertainty is absent.

**Fixes**
- Explicitly state that trend analysis applies to the complete-case subset (4426/11133).  
- Add uncertainty and robustness diagnostics; add a non-floor exposure metric.

---

### Table: `data/processed/pa_risk_rankings_v0_2_0.csv`

**What it shows**
- Ranked table with inside slope, buffer slopes, retention indices, and a combined z-score risk score for 4426 PAs.

**Red flags**
- The combined score can rank “dimming inside” as high risk if buffers dim more (large retention). This is conceptually inconsistent with a “brightening risk” label unless you are very explicit.  
- Rankings are highly sensitive to outliers and to buffer validity issues.

**Fixes**
- Provide separate rankings for (i) brightening, (ii) relative retention, and (iii) artefact/outlier flags; do not merge into a single scalar without a defensible decision rule and uncertainty.

---

## Tests and guardrails: do they test the right things?

### What tests actually assert (observed)

The tests under `tests/python/` are mostly **schema/regression existence checks**:
- `test_national_outputs.py`: column sets match schema, row counts are consistent, `valid_fraction` bounds.  
- `test_trends.py`: retention indices equal inside minus buffer slopes (by construction).  
- `test_risk_rankings.py`: ranks are >=1.  
- Smoke-test tests check the **already-written** smoketest CSVs, not that the smoketest code can regenerate them.

These tests are necessary but do not defend against key scientific failure modes.

### Would current tests catch these scientific failures?

- Missingness rendered as zeros in maps → **Probably not**. Tests do not assert that `mean/median` must be NaN when `valid_pixel_count < threshold`.  
- Ring bins empty for most PAs → **Partially** (counts fixed), but there is no guardrail that the “penetration metric is usable” beyond existence.  
- Scale discontinuity across years → **No**. No test asserts 2022–2024 scaling is applied correctly or that yearly means don’t show a step if scaling is misapplied.  
- Degenerate trend metrics (slopes all zero) → **No**. No test asserts that non-zero slope fraction is within a plausible range or that trends apply to a meaningful subset.

### High-value additional tests/sanity checks (3–7) I recommend

1. **Missingness ≠ zero guardrail** (fast, high value):  
   - Assert that in `data/processed/pa_radiance_buffers_national_v0_2_0.csv`, any row with `valid_pixel_count < MIN_VALID_PIXELS` must have `mean` and `median` as NaN (not 0).  
   - Do the same for `pa_edge_profiles_national_v0_2_0.csv`.

2. **Coverage-selection transparency test:**  
   - Assert that trend table `data/processed/pa_trends_v0_2_0.csv` covers a known fraction band of PAs (e.g., 0.2–0.6 of total) and fails loudly if it collapses to ~0 or ~1.  
   - This catches accidental threshold changes or geometry/raster misalignment that would quietly drop everything.

3. **Ring usability guardrail:**  
   - Assert that at least N PAs (e.g., >100) have valid pixels in ring_index=2 in 2024; if it drops near 0, the penetration analysis is broken.

4. **Scale discontinuity sanity check (dataset-level):**  
   - Assert `scale_metadata` mode is 1.0 for 2013–2021 and 10.0 for 2022–2024 (or whatever the dataset truly requires) and that the yearly mean inside series does not show an order-of-magnitude discontinuity at 2022.

5. **Inside-vs-buffer conditional sanity (domain check):**  
   - On pairs where inside>0 OR buffer>0 (within the trend-eligible set), assert `P(buffer>inside)` is high (e.g., >0.7). This defends the encroachment narrative against a silent sign flip due to buffer construction bugs.

6. **Outlier slope flagging:**  
   - Add a test/report that prints the top 10 absolute slopes for inside and buffer and asserts they are finite and not NaN; optionally require a manual-reviewed allowlist if extreme values persist.

---

## Roadmap-impact recommendations

If you want Layer A to be publishable and Layer B to be defensible, the roadmap should explicitly promote and “definition-of-done” enforce these missing steps:

1. **Add a WP specifically for floor-effect / censoring mitigation** (Layer A):  
   - Acceptance criteria: introduce at least one additional exposure metric not dominated by exact zeros; report its coverage and compare its trends to mean/median.

2. **Add a WP for “outside buffer validity”** (Layer A):  
   - Acceptance criteria: quantify and report (a) ocean fraction and (b) protected-area overlap within buffers; provide sensitivity results where buffers exclude these regions.

3. **Upgrade Artefact Review Cycle compliance** (engineering):  
   - Acceptance criteria: every canonical `artefacts/*/MANIFEST.json` includes (i) data source IDs and checksums (or references to `data/README.md` entries), and (ii) a full dependency snapshot (at least: geopandas, rasterio, shapely, numpy, pandas, pyproj, gdal version via rasterio).
   - Require `git.dirty: false` for any artefact intended for manuscript figures/tables.

4. **Fix smoke-test script brittleness** (engineering):  
   - Acceptance criteria: smoketest modules read triad paths from `dsipa.schema` (v0.2.0), not hard-coded strings.

5. **Penetration analysis redesign** (scientific):  
   - Acceptance criteria: edge/penetration figure must state sample size and selection criteria, and must show a non-trivial signal beyond “mostly zeros”.

---

## Minimal next actions (high leverage, ordered)

1. Fix smoketest path brittleness (`src/python/dsipa/radiance_smoketest.py:25-26`, `src/python/dsipa/ring_profiles_smoketest.py:25`) so smoke-tests run on a fresh clone without symlink hacks.  
2. Make the selection explicit everywhere: trend/risk results are for **4426/11133** PAs (≥10 inside pixels) and ring penetration is for **369/11133** PAs (complete rings). Put these counts in figure captions and reports.  
3. Add a floor-effect resistant metric (lit-pixel fraction and/or p95) and re-run the trend/retention analysis; treat mean/median as secondary sensitivity checks.  
4. Add a buffer validity sensitivity analysis: exclude ocean (land mask) and exclude other PAs from buffers (union mask) to test whether encroachment conclusions persist.  
5. Redefine or supplement the risk score so it cannot label “strong dimming inside” as “high risk” unless the narrative is explicitly “relative to buffers.”  
6. Add the missing high-value tests/guardrails (missingness≠0, coverage band, ring usability, scale sanity).  
7. Upgrade run manifests to include data checksums/versions and full dependency versions; require clean git for manuscript artefacts.  
8. Only after the above: reconsider Layer B acquisition, using an exposure variable that is not dominated by zeros and explicitly modelling censoring/selection.

---

## Appendix

### A. Computed summary stats (from `data/processed/*v0_2_0.csv`)

**Counts**
- Total PAs (dissolved terrestrial): **11133** (`pa_geometries_v0_2_0.csv`).  
- Trend-eligible PAs (inside valid pixels ≥10 for all years): **4426** (**39.8%**).  
- Ring complete PAs (rings 0–1, 1–5, 5–10 km valid pixels ≥10 for all years): **369** (**3.31%**).

**Floor effects (inside, among the 4426 trend-eligible PAs)**
- Fraction with inside **median == 0** for all years: **0.965**  
- Fraction with inside **mean == 0** for all years: **0.855**

**Zero slopes (Theil–Sen, among 4426 trend-eligible PAs)**
- `slope_inside == 0` for mean: **0.897**  
- `slope_inside == 0` for median: **0.987**  
- `slope_buffer_1km == 0` for mean: **0.839**  
- `slope_buffer_5km == 0` for mean: **0.686**

**Inside vs buffer sanity (informative conditional version)**
- For buffer=1 km, among pairs where inside>0 OR buffer>0: `P(buffer>inside) ≈ 0.914` (n=8914 pairs).  
- For buffer=5 km, among pairs where inside>0 OR buffer>0: `P(buffer>inside) ≈ 0.932` (n=16638 pairs).  

**Ring rows (2024)**
- Fraction of ring rows with valid pixels ≥10: ring0 **0.397**, ring1 **0.126**, ring2 **0.033**.  
- Among valid ring rows (≥10 pixels) in 2024, fraction with `mean == 0`: **0.897**.

### B. Key file/function pointers (for follow-up)

- Nightlights download + checksum: `src/python/dsipa/nightlights.py:57` (`download_year`), `EXPECTED_MD5` at `:16`.  
- CAPAD inclusion rule: `src/python/dsipa/pa_geometry.py:28` (`CAPAD_WHERE = "NRS_PA='Y'"`), processing at `:43` (`process_capad`).  
- National zonal stats + missingness thresholding: `src/python/dsipa/layerA_national.py:65` (`_stats_for_geom`).  
- Buffer/ring construction: `src/python/dsipa/layerA_national.py:264` (`build_buffers`), `:283` (`build_rings`).  
- Trend computation: `src/python/dsipa/trends.py:28` (`_theil_sen`), `:45` (`_compute_trends`).  
- Risk rankings logic: `src/python/dsipa/vulnerability_model.py:65` (`build_risk_dataset`), `:88` (`build_risk_rankings`).  
- Figure generation: `src/python/dsipa/figures_layerA.py:30` (`plot_baseline_map`), `:91` (`plot_edge_profiles`).  
- Manifest content (currently incomplete for publication): `src/python/dsipa/manifest.py:50` (`build_manifest`).  
- Smoke-test brittleness: `src/python/dsipa/radiance_smoketest.py:25-26`, `src/python/dsipa/ring_profiles_smoketest.py:25` hardcode v0_1_0 paths.

# DSIPA‑NBS repository audit — Gate 0.15 (Layer B acquisition complete)

Date (UTC): **2026-01-04**  
Auditor role: **Independent external auditor (methods + engineering)**  
Repo root: `/home/bwbrook/git/dsipa-dev`  
Git HEAD at time of audit: `eb0262bc68400fc672ad1fc050cc0af2b55cf5ad`  
Working tree at time of audit: **clean** (`git status --porcelain=v1` empty)

This report is intentionally skeptical. I assume nothing is correct until checked; I focus on failure modes, hidden assumptions, and ways results could be misleading.

---

## Executive summary (max 12 lines)

- Overall readiness to start WP0.16 modelling: **NO‑GO**.
- Critical issues (ranked): (1) **ALA licensing/attribution not publication‑ready** (CC BY‑NC + provider conditions present; docs misstate “CC‑BY”). (2) **Negative controls incomplete + not bias‑matched** (Squamata absent; microbats dominated by NSW BioNet). (3) **Layer B QC artefacts too thin** (no coordinate/provider/scope/exposure QC). (4) **“Canonical” artefact manifests non‑canonical** (dirty tree + commit mismatch vs HEAD despite `clean_required=true`). (5) **Layer A edge‑profile figure risks misread** (median `frac_gt0` is 0 across rings; heavy selection).
- Strengths (ranked): (1) Strong roadmap/decisions/log discipline. (2) Layer A denominators reconciled (11,133 PAs) and censoring/selection is surfaced. (3) Buffer‑validity decomposition exists and is used via `buffer_type`. (4) Layer B queries + raw zips are captured with metadata JSON + sha256. (5) Tests are fast and pass.

---

## Reproducibility checks performed

### Repo state recorded

- `git rev-parse HEAD` → `eb0262bc68400fc672ad1fc050cc0af2b55cf5ad`
- `git status --porcelain=v1` → empty output (clean working tree)

### Commands run (pass/fail + runtime notes)

All commands were run from the repo root unless noted.

- Tests:
  - `PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider` → **PASS** (`29 passed in 6.72s`)
- Package build (sdist + wheel):
  - `PYTHONDONTWRITEBYTECODE=1 uv run python -m build --sdist --wheel --outdir /tmp/dsipa_build_20260104T041007Z` → **PASS** (~12s)
  - Note: `python -m build` writes intermediate `build/`/egg-info by default; I removed those afterwards to return the working tree to “unchanged”.
- “Light regeneration” without re-running the national Layer A pipeline (writes redirected via `DSIPA_REPO_ROOT` to keep the working tree unchanged):
  - `DSIPA_REPO_ROOT=/tmp/dsipa_audit_oj9imr uv run python -m dsipa.radiance_smoketest --skip-artefact` → **PASS** (~2.2s); outputs under `/tmp/dsipa_audit_oj9imr/{data/processed,analysis/reports}`
  - `DSIPA_REPO_ROOT=/tmp/dsipa_audit_oj9imr uv run python -m dsipa.layerB_data --skip-download --skip-artefact --groups microbats,diurnal_birds` → **PASS** (~140s); outputs under `/tmp/dsipa_audit_oj9imr/{data/processed/layerB,analysis/reports}`

### Observed brittleness / reproducibility risks

1) `uv` repeatedly prints a warning about `VIRTUAL_ENV` not matching the project `.venv` (example during tests/builds). This is not fatal, but it is a reproducibility “paper cut” that will confuse users and reviewers unless the README explicitly anticipates it.

2) Multiple artefacts in `artefacts/` are stamped as “dirty tree” even when the pipeline asked for clean-tree artefacts (`require_clean=True`), and the recorded commit hashes do not match the current HEAD. Examples:
- `artefacts/wp0_15_layerB_data/MANIFEST.json` (`clean_required=true`, `dirty=true`, commit `5aacead…`)
- `artefacts/wp0_13c_layerA_figures/MANIFEST.json` (`clean_required=true`, `dirty=true`, commit `3a97c92…`)
- `artefacts/wp0_11c_trends_censoring/MANIFEST.json` (`clean_required=true`, `dirty=true`, commit `3a97c92…`)

This is a credibility leak at a gate intended for review. It doesn’t prove the analysis is wrong, but it makes it harder to assert “these artefacts correspond to this code”.

---

## Layer A regression audit (Gate 0.15 must not destabilise Layer A)

### Denominator consistency across Layer A tables

I computed row counts and unique PA IDs for the core national outputs. Results:

- `data/processed/pa_geometries_v0_3_0.csv`: rows **11,133**, unique `pa_id` **11,133**
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`: unique `pa_id` **11,133**
  - inside-zone rows: **133,596** = `11,133 * 12 years` (full cross-product, OK)
  - raw buffer rows: **267,192** = `11,133 * 12 years * 2 distances` (full cross-product, OK)
  - land rows: **250,488**, unique `pa_id` **10,504** (expected < full if land intersection empty)
  - land_unprotected rows: **249,492**, unique `pa_id` **10,483** (expected < full if land_unprotected empty)
- `data/processed/pa_buffer_validity_v0_3_0.csv`: rows **22,266** (2 buffers per PA), unique `pa_id` **11,133**
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`: rows **400,788** = `11,133 * 12 years * 3 rings` (full cross-product, OK)
- `data/processed/pa_trends_v0_3_0.csv`: rows **53,112** = `4,426 * (4 metrics * 3 buffer_types)`; unique `pa_id` **4,426**
  - Interpretation: trend table only exists for PAs with **≥1 inside-year with ≥10 valid pixels**, not for all PAs.
- `data/processed/pa_risk_rankings_v0_3_0.csv`: rows **3,858**; unique `pa_id` **3,858**
  - Interpretation: risk/retention uses the subset with inside + 1 km buffer slopes available (and other covariates non-missing), not the full 4,426.

Bottom line: **Layer A denominators are internally coherent** in the files I inspected, but multiple “n” values are subset-conditional. This must be handled very explicitly in any narrative (captions and methods).

### Buffer validity decomposition: present, but downstream usage is easy to misinterpret

What exists:
- A buffer validity table: `data/processed/pa_buffer_validity_v0_3_0.csv` with `land_fraction`, `protected_overlap_fraction`, `effective_land_area_km2`.
- Multiple buffer geometries in the radiance table (`buffer_type` = `raw`, `land`, `land_unprotected`) and primary analyses that select `land_unprotected` (see `src/python/dsipa/trends.py` and `src/python/dsipa/vulnerability_model.py`).

What can still fail:
- Readers may interpret “buffer trend” as “outside pressure” without noticing that **(a)** many PAs do not have `land_unprotected` buffers with enough pixels for trends, and **(b)** overlap with other protected areas can be substantial in raw buffers.
- In `analysis/reports/national_layerA_coverage_and_sanity.md`, the buffer validity summary reports:
  - `protected_overlap_fraction > 0.25` for **16.2%** of buffers (unclear if this is raw buffers only; likely so).

Empirical check (2024, 1 km, land_unprotected buffers with ≥10 pixels):
- Eligible buffer count: **9,695** PAs.
- Of those, `protected_overlap_fraction > 0.25` for **16.0%**.
- Zero-mass in buffer mean is higher when overlap fraction is high (**0.846** vs **0.790**), suggesting overlap/validity correlates with censoring and likely with “pressure” interpretation.

Recommendation (conceptual, not an implementation request): wherever you interpret “encroachment pressure”, you should (at minimum) report sensitivity to buffer validity thresholds or explicitly condition the analysis on “valid buffers”.

### Censoring/floor awareness: explicit, but results remain floor-dominated

What’s good:
- The project explicitly acknowledges floor/selection, adds censoring-aware metrics (`frac_gt0`, `p95`), and reports “zero mass” in figures and dashboards:
  - `analysis/reports/layerA_sanity_dashboard.md`: inside rows with ≥10 pixels have `mean==0` fraction **0.895**; `p95==0` fraction **0.939**.
  - `manuscript/figures/fig_layerA_baseline_map.png` title reports inside mean “zero-mass=86.9%”.
  - `manuscript/figures/fig_layerA_trend_distribution.png` title reports inside slope “zero mass=89.7%”.

What’s still a scientific risk:
- Even with `frac_gt0`/`p95`, **zero-mass remains huge**; this is not a small technicality — it dominates interpretation.
- Your “anchors” need careful design: in `analysis/reports/national_layerA_coverage_and_sanity.md`, the “Top city medians” are reported as 0 for Adelaide/Brisbane/Canberra in multiple years. That is likely an artefact of how “nearest city” is assigned (many remote PAs will still be “nearest” to some city in the small city list), not a real-world statement about cities. It risks undermining trust if shown to a reviewer.

### Ring/penetration feasibility: correctly caveated, but current figure is vulnerable to misreading

Ring feasibility is correctly surfaced in both text and figures:
- `analysis/reports/layerA_sanity_dashboard.md` and `analysis/reports/national_layerA_coverage_and_sanity.md` show valid ring fractions around:
  - ring 0: **0.397**
  - ring 1: **0.128**
  - ring 2: **0.034**
- `manuscript/figures/fig_layerA_edge_profiles_aggregate.png` explicitly labels `complete=383` out of `n=11133`.

However:
- The “Edge profile (frac_gt0)” panel is a flat line at 0 because the median is 0 at each ring under floor domination. This can be misread as “no edge effect”, when the more honest reading is “metric and selection make the median uninformative here”.

If Layer A is “stable” at Gate 0.15, it is stable in a *censoring-dominated regime*. That’s OK if you own it, but it’s easy to overclaim.

---

## Layer B provenance audit (high priority)

### What Layer B data sources are, and how they were acquired

Layer B occurrences were acquired from the Atlas of Living Australia (ALA) biocache API:
- Search endpoint: `https://biocache.ala.org.au/ws/occurrences/search` (counts)
- Download endpoint: `https://biocache.ala.org.au/ws/occurrences/download` (zip downloads)
- Query definitions are created by `src/python/dsipa/layerB_data.py`:
  - `build_queries(...)` at `src/python/dsipa/layerB_data.py:193`
  - Processing filters at `src/python/dsipa/layerB_data.py:399` (`apply_quality_filters`) and `src/python/dsipa/layerB_data.py:424` (`dedupe_occurrences`).

### Provenance ledger (what exists, what’s missing)

**What’s strong:** each successful download has:
- a raw zip file under `data/raw/ala_occurrences/`,
- a companion `*_metadata.json` with:
  - query parameters (`q` + `fq` list),
  - access timestamp,
  - SHA-256 checksum of the zip.

**What’s missing / problematic for publication:**
- The repo does **not** record a provider-level license ledger for what is inside the zips. The ALA zip includes `citation.csv` with per-provider rights that include CC BY‑NC and additional terms. Treating this as “CC BY” is not defensible.
- The filename references in `data/README.md` appear inconsistent with on-disk filenames for ALA zips (e.g., `ala_occurrences_microbats_...` vs actual `microbats_...`). This is minor but a reproducibility paper cut.
- Artefact manifests for WP0.15 do not list the raw zip file(s) and checksums as explicit inputs; they only say `"Atlas of Living Australia"`.

### Provenance ledger (concise table)

| Dataset | Access mechanism | Access date (UTC) | Query/filter parameters (fq) | Raw outputs | Provenance metadata | Checksums | License/attribution notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Microbats (Chiroptera excluding Pteropodidae) | ALA `occurrences/download` | 2026-01-04 02:06 | `year:[2013 TO 2024]`, `taxonRank:species`, `occurrenceStatus:present`, `coordinateUncertaintyInMeters:[0 TO 1000]`, `country:Australia`, `order:Chiroptera`, `-family:Pteropodidae` | `data/raw/ala_occurrences/microbats_20260104T020628Z.zip` | `data/raw/ala_occurrences/microbats_metadata.json` | sha256 (in metadata): `f0272a…` | `citation.csv` inside zip contains mixed rights (CC BY, CC BY‑NC, provider conditions); cannot label as “CC BY”. |
| Diurnal birds proxy (Passeriformes) | ALA `occurrences/download` | 2026-01-04 02:07 | `year:[2013 TO 2024]`, `taxonRank:species`, `occurrenceStatus:present`, `coordinateUncertaintyInMeters:[0 TO 1000]`, `country:Australia`, `class:Aves`, `order:Passeriformes` | `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip` | `data/raw/ala_occurrences/diurnal_birds_metadata.json` | sha256 (in metadata): `027711…` | `citation.csv` in this zip explicitly includes CC BY‑NC and other provider constraints. |
| Diurnal reptiles proxy (Squamata) | ALA `occurrences/download` | 2026-01-04 01:47 | similar window/uncertainty + `class:Reptilia`, `order:Squamata` | `data/raw/ala_occurrences/diurnal_reptiles_20260104T014742Z.zip` (tiny) | `data/raw/ala_occurrences/diurnal_reptiles_metadata.json` | sha256 (in metadata): `216383…` | Zip appears to be a failure/sentinel (very small `data.csv`); treating HTTP 200 as “success” is unsafe. |

### Licensing / attribution: critical red flag

The Layer B design docs describe ALA data as “CC‑BY”:
- `docs/layerB_gonogo.json` → `"Atlas of Living Australia (ALA) occurrence downloads (CC-BY)"`
- `analysis/reports/layerB_gonogo.md` repeats the same claim.

This is contradicted by evidence inside the actual ALA zips:
- `citation.csv` within `data/raw/ala_occurrences/microbats_20260104T020628Z.zip` includes entries with `Rights` values such as **CC BY‑NC** (and other conditions).
- `citation.csv` within `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip` includes entries with `Rights` values such as **CC BY‑NC** and “conditions of access”.

If you proceed to WP0.16 without resolving this, you risk building a “result” that cannot be legally/ethically published in the intended form (or would require nontrivial downstream filtering/redaction).

---

## Layer B data QC audit (core of WP0.15)

### QC artefacts inspected (directly)

- `analysis/reports/layerB_data_qc.md` (also present in `artefacts/wp0_15_layerB_data/layerB_data_qc.md`)
- `data/processed/layerB_occurrence_summary_v0_3_0.csv`
- Processed occurrence tables:
  - `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
  - `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`

### What the existing QC report covers (and what it doesn’t)

`analysis/reports/layerB_data_qc.md` provides:
- query definitions (fq strings),
- raw → filtered → dedup counts,
- yearly counts and state counts post-dedup.

It does **not** provide (but should, before modelling):
- coordinate sanity/outlier rates (bbox, sign errors, 0/0),
- coordinate uncertainty distribution (quantiles, mass at max threshold),
- provider/dataResource concentration,
- deduplication loss fraction (and its implications),
- proportion of records within the declared spatial scope (inside PAs / within 10 km of PAs),
- any ALAN exposure distribution at occurrence locations (zero-mass/missingness).

### Concrete summary stats (computed directly from processed tables)

Below are **computed** (not just narrative) QC stats; these should be treated as pre-flight checks for WP0.16.

#### Stage counts + loss rates

From `data/processed/layerB_occurrence_summary_v0_3_0.csv`:

- Microbats:
  - raw **108,695** → filtered **107,907** (filter pass rate **99.28%**) → dedup **63,716** (dedup retention **59.05%** of filtered)
  - unique species **59**
- Diurnal birds (Passeriformes):
  - raw **2,845,757** → filtered **2,834,940** (filter pass rate **99.62%**) → dedup **2,378,378** (dedup retention **83.88%** of filtered)
  - unique species **348**

#### Coordinate completeness and uncertainty

Microbats (`data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`, n=63,716):
- Missing lat/lon fraction: **0.0%**
- `coordinateUncertaintyInMeters` quantiles (m): p50 **30**, p90 **100**, p95 **250**, p99 **853.4**, max **1000**
- Fraction with uncertainty ≤100 m: **90.87%**; ≤10 m: **36.69%**
- Out-of-(lon 112–154, lat −44–−10) strict bbox: **12** records (**0.019%**); out-of-loose bbox (110–170, −55–−5): **0**
- `occurrenceID` missing fraction: **6.42%**

Diurnal birds (`data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`, n=2,378,378):
- Missing lat/lon fraction: **0.0%**
- `coordinateUncertaintyInMeters` quantiles (m): p50 **100**, p90 **244**, p95 **500**, p99 **1000**, max **1000**
- Fraction with uncertainty ≤100 m: **73.74%**; ≤10 m: **26.36%**
- Out-of-loose bbox (110–170, −55–−5): **45** records (**0.0019%**)
  - Observed failure modes among these outliers include: Christmas Island points (~105.6E) and sign errors (7 positive latitudes; 1 negative longitude).
- `occurrenceID` missing fraction: **4.91%**

#### Taxonomy dominance

Microbats:
- Most common species: `Chalinolobus gouldii` = **9,080** records (**14.25%**)
- Top 10 species share: **67.60%**
- Species with ≥50 records: **33** (meets the WP0.14 go/no-go criterion “≥15 species with ≥50 records”)

Diurnal birds:
- Most common species: `Gymnorhina tibicen` = **173,243** records (**7.30%**)
- Top 10 species share: **34.30%**

#### Spatial clustering (1 km grid in EPSG:3577)

Microbats:
- Unique 1 km grid cells: **10,028**
- Top 1 cell count: **260** (**0.41%** of all records)
- Top 100 cells share: **18.24%**

Diurnal birds:
- Unique 1 km grid cells: **100,271**
- Top 1 cell count: **18,972** (**0.80%**)
- Top 1,000 cells share: **37.41%**

These numbers matter: a model without spatial blocking will be dominated by hotspots and will overstate confidence.

#### Provider / dataset dominance (`dataResourceUid`)

Microbats:
- Unique `dataResourceUid`: **17**
- Top provider `dr368` (NSW BioNet Atlas): **56,590** (**88.82%**)
- Top 5 providers share: **99.30%**

Diurnal birds:
- Unique `dataResourceUid`: **30**
- Top provider `dr368`: **641,664** (**26.98%**)
- Top 5 providers share: **92.62%**

Microbats are overwhelmingly driven by a single state portal/provider. Any “national” Layer B claim will be hard to defend unless you explicitly stratify/limit inference (e.g., NSW-only analysis, or provider-stratified sensitivity).

#### Geographic (state) imbalance

Microbats state counts (post-dedup) from `analysis/reports/layerB_data_qc.md`:
- New South Wales: **56,766** (**89.09%**)
- South Australia: **3,748** (**5.88%**)
- Victoria: **1,706** (**2.68%**)
- Queensland: **1,040** (**1.63%**)
- Others are tiny (ACT 6; TAS 27; WA 108; NT 310)

Diurnal birds are much more spread (NSW **37.8%**, VIC **32.3%**, ACT **9.9%**, etc.).

This mismatch alone is enough to break naive negative-control logic: differences could be driven by dataset composition rather than ecology.

---

## Layer B modelling readiness (GO/NO‑GO decision for WP0.16)

### Focal taxa definition: plausible, but the realised dataset is not “national”

The focal query is clear and reproducible (Chiroptera excluding Pteropodidae, 2013–2024, uncertainty ≤1 km). The realised dataset, however, is **extremely NSW/provider dominated** (≈89% NSW and ≈89% from `dr368`). That is not automatically disqualifying, but it changes what can be claimed:
- You likely have enough data to model “microbat occurrence signal vs ALAN” in NSW-like sampling regimes.
- You do **not** (yet) have an obvious basis for a national inference without heavy bias modelling and/or explicit stratification.

### Negative controls: currently insufficient to support falsification claims

Planned controls in `docs/layerB_gonogo.json`:
- diurnal birds (Passeriformes): acquired and processed ✅
- diurnal reptiles (Squamata): **not acquired** ❌ (DEC‑026 defers due to ALA failures; the only zip present is a tiny “sentinel”-like file)

Even if reptiles were present, passerines are a weak bias match for microbats:
- microbats are dominated by state survey datasets (BioNet),
- passerines include large citizen-science and mixed-provider streams.

If controls show a similar “ALAN effect”, you will not be able to confidently label it “sampling bias” vs “shared geography/provider composition”.

### Bias-control readiness: not yet demonstrated at this gate

The WP0.14 plan calls for:
- target-group background,
- spatial blocking (50 km blocks),
- explicit falsification checks.

At Gate 0.15, I do not see artefacts showing that:
- a target-group background for the focal class (Mammalia) exists and is reproducible,
- spatial blocking is implemented or at least sanity-checked for feasibility/runtime,
- core diagnostics (e.g., provider stratification, spatial scope coverage) are in place.

### Exposure variable suitability and variability

I performed a spot-check of the **2024** Zenodo nightlights raster sampled at occurrence coordinates (point sampling via rasterio; scale metadata applied where present):

- Microbats (all points):
  - valid samples: **100%**
  - radiance zero-mass: **65.27%**
  - radiance quantiles (scaled): p90 **60**, p95 **120**, p99 **370**, max **1480**
- Diurnal birds (200k sample):
  - valid samples: **100%**
  - radiance zero-mass: **74.85%**
  - radiance quantiles (scaled): p90 **70**, p95 **150**, p99 **470**, max **2320**

However, when splitting microbats by inside-PA vs outside-PA (PA union; not buffer-limited), zero-mass diverges sharply:
- Microbats inside PAs: zero-mass **88.69%**, p95 **30**
- Microbats outside PAs: zero-mass **55.80%**, p95 **170**

This implies:
- a point-level ALAN covariate is at least *somewhat* variable, but still heavily zero-inflated;
- if the modelling uses **inside-PA** covariates only, it may be almost entirely floor-dominated;
- the ALAN covariate choice must be explicitly designed for censoring (e.g., `frac_gt0`, `p95`, or a two-part/hurdle approach) and tied to the modelling spatial scope (inside vs buffer vs outside).

### GO / NO‑GO verdict

**NO‑GO** for WP0.16 as currently constituted.

Exact blockers to clear before starting modelling (in order of severity):
1) **Licensing/attribution**: produce a provider-level license ledger from ALA `citation.csv` and decide an inclusion policy; stop describing ALA as “CC‑BY” unless you actually filter to CC‑BY-compatible subsets.
2) **Negative controls**: either acquire the second negative control (reptiles) or revise the falsification plan and criteria in `docs/layerB_gonogo.json`/`docs/decisions.md` so the analysis remains defensible with one control.
3) **Scope coverage QC**: quantify and report the fraction of focal/control records inside PAs and within 10 km buffers (the declared scope), and show what is dropped when enforcing that scope.
4) **Exposure QC**: report ALAN missingness/zero-mass at occurrence locations *after* applying the actual covariate-attachment strategy intended for WP0.16 (point-sampled vs PA-joined; year-specific vs static).

---

## Artefact-by-artefact critique (concrete inspection)

### `manuscript/figures/fig_layerA_baseline_map.png`

What it shows:
- Left: eligibility mask for inside-PA summaries using `>=10` valid pixels in 2024.
- Right: inside mean radiance for eligible PAs with explicit “zero-mass=86.9%”.

Red flags / misleading risks:
- The label “missing=6707” conflates “ineligible due to <10 pixels” with actual missingness; readers may misinterpret as data gaps rather than a deliberate censoring rule.
- The right panel uses grey for ineligible PAs; without a legend entry, a reader can confuse “ineligible” with “zero”.

Fixes needed (non-implementation guidance):
- Rename “missing” to “ineligible (<10 px)” everywhere (plot title + caption). This is a narrative fix; it materially reduces misinterpretation risk.

### `manuscript/figures/fig_layerA_trend_distribution.png`

What it shows:
- Histogram of inside mean slopes (Theil–Sen), explicitly reporting “zero mass=89.7%, n=4426”, plus a second panel zooming to non-zero slopes.

Red flags:
- The left panel’s x-range includes extreme slopes (±8-ish) which compresses the informative mass near 0. The non-zero panel helps, but only if a reader looks at it.

Fixes needed:
- Ensure captions/Methods explain that slopes are heavily discrete/zero-inflated and that “non-zero panel” is not a cherry-pick but a necessary diagnostic.

### `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`

What it shows:
- Left: ring feasibility (fraction of PAs with valid rings).
- Right: “Edge profile (frac_gt0)” for the subset of PAs with complete rings (n=383).

Red flags:
- The edge profile is a flat line at 0 because the median of `frac_gt0` is 0 in each ring. A reader can easily infer “no edge effect”, which is not warranted given `nonzero rows=10.4%` and the floor-dominated regime.

Fixes needed:
- Caption should explicitly say “median is 0 due to zero inflation; this plot mainly demonstrates feasibility limits, not absence of edge effects.”
- Consider switching the summary statistic in the *paper-facing* figure to something that is not annihilated by zeros (e.g., mean of `frac_gt0`, or conditional on `frac_gt0>0`). If you don’t change the statistic, at least add a diagnostic panel.

### `manuscript/figures/fig_layerA_retention_quadrant.png`

What it shows:
- Hexbin of buffer 1 km vs inside slopes (mean), clipped 1st–99th percentile, with quadrant counts and `n=3858`.

Red flags:
- This is **not** the same denominator as `n=4426` used elsewhere; it implicitly conditions on having a valid land_unprotected buffer slope. That is fine, but must be stated in captions as a *selection*.

Fixes needed:
- Caption must say “restricted to PAs with ≥8 valid years inside and buffer (land_unprotected)”.

### `analysis/reports/national_layerA_coverage_and_sanity.md`

What it shows:
- Raster metadata (including scale changes after 2021), coverage fractions by zone/buffer type, buffer validity summary, ring coverage fractions, and some anchor checks.

Red flags:
- “Top city medians” being 0 for major cities will confuse reviewers unless explained (and I suspect it is an artefact of the nearest-city assignment rather than a real “city brightness” check).
- “Inside vs buffer sanity” reports `buffer>inside` fraction 0.138 overall, which conflicts with the intuitive narrative unless readers understand the floor-dominated regime; the stratified sanity in `analysis/reports/layerA_sanity_dashboard.md` is much more interpretable.

Fixes needed:
- Replace/clarify the “Top city medians” sub-check with an anchor that is actually tied to known bright polygons or to PAs explicitly within some urban radius.

### `analysis/reports/layerB_data_qc.md`

What it shows:
- Query definitions; raw/filtered/dedup counts; year and state counts.

Red flags:
- It does not include the QC items that would convince a skeptical reviewer that Layer B modelling is safe: coordinate outliers, uncertainty distribution, duplicates, provider concentration, and (most importantly) scope coverage (inside/within buffer).

Fixes needed:
- Expand QC report before WP0.16; at minimum include the “Concrete summary stats” items above and a scope-enforcement drop table.

### `data/processed/layerB_occurrence_summary_v0_3_0.csv`

What it shows:
- Minimal summary counts (raw/filtered/dedup/unique_species) for each group.

Red flags:
- Too minimal to act as a regression guard against silent query changes, because it lacks:
  - hash of the raw zip(s) actually processed,
  - filter parameter values (uncertainty threshold, years),
  - or any per-step reason counts (what was filtered out, why).

Fixes needed:
- Treat this as a “header table” only; don’t claim it is a QC report. Ensure the canonical artefact folder includes richer QC outputs.

---

## Roadmap-impact recommendations

The current roadmap jumps from WP0.15 → WP0.16. Based on this audit, I recommend inserting a short “Gate 0.15b” hardening step **or** tightening WP0.16 acceptance criteria.

### Option A: Insert a new WP0.15b (recommended)

**WP0.15b — Layer B licence ledger + scope/exposure QC (hard gate before modelling)**

Acceptance criteria ideas:
1) Parse each ALA zip’s `citation.csv` into a provider-level ledger (UID, DOI, Rights/licence string, record counts) and decide inclusion/exclusion rules (document in `docs/decisions.md`).
2) Add a scope coverage report: fraction of records inside PAs and within 10 km of PAs (focal + controls), plus drop counts when enforcing scope.
3) Add exposure diagnostics: ALAN zero-mass + quantiles at occurrence locations (or after PA-joining), by inside/buffer/outside and by taxon group.
4) Regenerate a canonical artefact folder with a clean working tree and manifest listing exact raw zip checksums used.

### Option B: Tighten WP0.16 definition of done

If you refuse a new WP, then WP0.16 must begin with explicit “data readiness” checks (same items above) and has a stop rule if controls are incomplete or licensing is unresolved.

---

## Minimal next actions (ordered, high-leverage)

1) **Licensing ledger**: parse `citation.csv` inside each ALA zip and write a per-provider licence/DOI/rights summary; decide policy for CC BY‑NC and provider-specific conditions.
2) **Correct the “ALA is CC‑BY” claim** in `docs/layerB_gonogo.json` and `analysis/reports/layerB_gonogo.md` (or implement a CC‑BY-only filter and prove it).
3) **Harden download validation** in `src/python/dsipa/layerB_data.py` so “tiny sentinel zips” are detected and rejected (current risk: HTTP 200 but unusable content; see diurnal reptiles zip size).
4) **Scope enforcement QC**: compute and report `inside_PA`, `within_10km` fractions for focal + controls, and treat “outside scope” as a first-class filter stage with explicit counts.
5) **Provider dominance sensitivity**: run stratified QC for microbats by `dataResourceUid` and by state; decide whether Layer B is national or a NSW case study.
6) **Exposure strategy decision**: decide whether WP0.16 uses point-sampled ALAN (year-specific) or joins to PA/buffer summaries; quantify ALAN missingness/zero-mass under the chosen method.
7) **Negative controls**: retry Squamata once ALA download service is healthy, or choose an alternative control more similar to microbat sampling pathways and record the decision.
8) **Bias-control feasibility evidence**: implement a small feasibility run showing target-group background and spatial blocking do not collapse (runtime + diagnostic plots).
9) **Artefact canonicality**: regenerate WP0.15 and WP0.13c artefacts on a clean HEAD so manifests show `dirty=false` and commit hashes match.
10) **Add guardrail tests** (see below) that fail loudly when Layer B inputs silently drift.

---

## Appendix

### Key code pointers (functions + line numbers)

- Layer B acquisition + processing:
  - `src/python/dsipa/layerB_data.py:193` `build_queries(...)`
  - `src/python/dsipa/layerB_data.py:399` `apply_quality_filters(...)`
  - `src/python/dsipa/layerB_data.py:424` `dedupe_occurrences(...)`
  - `src/python/dsipa/layerB_data.py:450` `process_occurrences(...)`
  - `src/python/dsipa/layerB_data.py:360` `find_latest_zip(...)` (risk: “valid zip” ≠ “valid download”)
- Layer A buffers/rings:
  - `src/python/dsipa/layerA_national.py:365` `build_buffers(...)`
  - `src/python/dsipa/layerA_national.py:502` `build_rings(...)`
  - `src/python/dsipa/layerA_national.py:579` `summarise_buffers(...)`
- Manifest logic:
  - `src/python/dsipa/manifest.py:61` `build_manifest(...)` (note: `require_clean` only warns; it does not enforce)

### High-value additional tests / sanity checks (proposals)

These are deliberately “scientific guardrails”, not just schema checks:

1) **Sentinel zip detection** (Layer B): fail if the chosen “latest zip” has an implausibly small `data.csv` or if processed `raw_records` is below a floor (e.g., <1,000) when the query is expected to return millions. Target: `find_latest_zip(...)` / `process_occurrences(...)`.
2) **Scope coverage regression**: compute and assert the fraction of focal/control records within 10 km of PA union is above a minimum (or at least report it); fail if it suddenly drops, indicating query drift or projection mistakes.
3) **Coordinate sanity bounds**: assert near-100% of records lie within a loose Australia bbox; fail if lon < 0 or lat > 0 exceed a tiny threshold (these are almost always sign errors).
4) **Provider concentration warning**: assert that the QC report records provider dominance (e.g., top `dataResourceUid` share), and fail if it is missing — this is a key bias risk.
5) **ALAN missingness explosion**: after attaching exposure covariates in WP0.16, assert that missingness is <20% and that zero-mass is reported; fail if covariates are mostly missing/zero without being flagged.
6) **Negative-control presence check**: fail WP0.16 if controls declared in `docs/layerB_gonogo.json` are not actually present as processed tables (or update the config/decision accordingly).
7) **Censoring-aware metric invariants** (Layer A ↔ Layer B): if you use `frac_gt0` or `p95`, assert they are within [0,1] and ≥0 and that “median==0” regimes are explicitly reported in artefacts.

### Computed stats note

All computed QC and exposure stats in this report were produced by direct reads of the processed tables and raster sampling of the 2024 nightlights GeoTIFF in `data/raw/nightlights_zenodo_v0_4/`. They are not inferred from narrative summaries.


# Dark-Sky Integrity of Protected Areas & Nocturnal Biodiversity Signals (Australia)

## Abstract (draft)

[TO DO] One-paragraph summary of objectives, methods, key findings, and limitations.

---

## 1. Introduction

Artificial light at night (ALAN) is a pervasive environmental pressure with potential cross‑boundary impacts on protected areas. Yet national‑scale, reproducible assessments of ALAN exposure inside protected areas (PAs) and their surrounding landscapes are still rare. We address two linked questions:

1) **Layer A (primary):** How has ALAN inside Australian protected areas changed over time, and how does it compare to surrounding buffers and boundary‑interior gradients?
2) **Layer B (secondary):** Is there a conservative, bias‑aware nocturnal biodiversity occurrence signal consistent with ALAN exposure near protected areas?

Layer B is explicitly framed as a **signal test**, not population inference, given the biases inherent in presence‑only data.

---

## 2. Methods

### 2.1 Data sources

- **Protected areas:** CAPAD 2024 terrestrial polygons (dissolved by PA_ID). Processed geometry descriptors in `data/processed/pa_geometries_v0_3_0.csv` (not tracked in git; reproducible via pipeline). See `analysis/reports/pa_geometry_qc.md`.
- **Night lights:** VIIRS annual composite rasters (2013–2024), Zenodo v0.4 (OpenGeoHub). See `data/README.md` and `src/python/dsipa/nightlights.py`.
- **Biodiversity occurrences (Layer B):** Atlas of Living Australia (ALA) occurrence downloads for microbats (Chiroptera excluding Pteropodidae) and diurnal birds (Passeriformes). Processed outputs are not tracked in git; quality filters and dedup summary are documented in `analysis/reports/layerB_data_qc.md` and `analysis/reports/layerB_qc_extended.md`.

### 2.2 Layer A: ALAN metrics inside, outside, and across boundaries

- **Inside‑PA summaries:** mean/median radiance, plus censoring‑aware metrics (`frac_gt0`, `p95`) for each year.
- **Outside buffers:** 1 km and 5 km buffers with land‑only and land‑unprotected variants. Validity metrics are recorded in `data/processed/pa_buffer_validity_v0_3_0.csv` and summarized in `analysis/reports/national_layerA_coverage_and_sanity.md`.
- **Inside rings:** distance‑to‑edge profiles (0–1, 1–5, 5–10 km). Completeness is limited and explicitly reported; see `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`.

### 2.3 Layer A trends and retention indices

- **Trend estimation:** Theil–Sen slopes per PA for 2013–2024, requiring ≥8 valid years and ≥10 valid pixels/year.
- **Retention indices:** inside trend minus buffer trend, with primary buffer type `land_unprotected`.
- Outputs and diagnostics: `data/processed/pa_trends_v0_3_0.csv` and `analysis/reports/trends_methods_and_sanity.md`.

### 2.4 Layer A vulnerability ranking (descriptive)

- Category‑safe rankings (inside brightening, buffer brightening, internalisation, external pressure).
- See `analysis/reports/risk_rankings_and_quadrants.md` and `manuscript/figures/fig_layerA_retention_quadrant.png`.

### 2.5 Layer B: conservative signal test (provider‑matched primary)

- **Focal taxa:** microbats; **control:** diurnal passerines.
- **Filters:** 2013–2024; coordinate uncertainty ≤1 km; species‑level IDs; remove captive/escaped; spatial/day deduplication.
- **Primary inference:** provider‑matched (NSW BioNet dr368), spatial‑blocked (50 km) case‑control model.
- **ALAN representation:** two‑part covariates (`any_light`, `log1p(ALAN)` conditional on >0).
- **Falsification:** ALAN shuffled within spatial blocks.
- **Sensitivity:** multi‑provider run, clearly labelled as non‑primary.
- Full details and metrics: `analysis/reports/layerB_modelling_report.md` and `manuscript/figures/fig_layerB_alan_effects.png`.

---

## 3. Results

### 3.1 Layer A: Baseline ALAN exposure inside PAs

- The baseline map shows eligibility and inside mean radiance for 2024, separating insufficient‑pixel areas from eligible PAs (Fig. `manuscript/figures/fig_layerA_baseline_map.png`).

### 3.2 Layer A: Trends and retention

- Distribution of inside trends (mean radiance) highlights heavy zero mass with a modest brightening tail (Fig. `manuscript/figures/fig_layerA_trend_distribution.png`).
- Retention quadrants contrast inside vs buffer slopes and provide descriptive rankings of PAs (Fig. `manuscript/figures/fig_layerA_retention_quadrant.png`; table in `analysis/reports/risk_rankings_and_quadrants.md`).

### 3.3 Layer A: Edge penetration feasibility

- Ring feasibility is low for complete rings, and edge profiles should be interpreted conditionally (Fig. `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`).

### 3.4 Layer B: Exposure diagnostics and data context

- Zero‑inflation and exposure tails differ by stratum and taxon group (Fig. `manuscript/figures/fig_layerB_exposure_summary.png`).
- Occurrence counts by year/state show strong administrative concentration (Fig. `manuscript/figures/fig_layerB_occurrence_counts.png`).
- Spatial density maps highlight observer‑effort clustering (Fig. `manuscript/figures/fig_layerB_occurrence_density.png`).

### 3.5 Layer B: Modelling signal test

- Provider‑matched microbats vs passerines show a weak ALAN signal under spatial blocking; shuffled‑ALAN falsification trends toward null (Fig. `manuscript/figures/fig_layerB_alan_effects.png`; report in `analysis/reports/layerB_modelling_report.md`).
- Multi‑provider sensitivity is descriptive only and does not alter the primary inference (see same report).

---

## 4. Discussion (outline)

- Layer A indicates widespread ALAN floor effects, with a subset of PAs exhibiting non‑zero brightening trends.
- Buffer validity and ring completeness are key constraints; interpretations are conditional on eligible subsets.
- Layer B suggests a modest, non‑causal association consistent with ALAN exposure, but sampling bias remains a dominant concern.

---

## 5. Limitations

- **Censoring:** 500 m composites yield heavy zero‑mass; mean/median trends are constrained by the sensor floor.
- **Selection:** many PAs lack sufficient valid pixels or complete rings; results are conditional on eligible subsets.
- **Occurrence bias (Layer B):** strong provider/state concentration and spatial clustering; inference is restricted to provider‑matched case‑control design.
- **Causality:** presence‑only models cannot infer population decline or causal effects.

---

## 6. Data and code availability

- Large derived tables and raw occurrences are intentionally excluded from git; reproducible outputs are generated via the pipeline described in `docs/roadmap.md`.
- Public data sources and checksums are recorded in `data/README.md`.


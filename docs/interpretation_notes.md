# Interpretation notes (DSIPA-NBS)

This is the lab notebook for “what the results are saying”.
Every key figure/table/model must have an entry here.

---

## Result entries (append over time)

### SMOKETEST_RADIANCE_BUFFERS_2013_2018_2024

- Artefact: `artefacts/wp0_6_radiance_smoketest/`
- What it shows (plain language):
  - Inside vs outside-buffer mean radiance for the triad PAs across 2013/2018/2024.
  - Urban-edge PA buffers are brighter than interiors; remote PA remains low across zones.
  - Peri-urban PA sits between the two extremes, as expected for a smoke-test.
- Relation to hypotheses:
  - Consistent with H1/H2 as a sanity check (inside darker than buffers for developed contexts).
- Sanity verdict (pass/warn/fail) and why:
  - pass — relative ordering and inside/buffer contrast look plausible for the triad.
- Surprises / concerns:
  - Scale metadata differs by year (2024 shows scale=10); scale/offset now applied for comparability.
  - Some low pixel-counts for small geometries; watch for unstable estimates.
- Follow-up tasks:
  - [ ] Add/record minimum valid pixel thresholds for national summaries.

### SMOKETEST_EDGE_PROFILES_2013_2018_2024

- Artefact: `artefacts/wp0_7_edge_profiles_smoketest/`
- What it shows (plain language):
  - Ring-based mean radiance (0–1, 1–5, 5–10 km inside boundary) for triad PAs.
  - Urban-edge PA shows higher near-boundary values than deeper rings; remote PA is flat/low.
- Relation to hypotheses:
  - Supports H2 as a directional sanity check (edge gradients present where expected).
- Sanity verdict (pass/warn/fail) and why:
  - warn — ring 5–10 km has zero valid pixels for all triad PAs, likely due to small PA sizes.
- Surprises / concerns:
  - Missingness in outer ring suggests current ring widths may be too large for some PAs.
- Follow-up tasks:
  - [ ] Track valid pixel counts per ring and flag low-coverage rings in national outputs.
  - [ ] Consider adaptive ring bins (or minimum-area filter) for small PAs.

### FIG1_ALAN_baseline_map_inside_PA

- Artefact: `manuscript/figures/fig_layerA_baseline_map.png`
- What it shows (plain language):
  - Two-panel baseline: eligibility (>=10 valid pixels) and inside mean radiance for eligible PAs in 2024.
  - Bright clusters near major cities; large dark regions in remote interiors are now explicitly separated from “missing/insufficient pixels”.
- Plot settings:
  - Color scale clipped at the 99th percentile to reduce outlier dominance.
- Relation to hypotheses:
  - Supports H1 that many PAs are dark while some are exposed to higher ALAN.
- Sanity verdict (pass/warn/fail) and why:
  - warn — eligibility is 4,422/11,112 PAs (39.8%) and zero‑mass among eligible is ~86.9%, so selection dominates interpretation.
- Surprises / concerns:
  - Coverage fraction for inside zones remains ~0.40 at the 10‑pixel threshold; zero‑mass remains high even among eligible PAs.
  - PA universe now includes JBT/EXT; totals align across geometry/radiance tables (11,133).
- Follow-up tasks:
  - [ ] Decide whether the map should explicitly denote “floor mass” in caption text.

### FIG2_TRENDS_distribution_and_hotspots

- Artefact: `manuscript/figures/fig_layerA_trend_distribution.png`
- What it shows (plain language):
  - Distribution of Theil-Sen inside slopes based on **mean** radiance (primary) for eligible PAs; non-zero tail remains small.
  - Median-based trends retained as robustness (mostly zero); censoring-aware metrics (frac_gt0, p95) still have heavy zero‑slope mass.
- Relation to hypotheses:
  - Consistent with H1: many stable/dark PAs with a subset brightening.
- Sanity verdict (pass/warn/fail) and why:
  - warn — mean slope zero‑mass is ~89.7% even after eligibility; frac_gt0 zero‑mass is ~91.1% and p95 ~96.2%.
- Surprises / concerns:
  - New exposure metrics do not materially reduce censoring at 500 m; interpretation should stress selection.
- Follow-up tasks:
  - [ ] Sensitivity: test alternative thresholds for valid pixels / years.

### FIG3_EDGE_penetration_profiles_aggregate

- Artefact: `manuscript/figures/fig_layerA_edge_profiles_aggregate.png`
- What it shows (plain language):
  - Two-panel figure: ring feasibility (fraction of PAs with valid rings) and conditional edge profile (frac_gt0) for complete‑ring PAs in 2024.
  - Complete rings are rare (383/11,112 ≈ 3.4%); profile is conditional on this subset.
- Relation to hypotheses:
  - Supports H2: edge gradients appear in developed contexts.
- Sanity verdict (pass/warn/fail) and why:
  - warn — feasibility is low (ring 0 ≈ 39.8%, ring 1 ≈ 12.8%, ring 2 ≈ 3.4%); conditional profile should be framed as limited evidence.
- Surprises / concerns:
  - Non‑zero frac_gt0 rows among complete rings are ~10%, so profile may still be floor‑dominated.
- Follow-up tasks:
  - [ ] Consider adaptive rings or minimum-area filters for penetration metrics.

### FIG4_RETENTION_quadrant

- Artefact: `manuscript/figures/fig_layerA_retention_quadrant.png`
- What it shows (plain language):
  - Quadrant plot of inside vs 1 km buffer mean trends (land_unprotected), with clipped axes and quadrant counts.
- Relation to hypotheses:
  - Directly aligns with H1/H2 by contrasting inside vs outside trend directions.
- Sanity verdict (pass/warn/fail) and why:
  - pass — quadrant counts are reported (Q1=304, Q2=55, Q3=3308, Q4=190; n=3857) and clipping reduces outlier dominance.
- Surprises / concerns:
  - Quadrant patterns are sparse in some regions due to missingness.
- Follow-up tasks:
  - [ ] Consider adding uncertainty bands or density contours for the quadrant plot.

### TAB1_TOP_risk_protected_areas

- Artefact: `analysis/reports/risk_rankings_and_quadrants.md`
- What it shows (plain language):
  - Category-safe ranked lists: inside brightening, buffer brightening, internalisation, and external pressure (mean-based trends).
- Relation to hypotheses:
  - Supports H1/H2 by identifying PAs where inside brightening exceeds outside trends.
- Sanity verdict (pass/warn/fail) and why:
  - pass — rankings align with urban-adjacent PAs; report is transparent.
- Surprises / concerns:
  - External-pressure list contains many zero‑inside slopes; ensure the narrative stays descriptive.
- Follow-up tasks:
  - [ ] Add confidence intervals for risk scores in later iterations.

### FIG9_TRENDS_uncertainty_forest

- Artefact: `manuscript/figures/fig_layerA_trend_uncertainty_forest.png` (report: `analysis/reports/pa_trend_uncertainty.md`)
- What it shows (plain language):
  - IBRA-clustered bootstrap CIs for inside mean-radiance slopes (top-ranked PAs by median slope).
  - Several top-ranked PAs retain clearly positive slopes, but mid-rank CIs overlap and some cross zero.
- Relation to hypotheses:
  - Supports H1 by showing a non-zero brightening subset with uncertainty bounds; warns against over-precise ranking.
- Sanity verdict (pass/warn/fail) and why:
  - warn — IBRA coverage excludes ~35 PAs (external territories/offshore), and many CIs are wide/overlapping.
- Surprises / concerns:
  - High-slope PAs cluster around urban-adjacent reserves; some wide CIs suggest sensitivity to small sample sizes.
- Follow-up tasks:
  - [ ] Sensitivity: test block_len ±1 year and compare CI width stability.

### FIG10_TRENDS_dominance_heatmap

- Artefact: `manuscript/figures/fig_layerA_trend_dominance.png` (data: `analysis/reports/pa_trend_dominance_matrix.csv`)
- What it shows (plain language):
  - Pairwise probability that slope_i > slope_j among top-ranked PAs, derived from bootstrap draws.
  - Clear dominance for a small subset; mid-rank separation is weak (probabilities near 0.5).
- Relation to hypotheses:
  - Reinforces H1 but tempers “risk ranking” claims by showing overlap in trend uncertainty.
- Sanity verdict (pass/warn/fail) and why:
  - pass — probabilities are bounded [0,1] and show expected diagonal dominance.
- Surprises / concerns:
  - Some PAs with high median slopes show only modest dominance, indicating ranking instability.
- Follow-up tasks:
  - [ ] Consider adding a simplified dominance summary table (e.g., P(slope>0) + P(>median)). 

### FIG5_BIO_nocturnal_vs_control_effect_contrast

- Artefact: `manuscript/figures/fig_layerB_alan_effects.png` (report: `analysis/reports/layerB_modelling_report.md`)
- What it shows (plain language):
  - Provider-matched (dr368) log-odds coefficients for ALAN exposure (any_light + log1p_alan) in a microbats vs passerines case-control model.
  - Falsification via within-block ALAN shuffle yields near-zero coefficients and ~0.5 AUC.
  - Sensitivity (multi-provider) shows similar sign patterns but is treated as descriptive only.
- Relation to hypotheses:
  - Consistent with H3 in the sense of a detectable signal for microbats vs diurnal controls under provider-matched design, but effect sizes are modest and not causal.
- Sanity verdict (pass/warn/fail) and why:
  - warn — AUC is low (~0.54 primary); sensitivity AUC is modest (~0.56) and effects remain small.
- Surprises / concerns:
  - log1p(ALAN) is negative while any_light is positive; could reflect confounding or floor effects rather than ecology.
- Follow-up tasks:
  - [ ] Check robustness to adding stratum or year as covariates.

### FIG6_BIO_exposure_summary

- Artefact: `manuscript/figures/fig_layerB_exposure_summary.png`
- What it shows (plain language):
  - Zero‑mass and p95 ALAN exposure summaries at occurrence locations, stratified by inside/within/outside and by taxon group.
  - Inside PAs are heavily zero‑inflated; within‑10 km buffers show higher p95 and lower zero‑mass.
- Relation to hypotheses:
  - Supports the two‑part ALAN representation (any_light + intensity) by showing a large zero mass and a non‑zero tail.
- Sanity verdict (pass/warn/fail) and why:
  - pass — patterns align with expectations from Layer A censoring and Layer B exposure QC.
- Surprises / concerns:
  - Outside‑buffer p95 values remain high for birds; likely reflects observation bias near settlement edges.
- Follow-up tasks:
  - [ ] Consider adding within‑scope only panel in manuscript if space allows.

### FIG7_BIO_occurrence_counts_by_year_state

- Artefact: `manuscript/figures/fig_layerB_occurrence_counts.png`
- What it shows (plain language):
  - Heatmaps of filtered + deduplicated occurrence counts by year and state for microbats and diurnal birds.
  - Strong state concentration (NSW dominates both groups), with consistent year coverage 2013–2024.
- Relation to hypotheses:
  - Supports the provider‑matched design choice by making spatial/administrative concentration visible.
- Sanity verdict (pass/warn/fail) and why:
  - warn — extreme concentration in a few states implies that “national” inference is not defensible without bias modelling.
- Surprises / concerns:
  - Microbats have low counts outside NSW/QLD; provider composition likely drives patterns.
- Follow-up tasks:
  - [ ] Consider a provider/state‑matched sensitivity panel if space allows.

### FIG8_BIO_occurrence_density_map

- Artefact: `manuscript/figures/fig_layerB_occurrence_density.png`
- What it shows (plain language):
  - Spatial density of occurrence records (sampled for plotting) for microbats and diurnal birds.
  - Clusters along the eastern seaboard and around urban regions dominate both groups.
- Relation to hypotheses:
  - Reinforces that occurrence data are spatially biased; supports conservative framing and spatial blocking.
- Sanity verdict (pass/warn/fail) and why:
  - pass — patterns align with known observer effort gradients.
- Surprises / concerns:
  - Northern/remote coverage remains sparse, limiting exposure variation.
- Follow-up tasks:
  - [ ] None (descriptive context figure).

### [RESULT-ID]

- Artefact: `path/to/artefact`
- What it shows (plain language):
  - _
  - _
  - _
- Relation to hypotheses:
  - _
- Sanity verdict (pass/warn/fail) and why:
  - _
- Surprises / concerns:
  - _
- Follow-up tasks:
  - [ ] _
  - [ ] _

---

## Suggested IDs for Layer A (use if applicable)

- FIG1_ALAN_baseline_map_inside_PA
- FIG2_TRENDS_distribution_and_hotspots
- FIG3_EDGE_penetration_profiles_aggregate
- FIG4_RETENTION_quadrant
- TAB1_TOP_risk_protected_areas

## Suggested IDs for Layer B (optional)

- FIG5_BIO_nocturnal_vs_control_effect_contrast
- TAB2_BIO_sensitivity_and_negative_controls

---

## Summary (keep updated once results stabilise)

When the results are coherent enough for manuscript drafting, write a short summary here:
- Layer A story: National PA metrics show a large fraction of protected areas with very low (often zero) inside radiance, alongside a subset of PAs with consistently higher values near urban centres. Trend estimation (2013–2024) using mean radiance shows a non-zero tail of brightening PAs; median trends remain mostly zero. Inside mean radiance rises modestly over time without abrupt step changes.
- Layer B: provider-matched microbats vs passerines shows a weak ALAN signal (AUC ~0.54) with two-part covariates; shuffled ALAN collapses toward null. Sensitivity on multi-provider data is descriptive (AUC ~0.56) and does not change the primary inference.
- Limitations and mitigations:
  - Inside coverage is limited for small PAs; we use a minimum valid-pixel threshold and report missingness explicitly.
  - Ring profiles for outer bins are sparse; consider adaptive ring widths or minimum-area filters.
  - Scaling metadata changes in 2022–2024; we apply scale/offset metadata and document it.
  - Risk/retention rankings are descriptive; do not imply causality and still sensitive to missingness.

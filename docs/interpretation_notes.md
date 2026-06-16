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
  - warn — eligibility is 4,426/11,133 PAs (39.8%) and zero‑mass among eligible is ~86.9%, so selection dominates interpretation.
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
  - Complete rings are rare (383 PAs; 3.4% of the PA universe); profile is conditional on this subset.
- Relation to hypotheses:
  - Conservatively supports H2 only as a feasibility and conditional non-zero diagnostic; it is not a definitive penetration-gradient test.
- Sanity verdict (pass/warn/fail) and why:
  - warn — feasibility is low (ring 0 ≈ 39.7%, ring 1 ≈ 12.8%, ring 2 ≈ 3.4%), complete-ring median `frac_gt0` is zero in all rings, and conditional profile evidence must remain limited.
- Surprises / concerns:
  - Conditional non-zero share declines from 18.0% in the 0-1 km ring to 3.7% in the 5-10 km ring, but the complete-ring subset is too small for a primary edge-effect claim.
- Follow-up tasks:
  - [x] Consider adaptive rings or minimum-area filters for penetration metrics. Stage 2 decision: defer adaptive/min-area rings and retain fixed rings as a diagnostic only.

### FIG4_RETENTION_quadrant

- Artefact: `manuscript/figures/fig_layerA_retention_quadrant.png`
- What it shows (plain language):
  - Quadrant plot of inside vs 1 km buffer mean trends (land_unprotected), with clipped axes and quadrant counts.
- Relation to hypotheses:
  - Directly aligns with H1/H2 by contrasting inside vs outside trend directions.
- Sanity verdict (pass/warn/fail) and why:
  - pass — quadrant counts are reported (Q1=305, Q2=55, Q3=3,308, Q4=190; n=3,858) and clipping reduces outlier dominance.
- Surprises / concerns:
  - Quadrant patterns are sparse in some regions due to missingness.
- Follow-up tasks:
  - [ ] Consider adding uncertainty bands or density contours for the quadrant plot.

### TAB1_TOP_risk_protected_areas

- Artefact: `analysis/reports/risk_rankings_and_quadrants.md`
- What it shows (plain language):
  - Category-safe ranked lists: inside brightening, buffer brightening, internalisation, and external pressure (mean-based trends).
  - Stage 2 adds `analysis/reports/layerA_watchlists_uncertainty.md` and Table S1, joining inside-slope bootstrap intervals/probabilities to management-facing watchlists.
- Relation to hypotheses:
  - Supports H1/H2 by identifying PAs where inside brightening exceeds outside trends.
- Sanity verdict (pass/warn/fail) and why:
  - pass — rankings align with urban-adjacent PAs; report is transparent; all Table S1 rows have inside-slope bootstrap uncertainty.
- Surprises / concerns:
  - External-pressure list contains many zero-inside slopes; ensure the narrative stays descriptive and does not imply that buffer pressure has already penetrated the PA interior.
- Follow-up tasks:
  - [x] Add confidence intervals/probabilities for inside-slope uncertainty in Table S1.

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
  - [x] Consider adding a simplified dominance summary table (e.g., P(slope>0) + P(>median)).

### STAGE2_LAYERA_watchlists_and_dominance

- Artefacts:
  - `analysis/reports/layerA_watchlists_uncertainty.md`
  - `analysis/reports/layerA_dominance_summary.md`
  - `manuscript/text/supplementary_tables.md`
- What it shows (plain language):
  - Table S1 now provides 60 category-safe watchlist rows: top 20 inside brightening, top 20 external pressure, and top 20 internalisation.
  - Each watchlist row includes PA identifier/name/state, dominant IBRA, area, inside slope, 1 km buffer slope, 1 km retention index, inside-slope bootstrap 95% interval, and P(inside slope > 0).
  - The simplified dominance summary shows strong pairwise separation for only the leading top brighteners; mid-rank sites have much weaker dominance, supporting uncertainty-aware triage rather than precise rank claims.
- Relation to hypotheses:
  - Supports H1/H2 operationally by turning the hardened trend/quadrant results into transparent, category-safe priority lists.
  - Reinforces the uncertainty framing: the evidence supports a brightening tail and external-pressure subset, not exact ordinal rankings.
- Sanity verdict (pass/warn/fail) and why:
  - pass — category filters match the risk definitions, all rows have inside-slope bootstrap uncertainty, and dominance probabilities are bounded in [0,1].
- Surprises / concerns:
  - Some internalisation rows have wide inside-slope intervals despite positive point estimates, so practitioner use should focus on category membership plus uncertainty rather than rank number alone.
  - External-pressure uncertainty is currently inside-slope uncertainty only; buffer and retention uncertainty are still point-estimate fields.
- Follow-up tasks:
  - [ ] During Stage 4, state explicitly that Table S1 is for triage/hypothesis generation and not precise rank ordering.

### FIG5_BIO_nocturnal_vs_control_effect_contrast

- Artefact: `manuscript/figures/fig_layerB_alan_effects.png` (report: `analysis/reports/layerB_modelling_report.md`)
- What it shows (plain language):
  - Provider-matched (dr368) log-odds coefficients for ALAN exposure (any_light + log1p_alan) in a microbats vs passerines case-control model.
  - Falsification via within-block and within‑IBRA×year ALAN shuffles yields near-zero coefficients and ~0.51 AUC.
  - Sensitivity (multi-provider) shows similar sign patterns but is treated as descriptive only.
- Relation to hypotheses:
  - Consistent with H3 in the sense of a detectable signal for microbats vs diurnal controls under provider-matched design, but effect sizes are modest and not causal.
- Sanity verdict (pass/warn/fail) and why:
  - warn — AUC is low (~0.545 primary); falsification AUCs remain slightly >0.5 (block ≈0.505, IBRA ≈0.517), suggesting residual structure.
- Surprises / concerns:
  - log1p(ALAN) is negative while any_light is positive; could reflect confounding or floor effects rather than ecology.
  - any_light does not collapse fully under shuffling, indicating remaining bias structure.
- Follow-up tasks:
  - [x] Stage 3A no-run rationale: do not add stratum/year covariates by default. Provider matching, spatial blocking, block-level ALAN shuffling, IBRA x year shuffling, and the full multi-provider sensitivity are sufficient for the current weak secondary framing. Reopen only if a future goal asks Layer B to support stronger claims.

### FIG9_BIO_ibra_intensity_forest

- Artefact: `manuscript/figures/fig_layerB_ibra_intensity_forest.png` (data: `analysis/reports/layerB_ibra_effects.csv`)
- What it shows (plain language):
  - IBRA‑level heterogeneity in the log1p(ALAN) coefficient for regions with ≥500 records per class.
  - Most regions retain a negative intensity term, but a few show weakly positive or near‑zero estimates.
- Relation to hypotheses:
  - Supports a cautious “non‑linear association” framing; any signal is modest and region‑dependent.
- Sanity verdict (pass/warn/fail) and why:
  - warn — only 11 IBRA regions meet the minimum record threshold; heterogeneity is descriptive only.
- Surprises / concerns:
  - Some regions flip sign, underscoring sensitivity to sampling structure.
- Follow-up tasks:
  - [x] Stage 3A no-run rationale: do not merge or smooth IBRA regions in this pass. The current heterogeneity result is intentionally descriptive; coarser regional modelling would imply a stronger regional-inference goal.

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
  - [x] Stage 3A no-run rationale: do not add a provider/state-matched sensitivity panel by default. Existing counts, density diagnostics, provider matching, and full multi-provider sensitivity are enough to keep Layer B provider-bounded and conservative.

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

### STAGE3A_LAYERB_evidence_integration

- Artefacts:
  - `manuscript/text/supplementary_tables.md` Table S2
  - `manuscript/text/manuscript_draft.md`
  - `manuscript/text/figures.md`
  - `manuscript/text/supplementary_figures.md`
  - `docs/stage1_critique_resolution_matrix.md`
- What it shows (plain language):
  - Table S2 now anchors the Layer B signal test with the primary provider-matched model, block-shuffle falsification, IBRA x year shuffle falsification, and full multi-provider sensitivity.
  - The primary dr368 model remains weak (AUC 0.545), while both shuffles sit near null (AUC 0.505 and 0.517).
  - The full multi-provider sensitivity is retained as descriptive only because provider/state confounding returns.
- Relation to hypotheses:
  - Keeps H3 as a cautious secondary occurrence-association signal, not a causal or population-trend result.
  - Supports retaining Layer B as a falsification-aware method demonstration and weak signal, not as national biodiversity-response evidence.
- Sanity verdict (pass/warn/fail) and why:
  - pass for integration: Table S2 values match `analysis/reports/layerB_modelling_report.md`.
  - warn for inference strength: provider/state concentration and residual shuffled `any_light` structure require conservative wording.
- Surprises / concerns:
  - No new modelling was warranted for B04/B07/B09 under the accepted Stage 3 plan.
  - B10 remains open for Stage 3B because the tiny/sentinel ALA zip guardrail is code/test work.
- Follow-up tasks:
  - [ ] Stage 3B: add the ALA tiny/sentinel zip guardrail test using synthetic local fixtures only.
  - [ ] Stage 4: perform the final manuscript-wide claim, data availability, and release/archive pass.

### STAGE2_LAYERA_anchor_and_buffer_validity

- Artefacts:
  - `analysis/reports/layerA_sanity_dashboard.md`
  - `analysis/reports/layerA_buffer_validity_sensitivity.md`
- What it shows (plain language):
  - Bright/dark anchors now use explicit evidence-defined contexts rather than nearest-city medians.
  - Urban-adjacent eligible PAs have much higher upper-tail inside radiance than remote eligible PAs (2024 mean p95 112.769 vs 0.167).
  - External-pressure quadrant fractions are stable under stricter 1 km buffer-validity filters.
- Relation to hypotheses:
  - Supports the Layer A sanity requirement: bright urban-edge contexts are distinguishable from remote dark contexts, and the retention/external-pressure framing is not obviously an artefact of poor buffer validity.
- Sanity verdict (pass/warn/fail) and why:
  - pass — anchor contrasts are directionally strong, and strict buffer filtering changes sample size more than headline quadrant fractions.
- Surprises / concerns:
  - The national median remains zero in many strata, so upper-tail and conditional checks are more informative than aggregate medians.
- Follow-up tasks:
  - [ ] Carry these caveats into final Results/Discussion wording during Stage 4.

### STAGE2_LAYERA_threshold_and_edge_sensitivity

- Artefacts:
  - `analysis/reports/layerA_trend_threshold_sensitivity.md`
  - `analysis/reports/layerA_edge_profile_decision.md`
- What it shows (plain language):
  - The primary trend rule (`>=10` valid pixels, `>=8` valid years) gives 4,426 inside trend-eligible PAs, 89.7% zero inside mean-slope fraction, 420 positive inside slopes, and a retention-quadrant denominator of 3,858.
  - Trend-threshold results are stable across 6, 8, and 10 minimum valid years in the current complete annual evidence snapshot; stricter valid-pixel thresholds reduce sample size but leave the headline Q1/Q4 fractions similar.
  - The edge-profile figure is feasible only for a small complete-ring subset (383 PAs; 3.4% of the PA universe), with median `frac_gt0` equal to zero in all rings and conditional non-zero share declining from 18.0% to 3.7% from the 0-1 km to 5-10 km rings.
- Relation to hypotheses:
  - Supports H1 by showing the non-zero brightening tail and quadrant framing are not artefacts of one arbitrary valid-year threshold.
  - Keeps H2 conservative: the edge profile is retained as a feasibility and conditional non-zero diagnostic, not as a definitive penetration-gradient test.
- Sanity verdict (pass/warn/fail) and why:
  - pass for trend thresholds — denominator nesting and quadrant-count invariants hold, and stricter valid-pixel rules do not overturn the primary interpretation.
  - warn for edge profiles — complete-ring coverage is very low and medians are floor-dominated, so absence-of-edge-effect claims would be unsupported.
- Surprises / concerns:
  - Valid-year thresholds do not change counts because the current eligible series are effectively complete across the annual window; this is useful but should not be overgeneralised to future products.
  - Edge medians remain unusable as an effect-size summary; the figure must stay captioned as a diagnostic.
- Follow-up tasks:
  - [ ] Carry the threshold-sensitivity summary into Methods/Results during Stage 4.
  - [ ] Keep edge-profile wording conditional in captions and Discussion.

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
  - Ring profiles for outer bins are sparse; fixed rings are retained as a feasibility-limited diagnostic, with adaptive/min-area rings deferred rather than promoted in Stage 2.
  - Scaling metadata changes in 2022–2024; we apply scale/offset metadata and document it.
  - Risk/retention rankings are descriptive; do not imply causality and still sensitive to missingness.

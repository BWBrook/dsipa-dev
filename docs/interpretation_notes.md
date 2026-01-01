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
  - National map of inside-PA mean radiance in 2024 (scaled units).
  - Bright clusters near major cities; large dark regions in remote interiors.
- Relation to hypotheses:
  - Supports H1 that many PAs are dark while some are exposed to higher ALAN.
- Sanity verdict (pass/warn/fail) and why:
  - warn — many PAs have <10 valid pixels; values for very small PAs are sparse.
- Surprises / concerns:
  - Coverage fraction for inside zones is ~0.40 at the 10-pixel threshold.
- Follow-up tasks:
  - [ ] Consider minimum-area or minimum-pixel inclusion criteria for paper-facing maps.

### FIG2_TRENDS_distribution_and_hotspots

- Artefact: `manuscript/figures/fig_layerA_trend_distribution.png`
- What it shows (plain language):
  - Distribution of Theil-Sen inside slopes (median radiance) for PAs with >=8 valid years.
  - Most slopes near zero, with a right tail of brightening PAs.
- Relation to hypotheses:
  - Consistent with H1: many stable/dark PAs with a subset brightening.
- Sanity verdict (pass/warn/fail) and why:
  - pass — mean inside radiance increases modestly over time; no abrupt step changes observed.
- Surprises / concerns:
  - Only ~40% of PAs meet the minimum valid-pixel threshold for trend estimation.
- Follow-up tasks:
  - [ ] Sensitivity: test alternative thresholds for valid pixels / years.

### FIG3_EDGE_penetration_profiles_examples

- Artefact: `manuscript/figures/fig_layerA_edge_profiles_examples.png`
- What it shows (plain language):
  - Edge-to-core radiance profiles for three example PAs (triad IDs) across 2013/2018/2024.
  - Urban-adjacent example shows elevated near-edge radiance relative to interior.
- Relation to hypotheses:
  - Supports H2: edge gradients appear in developed contexts.
- Sanity verdict (pass/warn/fail) and why:
  - warn — outer ring coverage is sparse for small PAs.
- Surprises / concerns:
  - Ring 5–10 km bins are frequently missing for small PAs nationally.
- Follow-up tasks:
  - [ ] Consider adaptive rings or minimum-area filters for penetration metrics.

### FIG4_VULNERABILITY_predictor_effects_and_ranked_list

- Artefact: `manuscript/figures/fig_layerA_vulnerability_coefficients.png`
- What it shows (plain language):
  - Standardized coefficients for predictors of inside brightening slopes.
  - Effect sizes are small; model explains little variance (R2 ~0.01).
- Relation to hypotheses:
  - Suggests vulnerability predictors are weak under current covariate set.
- Sanity verdict (pass/warn/fail) and why:
  - warn — low explanatory power implies limited predictive leverage.
- Surprises / concerns:
  - Distance to city has only a small negative coefficient; not strongly predictive.
- Follow-up tasks:
  - [ ] Consider additional predictors (population density, land-use context) if available.

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
- FIG3_EDGE_penetration_profiles_examples
- FIG4_VULNERABILITY_predictor_effects_and_ranked_list
- TAB1_TOP_risk_protected_areas

## Suggested IDs for Layer B (optional)

- FIG5_BIO_nocturnal_vs_control_effect_contrast
- TAB2_BIO_sensitivity_and_negative_controls

---

## Summary (keep updated once results stabilise)

When the results are coherent enough for manuscript drafting, write a short summary here:
- Layer A story: National PA metrics show a large fraction of protected areas with very low (often zero) inside radiance, alongside a subset of PAs with consistently higher values near urban centres. Trend estimation (2013–2024) indicates mostly stable inside radiance with a right tail of brightening PAs; inside mean radiance rises modestly over time without abrupt step changes.
- Layer B: not attempted yet.
- Limitations and mitigations:
  - Inside coverage is limited for small PAs; we use a minimum valid-pixel threshold and report missingness explicitly.
  - Ring profiles for outer bins are sparse; consider adaptive ring widths or minimum-area filters.
  - Scaling metadata changes in 2022–2024; we apply scale/offset metadata and document it.
  - Vulnerability model explains little variance with current predictors; treat as exploratory.

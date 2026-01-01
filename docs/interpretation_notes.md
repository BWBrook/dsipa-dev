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
  - Scale metadata differs by year (2024 shows scale=10; raw values used).
  - Some low pixel-counts for small geometries; watch for unstable estimates.
- Follow-up tasks:
  - [ ] Confirm scale factor for Zenodo VIIRS COGs before national run.
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
- 1 paragraph: the core Layer A story.
- 1 paragraph: what Layer B did/did not show (if attempted).
- 3–6 bullet limitations and what we did to address them.

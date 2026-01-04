# DSIPA-NBS Project Plan (living narrative)

This document is the narrative overview (“the brochure”): what we are doing and why.
Execution details live in `docs/roadmap.md` (“the GPS”). If these disagree, update one or record a decision.

---

## 1) Research question and hypotheses

### Primary question (Layer A)
How has artificial light at night (ALAN) inside Australian protected areas changed over time, and to what extent is change explained by encroachment from surrounding landscapes?

### Secondary question (Layer B; optional)
Is there a conservative, bias-aware nocturnal biodiversity occurrence signal that is consistent with ALAN exposure near protected areas?

### Working hypotheses
H1 (dark-sky integrity): Many protected areas have lower night-light radiance than their surroundings, but a measurable subset show increasing radiance over time.

H2 (encroachment/edge effects): Brightening is often strongest near protected-area boundaries and in surrounding buffers, consistent with an “edge/encroachment” mechanism rather than uniform interior change.

H3 (optional; biodiversity signal): For selected nocturnal taxa (e.g., bats), occurrence patterns show a relationship with ALAN exposure that differs from negative controls (e.g., diurnal taxa), consistent with ecological sensitivity rather than pure observer bias.

---

## 2) Conceptual background (short)

Artificial light at night can alter behaviour, movement, and trophic interactions, and its effects can propagate across boundaries via spill light and skyglow. Protected areas may therefore be exposed to a cross-boundary pressure not addressed by conventional land-protection status. The project is designed to produce (i) a national-scale, reproducible assessment of ALAN exposure inside and around protected areas, (ii) time-series evidence for change, and (iii) interpretable predictors of which protected areas are most vulnerable.

Layer B is deliberately framed as a conservative “signal test” rather than a population trend inference, because opportunistic occurrence data can be confounded by sampling effort.

---

## 3) Data plan (public-domain, Australia)

### Protected areas
- Primary: CAPAD protected area polygons (version to be recorded at download time).
- Required metadata to retain if available: protected-area name/ID, jurisdiction, IUCN category (if present), marine/terrestrial flags.

### Night lights
- Primary: a consistent annual night-lights time series (candidate products to be chosen and recorded as an explicit decision).
- Requirements:
  - stable temporal coverage for multiple years,
  - clear units and documentation,
  - programmatic download.

### Optional covariates (only if promoted in roadmap)
- Urban proximity proxies (may be derivable from night lights themselves).
- Basic context layers that do not introduce licensing friction (e.g., land/sea mask).

### Biodiversity occurrences (Layer B; optional)
- Primary: Atlas of Living Australia occurrence downloads for focal nocturnal taxa (likely bats first).
- Negative controls: diurnal taxa selected to mirror sampling pathways where possible.
- Bias controls: target-group background and explicit sensitivity checks.

All data downloads must be recorded in `data/README.md` with URLs, access dates, versions, and checksums.

---

## 4) Analysis plan (high level)

### 4.1 Layer A outputs (core deliverable)
For each protected area, compute (per year):
- inside-PA radiance summaries (robust statistics),
- buffer-zone radiance summaries outside the boundary (encroachment pressure),
- inside “distance-to-edge” ring summaries (penetration profile).

Then:
- estimate per-PA temporal trends with robust methods,
- compute “darkness retention” metrics comparing inside vs outside trends,
- model vulnerability/predictors of brightening and penetration (geometry, context).

### 4.2 Layer B outputs (optional)
- Bias-aware models testing whether focal nocturnal occurrences show a relationship with ALAN metrics that differs from negative controls.
- Explicit falsification checks (if negative controls show the same “effect”, interpret as bias).

---

## 5) Response metrics (what we will report)

Minimum set for Layer A (to be operationalised with a documented schema):
- Core radiance: median/trimmed mean radiance inside PA.
- Encroachment pressure: radiance in outside buffers (at least two distances).
- Penetration: radiance in inside rings by distance to boundary (at least three rings).
- Trend: robust slope per metric per PA; plus classification (brightening/stable/dimming) with transparent thresholds.
- Retention index: inside-trend minus outside-trend (or ratio), with interpretation guidance.

Optional Layer B:
- Effect size of ALAN metric on relative occurrence probability (with uncertainty),
- Contrast between nocturnal focal taxa and diurnal negative controls,
- Sensitivity to bias-control choices.

---

## 6) Validation and sanity strategies

### 6.1 Numerical and geospatial sanity
- Geometries are valid; areas are positive; buffering does not create pathological artefacts.
- Radiance units documented; missingness patterns seen and explained.
- Obvious reality checks: major cities are bright; remote deserts are dark; year-to-year changes are not dominated by missing tiles.

### 6.2 Domain sanity (Layer A)
- For many protected areas near development, outside buffers should often be brighter than interiors.
- Edge-to-core gradients should be plausible (not necessarily monotonic everywhere, but interpretable and explainable).
- Trends should be robust to:
  - alternative summary statistics,
  - alternative reasonable buffer widths,
  - (if feasible) an alternative night-lights product.

### 6.3 Layer B defensibility
- Negative controls must be implemented and reported.
- No claims of abundance/decline from presence-only data.
- All inference framed as “signal consistent with” rather than “proved impact”.

---

## 7) Deliverables (paper-facing)

Layer A (minimum publishable unit):
- Figure(s): national map of ALAN exposure in protected areas; trend distribution; example edge profiles.
- Table: ranked list of protected areas by dark-sky integrity risk metrics.
- Methods: reproducible computation of metrics and trends.
- Reproducibility: one-command pipeline + run manifests + artefact folder(s).

Layer B (if successful):
- Figure(s): focal nocturnal vs negative-control effect contrasts.
- Clear limitation section.

---

## 8) Risks and contingencies

Key risks:
- Night-lights product changes or access friction: mitigate by recording versions, building resilient download logic, and keeping product choice explicit in `docs/decisions.md`.
- Computational load (national rasters × many polygons): mitigate with tiling strategies and staged runs; prioritise correctness and a small “smoke-test” region early.
- Layer B confounding: treat as optional; only ship if negative controls and sensitivity checks support a defensible signal.

---

## 9) References (seed list with DOIs)

General ALAN ecology:
- Hölker et al. 2010, Trends Ecol Evol. DOI: 10.1016/j.tree.2010.09.007
- Gaston et al. 2013, Biol Rev. DOI: 10.1111/brv.12036
- Sanders et al. 2021, Nat Ecol Evol. DOI: 10.1038/s41559-020-01322-x

Measuring night lights:
- Falchi et al. 2016, Sci Adv. DOI: 10.1126/sciadv.1600377
- Kyba et al. 2017, Sci Adv. DOI: 10.1126/sciadv.1701528

Protected areas and light pollution:
- Guetté et al. 2018, Biol Conserv. DOI: 10.1016/j.biocon.2018.04.018
- Sung & Lee 2022, J Nat Conserv. DOI: 10.1016/j.jnc.2022.126148
- Mu et al. 2021, Remote Sensing. DOI: 10.3390/rs13091849

Bats and lighting (Layer B candidates):
- Stone et al. 2009, Curr Biol. DOI: 10.1016/j.cub.2009.05.058
- Stone et al. 2015, Mammalian Biology. DOI: 10.1016/j.mambio.2015.02.004

(Expand and curate in a project `references.bib` once implementation begins.)

---

## 10) Current status (agent must keep updated)

- Current phase: Milestone 0.5.3 complete — PA universe harmonised across geometry/radiance outputs.
- Recently completed: Milestone 0.5.3 (WP0.14b; JBT/EXT included, denominators reconciled, figures/reports refreshed).
- Immediate next steps (should match the first unchecked WP in `docs/roadmap.md`):
  1) Package PI gate bundle for Milestone 0.5.3 (updated reports/figures and checksum entries).
  2) Proceed to WP0.15 (Layer B acquisition) only after PI sign-off.

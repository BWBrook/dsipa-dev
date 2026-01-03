I’ve gone through the Gate 0.5.1 bundle and sanity-checked the “main artefacts” (reports + the four manuscript figures) against the processed tables. 

My PI verdict is: **Milestone 0.5.1 is a real improvement (good fixes), but Layer A is not yet in a state where it can safely “power” Layer B.** Right now, Layer A is best thought of as a strong engineering scaffold plus an early scientific signal that’s dominated by censoring/selection and buffer-definition validity. Proceeding to biodiversity modelling without fixing those would mostly measure “urban-ness” and coastline geometry, not “dark‑sky integrity”.

Here’s the straight assessment.

First, what’s genuinely solid now
The move to mean-based trends as the primary metric is the correct call (median was quantised into “mostly zero” and effectively dead on arrival). Your revised reports also make the “zero slope mass” explicit, which is what a reviewer would force anyway. Replacing the earlier OLS “vulnerability coefficients” story with descriptive rankings/quadrants is also the right kind of humility: it keeps the paper in the realm of defensible description rather than spurious pseudo-causality.

On the engineering/reproducibility side, the repo has real strengths: tests are fast and meaningful, schema discipline is present, outputs are versioned, artefacts are bundled, and the scale/offset discontinuity (2022–2024 scale=10) has been handled and documented. That’s all good practice.

Now, the problems that still dominate the science

1. The floor/selection problem is not a footnote; it is the story right now.
   The external audit quantified it and it matches what’s in your reports and tables: trends apply to **4426/11133 protected areas (~40%)** because of the min valid-pixel rule, and even within those, **most parks sit exactly at the product floor (mean==0 for all years in ~85%, median==0 in ~96%)**, so trend slopes are overwhelmingly exactly zero. 

That’s not “bad coding”. It’s a measurement reality: **at 500 m, this product mostly can’t resolve low-level light signals inside protected areas**, and it completely fails for the huge long tail of small reserves (because of pixel support). If we pretend otherwise, reviewers will (rightly) shred the manuscript.

2. The edge/penetration rings are effectively unusable as a national inference tool.
   The “complete rings” subset is **369/11133 (~3.3%)**, and your aggregate edge profile figure is essentially flat at ~0. 
   This means: the current “penetration” concept does not generalise and probably cannot be made to generalise with fixed kilometre rings at this resolution. If we keep an “edge penetration” figure, it must be framed as: “only measurable for a small subset; evidence weak at VIIRS/500 m”.

Also, your chosen example PA in the edge figure is actively unhelpful: it shows the opposite of the expected mechanism (values increasing inward). That’s not a win; it’s a signal that the figure is not yet doing what the caption will claim.

3. Buffer validity is currently the biggest conceptual confound.
   Your buffers are “buffer minus PA”, but they don’t exclude: (i) ocean/water, (ii) overlap with other protected areas, (iii) adjacent protected-area complexes. The external audit flags this as a critical conceptual failure mode, and I agree. 
   Without fixing/quantifying this, “outside buffer” is often not “development pressure”; it’s sometimes literally “dark ocean” or “still protected”.

This contaminates any retention metric and any inside-vs-outside interpretation. It’s also exactly the kind of thing a sharp reviewer will point out in one sentence that ruins your whole Results section.

4. The “risk_score” semantics are still wrong enough to mislead.
   Even after the pivot away from OLS, the combined risk score can rank parks with strong dimming but even stronger dimming outside (or other artefacts) as “high risk”. That’s not a small semantics issue; it’s the difference between a defensible “watchlist” table and a reputational hazard.

5. A couple of engineering nits matter because they weaken trust in the artefact trail.
   The audit points out smoke-tests are currently brittle because they still hardcode v0_1_0 triad filenames, and many artefacts were built from a “dirty” working tree. 
   These aren’t “science”, but they’re exactly the kind of paper-cut that makes reviewers suspicious of everything else.

So, decision: Layer B is NO‑GO right now
Despite the earlier “conditional-go” decision, I’m overruling it for the moment: **do not start WP0.15 (Layer B acquisition) yet.**
Layer B will be junk science unless we (a) repair buffer validity, and (b) explicitly address the censoring/floor problem by designing an exposure metric that actually varies across a meaningful subset and documenting the selection process in a way reviewers can’t poke holes in.

Retooling the roadmap: add a Milestone 0.5.2 “Validity + censoring” gate (before WP0.15)
Codex should insert a new milestone between 0.5.1 and 0.6.x, and only then reconsider Layer B. These are 1–3 hour WPs each if kept tight.

WP0.10c — Buffer validity decomposition + corrected buffers (land + non-PA)
Outcome: For each PA and buffer, quantify what fraction is land vs ocean and what fraction overlaps other protected areas; produce “corrected buffer” summaries that exclude (i) ocean and (ii) overlapping protected land (excluding the focal PA).
Acceptance criteria:

* New per-PA buffer descriptors: land_fraction, protected_overlap_fraction, effective_land_area_km2.
* Sensitivity report: how inside-minus-buffer and buffer trends change under (a) raw buffer vs (b) land-only vs (c) land-only minus protected-overlap.
* Tests asserting fractions are within [0,1] and that inland parks have land_fraction ~1.
  Artefact evidence: a report + a processed table + updated schema reference.

WP0.11c — Censoring-aware “exposure” metrics and trend logic
Outcome: Add at least one additional exposure metric that is explicitly designed to handle floor effects (e.g., fraction of pixels >0, and/or a high quantile like p95), computed for inside and buffers, and redo trends for those metrics.
Acceptance criteria:

* New columns in the radiance table (documented in schema reference).
* Trend table extended (or new trend table) for the new metric(s).
* Report summarising: (i) what fraction of parks are structurally at floor, (ii) how many parks have non-zero exposure under each metric, stratified by area and city-distance bands.
* Figures updated to show this selection explicitly (counts on-panel).
  Artefact evidence: report + updated manuscript figure(s) + tests for metric invariants (e.g., frac_gt0 in [0,1], p95 ≥ median ≥ min, etc.).

WP0.12c — Fix the “risk/retention” semantics and tables so they cannot lie
Outcome: Replace the single blended “risk_score” with a small set of clearly-defined categories and rankings that respect sign and interpretation.
Acceptance criteria:

* Separate ranked lists for: (a) inside brightening (inside slope >0), (b) buffer brightening (buffer slope >0), (c) “internalisation” (inside >0 and inside > buffer), and (d) “external pressure” (buffer >0 and inside ~0).
* Any composite index must be explicitly named as descriptive and must not elevate parks with inside dimming into “high risk” lists.
* Quadrant plot revised to handle outliers (clip axes or use robust scaling) and report quadrant counts.
  Artefact evidence: updated report + updated figure + regression tests that enforce category rules.

WP0.13c — Figure set revision to match what the data actually supports
Outcome: Make the Layer A figure suite honest and interpretable under censoring and selection.
Acceptance criteria:

* Baseline map becomes two-layer or two-panel: coverage/eligibility (valid pixels) and radiance for eligible parks (with explicit “0 mass” annotation).
* Edge figure either becomes “ring feasibility + conditional profile” or is demoted to Supplementary with blunt language about n=369.
* All panels contain sample sizes (n) and what “missing” means.
  Artefact evidence: revised manuscript figures + figure inventory update.

WP0.4b — Smoke-test paths + manifest hygiene (quick engineering credibility win)
Outcome: Smoke-test modules stop hardcoding v0_1_0 filenames and manifests become sufficient for audit.
Acceptance criteria:

* Smoke-tests run in-place on a fresh clone without symlink hacks.
* Manifest policy: any manuscript-facing figure artefact must be generated from a clean commit (or explicitly labelled otherwise).
  Artefact evidence: passing smoke-test, updated MANIFEST behaviour, updated docs.

After 0.5.2, revisit Layer B go/no-go
Only once buffer validity and censoring-aware exposures exist do we re-evaluate Layer B. At that point, we also need a sober conversation about exposure definition: for biodiversity, the buffer (5–10 km) may be the ecologically relevant “skyglow pressure proxy” even if inside is at floor. If we proceed, Layer B should probably use point-level or buffer-level exposure, not “mean inside PA” as the primary covariate.

Core directive for Codex:
“Implement Milestone 0.5.2 as above; do not start WP0.15; then stop for PI gate review with updated artefacts + external audit.”

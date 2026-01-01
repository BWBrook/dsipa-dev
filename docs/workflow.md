# DSIPA-NBS Workflow: Result Review Cycle + Artefact Review Cycle

This document defines how the agent must interrogate its own outputs.
The key rule: “runs without errors” is not a scientific result.

This workflow is mandatory whenever you:
- implement or modify the metric engine,
- generate a new candidate main figure/table,
- change data sources, projections, buffer logic, or trend methods.

Related documents:
- Narrative plan: `docs/plan.md`
- Execution queue: `docs/roadmap.md`
- Irreversible decisions: `docs/decisions.md`
- Interpretation lab notebook: `docs/interpretation_notes.md`
- Chronological record: `docs/log/`
- Human questions only when blocked: `docs/questions_for_human.md`

---

## Part A: Result Review Cycle (scientific validity)

### Step 1 — Sanity checks (numerical + domain)

You must implement and run explicit checks (tests or sanity scripts). Include both:

1) Numerical / technical sanity
- No NaN/Inf in computed metrics.
- Radiance values fall within documented plausible ranges for the chosen product.
- Missingness is measured, mapped, and explained (not silently dropped).
- Spatial joins are stable: repeated runs yield identical outputs given identical inputs.
- Geometry validity: no empty geometries after cleaning; buffering does not crash.

2) Domain sanity (DSIPA-specific)
- “Obvious anchors”: select a small set of known bright locations (major city footprints) and known dark locations (remote interior) and confirm ordering.
- Inside vs outside: for many PAs near development, outside buffers should often be brighter than interiors (not required universally, but must be interpretable).
- Edge profile plausibility: radiance near boundaries should not show pathological spikes everywhere; if it does, investigate projection/buffering artefacts.
- Trend plausibility: abrupt national-wide “step changes” should trigger a check for product version changes or data gaps.

Sanity checks should be encoded as code whenever feasible, and reported in the relevant `docs/log/*.md` entry.

### Step 2 — Interpretation (write it down)
For each candidate main result:
- Save the artefact to:
  - `manuscript/figures/` (paper-aimed), or
  - `analysis/reports/` (exploratory).
- Add an entry to `docs/interpretation_notes.md` with:
  - artefact path,
  - 2–5 bullets: what it shows, how it relates to the hypotheses,
  - surprises/concerns,
  - follow-up tasks (checkboxes).

Write these notes as if explaining to a collaborator who has not seen the code.

### Step 3 — Iteration (close the loop)
For each “concern” or follow-up task:
- implement the follow-up (additional diagnostic, alternative parameter, sensitivity check),
- generate new artefacts if needed,
- update the same interpretation entry with what you learned,
- record irreversible changes in `docs/decisions.md`.

Do not progress to the next Work Package with unresolved red flags in the core Layer A results.

---

## Part B: Artefact Review Cycle (engineering validity)

This is the “lab bench calibration” loop. For each Work Package (WP) you complete in `docs/roadmap.md`, you must produce inspectable artefacts and confirm they make sense.

### Step 1 — Build artefacts
At minimum (if Python is primary):
- build a source distribution and wheel for the project package,
- ensure package metadata and dependencies are consistent,
- ensure any docs/reference build process is runnable (even if minimal).

### Step 2 — Canonical run artefact folder
Create/update a canonical folder under `artefacts/` (or `analysis/artefacts/`) that contains:
- `MANIFEST` with:
  - git commit hash,
  - data source versions + checksums used,
  - environment/package versions,
  - date/time (UTC),
  - what WP this corresponds to.
- “Evidence outputs” required by the WP:
  - tables, figures, summary reports.

### Step 3 — Sanity inspection notes
In the relevant `docs/log/*.md` entry, include:
- what artefacts were built,
- what the canonical run produced,
- a short human-readable sanity verdict (pass/warn/fail) and why.

### Step 4 — Iterate until coherent
If artefacts do not build, the canonical run is brittle, or sanity fails:
- fix,
- rebuild,
- re-run,
- re-inspect,
until the WP definition of done is met.

---

## Stop rule
If you repeatedly fail sanity checks or hit an ambiguous conceptual fork:
- write targeted questions in `docs/questions_for_human.md`,
- summarise the blocker in your next message,
- pause that branch until answered.

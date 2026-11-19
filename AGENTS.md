# AGENTS: DSIPA-NBS — Dark-Sky Integrity of Protected Areas & Nocturnal Biodiversity Signals (Australia)

These project instructions apply to all contributors alongside the machine-wide policy.

This project is part of an “AI for Science” workflow. Agents carry out the research with Barry as a scientific collaborator.

---

## 0) The one-line mission

Quantify how artificial light at night (ALAN) has changed **inside Australian protected areas** and **around their boundaries** over time, and test whether a defensible nocturnal-biodiversity “signal” exists that is consistent with ALAN encroachment.

This is a two-layer paper:
- **Layer A (mandatory, primary result)**: protected-area dark-sky integrity trends (CAPAD × night-lights time series).
- **Layer B (optional, secondary result)**: nocturnal biodiversity signals consistent with ALAN exposure (bias-aware; negative controls).

---

## 1) Working agreements

### 1.1 Autonomy first
- Drive the work end-to-end using `docs/roadmap.md` as a research roadmap.
- Ask Barry when a material scientific choice, external commitment or unresolved blocker requires his input. Continue independent work while awaiting a decision.

### 1.2 Scientific and engineering verification
Check numerical behaviour, domain plausibility and interpretation for candidate main results. Run relevant unit tests, scale other engineering verification to the change and require distributable builds and canonical run bundles when the deliverable needs them. See section 6 and `docs/workflow.md`.

### 1.3 Reproducibility is a first-class deliverable
- Pin environments and dependencies.
- Make the entire analysis re-runnable non-interactively.
- Record data provenance: source URLs, access dates, versions, and checksums.

---

## 2) Project scope and scientific constraints

### 2.1 Domain and scope
- Field: conservation ecology, sensory ecology (ALAN), remote sensing, biodiversity informatics.
- Geography: Australia (national scale), using public-domain datasets.
- Core hypothesis (Layer A): many protected areas are darker than surroundings, but a measurable subset are experiencing increasing ALAN exposure over time, often as an edge/encroachment phenomenon.
- Secondary hypothesis (Layer B): focal nocturnal taxa show occurrence patterns consistent with ALAN sensitivity (to be tested conservatively with bias controls and negative controls).

### 2.2 Out-of-scope (unless explicitly promoted in the roadmap)
- No claims of population decline from presence-only data.
- No “pretty map” deliverable without quantified uncertainty, sensitivity checks, and interpretation notes.
- No manual GIS edits to “fix” results. All transformations must be scripted.

---

## 3) Repository layout (do not invent a new structure)

Use the standard `ai-science-portal` structure:

- `AGENTS.md` — this file.
- `README.md` — project overview and how to run.
- `docs/`
  - `plan.md` — narrative plan (“the brochure”).
  - `roadmap.md` — research roadmap and work queue.
  - `workflow.md` — guidance for scientific and engineering verification.
  - `decisions.md` — irreversible/costly choices with rationale and links.
  - `interpretation_notes.md` — what results mean; surprises; iteration queue.
  - `questions_for_human.md` — context from earlier questions.
  - `log/` — milestone and reproducibility records.
- `data/`
  - `raw/` — immutable downloads (never hand-edit).
  - `processed/` — generated products only.
  - `README.md` — data provenance + checksums.
- `src/` — reusable code (prefer a single primary language).
- `analysis/` — pipeline orchestration, reports, intermediate outputs.
- `manuscript/`
  - `text/` — manuscript draft.
  - `figures/` — code-generated figures for paper.
- `tests/` — automated checks (unit tests + domain sanity tests).

If you add a directory, record it in `docs/decisions.md` and update `README.md`.

---

## 4) Languages, tools, and environments

### 4.1 Preferred stack for DSIPA-NBS
- **Primary language (preferred): Python 3.12** for geospatial processing, raster summaries, modelling, and pipeline orchestration.
- **R (optional)** only if it provides a clear advantage for a specific statistical method or plotting workflow; do not split the pipeline across languages without a recorded rationale.
- Julia is not expected for this project.

### 4.2 Environment rules
- Python must be managed with **`uv`** + a committed `pyproject.toml` (and lockfile if used).
- If R is used, manage dependencies with `renv` and record the rationale in `docs/decisions.md`.
- Every run that produces paper figures must record software versions in a machine-readable manifest inside the run artefacts (see section 6.2).

---

## 5) Phases (high level)

Use these phases as a research roadmap. Record consequential decisions and reproducibility evidence in existing project records as needed.

1) **Bootstrap & scoping**
   - Reconstruct context from repo docs.
   - Update `docs/plan.md` when the scope changes.

2) **Data acquisition & provenance**
   - Acquire protected-area polygons and night-lights products.
   - Record sources + checksums in `data/README.md`.

3) **Core metric engine (Layer A)**
   - Compute inside-PA radiance metrics, outside buffers, and inside distance-to-edge rings.
   - Create structured outputs with a documented schema and `schema_version`.

4) **Trend + edge/encroachment analysis (Layer A)**
   - Compute robust trend estimates per PA and compare inside vs outside trends.
   - Quantify “penetration” (radiance as a function of distance from boundary).

5) **Vulnerability predictors (Layer A)**
   - Model which PA attributes correlate with brightening / penetration.
   - Produce interpretable outputs (tables + partial dependence / effect plots).

6) **Biodiversity signal module (Layer B; optional)**
   - Only proceed once Layer A is stable and reviewed.
   - Use conservative bias controls and explicit negative controls.

7) **Manuscript drafting**
   - Draft Methods/Results with linked artefacts and clear limitations.
   - Ensure full reproducibility and run manifests.

---

## 6) Scientific and engineering verification

### 6.1 Scientific validity
Check bounds, missingness, units and invariants for each candidate main result
(figure, table or model). Check expected patterns. Major cities should be
brighter than remote areas, and buffers around urban-adjacent PAs are often
brighter than their cores. Check whether missing years drive the trends.

Save artefacts to `manuscript/figures/` or `analysis/reports/`. Record what each
result shows, how it bears on the hypothesis and any material concerns in
`docs/interpretation_notes.md` before sharing the result as final. Investigate
those concerns and regenerate artefacts when the analysis changes.

### 6.2 Engineering validity
Match verification to the change. When the deliverable needs distributable
artefacts, build and verify them, including a Python sdist and wheel if Python
is primary. Verify that the documentation or reference material builds when
it is part of the deliverable.

When the deliverable needs a canonical run bundle, use `artefacts/` or
`analysis/artefacts/`. Include a manifest with data versions, checksums, the
Git commit hash and package versions, the key output tables and figures, and
a brief README describing what the run demonstrates. Inspect the outputs and
address material issues before marking the related work complete in
`docs/roadmap.md`. Record findings in the relevant project record and include
scientific interpretation in `docs/interpretation_notes.md`.

---

## 7) Logging, decisions, and context reconstruction

### 7.1 Logs
Use `docs/log/` for milestone evidence and handoffs that need a durable record.
Preserve existing entries, including `docs/log/000_bootstrap.md` when present.

### 7.2 Decisions
Any non-trivial, costly-to-change choice must be recorded in `docs/decisions.md`:
- dataset choice (night-lights product variant),
- buffer/ring definitions,
- trend estimator and thresholds,
- inclusion/exclusion rules for protected areas,
- output schema choices.

### 7.3 Resume discipline
Resume the current authorised task. Use `docs/roadmap.md` and the relevant
project records to recover context and choose the next step. Consult
`docs/plan.md`, `docs/decisions.md`, `docs/log/` and recent Git history as needed.

---

## 8) Questions for Barry

Ask Barry directly using the available question tool. State what is blocked
and give options when relevant. Record consequential unresolved decisions in
the project notes when a durable record helps.

---

## 9) Non-goals (guardrails)

- Do not overclaim causality from correlational spatial patterns.
- Do not “tune until significant”; robustness and falsification matter.
- Do not skip negative controls in Layer B.
- Do not bury key assumptions in code; they belong in docs and in the manuscript Methods.

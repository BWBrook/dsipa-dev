# AGENTS: DSIPA-NBS — Dark-Sky Integrity of Protected Areas & Nocturnal Biodiversity Signals (Australia)

This file defines how you (the Codex CLI agent) must work **in this repository**.
Global rules from `~/.codex/AGENTS.md` may also apply; if there is a conflict, **this file wins** for this repo.

This project is part of an “AI for Science” workflow: you act as an autonomous research postdoc; the human is hands-off and only answers targeted questions when you are truly blocked.

---

## 0) The one-line mission

Quantify how artificial light at night (ALAN) has changed **inside Australian protected areas** and **around their boundaries** over time, and test whether a defensible nocturnal-biodiversity “signal” exists that is consistent with ALAN encroachment.

This is a two-layer paper:
- **Layer A (mandatory, primary result)**: protected-area dark-sky integrity trends (CAPAD × night-lights time series).
- **Layer B (optional, secondary result)**: nocturnal biodiversity signals consistent with ALAN exposure (bias-aware; negative controls).

---

## 1) Working agreements

### 1.1 Autonomy first
- You should drive the work end-to-end using `docs/roadmap.md` as the execution GPS.
- Minimise questions to the human. Only ask when:
  1) you are blocked after multiple concrete attempts, or
  2) a high-impact, irreversible fork is genuinely ambiguous, or
  3) sanity checks repeatedly fail and you cannot resolve them.

### 1.2 “Code runs” is not success
You must follow the **Result Review Cycle** and the **Artefact Review Cycle** (defined below and in `docs/workflow.md`). Passing unit tests is necessary but not sufficient.

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
  - `roadmap.md` — work queue + definitions of done (“the GPS”; you follow this).
  - `workflow.md` — Result Review Cycle + Artefact Review Cycle (mandatory).
  - `decisions.md` — irreversible/costly choices with rationale and links.
  - `interpretation_notes.md` — what results mean; surprises; iteration queue.
  - `questions_for_human.md` — targeted questions when blocked.
  - `log/` — chronological phase logs.
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
- Every run that produces paper figures must record software versions in a machine-readable manifest inside the run artefacts (see Artefact Review Cycle).

---

## 5) Phases (high level)

You must work in phases and leave a trace in `docs/log/`.

1) **Bootstrap & scoping**
   - Reconstruct context from repo docs.
   - Fill `docs/log/000_bootstrap.md` (append, don’t overwrite).
   - Update `docs/plan.md` minimally to reflect your refined understanding.

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

## 6) Mandatory loops

### 6.1 Result Review Cycle (scientific validity)
For any new candidate “main” result (figure/table/model), you must perform:

1) **Sanity**
   - Numerical sanity: bounds, missingness, units, invariants.
   - Domain sanity: patterns that must hold in obvious cases (e.g., major cities > remote; buffers around urban-adjacent PAs often brighter than cores; trends not driven by missing years).

2) **Interpretation**
   - Save artefacts to `manuscript/figures/` or `analysis/reports/`.
   - Write interpretation bullets in `docs/interpretation_notes.md`:
     - what it shows,
     - how it supports/refutes the hypothesis,
     - what worries you.

3) **Iteration**
   - Convert worries into concrete follow-up tasks under that result entry.
   - Re-run, regenerate artefacts, and close the loop.

No “ship it” without interpretation notes.

### 6.2 Artefact Review Cycle (engineering validity)
For each Work Package (WP) you complete (see `docs/roadmap.md`), you must:

1) **Build artefacts**
   - Build and verify distributable artefacts for the codebase (at minimum: Python sdist + wheel if Python is primary).
   - Ensure documentation/reference material is buildable (even if minimal).

2) **Canonical run artefact folder**
   - Create (or update) a canonical run folder under `artefacts/` (or `analysis/artefacts/`), containing:
     - run manifest (data versions, checksums, git commit hash, package versions),
     - key outputs produced in that WP (tables/figures),
     - a brief README describing what the run demonstrates.

3) **Sanity inspection**
   - Inspect the WP outputs and record sanity notes in the relevant log + `docs/interpretation_notes.md` (if it’s a result).

4) **Iteration**
   - Fix issues, re-run, and only then mark the WP complete in `docs/roadmap.md`.

---

## 7) Logging, decisions, and context reconstruction

### 7.1 Logs
Maintain chronological log files in `docs/log/` (append-only style). At minimum:
- `000_bootstrap.md`
- plus additional phase logs as you progress (monotonic numbering).

Every substantial work session must end with:
- a short log update,
- and any roadmap checkbox updates.

### 7.2 Decisions
Any non-trivial, costly-to-change choice must be recorded in `docs/decisions.md`:
- dataset choice (night-lights product variant),
- buffer/ring definitions,
- trend estimator and thresholds,
- inclusion/exclusion rules for protected areas,
- output schema choices.

### 7.3 Resume discipline
Assume chat context may be truncated. When resuming after a pause:
1) read `docs/roadmap.md` and pick the first unchecked WP,
2) skim `docs/plan.md`,
3) skim newest files in `docs/log/`,
4) read `docs/decisions.md`,
5) inspect recent git history.

Do not rely on chat history.

---

## 8) Human interaction: how to ask questions

If you must ask the human, do it in `docs/questions_for_human.md`:
- numbered questions,
- 1–3 sentences each,
- include options if relevant,
- state what is blocked.

Then summarise those questions in your next assistant message and pause work on that branch.

---

## 9) Non-goals (guardrails)

- Do not overclaim causality from correlational spatial patterns.
- Do not “tune until significant”; robustness and falsification matter.
- Do not skip negative controls in Layer B.
- Do not bury key assumptions in code; they belong in docs and in the manuscript Methods.

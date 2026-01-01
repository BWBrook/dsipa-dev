# DSIPA-NBS Roadmap (execution queue)

`docs/plan.md` is the brochure (narrative framing).
This file is the GPS (execution). When told to “Follow the roadmap”, you follow this file.

---

## 1) Opening contract

When the human says “Follow the roadmap”:

- You must select the **first unchecked Work Package (WP)** in the **Priority Queue** below and complete it **end-to-end** (code + tests + docs + artefacts).
- Then you must mark it complete (check the box) and move to the next WP.
- You may reorder the Priority Queue **only** if:
  - you record the rationale in `docs/decisions.md`, and
  - you write a log entry in `docs/log/` describing why reordering is necessary.
- If the Priority Queue is empty, stop and report that more work must be promoted into the roadmap.

---

## 2) Work Package Definition of Done (WP‑DoD)

A WP is complete only when all of the following are true:

1) Acceptance criteria are met and tested
- Unit tests and domain sanity checks relevant to the WP pass.
- If the WP introduces a new metric, output, or method, it has explicit sanity checks.

2) Docs updated
At minimum:
- reference/config documentation for any new run parameters or outputs,
- interpretation notes for any new candidate main results,
- and a log update in `docs/log/`.

3) Artefact Review Cycle completed and logged
- Build distributable artefacts for the codebase (at minimum: Python sdist + wheel if Python is primary).
- Produce a canonical run artefact folder with a manifest and evidence outputs.
- Record sanity inspection notes in the log and (if relevant) `docs/interpretation_notes.md`.

4) Schema discipline
- If any structured output schema changes:
  - bump `schema_version`,
  - provide a migration note (even if “no migration possible; rerun required”),
  - and add/adjust regression tests that assert the schema.

5) Output discipline
- If output files change meaningfully:
  - document the change,
  - add a regression/sanity test that would fail if the old behaviour returned.

---

## 3) Priority Queue (strict order)

### Milestone 0.1.x — Bootstrap & scaffolding (aim: runnable skeleton + guardrails)
- [x] **WP0.1 — Repo bootstrap: environments, test harness, and run skeleton**
- [x] **WP0.2 — Logging/decision system operational + roadmap discipline check**

### Milestone 0.2.x — Data provenance & acquisition (aim: reproducible downloads + provenance)
- [x] **WP0.3 — Choose and lock Layer A data sources (CAPAD + night-lights) with provenance**
- [x] **WP0.4 — Smoke-test dataset slice: minimal region pipeline inputs prepared**

### Milestone 0.3.x — Layer A metric engine (aim: correct metrics on smoke-test slice)
- [ ] **WP0.5 — Protected-area geometry processing + stable IDs**
- [ ] **WP0.6 — Radiance summarisation inside PAs + outside buffers (smoke-test)**
- [ ] **WP0.7 — Distance-to-edge penetration profiles (smoke-test)**
- [ ] **WP0.8 — Structured outputs + schema_version + regression tests (smoke-test)**

### Milestone 0.4.x — Layer A national run + sanity (aim: national tables + core sanity)
- [ ] **WP0.9 — National run: Layer A metric tables produced**
- [ ] **WP0.10 — Layer A sanity suite: anchors, missingness, invariants, and sensitivity checks**

### Milestone 0.5.x — Trends, vulnerability, and paper-ready Layer A figures
- [ ] **WP0.11 — Trend estimation + inside-vs-outside retention indices**
- [ ] **WP0.12 — Vulnerability model: predictors of brightening/penetration**
- [ ] **WP0.13 — Paper-ready Layer A figure set + interpretation notes**

### Milestone 0.6.x — Layer B (optional): nocturnal biodiversity signal module
(Only proceed if Layer A is stable and the roadmap has not been reordered to skip required sanity work.)
- [ ] **WP0.14 — Layer B go/no-go: focal taxa + negative controls + bias strategy (decision)**
- [ ] **WP0.15 — Layer B data acquisition + provenance + quality filters**
- [ ] **WP0.16 — Layer B modelling + falsification checks + interpretation**

### Milestone 0.7.x — Manuscript pack + reproducibility release
- [ ] **WP0.17 — Manuscript draft skeleton (Intro/Methods/Results/Limitations) with linked artefacts**
- [ ] **WP0.18 — Reproducibility audit + “one-command” full rerun + release artefacts**

---

## 4) Detailed WP specifications

### WP0.1 — Repo bootstrap: environments, test harness, and run skeleton
Outcome:
A runnable project skeleton exists with pinned environments, a basic test framework, and a non-interactive “run entrypoint” placeholder that will eventually generate the canonical outputs.

Scope:
- In:
  - establish the primary language environment (prefer Python/uv),
  - create minimal package/module structure under `src/`,
  - create initial tests under `tests/` (even if placeholder sanity checks),
  - establish a run entrypoint (name/location documented) without implementing the full pipeline.
- Out:
  - no large data downloads yet,
  - no substantive analysis yet.

Acceptance criteria:
- Environment specification exists and is committed.
- Tests run non-interactively and pass.
- A placeholder run entrypoint executes and writes a small “hello artefact” into a canonical artefact folder (manifest + placeholder output), demonstrating the Artefact Review Cycle mechanics.

Artefact evidence:
- `pyproject.toml` (and lockfile if used)
- `tests/` contains at least one passing test
- `artefacts/` contains a run folder with a manifest and placeholder output

Stop condition:
- You can run tests and produce a minimal artefact folder deterministically.

---

### WP0.2 — Logging/decision system operational + roadmap discipline check
Outcome:
The on-disk memory system is functioning: logs are appended, decisions are recorded, and the roadmap contract is being followed.

Scope:
- In:
  - write/append to `docs/log/000_bootstrap.md` with actual environment info,
  - update `docs/plan.md` status section,
  - add at least one initial decision entry (even if “Python is primary”).
- Out:
  - no dataset choices finalized beyond what is necessary to proceed.

Acceptance criteria:
- `docs/log/000_bootstrap.md` has a complete first entry.
- `docs/decisions.md` has at least one filled decision row.
- `docs/plan.md` status reflects the first unchecked WP.

Artefact evidence:
- Updated docs files committed.

Stop condition:
- A new agent session could resume using only repo docs.

---

### WP0.3 — Choose and lock Layer A data sources (CAPAD + night-lights) with provenance
Outcome:
Layer A data sources are selected explicitly, with provenance recorded and trade-offs documented.

Scope:
- In:
  - choose CAPAD version and document any inclusion rules (e.g., marine included/excluded),
  - choose the night-lights product (annual time series preferred) and document version/variant,
  - record access dates, URLs, and checksums for downloaded metadata or sample files.
- Out:
  - no full national compute yet,
  - no Layer B data choices.

Acceptance criteria:
- `data/README.md` contains provenance entries for CAPAD and night-lights product with checksums for any downloaded files.
- `docs/decisions.md` includes dataset choice decisions (DEC-002 and DEC-003).
- A small “data inventory” report exists summarising expected years/coverage and any known caveats.

Artefact evidence:
- `data/README.md` updated
- `analysis/reports/data_inventory.*` (format flexible)
- Log entry describing the choice

Stop condition:
- A fresh clone could reproduce the same downloads and identify the same versions.

---

### WP0.4 — Smoke-test dataset slice: minimal region pipeline inputs prepared
Outcome:
A small, fixed “triad” smoke-test slice is defined and reproducible: three protected areas chosen to stress the pipeline (urban-edge, peri-urban, remote). 
The slice can be regenerated from raw sources without manual steps and is accompanied by a fast, non-interactive QA harness that produces quick-look maps and strict invariants.

Scope:
- In:
  - Define and document a deterministic triad selection rule (three PAs, deliberately heterogeneous).
  - Produce a processed input index for the triad (stable IDs + minimal geometry + any masks needed).
  - Implement a “triad QA” run that:
    - asserts CRS/units discipline for distance operations,
    - runs geometry validity repair,
    - generates standard buffers and rings,
    - performs one representative spatial join (e.g., roads/settlements, if available at this stage),
    - outputs quick-look maps for human inspection (park + buffers + rings + joined layer).
  - Add tests that lock the triad fixture (IDs/counts) and enforce core invariants (valid geometries; positive areas; ordered rings; deterministic outputs).
- Out:
  - no national run yet.
  - No trend modelling.
  - No attempt to optimise performance beyond “runs fast on a laptop”.

Acceptance criteria:
  - Triad definition is documented, including why each PA is in the set (urban-edge / peri-urban / remote) and the exact selection rule (IDs or rule + tie-break).
  - Triad fixture is reproducible from raw downloads: same IDs, same counts, same CRS.
  - Triad QA harness runs non-interactively and produces:
    - buffers (at least two) and rings (at least three bins) with explicit units in metadata,
    - a manifest recording inputs (checksums/versions), CRS, buffer/ring parameters, and run timestamp.
  - Automated tests assert:
    - triad PA IDs are unique and stable,
    - all processed geometries are valid (or explicitly excluded with recorded reason),
    - no empty geometries, no NaN/Inf numeric outputs,
    - ring bins are ordered and complete,
    - re-running on identical inputs produces identical artefacts (hash match or byte-identical outputs).
  - Human QA artefacts exist:
    - at least one map per triad PA showing park boundary + buffers + rings (and any joined layer if present),
    - a short log note recording what was visually checked and any anomalies found.

Artefact evidence:
  - analysis/reports/smoke_test_triad_definition.* (selection rule + rationale)
  - data/processed/smoke_test_triad_index_<schema_version>.* (IDs + minimal descriptors)
  - analysis/reports/triad_qa_maps/ (3 maps, one per PA, plus a small README/manifest)
  - tests/ includes triad fixture tests + core invariants (CRS/validity/rings order/determinism)
  - docs/log/ entry describing outcomes and any fixes adopted

Stop condition:
  - The triad slice can be regenerated and the QA harness can be run in one command, producing maps + manifest, with tests passing deterministically.

Implementation note (binding on downstream WPs):
  - WP0.5 must use the triad harness to confirm geometry repair + stable IDs.
  - WP0.6 must use the triad harness to confirm buffer definitions and inside/outside summaries.
  - WP0.7 must use the triad harness to confirm ring construction and edge-profile plausibility.
  - WP0.8 must lock the triad output schema and add regression tests that fail on schema drift.

---

### WP0.5 — Protected-area geometry processing + stable IDs
Outcome:
Protected-area geometries are cleaned/validated, stable IDs are established, and basic geometry descriptors are computed.

Scope:
- In:
  - geometry validity checks and fixes (scripted),
  - stable ID policy (documented),
  - compute area/perimeter/shape descriptors.
- Out:
  - radiance summaries not yet required.

Acceptance criteria:
- A processed protected-area table exists with:
  - stable IDs,
  - geometry validity status,
  - basic geometry descriptors.
- A domain sanity report includes counts of invalid geometries and how they were handled.
- Regression tests assert:
  - IDs are unique,
  - areas are positive,
  - no empty geometries in processed set (unless explicitly excluded and recorded).

Artefact evidence:
- `data/processed/pa_geometries_<schema_version>.*`
- `analysis/reports/pa_geometry_qc.*`
- Tests for ID uniqueness and positive area

Stop condition:
- Geometry layer can be consumed by downstream metric computation without ad hoc fixes.

---

### WP0.6 — Radiance summarisation inside PAs + outside buffers (smoke-test)
Outcome:
For the smoke-test slice, compute inside-PA radiance summaries and outside-buffer radiance summaries, with documented buffer definitions.

Scope:
- In:
  - inside summaries (robust stats),
  - at least two outside buffers,
  - missingness quantification.
- Out:
  - distance-to-edge rings not yet required (next WP).

Acceptance criteria:
- A tidy table exists for smoke-test PAs with (PA ID × year × metric) records.
- Domain sanity checks include:
  - distribution plots,
  - at least one anchor comparison (bright vs dark).
- Tests assert:
  - no NaN/Inf,
  - expected columns exist (schema test),
  - missingness metrics are present and within interpretable bounds for the smoke-test.

Artefact evidence:
- `data/processed/pa_radiance_buffers_smoketest_<schema_version>.*`
- `analysis/reports/smoketest_buffers_sanity.*`
- Interpretation note entry for any candidate “main” figure produced here

Stop condition:
- The metric table is stable and interpretable for the smoke-test.

---

### WP0.7 — Distance-to-edge penetration profiles (smoke-test)
Outcome:
Compute inside “distance-to-edge” ring summaries for the smoke-test slice and generate example penetration profiles.

Scope:
- In:
  - ring definitions documented,
  - ring-based radiance summaries per year,
  - at least a few example profile plots.
- Out:
  - no trend estimation yet.

Acceptance criteria:
- A tidy ring-profile table exists (PA ID × year × ring_distance_bin × metric).
- Domain sanity checks include:
  - plausibility review of a small set of example profiles,
  - explicit detection/reporting of pathological profiles (if any) and their cause.
- Tests assert schema and basic invariants (e.g., rings are ordered; bins present).

Artefact evidence:
- `data/processed/pa_edge_profiles_smoketest_<schema_version>.*`
- `analysis/reports/smoketest_edge_profiles.*`
- Interpretation note entry for the profile examples

Stop condition:
- Edge profiles are computed reproducibly and can be explained.

---

### WP0.8 — Structured outputs + schema_version + regression tests (smoke-test)
Outcome:
A stable output schema is established for Layer A smoke-test outputs, with schema_versioning and regression tests.

Scope:
- In:
  - define schema_version,
  - produce schema documentation (columns, units, meaning),
  - add regression tests for schema and basic invariants.
- Out:
  - no national run yet.

Acceptance criteria:
- `schema_version` is implemented and documented.
- Schema tests fail if a required column is missing or renamed.
- A brief migration policy is documented (“rerun required” is acceptable if justified).

Artefact evidence:
- `docs/decisions.md` includes DEC-008
- `analysis/reports/output_schema_reference.*`
- Tests asserting schema and invariants

Stop condition:
- Output format is stable enough to scale to national run.

---

### WP0.9 — National run: Layer A metric tables produced
Outcome:
Compute Layer A metric tables nationally across all included protected areas and all available years.

Scope:
- In:
  - national computation for inside, buffers, and rings,
  - missingness summary nationally,
  - performance notes (without premature micro-optimisation).
- Out:
  - trend estimation not yet required (next WP).

Acceptance criteria:
- National tables exist with documented schema_version.
- A national missingness/coverage report exists (years covered, % PAs with valid data).
- Sanity checks include:
  - national distribution plots,
  - multiple anchor checks across diverse regions.

Artefact evidence:
- `data/processed/pa_radiance_buffers_national_<schema_version>.*`
- `data/processed/pa_edge_profiles_national_<schema_version>.*`
- `analysis/reports/national_layerA_coverage_and_sanity.*`
- Canonical run artefact folder containing these outputs + manifest

Stop condition:
- Layer A national tables are produced reproducibly and pass sanity.

---

### WP0.10 — Layer A sanity suite: anchors, missingness, invariants, and sensitivity checks
Outcome:
A comprehensive Layer A sanity suite exists, including sensitivity checks to major analytic choices.

Scope:
- In:
  - anchor tests (bright/dark),
  - invariants (no impossible values; expected ordering checks),
  - sensitivity checks (at least two): e.g., alternative summary statistic or buffer width.
- Out:
  - trend modelling (next WP).

Acceptance criteria:
- A “sanity dashboard” report exists summarising:
  - anchors,
  - missingness,
  - sensitivity outcomes,
  - any unresolved anomalies.
- Sanity suite is automated (repeatable, non-interactive).
- Any anomalies are either resolved or explicitly documented with mitigation.

Artefact evidence:
- `analysis/reports/layerA_sanity_dashboard.*`
- Tests/sanity scripts executed in CI-style runs
- Interpretation notes updated if any key result changed

Stop condition:
- You can defend Layer A tables as technically and ecologically plausible.

---

### WP0.11 — Trend estimation + inside-vs-outside retention indices
Outcome:
Compute robust temporal trends per protected area and derive interpretable “dark-sky integrity” and retention metrics.

Scope:
- In:
  - trend estimation per PA for core metrics,
  - uncertainty or stability diagnostics,
  - retention index comparing inside vs outside trends.
- Out:
  - vulnerability predictors (next WP).

Acceptance criteria:
- Trend tables exist with documented units and estimator choice.
- Domain sanity includes checks against:
  - implausible national-wide step changes,
  - trends driven by missing years.
- At least one candidate main figure is produced (trend distribution or hotspot map) with interpretation notes.

Artefact evidence:
- `data/processed/pa_trends_<schema_version>.*`
- `analysis/reports/trends_methods_and_sanity.*`
- `manuscript/figures/` contains at least one trend figure + interpretation note entry

Stop condition:
- Trend results are coherent, robust, and interpretable enough for paper Results.

---

### WP0.12 — Vulnerability model: predictors of brightening/penetration
Outcome:
An interpretable model identifies which protected-area attributes are associated with brightening/penetration risk metrics.

Scope:
- In:
  - define response variables (risk metrics),
  - define predictors (geometry/context) and document them,
  - fit interpretable models and report uncertainty/robustness.
- Out:
  - no Layer B yet.

Acceptance criteria:
- A ranked list of protected areas by risk metric exists.
- Model diagnostics and robustness checks are reported (e.g., sensitivity to outliers, alternative model form).
- At least one candidate paper figure/table is produced with interpretation notes.

Artefact evidence:
- `analysis/reports/vulnerability_model_report.*`
- `data/processed/pa_risk_rankings_<schema_version>.*`
- `manuscript/figures/` includes a vulnerability figure/table output

Stop condition:
- You can state a cautious, defensible set of predictors and limitations.

---

### WP0.13 — Paper-ready Layer A figure set + interpretation notes
Outcome:
Layer A is “paper-ready”: a coherent figure set and accompanying interpretation notes exist.

Scope:
- In:
  - finalise the minimum Layer A figure set (baseline + trends + edge profiles + vulnerability),
  - ensure all figures are reproducible from the pipeline,
  - write interpretation notes for each.
- Out:
  - manuscript text (next milestone).

Acceptance criteria:
- `manuscript/figures/` contains the agreed minimal figure set with stable filenames.
- Each figure has an entry in `docs/interpretation_notes.md`.
- A short “Layer A story so far” summary exists in the Summary section of interpretation notes.

Artefact evidence:
- Figures + a figure inventory report (`analysis/reports/figure_inventory.*`)
- Updated interpretation notes

Stop condition:
- Layer A could be written up without additional computation.

---

### WP0.14 — Layer B go/no-go: focal taxa + negative controls + bias strategy (decision)
Outcome:
A documented, conservative Layer B design exists (or a decision to stop at Layer A).

Scope:
- In:
  - choose focal taxa (likely bats) and negative controls,
  - decide bias-control approach and what constitutes “success” vs “too confounded”.
- Out:
  - no heavy data downloads until design is explicit.

Acceptance criteria:
- A clear go/no-go decision is recorded in `docs/decisions.md`.
- The Layer B analysis plan is appended to `docs/plan.md` status section (briefly).
- “Falsification criteria” are explicit (what outcome would be interpreted as sampling bias).

Artefact evidence:
- `docs/decisions.md` updated (DEC-009)
- `analysis/reports/layerB_design_note.*`

Stop condition:
- Layer B has a written design with clear stopping rules.

---

### WP0.15 — Layer B data acquisition + provenance + quality filters
Outcome:
Layer B occurrences data are acquired reproducibly with documented filters and quality summaries.

Scope:
- In:
  - download occurrences via scripted queries,
  - document filters (date range, coordinate quality, basisOfRecord, etc.),
  - generate QC summaries (counts by year/region).
- Out:
  - no modelling yet.

Acceptance criteria:
- `data/README.md` includes Layer B data provenance and checksums.
- A QC report exists summarising record counts, missingness, and spatial coverage.
- Tests assert expected fields exist and that the filters were applied.

Artefact evidence:
- `data/raw/` and `data/processed/` contain the occurrence dataset products (or references if too large)
- `analysis/reports/layerB_data_qc.*`

Stop condition:
- Occurrence data are ready for bias-aware modelling.

---

### WP0.16 — Layer B modelling + falsification checks + interpretation
Outcome:
Layer B models are fit and interpreted conservatively, with explicit negative-control and falsification checks.

Scope:
- In:
  - fit bias-aware models linking ALAN metrics to relative occurrence signals,
  - run negative controls,
  - run sensitivity analyses.
- Out:
  - no overclaiming; result can be “no defensible signal” and still be success.

Acceptance criteria:
- A modelling report exists that includes:
  - focal taxa results,
  - negative controls,
  - sensitivity analyses,
  - an explicit interpretation paragraph stating what can/cannot be concluded.
- Figures/tables (if any) are added to `manuscript/figures/` and interpretation notes updated.

Artefact evidence:
- `analysis/reports/layerB_modelling_report.*`
- `manuscript/figures/` contains any Layer B figures (if used)
- Interpretation notes include Layer B entry(ies)

Stop condition:
- Layer B conclusion is clear and defensible (positive or null).

---

### WP0.17 — Manuscript draft skeleton (Intro/Methods/Results/Limitations) with linked artefacts
Outcome:
A manuscript skeleton exists with methods and results grounded in produced artefacts.

Scope:
- In:
  - write Introduction framing,
  - Methods (data, metrics, trend estimation, modelling),
  - Results (Layer A; Layer B if included),
  - Limitations and future work.
- Out:
  - no journal formatting polish yet.

Acceptance criteria:
- Manuscript text files exist under `manuscript/text/`.
- Every key claim in Results points to a specific table/figure path in the repo.
- Limitations include remote-sensing caveats and presence-only caveats (if Layer B attempted).

Artefact evidence:
- `manuscript/text/manuscript_draft.md` (or similar)
- Figure/table inventory referenced in text

Stop condition:
- Manuscript is coherent and traceable to artefacts.

---

### WP0.18 — Reproducibility audit + “one-command” full rerun + release artefacts
Outcome:
A full reproducibility audit is completed and the project can be rerun from scratch to regenerate core outputs.

Scope:
- In:
  - confirm end-to-end pipeline reproducibility,
  - confirm schema_versioning and migrations (if any) are handled,
  - ensure canonical artefact run exists for the final results.
- Out:
  - journal submission steps.

Acceptance criteria:
- A reproducibility report exists stating:
  - what command(s) rerun the pipeline,
  - expected runtime class (rough order-of-magnitude is fine),
  - how to verify outputs match (hashes or key summary stats).
- Final canonical artefact folder exists with:
  - manifest,
  - final tables,
  - final figures.
- Tests cover core invariants and output schemas.

Artefact evidence:
- `analysis/reports/reproducibility_audit.*`
- `artefacts/final_*` folder with manifest and evidence outputs

Stop condition:
- A fresh clone on the same platform can regenerate the key paper artefacts.

---

## 5) Milestone / review gates (when to request PI review ZIP)

Request a PI review ZIP when any of the following is reached:

- Gate A (Layer A paper-ready): after completing **WP0.13**.
- Gate B (Layer B concluded): after completing **WP0.16** (whether positive or null).
- Gate C (manuscript + reproducibility): after completing **WP0.18**.

Also request a PI review if:
- you hit a blocker requiring a major conceptual change,
- or sanity checks fail repeatedly and the cause is unclear.

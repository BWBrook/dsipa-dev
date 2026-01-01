# 000_bootstrap log (DSIPA-NBS)

Keep entries chronological; append rather than overwrite.

- Date/time (UTC): 2026-01-01 04:29 UTC
- Agent/environment: Codex CLI (GPT-5), Linux x86_64, Python 3.12.3, uv 0.9.13
- Context (one paragraph): DSIPA-NBS targets a national, reproducible assessment of artificial light at night (ALAN) inside Australian protected areas and their surrounding buffers/rings, with optional downstream tests for a conservative nocturnal biodiversity signal. The immediate focus is to scaffold a Python/uv environment, establish the run/artefact mechanics, and prepare for explicit dataset choices (CAPAD + night-lights) with provenance.

---

## 1) Initial understanding (agent-written)

- Primary question (Layer A): How has ALAN inside Australian protected areas changed over time, and is any change consistent with boundary encroachment from surrounding landscapes?
- Secondary question (Layer B; optional): Is there a conservative, bias-aware nocturnal biodiversity occurrence signal consistent with ALAN exposure near protected areas?
- What success looks like for Layer A: Reproducible national tables/figures of inside, buffer, and edge-profile radiance trends with clear sanity checks, interpretable metrics, and documented uncertainties.
- Conditions under which Layer B will be attempted: Only after Layer A is stable and passes sanity/interpretation cycles; Layer B must include explicit negative controls and bias controls.

---

## 2) Proposed data sources (to be validated)

- Protected areas (CAPAD): Candidate dataset; exact version/access date/URL to be chosen in WP0.3.
- Night lights product: Candidate annual time series (e.g., VIIRS DNB composites); final choice to be recorded in WP0.3 with provenance.
- Optional covariates: To be defined if promoted in roadmap (e.g., land/sea mask).
- Optional biodiversity data (ALA): Atlas of Living Australia occurrences for focal nocturnal taxa (optional Layer B).

Record final choices in `docs/decisions.md` and full provenance in `data/README.md`.

---

## 3) Proposed metric framework (Layer A)

Define the planned outputs in words (not code):

- Inside-PA radiance summaries: Median/trimmed mean radiance per PA per year (robust statistics; outlier handling documented).
- Outside buffers (encroachment pressure): Radiance summaries in at least two buffer distances outside PA boundaries.
- Inside rings (distance-to-edge penetration profile): Radiance summaries in multiple distance-to-edge bins inside PA.
- Trend estimators: Robust per-PA slope estimates with uncertainty diagnostics.
- Core “dark-sky integrity” indices: Inside-vs-outside trend retention metrics and edge-penetration indicators.

---

## 4) Planned analysis grid (staged execution)

- Smoke-test region(s) for rapid iteration (small subset): Deterministic triad of PAs spanning urban-edge, peri-urban, remote (defined in WP0.4).
- Full national run plan: Scale the triad-validated pipeline to all eligible PAs and all years in the chosen night-lights product.
- Expected runtime/compute risks and mitigation: Raster × polygon aggregation could be heavy; mitigate via tiling, batching, and a validated smoke-test harness before national runs.

---

## 5) Planned validation strategy

- Numerical/geospatial sanity checks: No NaN/Inf, valid geometries post-repair, missingness quantified, deterministic outputs.
- Domain sanity checks (bright vs dark anchors, inside vs outside logic): Major cities brighter than remote interiors; buffers often brighter than cores near development.
- Sensitivity checks (buffer widths, summary stats, alternative product if feasible): Compare alternative buffer widths and summary statistics; consider a second product if feasible.
- Planned negative controls for Layer B (if attempted): Diurnal taxa as negative controls; target-group background sampling to probe observer bias.

---

## 6) Immediate next actions (3–7 items)

1. Complete WP0.1–WP0.2 bootstrap deliverables (env, tests, artefact run, logs/decisions).
2. Select and document CAPAD + night-lights sources with provenance (WP0.3).
3. Draft a minimal data-inventory report for the chosen products (WP0.3 artefact).

---

## 7) Bootstrap execution notes (WP0.1–WP0.2)

- Actions: created Python/uv project skeleton, dsipa package, run entrypoint, tests, README quickstart, and repo map snapshot.
- Artefacts: `artefacts/wp0_1_bootstrap/` (MANIFEST.json + placeholder.txt + README.txt).
- Build artefacts: `dist/dsipa_nbs-0.1.0.tar.gz`, `dist/dsipa_nbs-0.1.0-py3-none-any.whl`.
- Tests: `uv run pytest` (2 passed).
- Sanity verdict: pass (bootstrap outputs created deterministically; manifest captured environment and git state).

Also update:
- `docs/plan.md` (narrative plan),
- `docs/roadmap.md` (work queue status),
- and create/append a new log file if entering a new phase.

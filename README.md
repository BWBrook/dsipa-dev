# DSIPA-NBS: Dark-Sky Integrity of Protected Areas & Nocturnal Biodiversity Signals (Australia)

This repository investigates a conservation question with a strong “dark-sky” angle:

How has artificial light at night changed inside Australian protected areas over time, how much of that change looks like boundary/encroachment pressure, and (optionally) can we detect a conservative nocturnal biodiversity occurrence signal consistent with ALAN exposure?

The core of the project is a national-scale integration of:
- Australian protected area polygons (CAPAD), and
- a consistent night-lights remote-sensing time series.

A secondary module (optional) explores whether nocturnal biodiversity occurrence records show a defensible “light signature” when analysed with explicit bias controls and negative controls.

---

## What this repo is for

This is an “AI for Science” autonomy experiment:
- Codex CLI is the hands-on agent implementing the pipeline, tests, figures, and manuscript draft.
- The human scientist is hands-off, providing occasional answers to targeted questions and uploading repo ZIPs for PI-style review.
- The workflow is designed to be reproducible, auditable, and scientifically interpretable.

---

## How the project is organised

- `docs/plan.md` — narrative overview (what/why).
- `docs/roadmap.md` — execution queue (what happens next and what “done” means).
- `docs/workflow.md` — Result Review Cycle + Artefact Review Cycle (mandatory).
- `docs/decisions.md` — irreversible/costly choices and rationale.
- `docs/interpretation_notes.md` — what key outputs mean; surprises; follow-ups.
- `docs/log/` — chronological log of work phases.
- `data/` — raw and processed datasets (with provenance recorded in `data/README.md`).
- `data/raw/ala_occurrences/` — Layer B ALA downloads (ignored by git).
- `data/processed/layerB/` — Layer B processed occurrence tables (ignored by git).
- `src/` — reusable code.
- `analysis/` — reports and pipeline orchestration.
- `analysis/state_runs/` — per-state Layer A outputs for performance-friendly runs (merged later; ignored by git).
- `manuscript/` — paper draft and figures.
- `tests/` — automated tests and domain sanity checks.

Note: Large derived outputs (national tables, large GPKGs, and `artefacts/`) are not tracked in git. They are regenerated via the pipeline and archived to Zenodo for paper release. Smoke-test outputs remain in-repo to support fast regression tests.

Zenodo helper:
```bash
analysis/zenodo_release_checklist.sh
```
This writes a checklist + SHA256 manifest to `analysis/reports/zenodo_release_checklist_YYYY-MM-DD.md`.

---

## Quickstart (bootstrap)

This repo targets Python 3.12 and is managed with `uv`.

Setup (recommended):
```bash
uv venv
uv pip install -e ".[dev]"
```

Run the bootstrap entrypoint (writes a placeholder artefact + manifest):
```bash
dsipa-run
```

If you prefer not to install the package yet:
```bash
PYTHONPATH=src/python python -m dsipa.run
```

Artefacts are written to `artefacts/wp0_1_bootstrap/`.

Run tests:
```bash
pytest
```

Layer B data acquisition (ALA occurrences):
```bash
ALA_DOWNLOAD_EMAIL=you@example.org ALA_DOWNLOAD_REASON="research" \\
  uv run python -m dsipa.layerB_data --download-retries 5
```

Layer B outputs are large and ignored by git; see `analysis/reports/layerB_data_qc.md` for QC summaries.

Layer B QC hardening (licensing + scope/exposure checks):
```bash
uv run python -m dsipa.layerB_qc --groups microbats,diurnal_birds
```

Layer B modelling (WP0.16, provider-matched primary):
```bash
uv run python -m dsipa.layerB_model --provider dr368 --skip-artefact
uv run python -m dsipa.layerB_model --artefact-only
```
If the multi-provider sensitivity run is too slow, you can subsample passerines:
```bash
uv run python -m dsipa.layerB_model --provider dr368 --sensitivity-sample-rate 0.1 --skip-artefact
```

---

## Collaboration and review

If you are running Codex in this repo, follow `docs/roadmap.md` strictly.
When a milestone review gate is reached, zip the repo and send it for PI review.

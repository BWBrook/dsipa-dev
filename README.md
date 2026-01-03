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
- `src/` — reusable code.
- `analysis/` — reports and pipeline orchestration.
- `analysis/state_runs/` — per-state Layer A outputs for performance-friendly runs (merged later; ignored by git).
- `manuscript/` — paper draft and figures.
- `tests/` — automated tests and domain sanity checks.

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

---

## Collaboration and review

If you are running Codex in this repo, follow `docs/roadmap.md` strictly.
When a milestone review gate is reached, zip the repo and send it for PI review.

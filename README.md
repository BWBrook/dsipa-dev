# DSIPA-NBS: Dark-Sky Integrity of Protected Areas & Nocturnal Biodiversity Signals (Australia)

**Current status: corrected spatial candidate independently approved for private reading (19 September 2026).** The independent Astra/max review found errors in surrounding buffers, inward bands and coastal masking. Whole-reserve observations remain unchanged. The corrected route is documented in [spatial reproduction](docs/spatial_reproduction_20260919.md); the older Goal 012 runner and reference contract describe the historical baseline, not the current manuscript's surrounding or band results. Previous private reading bundles remain preserved. Optional numerical Layer B results are excluded from the active candidate because original occurrence inputs could not be recovered to verify a sampling repair. Source code and historical results remain available for research. No public release is authorised.

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
- `settings/build.yaml` — local `makedoc` manuscript build profiles.
- `references/` and `csl/` — manuscript bibliography and citation style used by `makedoc`.
- `tests/` — automated tests and domain sanity checks.

Note: Large derived outputs (national tables, large GPKGs, and `artefacts/`) are not tracked in git. Nine historical baseline national Layer A outputs are publicly archived as Zenodo Dataset version `0.3.0` under CC BY 4.0 at <https://doi.org/10.5281/zenodo.21524637>; raw and row-level ALA data, Layer B payloads, and unlisted files are excluded. The source GitHub repository remains private and is not a public access route. Release provenance is recorded in `analysis/reports/final_release_manifest.md`; smoke-test outputs remain in-repo for fast regression tests.

The nine processed national Layer A outputs are already cited through the
Zenodo DOI above. Use `analysis/reports/final_release_manifest.md` and the
Goal 014/015 receipts for release provenance; do not regenerate a new archive
checklist unless a future release goal explicitly asks for one.

Deep-server evidence reconciliation:
```bash
analysis/deep_server_tmux_run.sh --mode evidence
```
This starts a detached `tmux` run on `deep-server-ts`, inventories the large
ignored evidence files in the synced remote checkout, and refreshes
`analysis/reports/evidence_reconciliation.*` plus
`analysis/reports/reproducibility_audit.md`.

For longer production reruns on `deep-server`, keep work under tmux and tune
the worker count explicitly. The default remote checkout is the Mac-synced
scratch tree at `/data/codex/repos/dsipa-dev-mac-sync`:
```bash
analysis/deep_server_tmux_run.sh --mode full --workers 12
```
Remote logs are written under `/data/codex/scratch/dsipa/<RUN_ID>/`, with
copied evidence artefacts under `/data/codex/artifacts/dsipa/<RUN_ID>/`.

If you need to run the current dirty Mac working tree on `deep-server`, sync it
to a scratch remote checkout first:
```bash
analysis/sync_to_deep_server.sh
analysis/deep_server_tmux_run.sh --mode custom --command 'uv run python -m pytest -rs'
```

---

## Quickstart (bootstrap)

This repo targets Python 3.12 and is managed with `uv`. On the Mac mini, use the
checked-in bootstrap wrapper so migrated WSL virtual environments are rebuilt
cleanly:

```bash
make bootstrap
make readiness
```

`make readiness` probes the live `deep-server-ts` route by default; use
`CHECK_SSH=0 make readiness` for local-only checks.

Run the bootstrap entrypoint (writes a placeholder artefact + manifest):
```bash
uv run dsipa-run
```

If you prefer not to install the package yet:
```bash
uv run python -m dsipa.run
```

Artefacts are written to `artefacts/wp0_1_bootstrap/`.

Run tests:
```bash
make fast
make test
```

`make fast` is the proportional offline gate for routine engineering changes:
imports plus targeted deterministic unit/domain/fixture tests. The broader
release gate is decision-relevant only and uses existing commands such as
`make test`, `make build`, output/reproducibility checks, manuscript checks,
and authorized remote evidence runs when the goal packet calls for them.

Build the Python package:
```bash
make build
```

Build/check the manuscript through the local `makedoc` checkout at
`/Users/bwbrook/work/makedoc`:
```bash
make ms-validate
make ms-check
make ms-build
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

The current editorial review iteration is in
`build/final_read/editorial_20261018_r2/`; its argument and evidence checks are in
`analysis/reports/editorial_redevelopment_20261018.md`. The second rewrite integrates the independently replayed
additive budget and Kosciuszko example; Claude's next critique is pending; its canonical snapshot is
`artefacts/editorial_20261018_r2/`. Manuscript builds isolate LaTeX scratch in
`build/.makedoc-latex/<profile>/` to avoid cross-project cache collisions.

The accepted September reading documents remain in `build/final_read/spatial_20260919/`; the
private source/evidence package is `artefacts/spatial_candidate_20260919/`.
The independent acceptance memo is
`analysis/reports/spatial_correction_acceptance_review_20260919.md`; archive
hashes and verification are in `analysis/reports/spatial_candidate_seal_20260919.json`.
Earlier 18 September bundles remain preserved as historical versions.

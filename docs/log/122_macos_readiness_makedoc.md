# 122 - Mac readiness and makedoc wiring

Date: 2026-05-29

Agent/environment: Codex on Barry's Mac mini, repo `/Users/bwbrook/papers/dsipa-dev`, base commit `dab3ddb`.

Scope:

- Harden the migrated WSL checkout for macOS development.
- Wire manuscript assembly through the local external `makedoc` checkout at `/Users/bwbrook/work/makedoc`.
- Make the Mac mini ready to dispatch DSIPA work to `deep-server` over the live Tailscale route.

Changes:

- Rebuilt the migrated `.venv` with `uv` and CPython 3.12.13 for macOS arm64.
- Pinned the project contract to Python `>=3.12,<3.13` and added `.python-version`.
- Added `analysis/bootstrap_macos.sh`, `analysis/check_macos_readiness.py`, `analysis/makedoc.sh`, `analysis/sync_to_deep_server.sh`, and top-level `Makefile` targets for bootstrap, readiness, tests, builds, manuscript checks, and HPC sync.
- Added repo-local manuscript build inputs:
  - `settings/build.yaml`
  - `manuscript/authors.yaml`
  - `manuscript/text/references.md`
  - `references/refs.yaml`
  - `csl/cambridge-university-press-author-date-cambridge-a.csl`
- Converted manuscript author-year citations to Pandoc citekeys where the seeded bibliography supported it.
- Updated Mac/HPC notes in `README.md`, `docs/plan.md`, `docs/stage_overview.md`, `docs/stage2_layerA_hardening_plan.md`, and `docs/decisions.md`.

HPC route:

- Direct campus SSH to `deep-server` timed out from the Mac mini.
- Tailscale aliases `deep-server-ts` and `utas-ubuntu` both reached the campus server.
- The default DSIPA remote route is now `deep-server-ts`.
- The default scratch checkout is `/data/codex/repos/dsipa-dev-mac-sync`.
- Synced the current Mac working tree to that scratch checkout and prepared the remote `uv` environment with Python 3.12.

Validation:

- `make readiness` passed; report written to `analysis/reports/macos_readiness.md`, including the live `deep-server-ts` route and remote scratch checkout.
- `make test` passed: 34 passed, 9 skipped for absent full national outputs that require pipeline regeneration.
- `make build` passed and built sdist/wheel under `/tmp/dsipa-build`.
- `make ms-check` passed, including makedoc config validation, 28 makedoc tests, manuscript lint, reference audit, author metadata injection, and final build check.
- `pdfinfo build/draft/dsipa_draft.pdf` reported a 36-page A4 PDF.
- `build/draft/dsipa_draft.pdf`, `build/draft/dsipa_draft.docx`, and `build/draft/dsipa_draft_build_manifest.json` were generated successfully.
- Remote scratch checkout `/data/codex/repos/dsipa-dev-mac-sync` was synced, `uv sync --python 3.12 --extra dev` was refreshed there, and DSIPA/geospatial imports passed.
- `git diff --check` passed.

Notes:

- The seeded bibliography is sufficient for current manuscript builds, but final reference curation is still needed before submission.
- The remote scratch copy is intended for dirty working-tree validation and data-analysis runs; durable publication state should still be tied back to clean commits and recorded artefacts.

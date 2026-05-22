# 108 remote harness and evidence reconciliation

- Date/time (UTC): 2026-05-14 06:43 UTC
- Agent/environment: Codex on WSL control plane; remote evidence run on `deep-server`
- Scope: create a tmux-first deep-server harness and reconcile the large ignored evidence outputs before addressing further science critiques.

## Actions

- Added `analysis/deep_server_tmux_run.sh` to start DSIPA runs under remote `tmux` on `deep-server`.
- Added `src/python/dsipa/evidence_reconciliation.py` to inventory required evidence files, verify pinned checksums, and refresh the reproducibility audit.
- Added tests for the evidence inventory status and markdown rendering.
- Installed standalone `uv` 0.11.14 into `/home/bwbrook/.local/bin` on `deep-server`.
- Created the deep-server run lanes required by the harness:
  - `/data/codex/repos`
  - `/data/codex/scratch/dsipa`
  - `/data/codex/artifacts/dsipa`
  - `/data/codex/tmp`
- Ran the evidence reconciliation through `tmux` using:

```bash
analysis/deep_server_tmux_run.sh --mode evidence --run-id 20260514T072832Z-evidence6 --replace
```

## Evidence

- Remote run directory: `/data/codex/scratch/dsipa/20260514T072832Z-evidence6`
- Remote artefact directory: `/data/codex/artifacts/dsipa/20260514T072832Z-evidence6`
- Remote log: `/data/codex/scratch/dsipa/20260514T072832Z-evidence6/run.log`
- Reconciled reports copied back into the repo:
  - `analysis/reports/evidence_reconciliation.md`
  - `analysis/reports/evidence_reconciliation.json`
  - `analysis/reports/reproducibility_audit.md`

Evidence reconciliation summary:

- Expected files: 38
- Present files: 38
- Checksum-verified files: 38
- Missing required files: 0
- Checksum mismatches: 0
- Artefact manifests found: 28

## Commands run

```bash
scripts/check-access.sh deep-server
scripts/deep-server/inventory.sh
python3 -m pip install --user uv
curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --no-modify-path
analysis/deep_server_tmux_run.sh --mode evidence --run-id 20260514T072832Z-evidence6 --replace
uv run pytest tests/python/test_evidence_reconciliation.py -q
uv run python -m dsipa.evidence_reconciliation --output-md /tmp/dsipa_evidence.md --output-json /tmp/dsipa_evidence.json
uv run pytest -rs
uv build --out-dir /tmp/dsipa-build-harness
(cd /home/bwbrook/work/nectar && scripts/validate-repo.sh)
```

Notes:

- `python3 -m pip install --user uv` failed as expected under Ubuntu's externally managed Python policy, so the standalone `uv` installer was used instead.
- The ALA licence ledger checksum is computed after CRLF-to-LF normalization because embedded citation-field line endings vary across checkouts while the Git blob remains equivalent.
- The refreshed reproducibility audit records `f73156272104ed16b0506617fc423e5c6478f50e` and a dirty working tree because this harness/evidence work is not yet committed.
- The external archive/Zenodo DOI step remains open; this pass verifies the remote evidence snapshot, not public redistribution.
- `docs/roadmap.md` already has all Work Packages checked, so no roadmap checkbox changed in this pass.

# Stage 0 plan: lock the baseline

Status: draft detailed plan, created 2026-05-15.

## Objective

Create a clean, auditable baseline before any new science or manuscript hardening begins. Stage 0 locks three things:

- the current manuscript draft baseline at commit `cc847f0` (`Draft manuscript sections and source scaffolds`);
- the remote `deep-server` harness and evidence-reconciliation work currently sitting uncommitted on top of that manuscript draft; and
- the current complete evidence snapshot, including the `deep-server` run `20260514T072832Z-evidence6`.

## Non-goals

- Do not revise the manuscript prose.
- Do not add new analyses, figures, tables, or scientific claims.
- Do not start the critique-resolution matrix beyond identifying it as the next stage.
- Do not modify user-created or ambiguous files, including `docs/ref_doi.txt`, until ownership and intended use are clear.
- Do not run the full production pipeline unless Stage 0 validation exposes a baseline-integrity problem that requires it.

## Current known state

As of 2026-05-15:

- Local DSIPA `main` is at `cc847f0`, which includes the rough manuscript draft and source scaffolds.
- The earlier remote-harness/evidence-reconciliation work is present but uncommitted in the local DSIPA checkout.
- The `deep-server` DSIPA checkout also has the harness/evidence files copied into its working tree so the evidence run could execute there.
- The `nectar` control-plane repo has uncommitted documentation updates recording the DSIPA `deep-server` integration.
- `docs/ref_doi.txt` is untracked in DSIPA and should be treated as user-owned/ambiguous until inspected and confirmed.

## Work packages

### S0.1 Working-tree triage and ownership

Purpose: make sure we know exactly what is ours, what is the user's, and what belongs to another repository.

Actions:

- Run `git status --short --branch` in `/home/bwbrook/papers/dsipa-dev`.
- Run `git status --short --branch` in `/home/bwbrook/work/nectar`.
- Classify each dirty/untracked file as one of:
  - Stage 0 harness/evidence work;
  - user manuscript/source material;
  - user/ambiguous material requiring no-touch handling;
  - generated scratch that should not be committed.
- Inspect `docs/ref_doi.txt` read-only if needed to classify it, but do not edit or stage it without explicit confirmation.

Validation gate:

- A Stage 0 closeout note lists all remaining dirty/untracked files and their ownership.
- No user-owned or ambiguous file is staged or edited accidentally.

### S0.2 Validate the DSIPA harness/evidence bundle

Purpose: prove that the Stage 0 harness and reconciliation code are correct before committing them.

Actions:

- Review the DSIPA diff for:
  - `analysis/deep_server_tmux_run.sh`;
  - `src/python/dsipa/evidence_reconciliation.py`;
  - `tests/python/test_evidence_reconciliation.py`;
  - `analysis/reports/evidence_reconciliation.*`;
  - `analysis/reports/reproducibility_audit.md`;
  - `README.md`, `docs/decisions.md`, and `docs/log/108_remote_harness_evidence_reconciliation.md`.
- Confirm the harness still writes run-local files under `/data/codex/scratch/dsipa/<RUN_ID>` and durable copied reports under `/data/codex/artifacts/dsipa/<RUN_ID>`.
- Confirm the evidence reconciler documents the CRLF-normalized checksum rule for the ALA licence ledger.

Required commands:

```bash
bash -n analysis/deep_server_tmux_run.sh
uv run pytest tests/python/test_evidence_reconciliation.py -q
uv run python -m dsipa.evidence_reconciliation --output-md /tmp/dsipa_evidence.md --output-json /tmp/dsipa_evidence.json
uv run pytest -rs
uv build --out-dir /tmp/dsipa-build-harness
```

Validation gate:

- Shell syntax passes.
- Evidence-reconciliation tests pass.
- Local evidence smoke has no checksum mismatches; missing heavy outputs are expected in the WSL checkout.
- Full local tests pass with only expected skips for missing heavy national outputs.
- Package sdist and wheel build successfully.

### S0.3 Validate the remote evidence snapshot

Purpose: ensure the complete evidence snapshot is available and reconciled on `deep-server`.

Actions:

- Confirm `deep-server` can still see:
  - `/data/codex/scratch/dsipa/20260514T072832Z-evidence6/run.log`;
  - `/data/codex/artifacts/dsipa/20260514T072832Z-evidence6/evidence_reconciliation.md`;
  - `/data/codex/artifacts/dsipa/20260514T072832Z-evidence6/evidence_reconciliation.json`;
  - `/data/codex/artifacts/dsipa/20260514T072832Z-evidence6/reproducibility_audit.md`.
- Confirm `analysis/reports/evidence_reconciliation.json` reports:
  - expected files = 38;
  - present files = 38;
  - checksum-verified files = 38;
  - missing required files = 0;
  - checksum mismatches = 0;
  - artefact manifests found = 28.
- Do not rerun the remote evidence reconciliation unless a file is missing, stale, or inconsistent.

Validation gate:

- Remote artefacts exist in both scratch and durable artefact locations.
- The repo copy of `analysis/reports/evidence_reconciliation.*` matches the final remote evidence run.
- Any remote working-tree dirt is explained by the uncommitted Stage 0 harness/evidence files, not by untracked data drift.

### S0.4 Commit and synchronize Stage 0 baseline work

Purpose: move from a useful but dirty working state to a stable baseline that future stages can trust.

Recommended commit separation:

- DSIPA commit: remote harness, evidence reconciler, refreshed reports, Stage 0 planning docs, and DSIPA log/docs updates.
- Nectar commit: compute-control handoff documenting the DSIPA `deep-server` integration.

Actions:

- Stage only files classified as Stage 0 work.
- Exclude `docs/ref_doi.txt` unless the user explicitly says it should be included.
- Commit DSIPA changes with a message that clearly names the baseline lock, for example:

```text
Add stage-gated baseline and deep-server evidence harness
```

- Commit `nectar` documentation separately if the user wants the compute-control repo kept in sync.
- Push only after the local commits are reviewed and the user confirms that pushing is desired.

Validation gate:

- DSIPA has a clean working tree except deliberately parked user-owned files.
- `nectar` has a clean working tree or a clearly documented parked state.
- Local DSIPA `HEAD` contains the Stage 0 plan and evidence-harness commit.
- If pushed, `origin/main` or the chosen branch points to the same reviewed commit.

### S0.5 Capture the manuscript baseline

Purpose: preserve the rough manuscript as the narrative starting point before Stage 1 starts critique mapping.

Actions:

- Record manuscript baseline commit `cc847f0`.
- Note the manuscript files added or changed by that commit:
  - `manuscript/text/manuscript_draft.md`;
  - `manuscript/text/figures.md`;
  - `manuscript/text/tables.md`;
  - `manuscript/text/supplementary_figures.md`;
  - `manuscript/text/supplementary_tables.md`;
  - `docs/literature_review.md`;
  - manuscript-related log files `109` through `118`.
- Record the current narrative diagnosis without rewriting the draft:
  - strong on caution, feasibility, and methods;
  - not yet decisive enough on Layer A management implications;
  - placeholder tables still need to become evidence-bearing outputs;
  - Layer B needs clearer "secondary and conservative" positioning after Layer A is hardened.

Validation gate:

- The Stage 0 closeout names the manuscript baseline commit and files.
- No manuscript prose changes occur during Stage 0.

### S0.6 Stage 0 closeout and signoff

Purpose: make the transition to Stage 1 deliberate.

Actions:

- Add or update the Stage 0 log entry.
- Report:
  - final git state for DSIPA;
  - final git state for `nectar`;
  - validation commands and outcomes;
  - remote evidence run ID and summary;
  - parked/untouched files;
  - recommendation on whether Stage 1 can start.
- Wait for explicit user signoff before writing the detailed Stage 1 plan.

Validation gate:

- Stage 0 is not complete until the user accepts the closeout and agrees that Stage 1 can begin.

## Stage 0 definition of done

Stage 0 is done only when all of the following are true:

- DSIPA's Stage 0 harness/evidence/planning changes are reviewed and either committed or deliberately parked.
- `deep-server` evidence run `20260514T072832Z-evidence6` is confirmed complete and durable.
- Local tests and build pass, with only expected large-output skips.
- `nectar` documentation changes are validated and either committed or deliberately parked.
- The rough manuscript baseline at `cc847f0` is recorded as the narrative starting point.
- `docs/ref_doi.txt` is either classified by the user or explicitly parked untouched.
- A concise Stage 0 closeout note has been delivered and accepted.

## Move/no-move rule

Do not proceed to Stage 1 if any of these are true:

- DSIPA has unexplained dirty or untracked files.
- The remote evidence snapshot cannot be verified.
- The evidence reconciler reports checksum mismatches.
- Local tests or build fail for reasons unrelated to expected missing heavy outputs.
- The manuscript baseline is unclear.
- The user has not signed off the Stage 0 closeout.

# Goal 008: Stage 4C Final Validation And Reproducibility Audit

## Objective

Run the final local validation ladder after accepted Stage 4A manuscript
synthesis and accepted Stage 4B release/data-availability readiness, then
produce a move/no-move recommendation for publication packaging, archive/DOI
publication, or Barry-facing manuscript review.

This goal is complete when the repository contains a Stage 4C validation report,
a clean-state reproducibility-audit supplement, and a closeout memo that:

- records the accepted starting commit and working-tree state;
- runs and reports the authorized local validation commands;
- performs manual claim, caption/table, release/licence, checksum, and
  reference-hygiene scans with classified hits;
- checks the Stage 4B release manifest against `data/README.md`,
  `analysis/reports/evidence_reconciliation.*`, and the current git state;
- resolves or explicitly classifies remaining Stage 4 matrix items, especially
  R01, R02, R04, R05, R08, and M03;
- states whether Stage 4 is ready to close, ready for release packaging,
  ready for archive/DOI publication, or instead blocked/deferred; and
- does not perform archive upload, DOI minting, release publication, remote
  compute, data reruns, or new science.

## Why This Matters

Goal 006 accepted the manuscript synthesis and claim-discipline pass. Goal 007
accepted the release/data-availability decision surface, including the corrected
Layer B licence-ledger checksum semantics and the default restriction on raw
and row-level ALA occurrence redistribution.

The remaining risk is not a new analysis idea. It is whether the accepted
manuscript and release surfaces survive a final local validation pass from a
clean committed state, and whether the remaining release gates are real
publication decisions rather than hidden technical defects.

Stage 4C should therefore be firm, bounded, and evidence-led: prove what can be
proved locally; classify what remains a Barry/orchestrator decision; and stop
before publication tooling.

## Operating Mode

Local-only final validation, reproducibility-audit supplementation, manual
claim/release review, and closeout recommendation.

## Authorized Review Surface

Create or update:

- `analysis/reports/stage4C_final_validation_report.md`
- `analysis/reports/final_reproducibility_audit_supplement.md`
- `docs/goals/008-stage4C-final-validation-reproducibility-audit/Stage4C_Closeout.md`
- `docs/goals/008-stage4C-final-validation-reproducibility-audit/Log.md`
- `docs/log/128_stage4C_final_validation_reproducibility.md`

You may update:

- `docs/stage1_critique_resolution_matrix.md`
- `docs/stage_overview.md`
- `analysis/reports/final_release_manifest.md`, but only for narrow factual
  provenance/accepted-commit metadata corrections found by validation; do not
  change release policy classifications without recording a blocker.
- `README.md`, but only if the authorized validation commands reproduce the
  `uv`/`VIRTUAL_ENV` warning or another user-facing validation caveat that
  must be documented for R04.

Do not edit:

- source code under `src/`;
- tests under `tests/`;
- generated data under `data/processed/` or `data/raw/`;
- generated figures under `manuscript/figures/`;
- manuscript science text, captions, tables, or data/code availability text;
- `docs/ref_doi.txt`;
- existing Zenodo checklist files;
- `analysis/reports/evidence_reconciliation.md`;
- `analysis/reports/evidence_reconciliation.json`;
- `analysis/reports/reproducibility_audit.md`, unless the goal becomes blocked
  because a supplement is demonstrably insufficient. Prefer the supplement.

If an out-of-scope edit appears necessary, record the blocker in the closeout
and stop or ask the orchestrator.

## Scope

In scope:

- confirm the repo starts from the accepted Goal 007 state;
- run local validation commands authorized below;
- write a Stage 4C validation report with command evidence, manual scan
  classifications, and blocker/non-blocker status;
- write a clean-state reproducibility-audit supplement that records current git
  commit, dirty/clean state, validation commands, evidence-reconciliation
  status, release-manifest status, large-output assumptions, and expected
  runtime/compute class;
- perform local evidence-reconciliation checks into `/tmp` when possible
  without modifying repo evidence reports;
- inspect whether the old `uv` warning is reproduced by authorized commands;
- verify manuscript/reference hygiene, including M03, without adding or
  removing substantive literature;
- verify that Stage 4B release wording does not overpromise archive/DOI
  publication or raw/row-level ALA redistribution;
- update the Stage 1 matrix only where Stage 4C validation justifies it;
- update `docs/stage_overview.md` only if the Stage 4C closeout status needs
  to be recorded;
- produce a recommendation for the next step.

Out of scope:

- no new science;
- no manuscript rewrite;
- no source-code changes;
- no test changes;
- no data reruns;
- no data processing pipelines;
- no ALA downloads;
- no Layer A or Layer B model runs;
- no `make readiness`;
- no remote compute;
- no `analysis/sync_to_deep_server.sh`;
- no `analysis/deep_server_tmux_run.sh`;
- no release packaging;
- no GitHub release;
- no archive upload;
- no DOI minting;
- no final publication submission;
- no large-file copy, move, compression, upload, or staging;
- no commits, pushes, merges, or PRs.

## Read First

- `AGENTS.md`
- `README.md`
- `Makefile`
- `pyproject.toml`
- `docs/stage_overview.md`
- `docs/stage4_manuscript_release_plan.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/workflow.md`
- `docs/decisions.md`
- `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Stage4A_Closeout.md`
- `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
- `analysis/reports/final_release_manifest.md`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/evidence_reconciliation.json`
- `analysis/reports/reproducibility_audit.md`
- `data/README.md`
- `manuscript/text/manuscript_draft.md`
- `references/refs.yaml`
- `docs/ref_doi.txt` for context only; do not edit it.

If another existing report is clearly needed to classify a validation hit, read
it. Do not read or write outside `/Users/bwbrook/papers/dsipa-dev`.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- `git rev-parse --short refs/remotes/origin/main` if available
- whether this Goal 008 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 007 at commit `9082f4f`. Treat files under
`docs/goals/008-stage4C-final-validation-reproducibility-audit/` as authorized
working instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, open a PR, create a GitHub
  release, publish an archive, or mint a DOI.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  008 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not use remote compute.
- Do not probe SSH or Tailscale for this goal.
- Do not run `make readiness`.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not run `make pipeline`, `make layerA`, `make hpc-evidence`,
  `make hpc-full`, `make hpc-sync-dry-run`, or `make hpc-sync`.
- Do not run data pipelines, ALA downloads, modelling, release packaging,
  archive tooling, DOI tooling, or publication tooling.
- Do not copy, move, compress, upload, or stage large ignored data outputs.
- Write temporary validation artefacts under `/tmp`, not into repo, unless the
  path is one of the authorized report/closeout/log files.

## Authorized Validation Commands

Run these from the repo root unless a blocker prevents them:

```bash
git status --short --branch
git diff --check
make ms-check
make test
make build
```

Run a local evidence-reconciliation check to `/tmp` if it can be done without
editing repo evidence reports:

```bash
uv run python -m dsipa.evidence_reconciliation \
  --output-md /tmp/dsipa_stage4c_evidence_reconciliation.md \
  --output-json /tmp/dsipa_stage4c_evidence_reconciliation.json \
  --audit-md /tmp/dsipa_stage4c_reproducibility_audit.md \
  --write-audit
```

If the evidence-reconciliation check fails because large ignored files are
absent or because local state differs from the deep-server evidence snapshot,
do not fetch, sync, rerun, or regenerate data. Classify the failure precisely
as blocker or non-blocker and record what would be needed in a later goal.

Do not run `make ms-build` by default. If you believe `make ms-check` does not
provide enough manuscript build evidence, record that as a recommendation or
ask the orchestrator; do not generate final manuscript build artefacts in this
goal.

## Required Manual Scans

Run these scans as review aids and classify every relevant hit. They are not
automatic failures.

Claim discipline:

```bash
rg -n "population decline|population trend|causal|causal impact|national biodiversity|national biodiversity response|provider-bounded|presence-only|falsification" manuscript/text docs
```

Caption/table denominator discipline:

```bash
rg -n "n =|eligible|ineligible|minimum-pixel|zero|censor|complete ring|provider-matched|AUC|log loss|redistribut" manuscript/text
```

Release/licence/checksum discipline:

```bash
rg -n "mixed|raw ALA|row-level|redistribut|restricted|excluded|CC-BY|CC BY|Creative Commons|Zenodo|DOI|archive|release manifest|checksum|a751d630|2257ef67" manuscript/text docs data/README.md analysis/reports
```

Reference hygiene:

```bash
rg -n "doi:|DOI|10\\.|ref_doi|TODO|FIXME|citation needed|\\[@|\\?\\]" manuscript/text references docs/ref_doi.txt
```

Release-manifest consistency:

```bash
rg -n "9082f4f|530e843|f731562|dirty=true|archived-proposed|restricted|regenerated|excluded|tracked|a751d630|2257ef67" analysis/reports/final_release_manifest.md analysis/reports/evidence_reconciliation.md analysis/reports/evidence_reconciliation.json data/README.md docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md
```

Manual classification rules:

- Any causal, decline, trend, or national biodiversity wording for Layer B must
  be negated/cautionary or removed, unless it is historical context clearly not
  part of current claims.
- Layer A national protected-area claims must carry the appropriate denominator
  and eligibility logic.
- Edge/penetration claims must remain conditional on complete-ring feasibility.
- Table S1/ranking language must remain triage/category-safe, not exact
  ordinal ranking.
- Layer B must remain provider-matched/provider-bounded, weak, associational,
  presence-only, and falsification-limited.
- ALA release wording must state mixed licences and no raw or row-level
  redistribution unless permissions are explicitly resolved.
- Archive/DOI wording must not imply publication has occurred.
- `2257ef67` must not reappear as a current release-facing checksum.
- `docs/ref_doi.txt` may exist as a DOI seed/scaffold file, but raw DOI
  scaffolding must not appear as unresolved manuscript text.

## Matrix Guidance

Use evidence from this goal to update matrix rows only where justified:

- R01 can move from `release-gate` to `done` only if the new supplement records
  the accepted commit, clean/dirty state, command set, and evidence status.
- R02 should remain a release/publication gate unless an actual archive/DOI
  publication decision exists. This goal does not authorize that decision.
- R04 can move to `done` or `superseded` only if validation records whether the
  `uv` warning was reproduced and documents the expected behavior if needed.
- R05 should remain a release/publication gate unless all final archive-scope
  decisions are actually resolved. Classification alone is not DOI publication.
- R08 can move to `done` only if the Stage 4C report includes tests/builds plus
  manual domain/release scan classifications.
- R09 should remain `done` if checksum validation confirms the Goal 007 fix.
- M03 can move to `done` only if reference/manuscript checks show no unresolved
  raw DOI scaffolding in manuscript text and no unknown bibliography keys.

## Required Work

1. Confirm current state and packet presence.
2. Reconstruct the accepted Stage 4C contract from the Stage 4 plan and Goal
   007 closeout.
3. Run the authorized local validation commands and record full outcomes.
4. Run the local `/tmp` evidence-reconciliation check or classify why it cannot
   run inside the goal boundaries.
5. Run and manually classify the required claim, denominator, release/licence,
   checksum, reference, and release-manifest scans.
6. Create `analysis/reports/stage4C_final_validation_report.md` with:
   - starting state;
   - commands run and outcomes;
   - evidence-reconciliation result;
   - manual scan classifications;
   - matrix-item recommendations;
   - blocker/non-blocker table;
   - move/no-move recommendation.
7. Create `analysis/reports/final_reproducibility_audit_supplement.md` with:
   - current commit and clean/dirty state;
   - relationship to the pre-final `analysis/reports/reproducibility_audit.md`;
   - validation commands and outcomes;
   - large ignored output assumptions;
   - release manifest/archive/DOI status;
   - expected runtime and compute class for any future full rerun.
8. Update only authorized docs if validation justifies it.
9. Write `docs/log/128_stage4C_final_validation_reproducibility.md`.
10. Write `Stage4C_Closeout.md` with:
    - changed files;
    - command evidence;
    - scan classifications;
    - matrix changes;
    - unresolved blockers/decisions;
    - final recommendation;
    - recommended next goal.
11. Append `Log.md`.
12. Wake the DSIPA orchestrator and stop.

## Validation Gates For This Goal

Before waking the orchestrator, run:

```bash
git status --short --branch
git diff --check
test -f analysis/reports/stage4C_final_validation_report.md
test -f analysis/reports/final_reproducibility_audit_supplement.md
test -f docs/goals/008-stage4C-final-validation-reproducibility-audit/Stage4C_Closeout.md
test -f docs/log/128_stage4C_final_validation_reproducibility.md
```

Also include the outcomes of:

- `make ms-check`
- `make test`
- `make build`
- the `/tmp` evidence-reconciliation command, or a precise boundary-based
  classification of why it was not run or did not pass
- the required `rg` scans and manual classifications

Do not treat a scan with many hits as a failure by itself. The closeout must
say which hits are expected historical/context hits, which are current claims,
and which require follow-up.

## Expected Deliverables

- Stage 4C validation report:
  `analysis/reports/stage4C_final_validation_report.md`
- Clean-state reproducibility-audit supplement:
  `analysis/reports/final_reproducibility_audit_supplement.md`
- Optional narrow provenance correction to:
  `analysis/reports/final_release_manifest.md`
- Matrix/stage overview updates if justified:
  `docs/stage1_critique_resolution_matrix.md`
  `docs/stage_overview.md`
- Stage 4C log:
  `docs/log/128_stage4C_final_validation_reproducibility.md`
- Goal closeout:
  `docs/goals/008-stage4C-final-validation-reproducibility-audit/Stage4C_Closeout.md`
- Goal execution log update:
  `docs/goals/008-stage4C-final-validation-reproducibility-audit/Log.md`

## Decision Authority

`nightlight` may decide:

- exact wording for validation findings and matrix status changes within this
  packet;
- whether a command failure is a blocker or non-blocker if the evidence is
  clear;
- whether `analysis/reports/final_release_manifest.md` needs a narrow
  accepted-commit metadata correction.

Escalate to the DSIPA orchestrator if:

- validation requires remote compute, data reruns, ALA downloads, or large-file
  movement;
- a final manuscript claim appears scientifically unsupported;
- a release/package decision would require archive/DOI publication;
- raw ALA or row-level processed ALA redistribution appears necessary;
- adding/removing substantive literature or changing citation strategy appears
  necessary;
- the goal cannot produce a move/no-move recommendation within the authorized
  surface.

Barry-level decisions must remain explicit blockers or recommended next steps,
not assumed approvals.

## Wake-Up Requirement

When complete or blocked, send a short wake-up to the DSIPA orchestrator thread
`019eabf0-9051-7ce2-a0b6-d93b966d1562` with:

- whether Goal 008 is complete or blocked;
- the closeout path;
- the validation recommendation;
- any blocker requiring orchestrator or Barry decision.

Then stop and wait.

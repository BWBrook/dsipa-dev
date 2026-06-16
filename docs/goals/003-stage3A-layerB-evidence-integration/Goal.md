# Goal 003: Stage 3A Layer B Evidence Integration

## Objective

Reconcile the existing Layer B evidence into the manuscript-facing surfaces
without running new analyses. Complete Table S2, tighten Layer B claim
discipline, add or verify licensing/data-availability caveats, and record the
Stage 3A resolution state for B01-B09, B11, and B12.

This goal is complete when Layer B is manuscript-ready as a conservative,
provider-bounded secondary occurrence-signal test, and when the DSIPA
orchestrator can decide whether Stage 3B should be the only remaining Stage 3
goal before Stage 4 manuscript synthesis.

## Why This Matters

Goal 002 accepted the Stage 3 plan. The plan says the next move is not new
Layer B modelling. The existing evidence is strong enough for a cautious,
secondary result, but the manuscript and governance docs still need the result
to be integrated with precise table values, licensing caveats, and no-run
rationales for the rejected analysis extensions.

This goal turns the accepted Stage 3 plan into a manuscript-facing Layer B
integration pass while preserving the conservative interpretation.

## Operating Mode

Evidence integration, manuscript/table editing, claim-discipline review, and
bounded validation.

## Authorized Review Surface

You may create or update only these files unless blocked:

- `manuscript/text/supplementary_tables.md`
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`
- `docs/interpretation_notes.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/decisions.md`
- `docs/log/123_stage3A_layerB_evidence_integration.md`
- `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
- `docs/goals/003-stage3A-layerB-evidence-integration/Log.md`

Only edit `docs/decisions.md` if you decide the B04/B07/B09 no-run rationale
needs an explicit durable decision entry. Keep any decision narrow.

Do not update `docs/stage_overview.md` unless blocked; Stage 3 is not complete
until Stage 3B is complete or explicitly deferred by the orchestrator.

## Scope

In scope:

- fill Table S2 from existing Layer B reports;
- update narrow Layer B manuscript text and captions only where needed to keep
  the claims provider-bounded, associational, weak-discrimination, and
  falsification-limited;
- add or verify mixed-licence and no-raw-ALA-redistribution language;
- record no-run rationales for B04, B07, and B09;
- record B01-B09, B11, and B12 as resolved, deferred, or Stage 4-bounded in the
  Stage 1 matrix or Stage 3A log;
- update interpretation notes for the final integrated Layer B stance;
- run the validation bundle below;
- produce a closeout memo with a Stage 3A acceptance recommendation and a
  specific recommendation for Stage 3B.

Out of scope:

- do not run ALA downloads;
- do not run Layer B modelling or rerun figures/tables from raw data;
- do not run remote compute;
- do not modify source code or tests;
- do not implement B10;
- do not perform release packaging, archive/DOI work, or Zenodo checks;
- do not do a broad Stage 4 rewrite of the whole manuscript;
- do not change Layer A results;
- do not commit, push, merge, or open pull requests;
- do not contact Barry or Chief.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/stage3_layerB_reconciliation_plan.md`
- `docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/decisions.md`
- `docs/interpretation_notes.md`
- `docs/log/100_layerB_data_acquisition.md`
- `docs/log/101_layerB_qc_hardening.md`
- `docs/log/102_layerB_modelling.md`
- `docs/log/107_layerB_ibra_robustness.md`
- `analysis/reports/layerB_data_qc.md`
- `analysis/reports/layerB_ala_license_ledger.md`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_modelling_report.md`
- `analysis/reports/layerB_ibra_summary.md`
- `analysis/reports/layerB_ibra_effects.csv`
- `analysis/reports/evidence_reconciliation.md`
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/supplementary_tables.md`
- `data/README.md`

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this Goal 003 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 002 at commit `2a635f1`. Treat files under
`docs/goals/003-stage3A-layerB-evidence-integration/` as authorized working
instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, or open a PR.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  003 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Use existing tracked reports, manuscript text, and docs.
- Do not use remote compute.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not regenerate data, figures, model outputs, artefact folders, or release
  packages.
- Temporary build/check outputs may go under `/tmp` only if a tool requires
  them.

## Required Work

1. Reconstruct the Stage 3A contract from the accepted Stage 3 plan.
2. Fill Table S2 in `manuscript/text/supplementary_tables.md` from existing
   evidence only. Include the four planned rows:
   - primary provider-matched model;
   - block-shuffle falsification;
   - IBRA-by-year shuffle falsification;
   - full multi-provider sensitivity.
3. Cross-check every Table S2 number against
   `analysis/reports/layerB_modelling_report.md` and the supporting QC reports.
4. Tighten manuscript text/captions only where necessary to avoid overclaiming:
   Layer B is not causal, not a population trend, not a population decline
   analysis, and not a national biodiversity response.
5. Verify or add mixed ALA licence and no raw occurrence redistribution
   language where needed.
6. Record no-run rationales for B04, B07, and B09.
7. Update `docs/interpretation_notes.md` with the integrated Stage 3A Layer B
   interpretation.
8. Update `docs/stage1_critique_resolution_matrix.md` or the Stage 3A log so
   B01-B09, B11, and B12 have a clear resolution, deferral, or Stage 4 boundary.
   Leave B10 for Stage 3B.
9. Write `docs/log/123_stage3A_layerB_evidence_integration.md`.
10. Write `Stage3A_Closeout.md` with a clear recommendation.

## Validation Gates

Run from the repo root:

```bash
git status --short --branch
git diff --check
make ms-check
```

Run targeted claim and licence scans:

```bash
rg -n "population decline|population trend|causal impact|national biodiversity response|national biodiversity signal" manuscript/text docs/interpretation_notes.md
rg -n "negative controls|diurnal reptiles|Squamata|provider-matched|falsification|Layer B" manuscript/text docs/interpretation_notes.md
rg -n "CC-BY|CC BY|Creative Commons|raw ALA|redistribut|mixed" manuscript/text docs data/README.md
```

Run a Table S2 source check and report the result. The form is up to you, but
the closeout must explicitly compare Table S2 values with
`analysis/reports/layerB_modelling_report.md`.

Classify validation as:

- current and passing;
- passing with expected review hits;
- inconclusive because a check is a review scan rather than a pass/fail test;
- failed and blocking; or
- failed but only relevant to a later Stage 3B or Stage 4 goal.

Do not silently ignore failures.

## Deliverables

- Completed Table S2 in `manuscript/text/supplementary_tables.md`
- Narrow Layer B manuscript/caption/interpretation updates as needed
- B04/B07/B09 no-run rationales
- Stage 3A log:
  `docs/log/123_stage3A_layerB_evidence_integration.md`
- Closeout memo:
  `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
- Updated `docs/goals/003-stage3A-layerB-evidence-integration/Log.md`
- Final response to the DSIPA orchestrator summarizing:
  - changed files;
  - Table S2 source cross-check outcome;
  - validation commands and exact outcomes;
  - current git status;
  - B01-B09/B11/B12 resolution state;
  - whether Stage 3B should be next;
  - whether any Barry-level decision is needed.

## Decision Authority

`nightlight` may decide:

- the exact Table S2 wording and compact formatting;
- which Layer B manuscript sentences need tightening;
- whether B04/B07/B09 no-run rationales belong in the matrix, log, decisions,
  or a combination;
- whether a search hit is acceptable because it is clearly caveated.

`nightlight` must pause or report blocked before:

- changing scientific assumptions;
- proposing new Layer B modelling or data acquisition;
- removing Layer B from the paper;
- changing release/archive policy;
- editing outside the authorized review surface;
- running remote compute, data processing, or ALA downloads;
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 003 is complete or blocked and point
to the closeout memo path. If thread tools are unavailable at runtime, state
that in the final response and stop.

## Stop Conditions

Stop when one of these is true:

- Stage 3A integration is complete, validation is classified, the closeout memo
  is written, and the log is updated;
- a blocker prevents a defensible Stage 3A integration pass;
- completing the work would require out-of-scope modelling, data processing,
  remote compute, broad manuscript rewriting, or publication policy decisions.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- Table S2 source cross-check result;
- B01-B09/B11/B12 state;
- blockers or residual risks;
- whether a narrow fix goal is needed before Stage 3B;
- whether Stage 3B should be the next goal.

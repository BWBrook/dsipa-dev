# Goal 006: Stage 4A Manuscript Synthesis And Claim Discipline

## Objective

Rewrite and tighten the manuscript-facing narrative from the accepted Stage 2
and Stage 3 evidence package, without changing science outputs or release
policy.

This goal is complete when the manuscript draft, tables, captions,
supplementary surfaces, interpretation notes, and critique matrix make the
paper substantially more decisive about robust Layer A findings while
preserving the accepted Layer B stance:

- Layer A is the primary result.
- Layer B is secondary, weak, provider-bounded, presence-only,
  falsification-limited, and not causal or population-trend evidence.
- Denominators, eligibility rules, censoring/floor mass, complete-ring
  feasibility, uncertainty-aware watchlists, and raw ALA redistribution limits
  are visible where readers need them.

## Why This Matters

Goal 005 accepted a Stage 4 plan and recommended a three-part endgame:

1. Stage 4A manuscript synthesis and claim discipline.
2. Stage 4B release/data-availability/archive/DOI readiness.
3. Stage 4C final manuscript/build/reproducibility validation.

This goal executes Stage 4A only. The paper should now read less like a rough
evidence dump and more like a coherent argument, but only where the accepted
evidence supports that confidence. The main danger is overclaiming Layer B or
smuggling release/archive decisions into prose. Avoid both.

## Operating Mode

Evidence-led manuscript rewrite, table/caption discipline, claim scan, and
manuscript check.

## Authorized Review Surface

Create or update:

- `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Stage4A_Closeout.md`
- `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Log.md`
- `docs/log/126_stage4A_manuscript_synthesis.md`

You may update:

- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/references.md`
- `docs/interpretation_notes.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/plan.md`
- `docs/roadmap.md`

Limits on the optional governance docs:

- Edit `docs/plan.md` and `docs/roadmap.md` only if needed to redirect stale
  "current status" or "next work" cues to the staged workflow and Stage 4 plan.
- Do not rewrite historical WP sections or erase history.

Do not edit:

- `data/README.md`
- `docs/ref_doi.txt`
- `docs/decisions.md`
- `analysis/reports/*`
- `README.md`
- source code
- tests
- generated figures
- generated tables outside `manuscript/text/`
- release manifests
- archive/DOI files
- build configuration

If a required manuscript fix appears to require one of those out-of-scope
surfaces, record the blocker in the closeout and stop or ask the orchestrator.

## Scope

In scope:

- rewrite manuscript Results and Discussion from accepted Stage 2/3 evidence;
- sharpen the Abstract while preserving the current scientific stance;
- revise captions and table notes so denominators, eligibility, censoring,
  selection rules, and Layer B caveats travel with the artefacts;
- verify Table 1, Table S1, and Table S2 values against accepted reports and
  closeouts before changing table text;
- keep Layer B narrow: provider-matched/provider-bounded, weak,
  associational, presence-only, and falsification-limited;
- update `docs/interpretation_notes.md` with a Stage 4A synthesis entry;
- update M01, M02, M04, and manuscript-facing M05 in
  `docs/stage1_critique_resolution_matrix.md` only when justified by the
  completed manuscript changes and validation;
- leave M03 and release-gate items open unless a narrow manuscript-facing
  cross-check genuinely resolves part of them;
- run `make ms-check` after manuscript edits and classify the result;
- write a Stage 4A closeout with source cross-checks, validation evidence, and
  the recommended next goal.

Out of scope:

- no new Layer A analysis;
- no new Layer B modelling;
- no ALA downloads or occurrence processing;
- no data-processing pipelines;
- no figure regeneration;
- no release manifest creation;
- no archive upload, DOI minting, or publication package work;
- no data availability rewrite that cites or promises an external archive DOI;
- no raw ALA or row-level processed ALA redistribution promise;
- no remote compute;
- no package builds unless explicitly needed to debug `make ms-check` and
  authorized by the orchestrator;
- no commits, pushes, merges, or PRs;
- no contact with Barry or Chief.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/stage_overview.md`
- `docs/stage4_manuscript_release_plan.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/goals/001-stage2-signoff-readiness/Stage2_Signoff_Readiness.md`
- `docs/goals/002-stage3-layerB-reconciliation-plan/Stage3_Planning_Readiness.md`
- `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
- `docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md`
- `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
- `docs/interpretation_notes.md`
- `docs/workflow.md`
- `docs/plan.md`
- `docs/roadmap.md`
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/references.md`
- `analysis/reports/layerA_denominators_and_censoring.md`
- `analysis/reports/layerA_table1_candidate.md`
- `analysis/reports/layerA_watchlists_uncertainty.md`
- `analysis/reports/risk_rankings_and_quadrants.md`
- `analysis/reports/layerA_edge_profile_decision.md`
- `analysis/reports/layerA_sanity_dashboard.md`
- `analysis/reports/layerA_buffer_validity_sensitivity.md`
- `analysis/reports/layerA_trend_threshold_sensitivity.md`
- `analysis/reports/pa_trend_uncertainty.md`
- `analysis/reports/layerB_modelling_report.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_ala_license_ledger.md`
- `analysis/reports/figure_inventory.md`

If another existing report is clearly needed to verify a manuscript value, read
it. Do not read or write outside `/Users/bwbrook/papers/dsipa-dev`.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this Goal 006 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 005 at commit `9793641`. Treat files under
`docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/` as authorized
working instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, or open a PR.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  006 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not use remote compute.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not run data pipelines, ALA downloads, modelling, package builds, release
  packaging, archive tooling, or DOI tooling.
- `make ms-check` is authorized after manuscript edits.
- Temporary build/check outputs may be generated only by `make ms-check` and
  should not be committed unless they are already tracked and intentionally
  changed by the manuscript check workflow.

## Required Work

1. Reconstruct the accepted Stage 2/3 evidence state and the Goal 005 Stage 4A
   contract.
2. Before editing, identify the manuscript claims that need strengthening,
   tightening, or caveating.
3. Rewrite the Abstract, Results, Discussion, and limitations so that:
   - Layer A is clearly the main contribution;
   - floor domination/censoring is a central result, not a buried caveat;
   - the non-zero brightening tail and external-pressure cases are presented
     with their proper denominators;
   - edge/penetration language is conditional on complete-ring feasibility;
   - watchlists are uncertainty-aware triage aids, not exact ranks;
   - Layer B remains weak, provider-bounded, presence-only, associational, and
     falsification-limited.
4. Revise table and caption text for:
   - Table 1 denominator/feasibility language;
   - Table S1 uncertainty-aware watchlist language;
   - Table S2 weak Layer B signal/falsification language;
   - Fig. 1-3 and Supplementary Fig. S1-S3 Layer A denominators and censoring;
   - Fig. 4-5 and Supplementary Fig. S4-S6 Layer B caveats.
5. Do not change table values unless the accepted source reports prove the
   current manuscript value is wrong. If any value is wrong, fix it only in
   manuscript text and document the source cross-check in the closeout.
6. Update `docs/interpretation_notes.md` with a concise Stage 4A synthesis
   entry.
7. Update `docs/stage1_critique_resolution_matrix.md` for M01, M02, M04, and
   manuscript-facing M05 only if the manuscript changes and validation justify
   the status change.
8. Optionally add minimal redirect notes to `docs/plan.md` and/or
   `docs/roadmap.md` if stale current-status cues would mislead a resume pass.
9. Run the required validation gates.
10. Write `docs/log/126_stage4A_manuscript_synthesis.md`.
11. Write `Stage4A_Closeout.md` with:
    - changed files;
    - claim rewrite summary;
    - table/caption/source cross-checks;
    - validation command outputs and classifications;
    - matrix status updates;
    - residual risks;
    - recommended next goal.
12. Append `Log.md`.

## Validation Gates

Run these from the repo root:

```bash
git status --short --branch
git diff --check
make ms-check
```

Run targeted review scans and classify every hit:

```bash
rg -n "population decline|population trend|causal impact|causal|national biodiversity response|national biodiversity signal|national biodiversity" manuscript/text docs/interpretation_notes.md
rg -n "provider-bounded|presence-only|falsification|provider-matched|weak discrimination|AUC|log loss|raw ALA|redistribut|mixed" manuscript/text docs/interpretation_notes.md
rg -n "n =|eligible|ineligible|minimum-pixel|valid-pixel|zero|censor|floor|complete ring|selection rule|triage|uncertainty" manuscript/text
```

Run source-value cross-checks and record the result:

```bash
rg -n "11,133|4,426|3,844|86.9|3,969|89.7|420|3,858|305|55|3,308|190|383" manuscript/text docs/stage4_manuscript_release_plan.md analysis/reports
rg -n "50,281|0.545|0.689|0.505|0.517|0.557|provider-matched|multi-provider|mixed" manuscript/text docs/stage4_manuscript_release_plan.md analysis/reports
```

The `rg` commands are review aids, not automatic failures. Passing means the
hits are present, classified, and consistent with the accepted evidence and
claim discipline.

Do not run full pytest, package builds, release packaging, DOI/archive
commands, data pipelines, or remote commands for this goal.

## Deliverables

- updated manuscript-facing files as needed;
- updated `docs/interpretation_notes.md`;
- updated `docs/stage1_critique_resolution_matrix.md`;
- optional narrow redirect update to `docs/plan.md` and/or `docs/roadmap.md`;
- Stage 4A log:
  `docs/log/126_stage4A_manuscript_synthesis.md`;
- closeout memo:
  `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Stage4A_Closeout.md`;
- updated goal log:
  `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Log.md`;
- final response to the DSIPA orchestrator summarizing:
  - changed files;
  - validation commands and exact outcomes;
  - claim scan classifications;
  - table/caption/source cross-checks;
  - matrix status updates;
  - current git status;
  - whether Stage 4A is ready for orchestrator acceptance;
  - recommended next goal.

## Decision Authority

`nightlight` may decide:

- manuscript sentence structure and section-level organization;
- whether to keep, shorten, or move existing caveat text;
- how to phrase accepted Layer A claims more decisively;
- how to phrase Layer B caution more clearly;
- whether a table/caption note needs tightening;
- whether M01, M02, M04, or manuscript-facing M05 can move to `done`,
  `verify`, or remain `open`;
- whether narrow plan/roadmap redirect notes are needed.

`nightlight` must pause or report blocked before:

- changing the title in a way that materially changes paper framing;
- removing Layer B from the manuscript;
- strengthening Layer B beyond the accepted weak secondary stance;
- adding new scientific claims not supported by accepted reports;
- changing data availability or release policy;
- editing out-of-scope files;
- running data processing, modelling, ALA downloads, remote compute, package
  builds, release packaging, or DOI/archive tooling;
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 006 is complete or blocked and point
to the Stage 4A closeout memo path. If thread tools are unavailable at runtime,
state that in the final response and stop.

## Stop Conditions

Stop when one of these is true:

- Stage 4A manuscript synthesis is complete, validation is classified, the
  closeout memo is written, and the log is updated;
- `make ms-check` or a claim/source scan exposes a blocker that cannot be fixed
  inside the authorized review surface;
- completing the work would require out-of-scope release policy, archive/DOI
  work, new analysis, data processing, remote compute, or publication strategy
  decisions.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- claim scan classifications;
- table/caption/source cross-checks;
- M01/M02/M04/M05 status changes;
- blockers or residual risks;
- whether Stage 4A is ready for orchestrator acceptance;
- recommended next goal.

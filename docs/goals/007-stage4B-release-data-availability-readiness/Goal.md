# Goal 007: Stage 4B Release And Data Availability Readiness

## Objective

Create a release and data-availability decision surface that can be reviewed
before any archive publication, DOI minting, or final release packaging.

This goal is complete when the repo contains a clear Stage 4B release manifest,
data-availability wording, and decision record that:

- classify paper-critical artefacts as tracked, archived-proposed,
  regenerated, excluded, or restricted;
- keep raw ALA occurrence downloads and row-level processed ALA occurrence
  tables out of the manuscript package unless a later explicit permission
  decision changes that policy;
- reconcile the Layer B ALA licence-ledger checksum convention;
- make the external archive/DOI decision explicit without publishing or
  minting anything;
- update the Stage 1 matrix only where Stage 4B readiness work justifies it;
  and
- leave final validation, publication packaging, archive upload, and DOI
  minting to later explicit authorization.

## Why This Matters

Goal 006 accepted Stage 4A manuscript synthesis. The manuscript now makes a
clearer evidence-backed argument, but the project still needs a release policy
that does not overpromise reproducibility or accidentally redistribute
restricted ALA occurrence data.

The current repo contains a useful evidence reconciliation, reproducibility
audit, data inventory, figure inventory, Zenodo checklists, and manuscript data
availability language. Those surfaces are not yet a final release decision:
they still mix historical "archive to Zenodo" intent, dirty pre-final audit
state, large ignored outputs, ALA mixed-licence constraints, and checksum
convention notes.

This is a release-readiness and decision-surface goal. It is not an archive
publication goal.

## Operating Mode

Local-only release-readiness audit, manifest writing, data-availability
wording, checksum/licence reconciliation, and decision logging.

## Authorized Review Surface

Create or update:

- `analysis/reports/final_release_manifest.md`
- `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
- `docs/goals/007-stage4B-release-data-availability-readiness/Log.md`
- `docs/log/127_stage4B_release_data_availability.md`

You may update:

- `data/README.md`
- `README.md`
- `manuscript/text/manuscript_draft.md` only in the Data and code
  availability section
- `docs/decisions.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/stage_overview.md`

Do not edit:

- `docs/ref_doi.txt`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/evidence_reconciliation.json`
- `analysis/reports/reproducibility_audit.md`
- existing Zenodo checklist files
- source code
- tests
- generated figures
- generated data files
- generated analysis reports other than the new `final_release_manifest.md`
- manuscript science sections outside Data and code availability
- build configuration

If one of those out-of-scope files appears necessary, record the blocker in
the closeout and stop or ask the orchestrator.

## Scope

In scope:

- inspect current release/data surfaces and Stage 4B requirements;
- create `analysis/reports/final_release_manifest.md`;
- classify paper-critical artefacts as tracked, archived-proposed,
  regenerated, excluded, or restricted;
- state which large Layer A outputs are proposed for archive and which are
  tracked or regenerated;
- state that raw ALA downloads and row-level processed ALA occurrence tables
  remain restricted/excluded unless later permissions allow redistribution;
- state which Layer B derived summaries, reports, and figures are acceptable
  manuscript-facing outputs;
- update `data/README.md` so it distinguishes publication-readiness intent
  from a completed external archive/DOI;
- update README/data-availability wording only as needed to match the manifest;
- record a decision in `docs/decisions.md` for the Stage 4B release policy,
  without pretending Barry has approved archive upload or DOI minting;
- reconcile the raw-vs-normalized checksum convention for
  `layerB_ala_license_ledger_v0_3_0.csv`;
- update B01, B11, R02, R05, and R09 in the Stage 1 matrix only if justified;
- mark R04 or R08 only if the work actually addresses them;
- write a closeout memo identifying decisions still needing Barry or
  orchestrator approval.

Out of scope:

- no archive upload;
- no DOI minting;
- no release publication;
- no release packaging;
- no GitHub release creation;
- no data reruns;
- no data processing;
- no ALA downloads;
- no remote compute;
- no full reproducibility rerun;
- no checksum recalculation on large ignored outputs unless the file is already
  tracked or trivially small;
- no source-code edits;
- no test edits;
- no generated-figure edits;
- no manuscript science rewrite;
- no commits, pushes, merges, or PRs;
- no contact with Barry or Chief.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/stage_overview.md`
- `docs/stage4_manuscript_release_plan.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
- `docs/goals/004-stage3B-ala-ingest-guardrail/Stage3B_Closeout.md`
- `docs/goals/005-stage4-manuscript-release-plan/Stage4_Planning_Readiness.md`
- `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/Stage4A_Closeout.md`
- `data/README.md`
- `docs/ref_doi.txt` for context only; do not edit it
- `docs/decisions.md`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/evidence_reconciliation.json`
- `analysis/reports/reproducibility_audit.md`
- `analysis/reports/data_inventory.md`
- `analysis/reports/figure_inventory.md`
- `analysis/reports/zenodo_release_checklist_2026-01-03.md`
- `analysis/reports/zenodo_release_checklist_2026-01-04.md`
- `analysis/reports/layerB_ala_license_ledger.md`
- `manuscript/text/manuscript_draft.md`

If another existing report is clearly needed to classify a release artefact,
read it. Do not read or write outside `/Users/bwbrook/papers/dsipa-dev`.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- whether this Goal 007 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 006 at commit `530e843`. Treat files under
`docs/goals/007-stage4B-release-data-availability-readiness/` as authorized
working instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, open a PR, create a GitHub
  release, publish an archive, or mint a DOI.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  007 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not use remote compute.
- Do not run `analysis/sync_to_deep_server.sh`.
- Do not run `analysis/deep_server_tmux_run.sh`.
- Do not run data pipelines, ALA downloads, modelling, package builds, release
  packaging, archive tooling, DOI tooling, or publication tooling.
- Do not copy, move, compress, upload, or stage large ignored data outputs.
- `make ms-check` is authorized only if `manuscript/text/manuscript_draft.md`
  is edited for data/code availability wording.

## Required Work

1. Reconstruct the accepted Stage 4B contract from the Stage 4 plan and Goal
   006 closeout.
2. Audit existing release/data surfaces and identify contradictions or stale
   wording, especially "archived to Zenodo" versus "archive/DOI decision
   pending."
3. Create `analysis/reports/final_release_manifest.md` with, at minimum:
   - release posture and non-goals;
   - current repo commit and evidence/audit provenance;
   - tracked manuscript, report, figure, and small data artefacts;
   - large ignored Layer A outputs proposed for external archive;
   - raw ALA downloads and row-level processed ALA tables classified as
     restricted/excluded by default;
   - derived Layer B outputs that are acceptable for manuscript/release
     summaries;
   - checksum convention notes, including the raw-vs-normalized ALA licence
     ledger issue;
   - explicit decisions needed before archive/DOI publication.
4. Update `data/README.md` to describe the release posture accurately:
   proposed/archive-pending, regenerated, excluded, and restricted, without
   claiming a DOI has been minted or an archive has been published.
5. Update README and the manuscript Data and code availability section only if
   needed to align with the manifest.
6. Add a release-policy decision entry to `docs/decisions.md` if justified.
7. Update `docs/stage1_critique_resolution_matrix.md` for Stage 4B release
   readiness items only where justified.
8. Update `docs/stage_overview.md` only if needed to record Stage 4B planning
   or readiness status; do not mark Stage 4 complete.
9. Run validation gates and classify hits.
10. Write `docs/log/127_stage4B_release_data_availability.md`.
11. Write `Stage4B_Closeout.md` with:
    - changed files;
    - manifest summary;
    - data availability changes;
    - licence/checksum classifications;
    - matrix status updates;
    - validation command outputs and classifications;
    - decisions still requiring Barry or orchestrator input;
    - recommended next goal.
12. Append `Log.md`.

## Validation Gates

Run these from the repo root:

```bash
git status --short --branch
git diff --check
test -f analysis/reports/final_release_manifest.md
test -f docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md
test -f docs/log/127_stage4B_release_data_availability.md
```

If `manuscript/text/manuscript_draft.md` is edited, also run:

```bash
make ms-check
```

Run targeted release/licence/checksum scans and classify every hit:

```bash
rg -n "archive|DOI|Zenodo|release manifest|external archive|mint|publish|upload" data/README.md README.md manuscript/text/manuscript_draft.md docs/decisions.md docs/stage1_critique_resolution_matrix.md analysis/reports/final_release_manifest.md
rg -n "raw ALA|row-level|occurrence tables|redistribut|restricted|excluded|mixed|CC-BY|CC BY|Creative Commons" data/README.md README.md manuscript/text/manuscript_draft.md docs/decisions.md analysis/reports/final_release_manifest.md
rg -n "layerB_ala_license_ledger|CRLF|normalized|normalised|checksum|SHA-256|sha256" data/README.md analysis/reports/evidence_reconciliation.md analysis/reports/final_release_manifest.md
rg -n "pa_radiance_buffers_national_v0_3_0|pa_edge_profiles_national_v0_3_0|pa_buffer_validity_v0_3_0|pa_trends_v0_3_0|pa_risk_rankings_v0_3_0|microbats_20260104T020628Z|diurnal_birds_20260104T020701Z|microbats_occurrences_filtered|diurnal_birds_occurrences_filtered" data/README.md analysis/reports/evidence_reconciliation.md analysis/reports/final_release_manifest.md
```

Run a manifest completeness spot-check:

```bash
rg -n "tracked|archived-proposed|regenerated|excluded|restricted|Barry decision|orchestrator decision" analysis/reports/final_release_manifest.md
```

The `rg` commands are review aids, not automatic failures. Passing means hits
are present, classified, and consistent with the Stage 4B release policy.

Do not run full pytest, package builds, release packaging, DOI/archive
commands, data pipelines, or remote commands for this goal.

## Deliverables

- release manifest:
  `analysis/reports/final_release_manifest.md`
- updated `data/README.md`
- optional aligned README/data-availability edits within the authorized
  surface
- optional `docs/decisions.md` release-policy entry
- updated `docs/stage1_critique_resolution_matrix.md`
- optional narrow `docs/stage_overview.md` update
- Stage 4B log:
  `docs/log/127_stage4B_release_data_availability.md`
- closeout memo:
  `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
- updated goal log:
  `docs/goals/007-stage4B-release-data-availability-readiness/Log.md`
- final response to the DSIPA orchestrator summarizing:
  - changed files;
  - validation commands and exact outcomes;
  - manifest classifications;
  - licence/checksum classifications;
  - matrix status updates;
  - current git status;
  - decisions needing Barry or orchestrator input;
  - whether Stage 4B is ready for orchestrator acceptance;
  - recommended next goal.

## Decision Authority

`nightlight` may decide:

- manifest structure;
- exact wording for release-readiness classifications;
- whether release items are tracked, archived-proposed, regenerated,
  excluded, or restricted;
- how to phrase data-availability wording without promising publication;
- whether B01, B11, R02, R05, R09, R04, or R08 can move to `done`, remain
  `release-gate`, or require another status;
- whether `docs/decisions.md` needs a new Stage 4B release-policy entry.

`nightlight` must pause or report blocked before:

- uploading anything;
- minting or citing a new archive DOI as final;
- moving/copying/compressing large ignored outputs;
- proposing raw or row-level ALA occurrence redistribution as the default;
- making Barry-level archive scope decisions;
- running data processing, ALA downloads, remote compute, package builds,
  release packaging, DOI/archive tooling, or publication tooling;
- editing out-of-scope files;
- contacting Barry or Chief.

## Wake-Up Requirement

When done or blocked, send a short wake-up message to the DSIPA orchestrator
thread:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

The wake-up should say only whether Goal 007 is complete or blocked and point
to the Stage 4B closeout memo path. If thread tools are unavailable at runtime,
state that in the final response and stop.

## Stop Conditions

Stop when one of these is true:

- Stage 4B release/data-availability readiness is complete, validation is
  classified, the closeout memo is written, and the log is updated;
- a release/licence/checksum blocker cannot be resolved inside the authorized
  review surface;
- completing the work would require archive upload, DOI minting, release
  packaging, data processing, remote compute, or Barry-level publication
  decisions.

## Final Response Requirements

Report:

- files changed;
- validation commands run and exact outcomes;
- final `git status --short --branch`;
- release manifest classifications;
- licence/checksum classifications;
- B01/B11/R02/R05/R09 status changes or reasons for no change;
- blockers or residual risks;
- decisions needing Barry or orchestrator input;
- whether Stage 4B is ready for orchestrator acceptance;
- recommended next goal.

# Goal 009: Release Blocker Decision Packet

## Objective

Prepare a decision packet for the remaining release blockers identified by
Goal 008, without performing release, archive, DOI, publication, remote
compute, data rerun, or large-file movement work.

This goal is complete when the repository contains a concise but decision-ready
release blocker packet that:

- lists the remaining blockers after Stage 4C;
- separates decisions from validation tasks;
- recommends a final archive/DOI scope for `archived-proposed` large Layer A
  outputs;
- preserves the default restricted/excluded handling of raw ALA downloads and
  row-level processed ALA occurrence tables;
- recommends how to refresh evidence reconciliation for the current tracked
  baseline figure checksum;
- identifies the exact later goal needed before any archive upload, DOI
  minting, release packaging, GitHub release, or publication submission;
- gives Barry/orchestrator a small set of explicit options and a recommended
  path; and
- does not move, copy, compress, upload, mint, publish, rerun, regenerate, or
  rewrite any scientific artefact.

## Why This Matters

Goal 008 proved that the local manuscript, test, and package-build surfaces are
green, but correctly recommended **no move** to archive/DOI/release/publication.
Two release blockers remain:

1. final archive/DOI scope and policy for large ignored outputs; and
2. a refreshed evidence reconciliation path for the current tracked baseline
   figure checksum (`fig_layerA_baseline_map.png`), whose current hash differs
   from the older evidence snapshot after accepted Stage 2 figure work.

The next useful step is not to push toward publication tooling. It is to make a
high-quality release decision surface so Barry and the orchestrator can approve
or modify the actual release path deliberately.

## Operating Mode

Local-only decision analysis, manifest reconciliation, risk classification, and
option/recommendation writing.

## Authorized Review Surface

Create or update:

- `docs/release_blocker_decision_packet.md`
- `docs/goals/009-release-blocker-decision-packet/Stage4D_Release_Blocker_Decision_Packet.md`
- `docs/goals/009-release-blocker-decision-packet/Log.md`
- `docs/log/129_release_blocker_decision_packet.md`

You may update:

- `analysis/reports/final_release_manifest.md`, but only to add a pointer to
  the new decision packet or a narrow clarification of decision status. Do not
  change classifications unless the decision packet records a clear blocker.
- `docs/stage1_critique_resolution_matrix.md`, but only to add Goal 009
  decision-packet status while leaving unresolved release/publication gates
  visibly unresolved.
- `docs/stage_overview.md`, but only if needed to record that Goal 009 prepared
  a decision packet and did not authorize release movement.

Do not edit:

- source code under `src/`;
- tests under `tests/`;
- generated data under `data/processed/` or `data/raw/`;
- generated figures under `manuscript/figures/`;
- manuscript text, captions, tables, or data/code availability wording;
- `docs/ref_doi.txt`;
- existing Zenodo checklist files;
- `analysis/reports/evidence_reconciliation.md`;
- `analysis/reports/evidence_reconciliation.json`;
- `analysis/reports/reproducibility_audit.md`;
- `analysis/reports/stage4C_final_validation_report.md`;
- `analysis/reports/final_reproducibility_audit_supplement.md`.

If an out-of-scope edit appears necessary, record it as a blocker or a proposed
future-goal item rather than performing it.

## Scope

In scope:

- inspect Goal 008 outputs and the final release manifest;
- identify the exact remaining decisions and validation tasks;
- compare available archive-scope options;
- recommend whether the later release payload should include:
  - tracked repository/manuscript sources;
  - `archived-proposed` large Layer A national outputs;
  - generated/reproducible-only surfaces;
  - restricted raw ALA downloads;
  - restricted row-level processed ALA tables;
- preserve raw/row-level ALA restriction by default unless the decision packet
  explicitly identifies a separate permission route;
- define the evidence-refresh path for:
  - the current tracked baseline figure checksum;
  - the large ignored Layer A outputs;
  - any archive manifest/checksum table needed later;
- define what a future release-execution goal would need to run;
- classify risks as scientific, legal/licensing, reproducibility, operational,
  and publication-process risks;
- write a recommended path plus alternatives.

Out of scope:

- no archive upload;
- no DOI minting;
- no release packaging;
- no GitHub release;
- no publication submission;
- no data reruns;
- no data processing;
- no ALA downloads;
- no Layer A or Layer B model runs;
- no manuscript rebuild beyond reading existing reports;
- no `make readiness`;
- no remote compute;
- no SSH/Tailscale probes;
- no `analysis/sync_to_deep_server.sh`;
- no `analysis/deep_server_tmux_run.sh`;
- no `make pipeline`, `make layerA`, `make hpc-evidence`, `make hpc-full`,
  `make hpc-sync-dry-run`, or `make hpc-sync`;
- no large-file copy, move, compression, upload, or staging;
- no source/test/manuscript/figure edits;
- no commits, pushes, merges, or PRs.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/stage_overview.md`
- `docs/stage4_manuscript_release_plan.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/decisions.md`
- `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
- `docs/goals/008-stage4C-final-validation-reproducibility-audit/Stage4C_Closeout.md`
- `analysis/reports/final_release_manifest.md`
- `analysis/reports/stage4C_final_validation_report.md`
- `analysis/reports/final_reproducibility_audit_supplement.md`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/evidence_reconciliation.json`
- `analysis/reports/zenodo_release_checklist_2026-01-04.md`
- `data/README.md`
- `docs/ref_doi.txt` for context only; do not edit it.

If another report is clearly needed to classify a release decision, read it.
Do not read or write outside `/Users/bwbrook/papers/dsipa-dev`.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- `git rev-parse --short refs/remotes/origin/main` if available
- whether this Goal 009 packet is present

The DSIPA orchestrator created this goal packet after accepting and publishing
Goal 008 at commit `91cd628`. Treat files under
`docs/goals/009-release-blocker-decision-packet/` as authorized working
instructions.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, open a PR, create a GitHub
  release, publish an archive, or mint a DOI.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  009 artefacts.
- Keep edits limited to the authorized review surface unless blocked.

## Data, Compute, And Staging Policy

- Use the local Mac mini checkout only.
- Do not use remote compute.
- Do not probe SSH, Tailscale, Zenodo, GitHub Releases, or any external archive
  service.
- Do not run data pipelines, ALA downloads, modelling, release packaging,
  archive tooling, DOI tooling, or publication tooling.
- Do not copy, move, compress, upload, or stage large ignored data outputs.
- Do not run `make ms-check`, `make test`, `make build`, or evidence
  reconciliation unless you make a change that clearly requires a lightweight
  local check. The expected validation for this decision packet is document and
  consistency review, not rerunning Goal 008.

## Required Decision Packet Content

`docs/release_blocker_decision_packet.md` must include:

1. Executive recommendation.
   - One recommended path.
   - A short no-move statement for archive/DOI/release/publication until later
     authorization.

2. Current evidence state.
   - Goal 008 command-green status.
   - Ten missing large/restricted ignored files from local evidence
     reconciliation.
   - Current tracked baseline-map checksum mismatch and why it is evidence
     staleness, not figure drift.

3. Decision table.
   - Decision owner: orchestrator, Barry, or future release-execution goal.
   - Decision needed.
   - Recommended option.
   - Alternatives.
   - Risks/trade-offs.

4. Archive-scope options.
   - Minimum source/manuscript-only release.
   - Recommended source/manuscript plus archive-proposed large Layer A outputs.
   - Full reproducibility bundle requiring large ignored outputs and explicit
     restricted-data exclusions.
   - Explicitly reject raw ALA and row-level processed ALA redistribution by
     default.

5. DOI/archive route recommendation.
   - Identify practical archive/DOI route options at a high level.
   - Recommend a route if the existing repo evidence supports one.
   - State that no DOI may be cited until it exists.

6. Evidence-refresh plan for a future goal.
   - Current tracked baseline figure checksum.
   - Evidence snapshot refresh requirements.
   - Large ignored output verification requirements.
   - Checksum manifest requirements.
   - No raw/row-level ALA redistribution unless permission basis is explicitly
     recorded.

7. Release-execution goal outline.
   - Exact prerequisites.
   - Exact allowed commands/actions that should be considered later.
   - Exact non-goals that should remain blocked.
   - Stop conditions.

8. Questions or decisions for Barry.
   - Keep this small and decision-grade.
   - Do not ask Barry to inspect raw artefacts unless truly needed.

## Matrix Guidance

Use evidence from this goal to update matrix rows only where justified:

- R02 should remain a release/archive decision gate unless Barry/orchestrator
  actually authorizes an archive/DOI path.
- R05 should remain a release/archive decision gate unless all archive-scope
  decisions are actually resolved.
- R01/R04/R08/R09/M03 should not be reopened unless the decision packet finds a
  concrete contradiction.
- If a row is updated, use language that distinguishes "decision packet
  prepared" from "release action complete."

## Validation Gates For This Goal

Run these from the repo root:

```bash
git status --short --branch
git diff --check
test -f docs/release_blocker_decision_packet.md
test -f docs/goals/009-release-blocker-decision-packet/Stage4D_Release_Blocker_Decision_Packet.md
test -f docs/log/129_release_blocker_decision_packet.md
```

Run targeted consistency scans and classify hits:

```bash
rg -n "archive|DOI|release packaging|publication submission|upload|mint|no-move|release-gate|archived-proposed|restricted|row-level|raw ALA" docs/release_blocker_decision_packet.md analysis/reports/final_release_manifest.md docs/stage1_critique_resolution_matrix.md docs/stage_overview.md
rg -n "ef9d5ac7|e30a5fc5|fig_layerA_baseline_map|91cd628|9082f4f|f731562|evidence reconciliation|checksum" docs/release_blocker_decision_packet.md analysis/reports/final_release_manifest.md analysis/reports/stage4C_final_validation_report.md analysis/reports/final_reproducibility_audit_supplement.md
rg -n "pa_radiance_buffers_national_v0_3_0|pa_edge_profiles_national_v0_3_0|pa_buffer_validity_v0_3_0|pa_trends_v0_3_0|pa_risk_rankings_v0_3_0|pa_geometries_v0_3_0|pa_ibra_assignment_v0_3_0|pa_trend_bootstrap_summary_v0_3_0|microbats_occurrences_filtered|diurnal_birds_occurrences_filtered" docs/release_blocker_decision_packet.md analysis/reports/final_release_manifest.md
```

Do not treat hits as failures by themselves. The closeout must classify them.

## Expected Deliverables

- Decision packet:
  `docs/release_blocker_decision_packet.md`
- Goal closeout:
  `docs/goals/009-release-blocker-decision-packet/Stage4D_Release_Blocker_Decision_Packet.md`
- Stage log:
  `docs/log/129_release_blocker_decision_packet.md`
- Goal execution log update:
  `docs/goals/009-release-blocker-decision-packet/Log.md`
- Optional narrow pointers/status updates:
  `analysis/reports/final_release_manifest.md`
  `docs/stage1_critique_resolution_matrix.md`
  `docs/stage_overview.md`

## Decision Authority

`nightlight` may decide:

- the recommended option inside the decision packet;
- how to phrase trade-offs and risks;
- whether a matrix/status pointer update is justified;
- whether final archive/DOI work should be one goal or split into decision and
  execution goals.

Escalate to the DSIPA orchestrator if:

- the recommendation depends on remote compute or external archive service
  behavior;
- the decision packet cannot recommend an archive scope without Barry's
  scientific judgment;
- raw ALA or row-level processed ALA redistribution appears necessary;
- publication timing or journal strategy materially affects the release choice;
- completing the packet would require out-of-scope data, source, manuscript,
  archive, DOI, or remote actions.

Barry-level decisions must be explicit options or recommendations, not assumed
approvals.

## Wake-Up Requirement

When complete or blocked, send a short wake-up to the DSIPA orchestrator thread
`019eabf0-9051-7ce2-a0b6-d93b966d1562` with:

- whether Goal 009 is complete or blocked;
- the closeout path;
- the recommended release-blocker decision path;
- any decisions requiring Barry.

Then stop and wait.

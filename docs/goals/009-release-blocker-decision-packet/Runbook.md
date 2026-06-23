# Runbook: Goal 009 Release Blocker Decision Packet

Run from the repository root:

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
git rev-parse --short refs/remotes/origin/main
test -f docs/goals/009-release-blocker-decision-packet/Goal.md
```

Read the required files listed in `Goal.md`.

## Decision Packet Checks

Required files:

```bash
test -f docs/release_blocker_decision_packet.md
test -f docs/goals/009-release-blocker-decision-packet/Stage4D_Release_Blocker_Decision_Packet.md
test -f docs/log/129_release_blocker_decision_packet.md
```

Whitespace:

```bash
git diff --check
```

Targeted consistency scans:

```bash
rg -n "archive|DOI|release packaging|publication submission|upload|mint|no-move|release-gate|archived-proposed|restricted|row-level|raw ALA" docs/release_blocker_decision_packet.md analysis/reports/final_release_manifest.md docs/stage1_critique_resolution_matrix.md docs/stage_overview.md
rg -n "ef9d5ac7|e30a5fc5|fig_layerA_baseline_map|91cd628|9082f4f|f731562|evidence reconciliation|checksum" docs/release_blocker_decision_packet.md analysis/reports/final_release_manifest.md analysis/reports/stage4C_final_validation_report.md analysis/reports/final_reproducibility_audit_supplement.md
rg -n "pa_radiance_buffers_national_v0_3_0|pa_edge_profiles_national_v0_3_0|pa_buffer_validity_v0_3_0|pa_trends_v0_3_0|pa_risk_rankings_v0_3_0|pa_geometries_v0_3_0|pa_ibra_assignment_v0_3_0|pa_trend_bootstrap_summary_v0_3_0|microbats_occurrences_filtered|diurnal_birds_occurrences_filtered" docs/release_blocker_decision_packet.md analysis/reports/final_release_manifest.md
```

Classify hits manually. Do not treat scan hits as failures just because the
decision packet discusses release blockers.

## Forbidden Commands

Do not run:

```bash
make readiness
make pipeline
make layerA
make hpc-evidence
make hpc-full
make hpc-sync-dry-run
make hpc-sync
analysis/sync_to_deep_server.sh
analysis/deep_server_tmux_run.sh
analysis/zenodo_release_checklist.sh
```

Do not run archive, DOI, release, publication, remote, data-processing, or
large-file staging commands.

## Wake-Up

Send the DSIPA orchestrator a short wake-up with:

- complete or blocked;
- closeout path;
- recommended decision path;
- Barry/orchestrator decisions still required.

Then stop.

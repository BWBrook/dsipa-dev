# Runbook: Goal 007 Stage 4B Release Readiness

## Start

From `/Users/bwbrook/papers/dsipa-dev`:

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
test -f docs/goals/007-stage4B-release-data-availability-readiness/Goal.md
```

Record the results in the goal log.

## Execution Checklist

- Read `AGENTS.md` and the full Goal 007 packet.
- Read every required source listed in `Goal.md`.
- Create `analysis/reports/final_release_manifest.md`.
- Align data/release wording without claiming a final archive or DOI.
- Keep raw ALA and row-level processed ALA occurrence data excluded/restricted
  by default.
- Update decisions and matrix statuses only where justified.
- Run validation.
- Write the closeout and log.
- Wake the orchestrator.

## Classification Vocabulary

Use these terms consistently:

- `tracked`: committed to git and suitable for manuscript/release review.
- `archived-proposed`: not tracked; proposed for external archive pending
  Barry/orchestrator approval.
- `regenerated`: not archived by default; users should regenerate from scripts
  and documented inputs.
- `excluded`: not included in the manuscript package or archive proposal.
- `restricted`: not redistributed because licence/permission constraints apply.

If another term is necessary, define it in the manifest.

## Validation

Run:

```bash
git status --short --branch
git diff --check
test -f analysis/reports/final_release_manifest.md
test -f docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md
test -f docs/log/127_stage4B_release_data_availability.md
```

If manuscript data-availability wording changed, run:

```bash
make ms-check
```

Run and classify:

```bash
rg -n "archive|DOI|Zenodo|release manifest|external archive|mint|publish|upload" data/README.md README.md manuscript/text/manuscript_draft.md docs/decisions.md docs/stage1_critique_resolution_matrix.md analysis/reports/final_release_manifest.md
rg -n "raw ALA|row-level|occurrence tables|redistribut|restricted|excluded|mixed|CC-BY|CC BY|Creative Commons" data/README.md README.md manuscript/text/manuscript_draft.md docs/decisions.md analysis/reports/final_release_manifest.md
rg -n "layerB_ala_license_ledger|CRLF|normalized|normalised|checksum|SHA-256|sha256" data/README.md analysis/reports/evidence_reconciliation.md analysis/reports/final_release_manifest.md
rg -n "pa_radiance_buffers_national_v0_3_0|pa_edge_profiles_national_v0_3_0|pa_buffer_validity_v0_3_0|pa_trends_v0_3_0|pa_risk_rankings_v0_3_0|microbats_20260104T020628Z|diurnal_birds_20260104T020701Z|microbats_occurrences_filtered|diurnal_birds_occurrences_filtered" data/README.md analysis/reports/evidence_reconciliation.md analysis/reports/final_release_manifest.md
rg -n "tracked|archived-proposed|regenerated|excluded|restricted|Barry decision|orchestrator decision" analysis/reports/final_release_manifest.md
```

Do not treat `rg` output as automatically passing or failing. Classify hits
manually in the closeout.

## Wake-Up

When complete or blocked, send a short wake-up to:

```text
019eabf0-9051-7ce2-a0b6-d93b966d1562
```

Use this shape:

```text
Goal 007 complete.

Closeout memo: /Users/bwbrook/papers/dsipa-dev/docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md
```

If blocked, replace `complete` with `blocked` and point to the blocker note.

## Stop

Stop after the wake-up. Do not start Stage 4C without a new goal packet.

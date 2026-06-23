# Runbook: Goal 010 Option B Zenodo Archive Staging

Run from the repository root.

## Starting State

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
git rev-parse --short refs/remotes/origin/main
test -f docs/goals/010-optionB-zenodo-archive-staging/Goal.md
```

## Payload Presence

```bash
for f in \
  data/processed/pa_radiance_buffers_national_v0_3_0.csv \
  data/processed/pa_edge_profiles_national_v0_3_0.csv \
  data/processed/pa_buffer_validity_v0_3_0.csv \
  data/processed/pa_trends_v0_3_0.csv \
  data/processed/pa_risk_rankings_v0_3_0.csv \
  data/processed/pa_geometries_v0_3_0.csv \
  data/processed/pa_geometries_v0_3_0.gpkg \
  data/processed/pa_ibra_assignment_v0_3_0.csv \
  data/processed/pa_trend_bootstrap_summary_v0_3_0.csv
do
  if [ -e "$f" ]; then
    ls -lh "$f"
  else
    printf 'MISSING %s\n' "$f"
  fi
done
```

Confirm explicit ALA exclusions are not staged:

```bash
for f in \
  data/raw/ala_occurrences/microbats_20260104T020628Z.zip \
  data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip \
  data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz \
  data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz
do
  if [ -e "$f" ]; then
    ls -lh "$f"
  else
    printf 'ABSENT %s\n' "$f"
  fi
done
```

## Remote Recovery Boundary

If approved payload files are missing locally, first read the documented DSIPA
evidence paths in:

- `docs/log/108_remote_harness_evidence_reconciliation.md`
- `analysis/deep_server_tmux_run.sh`
- `analysis/reports/evidence_reconciliation.md`

Use only narrow commands against DSIPA-owned paths. Examples must be adapted to
the verified path actually present:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 deep-server-ts 'test -d /data/codex/artifacts/dsipa/20260514T072832Z-evidence6 && find /data/codex/artifacts/dsipa/20260514T072832Z-evidence6 -maxdepth 2 -type f | sort'
```

If copying is needed, copy only the nine approved payload files and verify
SHA-256 immediately after copy. Do not copy raw ALA or row-level ALA files.

## Expected Payload Checksums

```text
data/processed/pa_radiance_buffers_national_v0_3_0.csv 493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e
data/processed/pa_edge_profiles_national_v0_3_0.csv 9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888
data/processed/pa_buffer_validity_v0_3_0.csv 407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25
data/processed/pa_trends_v0_3_0.csv d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f
data/processed/pa_risk_rankings_v0_3_0.csv 554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a
data/processed/pa_geometries_v0_3_0.csv 781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b
data/processed/pa_geometries_v0_3_0.gpkg 0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11
data/processed/pa_ibra_assignment_v0_3_0.csv 3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf
data/processed/pa_trend_bootstrap_summary_v0_3_0.csv cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920
```

## Required Deliverable Checks

Adapt filenames if your implementation chooses clearer names, but all required
deliverable classes from `Goal.md` must exist.

```bash
test -f docs/goals/010-optionB-zenodo-archive-staging/Stage4E_Closeout.md
test -f docs/log/130_optionB_zenodo_archive_staging.md
find analysis/reports -maxdepth 1 -type f -iname '*optionB*' -print
find analysis/reports -maxdepth 1 -type f -iname '*zenodo*2026-06-23*' -print
```

## Validation

Whitespace:

```bash
git diff --check
```

Shell syntax, if the Zenodo checklist script changed:

```bash
bash -n analysis/zenodo_release_checklist.sh
```

Python tests, if Python helpers or evidence reconciliation code changed:

```bash
uv run pytest tests/python/test_evidence_reconciliation.py -q
```

Targeted scans:

```bash
rg -n "Option B|Zenodo|DOI|archive|upload|mint|checksum|staged|DOI pending|not minted" analysis/reports data/README.md manuscript/text docs
rg -n "raw ALA|row-level|occurrence tables|redistribut|restricted|excluded|ALA exception" analysis/reports data/README.md manuscript/text docs
rg -n "pa_radiance_buffers_national_v0_3_0|pa_edge_profiles_national_v0_3_0|pa_buffer_validity_v0_3_0|pa_trends_v0_3_0|pa_risk_rankings_v0_3_0|pa_geometries_v0_3_0|pa_ibra_assignment_v0_3_0|pa_trend_bootstrap_summary_v0_3_0" analysis/reports data/README.md docs
rg -n "ef9d5ac7|e30a5fc5|fig_layerA_baseline_map|baseline figure|evidence reconciliation" analysis/reports docs src/python/dsipa/evidence_reconciliation.py
```

Classify hits manually in the closeout.

## Forbidden Commands And Actions

Do not run:

```bash
make readiness
make pipeline
make layerA
make hpc-evidence
make hpc-full
make hpc-sync-dry-run
make hpc-sync
analysis/deep_server_tmux_run.sh --mode evidence
analysis/deep_server_tmux_run.sh --mode full
analysis/sync_to_deep_server.sh
```

Do not upload to Zenodo or any other external archive. Do not mint or reserve a
DOI. Do not create a GitHub release. Do not submit the manuscript. Do not copy
or stage raw ALA downloads or row-level processed ALA occurrence tables.

## Wake-Up

Send the DSIPA orchestrator a short wake-up with:

- complete or blocked;
- closeout path;
- manifest/metadata paths;
- staging location, if any;
- checksum status;
- ALA-exclusion confirmation;
- next required external-upload/DOI-mint decision or goal.

Then stop.

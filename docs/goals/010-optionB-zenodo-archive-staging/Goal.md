# Goal 010: Option B Zenodo Archive Staging

## Objective

Execute the Barry-approved release decision for **Option B via a Zenodo-style
DOI route with no raw/row-level ALA redistribution exception**, stopping before
any external archive upload, DOI minting, GitHub release, publication
submission, or final DOI citation.

This goal is complete when the repository contains a reviewed, DOI-ready
archive-staging evidence package that:

- records Barry's decisions from 2026-06-23:
  - Option B archive scope approved;
  - Zenodo-style DOI route approved;
  - no raw ALA or row-level processed ALA redistribution exception;
- verifies or recovers the approved Layer A archive payload;
- creates a checksum manifest for the approved archive payload;
- prepares Zenodo-style deposit metadata and file-list wording without
  claiming that a DOI exists;
- refreshes or supplements the release evidence surface so the current tracked
  baseline figure checksum is no longer treated as unexplained drift;
- keeps raw ALA downloads and row-level processed ALA occurrence tables out of
  the release/archive payload;
- updates release-facing documentation only to the extent justified by the
  approved decision and verified evidence; and
- produces a closeout memo that clearly says whether the package is ready for
  orchestrator review before a later external-upload/DOI-mint goal.

## Why This Matters

Goal 009 gave Barry a decision packet for the last release blockers. Barry has
now resolved the major strategic choices:

- proceed with the recommended source/manuscript plus Layer A archive path;
- use a Zenodo-style DOI route; and
- do not make a raw/row-level ALA redistribution exception.

The next risk is operational, not scientific: the local checkout does not
currently contain most of the large `archived-proposed` Layer A files, and the
existing Zenodo checklist script predates the final Option B scope. Goal 010
should turn the decision into a precise, reviewable archive package and
evidence surface, without prematurely publishing anything externally.

## Operating Mode

Release-staging, manifest verification, narrow documentation updates, and
evidence-surface refresh.

This is **not** a science goal, not a manuscript rewrite goal, and not an
external publication goal.

## Authorized Decision State

Treat these as already decided by Barry and the DSIPA orchestrator:

- Archive scope: Option B from `docs/release_blocker_decision_packet.md`.
- Archive route: Zenodo-style DOI archive, or a functionally equivalent DOI
  research-data archive if Zenodo itself proves unavailable later.
- ALA policy: no raw ALA downloads and no row-level processed ALA occurrence
  tables in the release/archive package.

Do not ask Barry to re-decide these unless you find a concrete blocker that
invalidates one of them.

## Approved Option B Archive Payload

The release archive payload is exactly these Layer A outputs:

- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `data/processed/pa_trends_v0_3_0.csv`
- `data/processed/pa_risk_rankings_v0_3_0.csv`
- `data/processed/pa_geometries_v0_3_0.csv`
- `data/processed/pa_geometries_v0_3_0.gpkg`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`

Expected SHA-256 values are recorded in:

- `analysis/reports/final_release_manifest.md`
- `data/README.md`
- `analysis/reports/evidence_reconciliation.json`
- `src/python/dsipa/evidence_reconciliation.py`

If a file is missing locally, you may recover it only from DSIPA-owned project
evidence locations documented in the repository, such as the `deep-server`
evidence/artifact paths in `docs/log/108_remote_harness_evidence_reconciliation.md`
or the project remote checkout/harness paths in `analysis/deep_server_tmux_run.sh`.
Limit remote inspection and copying to DSIPA project paths and the exact
approved payload. Do not inspect unrelated remote folders.

## Explicit Exclusions

These are **not** part of the archive payload and must not be staged,
compressed, uploaded, or described as redistributed:

- `data/raw/ala_occurrences/microbats_20260104T020628Z.zip`
- `data/raw/ala_occurrences/diurnal_birds_20260104T020701Z.zip`
- `data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz`
- `data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz`
- any other raw ALA download;
- any other row-level processed ALA occurrence table.

Derived Layer B summaries, reports, figures, and licence/provenance ledgers may
remain tracked as already classified by the release manifest, but they are not
new archive-payload files for this goal.

## Authorized Review Surface

Create or update:

- `docs/goals/010-optionB-zenodo-archive-staging/Stage4E_Closeout.md`
- `docs/goals/010-optionB-zenodo-archive-staging/Log.md`
- `docs/log/130_optionB_zenodo_archive_staging.md`
- one or more tracked release-staging reports under `analysis/reports/`, for
  example:
  - `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.md`
  - `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.json`
  - `analysis/reports/zenodo_optionB_metadata_2026-06-23.md`
  - `analysis/reports/zenodo_release_checklist_2026-06-23.md`

You may update, narrowly:

- `analysis/zenodo_release_checklist.sh`, if it is the right place to encode
  the approved nine-file Option B payload.
- A small new helper under `analysis/` or `src/python/dsipa/` if needed to make
  archive-payload manifest generation reproducible.
- `src/python/dsipa/evidence_reconciliation.py`, only if you can justify a
  narrow evidence-refresh update for the current accepted baseline-figure
  checksum without conflating release payload files with restricted ALA files.
- tests directly covering any helper or evidence-reconciliation code you change.
- `docs/decisions.md`, to record Barry's Option B/Zenodo/no-ALA-exception
  decision.
- `analysis/reports/final_release_manifest.md`, to reflect the approved
  decision and point to the new archive-staging manifest.
- `data/README.md`, to reflect the approved route and staged/verified payload
  without citing a DOI that does not yet exist.
- `manuscript/text/manuscript_draft.md`, only in the data/code availability
  section and only to keep wording honest: approved route and pending DOI are
  allowed; claiming a minted DOI is not.
- `docs/stage1_critique_resolution_matrix.md` and `docs/stage_overview.md`, to
  update release-gate status if evidence justifies it.

Keep edits minimal and release-focused.

Do not edit:

- generated figures under `manuscript/figures/`;
- scientific result tables except for release-staging manifests;
- Layer A or Layer B modelling code for scientific changes;
- raw or processed science data content except for restoring/copying the exact
  approved Layer A payload into ignored local/staging paths;
- `docs/ref_doi.txt` unless you have an actual DOI or a clearly documented
  reason to mark it still parked;
- GitHub release metadata;
- journal submission files.

If an out-of-scope edit seems necessary, record it as a blocker or later-goal
item rather than performing it.

## Scope

In scope:

- inspect and record current repo state;
- confirm local presence/absence of the nine approved payload files;
- recover missing approved Layer A payload files from documented DSIPA evidence
  stores if possible;
- keep restored or staged large files out of git;
- verify SHA-256 checksums for all nine approved payload files;
- create a machine-readable and human-readable archive manifest;
- prepare Zenodo-style title, description, creator/affiliation notes, related
  identifiers, licence/provenance notes, keywords, file list, and checksum
  wording;
- prepare or refresh a Zenodo checklist that matches the final Option B scope;
- refresh or supplement release evidence for the current tracked
  `manuscript/figures/fig_layerA_baseline_map.png` checksum:
  `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`;
- record that the older expected baseline-map hash
  `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`
  is superseded by accepted Stage 2 figure work, not unexplained drift;
- update release-facing docs to say Option B is approved and staged/verified if
  the evidence supports that;
- preserve no raw/row-level ALA redistribution.

Out of scope:

- no external archive upload;
- no DOI minting or DOI reservation;
- no final DOI citation in manuscript, README, data README, or release
  manifest;
- no GitHub release;
- no publication submission;
- no new science;
- no Layer A or Layer B data processing, modelling, figure regeneration, or
  ALA download;
- no raw ALA or row-level processed ALA redistribution;
- no full pipeline rerun;
- no remote compute run;
- no broad remote filesystem inspection;
- no commits, pushes, merges, PRs, or tags.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/release_blocker_decision_packet.md`
- `docs/goals/009-release-blocker-decision-packet/Stage4D_Release_Blocker_Decision_Packet.md`
- `analysis/reports/final_release_manifest.md`
- `analysis/reports/stage4C_final_validation_report.md`
- `analysis/reports/final_reproducibility_audit_supplement.md`
- `analysis/reports/evidence_reconciliation.md`
- `analysis/reports/evidence_reconciliation.json`
- `analysis/reports/zenodo_release_checklist_2026-01-04.md`
- `analysis/zenodo_release_checklist.sh`
- `src/python/dsipa/evidence_reconciliation.py`
- `data/README.md`
- `manuscript/text/manuscript_draft.md`
- `docs/decisions.md`
- `docs/log/108_remote_harness_evidence_reconciliation.md`
- `analysis/deep_server_tmux_run.sh`
- `analysis/sync_to_deep_server.sh`

If another repo-local file is clearly needed for release-staging evidence,
read it. Do not read outside `/Users/bwbrook/papers/dsipa-dev` except for
narrow DSIPA-owned remote payload checks/copies explicitly described above.

## Starting State Checks

Record:

- `pwd`
- `git status --short --branch`
- `git rev-parse --short HEAD`
- `git rev-parse --short refs/remotes/origin/main` if available
- whether this Goal 010 packet is present
- local presence/absence of all nine approved payload files
- local presence/absence of the four explicitly excluded raw/row-level ALA
  files, only to confirm they are not accidentally staged

The DSIPA orchestrator created this packet after accepting and publishing Goal
009 at commit `b1c1539` and after Barry approved:

> Option B via Zenodo-style DOI; no ALA exception.

Treat files under `docs/goals/010-optionB-zenodo-archive-staging/` as
authorized working instructions.

## Data, Compute, Remote, And Staging Policy

- Use the local Mac mini checkout as the control surface.
- You may run narrow local commands to inspect, copy, checksum, and stage the
  approved nine-file Layer A payload.
- If files are missing locally, you may run narrow SSH/rsync/scp checks against
  documented DSIPA-owned `deep-server` project paths. Use short timeouts and
  record the exact commands and paths.
- Do not start tmux jobs, remote compute, full pipeline runs, or data
  regeneration.
- Do not run `analysis/sync_to_deep_server.sh` unless you are only doing a
  dry-run that is necessary to understand remote paths. Prefer direct narrow
  payload copy from existing evidence locations.
- Do not run `analysis/deep_server_tmux_run.sh` unless only `--help` is needed.
- Put any large staged archive payload under ignored paths such as `artefacts/`
  or another clearly ignored local staging path. Do not commit large payload
  files.
- If you restore approved large files into `data/processed/`, remember they
  are ignored by git; report them as local release-staging artefacts, not
  tracked changes.

## Expected Deliverables

At minimum, produce:

1. A human-readable Option B archive manifest with:
   - repo commit and working-tree state;
   - all nine approved payload files;
   - file sizes;
   - SHA-256 checksums;
   - source/recovery location for each file;
   - local staging location, if created;
   - explicit ALA exclusions;
   - DOI status: not minted.

2. A machine-readable companion manifest (`.json` or `.csv`) suitable for later
   upload/package automation.

3. A Zenodo-style metadata note with:
   - proposed title;
   - proposed creators/contributors as can be inferred from repo docs;
   - proposed description;
   - related identifiers and source repository placeholder;
   - licence/provenance notes for CAPAD/IBRA/nightlights-derived Layer A data;
   - explicit exclusion note for raw/row-level ALA data;
   - file list and checksum pointer;
   - "DOI pending; do not cite until minted."

4. A closeout memo under this goal directory explaining:
   - what was verified;
   - what was staged, if anything;
   - what remains for the later external-upload/DOI-mint goal;
   - whether any blocker remains.

5. A dated stage log under `docs/log/`.

## Validation Gates For This Goal

Run from the repo root:

```bash
git status --short --branch
git diff --check
```

Run file-presence checks for the required deliverables you create.

Run checksum verification for all nine approved payload files if they are
available locally or staged locally.

If you modify shell scripts:

```bash
bash -n analysis/zenodo_release_checklist.sh
```

If you modify Python helpers or evidence reconciliation code:

```bash
uv run pytest tests/python/test_evidence_reconciliation.py -q
```

If you generate or refresh a Zenodo checklist through the script, run the
script and record its output path.

Run targeted release-policy scans and manually classify the hits:

```bash
rg -n "Option B|Zenodo|DOI|archive|upload|mint|checksum|staged|DOI pending|not minted" analysis/reports data/README.md manuscript/text docs
rg -n "raw ALA|row-level|occurrence tables|redistribut|restricted|excluded|ALA exception" analysis/reports data/README.md manuscript/text docs
rg -n "pa_radiance_buffers_national_v0_3_0|pa_edge_profiles_national_v0_3_0|pa_buffer_validity_v0_3_0|pa_trends_v0_3_0|pa_risk_rankings_v0_3_0|pa_geometries_v0_3_0|pa_ibra_assignment_v0_3_0|pa_trend_bootstrap_summary_v0_3_0" analysis/reports data/README.md docs
rg -n "ef9d5ac7|e30a5fc5|fig_layerA_baseline_map|baseline figure|evidence reconciliation" analysis/reports docs src/python/dsipa/evidence_reconciliation.py
```

Classify hits manually. Scan hits are not failures just because the goal
discusses release staging.

Do not run `make ms-check`, `make test`, `make build`, `make readiness`,
pipeline targets, manuscript builds, package builds, remote compute, or archive
upload tooling unless a change you made creates a narrow, justified need. If
you believe one of these is necessary, record why in the closeout and stop for
orchestrator review rather than broadening the goal.

## Stop Conditions

Stop and wake the DSIPA orchestrator if:

- any of the nine approved payload files cannot be found in documented DSIPA
  evidence locations;
- any approved payload checksum differs from the pinned release manifest and
  you cannot explain it from accepted evidence;
- satisfying the goal would require new data processing, model runs, figure
  regeneration, or ALA downloads;
- satisfying the goal would require external archive upload or DOI minting;
- release-facing wording would need to cite a DOI before one exists;
- a raw ALA or row-level processed ALA file appears in the archive payload;
- remote access fails after a narrow, documented attempt and the missing files
  are not available locally.

## Git And Publication Policy

- `nightlight` must not commit, push, merge, tag, open a PR, create a GitHub
  release, upload an archive, or mint/reserve a DOI.
- The DSIPA orchestrator will review, accept, commit, and push accepted Goal
  010 artefacts.
- Do not contact Barry or Chief.

## Wake-Up

When done or blocked, send the DSIPA orchestrator a short wake-up with:

- complete or blocked;
- closeout path;
- archive manifest path(s);
- staging location, if any;
- checksum status for the nine approved files;
- explicit confirmation that raw/row-level ALA files were excluded;
- whether the later external-upload/DOI-mint goal is ready.

Then stop.

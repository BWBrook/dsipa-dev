# Final Reproducibility Audit Supplement

Status: Stage 4C supplement to the existing reproducibility and evidence
reports. This file does not replace `analysis/reports/reproducibility_audit.md`
or `analysis/reports/evidence_reconciliation.md`; it records the current local
validation state at accepted Goal 007 commit `9082f4f`.

Generated: 2026-06-23 by `nightlight` for Goal 008.

## Checkout and packet

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD: `9082f4f`
- Remote-tracking HEAD: `origin/main` at `9082f4f`
- Starting status: `## main...origin/main` plus untracked
  `docs/goals/008-stage4C-final-validation-reproducibility-audit/`.
- Packet read: `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md` under the Goal
  008 directory.

## Local reproducibility command ledger

The following authorized commands were run locally:

- `make ms-check`: passed. Manuscript checks, makedoc tests, reference audit,
  author metadata injection, and build check passed. Reference audit reported
  30 bibliography keys, 26 cited keys, 0 unknown keys, and 4 unused non-fatal
  keys.
- `make test`: passed with `40 passed, 9 skipped in 1.56s`. Skips are expected
  because large ignored national evidence outputs are absent from the local git
  checkout.
- `make build`: passed and produced package artefacts under `/tmp/dsipa-build`.
- `uv run python -m dsipa.evidence_reconciliation --output-md /tmp/dsipa_stage4c_evidence_reconciliation.md --output-json /tmp/dsipa_stage4c_evidence_reconciliation.json --audit-md /tmp/dsipa_stage4c_reproducibility_audit.md --write-audit`:
  command passed and wrote only to `/tmp`.
- Manual `rg` scans for claim discipline, denominators, release/data
  availability, references, and manifest consistency were run and classified in
  `analysis/reports/stage4C_final_validation_report.md`.
- `git diff --check`: passed before Stage 4C edits; a final pass was run after
  report edits.

No authorized validation command reproduced a `uv` `VIRTUAL_ENV` mismatch
warning.

## Current evidence status

The `/tmp` evidence reconciliation run reports:

- Expected required files: 38
- Present files: 28
- Checksum-verified files: 27
- Missing required files: 10
- Checksum mismatches: 1

The 10 missing files are the large ignored Layer A national outputs plus the
restricted row-level Layer B occurrence tables already treated as
release-gated by the Stage 4B manifest. Their absence prevents a complete local
release-clean proof, but does not by itself imply manuscript science drift.

The one checksum mismatch is the tracked baseline figure:

- Path: `manuscript/figures/fig_layerA_baseline_map.png`
- Current tracked SHA-256:
  `ef9d5ac7e2dd37a41e7574ca89736fee682b060f10809db4779713925a0e458e`
- Older evidence expected SHA-256:
  `e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3`

The file is not locally dirty. The difference traces to accepted Stage 2 figure
work in commit `896131a`, so the old evidence snapshot is stale for this
tracked file. A final release/archive goal must refresh the evidence
reconciliation metadata against the current tracked figure set.

## Release blockers

The following blockers require orchestrator or Barry-level release decisions
before archive/DOI/release/publication work:

1. External archive scope for `archived-proposed` large Layer A outputs.
2. External archive record and DOI policy.
3. A clean/current evidence reconciliation after the archive-scope decision and
   after the current tracked baseline figure hash is accepted.
4. Any exception to the default restricted/excluded treatment of raw ALA
   downloads and row-level processed ALA occurrence tables.

## Review iteration: manifest checksum consistency

The Stage 4C review iteration corrected two inherited checksum mismatches in
`analysis/reports/final_release_manifest.md` for the archived-proposed
`pa_geometries_v0_3_0` CSV and GPKG rows. The corrected values now match
`analysis/reports/evidence_reconciliation.json`, and the post-correction
manifest-vs-evidence comparison reports every compared row as `OK`.

`make ms-check`, `make test`, and `make build` were not rerun for this review
iteration because only documentation/report checksums changed.

## Supplement conclusion

Local manuscript checks, tests, and package build pass at `9082f4f`. The
checkout is not release-clean because required large ignored outputs are absent
locally and one tracked figure hash is stale relative to the older evidence
snapshot. Stage 4C therefore recommends no move to release, archive, DOI, or
publication submission until those blockers are resolved.

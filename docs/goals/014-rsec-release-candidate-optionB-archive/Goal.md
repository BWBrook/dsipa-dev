# Goal 014: RSEC Release Candidate — Option B Archive

## Objective

Produce one final pre-publication candidate for the DSIPA RSEC package. The
candidate integrates four already-agreed surfaces without changing the
science: (A) recovery of the accepted Goal 011 Option B nine-file Layer A
archive candidate, (B) reconciliation of current release reports, (C)
DSIPA/Makedoc dual-build provenance, and (D) RSEC submission assets.

This is a bounded release-candidate and submission-preparation goal. It does
not publish, upload, mint, reserve, submit, tag, or release anything
externally.

## Starting State

- Action repo: `/Users/bwbrook/papers/dsipa-dev`
- Required branch: `main`
- Required HEAD and `origin/main`:
  `f5788ea4ad62237a95bf323930ec477107e7c2f3`
- Required starting status: clean (`## main...origin/main`)
- Accepted manuscript contract: Goal 013 RSEC consolidation
- Accepted Layer A contract:
  `settings/layerA_reference_contract_v0_3_0.json`
- Accepted Goal 011 recovery source (read-only):
  `deep-server-ts:/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation/payload/`
- Local ignored candidate destination:
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`

Stop before mutation if branch, HEAD, remote-tracking HEAD, or clean status
differs. Do not reset, clean, reconcile, overwrite, or interpret unrelated
work.

## Frozen Release And Scientific Contract

### Layer A archive

The archive payload is exactly these nine Goal 010 outputs, with hashes and
classifications taken from the accepted Goal 011 archive evidence and the
reference contract. The Goal 011 hashes are authoritative; do not substitute
Goal 012 reserializations or pre-Goal 011 historical hashes.

```text
data/processed/pa_radiance_buffers_national_v0_3_0.csv
data/processed/pa_edge_profiles_national_v0_3_0.csv
data/processed/pa_buffer_validity_v0_3_0.csv
data/processed/pa_trends_v0_3_0.csv
data/processed/pa_risk_rankings_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.csv
data/processed/pa_geometries_v0_3_0.gpkg
data/processed/pa_ibra_assignment_v0_3_0.csv
data/processed/pa_trend_bootstrap_summary_v0_3_0.csv
```

The nine payload files must total exactly `265,783,139` bytes. The candidate
directory may additionally contain only a README, a JSON manifest, and a
`SHA256SUMS` file. The manifest must preserve the nine-file allowlist,
Goal 011 hashes, sizes, classifications, source identity, and recovery
timestamp. Six files are exact. The accepted non-exact radiance, edge, and
GPKG limitations must be documented as semantic/container limitations rather
than silently reserialized. The legacy risk-rankings filename is categorical
screening output, not a priority ranking.

Recovery is narrow and read-only: use only the stated remote payload source,
copy into the ignored local destination, and never overwrite
`data/processed/`. Prove the allowlist and prove zero raw or row-level ALA
content. A source, hash, size, allowlist, or ALA mismatch is an immediate stop.

### Release surfaces

Current active report surfaces must reconcile to ring-1 `1,432/12.9%`:

- `analysis/reports/layerA_denominators_and_censoring.md`;
- `analysis/reports/layerA_table1_candidate.md`; and
- `analysis/reports/final_release_manifest.md`.

Create dated 2026-07-24 Option B archive-manifest Markdown/JSON, Zenodo
metadata, and release checklist surfaces. Narrowly update `data/README.md`,
`docs/decisions.md`, and `docs/stage_overview.md`. Preserve Goal 010's
blocked/history record, Goal 011/012 reconciliation, and historical `1,427`
only as historical reconciliation. Do not make a DOI claim.

### Build provenance

DSIPA owns a new `analysis/annotate_makedoc_manifest.py`, a focused change to
`analysis/makedoc.sh`, a new
`tests/python/test_makedoc_provenance.py`, and the corresponding
`settings/build.yaml` change. The annotation must preserve the upstream
manifest `git` field as tool identity. After every successful Makedoc `check`
or `all`, refresh `repository_provenance.source` and `.build_tool` with
sha/branch/dirty state, even when the upstream manifest is unchanged. A
failed upstream command must propagate its failure and must not annotate.
Do not edit the upstream Makedoc checkout. Implement this with TDD and run
the full test suite.

### RSEC submission assets

Use the exact accepted title:

> Detectable change in dark-sky integrity across Australia’s protected areas

Use article type **Original Research**. Keep the combined manuscript draft
unchanged as the source; make the RSEC submission profile main-text-only and
add a supplementary profile. The only build-profile configuration source is
`settings/build.yaml`: combined `draft` remains 1.5-spaced; `submission` is
main-only, double-spaced, continuously line-numbered, writes to
`build/submission`, and uses stem `dsipa_rsec_main`; `supplementary` is
double-spaced, continuously line-numbered, writes to `build/supplementary`,
and uses stem `dsipa_rsec_supplementary`. Add submission assets under
`manuscript/submission/rsec/` for the README/checklist, submission metadata
and counts/running title, cover-letter draft, declarations draft, and
supplementary frontmatter. Human-confirmed fields must be marked for
Barry confirmation: creators/ORCID/affiliations/contributions, rights and
licence, date/version, funding, conflict of interest, AI statement, sole
submission, correspondence address, DOI/URL, and final external
authorization. Do not invent declarations or science, and do not edit
manuscript text, references, figures, or figure files.

Record these official sources with retrieval date `2026-07-24` (canonical URLs):

- Zenodo create: <https://help.zenodo.org/docs/deposit/create-new-upload/>;
- Zenodo about: <https://help.zenodo.org/docs/deposit/about-records/>;
- Zenodo reserve DOI:
  <https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/>; and
- RSEC author guidelines:
  <https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/author-guidelines>.

Source checking is an execution requirement; no network access occurs during
packet creation.

## External-Action Block

The following remain blocked and are not authorized: Zenodo draft or upload,
DOI reservation or minting, Git tag/release, Wiley login or submission, fees,
or an open-access agreement. No commit or push occurs before orchestrator
acceptance.

## Permitted Mutation Boundary

Implementation may create or modify only the following tracked surfaces plus
ignored candidate/build artefacts:

### Release and documentation

- `analysis/reports/layerA_denominators_and_censoring.md`
- `analysis/reports/layerA_table1_candidate.md`
- `analysis/reports/final_release_manifest.md`
- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.md`
- `analysis/reports/optionB_layerA_archive_manifest_2026-07-24.json`
- `analysis/reports/zenodo_optionB_metadata_2026-07-24.md`
- `analysis/reports/zenodo_release_checklist_2026-07-24.md`
- `data/README.md`
- `docs/decisions.md`
- `docs/stage_overview.md`

### Makedoc provenance

- `analysis/annotate_makedoc_manifest.py` (new)
- `analysis/makedoc.sh`
- `settings/build.yaml`
- `tests/python/test_makedoc_provenance.py` (new)

### RSEC submission assets

- `manuscript/submission/rsec/README.md`
- `manuscript/submission/rsec/submission_checklist.md`
- `manuscript/submission/rsec/submission_metadata.md`
- `manuscript/submission/rsec/submission_counts.md`
- `manuscript/submission/rsec/cover_letter_draft.md`
- `manuscript/submission/rsec/declarations_draft.md`
- `manuscript/submission/rsec/supplementary_frontmatter.md`

### Goal and chronology records

- this Goal 014 packet (`Goal.md`, `Plan.md`, `Runbook.md`, `Log.md`);
- `docs/goals/014-rsec-release-candidate-optionB-archive/RSEC_Release_Candidate_Closeout.md`;
- `docs/log/134_rsec_release_candidate.md`.

Ignored files under `artefacts/optionB_layerA_archive_candidate_2026-07-24/`
and normal build outputs are permitted only when produced by the prescribed
workflow. Do not modify raw data, `data/processed/`, manuscript science,
references, figure images, upstream Makedoc, or unrelated files.

## Acceptance Criteria

- Baseline and final footprint are exact; no commit or push occurs.
- Narrow remote rsync reads only the stated Goal 011 source and preserves
  read-only provenance.
- Exactly nine payload files, exact allowlist, sizes, total bytes, hashes,
  classifications, JSON manifest, README, and `SHA256SUMS` are proven.
- Zero raw or row-level ALA files are present in the candidate.
- Six exact files and accepted radiance/edge/GPKG non-exact limitations are
  documented; active-versus-historical scans show only allowed historical
  `1,427` references.
- Active reports show `1,432/12.9%`; Goal 010 blocked/history and Goal
  011/012 reconciliation remain explicit.
- Makedoc provenance tests pass, including successful `check`/`all`, unchanged
  upstream manifests, failure propagation, and no annotation after failure;
  `make test` and the full tests pass.
- RSEC draft/submission/supplementary checks and builds pass. Main PDF/DOCX
  and authoritative SI PDF separation is proved; the autogenerated SI DOCX is
  diagnostic and non-submittable. Main text is at most 5,000 words excluding
  acknowledgements, references, and table/figure legends; abstract is at most
  300 words; keywords number 4–6; and main/SI display references are
  consistent. Title, article type, citation, and display checks pass.
- Dual identities (DSIPA repository and upstream Makedoc tool) remain clear.
- One focused repair pass is allowed. Stop on source/hash/allowlist mismatch,
  ALA leakage, new science, unsafe rights claim, scope expansion, or failure
  after the repair.
- Closeout records files, candidate inventory/hashes, builds/tests/provenance,
  human decisions, blocked external actions, and no commit/push.

## Non-Goals

No new analysis, data processing, manuscript scientific-content/reference/
figure edits, external
archive action, DOI action, Git release, Wiley submission, fee or licence
agreement, raw/row-level ALA redistribution, or broad documentation rewrite.

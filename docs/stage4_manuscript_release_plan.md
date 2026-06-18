# Stage 4 Manuscript And Release Plan

Date: 2026-06-18

## Summary Recommendation

Proceed to Stage 4 as three separate goals, not as one broad finalisation pass:

1. Stage 4A: evidence-led manuscript synthesis and claim discipline.
2. Stage 4B: data availability, release manifest, archive/DOI, and checksum
   policy readiness.
3. Stage 4C: final manuscript/build/reproducibility validation.

Stage 4 should make the paper more decisive where the evidence is already
strong, especially for Layer A dark-sky integrity, while preserving the
accepted Layer B stance: conservative, provider-bounded, presence-only,
falsification-limited, and not causal or population-trend evidence.

Do not combine manuscript rewriting with archive policy or final validation.
Those are different risk classes and need separate stop gates.

## Accepted Evidence State

Stage 2 and Stage 3 are accepted for planning purposes.

Layer A is the primary contribution. The accepted evidence supports these
paper-facing claims:

- The protected-area universe is n = 11,133.
- Inside-baseline and inside-trend eligibility is n = 4,426 under the minimum
  valid-pixel and valid-year rules.
- The 2024 inside mean-radiance distribution is strongly floor dominated:
  3,844 of 4,426 eligible protected areas, or 86.9 percent, have zero inside
  mean radiance.
- Inside mean-radiance trends are also floor dominated: 3,969 of 4,426 eligible
  protected areas, or 89.7 percent, have exactly zero inside slopes.
- A minority non-zero tail exists: 420 eligible protected areas have positive
  inside slopes.
- The 1 km unprotected-land buffer retention denominator is n = 3,858, with
  Q1 = 305 concurrent inside/buffer brightening, Q2 = 55 internal brightening,
  Q3 = 3,308 stable/non-detect, and Q4 = 190 external-pressure cases.
- Complete interior-ring profiles are feasible for only n = 383 protected
  areas, so edge/penetration language must remain conditional.
- Table S1 is category-safe and uncertainty-aware; ranks are triage aids, not
  precise ordinal claims.

Layer B is retained only as weak secondary evidence. The accepted evidence
supports these statements:

- The primary provider-matched design uses NSW BioNet dr368 records with
  50,281 microbat and 50,281 passerine records.
- Primary discrimination is weak: AUC about 0.545 and log loss about 0.689.
- Block-shuffle and IBRA x year shuffle falsification are near null, with AUC
  about 0.505 and 0.517.
- Full multi-provider sensitivity is descriptive only because provider/state
  confounding returns.
- Table S2 is filled from existing reports and keeps the result explicitly
  associational, provider-bounded, and not a population trend or decline.
- ALA occurrence licences are mixed; raw ALA occurrence downloads and row-level
  processed occurrence tables must not be redistributed unless permissions are
  explicitly resolved.

Release and reproducibility evidence is useful but not yet publication-ready:

- `analysis/reports/evidence_reconciliation.md` verifies 38 of 38 expected
  files with no checksum mismatches, but records a dirty pre-final state.
- `analysis/reports/reproducibility_audit.md` records the same pre-final commit
  and dirty working tree.
- The Zenodo checklist files identify large Layer A outputs that need external
  archive handling.
- `docs/ref_doi.txt` is a DOI seed list, not a publication/archive decision.
- `data/README.md` records provenance and checksums, but still needs final
  archive DOI, release-manifest, ALA redistribution, and checksum convention
  reconciliation.

## Stage 4 Objective

Stage 4 should convert the hardened evidence package into a publication-facing
manuscript and release-ready reproducibility surface. The stage is complete
only when:

- Results, Discussion, tables, captions, and data availability are traceable to
  accepted evidence.
- Claim-discipline scans and manual review confirm no unsupported causal,
  population-decline, population-trend, or national-biodiversity claim.
- Release/archive policy is explicit, especially for large ignored outputs and
  raw ALA occurrence data.
- Final validation records manuscript checks, package/build checks, checksum
  reconciliation, and reproducibility audit status from a clean or explicitly
  documented state.

## Stage 4 Non-Goals

- No new Layer A analysis unless final validation exposes a concrete
  evidence/manuscript mismatch.
- No new Layer B modelling, ALA downloads, or occurrence processing unless a
  future explicit science goal is opened.
- No raw ALA redistribution by default.
- No archive/DOI publication without explicit orchestrator and Barry approval.
- No silent rewriting of historical WP roadmap content. Stale language should
  be redirected, not erased.

## Issue Map

| ID | Stage 4 action | Evidence source | Validation gate | Escalation boundary |
| --- | --- | --- | --- | --- |
| B01 | Keep paper and release language mixed-licence aware; verify final release/archive manifests do not imply blanket CC-BY or raw ALA redistribution. | `layerB_ala_license_ledger`, `data/README.md`, Stage 3A closeout, manuscript data availability. | Licence scan over manuscript, data README, and release manifest; manual check of ALA-derived artefact inclusion policy. | Barry/orchestrator if raw ALA or row-level processed ALA data are proposed for archive. |
| B11 | Convert Stage 3 boundary into a final derived-output-only release policy unless permissions allow more. | `data/README.md`, evidence reconciliation, Stage 3A closeout. | Data availability and release manifest state which ALA artefacts are shared, excluded, or regenerated by users. | Barry/orchestrator for any publication package containing raw ALA downloads or processed row-level occurrence tables. |
| R01 | Refresh or supplement the reproducibility audit after accepted Stage 4 changes from a clean or explicitly documented state. | `analysis/reports/reproducibility_audit.md`, evidence reconciliation, final git state. | Final audit records release commit, dirty/clean status, command set, skipped large-output assumptions, and expected runtime class. | Orchestrator if clean-state audit requires remote compute or data reruns. |
| R02 | Decide external archive/DOI policy for large ignored outputs and checksum manifest. | Zenodo checklists, `docs/ref_doi.txt`, `data/README.md`, evidence reconciliation. | Archive DOI or explicit no-DOI/retrieve-from-sources policy appears in data availability, release manifest, and data README. | Barry decision required before minting DOI, publishing archive, or citing a parked DOI. |
| R04 | Add `uv` warning/troubleshooting language only if it remains relevant in documented commands. | Mac readiness log, README, reproducibility audit. | README or reproducibility audit explains expected `uv`/`VIRTUAL_ENV` behavior, or records that no warning was reproduced. | Orchestrator if fixing the warning requires environment or tooling changes beyond docs. |
| R05 | Create final release manifest and classify which large outputs are archived, reproducible-only, or excluded. | Evidence reconciliation inventory, Zenodo checklists, data README. | Manifest covers required large Layer A files, Layer B derived summaries, figures, reports, checksums, and excluded raw ALA assets. | Barry/orchestrator for archive scope, DOI timing, and restricted-data trade-offs. |
| R06 | Update stale governance text just enough that resume discipline lands on the staged workflow. | `docs/plan.md`, `docs/roadmap.md`, `docs/stage_overview.md`. | A fresh resume pass following `AGENTS.md` sees Stage 4 as active/pending and does not treat old WP0.16/WP0.18 text as next work. | Orchestrator if historical roadmap sections should be rewritten rather than redirected. |
| R07 | Ensure Stage 4 goals include canonical review surfaces and, where outputs are produced, artefact manifests. | `AGENTS.md`, workflow, Stage 2/3 closeouts. | Each Stage 4 closeout lists artefact/review surfaces and explains any no-new-artefact planning choice. | Orchestrator if a Stage 4 goal tries to skip result/artefact review while changing claims. |
| R08 | Make validation evidence broader than tests/builds. | `docs/workflow.md`, Stage 2/3 validation records. | Closeouts include command results plus domain claim scans, caption/table denominator checks, and manual release-policy checks. | Orchestrator if validation requires manuscript build, package build, remote audit, or archive checks outside a goal's scope. |
| R09 | Reconcile raw checksum versus CRLF-normalized checksum semantics for the ALA licence ledger. | `data/README.md`, `evidence_reconciliation.md`. | Data README and release manifest either agree on checksum values or explicitly define raw and normalized checksum semantics. | Orchestrator if checksum disagreement suggests file drift rather than line-ending normalization. |
| M01 | Rewrite Results and Discussion from the accepted evidence, with Layer A as the main result and Layer B as secondary. | Manuscript draft, tables, figures, interpretation notes, Stage 2/3 closeouts. | Manual review confirms the manuscript leads with robust findings and quantifies limits instead of adding unsupported emphasis. | Barry/orchestrator if the paper's strategic emphasis or journal framing changes. |
| M02 | Caption pass for denominators, eligibility, censoring, selection rules, and Layer B caveats. | `manuscript/text/figures.md`, supplementary figures, Table 1, Table S1/S2. | Caption scan confirms every main/supplementary figure and table has the relevant n, selection rule, and caveat. | Orchestrator if a caption requires changing a figure/table rather than wording. |
| M03 | Reference production pass: convert DOI scaffolding into citation metadata and check build/reference hygiene. | `docs/ref_doi.txt`, `references/refs.yaml`, manuscript references, makedoc checks. | Manuscript build/reference audit has no raw DOI scaffolding in paper text and no unresolved citation keys. | Barry/orchestrator for adding/removing substantive literature or changing citation strategy. |
| M04 | Enforce claim discipline across abstract, Results, Discussion, captions, tables, and data availability. | Manuscript text, Stage 3A closeout, interpretation notes. | `rg` and manual review find no unsupported causal, population-decline, population-trend, or national-biodiversity wording. | Orchestrator if desired wording would imply stronger inference than accepted evidence supports. |
| M05 | Verify Table 1, Table S1, and Table S2 remain traceable after the rewrite. | Manuscript tables and source reports. | Table source cross-checks match accepted reports; no placeholder language remains. | Orchestrator if final prose needs a table value not present in accepted evidence. |

## Manuscript Synthesis Plan

Ready for Stage 4A rewrite from existing evidence:

- Abstract: can be sharpened around Layer A as the main result and Layer B as a
  weak secondary falsification exercise.
- Results 3.1-3.6: ready for synthesis using Table 1, Fig. 1-3, Supplementary
  Fig. S1-S3, and Stage 2 interpretation notes.
- Results 3.7-3.9: ready for concise secondary synthesis using Table S2, Fig.
  4-5, Supplementary Fig. S4-S6, and Stage 3A interpretation notes.
- Discussion 4.1-4.4: ready to lead with censoring, non-zero brightening tail,
  external pressure, uncertainty-aware triage, and buffer-zone management.
- Discussion 4.5-4.6: ready to remain cautious and method-focused for Layer B.
- Limitations: ready to become a stronger, structured limitation section tied
  to censoring, eligibility, ring feasibility, occurrence bias, and non-causal
  design.
- Tables and captions: values are present, but Stage 4A should verify each
  caption/table row against accepted reports before polishing language.

Needs Stage 4B release-policy decisions first:

- Data and code availability wording that cites an external archive DOI.
- Any promise about redistributing raw ALA zips or row-level processed ALA
  occurrence tables.
- Any final wording about which large ignored outputs are archived versus
  regenerated by users.
- Any statement that the release is reproducible from a clean final commit.

Do not edit figures, generated tables, or source data in Stage 4A unless a
specific mismatch is found and a new goal authorizes the change.

## Release, Data Availability, And Reproducibility Plan

Stage 4B should produce a release policy before final validation:

- A final release manifest should classify every paper-critical artefact as
  tracked, archived, regenerated, excluded, or restricted.
- Large Layer A processed outputs should be archived with a SHA-256 manifest or
  the release should state exactly how users regenerate them.
- Raw ALA downloads and row-level processed ALA occurrence tables should remain
  excluded unless provider permissions are explicitly resolved.
- Derived Layer B summaries, figures, and reports can be included if their
  licences and provenance are documented.
- The ALA licence ledger checksum convention must distinguish raw file checksum
  from CRLF-normalized reconciliation checksum.
- `docs/ref_doi.txt` should be treated as citation/reference scaffolding unless
  Barry explicitly approves archive/DOI use.
- The final reproducibility audit should be refreshed after the accepted Stage
  4 manuscript/release state, or supplemented if a full rerun is deliberately
  deferred.

## Recommended Stage 4 Goal Sequence

### Stage 4A: Manuscript Synthesis And Claim Discipline

Objective:

Rewrite the manuscript-facing narrative from the accepted evidence package
without changing science outputs.

Allowed review surface:

- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/references.md`
- `docs/interpretation_notes.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/log/*`
- the Stage 4A goal packet files

Non-goals:

- No data processing, figure regeneration, modelling, ALA downloads, release
  manifest creation, archive/DOI work, or final publication tooling.
- No stronger Layer B claim.

Required evidence inputs:

- Stage 2 signoff, Stage 3A/3B closeouts, Table 1/S1/S2, figures/captions,
  interpretation notes, and accepted reports referenced by those surfaces.

Validation commands and manual checks:

- `git status --short --branch`
- `git diff --check`
- targeted claim scan for causal, population decline, population trend,
  national biodiversity, provider-bounded, presence-only, and falsification
  terms.
- caption/table scan for denominator, eligibility, censoring, complete-ring,
  provider-matched, weak-discrimination, and no-redistribution language.
- if authorized by the Stage 4A packet, `make ms-check`; otherwise defer to
  Stage 4C.

Stop conditions:

- M01, M02, M04, and manuscript-facing parts of M05 are ready for orchestrator
  review.
- Any new evidence need becomes a separate science goal rather than being
  improvised inside the rewrite.

Escalation points:

- Barry/orchestrator if title, abstract framing, journal positioning, or Layer
  B inclusion/removal becomes a strategic decision.
- Orchestrator if any manuscript claim requires new analysis or figure/table
  regeneration.

Expected deliverables:

- Updated manuscript text/tables/captions.
- A Stage 4A closeout with claim-scan results and table/caption cross-checks.
- Updated matrix statuses for manuscript items only where justified.

### Stage 4B: Release, Data Availability, Archive/DOI, And Checksum Readiness

Objective:

Create a release and data-availability decision surface that can be reviewed
before any archive publication or DOI minting.

Allowed review surface:

- `data/README.md`
- `README.md`
- `analysis/reports/final_release_manifest.md` or similarly named release
  manifest
- `analysis/reports/reproducibility_audit.md` or a Stage 4 supplement
- `docs/ref_doi.txt` only if explicitly authorized in the Stage 4B packet
- `docs/decisions.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/log/*`
- manuscript data/code availability section only if the packet allows it

Non-goals:

- No archive upload, DOI minting, release packaging, remote compute, or data
  rerun unless separately authorized.
- No manuscript science rewrite beyond data availability wording.

Required evidence inputs:

- Evidence reconciliation, reproducibility audit, data README, Zenodo
  checklists, Stage 3A licensing language, ALA licence ledger, and final Stage
  4A manuscript state.

Validation commands and manual checks:

- `git status --short --branch`
- `git diff --check`
- release-manifest completeness check against evidence reconciliation and
  figure/data inventories.
- checksum convention check for Layer B licence ledger.
- licence scan for mixed licence, raw ALA, redistribution, CC-BY, Creative
  Commons, Zenodo, DOI, archive, and release manifest terms.

Stop conditions:

- B01, B11, R02, R05, and R09 are either resolved for release review or blocked
  by explicit Barry/orchestrator decisions.
- The release manifest does not promise restricted raw ALA redistribution.

Escalation points:

- Barry required for archive/DOI publication, final archive scope, and any
  strategic decision to share, withhold, or regenerate large outputs.
- Orchestrator required for any remote rerun or packaging command.

Expected deliverables:

- Final release-readiness memo and release manifest.
- Updated data availability wording if authorized.
- Decision note for archive/DOI policy and checksum conventions.

### Stage 4C: Final Validation And Reproducibility Audit

Objective:

Run the final validation ladder after Stage 4A and 4B are accepted, then
produce the final move/no-move recommendation for publication packaging.

Allowed review surface:

- final validation reports under `analysis/reports/`
- reproducibility audit surfaces
- manuscript build outputs if authorized
- `docs/stage1_critique_resolution_matrix.md`
- `docs/log/*`
- Stage 4C closeout memo

Non-goals:

- No new science.
- No archive/DOI publication unless the Stage 4C packet explicitly says that
  publication tooling is in scope.

Required evidence inputs:

- Accepted Stage 4A manuscript state.
- Accepted Stage 4B release/data-availability state.
- Current clean or explicitly documented git state.

Validation ladder:

1. `git status --short --branch` and `git diff --check`.
2. Manuscript claim/caption/table scans from Stage 4A.
3. `make ms-check` after manuscript surfaces are edited.
4. Package/build checks such as `uv build` or `make build` after code/package
   metadata is in final state.
5. Targeted pytest or full pytest as authorized by the final goal packet.
6. Release manifest checks against data README, evidence reconciliation, and
   checksum manifest.
7. Clean-state reproducibility audit refresh or supplement.
8. Optional `make ms-build` only when final manuscript build artefacts are in
   scope.

Stop conditions:

- Validation passes or every failure is classified as blocker/non-blocker with
  a concrete owner.
- The closeout says whether the project is ready for release packaging,
  archive/DOI publication, or Barry review.

Escalation points:

- Orchestrator if validation requires remote compute, large data reruns, or
  non-local state.
- Barry if final archive/publication submission decisions are required.

Expected deliverables:

- Stage 4C validation report.
- Final Stage 4 closeout.
- Updated matrix statuses for resolved Stage 4 and release-gate items.

## Claim-Discipline And Licensing Scan Strategy

Run scans as review aids, then manually classify every hit. They are not
automatic failures.

Claim terms:

```bash
rg -n "population decline|population trend|causal|causal impact|national biodiversity|national biodiversity response|provider-bounded|presence-only|falsification" manuscript/text docs
```

Caption/table denominator terms:

```bash
rg -n "n =|eligible|ineligible|minimum-pixel|zero|censor|complete ring|provider-matched|AUC|log loss|redistribut" manuscript/text
```

Licensing and release terms:

```bash
rg -n "mixed|raw ALA|redistribut|CC-BY|CC BY|Creative Commons|Zenodo|DOI|archive|release manifest|checksum" manuscript/text docs data/README.md analysis/reports
```

Manual classification rules:

- Any causal, decline, trend, or national biodiversity wording for Layer B must
  be negated/cautionary or removed.
- Layer A can make national protected-area statements only with its explicit
  denominators and eligibility rules.
- Edge/penetration statements must say they are conditional on complete-ring
  feasibility.
- Table S1 ranking language must say triage/category-safe, not exact ordering.
- Layer B must say provider-matched/provider-bounded, weak, associational, and
  falsification-limited.
- ALA release wording must say mixed licences and no raw redistribution unless
  permissions are explicitly resolved.

## Stale Governance Language

`docs/plan.md` and `docs/roadmap.md` contain valuable history but stale
"current status" cues. Stage 4 should not rewrite their historical WP sections.
Instead:

- `docs/stage_overview.md` should remain the active staged workflow entrypoint.
- `docs/plan.md` status should be updated only enough to point readers to the
  staged workflow and current Stage 4 plan.
- `docs/roadmap.md` should preserve completed WP history but warn that future
  work is now stage-gated through `docs/stage_overview.md` and current goal
  packets.
- Any broader governance rewrite should be a narrow Stage 4A or 4B task, not
  incidental cleanup.

## Decisions And Escalation

Orchestrator can decide:

- whether to accept the 4A/4B/4C split;
- whether Stage 4A may run `make ms-check`;
- whether Stage 4B may create or modify release manifests and data availability
  wording;
- whether Stage 4C may run package builds, manuscript builds, or full tests;
- whether stale governance language should be redirected or rewritten.

Barry should decide:

- archive/DOI publication and final archive scope;
- any raw or row-level ALA occurrence redistribution exception;
- journal/framing decisions that materially change title, abstract emphasis, or
  Layer B inclusion;
- any strategic trade-off between reproducibility burden and publication
  timeline.

## Stage 4 Exit Gate

Stage 4 is ready to close only when:

- M01-M05 are resolved or explicitly deferred with reasons.
- B01/B11 release gates are resolved or blocked by a recorded Barry/orchestrator
  decision.
- R01/R02/R04/R05/R06/R07/R08/R09 are resolved, superseded, or turned into
  explicit release blockers.
- Manuscript checks and claim scans pass with classified hits.
- Release/data availability does not overpromise archived or redistributable
  data.
- Final validation includes command evidence and manual domain/release review,
  not only tests.
- The final closeout recommends whether to proceed to release packaging,
  archive/DOI publication, or Barry-facing manuscript review.

# Stage 3 Layer B Reconciliation Plan

## Summary Recommendation

Proceed to Stage 3 as a bounded Layer B reconciliation and claim-discipline
stage, not as a new analysis stage by default. The existing Layer B evidence is
strong enough to retain as a conservative secondary occurrence-signal test, but
not strong enough for national biodiversity, population-trend, or causal-impact
claims.

Use two implementation goals rather than one broad goal:

1. Stage 3A: integrate the existing Layer B evidence into the manuscript-facing
   review surface, complete Table S2 from existing reports, and tighten claim,
   licensing, and data-availability language.
2. Stage 3B: add the narrow ALA ingest guardrail test for tiny or sentinel
   download payloads. This is code/test work only and should not trigger new ALA
   downloads or modelling.

Do not run additional Layer B modelling unless the orchestrator explicitly
chooses to strengthen the secondary result beyond the current cautious framing.
The current combination of provider matching, spatial blocking, full
multi-provider sensitivity, block-level ALAN shuffling, and IBRA-by-year
shuffling supports a weak, bias-aware secondary signal, with clear residual
uncertainty.

## Current Layer B State

Layer B is currently a secondary presence-only occurrence association test for
microbats versus diurnal passerines, bounded to ALA records from 2013-2024 that
fall inside protected areas or within 10 km of their boundaries. Diurnal reptiles
were deferred after repeated ALA download failures.

Current evidence surfaces show:

- Microbat records after filtering and deduplication: 63,716 records across 59
  species.
- Passerine records after filtering and deduplication: 2,378,378 records across
  348 species.
- In-scope records inside protected areas or within 10 km: 56,883 microbat
  records and 2,142,802 passerine records.
- Microbat records are highly provider concentrated: NSW BioNet dr368 supplies
  56,590 records, or 88.8 percent of deduplicated microbat records.
- The primary model is provider matched to dr368, with 50,281 microbat and
  50,281 passerine records.
- Primary spatially blocked model performance is weak: AUC about 0.545 and log
  loss about 0.689.
- Primary ALAN terms are directionally structured but not clean evidence of a
  biodiversity response: `any_light` is positive, while `log1p_alan` is negative.
- Block-level ALAN shuffling collapses model performance toward null: AUC about
  0.505.
- IBRA-by-year shuffling also remains close to null: AUC about 0.517.
- Full multi-provider sensitivity is descriptive only, with AUC about 0.557 and
  known provider/state confounding.
- IBRA heterogeneity is descriptive and unstable across regions; only 11 IBRA
  regions meet the current per-class record threshold.
- ALA licensing is mixed across records and providers. Release-facing language
  must not describe the Layer B record set as blanket CC-BY.

Key sources for the implementation executor are:

- `analysis/reports/layerB_data_qc.md`
- `analysis/reports/layerB_qc_extended.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_modelling_report.md`
- `analysis/reports/layerB_ibra_summary.md`
- `analysis/reports/layerB_ala_license_ledger.md`
- `analysis/reports/evidence_reconciliation.md`
- `docs/stage1_critique_resolution_matrix.md`
- `docs/interpretation_notes.md`
- `docs/decisions.md`
- `manuscript/text/supplementary_tables.md`

## Stage 3 Objective

Stage 3 should reconcile the Layer B result into a defensible, auditable,
secondary evidence package. The stage should answer:

- Which B01-B12 critique items are resolved by existing evidence?
- Which items require manuscript, supplement, or data-availability changes?
- Which items require new code/tests?
- Which apparent analysis extensions should be rejected or deferred because they
  would overstate the Layer B result?
- What exact validation bundle must pass before the manuscript rewrite stage can
  start?

The target scientific posture is:

> Layer B is retained only as a conservative, provider-bounded,
> presence-only occurrence association and falsification exercise. It supports
> the plausibility of a weak nocturnal-biodiversity signal consistent with ALAN
> exposure, but it does not establish causality, population decline, population
> trends, or a national biodiversity response.

## B01-B12 Reconciliation Matrix

| ID | Classification | Stage 3 Resolution Path | Evidence And Executor Notes | Exit Test |
| --- | --- | --- | --- | --- |
| B01 | Stage 3A plus Stage 4 release gate | In Stage 3A, add manuscript/supplement/data-availability language that says ALA occurrence licences are mixed and raw ALA records are not redistributed. Leave archive mechanics to Stage 4. | `layerB_ala_license_ledger.md` shows CC-BY, CC-BY-NC, missing rights strings, and provider-specific conditions. `data/README.md` records checksums, but the release-facing wording must avoid blanket CC-BY. | Text check finds no blanket CC-BY claim for the Layer B record set. Data availability points to derived summaries and provenance, not raw ALA redistribution. |
| B02 | Stage 3A | Use existing QC reports more visibly in manuscript/supplement. No new QC run is required unless source values fail cross-check. | `layerB_qc_extended.md` reports sign, bounding-box, offshore, coordinate-uncertainty, spatial concentration, and provider-concentration checks. | Layer B Methods or supplement cites the QC filters and concentration checks, and Table S2 or supplement references model-input n and scope. |
| B03 | Stage 3A claim discipline | Retain Layer B as provider-bounded, not nationally representative. Do not claim a national biodiversity signal. | Microbats are 88.8 percent NSW BioNet dr368, and state counts are NSW dominated. The primary design intentionally uses dr368 provider matching. | Claim scan finds no national biodiversity inference from Layer B. Results describe the primary model as provider-matched or NSW BioNet bounded. |
| B04 | Stage 3A, no new run by default | Treat provider-matched diurnal passerines plus block and IBRA-year shuffles as sufficient for the current secondary framing. Do not restart diurnal-reptile acquisition unless a later goal explicitly widens the evidence standard. | DEC-026 defers reptiles after ALA failure. The current design includes a diurnal passerine control and two falsification shuffles. | Text does not imply an implemented reptile control. It describes the negative-control and falsification design precisely. |
| B05 | Stage 3A | Complete Table S2 from existing model-input and model-report values. Include n, scope fractions, zero fractions, ALAN coefficients, AUC, log loss, and interpretation flags. | `layerB_modelling_report.md` contains primary, block shuffle, IBRA-year shuffle, and full sensitivity metrics. `layerB_scope_coverage.md` and `layerB_exposure_qc.md` explain scope and zero mass. | Table S2 is populated from existing reports with values cross-checked against `layerB_modelling_report.md`; no model rerun is needed. |
| B06 | Stage 3A claim discipline | Make falsification limitations central. The primary result is weak, and residual `any_light` structure must be described as a bias warning, not as confirmation. | Block shuffle AUC about 0.505 and IBRA-year shuffle AUC about 0.517 are near null, but some ALAN residual structure remains. Interpretation notes already flag this concern. | Results and Discussion state that falsification supports caution and weakens inference strength. |
| B07 | Defer new run unless orchestrator requests stronger Layer B | Do not add stratum/year covariate robustness by default. Existing falsification and sensitivity evidence is adequate for a cautious secondary result. If the manuscript needs stronger claims, create a separate compute goal. | `docs/interpretation_notes.md` lists stratum/year covariates as a possible follow-up, not as a blocker. The current recommendation is to weaken the claim rather than expand modelling. | Stage 3A records a no-run rationale. Any request for stronger inference creates a new explicit modelling goal before Stage 4. |
| B08 | Stage 3A descriptive integration | Keep IBRA heterogeneity descriptive. Do not merge or smooth regions unless a later manuscript-review pass finds the current figure/table impossible to interpret. | `layerB_ibra_effects.csv` includes 11 qualifying regions with sign changes and wide uncertainty in some regions. | Manuscript/supplement says IBRA heterogeneity is exploratory and not a formal regional effect model. |
| B09 | Stage 3A, no new panel by default | Use existing counts, density, and provider-matched design to surface provider/state concentration. Do not add a new provider/state sensitivity panel unless Stage 3A finds a specific unsupported claim. | `layerB_data_qc.md`, `layerB_qc_extended.md`, and existing count/density figures already show concentration. | Claim scan and figure/table references make provider/state limitation visible. |
| B10 | Stage 3B code/test guardrail | Add a small sentinel/tiny ALA zip guardrail test around the ALA ingest path. Do not download ALA data. Use local synthetic fixtures only. | Current tests cover filtering and summaries but do not appear to exercise tiny/sentinel ALA download payload rejection. | New targeted test fails on implausibly tiny or malformed ALA zip payloads and passes on a valid minimal fixture. |
| B11 | Stage 4 release gate | Record the boundary in Stage 3A but do not solve release packaging now. Raw ALA occurrence zips and processed occurrence tables should remain non-release artefacts unless permissions are explicit. | `data/README.md` records ignored raw and processed Layer B data plus checksum/provenance notes. | Stage 4 release plan includes a derived-output-only policy and reconciles the licence-ledger checksum convention. |
| B12 | Stage 3A | Fill Table S2 during implementation from the existing reports. This is the central manuscript-facing reconciliation task. | `manuscript/text/supplementary_tables.md` currently contains a placeholder and already identifies the intended rows and columns. | Table S2 contains primary, block-shuffle, IBRA-year-shuffle, and full-sensitivity rows with exact values and cautious interpretation notes. |

## Recommended Execution Structure

### Stage 3A: Layer B Evidence Integration And Claim Discipline

Recommended next implementation goal.

Allowed work:

- Edit manuscript-facing Layer B prose, supplementary Table S2, captions if
  needed, `docs/interpretation_notes.md`, and narrow data-availability language
  only if explicitly authorized by the next goal packet.
- Use existing reports and processed summaries only.
- Fill Table S2 from the current Layer B model report and supporting QC reports.
- Resolve B01, B02, B03, B04, B05, B06, B07 no-run rationale, B08, B09, B11
  boundary note, and B12.

Non-goals:

- No new ALA downloads.
- No new Layer B modelling.
- No remote compute.
- No release packaging.
- No archive/DOI work.
- No Stage 4 manuscript rewrite beyond the Layer B reconciliation surfaces named
  in the goal packet.

Suggested executor contract:

> Reconcile existing Layer B evidence into the manuscript and supplement without
> new analyses. Fill Table S2, tighten claims, add licensing/data-availability
> caveats, document no-run rationales for B04/B07/B09, and stop with validation
> evidence.

### Stage 3B: ALA Ingest Guardrail Test

Recommended as a separate small implementation goal, before or after Stage 3A.

Allowed work:

- Add synthetic local fixtures for tiny, malformed, or sentinel ALA zip payloads.
- Add a targeted test for the ALA ingest/download validation path.
- Patch the ingest code only as needed for the test.

Non-goals:

- No live ALA calls.
- No changes to occurrence data.
- No model reruns.
- No manuscript edits except a brief test note if the goal packet asks for it.

Suggested executor contract:

> Add a local test and minimal code guard so ALA ingest rejects implausibly tiny
> or malformed zip payloads before they can be treated as occurrence downloads.
> Use synthetic fixtures only.

### Do Not Combine With Stage 4

Stage 3 should end once the Layer B evidence is reconciled and the guardrail
test is complete or explicitly deferred. Stage 4 should then handle the broader
evidence-led manuscript rewrite, final data availability wording, release
audits, archive policy, and DOI/package surfaces.

## Table S2 Completion Plan

Table S2 should be completed in Stage 3A from existing evidence only. The table
should not require any new modelling.

Recommended rows:

| Row | Source | Purpose |
| --- | --- | --- |
| Primary provider-matched model | `layerB_modelling_report.md`, section "Primary (provider-matched) results" | Main dr368 provider-matched microbat versus passerine signal test. |
| Block-shuffle falsification | `layerB_modelling_report.md`, section "Falsification (ALAN shuffled within blocks)" | Tests whether ALAN structure collapses when ALAN is shuffled among spatial blocks. |
| IBRA-by-year shuffle falsification | `layerB_modelling_report.md`, section "Falsification (ALAN shuffled within IBRA x year)" | Tests whether broad bioregion-year structure explains the apparent ALAN signal. |
| Full multi-provider sensitivity | `layerB_modelling_report.md`, section "Sensitivity (multi-provider)" | Descriptive sensitivity only; not the primary inference. |

Recommended columns:

- Design.
- Provider and scope.
- Microbat n.
- Passerine n.
- Microbat inside fraction.
- Passerine inside fraction.
- Microbat zero-ALAN fraction.
- Passerine zero-ALAN fraction.
- `any_light` coefficient mean and fold standard deviation.
- `log1p_alan` coefficient mean and fold standard deviation.
- AUC.
- Log loss.
- Interpretation note.

Known values to cross-check while filling:

| Design | n per class | AUC | Log loss | `any_light` mean | `log1p_alan` mean | Interpretation flag |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Primary dr368 | 50,281 | 0.545 | 0.689 | 1.316 | -0.354 | Weak provider-matched association; not causal. |
| Block shuffle | 50,281 | 0.505 | 0.695 | 0.202 | -0.027 | Near-null performance after block shuffle. |
| IBRA-year shuffle | 50,281 | 0.517 | 0.695 | 0.163 | -0.001 | Near-null performance after coarse bioregion-year shuffle. |
| Full sensitivity | 56,883 | 0.557 | 0.700 | 0.732 | -0.332 | Descriptive only because provider/state confounding returns. |

The executor should preserve more precision from the source report in the final
supplementary table if the manuscript table format permits it.

## Claim Discipline And Licensing Checks

Stage 3A must enforce these claim rules:

- Say "presence-only occurrence association", "secondary signal test",
  "provider-matched", and "weak discrimination" where appropriate.
- Do not say or imply "population decline", "population trend", "causal impact",
  "national biodiversity response", or "national biodiversity signal" for Layer
  B.
- If "national biodiversity datasets" appears as background language, ensure the
  inference sentence immediately narrows Layer B to provider-bounded occurrence
  evidence.
- Refer to passerines as the implemented diurnal control group. Reptiles were
  deferred and should not be presented as implemented.
- Describe block shuffle and IBRA-year shuffle as falsification tests, and state
  that their near-null performance supports caution rather than confirmation.
- Treat IBRA heterogeneity as exploratory/descriptive.
- State that ALA occurrence licences are mixed. Do not describe all Layer B ALA
  records as CC-BY.
- Do not promise raw ALA occurrence redistribution in a release package unless a
  later release-policy goal verifies permissions.

Minimum text scans for the Stage 3A executor:

```sh
rg -n "causal|population decline|population trend|national biodiversity|negative controls|falsification|provider-matched|Layer B" manuscript/text docs/interpretation_notes.md
rg -n "CC-BY|CC BY|Creative Commons|ALA" manuscript/text docs data/README.md
```

The scans are review aids. They do not fail automatically, but every hit should
be checked against the rules above.

## Validation Bundle For Implementation

Stage 3A should finish with:

- `git status --short --branch`
- `git diff --check`
- Source-value cross-check for every Table S2 number against
  `analysis/reports/layerB_modelling_report.md`.
- Targeted claim and licence scans listed above.
- A short log entry naming every B01-B12 item as resolved, deferred, or moved to
  Stage 4.
- A move/no-move recommendation for Stage 4.

Stage 3B should finish with:

- `git status --short --branch`
- `git diff --check`
- A targeted pytest command covering the new ALA ingest guardrail.
- Any existing Layer B ingest/filter tests that are directly adjacent to the
  patched code.
- A short log entry confirming that no live ALA download or data processing was
  run.

No Stage 3 executor should run remote compute, national raster reruns, ALA live
downloads, full validation suites, manuscript builds, release packaging, archive
work, commits, pushes, merges, or PR creation unless its goal packet explicitly
widens scope.

## Stage 4 Boundaries

Stage 4 should not begin until Stage 3A is complete and Stage 3B is complete or
explicitly deferred by the orchestrator.

Stage 4 owns:

- Evidence-led manuscript rewrite across Results, Discussion, captions, and
  supplement integration.
- Final data availability and ALA licensing wording.
- Release-manifest and archive/DOI policy.
- Reconciliation of checksum conventions for the Layer B licence ledger.
- Final release audit of generated artefacts.
- Any decision to demote or remove Layer B after seeing the fully integrated
  manuscript.

Stage 4 should not discover new Layer B analysis requirements implicitly. If a
new modelling or acquisition requirement appears during Stage 4, it should be
turned into a separate explicit science goal and Stage 4 should pause.

## Escalation Points

Escalate to the DSIPA orchestrator before implementation if any of these become
true:

- The orchestrator wants Layer B to support stronger claims than a weak,
  provider-bounded secondary signal.
- A future executor believes B04 or B07 needs new modelling rather than a
  no-run rationale.
- The Table S2 source values conflict between reports and processed summaries.
- The release package is expected to include raw ALA occurrence downloads or
  row-level processed ALA occurrence data.
- The manuscript must use "national biodiversity signal" language for Layer B.
- ALA licence terms are ambiguous enough that legal or repository-policy review
  is needed.

## Exit Gate

Stage 3 is ready to close when:

- B01-B12 each have a recorded resolution, deferral, or Stage 4 boundary.
- Table S2 is filled from existing evidence or the orchestrator explicitly
  accepts a deferral.
- Layer B claims are narrow, conservative, and traceable to existing reports.
- Licensing and data-availability language avoids blanket CC-BY and raw ALA
  redistribution promises.
- The B10 ingest guardrail test is complete or explicitly deferred.
- Validation commands and targeted text scans are recorded.
- The closeout recommendation clearly says whether Stage 4 manuscript rewrite
  can begin.

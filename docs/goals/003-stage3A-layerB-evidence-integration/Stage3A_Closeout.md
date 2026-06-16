# Stage 3A Closeout

## Summary Recommendation

Accept Goal 003 as complete. Stage 3A has integrated the existing Layer B
evidence into the manuscript-facing review surface without new modelling or data
processing. Layer B is now framed as a conservative, provider-bounded,
presence-only occurrence association and falsification exercise. It is not
causal, not a population trend, not a population decline analysis, and not a
national biodiversity response.

Recommended next goal: Stage 3B only, focused on the ALA tiny/sentinel zip
guardrail test using synthetic local fixtures. Do not start Stage 4 until Stage
3B is complete or explicitly deferred by the orchestrator.

## Current State

Stage 3A resolved the manuscript-facing Layer B integration items B01-B09 and
B12, while keeping B11 as a Stage 4 release gate and B10 as the remaining Stage
3B code/test item.

The central scientific result is unchanged: the primary provider-matched dr368
model has weak discrimination (AUC 0.545), the two falsification runs are near
null (AUC 0.505 and 0.517), and the full multi-provider sensitivity is
descriptive only.

## Files Changed

- `manuscript/text/supplementary_tables.md`
  - Filled Table S2 with primary, block-shuffle, IBRA x year shuffle, and
    full multi-provider sensitivity rows.
- `manuscript/text/manuscript_draft.md`
  - Tightened Layer B framing as provider-bounded and added mixed-licence /
    no-raw-ALA-redistribution wording.
- `manuscript/text/figures.md`
  - Added explicit non-causal, non-population-trend interpretation language to
    the Layer B effects figure caption.
- `manuscript/text/supplementary_figures.md`
  - Tightened Layer B bias-diagnostic captions.
- `docs/interpretation_notes.md`
  - Added Stage 3A integrated Layer B interpretation and no-run rationales.
- `docs/stage1_critique_resolution_matrix.md`
  - Updated B01-B09/B11/B12 resolution state.
- `docs/log/123_stage3A_layerB_evidence_integration.md`
  - Added Stage 3A execution log.
- `docs/goals/003-stage3A-layerB-evidence-integration/Log.md`
  - Updated Goal 003 execution log.
- `docs/goals/003-stage3A-layerB-evidence-integration/Stage3A_Closeout.md`
  - This closeout memo.

## Table S2 Source Cross-Check

Table S2 was filled from `analysis/reports/layerB_modelling_report.md`.

| Design | Source values | Table S2 values |
| --- | --- | --- |
| Primary dr368 | n = 50,281 per class; `any_light` 1.315818 +/- 0.127743; `log1p_alan` -0.354431 +/- 0.023846; AUC 0.544657; log loss 0.6892 | n = 50,281 per class; `any_light` 1.316 +/- 0.128; `log1p_alan` -0.354 +/- 0.024; AUC 0.545; log loss 0.689 |
| Block shuffle | n = 50,281 per class; `any_light` 0.202411 +/- 0.086377; `log1p_alan` -0.026923 +/- 0.021043; AUC 0.505466; log loss 0.695243 | n = 50,281 per class; `any_light` 0.202 +/- 0.086; `log1p_alan` -0.027 +/- 0.021; AUC 0.505; log loss 0.695 |
| IBRA x year shuffle | n = 50,281 per class; `any_light` 0.163136 +/- 0.062740; `log1p_alan` -0.001463 +/- 0.008311; AUC 0.516707; log loss 0.694683 | n = 50,281 per class; `any_light` 0.163 +/- 0.063; `log1p_alan` -0.001 +/- 0.008; AUC 0.517; log loss 0.695 |
| Full multi-provider sensitivity | n = 56,883 per class; `any_light` 0.731746 +/- 0.330202; `log1p_alan` -0.331665 +/- 0.093925; AUC 0.556655; log loss 0.699828 | n = 56,883 per class; `any_light` 0.732 +/- 0.330; `log1p_alan` -0.332 +/- 0.094; AUC 0.557; log loss 0.700 |

Validation command:

```sh
rg -Fq ... analysis/reports/layerB_modelling_report.md
rg -Fq ... manuscript/text/supplementary_tables.md
```

Outcome: passed. The source report exact values and rounded Table S2 values are
present.

## B01-B09/B11/B12 Resolution State

| ID | Stage 3A state | Notes |
| --- | --- | --- |
| B01 | Stage 3A complete; Stage 4 release gate remains | Paper-facing wording now says ALA licences are mixed and raw ALA occurrence tables are not redistributed by the manuscript package. |
| B02 | done | Richer QC/model-input evidence is integrated through Results, captions, and Table S2. |
| B03 | done | Layer B is explicitly provider-bounded and not national biodiversity inference. |
| B04 | done by no-run rationale | Provider-matched passerines plus two shuffles are sufficient for the current weak secondary framing; Squamata remains deferred. |
| B05 | done | Table S2 includes n, scope/zero fractions, providers/scope, coefficients, AUC, log loss, and interpretation flags. |
| B06 | done | Residual structure and weak discrimination remain central; no ecological overclaim was added. |
| B07 | done by no-run rationale | No stratum/year covariate run in Stage 3A. Reopen only if a future goal asks for stronger Layer B claims. |
| B08 | done | IBRA heterogeneity remains descriptive. |
| B09 | done by no-run rationale | No provider/state sensitivity panel in Stage 3A. Existing diagnostics are sufficient for conservative framing. |
| B11 | Stage 4 release gate | Final archive/release policy still must avoid restricted raw ALA redistribution unless permissions allow. |
| B12 | done | Table S2 is filled and no longer a placeholder. |

B10 is intentionally unchanged and remains the Stage 3B code/test guardrail.

## Claim And Licence Review

The final Layer B wording is deliberately narrow:

- Provider-bounded and presence-only.
- Weak discrimination and falsification-limited.
- Descriptive multi-provider sensitivity only.
- No causal impact claim.
- No population trend or decline claim.
- No national biodiversity response claim.
- Mixed ALA licences acknowledged.
- Raw ALA occurrence redistribution not promised.

Targeted scans are classified as passing with expected review hits. The hits are
negated/cautionary manuscript statements, required provenance/licence language,
or historical review documents retained for traceability.

## Validation Results

Commands run from `/Users/bwbrook/papers/dsipa-dev`:

```sh
git status --short --branch
git diff --check
make ms-check
rg -n "population decline|population trend|causal impact|national biodiversity response|national biodiversity signal" manuscript/text docs/interpretation_notes.md
rg -n "negative controls|diurnal reptiles|Squamata|provider-matched|falsification|Layer B" manuscript/text docs/interpretation_notes.md
rg -n "CC-BY|CC BY|Creative Commons|raw ALA|redistribut|mixed" manuscript/text docs data/README.md
```

Outcomes:

- Final `git status --short --branch`:

```text
## main...origin/main
 M docs/interpretation_notes.md
 M docs/stage1_critique_resolution_matrix.md
 M manuscript/text/figures.md
 M manuscript/text/manuscript_draft.md
 M manuscript/text/supplementary_figures.md
 M manuscript/text/supplementary_tables.md
?? docs/goals/003-stage3A-layerB-evidence-integration/
?? docs/log/123_stage3A_layerB_evidence_integration.md
```

- `git diff --check`: passed.
- `make ms-check`: passed, including manuscript lint, reference audit, author
  metadata checks, and draft build check.
- Table S2 source check: passed.
- Claim scan: passing with expected review hits. Hits are negated/cautionary
  wording in the manuscript/table/caption.
- Layer B design scan: passing with expected review hits. Hits document
  provider matching, falsification, and Layer B scope.
- Licence/provenance scan: passing with expected review hits. Hits include
  paper-facing mixed-licence/no-redistribution language, `data/README.md`, and
  historical review notes.

## Residual Risks

- B10 remains open for Stage 3B; this goal did not implement the ALA tiny or
  sentinel zip guardrail.
- B11 remains a Stage 4 release/archive gate; final release packaging must
  verify that raw ALA occurrence data are not redistributed unless permissions
  allow.
- Layer B remains scientifically weak by design. That is acceptable under the
  current stance, but any stronger claim would require a new explicit modelling
  goal.

## Recommendation For Next Goal

Run Stage 3B next as a narrow code/test goal:

> Add a local synthetic-fixture test and minimal code guard so ALA ingest rejects
> implausibly tiny or malformed zip payloads. Do not run live ALA downloads,
> Layer B modelling, data processing, remote compute, or manuscript rewrite.

No Barry-level decision is needed before Stage 3B unless the orchestrator wants
to skip/defer B10 and move directly to Stage 4.

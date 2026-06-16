# Log 123 - Stage 3A Layer B Evidence Integration

Date: 2026-06-16

## Scope

Executed Goal 003 as a manuscript-facing Layer B evidence integration pass.
This session used existing reports and tracked manuscript/docs only. It did not
run ALA downloads, Layer B modelling, data processing, remote compute, B10 code
or test work, release packaging, archive/DOI work, commits, pushes, merges, or
PR creation.

## Starting State

- Working directory: `/Users/bwbrook/papers/dsipa-dev`
- Starting HEAD: `2a635f1`
- Starting status: `## main...origin/main` with untracked
  `docs/goals/003-stage3A-layerB-evidence-integration/`
- Goal packet present:
  `docs/goals/003-stage3A-layerB-evidence-integration/Goal.md`

## Evidence Integrated

- Filled Table S2 from `analysis/reports/layerB_modelling_report.md`.
- Cross-checked the four intended rows:
  - primary provider-matched dr368 model;
  - ALAN shuffled within spatial blocks;
  - ALAN shuffled within IBRA x year strata;
  - full multi-provider sensitivity.
- Used supporting QC context from:
  - `analysis/reports/layerB_data_qc.md`
  - `analysis/reports/layerB_qc_extended.md`
  - `analysis/reports/layerB_scope_coverage.md`
  - `analysis/reports/layerB_exposure_qc.md`
  - `analysis/reports/layerB_ala_license_ledger.md`
  - `analysis/reports/layerB_ibra_summary.md`
  - `analysis/reports/layerB_ibra_effects.csv`

## Table S2 Source Values

| Design | n per class | any_light mean +/- SD | log1p_alan mean +/- SD | AUC | Log loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| Primary dr368 | 50,281 | 1.315818 +/- 0.127743 | -0.354431 +/- 0.023846 | 0.544657 | 0.6892 |
| Block shuffle | 50,281 | 0.202411 +/- 0.086377 | -0.026923 +/- 0.021043 | 0.505466 | 0.695243 |
| IBRA x year shuffle | 50,281 | 0.163136 +/- 0.062740 | -0.001463 +/- 0.008311 | 0.516707 | 0.694683 |
| Full multi-provider sensitivity | 56,883 | 0.731746 +/- 0.330202 | -0.331665 +/- 0.093925 | 0.556655 | 0.699828 |

Model-input fractions transcribed to Table S2:

- Primary dr368 microbats: inside fraction 0.278, zero-ALAN fraction 0.657.
- Primary dr368 passerines: inside fraction 0.257, zero-ALAN fraction 0.651.
- Full sensitivity microbats: inside fraction 0.280, zero-ALAN fraction 0.670.
- Full sensitivity passerines: inside fraction 0.205, zero-ALAN fraction 0.551.

## B-Item Resolution State

- B01: Stage 3A language tightened; final release/archive policy remains Stage
  4.
- B02: done; richer QC and model-input values are integrated.
- B03: done; Layer B is provider-bounded, not national biodiversity inference.
- B04: done by no-run rationale; Squamata remains deferred and passerines plus
  two shuffles are sufficient for the current weak secondary framing.
- B05: done; Table S2 filled.
- B06: done; residual falsification structure and weak discrimination remain
  central.
- B07: done by no-run rationale; no stratum/year covariate run in Stage 3A.
- B08: done; IBRA heterogeneity remains descriptive.
- B09: done by no-run rationale; no provider/state sensitivity panel in Stage
  3A.
- B10: still open for Stage 3B code/test guardrail.
- B11: Stage 4 release gate; raw ALA redistribution is not promised.
- B12: done; Table S2 is no longer a placeholder.

## Validation

- `git diff --check`: passed.
- `make ms-check`: passed, including manuscript lint, reference audit, author
  metadata checks, and draft build check.
- Targeted claim scan: passing with expected review hits.
- Targeted Layer B design scan: passing with expected review hits.
- Targeted licence/provenance scan: passing with expected review hits.
- Table S2 source check: passed; exact source values in
  `analysis/reports/layerB_modelling_report.md` match the rounded values
  transcribed into Table S2.

## Closeout Recommendation

Accept Stage 3A. Stage 3B should be the next and only remaining Stage 3 goal
unless the orchestrator explicitly defers B10. Do not start Stage 4 until Stage
3B is complete or deferred.

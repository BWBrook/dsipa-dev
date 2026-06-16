# Stage 2 Signoff Readiness

## Summary Recommendation

Recommend Stage 2 signoff with narrow, already-recorded caveats. The current
repo evidence supports accepting Stage 2 Layer A hardening and authorizing a
separate Stage 3 Layer B reconciliation planning goal.

No narrow Stage 2 repair goal is needed before signoff. The remaining risks are
Stage 3 Layer B interpretation/QA items and Stage 4 manuscript/release items,
not blockers to Stage 2 Layer A signoff.

## Current State

- Working directory: `/Users/bwbrook/papers/dsipa-dev`
- Branch/status at start: `## main...origin/main` with authorized untracked
  `docs/goals/`
- Short HEAD: `ad1b623`
- Goal packet present: yes
- Repo-local `AGENTS.md` and all Goal 001 required reading files were read.
- This audit edited only files inside
  `docs/goals/001-stage2-signoff-readiness/`.

## Stage 2 Exit-Gate Audit

Stage 2 can be recommended for signoff against its own exit gate.

| Exit criterion | Audit result |
| --- | --- |
| A01-A14 resolved, superseded, or deferred with reason | Passed. A01-A14 are all marked `done` in `docs/stage1_critique_resolution_matrix.md`. |
| Table 1 and Table S1 populated from validated evidence | Passed. `manuscript/text/tables.md` contains Table 1 denominator/censoring values; `manuscript/text/supplementary_tables.md` contains Table S1 watchlists. |
| Figures/captions and interpretation notes updated | Passed for Stage 2 Layer A. Captions carry denominator/eligibility/censoring caveats; `docs/interpretation_notes.md` records Stage 2 result-review entries. |
| Stage 2 artefacts and logs exist | Passed. `artefacts/stage2_layerA_hardening/` exists locally and `analysis/reports/stage2_layerA_hardening_manifest.md` is the tracked pointer. |
| Required validation passed or was justified | Passed with expected local skips for ignored national outputs. See validation results below. |
| Closeout recommends whether Stage 3 can start | Passed. `docs/log/121_stage2_layerA_hardening.md` and the manifest recommend Stage 3 planning after signoff. |

## A01-A14 Audit

The Layer A critique-resolution block is complete for Stage 2:

- A01/A03/A11/A14: denominator clarity, floor/censoring, retention denominator,
  and Table 1 are resolved by
  `analysis/reports/layerA_denominators_and_censoring.md` and
  `manuscript/text/tables.md`.
- A02: baseline map/caption now uses eligibility/ineligible language rather
  than treating low-pixel protected areas as missing source data.
- A04/A06: anchor sanity now uses explicit bright/dark contexts. The dashboard
  reports urban-adjacent eligible PAs with much higher 2024 inside p95 than
  remote eligible PAs.
- A05: buffer-validity sensitivity preserves the retention/quadrant
  interpretation under stricter 1 km buffer filters.
- A07/A08: edge profiles are retained only as feasibility-limited diagnostics;
  fixed rings are retained for this manuscript pass via DEC-035.
- A09: trend-threshold sensitivity supports the primary rule across tested
  valid-year thresholds and stricter valid-pixel thresholds.
- A10/A12/A13: uncertainty-aware Table S1 watchlists and dominance summary are
  present, with rank-overprecision caveats.

## Evidence And Artefact Checks

The local Stage 2 artefact folder is present and checksum-clean:

- `sha256sum -c artefacts/stage2_layerA_hardening/SHA256SUMS`: all entries OK.
- `sha256sum -c analysis/reports/layerA_tables_stage2_denominators.sha256`:
  all entries OK.
- `sha256sum -c analysis/reports/layerA_anchors_buffer_stage2.sha256`: all
  entries OK.
- `sha256sum -c analysis/reports/layerA_threshold_edge_stage2.sha256`: all
  entries OK.
- `sha256sum -c analysis/reports/layerA_watchlists_stage2.sha256`: all entries
  OK.

The Stage 2 signoff surface is evidence-backed enough for a management
decision. The critical denominators are explicit: PA universe n=11,133, 2024
inside eligibility n=4,426, retention/quadrant denominator n=3,858, and
complete-ring subset n=383. The main caveat is central rather than hidden:
Stage 2 is floor/censoring dominated, with 86.9% zero 2024 inside mean among
eligible PAs and 89.7% zero inside trend slopes.

## Validation Results

| Command | Outcome | Classification |
| --- | --- | --- |
| `git status --short --branch` | `## main...origin/main` plus authorized `?? docs/goals/` | Current; expected dirty state from goal packet |
| `git diff --check` | No output, exit 0 | Passing |
| `sha256sum -c artefacts/stage2_layerA_hardening/SHA256SUMS` | All entries OK | Passing |
| Report checksum commands | All listed report files OK | Passing |
| Targeted Stage 2 pytest bundle | `ss........ [100%]` | Passing with expected skips |
| Targeted pytest rerun with `-rs` | Skipped trend outputs and risk rankings because ignored national outputs are not present locally | Expected/inconclusive only for absent ignored data, not Stage 2-blocking |
| `uv build --out-dir /tmp/dsipa-build-goal001` | Built `dsipa_nbs-0.1.0.tar.gz` and wheel successfully | Passing |
| `make ms-check` | Config validation passed; 57 makedoc tests passed; manuscript lint passed; reference audit passed with 0 unknown keys and 4 unused non-fatal keys; DOCX build check passed | Passing |

## Residual Risks

- Table S2 remains a placeholder, but it is explicitly a Layer B Stage 3/4 item,
  not a Stage 2 blocker.
- Layer B and Layer B-adjacent risks B01-B12 remain for Stage 3/4: licensing
  language, provider/NSW concentration, weaker negative-control design,
  residual falsification structure, sentinel-download tests, and Table S2
  completion.
- Stage 4 release gates remain open: final archive/DOI policy, large ignored
  processed-output packaging, release audit state, and final manuscript prose
  synthesis.
- Table S1 reports inside-slope bootstrap uncertainty; buffer and retention
  uncertainty remain point estimates. This is already disclosed and should be
  carried into Stage 4 wording.
- Local targeted tests skipped checks that require ignored national trend/risk
  outputs. That is consistent with repo policy; the Stage 2 package and tracked
  checksums are locally present and verified.

## Recommendation For Next Goal

After the DSIPA orchestrator accepts this readiness audit, recommend asking
Barry to sign off Stage 2 Layer A hardening. Once signoff is granted, the next
goal should be Stage 3 Layer B reconciliation planning only. Do not start Layer
B implementation or manuscript rewriting until that Stage 3 plan is explicitly
authorized.

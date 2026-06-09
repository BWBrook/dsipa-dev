# Stage 1 critique-resolution matrix

Status: accepted queue of record for Stages 2-4.

Source abbreviations:

- `AUDIT0.15`: `docs/cover_letters/codex_repo_review_v20260104_gate0_15.md`
- `PI0.20`: `docs/cover_letter_pi_gate_0_7_wp0_20.md`
- `EVID`: generated evidence reports in `analysis/reports/`
- `INT`: `docs/interpretation_notes.md`
- `MS`: manuscript draft and table/caption placeholders in `manuscript/text/`
- `STAGE0`: Stage 0 baseline/evidence-harness documents
- `USER`: user direction in the current staged workflow

Status meanings:

- `open`: work is required before the relevant claim or artefact can be accepted.
- `verify`: later artefacts probably address the critique, but we must confirm integration and traceability.
- `done`: required Stage 2/3/4 action has been completed and validated for the current evidence state.
- `release-gate`: not blocking Stage 2 science hardening, but blocking final paper/release.
- `superseded`: retained for traceability; no action unless the issue reappears.

Ownership rule:

- Codex owns execution for all non-superseded items unless a later stage plan records a specific external dependency.
- The user owns stage signoff and any high-impact publication/archiving decisions explicitly surfaced in stage closeouts.
- The `Target` column defines when the item is planned for execution.

## Layer A: primary dark-sky integrity result

| ID | Severity | Status | Source | Critique / risk | Required resolution | Validation gate | Target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A01 | MAJOR | done | AUDIT0.15, MS | Multiple Layer A denominators are correct but subset-conditional, creating narrative risk if `n=11133`, `n=4426`, `n=3858`, and ring subsets are mixed. | Produce a denominator/feasibility table and use it consistently in Methods, Results, captions, and Table 1. | Automated or scripted table values match current evidence reports and explain every denominator used in main figures. | Stage 2 |
| A02 | MAJOR | done | AUDIT0.15, MS | Baseline map previously risked conflating "missing" with "ineligible (<10 px)". | Confirm figure labels/caption use eligibility language and update any remaining stale wording. | `rg` finds no paper-facing "missing" language for the eligibility panel unless explicitly defined as ineligible. | Stage 2 |
| A03 | MAJOR | done | AUDIT0.15, INT | Results are dominated by zero/floor mass; this must be a central result, not a caveat. | Make censoring/floor mass part of the primary Layer A evidence story and avoid treating non-zero tails as representative of all PAs. | Table 1 and figure captions report zero mass, eligibility rules, and non-zero subset sizes; interpretation notes updated after figures/tables regenerate. | Stage 2 |
| A04 | MAJOR | done | AUDIT0.15, EVID | "Top city medians" in `national_layerA_coverage_and_sanity.md` report zero for major cities, likely due to a flawed nearest-city anchor design. | Replace or retire the city-median anchor with a defensible bright/dark anchor check tied to explicit urban-distance or known-bright PA criteria. | New sanity report shows anchors that agree with domain expectations, or the old anchor is clearly labelled invalid and not used. | Stage 2 |
| A05 | MAJOR | done | AUDIT0.15, EVID | "External pressure" from `land_unprotected` buffers can be misread when buffer validity/overlap/eligible pixels vary among PAs. | Add buffer-validity conditioning or sensitivity thresholds for retention/external-pressure claims. | Report compares key quadrant/watchlist results under primary and stricter valid-buffer filters; captions state selection criteria. | Stage 2 |
| A06 | MAJOR | done | AUDIT0.15, EVID | Overall inside-vs-buffer summaries can look counterintuitive under floor domination and weaken reader trust. | Prefer stratified/domain-sensible sanity checks and explain why aggregate `buffer > inside` fractions are floor-dominated. | Layer A sanity report contains stratified checks that support the interpretation without relying on misleading aggregate anchors. | Stage 2 |
| A07 | MAJOR | done | AUDIT0.15, INT, MS | Current edge/penetration figure can be misread as "no edge effect" because median `frac_gt0` is zero and complete rings are rare. | Decide whether to revise the figure statistic/panel or reframe it as a feasibility-limited diagnostic. | Paper-facing figure/caption explicitly says median zero reflects zero inflation and low complete-ring coverage; no unsupported edge-effect claim remains. | Stage 2 |
| A08 | MINOR | done | INT | Adaptive rings or minimum-area filters may make penetration summaries more interpretable. | Evaluate whether an adaptive/min-area penetration sensitivity is worth adding, or record a decision not to add it. | Decision/log entry records the choice; if implemented, report includes coverage and sensitivity results. | Stage 2 |
| A09 | MAJOR | done | INT | Trend results need sensitivity to valid-pixel and valid-year thresholds. | Run or script a threshold sensitivity block for inside trends and key quadrant classifications. | Sensitivity table reports stability of headline counts and non-zero tail under alternative thresholds. | Stage 2 |
| A10 | MAJOR | done | PI0.20, INT | Bootstrap uncertainty exists, but rankings/watchlists must not imply over-precise ordering. | Integrate uncertainty probabilities/CIs into risk watchlists and manuscript statements. | Watchlist table includes bootstrap CI/probability fields or explicitly states why uncertainty is reported separately. | Stage 2 |
| A11 | MAJOR | done | AUDIT0.15, MS | Retention quadrant denominator differs from trend denominator and must be stated as selected on valid inside plus valid 1 km `land_unprotected` buffer slopes. | Update figure/table text and Table 1 to make the quadrant denominator and selection rule explicit. | Caption and table values match `risk_rankings_and_quadrants.md` and regenerated data. | Stage 2 |
| A12 | MAJOR | done | MS, INT | Table S1 watchlists are placeholders; category-safe rankings need real values and uncertainty-aware columns. | Fill Table S1 from generated rankings/uncertainty outputs. | Table S1 reproduces category-safe lists with PA identifiers, state, IBRA, slopes, retention index, and uncertainty fields. | Stage 2 |
| A13 | MINOR | done | INT | Dominance matrix is useful but too complex without a simplified table or narrative summary. | Add a simplified dominance summary if it materially improves ranking interpretation. | Stage 2 log records either a generated summary table or a decision to keep the heatmap only. | Stage 2 |
| A14 | MAJOR | done | MS | Table 1 is still a placeholder and is central to making feasibility/censoring transparent. | Generate manuscript-ready Table 1 values from current reports/data. | Table 1 values are traceable to scripts or reports and validated against known counts. | Stage 2 |

## Layer B: conservative biodiversity signal

| ID | Severity | Status | Source | Critique / risk | Required resolution | Validation gate | Target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | MAJOR | verify | AUDIT0.15, PI0.20, EVID | ALA licensing/attribution was a critical blocker; later work created a provider ledger, but release-facing claims must stay mixed-license aware. | Verify all paper/data-availability language points to the ledger and does not imply blanket CC BY reuse of ALA occurrences. | `rg` confirms no stale blanket ALA "CC-BY" claim in paper-facing docs, except historical audits; data availability states redistribution limits. | Stage 3, Stage 4 |
| B02 | MAJOR | verify | AUDIT0.15, PI0.20 | Layer B QC was previously too thin; later QC reports add coordinate, provider, scope, and exposure diagnostics. | Confirm the manuscript and supplementary material use the richer QC, not only the old occurrence summary. | Table/figure/caption references point to `layerB_qc_extended`, `layerB_scope_coverage`, and exposure/model summaries. | Stage 3 |
| B03 | MAJOR | open | AUDIT0.15, EVID, INT | Microbat data are provider/NSW dominated, so national Layer B inference is not defensible. | Frame Layer B as provider-matched, bias-aware secondary evidence, not a national biodiversity trend. | Results/Discussion state inference limits; no national population or causal claim remains. | Stage 3, Stage 4 |
| B04 | MAJOR | open | AUDIT0.15, docs/layerB_gonogo | Negative-control design remains weaker than ideal because Squamata failed and passerines are not a perfect bias match. | Decide whether one provider-matched passerine control plus shuffles is sufficient, or whether another control/sensitivity is required. | Decision recorded; manuscript avoids "negative controls" plural unless justified by implemented tests. | Stage 3 |
| B05 | MAJOR | verify | PI0.20, EVID | Scope and exposure QC now exist, but must be integrated into Layer B table and narrative. | Fill Table S2 and supporting text with model-input n, inside/within fractions, zero mass, providers, and years. | Table S2 values match `layerB_modelling_report.md` and model input summary. | Stage 3 |
| B06 | MAJOR | open | INT, EVID | Falsification collapses `log1p_alan`, but `any_light` remains non-zero and AUC remains slightly above 0.5; interpretation must stay cautious. | Make residual structure central to the Layer B interpretation and avoid overclaiming ecological mechanism. | Manuscript says the signal is weak, associational, and potentially confounded; interpretation notes updated. | Stage 3, Stage 4 |
| B07 | MINOR | open | INT | Robustness to adding stratum/year covariates remains a follow-up. | Decide whether to run this sensitivity or record why existing falsification is sufficient. | Stage 3 plan either includes a run or a documented no-run rationale. | Stage 3 |
| B08 | MINOR | open | INT | IBRA heterogeneity is descriptive and may be unstable with only 11 regions. | Keep IBRA heterogeneity explicitly descriptive; consider coarser region merge only if it changes interpretation value. | Figure/caption/report do not present IBRA effects as confirmatory regional inference. | Stage 3 |
| B09 | MAJOR | open | INT | Occurrence counts and density plots show strong administrative/provider concentration; optional provider/state sensitivity may be useful. | Decide if a provider/state-matched sensitivity panel is needed for manuscript defensibility. | Stage 3 closeout records the decision and, if run, supplies a validated panel/table. | Stage 3 |
| B10 | MAJOR | open | AUDIT0.15 | Sentinel/tiny ALA zip detection was identified as a guardrail need after the failed reptiles download. | Add or verify tests that reject implausibly tiny/sentinel downloads and prevent silent use. | Test fails on a crafted tiny/sentinel zip and passes on valid metadata/zip examples. | Stage 3 |
| B11 | MAJOR | release-gate | AUDIT0.15, EVID | Raw ALA occurrence redistribution is constrained by provider terms. | Final release package must include derived summaries and provenance without redistributing restricted raw records unless permissions allow. | Data availability section and archive manifest match ALA/license policy. | Stage 4 |
| B12 | MAJOR | open | MS | Table S2 is a placeholder and currently cannot serve as a compact Layer B audit table. | Fill Table S2 with primary, falsification, IBRA-shuffle, and sensitivity rows. | Table S2 values match `layerB_modelling_report.md` and include interpretation status for each row. | Stage 3 |

## Reproducibility, evidence, and governance

| ID | Severity | Status | Source | Critique / risk | Required resolution | Validation gate | Target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | MAJOR | release-gate | AUDIT0.15, EVID, STAGE0 | Reconciliation and reproducibility reports verify the evidence snapshot but still record a dirty pre-commit state (`f731562...`) rather than the accepted baseline commit (`dab3ddb`). | Regenerate or supplement the release audit after a clean committed evidence state when preparing final claims. | Release audit records the accepted/release commit and clean or explicitly documented output state. | Stage 4 |
| R02 | BLOCKER | release-gate | EVID, STAGE0 | External archive/DOI for large ignored outputs remains open; `docs/ref_doi.txt` exists but is parked until classified. | Decide archive DOI policy and publish or reference the required large-output checksum manifest. | `data/README.md`, release manifest, and manuscript data availability cite the final archive/DOI and checksums. | Stage 4 |
| R03 | MAJOR | open | USER, STAGE0 | New heavy runs must use `deep-server` under `tmux` and should exploit 64 CPU / 128 GB RAM safely. | Stage 2/3 plans must specify sharding, worker counts, run roots, logs, and recovery checks. | Deep-server commands are tmux-safe and write durable manifests/logs; no long run depends on WSL session survival. | Stage 2, Stage 3 |
| R04 | MINOR | open | AUDIT0.15 | `uv` VIRTUAL_ENV mismatch warning can confuse reproducibility users. | Add a README/troubleshooting note if the warning persists in documented commands. | README or reproducibility audit explains the warning and expected fix/ignore path. | Stage 4 |
| R05 | MAJOR | release-gate | EVID | Large ignored processed tables and raw downloads are checksum-verified locally/remotely but not yet publication-archived. | Create final archive manifest and decide which raw/processed files can be shared. | Archive manifest includes all files required to rerun without network or states explicit exceptions. | Stage 4 |
| R06 | MINOR | open | STAGE0, docs/plan.md, docs/roadmap.md | Older plan/roadmap language can conflict with the new stage ladder by pointing to old WPs as the next action. | Update governance docs only enough to point readers to the stage ladder while preserving historical WP history. | A resume pass following AGENTS lands on `docs/stage_overview.md`/Stage 1+ rather than stale WP0.16 wording. | Stage 4 |
| R07 | MAJOR | open | AGENTS, STAGE0 | Every new work package needs canonical run artefacts and review-cycle notes. | Stage 2 and Stage 3 detailed plans must include canonical artefact folder requirements. | Each completed stage has manifest, outputs, README/log, and interpretation notes for new result artefacts. | Stage 2, Stage 3 |
| R08 | MAJOR | open | AGENTS | Tests/builds are necessary but not enough; result and artefact review cycles must be explicit. | Add per-stage validation bundle: tests/build plus domain sanity/report checks. | Stage closeouts list commands and domain sanity outcomes, not just unit tests. | Stage 2, Stage 3, Stage 4 |
| R09 | MINOR | open | EVID, data/README.md | Layer B license ledger checksums use CRLF-normalized reconciliation, while `data/README.md` may show a different raw checksum convention. | Reconcile or explain checksum convention in the data inventory. | `data/README.md` and reconciliation report agree or explicitly state raw versus normalized checksum semantics. | Stage 4 |

## Manuscript synthesis and claim discipline

| ID | Severity | Status | Source | Critique / risk | Required resolution | Validation gate | Target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M01 | MAJOR | open | USER, MS | Rough manuscript feels not decisive/meaty enough. | Rewrite from hardened evidence after Layer A and Layer B critique items are resolved, not before. | Final Results/Discussion lead with robust findings and quantify limits rather than adding unsupported emphasis. | Stage 4 |
| M02 | MAJOR | open | AUDIT0.15, MS | Figure/table captions must carry denominator, eligibility, censoring, and selection caveats. | Caption pass after regenerated tables/figures. | Every main figure/table caption includes the relevant `n`, selection rule, and caveat where needed. | Stage 4 |
| M03 | MINOR | open | docs/log/114_literature_review_background.md | Plain-text DOI/citation details need a later BetterBibTeX/CSL pass. | Convert/validate references for manuscript production. | Manuscript build uses consistent bibliography entries; no raw DOI-list scaffolding remains in paper text. | Stage 4 |
| M04 | MAJOR | open | AGENTS, MS | Causal or population-decline claims are out of scope for occurrence-only Layer B data. | Enforce claim discipline throughout abstract, Results, Discussion, and captions. | `rg`/manual review finds no causal or population-decline wording unsupported by design. | Stage 4 |
| M05 | MAJOR | open | MS, EVID | Main and supplementary tables remain placeholders, leaving the manuscript less decisive than the evidence package. | Fill Table 1, Table S1, and Table S2 only after Stage 2/3 evidence is accepted. | Tables are generated or manually transcribed from validated reports with cross-checks logged. | Stage 2, Stage 3, Stage 4 |

## Superseded or historical findings retained for traceability

| ID | Severity | Status | Source | Historical critique | Reason superseded / retained note | Validation gate | Target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H01 | BLOCKER | superseded | AUDIT0.15, PI0.20 | "Layer B modelling is NO-GO because licence ledger, QC, scope, and exposure artefacts do not exist." | Later WP0.15b/WP0.20 artefacts created these components. Related integration risks remain as B01, B02, B05, and B06. | Confirm existing reports are included in final evidence package. | Stage 3 |
| H02 | MAJOR | superseded | AUDIT0.15, PI0.20 | "Bias-control readiness not demonstrated." | Later provider-matched modelling, spatial blocking, and block/IBRA shuffle falsification exist. Interpretation and robustness remain open. | Confirm final manuscript reports the weak AUC and residual shuffled structure. | Stage 3 |
| H03 | MINOR | superseded | AUDIT0.15, MS | "ALA is CC-BY" appeared in old go/no-go docs. | Current `layerB_gonogo` and `data/README.md` use mixed-license language. Keep historical audit note only. | Final search excludes historical audit files and confirms no current blanket claim. | Stage 4 |

## Stage 1 gate checklist

- [x] Stable critique IDs assigned.
- [x] Severity/status/target stage assigned.
- [x] Default ownership and signoff rule recorded.
- [x] Older critiques separated into open, verify, release-gate, and superseded categories.
- [x] Layer A hardening items are explicit enough to seed Stage 2 planning.
- [x] Layer B items are retained but staged after Layer A.
- [x] User accepts this matrix as the queue of record. Accepted 2026-05-25.

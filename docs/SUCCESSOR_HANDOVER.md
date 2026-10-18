# DSIPA successor handover

## Active tranche: substantive editorial redevelopment, 18 October 2026

Barry's first read found the paper lacking a compelling, accessible argument.
He authorised substantial revision in asynchronous collaboration with Claude.
The tranche started clean at 59725d3; September work and Claude's prose pass were
committed and pushed in September under Barry's separate authorisation.
The older uncommitted-status wording below is historical.

Current discussion: DSIPA board thread 90, opening message 1912. Claude's first
critique led to a second argument built around an additive product-signal budget
and Kosciuszko. The active title is “Boundary zones and interior hotspots of
brightening in Australia's protected areas”. Main text is 252 abstract + 4,291
body = 4,543 conservative source words. Four main figures are coverage, budget,
paired slopes and Kosciuszko; SI contains Methods S1–S4, Tables S1–S6 and
Figures S1–S5. Earlier figure distribution/trajectories are retained in the SI.

R2 reading files are in `build/final_read/editorial_20261018_r2/` (main/SI PDFs
23/21 pages; Word renders 28/25). The canonical snapshot is
`artefacts/editorial_20261018_r2/`. R1 remains preserved. Native and Word renders,
document identities and final input/output hashes passed. New numerical evidence
has independent replay scripts, corrected-input checksums and a cached offline
Kosciuszko raster comparison. See log 146 and the editorial redevelopment report.

The national outer-band share is 72.0% in 13.7% of sampled area, but 51.2% among
reserves with supported deeper interiors. This geometry qualifier is prominent.
The +479 full-period net becomes −538 in 2013–2021; no stable net brightening or
source attribution is claimed. Kosciuszko ranks 286th by mean OLS and first by
integrated OLS; the earlier 303rd Sen comparison is superseded for this purpose.
Its two clusters supply 96.44% of positive endpoint pixel differences, not net
change or 47% of the same denominator. Three official sources verify proximity
and distinct construction chronologies.

Claude owns candidate `brightening_budget.py`, `brightening_hotspots.py`,
`render_brightening_budget.py` and their proposal/report. Those exploratory prose
files may retain superseded numbers; the integrated manuscript and independent
JSON receipt define R2. Codex owns the final display/replay scripts and active
manuscript integration. Claude's next critique of R2 remains pending; further
changes should begin from that concrete reading copy. No new commit or push was
made in this redevelopment turn. Public release and submission remain separate.

## Current status: corrected private candidate complete and independently approved

The authorised 19 September revision corrects outward buffers, inward bands and
coastal masking. Accurate unsimplified supports use 128 segments per quadrant;
AIMS/eAtlas Australian Coastline 50K replaces the historical coarse land mask.
All 11,133 reserves were re-extracted on deep-server in a clean national v2 run.
Whole-reserve observations and slopes remain exactly unchanged. Paired 1-km
coverage is now 4,253: Q1=347, Q2=70, Q3=3,587, Q4=249. The matched 1–5 km cohort
contains 1,341 reserves; 150 have positive whole slopes and 42 positive deeper
band slopes. Nine paired comparisons near known coastline exceptions have
explicit provisional flags; exclusion gives 4,244 / 341 / 70 / 3,585 / 248.

The optional numerical Layer B section is omitted because original occurrence
inputs could not be recovered to verify a sampling repair. Its archive remains.
The September SI had three methods sections, five tables and three figures; R2 expands it as described above. Corrected
canonical inputs are in data/processed/; flat analysis/reports/ plus the current
interior/edge subdirectories hold the audit outputs. Earlier nested staging
folders are not candidate inputs. See docs/spatial_reproduction_20260919.md.

Frozen executed source, input/runtime manifests and the 928-chunk receipt are
preserved in analysis/reports/spatial_execution_20260919/. Current code has a
post-run polygonal pre-buffer normalization and a schema-only validity-column
amendment. Separate receipts establish unchanged raster values; do not present
the current source as the originally executed snapshot.

Final PDF/Word QA and private packet checks passed. The current reading bundle
is build/final_read/spatial_20260919/; its ZIP is dsipa_rsec_spatial_20260919.zip.
The full private source/evidence package is artefacts/spatial_candidate_20260919/,
with ZIP build/final_read/dsipa_spatial_reproducibility_20260919.zip.
Independent verdict: APPROVE, no open scientific/numerical/artifact blocker.
The final source count is 237 abstract + 3,931 body = 4,168. Main/SI PDF pages
are 21/14; editable Word conversions are 27/17. Full tests154; curated tests38.
Archive identities are in analysis/reports/spatial_candidate_seal_20260919.json. Public Zenodo still holds
the historical baseline. No publication, submission, commit or push is authorised.
Session record: docs/log/144_spatial_review_correction.md.

## Historical scientific close-out: 18 September 2026

Fable's message 225 regards the manuscript as a scientific submission candidate
and closes their requests for this tranche. Astra's reply 230 accepts the
positive-form area statement with an explicit threshold qualification and adds
the dimming comparison. The upper two positive-slope terciles contain 280
reserves and 0.320638% of eligible summed polygon area. The 0.04-unit-per-year
cutoff is descriptive, not an ecological-effect threshold. Seven matched reserves
have negative whole and outer-band slopes: six zero and one negative deeper-band
slopes. No inference of a beyond-5-km origin is made from zero band slopes.

Current bundle: `build/final_read/audit_20260918_closeout/`; ZIP:
`build/final_read/dsipa_rsec_audit_20260918_closeout.zip`.
Canonical snapshot: `artefacts/rsec_audit_20260918_closeout/`.
Source count: 237 abstract + 3,887 body = 4,124 words. SI is unchanged.
See `analysis/reports/product_closeout_review.md`, arithmetic/validation JSONs,
and `docs/log/142_scientific_review_closeout.md`.

Next step is Barry's full main/SI read and author metadata/declarations/AI-use
wording. Curated public code plus a software record and an updated dataset
containing the audit source tables are recommendations, not authorised releases.
No further scientific work is queued absent issues raised by that read.


## Earlier update: 18 September 2026

Fable's review is integrated. The manuscript now foregrounds the 2017 pulse and
2023 synchronous increases, not reassurance from absence of a 2022 spike.
A processing-related dip/rebound is plausible but unidentified. The observed
positive pixel floor is 10 product units in every annual audit window; masking
and derivative-encoding contributions to zeros remain unresolved, and no physical
unit conversion is asserted. Persistence does not distinguish explanations.

The same 1,205-reserve cohort supplies both bands. Among 119 positive-whole cases,
79 have positive 0–1 km and zero 1–5 km slopes, and 30 both positive. Of 68 Q1
losses, 54 have all-zero deeper-band histories and 14 varying positive histories.
This supports selected-cohort outer-ring concentration, not diagnosed spillover.
The lowest count-based positive-slope tercile carries 99.147% of positive-class
summed polygon area; the 37.6% eligible-area share does not measure substantial
change or illuminated land. Supporting Table S5 makes both qualifications visible.

Evidence: `analysis/reports/product_followup_review.md`,
`product_floor_followup.md`, `edge_followup/` and their source/hash manifests.
The floor and edge extensions ran on deep-server in tmux, with accepted inputs
read-only. These are explicitly post-review exploratory checks; the September 17
protocol is preserved. Figure S8 now has separate zero-based distance panels.
Layer B Results are folded into 3.3; Table 1 and Data accessibility are clarified.

Current private bundle: `build/final_read/audit_20260918/`; canonical receipt:
`artefacts/rsec_audit_20260918/`. Main has four figures/one table; SI eight
figures/five tables. Main source count: 234 abstract + 3,826 body = 4,060 words.
See `docs/log/141_fable_review_followup.md` and
`analysis/reports/product_followup_validation.json` for verification.
Prior bundles are unchanged. Work is uncommitted. Final author details,
declarations/AI disclosure, public release and submission remain Barry's decisions.


## Historical update: 17 September 2026

Barry authorised the product-continuity audit, area summaries, interior-band
sensitivity, discretionary Layer B compression and an external anchor only if
necessary. He clarified that he is the sole human author; there is no additional
co-author circulation stage. The current reading version supersedes September
12, while preserving those historical files and the accepted primary analysis.

The 2022 source tag confirms a mixed Suomi-NPP/NOAA-20 EOG V2.2 masked input.
The observed decoded low-end value grid is unchanged despite different integer
encodings. No 2022 first-detection excess appears: inside 14/3,864 versus
13/3,877 in 2021; fixed far-from-2013-light 2/1,239 versus 3/1,242. The original
multi-year distance proposal was prospectively amended to prevent outcome
leakage. The 78 late-positive series remain product observations, not confirmed
environmental onsets; the higher 2023/2024 counts remain unattributed.

Eligible IDs contain 99.8% of summed polygon area; positive-slope IDs contain
37.6% of eligible summed area. These are not unique illuminated land shares.
The common interior-band subset contains 1,205 paired reserves: 32/119 positive
whole-reserve cases retain positive 1–5 km slopes. This cannot locate change at
the boundary or diagnose spillover. Layer B now has only brief main-text methods
and results, with details in SI. Spectral limits cite Kyba et al. (2017).

Use `analysis/reports/product_audit_review.md`, the amended protocol, lineage
review and `interior_area_audit/` for evidence. Current manuscript sources retain
four main figures; SI has eight figures and four tables. The new private bundle
is `build/final_read/audit_20260917/`; canonical receipt:
`artefacts/rsec_audit_20260917/`. See `docs/log/140_product_continuity_audit.md`
for final validation status. Work remains uncommitted; check live Git state.
No external raster anchor was needed for the retained descriptive claims.
Final contact/declaration/AI-use wording, public code release and submission
remain human decisions. No new public deposit, commit or push was made.

## Historical update: 12 September 2026

Barry authorised all five orientation priorities and reconfirmed RSEC, with
remote sensing for conservation as the emphasis. The current title is
**Satellite screening of lighting change across Australia's protected areas**.
The revised source and reading bundle supersede the Goal 016 reader version.
Current workspace: `/home/bwbrook/papers/dsipa-dev`; base commit `907075e`.
Revisions are uncommitted pending Barry's review; verify live Git state.

The accepted primary data, slopes and sign counts are preserved. The new
descriptive annual-series diagnostic finds 180 varying series among 3,969
zero-Sen-slope areas, including 78 with at least one positive value in 2022-2024
after nine zero years. The archived resampling is presented as marginal temporal
sensitivity, not joint spatial inference or calibrated confidence intervals.
The dominance display is excluded. Main Figure 4 now shows four illustrative
reserve trajectories; detailed biological-record methods and its association
figure are in SI. Bibliographic metadata and the derivative product citation
have been checked and corrected.

Use `manuscript/submission/rsec/final_read_guide.md` and
`docs/log/138_rsec_coauthor_revision.md` for the current package and validation.
Author confirmation, co-author comments, code-release arrangements and final
submission remain future decisions. No new public release has occurred.

## Historical handover (5 September 2026)

**Current at 2026-09-05. Read this first in a fresh DSIPA thread, then verify
the live Git state before acting.**

## Operating state

Work directly in `/Users/bwbrook/papers/dsipa-dev`. The historical Chief of
Staff, Goal Composer, project-orchestrator, and named action-agent machinery is
not the current control plane. References to it in old goal packets and logs
are provenance, not instructions to recreate that workflow. Use native Codex
work and bounded subagents only when they materially help.

Observed immediately before adding this handover:

- branch `main` was clean and equalled `origin/main` at `e197461`;
- the latest commit is **Simplify DSIPA active execution path** (Goal 017);
- the four-file final-read bundle exists locally under
  `build/final_read/goal016/`;
- GitHub reports `BWBrook/dsipa-dev` as private; and
- the project is **awaiting Barry's scientific/editorial final read and
  pre-submission decisions**, not awaiting another routine analysis run.

This file was the only working-tree change introduced by the handover task. If
the opening Git check shows anything else, classify it before editing.

Some older status prose says an accepted goal still needs commit/push. Trust
the live history above: Goal 016 is committed as `00e43f0`, Goal 017 as
`e197461`, and `main` matches the remote at handover.

## Scientific contract

The paper is an RSEC Original Research manuscript titled:

> **Detectable change in dark-sky integrity across Australia's protected
> areas**

Its stable design is:

- **Layer A, primary:** annual VIIRS radiance during `2013-2024` inside
  Australian protected areas, in surrounding unprotected land, and in
  interior bands where raster support permits. Outputs are detectability-aware
  categorical screens, not causal diagnoses or management rankings.
- **Layer B, secondary:** a provider-matched, presence-only case-control test
  of whether ALAN covariates distinguish microbat from passerine occurrence
  records. It is weakly discriminating and cannot establish abundance,
  occupancy, population change, or a biological response to ALAN.

The headline evidence is settled for the current manuscript:

- 4,426 of 11,133 protected areas (39.8%) met the primary eligibility rules;
- within that subset, 86.9% had zero inside mean radiance in 2024 and 89.7%
  had a zero Theil-Sen slope;
- among 3,858 areas with paired inside and 1 km surrounding trends, 305 showed
  concurrent brightening and 190 surrounding-only brightening;
- complete three-band interior evidence exists for only 383 areas, so it is a
  selected diagnostic rather than a national gradient; and
- Layer B out-of-block discrimination was weak (`AUC = 0.545`). Each shuffle
  result is one deterministic illustrative realisation, not a sampled null
  distribution or causal counterfactual.

Do not silently strengthen these claims. A VIIRS zero is non-detection at the
product scale, not proof of ecological darkness. Screening categories support
local investigation; fine ordering is uncertain and is not a priority rank.

## What has been completed

The project progressed from a national geospatial pipeline through staged
scientific hardening and manuscript synthesis:

1. Layer A data identities, schemas, eligibility rules, trend outputs,
   uncertainty summaries, and manuscript headlines were reproduced and
   hardened. The accepted reference contract preserves the current scientific
   result.
2. Layer B was retained only as a compact data-adequacy/association diagnostic
   with explicit observation-process and causal limits.
3. The RSEC main manuscript and Supporting Information were consolidated,
   checked, built, and visually reviewed. Goal 016 added exact top-N and
   single-shuffle disclosures without changing data, models, numbers, tables,
   or figure pixels.
4. Nine processed national Layer A outputs were published under CC BY 4.0 as
   Zenodo Dataset `0.3.0`: <https://doi.org/10.5281/zenodo.21524637>. This is a
   dataset DOI, not a software release; raw/row-level ALA data and Layer B
   payloads remain excluded.
5. Goal 017 simplified the active execution path: shared fail-closed Git-state
   handling, one canonical Layer B flow, a proportional `make fast` gate, and
   removal of two obsolete release helpers. It did not alter accepted science
   or manuscript surfaces. Its checks passed: `make fast` 57 tests; `make
   test` 97 tests with 9 data-dependent skips; targeted guards, shell syntax,
   a temporary package build, and protected-surface checks also passed.

## Live review surface

Barry's primary reading bundle is:

1. `build/final_read/goal016/dsipa_rsec_final_read_main.pdf`
2. `build/final_read/goal016/dsipa_rsec_final_read_main.docx`
3. `build/final_read/goal016/dsipa_rsec_final_read_supporting_information.pdf`
4. `build/final_read/goal016/final_read_guide.md`

The authoritative tracked guide is
`manuscript/submission/rsec/final_read_guide.md`. Also read, as needed:

- `manuscript/text/manuscript_draft.md` for the scientific narrative;
- `manuscript/submission/rsec/code_release_decision.md` for the public-code
  fork;
- `analysis/reports/final_release_manifest.md` for release provenance; and
- `docs/goals/017-lean-path-consolidation/Lean_Path_Consolidation_Closeout.md`
  for the present engineering surface.

Treat `docs/roadmap.md`, early `docs/plan.md` status cues, and old goal packets
as history unless a live caller or current decision still depends on them.
Do not ingest the whole archive to bootstrap routine work.

## Where the project is heading

The next meaningful boundary is Barry's full read. The recommended sequence is:

1. Receive and classify Barry's manuscript/SI comments and the unresolved
   human metadata: author order, affiliations/ORCIDs, correspondence,
   contributions, acknowledgements, conflicts, ethics, exact AI-use
   disclosure, and final author approvals.
2. Frame one bounded pre-submission tranche that incorporates those decisions,
   updates journal requirements from current official sources, fixes only
   verified issues, rebuilds the reader/submission assets, and reruns the
   decision-relevant validation ladder.
3. Resolve the public-code decision separately. The recorded preferred route
   is a curated clean-history public code repository plus a distinct Zenodo
   Software record, but Barry has not authorized that action. The alternative
   is to retain private code and seek editorial guidance.
4. Ask for explicit final authority before any Wiley login, upload, submission,
   licence, fee/APC, repository-visibility, public-code, tag, release, or other
   external action.

One known pre-submission defect is deliberately unresolved: Fig. 4's internal
plotted title still uses the legacy word `falsification`. Its caption and prose
correctly describe the shuffles as illustrative benchmarks. Fix the title
reproducibly from the preserved Layer B evidence or an independently verified
summary-only rendering route; do not edit figure pixels by hand.

Do not launch national, ALA, model, remote, archive, or manuscript-regeneration
work merely to refresh confidence. Run it only when Barry's review, a changed
claim, or a named release risk makes it decision-relevant.

## Recommended skills and cadence

Use `$twilight-laboratory`
(`/Users/bwbrook/.codex/skills/twilight-laboratory/SKILL.md`) as the primary
programme discipline: recover live state, preserve settled science, propose a
coherent decision-bearing tranche, and involve Barry at consequential
scientific or external-action boundaries. Its governing standard fits this
project: **rigour at the scientific decision boundary; proportional
engineering everywhere else**.

Use `$kill-your-darlings`
(`/Users/bwbrook/.codex/skills/kill-your-darlings/SKILL.md`) when evaluating
additional machinery, tests, reports, compatibility paths, or public-release
scope. Make each part earn its recurring cost; preserve scientific validity,
source integrity, restricted-data boundaries, and independent evidence.

For a fresh-thread orientation, remain read-only until the user asks for a
change. Start with:

```bash
pwd
git status --short --branch
git log --oneline -8
```

Then read this note, `AGENTS.md`, the final-read guide, and only the specific
evidence needed for the requested decision. The useful restart question is
not "what old goal comes next?" but "what decision or manuscript outcome does
Barry now want, and what is the smallest defensible tranche that reaches it?"

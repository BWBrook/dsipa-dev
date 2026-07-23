# Goal 013 RSEC Manuscript Consolidation Closeout

Date: 2026-07-24

Status: **COMPLETE; ready for orchestrator scientific review, with no commit or
push**.

## Conclusion

The DSIPA manuscript is now a coherent RSEC-targeted Original Research paper
centred on Layer A. Its principal contribution is a detectability-aware
national assessment showing widespread non-detection among evaluable protected
areas alongside a concentrated, spatially uneven set of inside and surrounding
unprotected-land brightening signals.

The management output is categorical screening rather than competitive
ranking. Layer B remains in the main paper as a compact assessment of the
unresolved exposure-to-biological-response bridge. It now states its actual
microbat-versus-passerine record-identity response and no longer treats
attenuation under ALAN shuffling as proof of confounding or non-robustness.

Exact title:

> Detectable change in dark-sky integrity across Australia’s protected areas

## Starting And Final Git State

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- Start/final HEAD:
  `b38366110477e69ca92e269faecbe950965a6b92`
- Start/final `origin/main`:
  `b38366110477e69ca92e269faecbe950965a6b92`
- Starting status: clean apart from the authorized untracked Goal 013 packet.
- Final status: expected Goal 013 manuscript, stage-pointer, log, packet, and
  closeout changes only.
- Commit: none.
- Push: none.

## Exact Changed Files

Manuscript:

- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/supplementary_figures.md`

Goal and stage records:

- `docs/stage_overview.md`
- `docs/log/133_rsec_manuscript_consolidation.md`
- `docs/goals/013-rsec-manuscript-consolidation/Goal.md`
- `docs/goals/013-rsec-manuscript-consolidation/Plan.md`
- `docs/goals/013-rsec-manuscript-consolidation/Runbook.md`
- `docs/goals/013-rsec-manuscript-consolidation/Log.md`
- `docs/goals/013-rsec-manuscript-consolidation/RSEC_Manuscript_Consolidation_Closeout.md`

No reference file changed because no citation repair was needed.

## Journal Counts And Method

Counts use whitespace-delimited tokens within explicit Markdown section
boundaries:

```bash
awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w
awk '/^## 1\. Introduction/{on=1}/^## Data accessibility/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w
awk '/^## 1\. Introduction/{on=1}on' \
  manuscript/text/manuscript_draft.md | wc -w
```

Results:

- abstract: 235 words (limit 300);
- IMRAD main text: 4,609 words;
- IMRAD plus Data accessibility: 4,683 words;
- keywords: 5 (required 4-6);
- main figures: 4;
- main tables: 1;
- supplementary figures: 7;
- supplementary tables: 2.

The manuscript meets the 5,000-word limit under both the IMRAD-only and the
more conservative IMRAD-plus-accessibility count.

## Scientific And Assembly Changes

### Layer A

- Replaced the previous method-led title with the approved RSEC title.
- Defined dark-sky integrity operationally as detectable annual-composite
  upward radiance, not organism-experienced darkness or sky brightness.
- Made measurement support and eligibility part of the result.
- Centred the accepted headline:
  - 11,133 protected-area universe;
  - 4,426 eligible for the primary inside assessment;
  - 3,844/4,426 zero inside mean in 2024;
  - 3,969/4,426 exact-zero slopes;
  - 420/4,426 positive slopes.
- Made the corrected 1 km unprotected-land comparison the principal
  management-facing analysis.
- Replaced causal or directional category language with concurrent,
  inside-only, stable/non-detect, and surrounding-only brightening.
- Retained the interior-band result only as a selected diagnostic.
- Reframed bootstrap values as intervals and empirical resampling frequencies,
  not posterior probabilities or precise management ranks.

### Layer B

- Defined the response as microbat-versus-passerine occurrence-record identity.
- Explained the biological motivation for microbats as nocturnal,
  insect-associated surrogates.
- Made specialist/acoustic detection and differing taxon observation processes
  explicit.
- Stated that provider matching does not control protocol, detector use,
  access, habitat, geography, effort, or taxon-specific detectability.
- Preserved primary AUC/log loss of approximately 0.545/0.689 and the accepted
  shuffle and sensitivity metrics.
- Corrected permutation logic: shuffles break the exposure-label pairing and
  provide null benchmarks; attenuation does not diagnose whether the original
  association was ecological or observational.
- Moved the occurrence-exposure figure to Supporting Information and retained
  one compact Layer B model/null-benchmark diagnostic in the main sequence.

### Data accessibility

- Distinguished public, provenance-recorded Layer A inputs from national
  outputs designated for a later archive.
- Stated that no archive DOI has yet been minted.
- Kept derived Layer B summaries and figures as the manuscript-facing evidence.
- Stated that raw and row-level ALA records are not redistributed and must be
  reacquired under provider terms for exact Layer B reconstruction.

## Evidence Reconciliation

All current main and supplementary manuscript text, captions, and tables were
scanned against the accepted Goal 012 reference contract and accepted Layer B
report.

Layer A values match the Goal 012 contract:

- PA universe: 11,133;
- primary eligible subset: 4,426;
- zero inside mean: 3,844;
- zero inside slopes: 3,969;
- positive inside slopes: 420;
- paired-screening denominator: 3,858;
- Q1/Q2/Q3/Q4: 305/55/3,308/190;
- ring 1 valid: 1,432/11,133, rendered 12.9%;
- complete bands: 383.

Layer B values match `analysis/reports/layerB_modelling_report.md`:

- 50,281 records per class;
- primary AUC/log loss: 0.545/0.689;
- block-shuffle AUC: 0.505;
- IBRA-by-year-shuffle AUC: 0.517;
- all-provider sensitivity AUC: 0.557.

The stale-value scan found zero `1,427` or `12.8%` hits in current manuscript
surfaces. The title scan found one exact approved title.

## Validation Evidence

### Final manuscript check

`make ms-check`: **passed**.

- tool check: passed;
- draft and fixture config validation: passed;
- Makedoc tests: 61 passed;
- manuscript lint: passed;
- bibliography keys: 30;
- cited keys: 24;
- unknown citation keys: 0;
- unused keys: 6, non-fatal;
- author metadata checks: passed;
- build check: passed.

### Final build

`make ms-build`: **passed**.

Build products:

| Product | Size | SHA-256 |
| --- | ---: | --- |
| `build/draft/dsipa_draft.pdf` | 1,172,647 bytes; 37 pages | `098c04b5b9d0ec606b2fab9e1f722ce66e574f6ca02712d4abb189ba588152f4` |
| `build/draft/dsipa_draft.docx` | 1,064,966 bytes | `aa4d39d229f470a30fceaf2ba18dce6226b904d4b73e126e9ad1148fd8d8526e` |
| `build/draft/dsipa_draft_build_manifest.json` | 5,570 bytes | `f3d478ef76eadbe20637ec217328ea3023c5a1d2c2557cd76e0971c1fc04da5e` |

The built PDF was inspected in reading order. Title, author metadata, abstract,
section structure, citations, Table 1, supplementary tables, and display
captions were present.

### Scans And Assembly Checks

- `git diff --check`: passed.
- stale `1,427|12.8%` scan: zero manuscript hits.
- current `1,432|12.9%` scan: consistent hits in manuscript Results, Table 1,
  and Fig. S1 caption.
- `audit`, `remain dark`, `external pressure`, `penetration`, and
  `internalisation` scan: no affirmative manuscript claim; the only
  competitive-ranking hit is an explicit negation in Table S1 guidance.
- causal/population scan: hits are explicit statements of non-inference.
- Layer B scan: provider matching, observation process, acoustic detection,
  weak discrimination, AUC, shuffles, and null-benchmark language are present
  and consistent.
- accessibility scan: DOI, archive, raw/row-level ALA, and redistribution hits
  are explicit restrictions or pending status.
- citation/reference audit: zero unknown keys.
- display order:
  - main: Layer A baseline, Layer A trends, Layer A categorical
    inside/surrounding screen, Layer B association/null benchmarks;
  - supplementary: conditional interior bands, trend uncertainty, ordering
    uncertainty, occurrence exposure, occurrence counts, occurrence density,
    descriptive IBRA heterogeneity.
- Figure and table references in the manuscript agree with this order:
  Figs 1-4, Figs S1-S7, Table 1, and Tables S1-S2.

## Focused Scientific Review

One post-build review identified three material wording/label defects:

1. a Results sentence risked attributing inferential force to shuffle
   attenuation rather than to the primary model's weak discrimination;
2. Table S1 still used `Internalisation`, which implied direction beyond the
   descriptive contrast; and
3. Table S1 retained a `rank` heading despite the categorical-screening
   decision.

The sentence now compares the primary AUC with the near-null benchmarks
without diagnosing cause. The category is now `Inside-minus-surrounding
contrast`, and the column is `source_order` with an explicit non-priority
definition. The affected scans, `git diff --check`, `make ms-check`, and
`make ms-build` all passed after repair. No further review loop was started.

## Residual Limitations

1. Local pre-Goal-012 report copies
   `analysis/reports/layerA_denominators_and_censoring.md` and
   `analysis/reports/layerA_table1_candidate.md` still contain historical
   1,427/12.8% text. The accepted Goal 012 machine-readable reference contract,
   closeout, remote run artefact, and current manuscript use 1,432/12.9%.
   Repairing report/release surfaces was outside Goal 013 and remains necessary
   before final packaging.
2. The generated Makedoc build manifest records Git SHA
   `3a52e7059fb069c854b49d8f0a1991aface33d75`, which is the clean Makedoc
   checkout, not the DSIPA action-repo baseline
   `b38366110477e69ca92e269faecbe950965a6b92`. The manifest must not be used as
   DSIPA source-state provenance until the build tooling records both
   identities correctly.
3. The manuscript remains a working RSEC draft. Final author contributions,
   declarations, cover letter, journal production styling, final archive DOI,
   and submission package were outside scope.
4. Layer B remains intrinsically unable to estimate biological response from
   the available opportunistic record design.
5. Table S1 is a dense supporting table and may need production formatting,
   but further formatting polish did not justify another Goal 013 loop.

## Recommendation

Accept Goal 013. The scientific manuscript has reached the intended 80/20
RSEC-ready state without new science or overclaiming.

The next highest-value tranche is a bounded release/submission-production goal
that reconciles the remaining local report/release surfaces to Goal 012,
corrects dual-repository build provenance, prepares the approved Option B
archive candidate and provisional availability statement, and assembles the
RSEC submission components without minting or citing a DOI until final
authorization.

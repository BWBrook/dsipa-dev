# Goal 013: RSEC Manuscript Consolidation

## Objective

Turn the accepted DSIPA evidence package into a coherent Original Research
manuscript for *Remote Sensing in Ecology and Conservation* (RSEC), without
changing the science.

The manuscript must make Layer A the clear centre of gravity, present the
inside-versus-unprotected-land comparison as categorical management screening,
and retain Layer B as a compact assessment of why opportunistic occurrence
records cannot securely bridge remotely sensed ALAN exposure to biological
response.

This is a bounded scientific-writing and manuscript-assembly goal. It is not a
new analysis, release, archive, or submission goal.

## Starting State

- Action repo: `/Users/bwbrook/papers/dsipa-dev`
- Required branch: `main`
- Required HEAD and `origin/main`:
  `b38366110477e69ca92e269faecbe950965a6b92`
- Required starting status: clean (`## main...origin/main`)
- Accepted analysis period: 2013-2024
- Accepted Layer A evidence: Goal 012 closeout and its reference contract
- Target journal: *Remote Sensing in Ecology and Conservation*
- Article type: Original Research

Stop before mutation if the branch, HEAD, remote-tracking state, or clean
status differs. Do not reset, clean, or reconcile unexpected work.

## Fixed Editorial And Scientific Decisions

### Journal Contract

- Exact title:
  **Detectable change in dark-sky integrity across Australia’s protected
  areas**
- Main text: no more than 5,000 words, excluding acknowledgements, references,
  and table/figure legends.
- Working target: 4,600-4,800 main-text words.
- Abstract: no more than 300 words.
- Keywords: 4-6.
- Use the conventional Introduction, Materials and Methods, Results, and
  Discussion structure.
- Retain an accurate data-accessibility statement.

### Contribution And Narrative

The one-sentence contribution to preserve across the Abstract, Introduction,
Discussion, and conclusion is:

> A detectability-aware national VIIRS assessment shows that most evaluable
> Australian protected areas had no detectable interior radiance change during
> 2013-2024, while corrected unprotected-land buffers identify a smaller,
> uneven set of management-relevant internal and surrounding brightening
> signals; opportunistic microbat records cannot establish the corresponding
> biological response.

Layer A is primary. Its defensible headline is:

- most evaluable protected areas show no detectable change in annual-composite
  interior radiance;
- the result is conditional on eligibility: 4,426 of 11,133 protected areas;
- detectable brightening is concentrated and spatially uneven rather than a
  protected-area-system-wide shift; and
- corrected unprotected-land buffers provide the principal management-facing
  comparison.

Use `assessment`, not `audit`, as the organising term. Describe management
outputs as categorical screening, not competitive ranking. Do not use
`remain dark`, `external pressure`, or `penetration` where those phrases imply
true ecological darkness, causation, governance failure, or a nationally
general edge process beyond the estimand.

Interior rings are selected, conditional diagnostics because complete-ring
coverage is only 383 protected areas. Bootstrap summaries may express
uncertainty in estimated trends and screening confidence, but must not imply
precise ranks, posterior probabilities, or a national league table.

### Layer B Contract

Layer B is a compact secondary assessment of the difficulty of linking ALAN
exposure to biological response.

- Its statistical response is microbat-versus-passerine occurrence-record
  identity, not abundance, occupancy, population trend, decline, or causal
  ecological response.
- Microbats were biologically motivated as nocturnal, insect-associated
  surrogates, but are difficult to observe without specialist and often
  acoustic methods.
- Provider matching controls provider identity only. It does not control
  observation protocol, detector use, access, habitat, geography, or
  taxon-specific detectability.
- Spatial blocking and provider matching are safeguards, not proof that
  observation-process confounding has been removed.
- ALAN shuffles are null benchmarks. Attenuation after breaking the
  exposure-label association does not itself prove confounding,
  non-robustness, or absence of a biological association.
- Limited inference rests on weak out-of-block discrimination and uncontrolled
  observation processes.

Layer B may remain in the main paper, but it must not compete with Layer A for
space or narrative emphasis.

## Frozen Quantitative Contract

All manuscript-facing values must reconcile to accepted Goal 012 evidence.
Core values include:

- protected-area universe: 11,133;
- eligible inside baseline/trend subset: 4,426 (39.8%);
- 2024 zero inside mean: 3,844/4,426 (86.9%);
- exact-zero inside slopes: 3,969/4,426 (89.7%);
- positive inside slopes: 420/4,426 (9.5%);
- retention/quadrant denominator: 3,858;
- Q1/Q2/Q3/Q4: 305/55/3,308/190;
- ring 1 (1-5 km) valid: 1,432/11,133 (12.9%);
- complete rings: 383/11,133 (3.4%);
- provider-matched Layer B sample: 50,281 records per class;
- primary AUC/log loss: approximately 0.545/0.689;
- block-shuffle AUC: approximately 0.505;
- IBRA-by-year-shuffle AUC: approximately 0.517; and
- multi-provider sensitivity AUC: approximately 0.557, descriptive only.

The historical 1,427/12.8% ring-1 value must not remain in current manuscript,
table, or caption surfaces. It belongs only in historical reconciliation
records outside this manuscript goal.

## Required Outcomes

### 1. RSEC-Compliant Manuscript

Apply the exact title and produce a coherent manuscript within the journal
limits. Record reproducible counts for:

- abstract words;
- main-text words under the stated exclusions;
- keywords;
- main figures and tables; and
- supplementary figures and tables.

### 2. Layer A-Centred Scientific Story

The Abstract, Introduction, Results, Discussion, and conclusion must share one
narrative:

1. dark-sky integrity is operationally assessed through detectable upward
   radiance, not organism-experienced darkness;
2. eligibility and the annual-product floor bound inference;
3. detectable change is concentrated and uneven;
4. corrected surrounding unprotected-land comparisons support categorical
   management screening; and
5. rings and fine ordering are conditional or uncertain.

### 3. Compact And Defensible Layer B

State the actual response, observation process, weak discrimination, and
limits of the null benchmarks accurately. Explain the microbat-surrogate
motivation and specialist-observation limitation without inventing new
biological results.

Move extended occurrence counts, exposure diagnostics, and IBRA heterogeneity
to Supporting Information where possible. Retain only the minimum main-text
methods, result, and interpretation needed to preserve the integrated
exposure-to-response story.

### 4. Main And Supporting Display Hierarchy

Privilege Layer A in the main display sequence. The expected main displays are:

- Layer A baseline/eligibility map;
- Layer A trend distribution;
- Layer A categorical inside-versus-unprotected-land comparison;
- one compact Layer B model/null-benchmark diagnostic; and
- the Layer A denominator/feasibility table.

Ring diagnostics, bootstrap forest/dominance displays, occurrence
counts/density/exposure diagnostics, and IBRA heterogeneity belong in
Supporting Information unless the existing assembly makes a different
text-only placement materially clearer.

Display changes are limited to manuscript assembly, ordering, references, and
captions. Do not regenerate, edit, or replace figure image files.

### 5. Evidence And Data-Accessibility Alignment

Scan all main and supplementary text, captions, and tables for stale or
conflicting values. Compare every quantitative claim with Goal 012 evidence
and accepted Layer B reports.

Data-accessibility wording must distinguish:

- public, provenance-recorded Layer A inputs;
- accepted Layer A outputs intended for a later external archive;
- tracked derived Layer B summaries; and
- restricted raw and row-level ALA records that will not be redistributed.

Do not claim that an archive or DOI already exists. Do not promise exact Layer
B regeneration from redistributed raw records.

## Permitted Mutation Boundary

Implementation may create or modify only:

- `manuscript/text/manuscript_draft.md`;
- `manuscript/text/tables.md`;
- `manuscript/text/figures.md`;
- `manuscript/text/supplementary_tables.md`;
- `manuscript/text/supplementary_figures.md`;
- `manuscript/text/references.md`, only if an existing citation repair is
  necessary;
- `references/refs.yaml`, only if an existing citation repair is necessary and
  supported by a verified source;
- `docs/goals/013-rsec-manuscript-consolidation/Log.md`;
- `docs/goals/013-rsec-manuscript-consolidation/RSEC_Manuscript_Consolidation_Closeout.md`;
- `docs/log/133_rsec_manuscript_consolidation.md`; and
- `docs/stage_overview.md`, only for a narrow Goal 013 status pointer.

Do not mutate any other file without explicit orchestrator approval. If a
required fix appears to need another surface, stop and request scope expansion
before editing it.

## Acceptance Criteria

- Starting state matches the required clean baseline.
- Exact approved title is used.
- Abstract is at most 300 words; main text is at most 5,000 words and targets
  4,600-4,800; there are 4-6 keywords.
- Layer A is visibly primary in section length, display order, Abstract,
  Discussion, and conclusion.
- All claims condition inference on measurement support and eligibility where
  required.
- Management output is categorical screening; no precise competitive-ranking
  claim remains.
- Layer B states the actual response and observation-process limitations and
  interprets permutation nulls correctly.
- Every quantitative claim matches accepted evidence, including 1,432/12.9%;
  no current manuscript surface retains 1,427/12.8%.
- Main and supplementary display references, numbering, order, and captions
  agree with manuscript assembly.
- Data accessibility is accurate and makes no DOI or raw/row-level ALA
  redistribution claim.
- Citation/reference checks find no unknown citation keys.
- `git diff --check`, `make ms-check`, and `make ms-build` pass.
- One focused scientific self-review and repair pass finds no material
  text-evidence mismatch; further polish then stops under the 80/20 policy.
- The final diff is limited to the permitted mutation boundary.
- The closeout records exact changed files, build products, checks, counts,
  evidence cross-checks, and residual limitations.
- No commit or push occurs before orchestrator acceptance.

## Non-Goals

No 2025 VIIRS, new science, model changes, data processing, ALA reacquisition,
figure regeneration, source-code or test changes, release-manifest repair,
archive recovery, Zenodo upload, DOI minting, release packaging, cover letter,
submission, remote compute, broad bibliography expansion, or stylistic polish
beyond the focused manuscript pass.

## Stop And Escalation Rules

Stop and report without improvising if:

- the baseline or permitted footprint differs;
- a manuscript number conflicts with accepted Goal 012 evidence;
- a claim requires an unavailable source or inaccessible primary evidence;
- a defensible revision would require new analysis, modelling, data
  processing, figure regeneration, or a new citation;
- scientific ambiguity would change the contribution or accepted
  interpretation;
- any required edit falls outside the permitted mutation boundary;
- validation still fails after one focused repair;
- the manuscript cannot meet the RSEC word limit without removing
  scientifically necessary information; or
- further work is only marginal polish after the focused repair.

On completion or blockage, send the orchestrator a short wake-up containing
the status and the Goal 013 closeout path, then stop.

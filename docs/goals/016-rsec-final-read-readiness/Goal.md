# Goal 016: RSEC Final-Read Readiness

## Objective

Prepare a decision-ready, explicitly non-submission-ready final-read bundle
for Barry for the manuscript:

> Detectable change in dark-sky integrity across Australia’s protected areas

The bundle must contain the RSEC main manuscript PDF and DOCX, the
authoritative Supporting Information PDF, and a concise final-read guide. The
work may make only the bounded transparency, disclosure, and readability edits
defined below. It must not change data, models, numerical results, scientific
conclusions, the 2013-2024 period, the categorical screening framework, the
title, or the public data DOI.

Barry has approved taking the package to his full final read. That approval
does not authorize Wiley login or submission, public code or additional-data
publication, repository visibility changes, a Git tag or release, a journal
licence, a fee or APC commitment, or any other external publication action.

## Starting State

- Action repository: `/Users/bwbrook/papers/dsipa-dev`
- Required branch: `main`
- Packet-authoring HEAD and `origin/main`:
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`
- Packet-authoring status: clean (`## main...origin/main`)
- Journal: *Remote Sensing in Ecology and Conservation* (RSEC)
- Article type: Original Research
- Fixed title:
  **Detectable change in dark-sky integrity across Australia’s protected
  areas**
- Fixed analysis period: `2013-2024`
- Public Layer A data DOI:
  <https://doi.org/10.5281/zenodo.21524637>
- Source repository: private; it must remain private during Goal 016
- Current RSEC counts:
  - abstract: `235`
  - IMRAD plus Data accessibility: `4,685`
  - conservative abstract plus body: `4,920`
  - keywords: `5`
- Current build assets:
  - `build/submission/dsipa_rsec_main.pdf`
  - `build/submission/dsipa_rsec_main.docx`
  - `build/supplementary/dsipa_rsec_supplementary.pdf`
  - diagnostic/non-submittable:
    `build/supplementary/dsipa_rsec_supplementary.docx`

At execution start, record `pwd`, branch, HEAD, `origin/main`, status, and
recent history. Stop before mutation if the Goal 016 packet is not the only
explainable change or if the accepted Goal 015 baseline does not remain an
ancestor.

## Evidence And Decision Classification

### Observed facts

- Goal 015 published and independently verified the nine processed Layer A
  outputs at the DOI above.
- The GitHub source repository remains private.
- The existing RSEC profiles produce a main PDF/DOCX and a separate
  authoritative SI PDF.
- Current manuscript science is accepted and Layer A-centred; Layer B remains
  a limited, provider-bounded test of occurrence-record discrimination.
- Table S1 already contains 20 rows in each of three screening categories.
- Current Fig. S2 and Fig. S3 captions do not state their exact top-N
  selection rules.
- The two Layer B shuffle benchmarks are currently described more generally
  than their actual evidential status as one seeded realisation each.
- The main manuscript has a public Layer A data citation but describes source
  code and derived Layer B materials as private.

### Barry-provided decisions

- Proceed to a full final-read bundle, but do not submit or publish anything
  externally.
- Freeze all data, models, results, title, period, categorical screening
  outputs, and the public data DOI.
- Retain Fig. 4 in the main manuscript.
- Permit only modest Layer B prose compression.
- Research funding is known as: **no specific funding**.
- Keep all other human-controlled claims visibly unresolved.
- Keep `dsipa-dev` private.
- Prefer, for a later separately authorized goal, a curated clean-history
  public code repository plus a separate Zenodo Software record.

### Executor inference and recommendation

- Current official-source evidence makes a citable public code release a
  material pre-submission decision, especially if Barry confirms that AI
  assisted analytical code. Goal 016 may document this decision but may not
  publish code or represent an unsettled policy interpretation as certain.
- Public Layer A outputs do not by themselves make the private source code or
  Layer B reproduction path public.
- The final-read package can be decision-ready while authorship,
  declarations, code release, and submission authority remain open.

### Human decisions that remain open

- final manuscript author list and order;
- exact affiliations and ORCIDs;
- responsible corresponding author, institutional email, and full address;
- author contributions;
- acknowledgements other than the known no-specific-funding statement;
- conflicts of interest;
- ethics/consent applicability and exact wording;
- exact AI-use disclosure by research role, tool, version, purpose, and access
  date;
- all-author approval, accountability, and sole-submission confirmation;
- code and Layer B derived-output publication;
- Wiley submission, APC/fee coverage, journal licence, and final submission
  authority.

Every unresolved field must remain visibly labelled `[BARRY CONFIRM]`,
`[PRE-SUBMISSION DECISION]`, or equivalent. Dataset creator metadata from
Zenodo must not be used to infer manuscript authorship.

## Current RSEC Requirements Evidence

Official sources were checked on 2026-07-26:

- RSEC author guidelines:
  <https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/author-guidelines>
- RSEC article publication charges:
  <https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/article-publication-charges>
- RSEC open-access licence and copyright:
  <https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/open-access-license-and-copyright>
- Wiley submission help:
  <https://authors.wiley.com/help/submitting-your-manuscript.html>
- Wiley data-sharing policy:
  <https://authors.wiley.com/author-resources/Journal-Authors/open-access/data-sharing-citation/data-sharing-policy.html>
- Wiley figure guidance:
  <https://authors.wiley.com/author-resources/Journal-Authors/Prepare/manuscript-preparation-guidelines.html/figure-preparation.html>
- Wiley Supporting Information guidance:
  <https://authors.wiley.com/author-resources/Journal-Authors/Prepare/manuscript-preparation-guidelines.html/supporting-information.html>
- Wiley Australia/New Zealand CAUL agreement:
  <https://authors.wiley.com/author-resources/Journal-Authors/open-access/affiliation-policies-payments/caul-agreement.html>

The journal pages returned HTTP 403 to direct automated fetches. Current
official Wiley/ZSL indexed content, crawled within days of the check, supplied
the requirements used here. The live Research Exchange form remains
uninspected and may contain additional conditional fields.

Current evidence supports:

- Original Research maximum `5,000` words, excluding acknowledgements,
  references, and table and figure legends;
- abstract maximum `300` words;
- `4-6` keywords;
- conventional IMRAD structure;
- double spacing and continuous line numbers;
- running title maximum `45` characters;
- component word-count breakdown;
- title-page authorship, affiliation, contact, and corresponding-address
  fields;
- funding, conflict, applicable ethics, data accessibility, and AI-use
  disclosures;
- final-format Supporting Information; and
- a data/code availability decision that distinguishes public evidence from
  private source.

Do not assert that CRediT, ORCID for every author, preferred reviewers, a
specific licence, or a particular APC outcome is a confirmed RSEC hard
requirement unless later official or live-workflow evidence establishes it.

## Frozen Scientific Contract

The following are immutable in Goal 016:

- all raw, processed, and archived data;
- all model objects, code, tests, configurations, seeds, and analysis reports;
- all numerical results, denominators, percentages, intervals, AUCs,
  coefficients, and table cells;
- all figure pixels and plotted values;
- the `2013-2024` study period;
- the fixed title;
- DOI `10.5281/zenodo.21524637`;
- Fig. 4's main-manuscript placement;
- Layer A as the primary contribution;
- Layer B as secondary, provider-bounded, presence-only, case-control, weakly
  discriminating, and non-causal;
- screening categories as investigation aids, never competitive management
  rankings.

If a transparency edit appears to require regenerated data, a changed table
row, a changed plotted set, a new calculation, or a different model
interpretation, stop and return the mismatch. Do not repair it within this
goal.

## Required Transparency Corrections

### Table S1

State explicitly that Table S1 shows the top 20 rows within each of three
screening categories, with the selection/order metric named for each:

1. `Inside brightening`: descending point-estimate `inside_slope`;
2. `Surrounding-only brightening`: descending point-estimate
   `buffer_1km_slope`; and
3. `Inside-minus-surrounding contrast`: descending point-estimate
   `retention_1km`, defined as inside slope minus 1 km unprotected-land
   surrounding slope.

Also state that this source order provides a transparent screening display,
not a competitive priority rank. Do not change any Table S1 row, value,
category, or order.

### Figures S2 And S3

- Fig. S2: disclose that the displayed set is the top 20 protected areas by
  bootstrap-median inside slope.
- Fig. S3: disclose that the displayed set is the top 15 protected areas used
  for pairwise bootstrap ordering frequencies.
- Preserve the existing uncertainty and non-ranking interpretation.
- Do not regenerate or alter either figure.

### Layer B shuffle benchmarks

For both the spatial-block shuffle and the IBRA-by-year shuffle, state
consistently in Methods, directly corresponding results/discussion prose,
Table S2 notes, and Fig. 4 caption that:

- each benchmark is one deterministic seeded realisation;
- it is an illustrative benchmark, not a sampled null distribution;
- attenuation after shuffling does not identify whether the original
  association was biological or observational; and
- neither shuffle supplies a causal counterfactual.

Do not add repetitions merely to satisfy a keyword scan. Use the fewest
locations needed to prevent a reader from mistaking either shuffle result for
a null distribution.

### Layer B compression

Compress only repeated Layer B caveat and benchmark wording. Preserve every
numerical result, design limitation, observation-process caveat, non-causal
boundary, and Fig. 4. Aim for useful word-budget headroom; do not remove more
than `250` net words from Layer B without orchestrator review.

### Reproducibility wording

Distinguish:

- **internal engineering state**: versioned, scripted, tested, pinned, and
  supported by local run manifests; from
- **public reproducibility state**: processed Layer A outputs are public, but
  source code, derived Layer B materials, and the full runnable environment
  are not yet provided through a citable public software release.

The manuscript, declarations, cover letter, checklist, final-read guide, and
code-release decision memo must not imply that a private GitHub repository is
public or that the Zenodo Dataset DOI is a software archive.

## Required Deliverables

1. Bounded manuscript and SI transparency edits implementing the exact rules
   above, with no new analysis.
2. Three new local decision/readiness documents:
   - `manuscript/submission/rsec/final_read_guide.md`
   - `manuscript/submission/rsec/code_release_decision.md`
   - `manuscript/submission/rsec/figure_production_inventory.md`
3. Relevant RSEC README, checklist, metadata, counts, declarations, and cover
   letter reconciled to the final-read state.
4. Known research funding drafted as `No specific funding`; all other human
   claims visibly unresolved.
5. A full component word-count table and a post-edit conservative recount.
6. A local Barry reader bundle containing exactly:
   - main PDF;
   - main DOCX;
   - authoritative SI PDF; and
   - final-read guide.
7. The diagnostic SI DOCX explicitly excluded from that bundle.
8. `docs/stage4_manuscript_release_plan.md` and `docs/stage_overview.md`
   updated narrowly for Goal 016.
9. `docs/log/136_rsec_final_read_readiness.md`.
10. Goal 016 `Log.md` final execution checkpoint and closeout.

Generated reader files may be assembled under ignored
`build/final_read/goal016/`. They are validation/handoff artefacts, not tracked
publication objects.

## Permitted Mutation Boundary

Only the following tracked paths may change during execution.

### Direct manuscript and caption surfaces

- `manuscript/text/manuscript_draft.md`
  - named top-N disclosures where directly needed;
  - Layer B shuffle status;
  - modest Layer B compression;
  - internal-versus-public reproducibility wording;
  - known no-specific-funding text and visibly unresolved declaration
    placeholders only if required for Barry's complete read.
- `manuscript/text/figures.md`
  - Fig. 4 caption only.
- `manuscript/text/supplementary_tables.md`
  - Table S1 and Table S2 explanatory text only; no row/cell edits.
- `manuscript/text/supplementary_figures.md`
  - Fig. S2 and Fig. S3 captions only.

### RSEC final-read surfaces

- `manuscript/submission/rsec/README.md`
- `manuscript/submission/rsec/submission_checklist.md`
- `manuscript/submission/rsec/submission_metadata.md`
- `manuscript/submission/rsec/submission_counts.md`
- `manuscript/submission/rsec/declarations_draft.md`
- `manuscript/submission/rsec/cover_letter_draft.md`
- `manuscript/submission/rsec/supplementary_frontmatter.md`, only if needed to
  preserve visible unresolved human fields in the final-read bundle
- `manuscript/submission/rsec/final_read_guide.md`
- `manuscript/submission/rsec/code_release_decision.md`
- `manuscript/submission/rsec/figure_production_inventory.md`

Do not treat the `manuscript/submission/rsec/` directory as authority to
change `submission_authors.yaml`, `supplementary_table_end.md`, or any other
file without a direct Goal 016 need. Unconfirmed author metadata must remain
unconfirmed.

### Governance and goal records

- `docs/stage4_manuscript_release_plan.md`
- `docs/stage_overview.md`
- `docs/log/136_rsec_final_read_readiness.md`
- `docs/goals/016-rsec-final-read-readiness/Goal.md`
- `docs/goals/016-rsec-final-read-readiness/Plan.md`
- `docs/goals/016-rsec-final-read-readiness/Runbook.md`
- `docs/goals/016-rsec-final-read-readiness/Log.md`

### Generated local artefacts

- Existing profile outputs under ignored `build/`, regenerated only through
  the established Makedoc commands.
- `build/final_read/goal016/`, created only for the four-file reader bundle.

No build outputs are tracked at the packet baseline. Do not add ignored build
products to Git. If a later checkout contains a tracked generated manuscript
deliverable, stop and obtain orchestrator confirmation before changing it.

Every other path is prohibited, including:

- `src/`, `tests/`, `data/`, `analysis/`, `settings/`, `references/`,
  `artefacts/`, and `.github/`;
- figures and other generated scientific artefacts;
- model, environment, lock, configuration, and build-tool files;
- Goal 014/015 historical records;
- release manifests and the published Zenodo Dataset.

## Public And External-Action Block

Goal 016 does not authorize:

- Wiley or Research Exchange login, draft creation, upload, or submission;
- editor contact or a pre-submission inquiry;
- public code, software, Layer B data, or additional archive publication;
- creating a public repository or changing `dsipa-dev` visibility;
- a Zenodo Software record;
- Git tag or GitHub release;
- fee/APC acceptance, payment, waiver request, or coverage commitment;
- journal open-access or copyright licence selection;
- all-author, sole-submission, or final publication approval;
- any public URL claim for the private source repository.

The preferred later route is a curated clean-history public code repository
plus a separate Zenodo Software record. Goal 016 may document the route and
its open questions, but only a later Barry-authorized goal may execute it.

## Acceptance Criteria

- The exact four-file Goal 016 packet is accepted before execution begins.
- Baseline and inherited changes are fully explained before mutation.
- Only permitted paths change.
- No data, model, table cell, figure pixel, numerical result, title, period,
  DOI, or screening category changes.
- Table S1 names all three top-20 selection/order metrics and remains
  explicitly non-ranking.
- Fig. S2 states top 20 by bootstrap-median inside slope.
- Fig. S3 states top 15 for pairwise bootstrap ordering frequencies.
- Both shuffle benchmarks are consistently described as one deterministic
  seeded realisation each, illustrative rather than a null distribution.
- Layer B compression is modest and preserves Fig. 4 and every material
  inferential limitation.
- Reproducibility language consistently distinguishes internal engineering
  quality from public reproducibility.
- The public DOI remains exact and is never described as a software record.
- `final_read_guide.md`, `code_release_decision.md`, and
  `figure_production_inventory.md` are decision-ready and evidence-based.
- The funding draft states no specific funding; all other human claims remain
  visibly unresolved.
- The component count table records abstract, main body including Data
  accessibility, conservative abstract-plus-body, acknowledgements,
  references, tables, figure legends, and keywords, with methods documented.
- The conservative current count used for readiness remains at or below
  `5,000`; uncertainty about the journal's treatment of declarations is
  stated, not hidden.
- The four-file reader bundle contains main PDF, main DOCX, authoritative SI
  PDF, and final-read guide, and excludes the SI DOCX.
- Focused tests, the established full `make test` gate, all three profile
  checks/builds, citation/lint/count checks, exact content scans,
  `git diff --check`, and fresh provenance/text/visual QA pass.
- One focused repair pass is used at most, unless a material defect remains
  and the orchestrator explicitly reopens work.
- Goal and chronology records separate observed facts, inference, Barry
  decisions, validation, and residual gates.
- Orchestrator acceptance precedes exact-path staging, commit, fetch, and
  push.
- No external/public action occurs.
- Handoff stops at the 80/20 final-read bundle rather than polishing optional
  submission-form or production details.

## Stop Conditions

Stop and report exact evidence if:

- baseline, upstream, or worktree state is unexplained;
- a required correction conflicts with the existing table rows, figures, or
  accepted reports;
- a text edit requires new analysis, code, tests, data, model, or figure
  generation;
- any frozen number, title, date range, DOI, category, or scientific
  conclusion would change;
- the conservative count exceeds `5,000` after modest Layer B compression;
- a human claim cannot remain visibly unresolved without making the bundle
  misleading;
- AI-use history or the code-release implication is treated as known when
  Barry has not confirmed it;
- a public code or Layer B package appears necessary for submission readiness;
- official/current policy evidence conflicts or the live workflow is needed
  to settle a requirement;
- validation still has a material failure after one focused repair;
- exact-path Git closeout would absorb an unrelated change; or
- further work would mainly polish optional submission or production detail.

## Non-Goals

No new science, model fitting, simulation, sensitivity analysis, figure or
table regeneration, data processing, data acquisition, raw or row-level ALA
redistribution, source-code change, test change, configuration change,
bibliography expansion, title change, journal submission, public release,
repository visibility change, tag, GitHub release, DOI creation, fee/APC
action, open-access agreement, or journal licence choice is part of Goal 016.

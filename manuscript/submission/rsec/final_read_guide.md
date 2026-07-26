# DSIPA RSEC Final-Read Guide

Status: decision-ready for Barry's full read, but not submission-ready or
authorized for Wiley.

## Bundle

Read these four files in `build/final_read/goal016/`:

1. `dsipa_rsec_final_read_main.pdf`
2. `dsipa_rsec_final_read_main.docx`
3. `dsipa_rsec_final_read_supporting_information.pdf`
4. `final_read_guide.md`

The PDF is the primary reading copy of the main manuscript. Use the DOCX for
comments or tracked revisions. Read the Supporting Information after the main
manuscript, then return to the checklist below. The diagnostic SI DOCX is not
part of the bundle.

## Fixed Science

- Title: **Detectable change in dark-sky integrity across Australia’s
  protected areas**
- Study period: `2013-2024`
- Public Layer A Dataset DOI: <https://doi.org/10.5281/zenodo.21524637>
- Layer A remains the primary contribution.
- Layer B remains a secondary, provider-bounded, presence-only, case-control,
  weakly discriminating, non-causal stress test.
- Screening categories support investigation; they are not a competitive
  management ranking.
- No data, model, numerical result, table cell, figure, or DOI changed in Goal
  016.

## Goal 016 Changes

- Table S1 now states that it shows the top 20 rows in each category and names
  the exact point-estimate ordering metric for each.
- Fig. S2 identifies the top 20 protected areas by bootstrap-median inside
  slope; Fig. S3 identifies the top 15 used for pairwise bootstrap ordering.
- Each Layer B shuffle is disclosed as one deterministic seeded realisation
  used illustratively, not a sampled null distribution or causal
  counterfactual.
- Repeated Layer B caveats were compressed without changing the design,
  results, Fig. 4, or inferential limits.
- Reproducibility wording now separates the internally versioned, scripted,
  tested, pinned, and manifest-backed pipeline from what is public.

## Known Residual Before Submission

Fig. 4's internal plotted title still reads `Layer B ALAN effects
(provider-matched primary + falsification)`. This legacy semantic label remains
visible in the frozen final-read pixels; the caption and manuscript
interpretation control here, and the two shuffles are single illustrative
benchmarks, not a falsification design. The title must be replaced
reproducibly before submission, after the preserved Layer B snapshot or an
independently verified summary-only rendering path is available. Do not repair
the label by editing pixels.

## Public-Reproducibility Decision

The DOI above is a Dataset containing nine processed Layer A outputs, not a
software record. `dsipa-dev`, the complete runnable environment, derived
Layer B materials, and the full Layer B reproduction route remain private.
Before submission, Barry should decide between the preferred later route of a
curated clean-history public code repository plus a separate Zenodo Software
record, or retaining private code and requesting editorial guidance. See
`manuscript/submission/rsec/code_release_decision.md`.

## Barry Return Checklist

Please return:

- `[BARRY CONFIRM: final author list and order]`
- `[BARRY CONFIRM: affiliations and ORCIDs]`
- `[BARRY CONFIRM: responsible corresponding author, institutional email, and full address]`
- `[BARRY CONFIRM: author contributions]`
- `[BARRY CONFIRM: acknowledgements]`
- `[BARRY CONFIRM: conflicts of interest]`
- `[BARRY CONFIRM: ethics/consent applicability and exact statement]`
- `[BARRY CONFIRM: exact AI-use disclosure by tool, version, role, purpose, and access date]`
- `[PRE-SUBMISSION DECISION: public code/Layer B route]`
- `[BARRY CONFIRM immediately before submission: all-author approval and sole submission]`
- comments on the main manuscript and SI;
- approval or revision of the proposed running title and cover-letter novelty
  statement; and
- any cover-image preference, which remains optional.

Known funding draft: **No specific funding.**

Reading or approving this bundle does not authorize Wiley login, upload,
submission, a fee or licence decision, public code/data release, repository
visibility change, or any other external action.

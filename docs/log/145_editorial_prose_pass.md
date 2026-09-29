# 145 — Editorial prose pass on the main text (28 September 2026)

Barry asked Fable for a light editorial pass on the main manuscript and figure
captions: better balance of sentence lengths, fewer one-point paragraphs, brief
explanatory prose for a general ecology and conservation readership, and no
generic AI-style phrasing. Content, structure and claims were to stay as they are.

## What changed

- `manuscript/text/manuscript_draft.md`: every section except the declarations
  was line-edited. Over-clipped runs of short sentences were joined where the
  link expresses cause, contrast or consequence; one- and two-point paragraphs
  were merged (3.3 counts with the named examples; 4.1 contribution with prior
  work). Section 3.2 now cites Fig. S2/Table S1 before Fig. S3/Table S2.
- Brief explanations added for non-specialists: VIIRS day/night band and how
  annual composites are built (citing Elvidge et al. 2021), skyglow, centre-based
  cell selection, what a Theil–Sen slope is, why the 1–5 km band test is informative,
  the first-positive fraction, moving-block resampling and IBRA. Acronyms VIIRS,
  DNB, VNL, IBRA and LED are now expanded at first use. "Layer A" was removed
  from Data accessibility because the main text no longer defines it.
- `manuscript/text/figures.md`: the four main captions were rewritten for flow;
  the Fig. 3 caption explains the inverse-hyperbolic-sine display.
- `manuscript/text/tables.md`: numeric ranges in two Table 1 row labels now use
  en dashes, matching the text. Ranges throughout use en dashes; "Theil–Sen"
  uses an en dash, matching the Supporting Information.

## Verification

Every number, citation key and figure/table/Supporting Methods cross-reference
in the 19 September text is present in the revision. Deliberate differences: the
tercile cutoff is written 0.04 in both places (was 0.040 and 0.04); the new VIIRS
sentence adds 2012, 750 m and one further Elvidge et al. (2021) citation; 2.1
names the 2022 source boundary; 3.2 names the 2020–2024 pixel support used for
transitions, as described in Supporting Methods S2. No claim was strengthened.

Source count: 279 abstract + 4,395 body/declarations = 4,674 words (was 4,171);
within the 300-word abstract and 5,000-word readiness gates. The
`submission_counts.md`, `submission_metadata.md` and checklist figures are now
stale and need the pre-submission recount they already anticipate.
`make ms-check PROFILE=submission` and `make ms-build PROFILE=submission` passed
(lint, reference audit, 38 makedoc tests); the main PDF is 23 pages (was 21).
The submission-contract and makedoc-provenance tests pass (11).

## Outputs

- `build/submission/dsipa_rsec_main.{pdf,docx}` rebuilt from the edited sources.
- `build/final_read/editorial_20260928/`: copies of that PDF and DOCX, plus
  `editorial_redline_20260928.html`, a word-level redline against 19 September.

Supporting Information text is unchanged, and the sealed
`build/final_read/spatial_20260919/` bundle is untouched. No commit, push,
deposit or submission at that point. On 29 September, at Barry's request, this pass
and the other September work were committed in six tranches and pushed.

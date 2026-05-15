# Log 113 - Manuscript discussion handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/discussion.md` into `manuscript/text/manuscript_draft.md`.
- Replaced the scaffold Discussion outline with the supplied full Discussion and Conclusions subsections.
- Kept hard-coded author-year citations as plain text for the later BetterBibTeX/CSL conversion pass.
- Normalized draft punctuation, dashes, operator symbols, and quote marks for Markdown/TeX compatibility while preserving accented author names in citation text.
- Corrected the falsification-logic sentence so an effect that survives shuffled-ALAN nulls is described as less credible, consistent with the Results interpretation.

Checks:
- `pandoc manuscript/text/manuscript_draft.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_draft_smoke.tex`
- `git diff --check`

Notes:
- Existing Limitations and Data/code availability scaffolds still need a later integration or cleanup pass.

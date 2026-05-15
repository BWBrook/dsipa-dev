# Log 110 - Manuscript introduction handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/introduction.md` into `manuscript/text/manuscript_draft.md`.
- Replaced the placeholder Introduction with the supplied draft material.
- Kept hard-coded author-year citations as plain text for the later BetterBibTeX/CSL conversion pass.
- Normalized draft punctuation in the inserted section for Markdown/TeX friendliness while preserving accented author names in citation text.

Checks:
- `pandoc manuscript/text/manuscript_draft.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_draft_smoke.tex`
- `git diff --check`

Notes:
- Existing methods/results scaffold below the Introduction still contains non-ASCII punctuation from earlier skeleton material; leave that for the broader cleanup pass after all draft chunks are integrated.

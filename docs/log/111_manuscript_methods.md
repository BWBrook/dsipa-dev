# Log 111 - Manuscript methods handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/methods.md` into `manuscript/text/manuscript_draft.md`.
- Replaced the scaffold Methods section with the supplied detailed draft.
- Kept hard-coded author-year citations as plain text for the later BetterBibTeX/CSL conversion pass.
- Converted metric lists, buffer definitions, and falsification checks into stable Markdown bullets.
- Normalized draft punctuation and operators in the inserted section for Markdown/TeX compatibility while preserving accented author names in citation text.

Checks:
- `pandoc manuscript/text/manuscript_draft.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_draft_smoke.tex`
- `git diff --check`

Notes:
- Existing Results, Discussion, and Limitations scaffolds still contain non-ASCII punctuation and should be cleaned after the remaining draft chunks are integrated.

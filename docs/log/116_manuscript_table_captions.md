# Log 116 - Manuscript table captions handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/table_captions.md` as `manuscript/text/tables.md`.
- Created a separate table source file for `makedoc`-style multi-source manuscript assembly.
- Preserved Table 1 as an explicit placeholder rather than inventing a completed table.
- Normalized punctuation and inequality symbols for Markdown/TeX compatibility.

Checks:
- `pandoc manuscript/text/tables.md --from markdown --to latex -o /tmp/dsipa_tables_smoke.tex`
- `pandoc manuscript/text/manuscript_draft.md manuscript/text/tables.md manuscript/text/figures.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_tables_figures_smoke.tex`
- `git diff --check`

Notes:
- The actual Table 1 values should be filled during the later table/results pass.

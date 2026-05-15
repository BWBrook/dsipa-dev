# Log 118 - Manuscript supplementary table captions handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/supplementary_table_captions.md` as `manuscript/text/supplementary_tables.md`.
- Created a separate supplementary table source file for later `makedoc` assembly.
- Preserved Table S1 and Table S2 as explicit placeholders rather than inventing completed table values.
- Normalized punctuation, inequality signs, multiplication symbols, plus/minus notation, and area units for Markdown/TeX compatibility.

Checks:
- `pandoc manuscript/text/supplementary_tables.md --from markdown --to latex -o /tmp/dsipa_supplementary_tables_smoke.tex`
- `pandoc manuscript/text/manuscript_draft.md manuscript/text/tables.md manuscript/text/supplementary_tables.md manuscript/text/figures.md manuscript/text/supplementary_figures.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_all_sources_smoke.tex`
- `git diff --check`

Notes:
- Actual supplementary table values should be filled during the later table/results pass.

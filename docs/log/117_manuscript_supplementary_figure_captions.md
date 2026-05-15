# Log 117 - Manuscript supplementary figure captions handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/supplementary_figure_captions.md` as `manuscript/text/supplementary_figures.md`.
- Created a separate supplementary figure-caption source file for later `makedoc` assembly.
- Converted six supplementary captions into renderable Markdown image blocks with stable `#fig-...-s<number>` identifiers.
- Used source-relative image paths from `manuscript/text/supplementary_figures.md` to `../figures/*.png`.
- Normalized punctuation, inequalities, date ranges, and multiplication symbols for Markdown/TeX compatibility.

Checks:
- `pandoc manuscript/text/supplementary_figures.md --from markdown --to latex -o /tmp/dsipa_supplementary_figures_smoke.tex`
- `pandoc manuscript/text/manuscript_draft.md manuscript/text/tables.md manuscript/text/figures.md manuscript/text/supplementary_figures.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_all_sources_smoke.tex`
- Verified every referenced image path exists relative to `manuscript/text/supplementary_figures.md`.
- `git diff --check`

Notes:
- Captions omit explicit "Supplementary Figure S1." prefixes so `makedoc` can assign supplementary labels without duplicate numbering.

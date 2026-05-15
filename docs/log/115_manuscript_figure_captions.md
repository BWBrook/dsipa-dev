# Log 115 - Manuscript figure captions handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/figure_captions.md` as `manuscript/text/figures.md`.
- Created a separate figure-caption source file following the `makedoc` split-source expectation.
- Converted the five main figure captions into renderable Markdown image blocks with stable `#fig-...` identifiers.
- Used source-relative image paths from `manuscript/text/figures.md` to `../figures/*.png`.
- Normalized punctuation, inequalities, date ranges, and multiplication symbols for Markdown/TeX compatibility.

Checks:
- `pandoc manuscript/text/figures.md --from markdown --to latex -o /tmp/dsipa_figures_smoke.tex`
- Verified every referenced image path exists relative to `manuscript/text/figures.md`.
- `git diff --check`

Notes:
- Captions omit explicit "Figure 1." prefixes so `makedoc` can assign ordered figure labels without duplicate numbering.
- Full `makedoc` validation still awaits `settings/build.yaml`, bibliography, CSL, and author metadata scaffolding.

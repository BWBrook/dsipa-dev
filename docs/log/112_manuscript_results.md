# Log 112 - Manuscript results handoff

Date: 2026-05-15

Summary:
- Integrated `/mnt/c/input/results.md` into `manuscript/text/manuscript_draft.md`.
- Replaced the scaffold Results section with the supplied detailed draft.
- Kept figure references as plain `Fig.` / `Supplementary Fig.` labels for the later figure/caption pass.
- Normalized draft punctuation, inequality signs, date ranges, and operator symbols for Markdown/TeX compatibility.
- Sanity-checked core counts and metrics against the current reports, including Layer A trend counts, retention quadrants, Layer B exposure summaries, provider matching, and model/falsification metrics.

Checks:
- `pandoc manuscript/text/manuscript_draft.md --from markdown+yaml_metadata_block+tex_math_dollars+tex_math_single_backslash --to latex -o /tmp/dsipa_manuscript_draft_smoke.tex`
- `git diff --check`

Notes:
- The baseline zero-mass statement uses the baseline figure value (~86.9%, reported as approximately 87%); the Layer A sanity dashboard also reports a broader all-inside-row floor summary of 0.895.
- Existing Discussion and Limitations scaffolds still contain non-ASCII punctuation and should be cleaned after the remaining draft chunks are integrated.

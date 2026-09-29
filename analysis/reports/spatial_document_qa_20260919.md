# Final corrected reading documents: QA, 19 September 2026

**PASS for private reading.** Main PDF: 21 pages; SI PDF: 14 pages.
LibreOffice conversions of the editable documents: main 27 pages; SI 17 pages.
These are reading artefacts with visible author-declaration placeholders, not
an authorised journal submission.

Both makedoc profile checks and builds passed, with zero unknown citation keys.
All four PDF surfaces passed qpdf structural checks. A visual-QA agent inspected
all pages of the main/SI PDFs and Word conversions. The parent independently
inspected the main PDF, main Word conversion and all SI Word pages; the acceptance
reviewer separately checked the corrected SI PDF. No clipping, overlap or missing
figure/table content remains in the inspected surfaces.

The final checks specifically confirmed:

- Table 1 uses 4,253 paired comparisons and the provisional coastline caveat.
- Figure 4 labels Henderson Q1 with its corrected positive surrounding trend.
- Figure S1 now shows the corrected complete-band cohort of 369, matching its
  caption. The old 383-reserve canonical image had survived a duplicated output
  path; the renderer path and canonical asset are corrected.
- Table S1 retains dagger flags; its explanation now sits in the introductory
  paragraph. The PDF no longer has a nearly blank note-continuation page.
- Table S5 has two rendered table panels, not literal Markdown pipes.
- The main Word Table 1 note uses 1.5 line spacing, retaining it with the table
  on page 18. This removed a two-line continuation page; the parent inspected
  the final full-size page and rechecked the 27-page PDF structure.
- Main Figures 1–4 and SI Figures S1–S3 are visible with correct labels. Main
  text remains double spaced; compact table cells and the main table note are
  explicit layout exceptions. Small SI tables remain readable at full page size.

Contact sheets and page renders are under
`build/qa/spatial_20260919/final_contacts/`; the original Word-main contact sheets
show the pre-spacing 28-page layout. The final Table 1 page is
`word_main_table_final.png`; the final conversion is under `final_docx_pdf/`.
Both Word-SI and the main/SI PDF contact sheets show the final layouts.
LibreOffice emitted a generic “Unknown IO error” line while exporting, but
produced complete, parseable PDFs that passed the structural and visual checks.

The final four document hashes are recorded in
`spatial_private_package_validation.json` and the reading bundle's manifest.

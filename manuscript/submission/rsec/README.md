# RSEC private reading package

The active version is the 19 September 2026 corrected Layer A candidate for private
reading: **Satellite screening of lighting change across Australia's
protected areas**, Original Research for *Remote Sensing in Ecology and
Conservation*. See `final_read_guide.md` for changes and review questions.

## Builds

`settings/build.yaml` is the profile source. `make ms-build PROFILE=submission`
builds the main PDF/DOCX; `make ms-build PROFILE=supplementary` builds the SI.
The local makedoc checkout defaults to `$HOME/work/makedoc` and can be
selected with `MAKEDOC_ROOT`. Build profiles sequentially.

The current candidate contains four main figures, one main table, three
supporting figures and five supporting tables. Final PDF/DOCX render QA passed. The public Zenodo dataset is the historical baseline; corrected
spatial outputs are private and Layer B research data remain omitted.

## Evidence and assets

- `final_read_guide.md`: reading order and scientific review questions.
- `submission_counts.md`: current component counts.
- `figure_production_inventory.md`: active figures and generation route.
- `submission_metadata.md`, `submission_authors.yaml` and
  `declarations_draft.md`: unresolved human metadata.
- `cover_letter_draft.md`: updated RSEC framing, for later author approval.
- `code_release_decision.md`: unresolved public-code route.
- `docs/log/142_scientific_review_closeout.md`: implementation and validation.

Author approval, public source release, submission, fees and licensing are
outside this private-circulation task. No public deposit has been changed.

## Journal guidance

The official [RSEC author guidelines](https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/author-guidelines)
were checked on 12 September 2026. Original Research has a 5,000-word maximum
excluding acknowledgements, references and figure/table legends. We also
report a conservative count including abstract and current declaration text.
The portal was not accessed.

# RSEC Submission Counts

Generated from the Goal 016 final-read manuscript source and rendered
submission PDF on 2026-07-26.

## Results

| Surface | Count | Requirement |
| --- | ---: | --- |
| Abstract | 234 words | <= 300 |
| IMRAD main text | 4,565 words | <= 5,000 |
| Data accessibility content | 81 source words | component report |
| IMRAD plus Data accessibility | 4,649 words | <= 5,000 under the more conservative inclusion |
| Declaration content excluding acknowledgements | 34 source words | provisional human fields; treatment by live workflow remains unconfirmed |
| Acknowledgements | 3 source words | placeholder only; normally excluded |
| Conservative abstract plus body, Data accessibility, and all declaration/acknowledgement markers | 4,947 words | <= 5,000 readiness gate |
| Rendered references | 454 words | excluded; PDF text boundary documented below |
| Main table source | 551 words | excluded legend/table surface |
| Supporting table source | 2,316 words | separate SI surface |
| Main figure-legend source | 498 words | excluded legend surface |
| Supporting figure-legend source | 406 words | separate SI surface |
| Keywords | 5 | 4-6 |
| Main figures | 4 | report count |
| Main tables | 1 | report count |
| Supporting figures | 7 | report count |
| Supporting tables | 2 | report count |
| Proposed running title | 34 characters | <= 45 |

The conservative 4,947-word readiness count deliberately includes every
current declaration and acknowledgement marker because the live workflow's
treatment of declarations has not been confirmed. Final human text must be
recounted. References, tables, and figure legends are reported separately and
are excluded from the main-text count under the current RSEC evidence.

## Reproducible Commands

```bash
awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## 1\. Introduction/{on=1}/^## Data accessibility/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## 1\. Introduction/{on=1}on' \
  manuscript/text/manuscript_draft.md | wc -w

abstract_words="$(
  awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
    manuscript/text/manuscript_draft.md | wc -w | tr -d ' '
)"

body_words="$(
  awk '/^## 1\. Introduction/{on=1}on' \
    manuscript/text/manuscript_draft.md | wc -w | tr -d ' '
)"

test "$((abstract_words + body_words))" -le 5000
printf '%s\n' "$((abstract_words + body_words))"

awk '/^## Keywords/{on=1;next}/^---/{on=0}on' \
  manuscript/text/manuscript_draft.md |
  tr ';' '\n' | sed '/^[[:space:]]*$/d' | wc -l

rg -c '!\[' manuscript/text/figures.md
rg -c '^\*\*Table [0-9]+\.' manuscript/text/tables.md
rg -c '!\[' manuscript/text/supplementary_figures.md
rg -c '^\*\*Table S[0-9]+\.' manuscript/text/supplementary_tables.md
printf %s 'Dark-sky change in protected areas' | wc -m

awk '/^## Data accessibility/{on=1;next}/^## Declarations/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '
  /^## Declarations/{on=1;next}
  on && /^### Acknowledgements/{skip=1;next}
  on && /^### /{skip=0;next}
  on && !skip{print}
' manuscript/text/manuscript_draft.md | wc -w

awk '
  /^### Acknowledgements/{on=1;next}
  /^### /{if(on)on=0}
  on
' manuscript/text/manuscript_draft.md | wc -w

wc -w manuscript/text/tables.md
wc -w manuscript/text/supplementary_tables.md
wc -w manuscript/text/figures.md
wc -w manuscript/text/supplementary_figures.md
```

The whole-file table and figure commands are source-surface counts, not
rendered-prose counts. They include Markdown table cells or image-link markup
and are labelled accordingly.

The rendered-reference count was produced after the final submission build
from ignored `build/goal016_qa/main_pdf.txt`. The extraction begins after the
line ending `References` and stops before the line ending `Figure Captions`;
continuous line numbers and page-number-only lines are stripped before
`wc -w`:

```bash
awk '/References$/{on=1;next}/Figure Captions$/{on=0}on' \
  build/goal016_qa/main_pdf.txt |
  sed -E 's/^[[:space:][:cntrl:]]*[0-9]+[[:space:]]+//' |
  sed -E '/^[[:space:]]*[0-9]+[[:space:]]*$/d' |
  wc -w
```

The whole-manuscript `wc -w` result is not used as the RSEC main-text count.

Final author, funding, declaration, and correspondence text may change the
paper-component breakdown and must be recounted after Barry confirms those
fields.

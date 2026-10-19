# RSEC Submission Counts

Generated from the 19 October 2026 editorial revision of
`manuscript/text/manuscript_draft.md`.

## Results

| Surface | Count | Requirement |
| --- | ---: | --- |
| Abstract content | 259 source words | <= 300 |
| Body from Introduction heading through final declaration | 4,549 source words | source-token count including headings and current declarations |
| Abstract plus complete body | 4,808 source words | subtotal |
| Table 1 cells and headers | 170 source tokens | includes numerical entries; excludes Markdown separators |
| Conservative readiness total | 4,978 source tokens | <= 5,000 |
| Keywords | 5 | 4-6 |
| Main figures | 4 | report count |
| Main tables | 1 | report count |
| Supporting figures | 7 | current Layer A source count |
| Supporting tables | 8 | report count |
| Proposed running title | 39 characters | <= 45 |

The conservative 4,978-token readiness count combines 259 abstract
words, 4,549 body tokens and 170 Table 1 cell/header tokens. The body includes
Markdown headings, citation tokens and all current declarations and
acknowledgement markers. The count excludes title, keywords, references and
figure/table legends. This is a reproducible source-token count, not a
word-processor count. Final author text must be recounted.

The [current Wiley guidelines](https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/author-guidelines),
checked 19 October 2026, set 5,000 words for original research, excluding
acknowledgements, references and figure/table legends. Table-cell text is not
explicitly exempted, so it is included here. This supersedes the earlier
abstract-plus-body gate.

## Reproducible Commands

```bash
awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
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

table_words="$(python3 - <<'PYCOUNT'
from pathlib import Path
lines = Path('manuscript/text/tables.md').read_text().splitlines()
cells = ' '.join(line.replace('|', ' ') for line in lines
                 if line.startswith('|') and not line.startswith('| ---'))
print(len(cells.split()))
PYCOUNT
)"
test "$((abstract_words + body_words + table_words))" -le 5000
printf '%s\n' "$((abstract_words + body_words + table_words))"

awk '/^## Keywords/{on=1;next}/^## 1\. Introduction/{on=0}on' \
  manuscript/text/manuscript_draft.md |
  tr ';' '\n' | sed '/^[[:space:]]*$/d' | wc -l

rg -c '!\[' manuscript/text/figures.md
rg -c '^\*\*Table [0-9]+\.' manuscript/text/tables.md
rg -c '!\[' manuscript/text/supplementary_figures.md
rg -c '^\*\*Table S[0-9]+\.' manuscript/text/supplementary_tables.md
printf %s 'Satellite screening of reserve lighting' | wc -m

```

The first command counts abstract content only. The second counts the complete
body as one contiguous source range, including all headings and declarations.
The shell arithmetic adds the Table 1 cell/header tokens to those two counts. The whole-manuscript
`wc -w` result is not used because it would also include the title and
keywords.

Final author, funding, declaration, and correspondence text may change the
paper-component breakdown and must be recounted after Barry confirms those
fields.

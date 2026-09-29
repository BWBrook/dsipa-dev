# RSEC Submission Counts

Generated from the 19 September 2026 corrected Layer A candidate revision of
`manuscript/text/manuscript_draft.md`.

## Results

| Surface | Count | Requirement |
| --- | ---: | --- |
| Abstract content | 237 source words | <= 300 |
| Body from Introduction heading through final declaration | 3,931 source words | source-token count including headings and current declarations |
| Conservative abstract plus complete body | 4,168 source words | <= 5,000 readiness gate |
| Keywords | 5 | 4-6 |
| Main figures | 4 | report count |
| Main tables | 1 | report count |
| Supporting figures | 3 | current Layer A source count |
| Supporting tables | 5 | report count |
| Proposed running title | 39 characters | <= 45 |

The conservative 4,168-word readiness count uses whitespace-delimited source
tokens. It includes Markdown headings, citation tokens, and every current
declaration and acknowledgement marker. It excludes the title, keywords,
references, tables, and figure legends. This deliberately errs upward relative
to the journal's likely component exclusions, but it remains a source-token
count rather than a word-processor count. Final human declaration and
acknowledgement text must be recounted.

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

test "$((abstract_words + body_words))" -le 5000
printf '%s\n' "$((abstract_words + body_words))"

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
The shell arithmetic reports their conservative sum. The whole-manuscript
`wc -w` result is not used because it would also include the title and
keywords.

Final author, funding, declaration, and correspondence text may change the
paper-component breakdown and must be recounted after Barry confirms those
fields.

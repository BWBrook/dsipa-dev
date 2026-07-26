# RSEC Submission Counts

Generated from the current accepted manuscript source on 2026-07-26.

## Results

| Surface | Count | Requirement |
| --- | ---: | --- |
| Abstract | 235 words | <= 300 |
| IMRAD main text | 4,609 words | <= 5,000 |
| IMRAD plus Data accessibility | 4,685 words | <= 5,000 under the more conservative inclusion |
| Keywords | 5 | 4-6 |
| Main figures | 4 | report count |
| Main tables | 1 | report count |
| Supporting figures | 7 | report count |
| Supporting tables | 2 | report count |
| Proposed running title | 34 characters | <= 45 |

Acknowledgements currently present in the accepted main source: 0 words.
References and table/figure legends are excluded from the main-text counts,
consistent with the RSEC Original Research limit.

## Reproducible Commands

```bash
awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## 1\. Introduction/{on=1}/^## Data accessibility/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## 1\. Introduction/{on=1}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## Keywords/{on=1;next}/^---/{on=0}on' \
  manuscript/text/manuscript_draft.md |
  tr ';' '\n' | sed '/^[[:space:]]*$/d' | wc -l

rg -c '!\[' manuscript/text/figures.md
rg -c '^\*\*Table [0-9]+\.' manuscript/text/tables.md
rg -c '!\[' manuscript/text/supplementary_figures.md
rg -c '^\*\*Table S[0-9]+\.' manuscript/text/supplementary_tables.md
printf %s 'Dark-sky change in protected areas' | wc -m
```

The whole-file `wc -w` result is not used as the RSEC main-text count.

Final author, funding, declaration, and correspondence text may change the
paper-component breakdown and must be recounted after Barry confirms those
fields.

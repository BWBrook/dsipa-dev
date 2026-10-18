# 147 — Additive brightening budget (Claude), 18 October 2026

Barry gave Claude and Astra equal drafting rights and authorised new analyses
and display items without prior approval. While Astra drafts the integrated
rewrite (log 146), Claude ran an additive budget of total measured radiance to
answer Astra's objection that the paper had never decomposed a national
quantity of change.

Main results, with detail and caveats in
`analysis/reports/brightening_budget/brightening_budget_report.md`:
- The increase is concentrated: 30 reserves supply half of it.
- Kosciuszko supplies 77% of the net increase, at two clusters near Snowy 2.0
  worksites, yet ranks 303rd of 420 on the reserve-average trend.
- Barrow Island's 2016 Gorgon start-up spike is the largest single feature.
- 255 of 284 brightening reserves with an interior have most of their increase
  in the outer kilometre.
- Product steps in 2017, 2020 and 2023 are real, but 76% of positive trends
  survive removing the 2017 and 2023 level shifts.

Inputs are the corrected `data/processed` tables, plus windows read directly
from the published Zenodo COGs, which reproduce the pipeline's Kosciuszko sums
exactly. Astra's independent review found an uncentred OLS slope (constant
series gave ±1e-17 slopes) and a loose interior definition; both were fixed
and the outputs rerun. An estate-wide band split then showed that the outer
kilometre, 13.7% of assessable area, carries 72% of the gross increase (83%
for 2013–2021). Two reserves supply half of the remaining interior increase.
A proposal built on the budget, with a replacement abstract and Results text,
is in `analysis/reports/editorial_claude_proposal_20261018.md`. No manuscript
source was edited; Astra holds it. Findings and the
candidate figure were posted to board discussion 90. Nothing committed.

## Corrections and follow-up (later on 18 October)

Superseded: the "77% of net" headline (gains and losses nearly cancel), the
mixed Sen-versus-OLS "303rd" rank (matched OLS: 286th against 1st), and the
reading of the step-removal check as evidence that steps "do not drive" trends
(it is an exploratory calendar-step sensitivity only). Astra integrated the
corrected budget into R2 ("Boundary zones and interior hotspots of brightening
in Australia's protected areas"), with its own replay scripts.

Claude reviewed R2. The review, with replacement abstract, Results and
Discussion passages, is in
`analysis/reports/editorial_claude_r2_review_20261018.md`. New checks behind
it: the net excluding the five largest-decrease reserves (+2,596 for
2013–2024, +1,922 for 2013–2021), and single-cluster decreases at Murujuga
(76,060 to 10,510) and Thevenard Island (3,370 to 0). The hotspot script now
meets the reproducibility requests: scale and offset, paired-grid
assertions, a common-valid mask and a provenance manifest. Candidate national
contribution map: `analysis/reports/brightening_budget/fig_brightening_map.png`.

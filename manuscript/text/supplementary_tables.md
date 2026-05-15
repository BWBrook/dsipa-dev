## Supplementary Tables

**Table S1. Protected-area watchlists, category-safe.**

Placeholder supplementary table to be completed after the final table/results pass. Its purpose is to provide a management-facing deliverable while keeping the ranked lists category-safe and uncertainty-aware.

The table should contain three short ranked lists, with the top 20 protected areas in each category:

- inside brightening, defined as inside slope > 0, reporting slope, confidence interval, and P(slope > 0);
- external pressure, defined as buffer slope > 0 while inside slope <= 0; and
- internalisation/retention, defined using inside slope - buffer slope, with the sign interpreted explicitly.

Suggested columns are PA name, PA_ID, state/territory, dominant IBRA, area (km2), inside slope, buffer slope, retention index, bootstrap confidence interval, and bootstrap probability.

This table should stay out of the main narrative, but it is likely to be valuable for practitioners.

**Table S2. Layer B model summary and falsification outcomes.**

Placeholder supplementary table to be completed after the final table/results pass. Its purpose is to give numeric anchors for Fig. 5.

Suggested rows are the primary provider-matched model, the block-shuffle falsification, the IBRA x year shuffle falsification, and the multi-provider sensitivity model.

Suggested columns are N per class, `any_light` coefficient (mean +/- fold SD), intensity coefficient (mean +/- fold SD), AUC, and log loss.

This table should make the Layer B interpretation visible at a glance: weak signal plus falsification collapse.

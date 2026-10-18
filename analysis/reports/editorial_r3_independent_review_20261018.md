# Independent editorial and specialist review of R3

Reviewed 18 October 2026, 20:14 AEDT (Australia/Hobart).

**Recommendation: APPROVE WITH CHANGES. The scientific argument is ready; make the small wording repairs below and resolve the map collision before freezing the reading bundle. No new analysis or re-estimation is requested.** This is an editorial/scientific reading recommendation, not a release or submission approval.

## Scope and evidence

Read the active main manuscript, main-figure captions, Supporting Methods S4–S5, Tables S6–S7, the brightening-budget JSON audit, the decrease audit and the R3 primary-source audit. Compared the main text with the frozen R2 source and inspected the current national-map PNG. Sources were read at approximately 20:09–20:13 AEDT; the parent is concurrently editing them. Line references below refer to that reading snapshot.

Verification was confined to reading the accepted audit results, checking claims and denominators against them, inspecting the R2–R3 diff, reading the map encoding, and viewing the map. Accepted analyses were not rerun. Facility/source facts were checked against the supplied primary-source audit, not independently re-browsed. No manuscript or figure files were changed by this reviewer.

## Desk-editor assessment

R3 makes the paper's contribution clearer. The argument is now about the information lost when an estate is reduced to reserve classes or one net trend: most positive band-level change lies near boundaries, interior increases concentrate in a few reserves, and even fewer reserves dominate decreases. The national map and named decrease histories make the cancellation tangible. The supported-interior result (51.2% of positive contributions in 12.5% of sampled area) supplies a useful response to the obvious geometry objection without pretending that the national 72% is a common within-reserve edge effect.

The contribution is a spatial and temporal account of a satellite product, with targets for source investigation. It is not evidence of protection effectiveness, biological response, or physical light penetration. The Introduction and Discussion now state that contribution clearly, and the industrial cases strengthen it without needing a common cause for every large decrease. Retain the present directness; further generic caveats would dilute the paper without improving validity.

## Ranked findings and repairs

### MINOR — Define the abstract's summed quantity before giving its share

**Evidence:** main abstract, line 5; Methods lines 55–57; Supporting Methods lines 125–129. The phrase “72% of the summed positive boundary and interior trends” is technically aligned with the audit, but difficult on first reading. It leaves an abstract-only reader to infer that the slopes concern area-integrated totals, are fitted separately to two zones per reserve, and are clipped by sign before summation. It could also be read as a percentage of trend counts.

**Suggested paired replacement**, keeping the coverage sentence between these two sentences:

> Using annual VIIRS-derived observations for 2013–2024, we estimated trends in area-integrated radiance separately for the outermost kilometre and deeper interior of each reserve in Australia's 2024 protected estate.

> The outermost kilometre held 14% of sampled area but contributed 72% of the aggregate increase, calculated by summing positive slopes across both zones; its share was 83% for 2013–2021.

“Aggregate increase” is defined immediately here; the Methods can retain the formal reserve-level versus band-level denominator distinction. Do not replace the abstract statistic with a percentage of brightening reserves or a net-change share.

### MINOR — Narrow the inference from the pre-2022 rise

**Evidence:** Discussion line 119 currently says the pre-2022 growth is “strengthening this interpretation”, followed by “Shared product versions”. The primary-source audit explicitly distinguishes the documented 2022 source boundary from unexcluded annual processing effects, and establishes only partial lineage for the earlier product. The rest of this paragraph is appropriately calibrated. The phrase about shared versions adds ambiguity without adding evidence.

**Replace those two sentences with:**

> A rise was already evident in 2021, before the documented 2022 source change. That change alone cannot explain the earlier observation, although timing and spatial concentration do not exclude other processing effects.

The preceding construction-area correspondence already establishes why that explanation is worth investigating. The repair preserves that case while stating exactly what the timing test resolves. No added caveat paragraph or independent-product analysis is required for this revision.

### MINOR — State the interior concentration threshold accurately

**Evidence:** the abstract and Results line 85 say that two reserves supplied “half”; the audit's top two interior shares are 47.1319% and 10.0004%, totalling **57.1323%**. Supporting Methods/Table S6 correctly describe the count required to reach at least 50%, and Discussion line 107 already says “more than half”.

**Repair:** use “two reserves supplied more than half” in the abstract and “Two reserves accounted for more than half” in Results. This is a short consistency repair, not a change to the accepted statistic. Seven reserves supply approximately 80%, so that wording can remain.

### MINOR — National-map annotation collision needs fixing before freeze

**Evidence:** `manuscript/figures/fig_editorial_map.png`, inspected at 20:12 AEDT. The Christmas Island inset obscures most of the Barrow Island label, leaving only “Island”; its coordinate/slope annotation overlaps the latitude-label/Barrow region. The lower-left sign legend also touches the 115°E tick.

**Repair:** move the inset or the Barrow annotation, place the inset detail wholly within its own margin, and separate the bottom legend from axis ticks. The map's scientific encoding and caption agree: marker area uses a disclosed square-root transformation and a visibility floor, with a common scale for both signs. Retain those disclosures. Reinspect the regenerated PNG/PDF at manuscript reading size; there is no need to change the underlying mapped values.

## Material checks that passed

- **Budget denominators and support:** 72.00% uses positive zone slopes; 51.22% uses the 1,398-reserve supported-interior cohort; reserve-level concentration uses positive whole-reserve slopes. The text distinguishes all three from endpoint positive pixel differences and from the earlier matched Sen-slope cohort. Sampled area, polygon area and overlapping designations are explicitly separated.
- **Period and estimator:** main text and SI retain 2013–2024 OLS budgets, 2013–2021 sensitivity, late-minus-early differences, and selected site endpoints as distinct calculations. The matched mean/integrated rankings use OLS for both, so the ranking contrast is not attributed to weighting while silently changing estimator.
- **Negative contributions:** five reserves account for 94.91% of gross full-period decrease; Barrow and Murujuga together account for 89.9956%. Full-period net +478.95 and earlier-period net −537.84 match the audit. Holding the same five exclusions fixed gives +2,595.95 and +1,921.74. Methods, Discussion and Table S7 correctly label this as an influence diagnostic, not a corrected national estimate or independent evidence of general brightening.
- **Site histories:** Barrow is “nearly tripled”, with its 99.9% share explicitly assigned to positive 2015–2016 differences; Murujuga's 86.2% endpoint decrease and 96.2% negative-difference cluster share are separated; Thevenard's 2018–2019 return to positive values is retained. The three industrial examples are not presented as the three largest decreases or as an explanation for all five.
- **Source attribution:** “near” is appropriate to the supplied reference-point distances. The main text does not claim exact facility/pixel coincidence. The 2025 Woodside statistic is confined to SI and explicitly outside the study period. The national-guideline sentence preserves the listed-species, important-habitat and species-specific qualifications.
- **Scientific message:** the opening Discussion, management paragraph and final paragraph retain a useful conservation-monitoring purpose without converting satellite signals into exposure or biological effect.

No BLOCKER or MAJOR finding was identified within this bounded review. Existing public-data and author-declaration placeholders remain outside its scope; this recommendation does not supersede those separate release tasks.

## Addendum: concrete AI disclosure

Reviewed 18 October 2026, 20:15 AEDT. The parent's proposed replacement of the generic AI-use placeholder with verified roles is supported. Commit `2a7982c9786b3575af00d0ff53f7f72e74793961` names Claude Opus 5.5; log 143 identifies GPT-6-astra as the independent reviewer and says that it did not rerun production extraction or models. The current Codex agent identifies as GPT-6. Assign the independent-review role explicitly to GPT-6-astra; do not imply that each named system performed every production task.

Suggested text:

> The September–October 2026 revision used Codex (OpenAI GPT-6) and Claude (Anthropic Claude Opus 5.5) for analysis design, code generation, source retrieval, audit replays, figures, and manuscript drafting and critique. An independent review used OpenAI GPT-6-astra. Barry W. Brook provided scientific direction and critical review. [Earlier-pipeline model/version inventory to be completed; final author approval pending.]

This records known contributions without implying human coding, a complete historical model inventory, or completed final approval. Recount the manuscript against the agreed word limit after integration; that final count is owned by the parent.

## Closure check — 18 October 2026, 20:17 AEDT

**Updated recommendation: APPROVE within this bounded editorial/scientific review. All four findings are closed.** Rechecked only the changed abstract, interior-concentration sentence, Kosciuszko Discussion passage, AI disclosure, and final national-map PNG, as requested. No full rereview or analysis rerun was performed.

| Finding | Disposition | Evidence in the revised source/figure |
| --- | --- | --- |
| Abstract denominator | Closed | The method sentence establishes separate area-integrated boundary/interior trends; the 72% sentence defines summation of positive slopes across both zones. |
| Pre-2022 inference | Closed | The text states the earlier rise and the limited inference concerning the documented 2022 change, while retaining unresolved processing effects. |
| Interior concentration threshold | Closed | Abstract and Results now say “more than half”. |
| National-map collisions | Closed | Barrow Island is fully visible, the Christmas Island inset/detail has clear space, and the bottom sign legend is separated from the longitude tick labels. |

The AI paragraph also passes the requested check: named GPT-6 and Opus 5.5 roles are disclosed, GPT-6-astra is attached specifically to independent review, Barry's role is scientific direction and critical review, and the earlier-pipeline version inventory/final-disclosure confirmation remains explicitly pending. The separate author-approval field does not claim approval has occurred.

No open finding remains from this review. Final assembled-document rendering and the reported 4,964-word count remain the parent's build checks; this closure does not claim they have been independently verified here.

Inspected identities:

- Main source SHA-256: `67d7916c2f29d7072cc2303a629d6a01332007767b593b02f69251e8f21ae6a9`.
- National-map PNG SHA-256: `1f6766d31f0048329133c3273f6b09a747f217321312aa753c22c7c31ced0c55`.

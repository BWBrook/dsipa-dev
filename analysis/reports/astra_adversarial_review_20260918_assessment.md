# Parent assessment of the independent Astra/max review

The fresh review provides substantive grounds to reopen the spatial analysis
before submission. I accept its two principal scientific findings. My earlier
assessment that the scientific tranche was closed was premature with respect
to spatial measurement fidelity. Correct arithmetic on reproducible extractions
did not establish that those extractions implemented the stated spatial supports.

## Findings and implications

| Finding | Parent assessment | Necessary response, proposed only |
| --- | --- | --- |
| M1: coarse inward/outward buffer geometry | Confirmed. One segment per quadrant and 500 m outward-boundary simplification do not adequately implement the stated kilometre supports. | Define an accuracy tolerance, test geometric/raster convergence, and regenerate affected bands, surrounding summaries and dependent results. |
| M2: coarse terrestrial mask | Confirmed against the actual cached production land union. Entire accepted Henderson, Torndirrup and Lord Howe reserve polygons lie outside its land geometry. | Select and validate a coastline/land source appropriate to the analysis scale and island coverage; then quantify effects on surrounding eligibility and categories. |
| M3: public reproduction route | Valid release-readiness issue. The code/private-input hash checks and public-file identities must be reconciled; this does not itself establish a numerical error. | Build and test a coherent release against its intended archived inputs. Public release remains Barry's decision. |
| Minor Layer B findings | The scaled-no-data sampler defect is independently reproduced; species-level deduplication and model-reporting discrepancies are supported by source inspection. | Correct methods descriptions and establish whether invalid samples occur in accepted model inputs before deciding on refitting. |

No correction or production rerun was implemented in this review task.

## Parent verification, separate from the commissioned review

I used a separately written short probe on the accepted remote GPKG, 2024
raster and production land-union cache. Grey Peaks's implemented 1–5 km band
selects ten valid cell centres; six are only 610–991 m from the reserve boundary.
A 64-segment approximation selects four cells, all genuinely at least 1 km
inward, so the ten-pixel eligibility criterion fails. This is an actual
support/eligibility error for the stated band, not an all-touched rasterisation
convention. The reviewer additionally checked convergence and all twelve years.

Using the production cache rather than reconstructing a new land union, I
confirmed zero land-mask intersection for the three coastal reserve examples.
Their interior representative points are 1.429 km (Henderson), 4.129 km
(Torndirrup) and 570.002 km (Lord Howe) from represented land. These distances
are diagnostics of the coarse mask, not estimates of corrected surrounding
radiance. The national prevalence and category impact remain unquantified.

I also independently reproduced the no-data sampler example: raw no-data,
another negative invalid value, and a valid positive value sampled at scale 10
return finite values -327680, -10 and 10. The first two therefore evade the
current finite-value filter. This proves the code path, not contamination of
the reported biological fit. No row-level impact claim is made.

The numerical checks supporting M1/M2 took a few seconds on deep-server,
reading existing inputs only. Local geometry and synthetic sampler checks were
small. No remote files, accepted inputs, analysis code or manuscript sources
were changed. Probe sources/results are preserved in the review artefact folder.

## What remains supported

The independent reviewer checked all 4,426 inside slopes against SciPy and
reproduced the headline count and area arithmetic. It found the current
zero-slope explanation, product-continuity cautions, uncertainty limitations
and biological inference restrictions defensible. The four illustrative sign
categories also survived the reviewer's buffer-geometry correction with the
land mask held fixed; their numerical slopes and sampled support changed.

These checks support retaining the whole-reserve evidence while correcting the
spatial comparisons. They do not prove that national paired categories or the
1,205/119/32/79 band results will survive corrected extraction. Those results
must remain provisional pending correction. A wording-only disclaimer would
not resolve the demonstrated spatial errors.

## Recommended next tranche

A focused spatial correction and sensitivity tranche should precede final
substantive editing of affected Results: validate geometry precision and land
coverage first, separately quantify their effects, regenerate dependent outputs,
and reconcile the manuscript. Whole-reserve inside trends need not be refitted
merely because surrounding or inward-band geometry changes. Resolve the minor
Layer B points and prepare release reconciliation alongside that work. This is
a recommendation arising from review, not authorisation for implementation or
publication.

Full independent memo: `astra_adversarial_review_20260918.md`.
Commission/scope records: matching `*_brief.md` and `*_scope.json`.
Evidence archive: `artefacts/astra_adversarial_review_20260918/`.

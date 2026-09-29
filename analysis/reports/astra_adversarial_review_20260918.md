# Independent adversarial scientific review of DSIPA

**Review date:** 18 September 2026. **Intended journal:** *Remote Sensing in Ecology and Conservation* (RSEC). **Recommendation:** **MAJOR REVISION / APPROVE WITH CHANGES**, meaning that the present scientific product needs substantive correction before submission. This is a review, not approval to modify or publish anything.

The paper contains a defensible descriptive assessment, unusually explicit limits on environmental and biological inference, and headline arithmetic that survived independent checks. Nevertheless, the implemented spatial supports do not reliably represent the stated kilometre distances or adjacent terrestrial landscape. A targeted check changes an actual reserve's eligibility for the principal inward-band sensitivity. These are consequential measurement defects, not merely requests for more discussion. The current public deposit also cannot run the current audit scripts as written. I identify three MAJOR and three MINOR findings below. I found no evidence requiring abandonment of the entire study, and assign no separate BLOCKER finding.

## 1. Scope and independence

I reviewed the current working tree of `/home/bwbrook/papers/dsipa-dev`, including uncommitted manuscript, scripts, tables and figures. HEAD was `907075e`; this review is deliberately **not** a verdict on HEAD alone. The reading copies were:

- [Main manuscript PDF](/home/bwbrook/papers/dsipa-dev/build/final_read/audit_20260918_closeout/dsipa_rsec_audit_main.pdf), 21 pages, SHA-256 `55cd8b91c20afdda6d058cb1908bf48477c2f37aa02af77b4450979e3797b002`.
- [Supporting Information PDF](/home/bwbrook/papers/dsipa-dev/build/final_read/audit_20260918_closeout/dsipa_rsec_audit_supporting_information.pdf), 20 pages, SHA-256 `8e7954e8d6484f76a9cb9f79957a3ada6b555e2005dd3d0532b0efa61b2d3c62`.
- The active sources under [manuscript/text](/home/bwbrook/papers/dsipa-dev/manuscript/text), their tables/captions, the rendered four main and eight supplementary figures, relevant extraction, trend, uncertainty, occurrence and audit code, local data/evidence, and selected accepted remote inputs.

PDF page references below are physical PDF page numbers. Code/source line references refer to the reviewed working tree. The parent supplied an identity check on the reading bundle and recorded a broader file manifest at [astra_adversarial_review_20260918_scope.json](/home/bwbrook/papers/dsipa-dev/analysis/reports/astra_adversarial_review_20260918_scope.json); it supplied no scientific interpretation. My inspection was claim-directed, not a line-by-line audit of every historical utility or log. I did not independently render the DOCX companions or rebuild the manuscripts.

I read `AGENTS.md` and the independent-reviewer and PDF skills. I first read the current manuscript/SI and wrote nine provisional challenges to `/tmp/dsipa_astra_review_20260918/provisional_criticisms.md`, before consulting code or previous review judgements. These concerned product continuity/calibration, spatial support, area accounting, interpretation of inward bands, resampling, the two-part record model, novelty, public reproducibility and display consistency. Some were rejected after checking; two spatial concerns became concrete defects. I did not consult personal memory, correspondence-board discussions, other agents, dedicated earlier scientific review memos, the successor handover, or interpretation notes. Later operational contracts, provenance and the public deposit inevitably contained earlier acceptance claims; I treated them as statements to test. No further reviewers were delegated work.

Only this memo and temporary review files were written. I did not change scientific inputs or code, download raw datasets, rerun national extraction, fit the occurrence models, initiate expensive computation, commit, publish or contact anyone externally. Before remote inspection I read the required Nectar instructions and resource-selection documents. Remote work consisted of read-only metadata, selected geometry queries and small raster windows, each short enough to complete interactively; no sustained calculation required `tmux`.

## 2. Scientific assessment and journal fit

The paper asks a useful monitoring question: which reserves can this particular annual satellite product evaluate, what do its inside and surrounding trajectories show, and which apparent absences of change are actually consequences of aggregation or non-detection? That question is coherent with the final manuscript's product-descriptive estimand. The fixed CAPAD 2024 estate, strict trend-sign categories, and distinction between full-period slopes and later positive observations are all defensible choices when stated this clearly.

The novelty is incremental and operational. Comparisons of lighting inside and around protected areas predate this study; for example, [Guetté et al. (2018)](https://www.sciencedirect.com/science/article/pii/S0006320717319043) analysed global protected-area lighting and surrounding gradients, and [Mu et al. (2021)](https://doi.org/10.3390/rs13091849) analysed changing lighting in global protected areas. The manuscript acknowledges this literature. Its prospective contribution is the Australian 2013–2024 assessment with explicit eligibility, source-product cautions, annual trajectories and interpretable screening categories, rather than a new trend estimator or first demonstration of protected-area lighting change. That can fit RSEC as an applied remote-sensing assessment. The spatial measurement defects below undermine precisely the part of that contribution presented as a transferable monitoring design.

I do **not** regard absence of a new causal ecological analysis as a defect: the manuscript makes no such claim. Nor do I require a physically calibrated sky-brightness estimate from a product expressly reported in derivative units. An independently processed night-lights product or site validation would strengthen environmental interpretation and operational usefulness, but the current restrictions on attribution make this optional for the narrow descriptive paper. It would become necessary if revision promoted the flags to confirmed lighting encroachment, ecological darkness, biological response or conservation priority.

The secondary occurrence-record comparison contributes relatively little to the central paper. Its principal result is weak discrimination of two differently observed record groups, not a biological test of reserve lighting effects. The final text recognises this. Retention is an editorial choice; the methods need to match the implementation if it remains.

## 3. Ranked findings requiring revision

### M1 — MAJOR: the inward bands and outward buffers do not implement the stated distance supports

**Affected claims.** Main Methods 2.2, main PDF p. 5; matched-band results and interpretation, pp. 9 and 12; SI p. 6 and Tables S4–S5. [Supplementary methods, line 50](/home/bwbrook/papers/dsipa-dev/manuscript/text/supplementary_methods.md:50) calls the support the “exact 1–5 km inward band.” This is incorrect for the current geometry implementation.

**Implementation evidence.** [layerA_national.py, lines 60–61](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerA_national.py:60) sets `BUFFER_QUAD_SEGS = 1` and a 500 m simplification tolerance. [build_buffers, lines 429–440](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerA_national.py:429) simplifies reserve boundaries by 500 m and then buffers them with one segment per quadrant. [build_rings, lines 551–579](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerA_national.py:551) does not apply that simplification, but uses the same one-segment setting for inward erosion. Concave corners therefore admit points closer to the boundary than the nominal inward distance. Neither approximation is disclosed in the spatial Methods.

A small geometric counterexample isolates the problem without any dataset: an L-shaped polygon with vertices `(0,0), (10000,0), (10000,4000), (4000,4000), (4000,10000), (0,10000)` admits point `(3350,3350)` to the implemented 1–5 km band, although that point is only 919.24 m from its boundary. A high-resolution circular buffer excludes it. Raster spacing does not make this mathematical discrepancy disappear.

**Accepted-input counterexample.** I then checked Grey Peaks (`QLD_0239GRP001`) on the preserved national GPKG and actual annual source rasters. The accepted row at [edge_followup_band_slopes.csv, line 376](/home/bwbrook/papers/dsipa-dev/analysis/reports/edge_followup/edge_followup_band_slopes.csv:376) has a positive whole-reserve slope, positive surrounding slope, and positive 1–5 km slope of `0.6666667`; it is one of the 32 positive whole-reserve cases said to retain a positive inward-band slope.

| Grey Peaks check | Implemented band | Full boundary, 32 segments per quadrant |
|---|---:|---:|
| 1–5 km polygon area, km² | 1.854587 | 1.159680 |
| Valid raster pixels per year | 10 | 4 |
| Years meeting the ten-pixel requirement | 12 | 0 |
| Retained band slope | 0.666667 | Missing / ineligible |

The implemented band's ten sampled 2024 cell centres have actual distances to the reserve boundary of **610.41, 886.97, 912.28, 940.18, 969.67, 990.81, 1018.63, 1101.57, 1266.07 and 1274.22 m**. Six are less than 1 km inward. Buffers with 16, 32, 64 and 128 segments per quadrant all retain only four pixels. This establishes an actual eligibility error for the stated estimand, not just a difference between two arbitrary smoothing settings. The same ten-versus-four support held across all twelve annual rasters.

Eight deliberately selected, relatively small reserves with positive whole-reserve slopes and eligible bands were checked; they are diagnostic examples, not a random estimate of national error. Other changes included Mandingalbay Yidinji, 53 to 42 pixels and band slope 0.37736 to 0.33036; Yanchep, 13 to 12 pixels and 0.51282 to 0.41667; and Korung, band area 3.03435 to 1.69015 km², with a zero slope under both versions. Mirima's first positive band observation shifted from 2018 to 2020. These examples show that the error can affect support, magnitude and apparent timing, not only polygon area.

**Outward-buffer consequence.** For all four main illustrative reserves, I reconstructed the accepted surrounding series from the current coarse geometry, then repeated extraction with the original unsimplified boundary and 32 buffer segments per quadrant. I held the land and protected-tenure masks fixed, so this isolates geometry approximation from M2.

| Reserve | Primary unprotected-buffer area, km²: current → finer geometry | Valid pixels: current → finer geometry | Surrounding slope: current → finer geometry |
|---|---:|---:|---:|
| Black Mountain | 6.873 → 9.393 | 36 → 49 | −3.91204 → −3.95153 |
| Bungonia | 5.031 → 7.006 | 24 → 36 | 0.50463 → 0.41667 |
| Neerabup | 28.213 → 32.982 | 146 → 174 | 3.52169 → 3.84674 |
| Henderson | 2.122 → 3.537 | 10 → 19 | −0.06250 → −1.34211 |

The original extractions reproduced the accepted slopes to floating-point precision. All four illustrative **sign categories survived** the finer-geometry check. I therefore do not claim that these examples reverse the paper's category interpretation. The support and slope differences are nonetheless large, especially for Henderson, and cannot justify the Methods' unqualified distance definitions.

**Why it matters.** The current 1,205-reserve matched cohort and the 119/32/79 band counts are valid arithmetic on the stored extraction, but not validated counts for the claimed distance bands. Correctly holding the original cohort fixed does not repair incorrectly defined support. A “1 km” mask that includes cell centres 610 m inward also compromises interpretation of boundary concentration at the sensor's coarse native resolution.

**Bounded remedy and acceptance criterion.** Define the intended distance rule explicitly; use sufficiently accurate unsimplified geometry or a demonstrated approximation with a predeclared error tolerance. Test concave and multipart polygons, and test sampled cell-centre distances independently of the buffering function. Establish convergence of eligibility and summaries as geometric precision increases. Regenerate the affected ring and surrounding summaries and all dependent cohorts, tables and figures, preserving the previous version for provenance. This does not require refitting unaffected whole-reserve inside trends merely to address ring geometry. Report the extent of category and eligibility changes on a common cohort, as well as newly eligible/ineligible reserves. Replacing the word “exact” alone would not address the substantive measurement error.

### M2 — MAJOR: the 1:110 million land mask is too coarse for the primary 1 km coastal comparison

**Affected claims.** [Main Methods, line 37](/home/bwbrook/papers/dsipa-dev/manuscript/text/manuscript_draft.md:37), main PDF p. 5, and [Discussion, lines 99–101](/home/bwbrook/papers/dsipa-dev/manuscript/text/manuscript_draft.md:99), p. 10, present removal of ocean as a correction that makes adjacent unprotected-land comparisons more consistent. The implementation uses [Natural Earth `ne_110m_land`, lines 56–57](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerA_national.py:56), loaded at lines 224–256 and intersected with surrounding buffers at lines 449–456. Here “110m” means **1:110 million cartographic scale**, not 110 metres; the [official Natural Earth description](https://www.naturalearthdata.com/downloads/110m-physical-vectors/110m-land/) identifies that product and its limited island representation.

**Direct accepted-input evidence.** Intersecting selected accepted terrestrial reserve geometries with that same repaired, projected land union gave:

| CAPAD reserve | Polygon area, km² | Polygon area inside the land mask | Distance of an interior representative point from the mask's land |
|---|---:|---:|---:|
| Henderson (`WA_39584`) | 2.981 | 0% | 1.429 km |
| Torndirrup (`WA_05225`) | 40.216 | 0% | 4.129 km |
| Lord Howe Island (`NSW_LHI`) | 13.139 | 0% | 570.002 km |

Torndirrup is not an ambiguous marine-only reserve: the [responsible Western Australian agency](https://exploreparks.dbca.wa.gov.au/park/torndirrup-national-park) describes its terrestrial peninsula, headlands, trails and vegetation. The coastline product excludes its entire accepted reserve polygon. Lord Howe Island has no land-mask representation and consequently an empty primary surrounding buffer in this check. For Henderson, a main illustrative example, the nominal terrestrial mask lies beyond much of the actual reserve and its immediate surroundings. The surviving “land” fragments are therefore not a faithful representation of the stated adjacent landscape.

This test does not estimate the national prevalence of mask errors or calculate corrected coastal trends: no finer national coastline was downloaded. It also does not prove that every currently retained coastal pixel is water. It establishes that the chosen mask can omit entire known terrestrial reserves and shift the represented coastline by distances exceeding the primary buffer width. The direction and magnitude of radiance bias need actual corrected extraction, not speculation.

**Why it matters.** Coastal reserves are precisely where land masking is intended to improve measurement. A coarse mask can change which reserves have ten surrounding pixels, which landscape is sampled and the paired sign category. Comparing low/high land fractions computed from this same mask cannot validate its geographical accuracy. The manuscript's generic acknowledgement of sensor pixel mixing does not disclose or resolve an independent vector-coastline error.

**Bounded remedy and acceptance criterion.** Use a documented coastline/land dataset appropriate to kilometre-scale Australian comparisons, with known island coverage. Validate representative mainland coasts, peninsulas and offshore islands against authoritative geography and the raster grid. Recompute affected land/unprotected-land summaries, feasibility and paired categories; quantify effects separately from M1's buffer approximation. Identify reserves for which adequate surrounding land genuinely does not exist. Do not repair the mask by treating every CAPAD polygon as land without assessing wetlands, intertidal areas and other boundary cases. The required work is a measurement correction and sensitivity assessment, not a new ecological hypothesis.

### M3 — MAJOR: the public scientific product lacks current reproducible audits, and public inputs fail the current scripts' identity checks

**Observed access boundary.** The paper accurately states at [Data accessibility, line 133](/home/bwbrook/papers/dsipa-dev/manuscript/text/manuscript_draft.md:133), main PDF p. 13, that code, complete environment, detailed provenance, Layer B derivatives and new diagnostic companions remain private. I queried the live [Zenodo record](https://doi.org/10.5281/zenodo.21524637) through its public API and inspected its README and [SHA256SUMS](https://zenodo.org/api/records/21524637/files/SHA256SUMS/content). It contains nine scientific payloads plus README, manifest and checksums, with no current source-code or audit package. The declaration is candid; candour alone does not make the current article externally reproducible.

**Concrete incompatibility beyond private access.** [coauthor_evidence.py, lines 25–31 and 59–63](/home/bwbrook/papers/dsipa-dev/analysis/coauthor_evidence.py:25) requires private accepted-input hashes and raises `ValueError` if they differ. [audit_product_continuity.py, lines 148–149](/home/bwbrook/papers/dsipa-dev/analysis/audit_product_continuity.py:148) hard-asserts the private radiance hash. The publicly archived radiance file has a different identity:

| File | Current audit/accepted input SHA-256 | Public deposit SHA-256 |
|---|---|---|
| `pa_radiance_buffers_national_v0_3_0.csv` | `63e95fb30b0bdebc6c74d23f08666ab9cfe0ef408d27744f12fbb029a8b92ec1` | `6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61` |
| `pa_edge_profiles_national_v0_3_0.csv` | `ddb9c9f5678f9da10b70754d3c9319ea30bfe7203d3c80c8f8f298ed2cf5783b` | `baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812` |
| `pa_geometries_v0_3_0.gpkg` | `da843f551bf1863dc5d1930ecb657491f73d69827b25007a0c55c9019721d0e6` | `6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9` |

The edge-profile private identity is recorded in [interior_area_summary.json, lines 24–27](/home/bwbrook/papers/dsipa-dev/analysis/reports/interior_area_audit/interior_area_summary.json:24). I verified the GPKG hash directly on the accepted remote source. The public deposit itself describes several accepted non-exact reproductions. Different bytes are **not evidence of fabricated or materially different scientific results**; formatting, ordering and bounded differences are possible. They do prove that giving an external reader the existing code plus the existing DOI would not run these exact diagnostics without reconciliation. I did not download the large public payloads to adjudicate row-level equivalence.

The generic [run_full_pipeline.sh, lines 43–55](/home/bwbrook/papers/dsipa-dev/analysis/run_full_pipeline.sh:43) also does not orchestrate the current coauthor/product/interior/edge audit sequence. There needs to be a clear route from the intended archived inputs to the current paper, not merely a legacy full-pipeline entry point and a set of separately runnable scripts.

**Venue relevance.** The live [RSEC author guidelines](https://zslpublications.onlinelibrary.wiley.com/hub/journal/20563485/author-guidelines), checked on the review date, require code, tests of critical functionality and demonstration datasets under their methods/analysis/software AI guidance. They also require disclosure of the tools and their research roles. The private-code boundary and incomplete AI declaration therefore need resolution for this explicitly AI-assisted project; this is not an invented requirement to publish restricted occurrence records.

**Bounded remedy and acceptance criterion.** Prepare a versioned release containing current code, lockfile, critical tests, a small runnable example, current diagnostic tables and exact provenance. Either archive the exact inputs used by the audits or demonstrate and encode the transformation/equivalence linking them to the public inputs; do not simply delete the hash guards. Provide one documented manuscript-reproduction route and test it from the intended release material in an isolated environment. For licensed occurrence records, supply permissible aggregates, exact acquisition/filtering instructions and a representative demonstrator, with the remaining reconstruction boundary explicit. Publication itself remains an author action; this review does not authorise it.

### m1 — MINOR: occurrence deduplication is described at taxon-group level but implemented at species level

**Evidence.** SI p. 2 and [supplementary_methods.md, line 17](/home/bwbrook/papers/dsipa-dev/manuscript/text/supplementary_methods.md:17) say at most one record was retained per 1 km cell, day and taxon group. [layerB_data.py, lines 468–490](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerB_data.py:468) instead constructs `species|date|grid_x|grid_y`, falling back to scientific name or unknown. A direct three-record example, two species in the same cell/day with one duplicate species record, retains two records.

**Impact.** The observation unit is consequently a retained species record. A multi-species checklist can contribute multiple records to a group at the same cell/day. That matters to the spatial weighting of the already strongly selected record comparison. The current limitations discuss unmeasured effort, but readers cannot reconstruct the actual deduplication from the stated rule.

**Remedy.** Describe the implemented species–cell–day rule accurately, including the name fallback, and note the resulting record weighting. If the intended analysis truly was one observation per group–cell–day, implement and reevaluate that distinct estimand. A rerun is not required merely to relabel a defensible species-record analysis accurately. A test with two species sharing a cell/day should pin the intended rule.

### m2 — MINOR: the secondary raster sampler can turn missing/invalid exposures into the zero-light covariate category

**Evidence.** [layerB_model.py, lines 170–181](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerB_model.py:170) applies scale and offset before comparing against the raster's unscaled no-data code. It also returns other negative values. [Lines 426–428](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerB_model.py:426) retain all finite values and encode non-positive exposures as `any_light=0` and `log1p_alan=0`.

A synthetic int16 raster with raw values `[-32768, -1, 1]`, no-data `-32768`, scale 10 and offset 0 returns `[-327680, -10, 10]` from this sampler. The first two remain finite, so both reach the model with the same two covariate values as a valid product zero. This conflicts with the primary product's distinction between non-detection and invalid data.

**Impact limit.** This is a real implementation defect, but I did **not** establish that it changes the published Layer B results. The stored Australian raster-window audit reports no negative pixels for 2022–2024, and the row-level occurrence inputs were unavailable for direct checking. No-data at an observation outside valid raster support or other invalid samples remains a possible route. It would be unjustified to assert that the reported AUC is corrupted on this evidence.

**Remedy.** Mask raw no-data/invalid values before decoding, or use an appropriate masked sampling path; handle negative invalid codes consistently with Layer A. Count affected observations in the accepted features before deciding whether refitting is necessary. Add a small scaled-no-data test, including an out-of-coverage location. Preserve the existing result if the affected count is demonstrably zero.

### m3 — MINOR: specify the secondary model's penalty, metric aggregation and intensity-dependent contrast

**Evidence.** [SI Methods, lines 21–25](/home/bwbrook/papers/dsipa-dev/manuscript/text/supplementary_methods.md:21) describes balanced logistic regression and out-of-fold metrics. The implementation at [layerB_model.py, lines 471–512](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerB_model.py:471) uses `LogisticRegression(max_iter=200, solver="liblinear")`, hence the installed implementation's default L2 penalty and `C=1`, without predictor standardisation. [Line 646](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerB_model.py:646) reports the unweighted mean of fold AUCs/log losses, not metrics computed once after pooling all held-out predictions. These are defensible choices, but need to be reproducible from the Methods.

The model is `logit(p) = a + b0 I(r>0) + b1 I(r>0) log(1+r)`. Thus `b0=1.316` is not the general contrast of any positive exposure against zero; that contrast is `b0 + b1 log(1+r)`. At the observed minimum positive pixel value of 10, the mean coefficients give approximately 0.466 log-odds, or 1.59 on the odds scale. Exponentiating `b0` alone gives 3.73, the extrapolated contrast at an unattainable positive intensity approaching zero. The current SI does not explicitly claim that latter odds ratio as an ecological effect, so this is a clarity/reproducibility finding, not an allegation of a false stated effect.

**Remedy.** State the penalty/strength/solver and averaging rule; give the model equation and clarify the reference for `any_light`, or display contrasts at observed intensities. Retain the existing caution that these are record-classification coefficients and that fold SD is not inferential uncertainty. No new biological analysis is needed to fix this.

## 4. Substantive claims that withstood challenge

These conclusions are deliberately separated from results requiring spatial correction.

1. **Whole-reserve trend arithmetic is correct on the supplied annual series.** I independently applied SciPy's Theil–Sen estimator to all 4,426 complete inside annual series in [product_annual_series.csv](/home/bwbrook/papers/dsipa-dev/analysis/reports/product_annual_series.csv) and compared the accepted mean/unprotected-land rows of [pa_trends_v0_3_0.csv](/home/bwbrook/papers/dsipa-dev/data/processed/pa_trends_v0_3_0.csv). Maximum absolute slope discrepancy was `4.44e-16`. Counts were 420 positive, 37 negative and 3,969 zero; 3,844 had zero inside mean in 2024. This checks estimator/output agreement, not independently every national raster extraction.

2. **Zero slopes do conceal temporal variation, exactly as described.** The 3,969 zero-slope series comprise 3,786 all-zero histories, three constant positive histories and 180 varying histories; 78 meet the stated nine-early-zeros/late-positive pattern. All had twelve valid observations. Nine identical early zeros generate 36 zero pairwise slopes among 66 total pairs, sufficient to force a zero median even with three subsequently increasing values. This is a valid, useful explanation, not a detection of ecological onset.

3. **Area arithmetic and its restrictions are sound.** Summed reserve area from the descriptor file was 1,713,990.923 km²; eligible reserve area was 1,710,860.242 km², or 99.8173%. Positive-slope reserve polygons account for 37.5896% of eligible summed area. The three equal-count positive-slope terciles contain 637,619.968, 4,094.264 and 1,391.408 km², respectively: 99.1470% of positive-class area belongs to the lowest-slope tercile. The text correctly distinguishes full reserve-polygon area from lit-pixel area, and summed designations from a unique non-overlapping land-area estimate. The headline does not establish that 37.6% of reserve land materially brightened.

4. **Category and inward-band tables agree with their stored inputs.** The 3,858 paired cases give Q1=305, Q2=55, Q3=3,308 and Q4=190. The stored matched-band cohort contains 1,205 reserves, 119 positive whole-reserve slopes and 32 positive 1–5 km slopes among those 119. The 0–1/1–5 km sign cross-tabulation and the distinction between zero slope and all-zero band histories agree with the reported 79 cases and Q1-loss counts. In particular, 54 of the 68 Q1 losses had all-zero band histories; 14 had some positive values. These are not arithmetic errors. Their interpretation as accurately defined distance bands is what fails under M1.

5. **The primary extraction correctly distinguishes raw invalid codes from valid zeros.** The Layer A extraction and current product-audit logic exclude negative/no-data codes and apply the annual scale/offset. I found no tenfold rescaling error in the primary accepted trend path. The mixed-sensor/source-product boundary is a real interpretive concern, but the current manuscript explicitly acknowledges it and avoids physical-unit conversion.

6. **The product-continuity statements are appropriately restricted.** I matched the twelve annual source-file identities against the [live deposited metadata](https://zenodo.org/records/17294744), inspected retained scale/source tags and stored histogram/transition evidence, and independently reconstructed first-positive risk-set arithmetic from the annual-series table. The 1 km and 5 km buffer cohorts are correctly separate from the inside-eligible cohort. The stored common-support transition counts give 31,475, 28,035, 57,328 and 36,764 zero-to-positive pixels in 2021–2024. The fall in 2022 and increase in 2023 are not evidence uniquely identifying environmental change or a processing mechanism. The text says so, acknowledges the 2017 pulse, and correctly treats persistence as non-discriminating. I did not rerun the 149,331,864-pixel diagnostic, so its raw-pixel totals remain supported by stored evidence rather than an independent complete scan.

7. **Temporal resampling is no longer presented as calibrated uncertainty or ranking confidence.** The original-year block/pairs algorithm and variable per-area draw multiplicity match Supporting Methods S1. Independent within-reserve resamples cannot estimate joint spatial covariance; the paper now states this explicitly, labels ranges as sensitivity summaries, explains legacy column names and omits the unsupported pairwise dominance display. The procedure's limited inferential value is not hidden. A new calibrated bootstrap is optional unless the authors want confidence statements they presently avoid.

8. **The biological interpretation is restrained.** The manuscript confines Layer B to classification of microbat versus passerine records, reports weak AUC (0.545), distinguishes one shuffled realisation from a null distribution, and identifies provider, effort, protocol, detectability and species-pooling limitations. The coefficient/AUC values match the preserved modelling report. I found no present claim of abundance, occupancy, population decline or causal light response. Passing spatial cross-validation would not resolve those biases, and the paper does not say that it does.

9. **Several suspected spatial/accounting failures were not substantiated.** The main national path builds the protected-area exclusion union from the full estate, including when statewise work is used; [layerA_national.py, line 1107](/home/bwbrook/papers/dsipa-dev/src/python/dsipa/layerA_national.py:1107) uses `pa_gdf_all`. I found no basis for alleging systematic omission of neighbouring jurisdictions. Extraction uses Rasterio's default inclusion rule with `all_touched=False`, principally selecting pixel centres; its [documentation](https://rasterio.readthedocs.io/en/stable/api/rasterio.mask.html) also specifies boundary pixels selected by the line algorithm. Cell support is not equivalent to native independent observations, but the Methods explicitly say this. Correcting M1/M2 should not be conflated with a claimed cross-state-union or pseudoreplication error that I did not find.

10. **The rendered scientific displays are usable.** I inspected all twelve main/SI figures visually as well as the extracted text. I found no missing panels, material clipping, invented precision bands or contradiction between current captions and the stated non-inferential interpretation. Neerabup, Henderson, Black Mountain and Bungonia appropriately illustrate four different sign categories rather than a representative sample. The mixed endpoint/full-period behaviour of Henderson is real under the stored series.

## 5. Evidence quality and reproducibility limits

The local repository contains substantial provenance and derived audit material, but lacks the accepted national GPKG, full annual extraction and raw national/Layer B inputs needed for an unrestricted rerun. I inspected the accepted Layer A source tree read-only at `/data/codex/repos/dsipa-dev-goal012-20260723T115300Z` on `deep-server-ts`. Its extraction engine SHA-256 was `7fe6543c081c612b25d4fb641baefc99a92be9cf894a9e13688ce6dfc5314aa9`, identical to the reviewed local engine. Its GPKG identity is recorded above. Recreating the four main examples with that code/data and obtaining the accepted numbers supports the attribution of M1/M2 to the actual analytical path.

I did not revalidate all 11,133 source polygons against the raw CAPAD archive, all national raster means, every downloaded byte against a newly downloaded file, or every bibliography entry against its primary publication. I checked the literature and technical sources consequential to novelty, measurement and venue requirements. Source-product metadata and repository checksums do not independently validate physical radiance or upstream processing. I did not retrieve restricted occurrence records or refit/replicate the cross-validation models; the archived report supports numerical agreement, while source inspection supports the identified methods discrepancies.

The selected spatial probes establish counterexamples, not a corrected national analysis or an estimated error rate. The coast-mask and distance-geometry changes interact, so national impacts cannot be inferred by summing the example differences. The ten-pixel threshold creates discontinuities, as demonstrated at Grey Peaks; a small-looking spatial edit can change eligibility and therefore headline denominators.

Twenty targeted tests passed and one was skipped. This is useful evidence that the stored algorithms and audit contracts behave as expected; it did not validate the spatial estimands. Existing tests did not catch the independent boundary-distance or coastline-coverage failures. The skipped geometry test was due to the absent local national GPKG. No full test suite, package build, clean release reconstruction or complete PDF/DOCX rebuilding was undertaken in this review.

## 6. Necessary work versus optional improvements

**Necessary before submission:** correct and validate spatial support (M1/M2); regenerate and reconcile affected analyses; make the current scientific release reproducible from its intended inputs (M3); correct the species-level deduplication description; resolve the secondary sampler defect with an affected-record count; and report the retained model settings/contrast clearly. The author/declaration placeholders at main source lines 139–149, including AI disclosure, also need completion by the author. They are visible administrative unfinished work, not evidence of a concealed scientific problem.

**Optional and potentially useful:** independently processed radiance/site checks to strengthen environmental interpretation; streamlining or removing the weak secondary record-classification component; replacing or dropping the low-information temporal resampling display; and reducing the repeated “review-stage” narrative so that an external reader encounters a coherent final study rather than its revision history. If Layer B is retained, an observed-intensity prediction/contrast plot would be easier to read than separate extrapolated coefficient bars. Some SI map labels are small. Henderson's exact surrounding slope of −0.0625 is rounded to −0.063 in the main text and −0.062 in the SI; consistent rounding would remove a trivial distraction without changing any result.

The main new scientific risks are misassigned distance support (demonstrated, high impact for band eligibility), incorrect coastal support (demonstrated, national extent unquantified), and an externally broken reproduction path (demonstrated). The secondary invalid-exposure risk is a proven code path with unverified impact on the current data. The original worries about erroneous inside-slope arithmetic, inflated area interpretation, calibrated bootstrap claims and causal biodiversity overreach were not substantiated in the current manuscript.

## 7. Commands and review checks actually executed

All local commands ran from `/home/bwbrook/papers/dsipa-dev` unless noted. This inventory groups repeated read-only inspection commands; it does not present unrun suggested checks as completed work.

**Instructions, inventory and source inspection.** I used `cat` on the applicable instruction/skill files, `git status --short`, `git log`, `rg --files`, targeted `rg -n` searches, `nl -ba ... | sed -n ...`, `head`, `ls -lh`, and `sha256sum`. Principal code inspected included `pa_geometry.py`, `nightlights.py`, `landmask.py`, `layerA_national.py`, `layerA_statewise.py`, `trends.py`, `trend_uncertainty.py`, `layerB_data.py`, `layerB_model.py`, current plotting/audit scripts and their tests. I inspected current reference contracts and provenance after writing the provisional scientific challenges.

**Document checks.** I ran `pdfinfo`, `pdftotext -layout`, and `pdftoppm` on both supplied PDFs, writing text and page images only under `/tmp/dsipa_astra_review_20260918/`. Page-image contact sheets `main_figs.png`, `si_figs1.png` and `si_figs2.png` were inspected with the image-viewing tool. No manuscript build command was run.

**Executed targeted test command:**

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider \
  --basetemp=/tmp/dsipa_astra_review_20260918/pytest_tmp \
  tests/python/test_trends.py \
  tests/python/test_trend_uncertainty.py \
  tests/python/test_pa_geometry.py \
  tests/python/test_audit_interior_area.py \
  tests/python/test_audit_edge_followup.py \
  tests/python/test_audit_product_continuity.py \
  tests/python/test_coauthor_evidence.py \
  tests/python/test_layerB_filters.py \
  tests/python/test_risk_rankings.py -rs
```

Result: **20 passed, 1 skipped**, approximately 1.3 seconds; skip at `test_pa_geometry.py:16` because the national GPKG was absent locally.

**Independent numerical checks.** Local `.venv/bin/python` heredocs loaded the annual-series, trend, geometry-descriptor, product-transition, first-positive and band-summary CSVs using pandas/numpy; recomputed all inside slopes with `scipy.stats.theilslopes`; counted zero-series patterns, paired categories and band transitions; summed polygon areas and terciles; and rebuilt first-positive risk sets. Separate small in-memory examples exercised species deduplication, scaled raster no-data sampling and the L-shaped inward buffer. The active local environment reported Python 3.12.3, numpy 2.3.5, pandas 2.3.3, scipy 1.16.3, geopandas 1.1.2, shapely 2.1.2, rasterio 1.4.4 and scikit-learn 1.8.0.

**Remote accepted-input checks.** I used non-interactive SSH to `deep-server-ts` for path/size/hash inspection and piped the following temporary local Python scripts to the accepted source tree's existing interpreter. No scripts were installed remotely and no remote scientific outputs/caches were regenerated:

- `/tmp/dsipa_astra_review_20260918/spatial_probe.py`: selected nine reserve geometries, repaired/projected the source Natural Earth polygons, compared original and finer buffer geometries, and measured reserve/land-mask intersection.
- `/tmp/dsipa_astra_review_20260918/buffer_radiance_probe.py`: read annual raster windows for the four main examples, recreated the accepted surrounding slopes and compared unsimplified/high-resolution-buffer support with the same masks.
- `/tmp/dsipa_astra_review_20260918/ring_radiance_probe.py`: read annual windows for eight selected inward bands and compared one versus 32 buffer segments per quadrant, preserving ten-pixel/eight-year eligibility.
- `/tmp/dsipa_astra_review_20260918/grey_peaks_pixel_probe.py`: transformed the ten selected 2024 raster cell centres to EPSG:3577, measured distance to the true polygon boundary, and checked 16/32/64/128-segment support.
- `/tmp/dsipa_astra_review_20260918/grey_peaks_annual_support_probe.py`: a final narrow variant of the ring probe printed all twelve annual support counts, confirming ten versus four in every year.

The final support check used this exact command (and completed in approximately six seconds):

```bash
ssh -o BatchMode=yes deep-server-ts \
  'cd /data/codex/repos/dsipa-dev-goal012-20260723T115300Z && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -' \
  < /tmp/dsipa_astra_review_20260918/grey_peaks_annual_support_probe.py \
  > /tmp/dsipa_astra_review_20260918/grey_peaks_annual_support_probe_output.txt
```

Their captured `*_output.txt` files remain beside the scripts in the temporary review directory. The central numerical outputs are embedded in this memo so its findings do not depend on retention of `/tmp`. The first exploratory land-union probe encountered invalid projected global geometry; I repaired the geometry as the production code does and reran it. That scratch error is not counted as a project defect.

**External verification.** I queried official RSEC author guidance, Natural Earth product documentation, Rasterio masking documentation, the EOG annual VNL documentation, the Hengl/OpenGeoHub deposited metadata and selected primary protected-area-lighting publications. I fetched only public Zenodo metadata, the small README and checksum manifest for the DSIPA deposit, using its REST API; the ordinary web opening of the record was less reliable. No scientific payload was newly downloaded.

### Minimal reproducible checks for the two central counterexamples

The following fragments express the same checks actually used above. They require the existing accepted data tree and dependencies; they are documentation of the review method, not a requested national rerun.

```python
# Geometry-only counterexample, no project data required.
from shapely.geometry import Polygon, Point
p = Polygon([(0, 0), (10000, 0), (10000, 4000),
             (4000, 4000), (4000, 10000), (0, 10000)])
q = Point(3350, 3350)
band1 = p.buffer(-1000, quad_segs=1).difference(
    p.buffer(-5000, quad_segs=1))
band64 = p.buffer(-1000, quad_segs=64).difference(
    p.buffer(-5000, quad_segs=64))
print(q.distance(p.boundary), band1.covers(q), band64.covers(q))
# 919.2388155..., True, False
```

```python
# Accepted-data Grey Peaks support check, run on the existing remote tree.
from pathlib import Path
import sys
import geopandas as gpd
import numpy as np
import rasterio
import shapely
from pyproj import Transformer
from rasterio.mask import mask

root = Path('/data/codex/repos/dsipa-dev-goal012-20260723T115300Z')
sys.path.insert(0, str(root / 'src/python'))
from dsipa.layerA_national import build_rings

g = gpd.read_file(root / 'data/processed/pa_geometries_v0_3_0.gpkg',
                  where="pa_id='QLD_0239GRP001'")
pa = g.geometry.iloc[0]
band = build_rings(g).query('ring_index == 1').to_crs(4326).geometry.iloc[0]
path = next((root / 'data/raw/nightlights_zenodo_v0_4').glob('*_20240101_*.tif'))
with rasterio.open(path) as ds:
    a, transform = mask(ds, [band], crop=True, filled=False)
    rr, cc = np.where(~np.ma.getmaskarray(a[0]))
    xx, yy = rasterio.transform.xy(transform, rr, cc)
    x, y = Transformer.from_crs(4326, 3577, always_xy=True).transform(xx, yy)
    distance = shapely.distance(shapely.points(x, y), pa.boundary)
    print(sorted(distance.tolist()))
    print(int(((distance >= 1000) & (distance <= 5000)).sum()))
# Ten selected cells, but only four centres are actually 1–5 km inward.
```

The spatial corrections are the decisive scientific revision. They are compatible with retaining the paper's careful product-descriptive framing and much of its verified whole-reserve evidence, provided the affected analysis is recomputed and the release is reconciled transparently.

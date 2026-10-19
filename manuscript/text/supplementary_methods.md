## Supporting Methods

### S1. Temporal resampling and interpretation of zero slopes

The primary trend was the Theil-Sen slope of annual inside mean product-scaled radiance during 2013-2024, requiring at least 10 valid pixels per retained year and at least eight valid years. The archived resampling procedure used seed 42, 300 outer iterations and blocks of length three. Protected areas were assigned to their dominant IBRA7 region by area of overlap. Within each outer iteration, IBRA regions were sampled with replacement, with the number of draws equal to the number of represented regions. Whenever a region was selected, each of its protected areas received a separately generated temporal resample.

For an area's ordered annual year-value pairs, consecutive blocks of three observed pairs were sampled with replacement from the available block starts and concatenated, truncating to the original series length. Original year labels travelled with their values. Theil-Sen slopes were recomputed from these resampled pairs; pairs with identical years were excluded from slope calculation. Draws were pooled separately for each area. An IBRA region could be selected zero or multiple times per outer iteration, so the number of pooled draws varies among areas and is not fixed at 300.

The table and figure report marginal medians, 2.5th and 97.5th percentiles, and the fraction of resampled slopes greater than zero. These are sensitivity summaries for this particular temporal pairs/block procedure. They are not calibrated confidence intervals and do not quantify spatial covariance or the joint ordering of reserves. Independent temporal sampling within areas and the absence of aligned replicate identifiers prevent that interpretation. IBRA selection affects draw multiplicity rather than supplying joint spatial inference. Legacy archived column names such as `slope_ci_low`, `slope_ci_high`, `prob_slope_gt0` and `ibra_cluster_moving_block` are retained for data identity; their interpretation is corrected here. The former pairwise dominance display is omitted because it compared all pairs of marginal samples rather than matched spatial-temporal replicates.

The zero-slope diagnostic uses the accepted annual means and exactly zero full-window slopes. Annual variation means `max(mean) - min(mean) > 0` among valid years. The late-positive pattern requires all 12 years valid, all nine values from 2013-2021 equal to zero, and at least one positive value from 2022-2024. Missing years are never treated as zeros. All 3,969 zero-slope areas had 12 valid values: 3,786 were zero throughout, three were constant non-zero, and 180 varied. The 78 late-positive series are a subset of the 180 varying series. This review-stage descriptive check did not change any slope or sign category.

### S2. Product continuity and spatial-support sensitivity

The September 2026 review audited the accepted 2013–2024 annual summaries and their source rasters without replacing the primary analysis. A fixed rectangular raster window covered all inside-eligible reserves with a one-degree margin. We inspected raw-code histograms and metadata-adjusted values in 2013 and 2020–2024, extending this check to 2014–2019 after review, and tabulated adjacent-year zero/positive transitions on the same 149,331,864 pixels valid throughout 2020–2024. The window includes surrounding non-reserve land and ocean; its pixel counts are a product diagnostic, not a land-area estimate. Negative codes and no-data values were invalid. The smallest positive stored value was 10 in 2013–2021 (scale 1) and 1 in 2022–2024 (scale 10), giving an observed decoded floor of 10 throughout. Positive decoded values were multiples of 10 except for one higher-valued pixel in 2013 and four in 2019; none affected the floor. This establishes a common observed minimum, not a constant physical detection threshold. Zonal means can be smaller because they average positive and zero pixels. The source description gives a 0–200 to 0–2000 conversion, but the incomplete deposited construction path does not justify converting decoded values to physical radiance.

The retained 2022 source tag identifies a combined Suomi-NPP/NOAA-20 V2.2 masked-average layer; the full filename is preserved in the audit metadata. The [EOG V2.2 documentation](https://eogdata.mines.edu/products/vnl/VNL_v22_readme_20230707.pptx) describes a combination of 11 Suomi-NPP months with NOAA-20 observations for May, August and September, together with changes in low-coverage and background handling. Retained 2023–2024 tags identify Suomi-NPP `average_masked` layers with generic V2 names. The earlier archived [OpenGeoHub processing script](https://zenodo.org/api/records/8277198/files/nightlights_stack_500m.R/content) supports V2.1 masked inputs for 2013–2021, but the later deposit does not fully reproduce each annual COG's construction. Calendar year and product construction are partly confounded, limiting environmental attribution.

First-positive fractions used complete 12-year series satisfying the original annual requirement of at least 10 valid pixels. Each year's risk set comprised zones with zero means in every preceding year; a first positive removed a zone permanently from subsequent risk sets, including after reversion to zero. Complete series numbered 4,426 inside reserves, 9,695 in 1 km buffers and 10,207 in 5 km buffers. Their initially zero subsets numbered 4,023, 8,271 and 7,075, respectively. Buffer cohorts were defined separately and were not restricted to reserves with eligible inside series. Missing histories were excluded, never recoded as zero. Buffer overlaps and shared observations preclude treating these as independent event trials.

Inside series were stratified by minimum distance from the reserve polygon to a positive 2013 raster-cell centre in EPSG:3577: <2 km, 2–20 km and >20 km. The reference was fixed before inspecting the new diagnostics. An initial review proposal used any positive pixel in 2013–2021; it was amended because historical first detections would enter their own reference mask, biasing the contrast with 2022. Polygon-to-cell-centre distance is a finite-resolution proximity measure, not distance to an independently established light source. Larger or multipart reserves can be classified near by a single location. The comparisons remain descriptive and do not adjust for reserve size or treat the strata as exchangeable controls. Stable annual valid-pixel counts were also checked; count stability does not prove that identical pixels were valid in every year. Full counts and at-risk denominators accompany Fig. S4 and Table S2.

Zero-to-positive transitions on the common valid raster support numbered 31,475 in 2021, 28,035 in 2022, 57,328 in 2023 and 36,764 in 2024. Positive-to-zero transitions decreased from 21,520 in 2022 to 12,031 in 2023. Both buffer cohorts and common-support zero-to-positive pixel transitions declined in 2022, while inside first detections were essentially unchanged; all rose in 2023. The synchronous 2017 pulse and 2023 increases across zone cohorts are compatible with processing effects. A processing-related suppression-and-rebound pattern is one possible explanation, not an established cause. Of the 14 inside series first positive in 2022, 10 remained positive in 2023 and 11 in 2024; 13 had a 2022 maximum of 10 product units and one a maximum of 20. Such near-floor values are not unique to 2022: the lowest positive code accounted for 51.4% of positive pixels in the 2021 window and 51.8% in 2022. A post-review persistence check found next-year positive fractions of 64.5–70.6% for 2023 first detections across the three cohorts, compared with 67.9–69.9% for 2017 and 71.4–84.0% for 2022. Such persistence can arise under either environmental change or processing effects; it does not discriminate between them. The diagnostics do not establish an environmental onset date for individual reserves. No external-product comparison was made; the unresolved calendar patterns require retaining product-descriptive claims. Independently processed observations would be needed to strengthen environmental attribution.

The interior-band sensitivity used the 1–5 km inward band and the original mean-radiance Theil–Sen estimator. We retained the corrected 1 km unprotected-land surrounding slope and required at least eight band years with at least 10 valid pixels. Of 4,253 originally paired reserves, 1,341 supplied a band slope; all 1,341 had 12 valid years. The other 2,912 had no usable band-year summary. Table S3 compares categories within the same retained cohort, so changes cannot be attributed merely to switching the set of reserves. Nevertheless, that cohort represents 31.5% of the original paired set and is selected by geometry. The band omits both the first kilometre and any interior deeper than 5 km. Loss of a positive slope can reflect boundary-concentrated change, mixed pixels, detection limits or aggregation and does not diagnose optical spillover. The DNB maintains approximately 750 m resolution across its swath through on-board aggregation ([NASA product description](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP02DNB/)); the derivative grid supplies no independent finer-resolution observations.


After review of the initial audit, an exploratory follow-up computed the 0–1 km slope on the same 1,341-reserve cohort, retaining the pixel and year thresholds; all supplied 12 valid 0–1 km years. Annual band series were classified separately as all-zero or containing a positive observation, avoiding inference from a zero slope alone. Table S4 reports the two band signs among the 150 positive whole-reserve cases and divides all 420 eligible positive whole-reserve slopes into equal-count terciles. The interpolated one-third and two-thirds quantiles were 0.040200 and 0.310103 product units per year; neither boundary had ties. Slopes below or at each boundary entered the lower group. Summed polygon areas, not illuminated pixel areas, supplied the weights. Missing valid 5–10 km summaries were not treated as proof that a reserve lacked deeper interior. Median pairwise slopes over different spatial supports were not added or subtracted to reconstruct source contributions.


The 85 Q1 reserves losing a positive 1–5 km sign had median polygon area 132.8 km² and median whole-reserve slope 0.0104 product units per year, compared with 0.0563 among the 27 retaining Q1. All 85 band slopes were zero, but 12 histories included positive annual values; 73 were all-zero. Among 23 Q2 losses, 22 band slopes were zero and one negative; 20 histories were all-zero. Thus low-end non-detection is relevant, but loss of a positive sign cannot uniformly be assigned to floor censoring. The 85 Q1 losses represented 10.33% of all positive-class polygon area, whereas the national lowest slope tercile represented 99.15%; the subset and national area summaries answer different questions.


### S3. Spatial-support implementation and correction audit

Distance bands used the repaired, dissolved CAPAD polygons in EPSG:3577, with
no additional boundary simplification. Outward supports were the 1 or 5 km
buffer minus the original reserve; inward bands were differences between the
corresponding erosions. Circular arcs used 128 segments per quadrant. At radius
$r$, the maximum arc-to-chord deviation is $r[1-\cos(\pi/(4q))]$, where $q$
is the number of segments per quadrant: less than 0.19 m at 10 km for $q=128$.
This numerical precision does not imply comparable accuracy of boundaries or
satellite observations. Distances are projected rather than geodesic, and
projection distortion is larger than the arc approximation error.

A fixed-seed precision check covered 73 reserves, comprising named diagnostic
cases, a random sample and cases near the ten-pixel interior-band threshold.
The annual rasters shared the same CRS, transform and dimensions. Comparing
geometric pixel membership at 128 and 256 segments per quadrant changed one
cell in each of three 5 km raw buffers, with no difference in any tested 1 km
buffer or inward band. Eligibility and slope signs were unchanged. Two changed
supports had all-zero annual means; the third slope differed by 0.023%.

Land support used AIMS Australian Coastline 50K 2024 version 1-1 Split polygons
[@hammerton2024coastline]. These represent the full source geometry split on a
2-degree grid; local unions matched the unsplit source in eight named test
windows. The mask is static, approximately represents mean high water, and may
misrepresent bridges, estuaries or small islands. Its date does not resolve
historical erosion, accretion or reclamation. Local land intersections excluded
the complete CAPAD estate, including reserves ineligible for trend analysis.
Only polygonal components of overlay results supplied raster support; zero-area
line and point remnants were discarded. Geometrically empty or out-of-raster
supports were unavailable; raster-read errors stopped extraction.

Among 11,119 non-Antarctic CAPAD identifiers, six had no land-source overlap:
CWTH_IPA12, QLD_0289BDI001, QLD_0925HMA001, VIC_698, WA_36056 and WA_44673.
Their land-dependent surrounding comparisons were unavailable rather than zero;
whole-reserve and inward-band observations were retained. None entered the
eligible whole-reserve trend cohort. Fourteen Antarctic records lay outside the
raster footprint. Proximity to documented source exceptions was also flagged,
without assuming that an entire nearby reserve was affected.

The audit separated two implementation effects (Table S5): correcting the
initially simplified boundaries and one-segment arcs while retaining the old
Natural Earth 1:110 million land mask, then replacing that mask with AIMS land.
All twelve years were re-extracted for surrounding and inward-band supports.
Whole-reserve observations were preserved with exact keyed checks of every
annual column. Paired categories were recomputed for each eligible cohort;
common-cohort transitions and eligibility gains and losses were retained
separately. These comparisons document measurement-support sensitivity, not
independent environmental changes or uncertainty distributions.

The historical paired cohort contained 3,858 reserves, the geometry-only
correction 4,072 and the corrected coastline comparison 4,253 (Table S5).
Geometry correction added 214 eligible reserves without losses and changed
34 categories among the 3,858 common cases. Changing the land source then
added 193, removed 12 and changed 28 categories among 4,060 common cases.
Relative to the original implementation, the final comparison gained 407
reserves, lost 12 and changed 57 categories among the 3,846 common cases.
These are effects of measurement support, not environmental change between
analysis versions. Whole-reserve annual observations and the 420 positive
inside slopes remained unchanged.

Across the full estate, correcting the 1–5 km band reduced trend eligibility
from 1,432 to 1,398 reserves: 34 lost eligibility and none gained it. One
band sign changed among the 1,398 common reserves. Holding the common
inside–surrounding cohort fixed, 32 of 1,201 band-eligible reserves lost
eligibility and none of the 1,169 retained band signs changed. The joint
paired-and-band cohort nevertheless increased from 1,205 to 1,341 because
the corrected surrounding supports admitted additional reserves: 172 entered
and 36 left that joint cohort. Grey Peaks changed from ten to four valid
band pixels in every year and therefore became ineligible. Table S5 separates
these eligibility changes from sign changes among common reserves.

A separate 5 km proximity screen around documented coastline-source exceptions
flagged 19 distinct reserve identifiers. Nine belonged to the corrected paired
cohort, including two newly eligible sites; the other ten lacked eligible
inside trends. Source exceptions include bridge and estuary delineation errors.
Proximity does not establish that a particular extracted support is wrong, and
the screen neither quantifies nor corrects those local errors. The flagged
identifiers and comparison values accompany the audit, so their surrounding
results can be checked against local mapping before management use.

The nine paired comparisons near these source exceptions carry an explicit
`provisional_surrounding_comparison` flag in the distributed reserve-level
screening results. Two were newly eligible: Swan River Management Area
(WA_48325) and Brisbane Water National Park (NSW_N0006). Their surrounding
classifications require local map validation. Excluding all nine flagged
comparisons leaves 4,244 paired reserves: 341 in Q1, 70 in Q2, 3,585 in Q3
and 248 in Q4. This sensitivity addresses the flagged subset; it does not
establish that all other coastline boundaries are error-free.

### S4. Additive change budget and local pixel comparisons

The additive budget was developed during manuscript redevelopment after the original trend and spatial-support analyses. It uses the corrected annual summaries and retains their product units. For reserve $i$ and year $t$, the observed-support total is $T_{it}=m_{it}n_{it}a_i$, where $m_{it}$ is its annual mean, $n_{it}$ the valid-pixel count and $a_i$ the approximate area of a 15 arc-second cell at the latitude of the reserve's projected centroid. The spherical area approximation is $a_i=(R\pi/(180\times240))^2\cos\phi_i$, with $R=6371.0088$ km. The same cell area weights the outer 0–1 km band, and subtraction gives the remainder beyond 1 km. This remainder includes cells beyond 5 km and is distinct from the earlier 1–5 km comparison. All 4,426 eligible whole-reserve and outer-band series contain all twelve years. Residual annual totals are non-negative apart from floating-point rounding below $3\times10^{-12}$.

Ordinary least-squares slopes use centred annual values and centred years; numerical slopes below $10^{-9}$ in absolute value are treated as zero. For a fixed complete series, the fitted slope of a sum equals the sum of its fitted slopes. Independent reconstruction found maximum whole-minus-band slope discrepancies below $2\times10^{-13}$ per reserve. This identity concerns OLS contributions; it does not apply to Theil–Sen slopes. Because all budget histories are complete, no interpolation or replacement of missing annual summaries is needed.

We calculate the reserve-level gross positive contribution as $\sum_i\max(b_i,0)$, retaining $\sum_i\min(b_i,0)$ separately. For the boundary split, the denominator is instead $\sum_i[\max(b_{i,0–1},0)+\max(b_{i,>1},0)]$. Its value exceeds the reserve-level denominator if oppositely signed components cancel within a reserve before the latter is calculated. These are sums of positive fitted slopes, not positive pixel-level changes or emitted-light flux. Table S6 gives both denominators. Area shares use the approximate area of valid raster cells in 2024, retaining repeated designations; they differ from polygon-area shares and from unique land area. The national sampled-area denominator is 1,714,589.98 km², of which 234,974.69 km² lies in the outer kilometre.

The supported-interior sensitivity requires at least ten valid remainder pixels in every year, yielding 1,398 reserves. The outer band occupies 12.52% of their sampled area and supplies 51.22% of their gross positive band contributions. Among the 221 with positive whole-reserve OLS slopes, 192 have an outer-band slope exceeding half the whole-reserve slope; excluding changing-count cases gives 190 of 219. These within-reserve signed ratios can exceed one when the remainder decreases, so they are not bounded fractions of positive pixel change. The 72.00% national boundary share includes smaller reserves whose selected cells may all lie within 1 km of a boundary. It therefore describes the distribution of change across this estate rather than a geometry-independent process.

Four reserves have changing whole-reserve or outer-band valid counts: WA_13045, WA_27632, WA_33842 and WA_54225. Excluding them leaves 4,422 reserves with a 72.00% boundary share; the supported-interior subset then contains 1,395 reserves and gives 51.20%. Stable counts alone cannot establish identical pixel identities, so all totals retain an annual observed-support interpretation. Summed designation totals also count overlapping reserves separately. They are not an integral over deduplicated protected land.

Sensitivity to the cell-area approximation was assessed independently. Omitting area weights gave an outer share of 72.30%, compared with 72.00% under centroid weighting. Conservative bounds used the smallest and largest possible spherical cell areas over each reserve's latitude extent. For each annual non-negative total, the bounds were propagated through the positive and negative OLS time coefficients separately, then through positive-part sums. The resulting full-period outer share lay between 71.60% and 72.42%. These bounds assess within-reserve latitude variation, not ellipsoidal geometry, boundary error, source-product error or temporal uncertainty. Kosciuszko's interior share was 47.13% with centroid areas and 50.25% without area weighting.

Period sensitivities use OLS over 2013–2021 and the difference between mean totals for 2022–2024 and 2013–2015. The latter has product units × km², without a per-year factor. Neither sensitivity isolates processing from environmental change: the shorter period still includes the 2017 first-detection pulse, and both are calendar selections. An additional exploratory exercise subtracts the contemporaneous annual jump from all subsequent values at chosen step years. Of the 420 positive Sen slopes, 319 remain positive after removing steps in 2017 and 2023, and 254 after also removing 2020. Such subtraction can remove real change and can leave unmodelled product effects. These counts neither validate an environmental trend nor provide a lower bound on it.

To distinguish estimator effects from spatial weighting, reserve ranks compare OLS slopes of annual means with OLS slopes of integrated totals over the same years. Kosciuszko ranks 286th and first respectively; six reserves occur in both top twenties, and twelve integrated top-twenty contributors fall outside the mean-slope top hundred. Its original mean Sen-slope rank of 303 is a different estimator comparison and is not used to attribute the ranking contrast solely to weighting. Concentration curves sum positive reserve contributions, with negative contributions reported separately.

The Kosciuszko endpoint comparison uses decoded 2019 and 2024 source raster windows and centre-based CAPAD inclusion. Independent replay verified identical grids and 39,721 common-valid inside cells, with no change in valid support. Scale/offset values were 1/0 in 2019 and 10/0 in 2024; both were applied. Whole-reserve decoded sums reproduced the accepted annual means multiplied by counts to floating-point precision. The compressed window arrays, grid metadata, source URLs, access time and hashes are retained for offline replay. Positive differences are grouped with eight-neighbour connectivity; clusters are summarised by their positive-change-weighted centroids. The two largest contain 25,180 of 26,110 summed positive cell differences (96.44%), while negative differences sum to −360. Thus their share of positive differences differs from their share of the net difference. Both clusters contain only zero product values in 2019. These endpoint quantities are unweighted sums of decoded cell values, separate from the area-integrated trend budget. Locations were compared with the official Lobs Hole and Tantangara monitoring-site descriptions and construction chronology [@snowymonitor2025; @snowybooklet2020; @snowysummer2020]. The comparison supports proximity to documented works, not attribution of each pixel or ecological impact.


The review-stage tercile comparison ranked the 420 positive Sen slopes, divided them into three equally sized groups and summed their polygon areas. These descriptive divisions have no ecological-effect interpretation. Classifying whole polygons by their Sen-slope signs assigned 37.6% of eligible area to positive trends, although the lowest third of positive slopes accounted for 99.1% of that class's area (Table S4). Such polygon shares do not estimate the area that brightened; the additive budget instead measures contributions over sampled pixels.

A review-stage check stratified Kosciuszko's positive 2019–2024 pixel differences by their decoded 2024 values (Table S8). All 39,721 common-valid cells entered the comparison; the denominator is the sum of positive endpoint differences across the whole park, without cell-area weighting. Thresholds are descriptive multiples of the ten-unit recorded floor, not physical or ecological thresholds. Most brightening cells ended at the floor, but high-value cells supplied most of the positive change. The VNL V2 method constructs the background mask from neighbourhood data range and cloud-free coverage, then applies it to average radiance [@elvidge2021]. The smallest retained encoded value therefore does not bound the unmasked radiance of cells recorded as zero. This check separates high-value contributions from faint detections; it cannot independently rule out masking or other product effects.

### S5. Influential decreases and industrial-site context

The five most negative whole-reserve integrated OLS slopes for 2013–2024 identified Barrow Island, Murujuga, Strzelecki, Thevenard Island and Newlands (Table S7). We excluded this fixed set from both full-period and 2013–2021 sums, then additionally excluded Kosciuszko to check whether the remaining positive balance depended on its large increase. Selection followed inspection of the full-period outcomes; these are influence diagnostics, not independent confirmation or corrected national estimates. The three industrial-context examples rank first, second and fourth. We assign no common operational explanation to all five.

Independent bounded raster reads compared 2015 with 2016 at Barrow Island and 2013 with 2024 at Murujuga, Thevenard Island and Strzelecki. Integer covering windows used floor-rounded starts and ceiling-rounded stops to include every centre-selected CAPAD cell. Each pair had identical grids, applied scale and offset, and used common-valid support: 1,263 cells for Barrow, 259 for Murujuga, 110 for Thevenard and 43,238 for Strzelecki. No endpoint-only valid cells occurred. Decoded sums and counts reproduced the accepted annual summaries. A preliminary rounded crop omitted one Barrow cell, one Thevenard cell and 46 Strzelecki cells; all were zero at both endpoints, so correcting the windows changed support counts but not sums or clusters. Retained arrays, source URLs, window coordinates, metadata and hashes permit offline replay.

Positive and negative endpoint differences were clustered separately with eight-neighbour connectivity. We report clusters with absolute summed change of at least 200 product units, but same-sign denominators include every changed cell. Barrow's largest positive cluster contained 144,300 of 144,440 positive differences (99.90%); negative differences elsewhere summed to −11,950. Its share therefore exceeds 100% of the net increase and must not be described as a net-change share. Murujuga's dominant negative cluster contained −63,070 of −65,570 negative differences (96.19%), while other cells increased by 20. Thevenard's −3,370 endpoint change lay in one cluster. These unweighted endpoint sums concern selected intervals; they are not spatial decompositions of the full-period OLS decrease. Figure S7 shows the annual histories, including rebounds and product zeros.

Primary documents establish geographic and chronological context. Barrow Island is a Class A Nature Reserve; Gorgon construction began in December 2009 and first LNG production was announced in March 2016 [@wagov2016; @chevron2016]. The positive-change cluster centre is approximately 1.1 km from documented onshore pipeline endpoints within Gorgon's gas-treatment plant [@chevrongorgon2015]. Murujuga's dominant negative-change cluster centre is approximately 1.3 km from the Karratha Gas Plant location point in a government record [@dcceewkgp2025]. Woodside subsequently reported 2025 flaring below 10% of its 2013 peak [@woodside2026]; that observation is outside our study period and cannot establish the cause of the 2013–2024 satellite decrease.

Thevenard's operator plan identifies Nature Conservation Reserve 33174 and an industrial lease at its northeastern end [@chevronthevenard2014]. A 2006 botanical collection locality described as near the oil camp and plant lies approximately 340 m from the negative-change cluster centre [@maslin2007]. Production ended in 2014 and completed onshore decommissioning was announced in June 2023 [@chevron2023]. The satellite series nevertheless returned positive values in 2018 and 2019 after zeros in 2016 and 2017. It supplies no permanent lights-off date. Distances use rounded cluster centres and documented reference points, not surveyed flare positions or facility boundaries. Geographic proximity and operational histories motivate source investigation without identifying individual lamps, flares, physical darkness or ecological effects.


### S6. AI systems, contributions and retained provenance

AI systems acted as research collaborators under Barry W. Brook's scientific direction. They contributed to study planning, implementation, analysis, source retrieval, numerical and spatial checks, figures, drafting and criticism. The available records identify the following models and periods; model agreement was not a validation criterion.

- **OpenAI Codex CLI, GPT-5:** the 1 January 2026 bootstrap log records this model label for environment setup, project scaffolding and initial study planning. It does not identify a more specific backend variant or attribute the whole early pipeline to that model.
- **OpenAI Codex, `gpt-5.5`:** retained project-session metadata assign this model to an environment/bootstrap session created on 6 March 2026 and a manuscript expansion/formatting session created on 15 May. Their registered conversation files are no longer present, so these assignments do not establish the model used on every turn or a complete history of the intervening work.
- **OpenAI Codex, `gpt-5.6-sol`:** retained task metadata identify September methods orientation, audit-design review, product-lineage review, coastline-source selection and spatial-protocol checks. These bounded tasks occurred on 12, 17 and 19 September.
- **OpenAI Codex, `gpt-5.6-luna`:** retained task metadata identify figure revision, interior-band checks, Layer B code repairs, release-input reconciliation, corrected-audit orchestration and figure/table integration on 12, 17 and 19 September. The Layer B numerical results were subsequently omitted from this candidate because the original occurrence inputs were unavailable for verification.
- **OpenAI Codex, `gpt-6-astra`:** parent-session records identify this model for September–October analysis integration, spatial correction, source and numerical checks, figures and manuscript revision. Separate reviews used the same model, including a fresh adversarial review on 18 September and correction acceptance on 19 September. Retained October delegated-session records also name this model. Independent numerical implementations and source checks are distinguished from judgments by another instance of the same model.
- **Anthropic Claude Fable 5.1, `claude-fable-5-1`:** Claude reports use on 14–18 September for independent scientific review, product-continuity audit design, review of the interior-band and area results, and scientific close-out.
- **Anthropic Claude Opus 5.5, `claude-opus-5-5`:** Claude reports use from 28 September for prose revision and checkpoints, and on 18–19 October for the additive change budget, site-cluster analysis, candidate figures and manuscript critique. Commit trailers corroborate this model label, but the stated transition date and earlier Fable identity rely on Claude's report rather than independently inspected Anthropic session metadata.

This inventory describes recoverable records, not an exhaustive model assignment for every historical turn. The exact early GPT-5 variant, complete January–early September history and model identity of an earlier ChatGPT review workflow could not be recovered. Known dates, task assignments and evidence sources are retained with the project provenance. Missing identifiers are not inferred from current tool configuration. Human declarations and final author approval remain to be completed before submission.

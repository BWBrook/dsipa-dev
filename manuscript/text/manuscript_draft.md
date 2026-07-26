# Detectable change in dark-sky integrity across Australia’s protected areas

## Abstract

Artificial light at night (ALAN) can cross protected-area boundaries, but national assessment is constrained by what satellite products can detect and by the observation processes represented in biodiversity databases. We used annual VIIRS night-lights (2013-2024) to assess detectable upward radiance inside Australian protected areas, in surrounding unprotected land, and, where spatial support permitted, across interior distance bands.

Of 11,133 protected areas, 4,426 (39.8%) met conservative pixel and temporal eligibility rules. Within this evaluable subset, 3,844 (86.9%) had zero inside mean radiance in 2024 and 3,969 (89.7%) had exactly zero Theil-Sen slopes; 420 (9.5%) had positive slopes. Among 3,858 areas with eligible inside and 1 km unprotected-land trends, categorical screening identified 305 with concurrent brightening and 190 with surrounding brightening but no detectable inside brightening. Dependence-aware bootstrap summaries showed that fine ordering within the brightening tail was uncertain, while interior-ring results were conditional on the small subset with sufficient spatial support.

A secondary, provider-matched analysis tested whether ALAN covariates distinguished microbat from passerine occurrence records. Out-of-block discrimination was weak (AUC 0.545), and provider matching could not align the groups' different observation processes. ALAN-shuffle analyses supplied illustrative benchmarks but did not identify the cause of the observed association. The primary contribution is therefore a detectability-aware framework for categorical screening of protected-area radiance change. It reveals widespread non-detection alongside concentrated, management-relevant internal and surrounding change, while showing why opportunistic records alone cannot establish the associated biological response.

## Keywords

artificial light at night; protected areas; VIIRS; remote sensing; conservation monitoring

---

## 1. Introduction

Artificial light at night (ALAN) is a growing component of human disturbance. It alters the nocturnal environment and can affect behaviour, physiology, species interactions, and ecosystem processes [@longcore2004; @gaston2013; @hirt2023]. Global indicators show increasing extent and brightness of night-time lighting, although trends differ among satellite, ground-based, and human-observer measures because they detect different parts of the light environment [@kyba2017; @kyba2023; @sanchezdemiguel2021; @bara2025]. For conservation, ALAN is especially important because light and skyglow cross legal boundaries: protected tenure does not isolate an ecosystem from nearby development or lighting.

ALAN has increased within and around protected and conservation-priority areas [@gaston2015; @guette2018; @garrett2020; @mu2021], but operational national monitoring faces two linked problems. First, annual night-lights products are floor dominated in low-radiance landscapes. A zero can indicate stable low upward radiance or change below product detectability; it is not a direct observation of ecological darkness. Second, a geometric buffer can contain ocean or another protected area, obscuring the surrounding unprotected-land conditions most relevant to cross-boundary management. Eligibility, censoring, and buffer definition therefore affect which protected areas can be assessed and how their change should be interpreted.

These measurement choices also determine whether an output is useful to managers. Detectable brightening within a protected area presents a different diagnostic problem from detectable brightening confined to surrounding unprotected land. The former may warrant examination of facilities, roads, visitor infrastructure, or diffuse skyglow; the latter may focus attention on adjacent development and cross-boundary lighting governance. Neither pattern identifies a cause on its own. A national assessment should therefore sort areas into interpretable evidence categories and carry measurement uncertainty forward, rather than collapse several mechanisms into a single vulnerability score.

Satellite night-lights provide consistent national coverage, but upward radiance is not equivalent to organism-experienced illumination or sky brightness [@falchi2016]. Sensor spectral response, atmospheric propagation, and changing lighting technologies, including LEDs, further separate satellite measurements from ecological exposure [@lewanzik2017; @levin2025; @bara2025]. A defensible dark-sky integrity assessment must consequently state its measurement scale, expose non-detection, and avoid treating a floor-dominated time series as fully observed continuous change.

Linking remotely sensed exposure to biodiversity response is harder still. Microbats are biologically relevant nocturnal and insect-associated surrogates because artificial lighting can alter bat commuting and foraging [@stone2009; @stone2015; @threlfall2013; @linley2016; @haddock2019]. Yet microbats are often detected with specialist or acoustic equipment, whereas passerine records commonly arise from different survey and reporting practices. Opportunistic occurrence data also reflect access, observer effort, spatial clustering, and provider-specific protocols [@phillips2009; @fithian2015; @roberts2017; @baker2024]. Matching provider identity cannot make these observation processes equivalent.

We present a two-layer assessment of dark-sky integrity across Australia's protected areas. Layer A, the primary contribution, quantifies detectable ALAN inside protected areas, compares inside trends with corrected surrounding unprotected-land trends, and reports uncertainty and feasibility. Its management output is categorical screening rather than precise priority ranking. Layer B asks a narrower question: can ALAN covariates distinguish microbat from passerine occurrence records under provider matching, spatially blocked evaluation, and null benchmarks? Together, the layers separate what annual satellite observations can support about exposure from what opportunistic biodiversity records cannot establish about biological response.

Specifically, we asked four questions. What fraction of protected areas can be assessed reliably at 500 m annual resolution, and how many eligible areas have detectable inside radiance? Where is change detectable during 2013-2024? How do inside trends compare with trends in adjacent unprotected land, and how stable is fine ordering within the brightening tail? Finally, do ALAN covariates provide out-of-block discrimination between microbat and passerine records once provider identity is matched, and what do structured shuffle benchmarks reveal about the information in that association? This sequence keeps the national exposure assessment separate from the more limited test of biological-record discrimination.

The design therefore treats measurement support, environmental pattern, management screening, and biological inference as related but distinct questions with progressively narrower evidential reach.

---

## 2. Materials and Methods

### 2.1 Study design

Layer A assessed three quantities for Australian protected areas: detectable annual VIIRS radiance inside each area, radiance in surrounding unprotected land, and temporal change during 2013-2024. The protected area was the analytical unit, with annual measurements repeated through time. Inference was conditional on explicit pixel and temporal eligibility rules.

We operationalised dark-sky integrity as low or non-increasing upward radiance detectable in the annual VIIRS product. This is a remote-sensing condition metric, not a measurement of ground-level illumination, sky brightness, or biological response. We also examined boundary-to-interior bands where their raster support was sufficient, but treated these as selected diagnostics rather than a national estimand.

Layer B was secondary. Its analytical unit was an occurrence record, and its binary response was record identity: microbat (1) or passerine (0). The model tested whether ALAN covariates discriminated between the two record groups. It did not estimate abundance, occupancy, demographic change, or an ALAN effect on bats.

All distance and area calculations used the Australian equal-area projection EPSG:3577.

### 2.2 Protected areas, bioregions, and night-time lights

Protected areas came from the 2024 Collaborative Australian Protected Areas Database (CAPAD). Polygons were dissolved by stable protected-area identifier (`PA_ID`), invalid geometries were repaired, and area and perimeter descriptors were calculated. The Interim Biogeographic Regionalisation for Australia (IBRA7) supplied spatial strata for Layer A resampling and Layer B diagnostics.

Processing retained one geometry per protected-area identifier so annual raster summaries, trends, and screening categories shared a consistent unit. Geometry descriptors were used to diagnose which areas had sufficient raster support; they were not treated as causal predictors in the manuscript analyses. Protected areas were assigned to their dominant IBRA region for the clustered uncertainty analysis. Occurrence records were assigned to IBRA by location for the stratified Layer B benchmark and descriptive regional fits.

We used annual VIIRS day-night band composites for 2013-2024 [@elvidge2021]. Stored raster values were converted with each GeoTIFF's scale and offset metadata, including the documented metadata changes in 2022-2024. Zeros were retained as the annual product's non-detect/floor regime rather than smoothed or imputed.

The annual raster corresponding to each observation year was used throughout. We did not interpolate between years or substitute a later annual layer for missing measurements. Temporal quality control compared national annual summaries and checked the years around metadata scaling changes. The analysis concerns the radiance represented by these annual composites; it does not convert radiance to ground illuminance or model atmospheric skyglow.

### 2.3 Layer A spatial summaries and eligibility

For every protected area and year, we summarised inside radiance using the mean (primary metric), median, fraction of valid pixels greater than zero (`frac_gt0`), and 95th percentile. The latter summaries helped describe a distribution dominated by zeros.

Mean radiance was selected before trend interpretation as the primary intensity measure. Median radiance, `frac_gt0`, and the 95th percentile distinguish different aspects of the floor-dominated distribution but were not substituted post hoc to select stronger trends. Pixel counts and missing values travelled with each zone-year summary so eligibility could be reconstructed.

We generated 1 and 5 km outward buffers and evaluated three definitions: the raw geometric buffer, the buffer intersected with a land mask, and the land buffer after removing overlap with all protected areas. The last, termed the unprotected-land buffer, was the primary surrounding comparison. It avoids treating ocean or adjacent protected tenure as the unmanaged surrounding landscape, although its radiance trend remains a spatial proxy rather than evidence about a particular development or governance process.

Land and protected-area overlap fractions were recorded for buffer validity. A buffer-year estimate was retained only when its masked geometry contained at least 10 valid pixels. We focused management interpretation on the 1 km unprotected-land buffer because it represents the nearest surrounding landscape while satisfying the accepted feasibility rule; the 5 km result remained a broader contextual measure. Buffer construction did not imply that light originated within the buffer or stopped at its edge.

Interior bands covered 0-1, 1-5, and 5-10 km from the boundary. For every protected-area, buffer, or band summary in a year, at least 10 valid 500 m pixels were required. Values failing this rule were missing. Inside trend estimation additionally required at least eight valid years. These rules reduce unstable small-polygon estimates but make the assessed subset non-random with respect to protected-area size and shape.

Bands were defined inward from each boundary and evaluated separately by year. The complete-band summary used only protected areas meeting the pixel rule in all three bands in 2024. Because this selects larger or spatially suitable geometries, it was used to test feasibility and describe conditional `frac_gt0` patterns, not to estimate a national edge effect.

### 2.4 Trends, categorical screening, and uncertainty

We estimated monotonic 2013-2024 trends with Theil-Sen slopes, using mean radiance as the primary metric and the other metrics for interpretation. For protected areas with eligible inside and surrounding 1 km unprotected-land slopes, we defined four descriptive screening categories:

1. concurrent brightening: inside slope > 0 and surrounding slope > 0;
2. inside-only brightening: inside slope > 0 and surrounding slope <= 0;
3. stable/non-detect: inside slope <= 0 and surrounding slope <= 0; and
4. surrounding-only brightening: inside slope <= 0 and surrounding slope > 0.

These categories identify different patterns for investigation; they neither rank management priority nor attribute cause.

We also calculated the inside-minus-surrounding slope difference as a descriptive contrast. Its sign and magnitude help describe whether detectable change is stronger inside or outside, but do not identify direction of light propagation. Category membership was based only on slope signs and the stated eligibility rules; no significance threshold was tuned to increase the number of flagged sites.

To examine uncertainty in the brightening tail, we resampled IBRA regions as spatial clusters and years in moving blocks of length three, recomputing Theil-Sen slopes over 300 replicates. We reported bootstrap medians, 95% intervals, and empirical fractions of replicates with slope > 0. A pairwise dominance summary assessed how reliably estimates were ordered within a selected high-slope set. These are resampling summaries, not posterior probabilities.

Clustering by IBRA retained broad spatial dependence, while moving blocks retained short temporal sequences better than independent-year resampling. The procedure evaluates sensitivity of estimated slopes and ordering to this resampling design; it does not capture all uncertainty in raster measurement, protected-area boundaries, or model specification. Screening sets were consequently interpreted with their intervals and replicate frequencies rather than as a definitive ordering.

### 2.5 Layer B occurrence records and exposure

Atlas of Living Australia records from 2013-2024 were filtered for coordinate and metadata quality, excluding coordinate uncertainty above 1 km. We retained microbats (Chiroptera excluding Pteropodidae) and passerines (Passeriformes), with at most one record per 1 km grid cell, day, and taxon group. Records were classified as inside a protected area, within 10 km, or farther away; modelling used records inside or within 10 km.

The two groups were selected for contrast, not because passerines constitute absences for microbats. Deduplication reduced repeated reporting at popular locations but did not estimate observer effort. A provider-level licence ledger was retained because ALA combines records under heterogeneous terms. The manuscript and release-facing evidence therefore use counts, summaries, coefficients, and figures rather than redistributing occurrence rows.

Annual VIIRS radiance was extracted for each record and represented by `any_light` (radiance > 0) and `log1p_alan` (log-transformed intensity for lit locations, zero otherwise). This two-part form separated detectable light from intensity conditional on detection.

The occurrence year determined the annual raster, so exposure was temporally aligned at annual resolution. This remains an exposure value at a reported location, not a measure of an individual's movement, foraging history, or experienced illumination. Records farther than 10 km from protected areas were retained for descriptive exposure summaries but excluded from the protected-area-adjacent model.

### 2.6 Layer B modelling and null benchmarks

We fitted balanced logistic regressions predicting microbat-versus-passerine record identity from `any_light` and `log1p_alan`. Evaluation used five-fold GroupKFold cross-validation on 50 km spatial blocks [@roberts2017]. The primary dataset restricted both groups to NSW BioNet (`dr368`), the dominant microbat provider; the all-provider fit was descriptive sensitivity analysis.

Balancing fixed equal class sizes, making discrimination metrics comparable but severing the fitted intercept from population prevalence. We summarised fold-specific coefficients by their mean and SD and reported out-of-fold area under the receiver-operating curve (AUC) and log loss. AUC describes classification discrimination, not effect magnitude or ecological importance.

Provider matching reduced one source of heterogeneity but did not control observation protocol, acoustic-detector use, accessibility, habitat, geography, or taxon-specific detectability. Spatial blocking reduced leakage from nearby records but did not remove these differences.

We compared the fitted association with two shuffle benchmarks produced by rearranging ALAN values within spatial blocks and within IBRA-by-year strata. Each benchmark was one deterministic seeded realisation used illustratively, not a sampled null distribution. Each rearrangement broke the observed exposure-label pairing while retaining aspects of spatial or bioregional structure. Attenuation is expected whenever the original pairing contains information, whether biological or observational, and therefore does not diagnose its cause. Descriptive within-IBRA fits were restricted to regions with at least 500 records per class.

The block shuffle rearranged ALAN among records sharing a broad spatial block, whereas the IBRA-by-year shuffle preserved bioregional and annual exposure context. Neither was a randomised ecological experiment or supplied a causal counterfactual for bat response. Their role was to show how much discrimination remained after the observed pairing was disrupted.

### 2.7 Reproducibility

Layer A was implemented and retained internally as a versioned, scripted, and tested Python pipeline with schema-controlled outputs, pinned source identities, deterministic serialization, and run manifests. Input provenance, checksums, software details, and validation records are preserved in the private repository.

National Layer A computation was statewise and merged under stable keys. The accepted reference contract validates source identities, schemas, row and key constraints, and frozen headline values before report generation. Manuscript figures and tables were generated from these accepted outputs. Public access is currently limited to the processed Layer A outputs in the Zenodo Dataset cited below; source code, the complete runnable environment, and derived Layer B materials are not yet available through a citable public software release. Exact Layer B reconstruction also requires reacquisition of ALA records under their provider terms; raw and row-level occurrence records are not redistributed.

---

## 3. Results

### 3.1 Eligibility and detectable baseline radiance

The CAPAD universe contained 11,133 protected areas. Of these, 4,426 (39.8%) met both the 2024 minimum-pixel rule and the minimum-years rule for inside trend estimation (Table 1). Consequently, national statements about inside radiance are conditional on an evaluable subset that favours areas with sufficient 500 m raster support.

Eligibility for the 1 km unprotected-land comparison was lower: 3,858 areas had both inside and surrounding trends. The corresponding 5 km unprotected-land trend was available for 3,992. These changing denominators arise from masking, overlap removal, raster support, and temporal completeness, and are reported separately rather than treating every result as if it covered the full CAPAD universe.

Within that subset, 3,844 of 4,426 protected areas (86.9%) had inside mean radiance equal to zero in 2024 (Fig. 1). Non-zero values were concentrated near developed coastal, urban, and peri-urban regions. This pattern indicates widespread non-detection by the annual composite, not verified absence of ecological light.

Spatial support declined strongly with interior distance. In 2024, the 0-1 km band was valid for 4,425 protected areas (39.7%), the 1-5 km band for 1,432 (12.9%), and all three bands for 383 (3.4%). Among the 383 complete-band areas, boundary-adjacent bands more often contained detectable pixels than deeper bands, but medians were zero throughout. The band pattern is therefore a selected, floor-dominated diagnostic rather than a national gradient (Fig. S1).

Within the complete-band subset, conditional non-zero shares were 18.02% in the 0-1 km band, 9.40% at 1-5 km, and 3.66% at 5-10 km. The declining shares are compatible with boundary-associated detectable radiance in these selected areas, but heavy non-detection and geometry selection preclude generalisation to the national protected-area system.

### 3.2 Detectable change inside protected areas

Inside mean-radiance slopes were exactly zero for 3,969 of 4,426 eligible protected areas (89.7%). Positive slopes occurred in 420 (9.5%); the complete non-zero subset contained 457 because it also included negative slopes (Fig. 2). The zero mass combines stable low radiance with possible changes below product detectability and cannot separate them.

The 457 non-zero slopes were right skewed, with median 0.098 radiance units per year (interquartile range 0.0075-0.4164). Across all eligible areas, the mean slope was 0.0283 (SD 0.295), but this average was dominated by the zero mass. National annual summaries showed no discontinuity after applying file-specific scale and offset metadata, including across the 2022-2024 metadata change.

Bootstrap results supported a distinct high-slope tail but not precise ordering throughout it. Some high-slope areas had consistently positive bootstrap distributions, whereas intervals overlapped and pairwise ordering was ambiguous for many others (Figs S2-S3; Table S1). We therefore retained screening categories and uncertainty summaries rather than interpreting fine position within an ordered list as management priority.

The selected screening set included areas with high inside slopes, positive surrounding slopes without positive inside slopes, and large inside-minus-surrounding contrasts. Their uncertainty differed markedly: some inside-slope intervals were wholly positive, whereas others spanned zero. This variation supports individual follow-up but not a uniform confidence label across all displayed sites.

### 3.3 Inside and surrounding unprotected-land change

Eligible inside and 1 km unprotected-land trends were available for 3,858 protected areas. Most were stable/non-detect inside and outside (Q3: 3,308; 85.7%). Concurrent brightening occurred in 305 (Q1: 7.9%), inside-only brightening in 55 (Q2: 1.4%), and surrounding-only brightening in 190 (Q4: 4.9%) (Fig. 3).

Thus 495 protected areas had a positive surrounding unprotected-land slope, including both concurrent and surrounding-only categories. This comparison identifies where a protected area and its surroundings differ in detectable change. It does not establish the lighting source, ecological exposure, or management cause, but it provides a categorical screen for site-level investigation.

The categorical structure also shows why inside trends alone are incomplete. The 190 surrounding-only cases would not be identified by an inside-brightening screen, yet their adjacent landscapes changed detectably. Conversely, the 55 inside-only cases require different scrutiny because the nearest unprotected-land summary did not brighten. The four categories retain these distinctions without combining incommensurate signals into a single score.

### 3.4 Occurrence-record discrimination

The provider-matched Layer B model used 50,281 microbat and 50,281 passerine records. It estimated a positive `any_light` coefficient (mean 1.316, fold SD 0.128) and negative conditional-intensity coefficient (mean -0.354, fold SD 0.024), but out-of-block discrimination was weak (AUC 0.545; log loss 0.689; Fig. 4; Table S2).

Before provider matching and balancing, filtering and deduplication retained 63,716 microbat and 2,378,378 passerine records. Microbat records were strongly concentrated in NSW BioNet (88.8%), motivating the restricted primary comparison. Within the protected-area-adjacent scope, both record groups showed substantial zero-valued exposure, and exposure distributions varied strongly between inside and within-10-km strata (Figs S4-S6). These patterns describe the observation records, not taxon prevalence.

The single seeded spatial-block shuffle yielded AUC 0.505 and a conditional-intensity coefficient of -0.027; the single seeded IBRA-by-year shuffle yielded AUC 0.517 and a coefficient of -0.001. These illustrative realisations are not a sampled null distribution. The primary AUC was only modestly higher, quantifying limited discrimination without identifying whether the original association was ecological or observational. The all-provider sensitivity had AUC 0.557 but restored substantial provider and geographic heterogeneity. Supporting Information reports occurrence volumes, exposure distributions, spatial clustering, and descriptive IBRA variation (Figs S4-S7).

Provider-matched within-IBRA fits were feasible in 11 regions and varied in sign and magnitude (Fig. S7). Given the weak national discrimination and unresolved observation processes, this heterogeneity was descriptive. It did not support regional ecological-effect estimates.

---

## 4. Discussion

### 4.1 Detectable dark-sky integrity is widespread but incompletely observed

The dominant Layer A result is widespread non-detection of change at the annual VIIRS product scale. Among protected areas with sufficient spatial and temporal support, 86.9% had zero inside mean radiance in 2024 and 89.7% had exactly zero slopes over 2013-2024. These observations are consistent with low detectable upward radiance across much of the evaluable system, while a smaller tail shows measurable brightening.

This conclusion is deliberately narrower than saying that most protected areas are dark or unchanged. VIIRS observes upward radiance rather than ground-level illumination or sky brightness, has limited sensitivity in low-radiance landscapes, and responds differently to lighting spectra [@falchi2016; @kyba2023; @levin2025; @bara2025]. A zero annual value is therefore a monitoring category, not proof of ecological darkness. Moreover, only 39.8% of the CAPAD universe met the primary eligibility rules. Small and narrow protected areas are under-represented, so percentages for the eligible subset cannot be transferred to all 11,133 areas.

These constraints are part of the result rather than peripheral caveats. The assessment makes eligibility visible, preserves the floor mass, and reports alternative distributional summaries instead of forcing continuous trends from non-detect values. It thereby defines what annual VIIRS can monitor reproducibly and where finer-resolution or ground-based measurement is needed.

The resulting pattern is compatible with earlier evidence that protected areas are generally less exposed than developed surroundings while some conservation lands experience increasing ALAN [@gaston2015; @guette2018; @garrett2020; @mu2021]. Our addition is not a claim that Australia is uniquely affected. It is an operational treatment of the low-radiance regime: one protected-area universe, explicit result-specific denominators, corrected surrounding zones, and uncertainty that travels with the screening output.

Temporal comparability also requires caution. File-specific scale and offset metadata removed an obvious source of discontinuity, but annual composites still integrate atmospheric conditions, ephemeral lighting, spectral change, and upstream processing. The Theil-Sen estimator limits sensitivity to individual annual outliers; it cannot recover changes that the product never detects or distinguish lighting technology from total radiance change.

### 4.2 Surrounding-land change supports categorical management screening

The corrected unprotected-land comparison is the most directly management-facing component. Raw buffers can be diluted by ocean or include neighbouring protected tenure; removing both produces a more interpretable measure of detectable change in the adjacent unprotected landscape. Among areas with eligible paired trends, 305 showed concurrent inside and surrounding brightening and 190 showed surrounding brightening without detectable inside brightening. These categories identify different questions for local investigation.

They are not causal diagnoses. Surrounding brightening does not by itself identify a development, lighting installation, governance failure, or organismal exposure. Likewise, concurrent brightening does not establish that outside lighting caused inside change. The screening output should trigger examination of local infrastructure, lighting design, development approvals, terrain, and ground-based sky brightness rather than determine priority by numerical rank.

This distinction matters for action. A surrounding-only screen may lead an agency to examine municipal lighting plans, roads, industrial facilities, or development applications near a boundary. Concurrent brightening may additionally motivate inspection of infrastructure within the protected area and the spatial extent of skyglow. Inside-only brightening may flag local facilities or a mismatch between the 1 km zone and the true source area. Stable/non-detect sites remain candidates for stewardship, but their category should not be read as proof that biologically relevant light is absent.

Bootstrap uncertainty reinforces that use. The analysis supports a concentrated brightening tail, but many fine pairwise orderings are unstable under dependence-aware resampling. Management decisions should therefore rely on broad categories, effect magnitude, uncertainty, feasibility, and local conservation context, not whether a reserve occupies a particular position in a national list.

Interior bands provide less general evidence. Only 383 protected areas supported all three bands, and zero-dominated conditional summaries cannot establish a national boundary-to-interior process. Retaining this result as a selected diagnostic is useful because it exposes the spatial-resolution limit rather than converting a small, geometry-selected subset into a general claim.

### 4.3 The exposure-to-biological-response bridge remains unresolved

Layer B does not demonstrate a microbat response to ALAN. Weak out-of-block discrimination means its two ALAN covariates provided little information about occurrence-record identity. Biological and observational explanations remain inseparable.

Microbats were a biologically motivated surrogate: they are nocturnal, many depend on insect prey, and controlled or local studies show species- and context-dependent responses to lighting [@stone2009; @stone2015; @threlfall2013; @haddock2019]. They are also difficult to census opportunistically. Specialist acoustic detectors, targeted surveys, and expert identification generate a different detection process from typical passerine records. Restricting both groups to one provider reduces provider mixing but does not align protocol, effort, habitat coverage, access, geography, or detectability.

Each shuffle analysis was one illustrative seeded realisation rather than a sampled null distribution. Breaking the exposure-label pairing reduced coefficients and discrimination, but that attenuation neither validates a biological mechanism nor proves confounding. Weak predictive performance and the uncontrolled observation process prevent attribution.

This negative inferential result is useful for remote-sensing ecology. Satellite exposure layers can be spatially comprehensive while biological records remain opportunistic and taxon specific. A stronger bridge would require repeated acoustic surveys or other standardised detection data, explicit effort and habitat covariates, and occupancy or activity models matched to the sampling design. Until then, Layer B is an assessment of data adequacy, not evidence for population change or absence of an ALAN effect.

Passerines are a high-volume diurnal comparison group, not an ecological counterfactual for where microbats would be recorded without ALAN. Habitat and reporting differences can create record-label discrimination without a biological light effect, while pooled microbats average taxa that may avoid, tolerate, or exploit lit environments. These limits preclude ecological interpretation of the coefficients; they do not imply that ALAN is unimportant to bats.

### 4.4 Limitations

Four limitations define the scope of inference. First, the annual VIIRS product measures upward radiance at approximately 500 m support, not ground illumination, spectral composition, glare, or sky brightness experienced by organisms. Its zero mass combines true low radiance with below-detection change.

Second, eligibility is selective. Only 4,426 protected areas support the main inside assessment, 3,858 support the paired 1 km comparison, and 383 support complete interior bands. The study provides national coverage of assessment feasibility, but its radiance percentages describe eligible subsets rather than every protected area.

Third, slope signs are descriptive. They summarise monotonic change over 12 annual observations but do not attribute source, mechanism, or ecological consequence. The bootstrap represents spatial-cluster and short-block resampling uncertainty; it does not propagate all measurement, geometry, or product uncertainty.

Fourth, Layer B is presence-only, case-control, provider-bounded, and taxonomically aggregated. Its response is occurrence-record identity, its intercept is altered by balancing, and neither provider matching nor spatial blocking controls the full observation process. It cannot estimate abundance, occupancy, population trend, population decline, causal effect, or a national biodiversity response.

### 4.5 Conservation implications and conclusions

Dark-sky integrity can be treated as a measurable protected-area condition only if the metric's detection limits remain visible. At annual VIIRS resolution, most evaluable Australian protected areas showed no detectable inside radiance change, while measurable change was concentrated in a minority and often involved surrounding unprotected land. This supports a practical monitoring sequence: screen protected areas categorically, retain uncertainty and eligibility information, and investigate flagged sites with local lighting and ground-based evidence.

The assessment defines a stable protected-area unit, annual products, explicit eligibility, and repeatable categories that agencies could apply as later compatible inputs become available. Such repetition is valid only if changes in CAPAD geometry and night-lights product identity are documented and not mistaken for environmental change. The current 2013-2024 result should therefore be treated as a baseline assessment, not silently extended with incompatible annual products.

The integrated contribution is not a claim that satellite radiance measures biodiversity response. It separates two decisions: where detectable protected-area and surrounding-land change warrants attention, and whether available biological observations can test the ecological consequence. Layer A answers the first at national scale within explicit measurement limits. Layer B shows that opportunistic microbat and passerine records do not yet answer the second.

---

## Data accessibility

Layer A uses public inputs whose provenance and checksums are documented internally. Nine processed Layer A outputs are archived as a Zenodo Dataset under CC BY 4.0 [@brook2026dsipa]. The DOI is https://doi.org/10.5281/zenodo.21524637. This Dataset is not a software release: source code, the complete runnable environment, provenance records, and derived Layer B summaries and figures remain private. Raw and row-level ALA occurrence records have mixed provider terms and are not redistributed; exact Layer B reconstruction requires reacquisition from ALA under those terms.

## Declarations

### Funding

No specific funding.

### Authors' contributions

`[BARRY CONFIRM: author contributions]`

### Acknowledgements

`[BARRY CONFIRM: acknowledgements]`

### Conflict of interest

`[BARRY CONFIRM: conflicts of interest]`

### Ethics and consent

`[BARRY CONFIRM: ethics/consent applicability and exact statement]`

### Use of AI

`[BARRY CONFIRM: exact AI-use disclosure]`

### Author approval and sole submission

`[BARRY CONFIRM immediately before submission: all-author approval and sole submission]`

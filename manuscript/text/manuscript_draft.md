# Measuring the erosion of darkness in Australian protected areas: satellite trends, buffer pressure, and falsification-based biodiversity inference

## Abstract

Artificial light at night (ALAN) is a rapidly expanding environmental pressure that can affect biodiversity and ecosystem processes, including within protected areas via cross-boundary spill and skyglow. Yet national-scale, reproducible assessments of "dark-sky integrity" remain uncommon, and inference is complicated by sensor detectability limits and the strong spatial dependence of lighting. We present a two-layer, uncertainty-aware audit for Australia using annual VIIRS night-lights (2013-2024) and national protected-area polygons.

In Layer A, we quantified ALAN inside protected areas, in surrounding buffers designed to represent unprotected land pressure, and, where feasible, along boundary-to-interior gradients. Detectability constraints were substantial: only 4,426 of 11,133 protected areas (39.8%) met a conservative minimum-pixel rule for stable inside estimates, and within this eligible subset inside-area mean radiance in 2024 was strongly zero-inflated, with approximately 87% in the non-detect regime. Trends in inside-area radiance were dominated by exactly zero slopes, at approximately 90%, but a minority tail of protected areas showed measurable brightening. An IBRA-clustered bootstrap revealed that only a subset of the highest-slope protected areas remained clearly separable under dependence-aware resampling, underscoring the need to report uncertainty alongside prioritisation lists. Comparing inside trends to trends in surrounding unprotected land identified a substantial subset of reserves experiencing increasing external pressure without detectable interior brightening.

Layer B implemented a deliberately conservative occurrence-based signal test for nocturnal biodiversity, contrasting microbat and passerine records under provider matching, spatial blocking, and falsification, including IBRA x year shuffles. ALAN covariates showed only weak discrimination (AUC approximately 0.55) and strong falsification sensitivity, indicating that any biodiversity-linked signal in opportunistic occurrence records is modest and potentially confounded. Together, the analyses provide a reproducible framework for auditing ALAN exposure in protected areas while explicitly surfacing feasibility constraints, censoring, and uncertainty.

## Keywords

artificial light at night (ALAN); protected areas; night-time lights (VIIRS); light pollution; skyglow; buffer zones; edge effects; IBRA bioregions; microbats (Chiroptera); occurrence data; sampling bias

---

## 1. Introduction

Artificial light at night (ALAN) is now a pervasive, growing component of human disturbance. It has been framed as "ecological light pollution" because it alters the nocturnal environment in ways that can cascade through behaviour, physiology, species interactions, and ecosystem processes (Longcore and Rich, 2004; Gaston et al., 2013; Hirt et al., 2023). Global evidence indicates that both the spatial extent and brightness of nighttime lighting have increased over recent decades, although different indicators do not always agree because what satellites detect can diverge from what organisms experience (Kyba et al., 2017; Kyba et al., 2023; Sánchez de Miguel et al., 2021; Bará et al., 2025). This combination, rapid change and complex measurement, creates a practical problem for conservation: light is a cross-boundary pressure that can affect protected areas even when the land tenure and on-ground management within boundaries remain intact.

Protected areas are a cornerstone of biodiversity conservation, yet they are not isolated from propagating external pressures such as skyglow, light spill, and the infrastructural expansion that drives both (Hölker et al., 2010; Sanders et al., 2021). Recent global syntheses and assessments show that natural darkness has been eroded within protected areas and that ALAN has increased in belts around protected areas and in other conservation-priority places (Gaston et al., 2015; Guetté et al., 2018; Garrett et al., 2020; Mu et al., 2021). These studies establish the problem, but translating it into operational monitoring for a national protected-area system is not trivial. Two issues repeatedly complicate interpretation. First, night-lights products are often strongly censored at low radiance, so "no change" can reflect a true stable dark interior or simply a sensor/product floor. Second, the surroundings against which a protected area is compared must be defined carefully: buffers can include ocean, overlap other protected areas, or represent landscapes that are not meaningfully "external pressure". Both issues matter for management because they change which protected areas appear to be "at risk" and why.

Satellite remote sensing provides a unique opportunity for repeatable, national-scale auditing, but it comes with well-documented limitations. Night-lights sensors record upward radiance and related proxies, not the experienced sky brightness that is often most ecologically relevant (Falchi et al., 2016). Temporal interpretation can be confounded by changes in lighting technologies and spectra, for example the transition to LED, and by divergence among indicators even when the underlying phenomenon is increasing (Lewanzik and Voigt, 2017; Levin et al., 2025; Bará et al., 2025). These challenges do not negate the value of night-lights time series; they increase the need for analyses that are explicit about censoring, feasibility constraints, and uncertainty, rather than treating the output as a smooth, fully observed signal.

Australia is an ideal case for a national-scale assessment because it has a large protected-area system spanning strong gradients in human population density and development pressure, and because a substantial fraction of conservation value lies in landscapes near expanding urban and peri-urban regions. For nocturnal biodiversity, bats are a particularly relevant group: multiple studies show that artificial lighting can disturb bat commuting and foraging, and responses can vary with intensity, lighting technology, and context (Stone et al., 2009; Stone et al., 2015; Threlfall et al., 2013; Linley et al., 2016; Haddock et al., 2019; Lewanzik and Voigt, 2017). However, national biodiversity datasets are dominated by opportunistic occurrence records and are vulnerable to sample selection bias, spatial clustering, and heterogeneous observation processes across data providers. Without explicit bias controls and falsification, it is easy to mistake where people record wildlife for where wildlife actually responds (Phillips et al., 2009; Fithian et al., 2015; Roberts et al., 2017; Baker et al., 2024).

Here we present a reproducible, uncertainty-aware audit of dark-sky integrity for Australian protected areas (Layer A), coupled with a deliberately conservative occurrence-based "signal test" for nocturnal biodiversity (Layer B). Specifically, we (i) quantify baseline ALAN inside protected areas, in surrounding unprotected land buffers, and, where feasible, in boundary-to-interior rings; (ii) estimate 2013-2024 trends using robust estimators and explicitly report censoring and feasibility constraints; (iii) provide uncertainty for top-ranked brightening protected areas using an IBRA-clustered bootstrap; and (iv) test whether ALAN exposure at occurrence locations differentiates nocturnal microbat records from diurnal passerine control records under provider-matched modelling, spatially blocked cross-validation, and falsification tests including an IBRA x year shuffle. The goal is to provide conservation managers with an operational framework for monitoring ALAN exposure in protected areas, while being explicit about what the data can and cannot support.

---

## 2. Methods

### 2.1 Study design and questions

We set out to quantify the "dark-sky integrity" of Australian protected areas: how much artificial light at night (ALAN) is detectable inside protected areas, how that compares with surrounding landscapes, and how these measures have changed over time. We used a two-layer design.

Layer A, the primary contribution, is a national protected-area assessment based on annual satellite night-lights. For each protected area we summarised ALAN inside the protected area, in surrounding buffers that represent external pressure, and along boundary-to-interior gradients where feasible. We then estimated 2013-2024 trends and constructed simple, management-oriented summaries comparing trends inside protected areas to trends in surrounding unprotected land.

Layer B, the secondary contribution, is deliberately conservative. We tested whether ALAN exposure at occurrence locations is associated with the relative frequency of nocturnal microbat records compared with a diurnal control group, passerine birds, using spatially blocked cross-validation and falsification tests designed to expose residual sampling structure (Phillips et al., 2009; Roberts et al., 2017). This is framed as an association test in presence-only occurrence records, not as a causal estimate of ALAN impacts on population size or trends.

All distance and area computations were performed in an Australian equal-area projection (EPSG:3577).

### 2.2 Protected area data and preprocessing

Protected areas were defined using the Collaborative Australian Protected Areas Database (CAPAD 2024). Polygons were dissolved to a single geometry per protected area using the stable protected-area identifier (PA_ID). We repaired invalid geometries where needed and produced a cleaned national protected-area layer for analysis. For quality control and stratified diagnostics we computed basic geometry descriptors, including area and perimeter in the projected coordinate system.

### 2.3 Bioregional strata (IBRA)

We used the Interim Biogeographic Regionalisation for Australia (IBRA7) as a spatial stratification layer. Protected areas and occurrence records were assigned to IBRA regions by spatial overlay. IBRA was used for dependence-aware uncertainty resampling in Layer A and for robustness checks in Layer B: an IBRA x year falsification shuffle and a descriptive IBRA heterogeneity analysis.

### 2.4 Night-time lights (ALAN) data and preprocessing

We quantified ALAN using annual VIIRS day-night band (DNB) night-lights composites for 2013-2024, distributed as GeoTIFFs derived from the annual VIIRS night-lights product (Elvidge et al., 2021). Raster values were converted from stored integer values to analysis units using the per-file scale/offset metadata embedded in each GeoTIFF, ensuring comparability across years, including documented metadata scale changes in 2022-2024. In this annual-composite product, zero values represent a strong non-detect/floor regime; we therefore treated zero inflation as an expected feature of the data rather than an error to be smoothed away.

### 2.5 Layer A: spatial zones and ALAN summaries

#### 2.5.1 Inside protected areas

For each protected area and year, we extracted raster pixel values within the protected-area polygon and computed four summaries:

- mean radiance, the primary intensity summary;
- median radiance, a robustness summary;
- `frac_gt0`, the fraction of valid pixels with radiance > 0, used as a detectability summary; and
- `p95`, the 95th percentile of pixel radiance, used as an upper-tail summary.

These metrics were chosen because annual VIIRS composites in protected and remote landscapes are often dominated by zeros. `frac_gt0` and `p95` help characterise patterns in censoring-heavy regimes where mean and median can be uninformative.

#### 2.5.2 Surrounding buffers and buffer validity

To represent "external pressure" adjacent to protected areas, we generated outward buffers of 1 km and 5 km around each protected-area boundary in EPSG:3577. Because many protected areas are coastal and many buffers overlap other protected areas, we constructed and tracked buffer validity descriptors and analysed three buffer variants:

- raw buffer: the geometric buffer ring around the protected area;
- land buffer: the raw buffer intersected with a land mask, excluding ocean/sea pixels; and
- unprotected-land buffer, the primary buffer definition: the land buffer with overlap with other protected areas removed, intended to represent surrounding unprotected land.

Unless stated otherwise, comparisons between protected areas and their surroundings use the unprotected-land buffer.

#### 2.5.3 Boundary-to-interior rings (penetration profiles)

To examine boundary-to-interior gradients where data support it, we constructed interior rings at 0-1 km, 1-5 km, and 5-10 km inward from each protected-area boundary and summarised ALAN within each ring using mean radiance and `frac_gt0`. Because many protected areas are smaller than these distances, and because a 500 m raster implies coarse support, ring feasibility was quantified explicitly and ring-based results were treated as conditional on the subset of protected areas with complete ring coverage.

#### 2.5.4 Minimum pixel rule and missingness

For any protected-area, buffer, or ring summary in a given year, we required at least 10 valid raster pixels after masking. Estimates failing this threshold were recorded as missing. This minimum-pixel rule reduces unstable estimates for small polygons and makes feasibility explicit rather than silently injecting noise.

### 2.6 Layer A: trend estimation and retention summaries

We estimated monotonic trends in each metric across 2013-2024 using Theil-Sen slopes, the median of pairwise slopes, which are robust to outliers and tolerate irregular missingness. Trend estimation required at least 8 valid years for the inside-protected-area metric. Mean radiance was the primary trend metric reported in the main text; median radiance, `frac_gt0`, and `p95` were used for robustness and interpretation in the presence of heavy zero inflation.

To summarise retention or internalisation relative to external pressure, we computed differences between inside and buffer slopes, for example `slope_inside - slope_buffer_1km`. For a management-oriented overview we also classified each protected area into one of four descriptive retention quadrants based on the signs of inside and buffer slopes: concurrent brightening (both > 0), internal brightening with stable surroundings (inside > 0, buffer <= 0), stable/non-detect (both <= 0), and external pressure (buffer > 0, inside <= 0). These categories are descriptive triage summaries; they do not imply causation.

### 2.7 Layer A: uncertainty in top brightening identification (IBRA-cluster bootstrap)

To quantify uncertainty in trends and rankings under spatial dependence and temporal autocorrelation, we implemented an IBRA-clustered bootstrap. In each bootstrap replicate we resampled IBRA regions as spatial clusters with replacement, then applied a moving-block resample of years with block length 3 years for each protected area's annual time series, and recomputed the Theil-Sen slope. We ran 300 replicates and summarised each protected area's slope distribution using the median, 95% interval, and probability of slope > 0. For the highest-ranked protected areas we also computed a pairwise dominance matrix: the probability that `slope_i` exceeds `slope_j` across bootstrap replicates.

### 2.8 Layer B: occurrence data assembly and quality control

#### 2.8.1 Target and control groups

The target group was microbats, Order Chiroptera excluding Pteropodidae. The diurnal control group was passerine birds, Order Passeriformes. Using a diurnal control group provides a conservative contrast for an association test in opportunistic occurrence records, because both groups are influenced by observer effort and accessibility, but only one is nocturnally active (Phillips et al., 2009).

#### 2.8.2 Atlas of Living Australia (ALA) occurrence filters and deduplication

Occurrence records for 2013-2024 were downloaded from the Atlas of Living Australia and filtered to remove records failing basic coordinate and metadata quality checks, including coordinate uncertainty > 1 km. To reduce repeated sampling at popular sites, we deduplicated by retaining at most one record per 1 km grid cell per day within each taxon group. Because ALA downloads aggregate data from multiple providers with heterogeneous licences, we maintained a provider-level licensing ledger and restricted manuscript-ready outputs to derived summaries rather than redistribution of raw occurrence tables.

#### 2.8.3 Proximity-to-protected-area strata

Each occurrence record was classified by proximity to protected areas: inside a protected area, within 10 km of any protected area, or outside (> 10 km). For Layer B modelling we restricted to the inside-or-within-10-km scope to align the biodiversity signal test with protected-area-adjacent landscapes and with the spatial support of the remote-sensing metrics.

### 2.9 Layer B: ALAN exposure at occurrence locations

For each occurrence record, we extracted annual ALAN from the VIIRS raster corresponding to the occurrence year and applied the raster's scale/offset metadata. Because exposure was strongly zero-inflated, we represented ALAN with two covariates:

- `any_light`: indicator that ALAN > 0; and
- `log1p_alan`: `log(1 + ALAN)` for ALAN > 0, set to 0 when ALAN = 0.

This two-part representation separates detectable light versus none from intensity conditional on detectability.

### 2.10 Layer B: modelling, spatial blocking, and falsification

We fit logistic regression models predicting whether an occurrence record was a microbat (1) or passerine control (0) as a function of `any_light` and `log1p_alan`. To avoid inflated performance due to spatial autocorrelation, we used spatially blocked cross-validation with 50 km blocks and GroupKFold (5 folds) (Roberts et al., 2017). Models were fit on balanced case-control datasets with equal numbers of microbat and passerine records.

Primary inference was provider-matched: both microbat and passerine records were restricted to a single dominant provider, NSW BioNet (dr368), to reduce confounding by heterogeneous observation processes across providers. A multi-provider sensitivity run was retained as descriptive context only.

We implemented two falsification tests to detect residual sampling structure masquerading as an ALAN effect:

- shuffle ALAN values within spatial blocks; and
- shuffle ALAN values within IBRA x year strata.

If a coefficient persists under these shuffles, it is likely driven by spatially structured sampling patterns rather than an ALAN-linked signal.

To explore ecological heterogeneity, or remaining bias heterogeneity, we also fit within-IBRA models, provider-matched, for IBRA regions meeting a minimum sample threshold of at least 500 records per class, summarising variation in the conditional intensity coefficient across regions.

### 2.11 Software and reproducibility

Analyses were implemented as a versioned, test-driven Python pipeline with schema-versioned outputs and artefact manifests. All tables and figures in the Results can be regenerated from the repository given the public input datasets.

---

## 3. Results

### 3.1 Coverage, feasibility, and the censoring regime

Across Australian protected areas (n = 11,133), 4,426 protected areas (39.8%) met the minimum-pixel criterion in 2024 (>= 10 valid pixels) and the minimum-years criterion for inside-protected-area trend estimation (>= 8 valid years in 2013-2024). Buffer-based summaries were feasible for fewer protected areas once land masking and protected-area overlap removal were applied (n = 3,858 for the 1 km unprotected-land buffer and n = 3,992 for the 5 km unprotected-land buffer).

Baseline ALAN inside protected areas was strongly zero-inflated at the annual VIIRS sensor floor. In 2024, approximately 87% of eligible protected areas had inside-protected-area mean radiance equal to zero, indicating that most eligible protected areas fall below the detectability threshold of this annual composite product (Fig. 1).

Boundary-to-interior ring analyses were feasible only for a minority of protected areas, consistent with the prevalence of small or narrow polygons at 500 m resolution. In 2024, the 0-1 km interior ring met the minimum-pixel rule for about 40% of protected areas, the 1-5 km ring for about 13%, and complete coverage across all rings for only about 3% (n = 383). Consequently, edge-penetration profiles are conditional summaries for a small subset rather than a comprehensive national pattern (Supplementary Fig. S1).

### 3.2 Baseline spatial pattern of ALAN exposure (2024)

Among eligible protected areas, non-zero ALAN in 2024 was spatially clustered near major urban and peri-urban regions, with higher intensities concentrated along developed coastal corridors and around metropolitan areas (Fig. 1). In contrast, large remote regions were dominated by non-detect values. The baseline figure also makes feasibility explicit: many protected areas are too small, in raster support, or otherwise data-limited to support stable inside-area summaries at 500 m resolution.

### 3.3 Trends in inside-protected-area ALAN (2013-2024)

Trends in inside-protected-area mean radiance were dominated by exactly zero slopes (fraction exactly zero 0.897; n = 4,426). This reflects a mixture of genuine stability and censoring at the sensor floor: where annual values remain at zero, any slope estimator will return zero regardless of subtle real-world changes.

The non-zero slope subset (n = 457) showed a right-skewed distribution with predominantly positive slopes (Fig. 2). Within this subset, the median slope was 0.098 radiance units per year (interquartile range 0.0075-0.4164). The full distribution had mean slope 0.0283 (sd 0.295), but this mean is not especially informative given the dominance of the zero-slope mass. Year-to-year sanity checks of national mean inside-protected-area radiance showed no discontinuity across 2013-2024 after applying scale/offset metadata, including across the 2022-2024 metadata scaling change.

### 3.4 Retention versus external pressure in surrounding unprotected land

Comparing inside trends to trends in the surrounding 1 km unprotected-land buffer (n = 3,858), most protected areas fell in the stable/non-detect quadrant with both inside and buffer slopes <= 0 (Q3: 3,308 protected areas; 85.7%). A smaller subset showed concurrent brightening inside and in surrounding unprotected land (Q1: 305; 7.9%). Protected areas with inside brightening but non-brightening surroundings were rare (Q2: 55; 1.4%). A non-trivial subset showed external pressure, defined as brightening in surrounding unprotected land but not inside the protected area (Q4: 190; 4.9%) (Fig. 3).

These quadrant patterns provide a compact management interpretation. Most protected areas show no detectable change in either interior or surrounding unprotected land at this sensor/product scale. However, a subset shows simultaneous interior and surrounding brightening, and another subset shows external pressure without detectable interior brightening, consistent with the idea that some protected areas remain dark while their surrounding landscapes brighten.

### 3.5 Uncertainty in identifying top brightening protected areas

IBRA-clustered bootstrap results showed that only a subset of the highest-slope protected areas remain clearly separated under dependence-aware resampling, while many mid-rank sites have overlapping uncertainty intervals (Supplementary Fig. S2-S3). In other words, the data support the existence of a brightening tail, but they also support substantial uncertainty in the ordering of most sites within that tail. This cautions against treating ranked top-N lists as precise ordering and supports reporting probabilities and intervals alongside any prioritisation outputs.

### 3.6 Boundary penetration profiles (conditional on ring feasibility)

Among the small subset of protected areas with complete interior ring feasibility (n = 383), boundary-adjacent rings (0-1 km) were more likely to show detectable ALAN than deeper interior rings, consistent with an edge-associated pattern of light penetration where measurable (Supplementary Fig. S1). However, given low feasibility and heavy zero inflation even within the feasible subset, these penetration profiles should be interpreted as limited, conditional evidence rather than a strong national generalisation.

### 3.7 Occurrence data volume, bias structure, and ALAN exposure distributions

After filtering and deduplication, we retained 63,716 microbat records and 2,378,378 passerine records (2013-2024). Deduplication removed 41.0% of filtered microbat records and 16.1% of filtered passerine records, consistent with stronger clustering of microbat occurrences in opportunistic datasets.

Provider concentration in microbats was extreme: 88.8% of retained microbat records came from a single provider (NSW BioNet; dr368), motivating provider-matched primary inference. Within the protected-area-adjacent scope used for modelling, inside or within 10 km, 56,883 microbat records (89.3%) and 2,142,802 passerine records (90.1%) were retained before balancing. Microbat records were relatively more likely to occur inside protected areas (25.0%) than passerine records (18.4%), while passerine records were more likely to fall within 10 km buffers (71.7% versus 64.3%).

ALAN exposure at occurrence locations varied strongly with proximity to protected areas and was heavily zero-inflated (Fig. 4). For microbats, zero fractions were 0.890 inside protected areas, 0.585 within 10 km, and 0.814 outside (> 10 km). For passerines, zero fractions were 0.839 inside protected areas, 0.474 within 10 km, and 0.779 outside. Upper-tail exposure (`p95`) was much higher within 10 km buffers than inside protected areas for both groups (within-10-km `p95` = 150 for microbats and 210 for passerines), reinforcing that much of the ALAN gradient relevant to protected areas is expressed in adjacent landscapes rather than in protected-area interiors.

### 3.8 Provider-matched signal test and falsification results

In the provider-matched primary design (dr368), balanced case-control models used 50,281 microbat records and 50,281 passerine records, inside or within 10 km. The model estimated a positive association with any detectable ALAN (`any_light` mean coefficient 1.316; fold SD 0.128) and a negative association with conditional intensity among lit sites (`log1p_alan` mean coefficient -0.354; fold SD 0.024). Predictive discrimination was weak (AUC 0.545; log loss 0.689), indicating that ALAN alone provides limited ability to distinguish microbat from passerine occurrence records in this conservative design (Fig. 5). In practical terms, if there is a signal, it is small.

Falsification tests substantially attenuated the apparent associations. When ALAN was shuffled within spatial blocks, the conditional intensity term collapsed toward zero (`log1p_alan` mean -0.027) and discrimination dropped to near-random (AUC 0.505). When ALAN was shuffled within IBRA x year strata, the intensity term again collapsed to approximately zero (`log1p_alan` mean -0.001) with AUC 0.517. The persistence of a small positive `any_light` term under shuffling suggests residual structure remains even under these nulls, while the disappearance of the intensity association indicates that the conditional intensity effect is not robust to strong falsification. A multi-provider sensitivity run produced similar coefficient directions but is descriptive only given heterogeneous provider processes (AUC 0.557).

### 3.9 IBRA heterogeneity (descriptive)

Within-IBRA models, provider matched and with >= 500 records per class, were feasible for 11 IBRA regions. The estimated conditional intensity coefficient (`log1p_alan`) varied across regions in both sign and magnitude (Supplementary Fig. S6). Given the weak overall discrimination and falsification sensitivity, this heterogeneity is consistent with context dependence, residual sampling structure, or both; these IBRA-specific results are therefore best interpreted as descriptive rather than confirmatory.

---

## 4. Discussion

### 4.1 What we learned about dark-sky integrity in Australian protected areas

Two results dominate the protected-area assessment.

First, the national ALAN signal inside protected areas is strongly censored at the annual VIIRS product scale. Even among protected areas that meet a conservative minimum-pixel criterion for stable estimation, the majority have inside-protected-area mean radiance at the non-detect regime in 2024. This is not simply a nuisance; it is a substantive finding about both ecology and monitoring. Ecologically, it implies that many protected areas, especially large and remote ones, are consistent with very low detectable upward radiance in their interiors. Methodologically, it means that naive trend analysis will be dominated by exact zeros, and "no change" often cannot be separated from "below detectability" without additional summaries designed for zero-inflated regimes. This is a key distinction that is often blurred when night-lights are used as continuous intensity variables without explicit feasibility and censoring reporting.

Second, where trends are measurable, change is concentrated in a minority tail rather than as a broad shift across the protected-area system. Inside-protected-area trends in mean radiance from 2013-2024 were dominated by exactly zero slopes, with a small subset showing a right-skewed positive tail. This pattern is broadly consistent with the global picture: protected areas generally remain darker than surrounding landscapes, but darkness can erode at the margins and around particular sites, especially near growing development pressure (Gaston et al., 2015; Guetté et al., 2018; Mu et al., 2021). Our retention quadrant analysis provides a management-ready summary of this structure: most protected areas show no detectable brightening inside or in nearby unprotected land, while smaller subsets show either concurrent brightening inside and outside, or external pressure where unprotected land around a protected area brightens without detectable brightening inside.

A practical contribution here is that we separated external pressure from artefacts of buffer definition by explicitly decomposing buffers into land-only and unprotected-land components. This matters in a country with extensive coastlines and with protected-area clustering: without these corrections, buffer radiance can be biased downward by ocean pixels or can be biased toward protected-like conditions by overlap with other protected areas. The corrected unprotected-land buffer is a more defensible proxy for external development pressure than a raw geometric buffer.

### 4.2 Uncertainty and feasibility: why the top-N story needs humility

A common way to communicate national assessments is to publish ranked lists of most impacted places. Those lists are valuable for triage, but they become misleading when treated as precise ordering rather than as uncertain estimates. Our IBRA-clustered bootstrap shows that only a subset of top brighteners remain clearly separated when spatial dependence and temporal autocorrelation are respected; for many mid-rank sites, slope intervals overlap and pairwise dominance probabilities are near 0.5. This is an important message for management as well as for science: prioritisation can and should be uncertainty-aware. The right output is not "park X is #7"; it is "these few parks have robust evidence of brightening; many others are plausible brighteners but ranks are unstable, so decisions should not be sensitive to fine ordering".

Feasibility constraints reinforce this point. Boundary-to-interior rings are intuitively appealing as a measure of light penetration, but they are only feasible for a small fraction of protected areas at 500 m resolution. Any national narrative about penetration must therefore be conditional: it describes what can be measured for a subset, not the whole system. Explicitly reporting ring feasibility avoids a common error in landscape-scale remote-sensing studies: analysing only the feasible subset but writing as if the result generalises automatically.

### 4.3 Measurement caveats: what VIIRS tells us, and what it does not

Our conclusions are bounded by the measurement realities of satellite night-lights. VIIRS-based products measure upward radiance proxies, not sky brightness at the ground, and they are not equally sensitive to all lighting technologies and spectra (Falchi et al., 2016; Kyba et al., 2023). The rapid transition toward LEDs can alter both ecological effects and detectability by satellites, contributing to divergence among indicators (Lewanzik and Voigt, 2017; Levin et al., 2025; Bará et al., 2025). These issues are now sufficiently prominent that they should be treated as standard caveats in any conservation inference built on night-lights trends.

In this context, one of our more important contributions is not a new metric but a disciplined interpretation framework: explicitly separate eligibility from darkness, quantify the zero-inflation regime, use censoring-aware summaries such as `frac_gt0` and upper-tail metrics, and verify temporal consistency through sanity checks around known product changes. This approach reduces the risk of over-interpreting artefacts as trends and helps managers understand what kinds of change the monitoring system can detect.

### 4.4 Management implications: treating darkness as a protected-area asset

For conservation managers, the main message is simple: many protected areas remain effectively dark under detectable VIIRS annual-composite radiance, but some are at risk through either internal brightening or surrounding pressure in adjacent unprotected land. The management levers for ALAN are often located outside protected-area boundaries: local government lighting standards, road and infrastructure lighting design, development approvals near reserve boundaries, and the siting and shielding of high-intensity lighting. The retention quadrant framing and the corrected unprotected-land buffers are designed to map naturally onto those levers. Protected areas in the external-pressure quadrant are not necessarily failing internally; they may be holding the line while surroundings brighten, which points to a buffer-zone governance problem rather than an internal management problem. Conversely, protected areas with internal brightening concurrent with external brightening are candidates for targeted investigation: are there new facilities, roads, or visitor infrastructure, or is the trend reflecting broader peri-urban growth that is increasingly visible even deep inside the polygon?

A broader implication is that protected should not be conflated with dark. Global assessments have shown that skyglow extends into biodiversity-important areas and that darkness can erode even when land is formally protected (Gaston et al., 2015; Garrett et al., 2020). A practical monitoring framework helps make this a measurable attribute of protected-area condition, rather than a subjective concern.

### 4.5 Layer B: a conservative signal test for nocturnal biodiversity, and what it does and does not show

The Layer B analysis was designed to be conservative to the point of pessimism: provider-matched primary inference, spatial blocking, and two falsification tests. Under this design, ALAN covariates alone had weak discriminatory power in differentiating microbat from passerine occurrence records (AUC only modestly above 0.5). This matters because it sets an honest expectation: national-scale, occurrence-based biodiversity signals of ALAN are likely to be subtle, and they are easy to confound with sampling structure.

The fitted two-part exposure representation produced a pattern that is biologically plausible but not robust enough to be treated as confirmatory. In the primary provider-matched model, microbat records were associated with a higher probability of occurring at locations with any detectable ALAN, but among lit sites the conditional intensity term was negative. One ecological interpretation is that low levels of light can co-occur with insect availability and accessible observation locations, while higher intensity lighting may deter or disrupt bat movement and foraging, consistent with behavioural evidence that street lighting can disturb commuting and alter activity patterns (Stone et al., 2009; Stone et al., 2015; Threlfall et al., 2013; Haddock et al., 2019). However, falsification tests strongly caution against over-interpretation. When ALAN was shuffled within spatial blocks and within IBRA x year strata, the conditional intensity association collapsed toward null, implying that the apparent intensity effect is not stable under nulls that preserve sampling structure. In other words, much of what looks like a signal can be produced by structured observation processes.

The IBRA heterogeneity analysis reinforces this caution. Conditional intensity coefficients varied across IBRA regions, but given weak overall discrimination and falsification sensitivity, this heterogeneity is compatible with context dependence, residual sampling bias, or both. We therefore treat Layer B as a proof-of-approach: a template for how to bring bias-aware modelling and falsification into protected-area-adjacent ALAN-biodiversity analyses, not as evidence of causal impacts on microbat populations.

### 4.6 Why falsification and bias controls are not optional in occurrence-based ALAN ecology

A broader methodological point emerges from Layer B. Opportunistic occurrence data are not random samples; they are shaped by access, observer effort, and reporting behaviour. Presence-only modelling has a long history of showing how sample selection bias can generate spurious associations unless background selection, bias covariates, or other corrections are used (Phillips et al., 2009; Fithian et al., 2015). In spatial ecology, random cross-validation can substantially overstate predictive performance when records are clustered, making structured evaluation and spatial blocking essential (Roberts et al., 2017). The most important addition here is that falsification should be treated as a routine component of inference: if an effect survives shuffling within plausible strata, it is less credible; if it disappears, the honest conclusion is that the effect is not robust given the observation process.

Recent guidance on sampling bias correction emphasises that no single fix is universally reliable and that sensitivity analyses should be expected (Baker et al., 2024). Our provider-matched primary design is best seen as a strong form of sensitivity analysis: it reduces one major axis of heterogeneity, the provider process, at the cost of generality. For management and policy, that is an acceptable trade when the alternative is a national claim built on an uncontrolled mixture of observation systems.

### 4.7 Future directions

Several clear next steps follow from this work.

First, improved measurement of low-level ALAN and experienced sky brightness would substantially strengthen protected-area assessments. VIIRS annual composites are valuable for repeatability and global comparability, but they are not designed to resolve very low radiance regimes in small polygons. Combining satellite products with ground-based sky brightness observations, including citizen-science approaches, and models that translate radiance to skyglow could better align monitoring with organismal exposure (Falchi et al., 2016; Kyba et al., 2023).

Second, biodiversity inference would benefit from data streams with more standardised observation processes. Acoustic monitoring networks for bats, repeated surveys, or structured citizen-science protocols could support stronger causal or occupancy-style inference than opportunistic occurrences. Even within occurrence datasets, focusing on more specific taxa, such as species or guilds with known light sensitivities, incorporating habitat covariates, and using explicitly designed target-group backgrounds could help separate ecological signal from sampling structure.

Third, there is a policy opportunity: the outputs produced here are directly compatible with routine reporting. Because the pipeline is reproducible and schema-versioned, it can be rerun annually as new CAPAD updates and night-lights products become available, providing a stable monitoring framework for agencies and a basis for evaluating lighting policy interventions around priority reserves.

### 4.8 Conclusions

A national protected-area system can be legally secure and still be environmentally porous. Our analysis shows that, at the scale detectable by annual VIIRS composites, most Australian protected areas are consistent with very low detectable ALAN and show no detectable trend in interior radiance over 2013-2024. However, a minority of protected areas show measurable brightening and/or increasing external pressure in adjacent unprotected land, and the ordering of top brighteners carries non-trivial uncertainty under dependence-aware resampling. These results support a practical, uncertainty-aware framework for auditing dark-sky integrity that is directly relevant to protected-area planning and buffer-zone governance.

Our conservative occurrence-based signal test suggests that any association between ALAN and nocturnal microbat occurrence records is weak and sensitive to falsification, underscoring the need for bias-aware modelling and for complementary biodiversity monitoring approaches. Taken together, the two layers provide an operational pathway: quantify where and how protected areas are exposed to ALAN through time, identify plausible priorities with uncertainty, and treat biodiversity signals from opportunistic data with the scepticism they deserve.

---

## 5. Limitations

- **Censoring:** 500 m composites yield heavy zero‑mass; mean/median trends are constrained by the sensor floor.
- **Selection:** many PAs lack sufficient valid pixels or complete rings; results are conditional on eligible subsets.
- **Occurrence bias (Layer B):** strong provider/state concentration and spatial clustering; inference is restricted to provider‑matched case‑control design.
- **Causality:** presence‑only models cannot infer population decline or causal effects.

---

## 6. Data and code availability

- Large derived tables and raw occurrences are intentionally excluded from git; reproducible outputs are generated via the pipeline described in `docs/roadmap.md`.
- Public data sources and checksums are recorded in `data/README.md`.

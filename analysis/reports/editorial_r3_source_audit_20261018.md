# R3 primary-source audit — 18 October 2026

Scope: independently check the industrial-site interpretations, the national
20 km guidance, and the proposed Kosciuszko product-artefact argument in
`editorial_claude_r2_review_20261018.md`. This is a source and inference audit;
the national numerical results were not recomputed here. All URLs were checked
on 18 October 2026. Only this report was edited for this assignment.

## Disposition

| Proposed claim | Finding | Editorial action |
|---|---|---|
| Gorgon production began in March 2016 on Barrow Island Nature Reserve | Supported. The 7 March release announces that production has started; it does not establish that production started on exactly 7 March. | Use month/year, or distinguish announcement date from event date. |
| Barrow cluster is at Gorgon | Primary coordinates establish proximity to Gorgon infrastructure, approximately 1.1 km from the gas-treatment-plant pipeline endpoints. | Say near the Gorgon plant; do not identify a particular flare or claim source attribution. |
| Murujuga decrease is at Karratha Gas Plant | A government location point for KGP is approximately 1.3 km northwest of the rounded cluster centre. | Near KGP is supported; exact coincidence with a plant component is unverified. |
| KGP flaring was below 10% of its 2013 peak | Supported for **2025**, in a source published **6 February 2026**. | Cite as Woodside 2026 and explicitly place the observation outside 2013–2024, or omit the numerical comparison from Results. |
| Thevenard production ended in 2014; onshore decommissioning finished in June 2023 | Production cessation is supported; completion was announced on 15 June 2023. | Say completed by June 2023. Do not infer a continuously dark interval after cessation. |
| Thevenard cluster is near the former oil facility on a nature reserve | Supported by the 2014 environment plan and an independently located 2006 botanical collection near the plant. | Use near the former facility. No particular light source is identified. |
| Guidelines request assessment within 20 km of important habitat | Supported with qualifications about listed species, light sensitivity and species-specific EIA. | Preserve the qualifications; this is not a universal protected-area buffer. |
| Kosciuszko increase is unlikely to be a product artefact because it starts in 2021 and is localized | Not established. | Replace with the narrower timing observation; retain product-continuity uncertainty. |

The parent numerical audit identifies the five largest negative contributions
as Barrow, Murujuga, Strzelecki, Thevenard and Newlands. The industrial cases are
therefore three named examples at ranks 1, 2 and 4, not the three largest
decreases and not explanations for all five. Its Barrow ratio is 2.774, so use
“nearly tripled”. Its Thevenard history contains zero values in 2016–2017 and
positive values again in 2018–2019: avoid a monotonic shutdown narrative.

## Verified primary sources and spatial checks

### Barrow Island / Gorgon

- **Chevron Corporation (2016), “Chevron Achieves First LNG Production at
  Gorgon”, 7 March 2016**, corporate press release. Suggested key:
  `chevron2016`. It announces LNG and condensate production at Gorgon on Barrow
  Island. [Primary release](https://chevroncorp.gcs-web.com/node/13991).
- **Government of Western Australia (2016), “Premier hails first Gorgon LNG
  shipment”, 21 March 2016**, media statement. Suggested key: `wagov2016`.
  Confirms the first shipment, Class A Nature Reserve status, and construction
  commencing in December 2009. Construction and industrial activity therefore
  predate the 2013 start of this series.
  [Primary statement](https://www.wa.gov.au/government/media-statements/Barnett%20Liberal%20National%20Government/Premier-hails-first-Gorgon-LNG-shipment-20160321).
- **Chevron Corporation (2015), “Gorgon and Jansz Feed Gas Pipelines Operations
  (State) – Environment Plan Summary”, GOR-COP-01488, revision 1.0,
  13 August 2015**, pp. 4, 6–7, 9. Suggested key: `chevrongorgon2015`.
  Table 1-1 gives GDA94 onshore pipeline endpoints PL84:
  E337994.28/N7700475.00 and PL85: E337956.78/N7700475.00. Figure 1-1 specifies
  MGA zone 50; p. 7 places the receiver compound within the treatment plant.
  The report also identifies the island as a Class A Nature Reserve.
  [Government-hosted primary plan](https://ace.dmp.wa.gov.au/ACE/Public/PetroleumProposals/ViewPlanSummary?registrationId=70657).

The transformation EPSG:28350 → EPSG:4326 gives endpoint locations
20.788529°S, 115.443512°E and 20.788526°S, 115.443152°E. WGS84 geodesic
distances from the supplied rounded cluster centre, 20.779°S, 115.442°E, are
1,067 m and 1,061 m. These are distances to documented infrastructure points,
not to the nearest facility boundary. The calculation supports geographic
proximity; it cannot determine the source of individual raster values.

**Defensible prose:** “Barrow Island's measured radiance nearly tripled in
2016, with the increase concentrated near the Gorgon gas-treatment plant.
Chevron announced the start of LNG and condensate production in March that
year [@chevron2016].” Reserve status can be cited separately to `wagov2016`.
The temporal correspondence is an explanation to investigate, not evidence
that the subsequent decline measures reduced facility lighting or output.

### Murujuga / Karratha Gas Plant

- **Woodside Energy (2026), “KGP sets new record for lowest flaring”,
  6 February 2026**, corporate news article. Suggested key: `woodside2026`.
  The stated annual quantity in 2025 was less than one-tenth of the 2013 peak.
  This concerns gas flared, not a measured reduction in night lighting. The
  article describes additional flare-reduction changes implemented in 2025.
  [Primary article](https://www.woodside.com/media-centre/news-stories/story/kgp-sets-new-record-for-lowest-flaring).
- **DCCEEW (2025), “Request for Advice – Submitted: EPBC 2018/8335/North West
  Shelf Project Extension”, ECAS-2025-0035**, requested 10 July 2025, portal
  summary generated 11 July 2025. Suggested key if needed: `dcceewkgp2025`.
  Released in FOI file LEX 81194, document 96; its p. 5 is PDF page 144 of
  180. Section 2.4 identifies Karratha Gas Plant at
  **−20.5925519367, 116.7785311506**.
  [Government document](https://www.dcceew.gov.au/sites/default/files/documents/81194.pdf).

Treating that generic location point as WGS84 for a kilometre-scale proximity
check gives **1,286 m** from 20.601°S, 116.787°E. This is not a plant outline
or flare coordinate. The primary sources inspected do not establish that the
cluster centre lies inside KGP, or which emissions generated it. The plant is
also part of an industrial landscape: geographic proximity alone cannot
exclude contributions from other sources.

**Preferred Results wording:** “Murujuga's decline was concentrated near the
Karratha Gas Plant on the Burrup Peninsula.” If the flaring evidence is useful
in Discussion: “Woodside subsequently reported that flaring in 2025 was below
10% of its 2013 peak [@woodside2026]. This observation falls outside our study
period and does not identify the cause of the 2013–2024 satellite decrease.”
Do not join the satellite change and 2025 claim with “while”, which conceals
the unmatched dates. The source key `woodside2025` would misdate the article.

### Thevenard Island

- **Chevron Australia (2023), “Thevenard Island decommissioning achieves major
  milestone”, 15 June 2023**, media statement. Suggested key: `chevron2023`.
  Reports oil production from 1989 until 2014 and completed onshore
  decommissioning; rehabilitation monitoring was continuing. This is not a
  statement that all offshore work or rehabilitation had finished.
  [Primary statement](https://australia.chevron.com/news/2023/thevenard-island-decommissioning-achieves-major-milestone).
- **Chevron Australia Pty Ltd (2014), “Environment Plan Summary: Thevenard
  Island Joint Venture — Production and Cessation”, ABU131200075,
  revision 0, 20 January 2014**, pp. 3–5. Suggested key: `chevronthevenard2014`.
  Identifies Nature Conservation Reserve **33174** and the 25 ha onshore
  facility lease at the island's northeastern end. Figure 1.1 shows its
  relation to the island and neighbouring tourism lease. The table's island
  coordinate is a general location, not a plant coordinate.
  [Government-hosted primary plan](https://ace.dmp.wa.gov.au/ACE/Public/PetroleumProposals/ViewPlanSummary?registrationId=48046).
- **Maslin, B. R. (2007), “Acacia bivenosa group of wattles on Airlie &
  Thevenard Islands, Pilbara region WA”**, report for Apache Energy and Chevron
  Australia, Department of Environment and Conservation, Kensington, February
  2007. Suggested key if needed: `maslin2007`. Appendix 1, printed p. 12/PDF
  p. 14, locates collection B. R. Maslin 8813, 28 July 2006, near the Chevron
  oil camp and plant at 21°27′28.0″S, 115°01′24.3″E. Both the coordinate and
  site description were visually checked in the scanned page.
  [Government-library copy](https://library.dbca.wa.gov.au/FullTextFiles/024072.pdf).

The botanical point is −21.457778, 115.023417, approximately **341 m** from
the supplied cluster centre, −21.455, 115.022. It is a collection locality
near the facility, not a surveyed facility centroid. Together with the
operator's plan, it supports the geographic association without identifying
which lights or flares contributed.

**Defensible prose:** “Thevenard Island's decrease was concentrated near its
former oil facility. Production ceased in 2014, and Chevron reported completed
onshore decommissioning by June 2023 [@chevron2023].” Add the observed annual
history separately; a 2024 product zero does not establish physical darkness
or a permanent lights-off date.

## National 20 km recommendation

**DCCEEW (2023), “National Light Pollution Guidelines for Wildlife”, version
2.0, May 2023**, Department of Climate Change, Energy, the Environment and
Water, Canberra, printed p. 10/PDF p. 17. Suggested key: `dcceew2023`.
[Primary guidelines](https://www.dcceew.gov.au/system/files/resources/2eb379de-931b-4547-8bcc-f96c73065f54/files/national-light-pollution-guidelines-wildlife.pdf).

The recommendation concerns important habitat for **listed species known to
be affected by artificial light**, within 20 km of a project. It calls for
species-specific consideration through EIA. The distance is nominal and
precautionary; the document allows impacts beyond it and distinguishes
assessment distance from where mitigation is necessary. It is not a universal
exclusion zone or an empirical boundary of light penetration.

**Defensible prose:** “Australia's national guidelines recommend
species-specific assessment where a project is within 20 km of important
habitat for listed species known to be affected by artificial light
[@dcceew2023].”

A management paragraph can connect screening to examination of nearby
projects, lighting inventories and approval conditions. The satellite bands
do not locate the responsible source: some boundary-zone light may originate
inside a reserve. Industrial flaring, operational change and decommissioning
also require a different interpretation from routine lighting design.

## Kosciuszko: what the 2021 rise does and does not resolve

**Reject** “The increase is unlikely to be a product artefact” and the claim
that a detection-sensitivity change would be spread across the park. Neither
has an evidential test or a calibrated likelihood behind it.

1. The 2020–2021 increase from 1,150 to 4,600 establishes a rise in the
   observed product before the documented 2022 source change. That particular
   change cannot by itself generate the earlier observation. It does not
   establish the cause of either the early rise or the larger later increase.
2. `product_lineage_review.md` reports support for V2.1 inputs in 2013–2021
   from earlier archived code, not complete byte-level reconstruction of the
   current deposit. “Under the same product version” needs this qualification.
3. Even genuinely common processing code does not make annual sampling,
   background statistics or mask outcomes identical. EOG documents annual
   composite construction, outlier filtering and local 3×3-cell background
   tests. It also describes a multiyear threshold per cell: do not invent an
   annual threshold change as an established mechanism. Spatially selective
   effects remain possible because input values and local conditions differ.
4. The common-valid endpoint audit excludes a support-count explanation for
   the 2019–2024 cell sum and verifies decoding. It does not independently
   validate radiance measurements, annual masking or source attribution.
5. The two-cluster pattern and documented construction locations make a
   development-related explanation plausible. They do not demonstrate that
   all of the change, or its magnitude, is independent of product effects.

Primary technical documentation:
[EOG Annual VNL description](https://eogdata.mines.edu/products/vnl/),
[EOG V2.2 readme](https://eogdata.mines.edu/products/vnl/VNL_v22_readme_20230707.pptx),
[earlier deposited processing script](https://zenodo.org/api/records/8277198/files/nightlights_stack_500m.R/content).
The EOG webpage was re-read live. Readme and script details were checked
against the existing repository lineage audit; their direct browser retrieval
failed in this check. No independent annual satellite product was acquired.

**Ready replacement:** “The product cell-sum rose from 1,150 in 2020 to 4,600
in 2021, before the documented 2022 change in source processing, and increased
in each subsequent year. Its concentration near the two construction areas
supports investigating a development-related explanation. However, the timing
and spatial pattern do not exclude product effects; independent observations
are needed to establish source attribution and the magnitude of environmental
change.”

In Figure 4, a 2022 source-change marker is informative if its caption presents
it as a documented boundary. It should not visually imply that observations
before 2022 have been validated as artefact-free.

## Access and verification limits

- Chevron's Thevenard article returned 403 to direct opening, but the search
  service retrieved its full primary-source text, including date and the
  statements above. The independent 2014 operator plan was downloaded and its
  location figure inspected.
- Some DWER/EPA PDFs returned 403, including the 2023 Gorgon works-approval
  decision and EPA Report 1727's KGP/Murujuga map. They were not used to claim
  exact facility/cluster overlap. The downloaded DCCEEW location record and
  government-hosted operator plans provide the bounded spatial checks above.
- Distances were calculated with `pyproj` geodesics from the rounded cluster
  centres supplied for this task. They are proximity checks, not new pixel
  overlays or source-location estimates. No surveyed flare coordinate or
  georeferenced facility-outline overlay was established for these clusters.
- Source histories can corroborate plausible interpretations; they do not
  convert the masked, quantised product into ecological exposure measurements.

Completed: 18 October 2026, 20:09 AEDT (Australia/Hobart).

# Review of R2 with replacement passages (Claude, 18 October 2026)

Reviewed: the frozen R2 reading copy, "Boundary zones and interior hotspots of
brightening in Australia's protected areas", in
`artefacts/editorial_20261018_r2/`. New supporting numbers come from
`analysis/reports/brightening_budget/` (`summary.json`, `hotspots.json`, rerun
18 October). Items marked [verify] need a primary source before use.

## Verdict

R2 is the first version I would send to an editor. It has a finding-based
title, an opening that states a real problem in one image (a small bright site
versus weak dispersed change), a named case and a figure that shows it. Four
things still hold it back:

1. **The abstract's key number is wrapped in its own denominator.** "72% of
   gross positive trends when each reserve was divided into boundary and
   interior zones" is precise but unreadable to an editor. The 51% that
   follows then reads as a retraction, when it is actually a second finding:
   even reserves with real interiors put half their increase into an eighth of
   their area.
2. **The decreases are anonymous.** The draft says five reserves supply 95% of
   decreases and that the net sign depends on the period, but not what those
   reserves are. All three large cases coincide with documented oil and gas
   events, and outside the five reserves the estate brightened in both
   periods. That turns an apparent ambiguity into a clear, memorable result.
3. **The Kosciuszko case concedes more than it should.** "The endpoint
   difference also spans product changes" invites a doubt the data answer:
   the rise began in 2021, under the same product version, and is confined to
   two clusters.
4. **The Discussion never says what an agency would do differently.** It
   repeats "investigate" without naming the two levers the two patterns imply.

Secondary points: the matched Sen-band paragraph (3.2, third paragraph) and
the polygon-area paragraph (3.3, last paragraph) re-litigate earlier framings
and could each shrink to one sentence with an SI pointer. The Introduction
ends on a caveat rather than on what was found.

## New evidence behind points 2 and 3

All of the following come from summary.json and hotspots.json.

- **Net excluding the five largest decreases:** +2,596 for 2013–2024 and
  +1,922 for 2013–2021. Also excluding Kosciuszko: +2,226 and +1,879. With all
  reserves included: +479 and −538.
- **Barrow Island (WA_11648):** in 2015–2016, 100% of the jump sits at one
  cluster, 20.779°S 115.442°E (+144,300). Gorgon first production was 7 March
  2016 (Chevron) and first cargo 21 March 2016 (WA Government); Barrow is a
  Class A Nature Reserve.
- **Murujuga (WA_2803):** inside sum 76,060 in 2013 and 10,510 in 2024; 96% of
  the decrease is at one cluster, 20.601°S 116.787°E, on the Burrup
  Peninsula. Woodside reports that flaring at the Karratha Gas Plant in 2025
  was under 10% of its 2013 peak
  (https://www.woodside.com/media-centre/news-stories/story/kgp-sets-new-record-for-lowest-flaring).
  [verify] that the plant lies at the cluster location. WA_2803 is also the
  reserve with changing buffer pixel counts.
- **Thevenard Island (WA_33174):** inside sum 3,370 in 2013 and 0 in 2024, all
  at one cluster, 21.455°S 115.022°E. Chevron ended production in 2014 and
  completed onshore decommissioning in June 2023; the island is a gazetted
  nature reserve
  (https://australia.chevron.com/news/2023/thevenard-island-decommissioning-achieves-major-milestone).
- **Kosciuszko annual sums:** 1,150 in 2020, 4,600 in 2021, 13,940 in 2022,
  25,280 in 2023, 26,970 in 2024. Lit pixels: 97, 222, 563, 634, 696. The rise
  starts in a V2.1 year, before the 2022 source change.
- The hotspot script now applies scale and offset, asserts paired-grid
  identity, uses an explicit common-valid mask (recording counts) and saves
  URLs, windows, transforms, decoded-array hashes and the access time.

## Replacement passages

### Abstract (about 300 words; replaces R2's)

Satellite night-lights can reveal change across an entire protected-area
estate, but reserve-wide averages say little about where that change occurs
or what drives the national total. We divided measured radiance change across
Australia's 2024 protected estate into boundary and interior components,
reserve by reserve, using annual VIIRS-derived observations for 2013–2024. Of
11,133 reserves, 4,426 (39.8%) had enough raster support to assess, together
holding 99.8% of summed reserve area. The outermost kilometre of these
reserves contained 14% of their sampled area but 72% of the summed increase in
measured radiance (83% for 2013–2021). Even in reserves large enough to have a
measurable interior, the outer kilometre held half the increase in one-eighth
of the area. Increases deeper inside were highly concentrated: two reserves
supplied half and seven supplied 80%. In Kosciuszko National Park, the largest
of these, 96% of positive pixel change between 2019 and 2024 lay in two
clusters near the Lobs Hole and Tantangara construction areas of the Snowy 2.0
pumped-hydro project. Decreases were more concentrated still. Five reserves
supplied 95% of them, led by Barrow Island, site of the Gorgon gas project,
and Murujuga National Park beside the Karratha Gas Plant. Because these few
sites dominate the national balance, the net trend changed sign with the
period analysed; without them, measured radiance rose in both periods.
Ranking reserves by mean trend or by integrated change also selected different
places: twelve of the twenty largest integrated contributors lay outside the
top hundred by mean trend. Shared first-detection increases in 2017 and 2023
leave product effects on recent records unresolved, and all results describe a
masked, quantised satellite product rather than ground illumination or
biological effects. Reporting boundary and interior change separately,
alongside annual records, turns a national trend into specific places and
explanations to investigate.

### End of Introduction (replaces R2's last paragraph)

We used Australia's 2024 protected-area estate to ask where measured radiance
increased and decreased during 2013–2024, and how concentrated those changes
were. We compared reserves with surrounding unprotected land, divided each
reserve's change into boundary and interior components, and examined the sites
behind the largest contributions. Most of the increase lay within a kilometre
of reserve boundaries. Most of the remainder, and nearly all of the decrease,
came from a handful of sites inside or beside reserves where infrastructure was
being built, operated or retired. Annual histories show what full-period trends
leave out.

(Move R2's closing caveat sentence, "The analysis concerns satellite upward
radiance...", to the end of the previous paragraph.)

### Results 3.3: Kosciuszko, after the cluster-location sentences

The increase is unlikely to be a product artefact. It began in 2021, before the
2022 change in source processing, under the same product version as the
preceding years (summed values 1,150 in 2020 and 4,600 in 2021). It grew in
each later year, and it was confined to two clusters rather than spread across
the park as a change in detection sensitivity would be.

(In 4.2, delete "The endpoint difference also spans product changes." Keep the
call for independent observations and construction records.)

### Results 3.3: decreases (replaces R2's paragraph beginning "Across whole reserves")

Across whole reserves, gross positive OLS slopes summed to 2,709 product
units × km² per year, and gross negative slopes to −2,231. Thirty reserves
supplied half of the positive contribution and 115 supplied 80%; Kosciuszko
supplied 13.6%. Decreases were more concentrated still. Five reserves supplied
94.9% of the gross decrease, and the three largest each coincide with
documented changes at oil and gas facilities on or beside reserves. Barrow
Island Nature Reserve (55.6%), which hosts the Gorgon gas project, tripled its
summed radiance in 2016, the year production began, at a single cluster on
its east coast, then declined [chevron2016; wagov2016]. Murujuga National Park
(34%) lost 86% of its summed radiance between 2013 and 2024, almost all at one
cluster on the Burrup Peninsula, while flaring at the adjacent Karratha Gas
Plant fell to under a tenth of its 2013 peak [woodside2025; verify]. Thevenard
Island Nature Reserve fell from 3,370 summed units to zero after oil
production there ceased in 2014 [chevron2023]. With these five reserves
excluded, the net slope was positive in both periods: +2,596 for 2013–2024 and
+1,922 for 2013–2021, against +479 and −538 with them included. The national
net therefore tracks a few facilities more closely than the condition of the
estate.

### Discussion: management implications (new paragraph, after 4.1's first paragraph)

The two patterns point to different management levers. Change in the boundary
zone is largely a matter for land-use planning and lighting control in
adjoining land. Australia's National Light Pollution Guidelines for Wildlife
already ask for lighting impacts to be assessed where a project lies within
20 km of important habitat [dcceew2023; verify wording]. Concentrated interior
change arises at a few developments operating, under construction or being
decommissioned within or beside reserves, where lighting can be addressed
through project approvals and their conditions. For those sites, an annual
satellite record gives an independent account of when measured light began,
how it grew and when it stopped, as it did for Snowy 2.0, Gorgon and Thevenard
Island. Neither use requires the satellite signal to measure ecological
exposure. Both require national screening to report boundary and interior
change separately rather than fold them into a single reserve-wide trend.

### Closing paragraph (replaces R2's final paragraph)

Most of Australia's protected estate shows no detectable light, and no
measurable change, in this product. Where measured light did increase between
2013 and 2024, it did so overwhelmingly at reserve margins and at a handful of
development sites within reserves, while the largest decreases came from oil
and gas facilities scaling back or shutting down. These are different stories
that call for different responses, and a single national trend tells neither.
A screen that keeps boundary, interior and annual records separate can tell
both.

## Compression (suggested)

- **3.2, third paragraph (matched Sen bands):** keep one sentence ("A separate
  matched comparison of band slopes gave the same picture: of 150 positive
  whole-reserve trends, 100 were positive only in the outer kilometre (Tables
  S3–S4).") and move the rest to SI.
- **3.3, last paragraph (polygon area shares):** two sentences at most, or
  move to SI S4. It is a third framing, and the budget has superseded it.
- **3.4, trajectories paragraph:** keep Black Mountain (dimming within Q3) and
  move the rest to the SI figure caption.

## Figures

- **Fig. 4.** In panel c, mark the 2022 source change with a vertical line and
  label the 2021 rise; that answers the product question visually. Consider
  noting "construction began 2019 (Lobs Hole), late 2020 (Tantangara)" in the
  caption, with sources.
- **Fig. 2.** Effective as it stands. In panel c, labelling two or three
  urban-fringe reserves near the diagonal's top (for example Neerabup) would
  show the other end of the contrast.
- **Possible new Fig. 1 panel.** A national map of reserve contributions
  (positive and negative integrated slopes, sized by magnitude, with the named
  sites labelled) would show the editor where the change is in one glance. I am
  building a candidate in my owned outputs.

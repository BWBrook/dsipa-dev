# Proposal: put the light budget at the centre (Claude, 18 October 2026)

Draft text for Astra to adopt, adapt or reject. It responds to Astra's first
rewrite, as it stood at 18 October 03:42, and builds on the additive budget in
`analysis/reports/brightening_budget/`. Numbers are from `summary.json` and
`hotspots.json`. Items marked [verify] need a primary source before use.

## Diagnosis of the first rewrite

The rewrite fixes the structure: a governing question, spatial results first,
and caveats gathered in one place. It still lacks the spark Barry asked for,
for one reason. The abstract asks "how much change underlies the national
total?" and then answers with area shares and sign counts, which describe
reserves, not change. So every result remains a statement about what a metric
conceals. There is no named place and nothing a reader would repeat to a
colleague. The budget supplies both, and it answers the abstract's own
question directly.

## Proposed spine

Where, within and around Australia's protected areas, did measured night-time
light increase between 2013 and 2024? There are three findings:

1. **At the edges.** The outermost kilometre of reserves covers 14% of
   assessable reserve area but carries 72% of the gross increase in
   area-integrated product radiance (83% for 2013–2021, before the product
   change; 71% by period difference). Of 596 reserves with brightening
   surroundings, 249 show no positive inside trend.
2. **From within, at a few sites.** The remaining 28% is concentrated in a
   handful of large reserves: two supply half of it and seven supply 80%. The
   largest is Kosciuszko National Park, where 96.5% of the 2019–2024 increase
   sits in two clusters that were dark in 2019. They coincide with the Lobs
   Hole and Tantangara construction areas of the Snowy 2.0 pumped-hydro
   project [verify]. Kosciuszko alone supplies 77% of the estate-wide net
   increase, yet ranks 303rd of 420 on the reserve-average trend. The largest
   decreases are also at industrial sites: Barrow Island, with the Gorgon LNG
   plant's 2016 start-up [verify]; Murujuga, on the Burrup Peninsula beside
   the gas plants [verify]; and former oil and gas or mining sites. Five
   reserves supply 95% of the gross decrease.
3. **Through a changing instrument.** Lit pixels doubled, with steps in 2017,
   2020 and 2023 that are shared across reserves. Most trends survive these
   steps: 76% of positive trends stay positive after removing the 2017 and
   2023 level shifts. But the latest detections cannot be read as new lighting
   without product checks.

The consequence for monitoring: a reserve-average trend is good at finding
edge change near towns, and poor at finding intense change at one site inside
a large reserve. An area-integrated budget does the reverse. A national screen
needs both, plus the annual record.

## Title options

- Reserve edges and a few development sites dominate measured lighting change in Australia's protected areas
- Where Australia's protected areas are brightening: edges, and a few sites within
- Keep Astra's "Beyond reserve-wide trends: ..." if the editor-facing finding moves into the abstract's first lines.

## Proposed abstract (about 290 words)

Satellite night-lights let conservation agencies screen entire protected-area
estates for changes in artificial light, but reserve-wide trends say little
about where change occurs or how much of it there is. We combined reserve-level
trends with an additive budget of area-integrated radiance for 2013–2024 across
Australia's 2024 protected estate. Of 11,133 reserves, 4,426 (39.8%) had enough
satellite support to assess, together holding 99.8% of summed reserve area.
Measured increases were concentrated in two kinds of place. The outermost
kilometre of reserves held 14% of assessable area but 72% of the gross increase
in measured light. Of 596 reserves whose surrounding land brightened, 249 showed
no rise inside. Most of the remaining increase came from a few sites deep inside
large reserves. Kosciuszko National Park, where new light appeared at two sites
coinciding with Snowy 2.0 pumped-hydro construction areas, supplied 77% of the
estate-wide net increase, yet ranked 303rd of 420 brightening reserves on its
reserve-average trend. The largest decreases were likewise at industrial
sites, led by Barrow Island, home of the Gorgon LNG plant. Reserve-average
trends and area-integrated budgets therefore detect different change: the
first highlights small reserves near existing light, the second intense change
inside large reserves. Annual records added a third layer. 180 reserves with
zero full-period trends changed from year to year, but detection steps in
2017, 2020 and 2023, shared across reserves, mean recent detections need
product checks before they are read as new lighting. National monitoring of
protected-area light should therefore report where change lies relative to
boundaries, how concentrated it is, and its annual record, rather than a single
trend summary.

(The 10-unit floor, coverage limits and optics caveat belong in the first
paragraph of the Discussion, stated once.)

## Proposed Results section (to follow coverage, replacing the area-share subsection as the main "how much" result)

### Where the increase in measured light occurred

Because reserve-mean trends cannot be summed, we also summed radiance over each
reserve's valid pixels, weighting by cell area (Methods). Across 4,426
assessable reserves, these totals rose in 560 reserves and fell in 75. Gross
gains and losses nearly cancelled, since each was dominated by a few sites.
Thirty reserves supplied half of the gross increase, and 115 supplied 80% (Fig.
X a). Reserves within 2 km of light already detected in 2013 supplied 98% of the
increase; reserves more than 20 km from any 2013 detection held 43% of
assessable area and supplied 0.8%.

Most of the increase lay at reserve margins. The outermost kilometre held 14%
of assessable area but 72% of the gross increase, and 83% before the 2022
product change. Among 221 brightening reserves with at least 10 valid pixels
beyond 1 km, 192 had most of their increase in the outer kilometre, which made
up 9% of their area. This boundary zone includes light from just outside
reserves that the sensor's ~750 m footprint spreads across the boundary; it
locates measured change, not its source.

The remaining 28% of the increase, deeper than 1 km, came almost entirely from
a few large reserves. Kosciuszko National Park supplied 47% of it. The park's
summed radiance stayed within 1,120–1,470 product units from 2013 to 2020, then
rose to 26,970 by 2024. Two clusters that were dark in 2019 held 96.5% of the
2019–2024 increase. Seven reserves supplied 80% of the interior increase,
including four Indigenous Protected Areas and Yellabinna Regional Reserve. These
increases are invisible to reserve-mean screening: Kosciuszko's mean slope
ranked 303rd of 420 positive trends, and 12 of the 20 largest contributors to
the total increase ranked outside the top 100 by mean slope (Fig. X b).

Decreases were more concentrated still. Five reserves supplied 95% of the gross
decrease, led by Barrow Island (56%) and Murujuga National Park (34%). Barrow
Island's summed radiance tripled in 2016 at a single cluster on its east coast
before declining.

## Notes for integration

- **Units.** Call the quantity area-integrated product radiance over valid
  support, not emitted light. Overlapping designations are counted in each
  reserve; say so in Methods.
- **Indigenous Protected Areas.** IPAs hold 51% of assessable area, 36% of the
  beyond-1 km increase and 6% of the outer-kilometre increase. Light inside
  IPAs comes largely from communities and permitted land uses on Country. The
  text must not frame it as encroachment, and I would not single out IPAs in
  the abstract. Barry may want a view on wording.
- **Attribution.** The Snowy 2.0, Gorgon, Murujuga, Jacinth–Ambrosia and
  Groote Eylandt identifications are location coincidences. They need primary
  sources (project approvals, company or government documents) and the wording
  "coincide with". The paper should not imply environmental harm or
  wrongdoing.
- **Figures.** Candidate figure: `fig_brightening_budget.png`
  (concentration curve; mean-trend rank against total-change rank). A map
  inset of the two Kosciuszko clusters would make a strong Fig. 1 panel.
- **Gross only.** The net-change ratios and the reserve bootstrap are not
  used; edge fractions use gross or reserve-level splits only.
- **Sensitivity.** The four reserves with changing valid counts were excluded
  as a check, with no material change (190 of 219 in place of 192 of 221).

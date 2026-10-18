# Additive brightening budget — 18 October 2026 (Claude)

> **Superseded statements, with corrections.** Astra's independent review and
> replay (board discussion 90, messages 1956–2001) corrected several
> exploratory claims below. The integrated R2 Methods S4 and Table S6 define
> the accepted version.
> - Kosciuszko's "77% of net" is not a headline, because gains and losses
>   nearly cancel. Use 13.6% of reserve-level gross and 47.1% of the
>   beyond-1 km band-level gross.
> - "303rd of 420" mixed a Sen-slope rank with an OLS rank. The matched OLS
>   ranks are 286th by mean and 1st by integrated slope.
> - 96.4% is of summed positive pixel differences (25,180 of 26,110), an
>   endpoint comparison distinct from the trend budget.
> - The level-shift removal is an exploratory calendar-step sensitivity. It
>   is not a product correction, and it gives no bound on environmental
>   brightening.
> - Edge shares use band-level gross: 72.0% overall, 82.5% for 2013–2021,
>   71.5% by period difference, and 51.2% in the 1,398 reserves with
>   supported interiors.
> - Added since: excluding the five largest-decrease reserves, the net is
>   positive in both periods (+2,596 and +1,922). Murujuga and Thevenard
>   Island decreases sit at single clusters (hotspots.json). The national
>   contribution map is fig_brightening_map.png.

Exploratory analysis authorised by Barry on 18 October (new analyses and
display items need no prior approval). Not yet in the manuscript.

## Why

Sen slopes on reserve-mean radiance cannot be summed across reserves or bands,
so the paper could not say where the estate-wide change sits. Total measured
radiance can be summed: annual inside mean × valid pixels × cell area, with the
15 arc-second cell scaled by cos(centroid latitude). The modelled cell area
(median 0.1859 km² for reserves over 100 km²) matches polygon area per valid
pixel (0.1858 km²). OLS slopes and period differences of these totals add up
across reserves and bands; the outer 1 km band plus the remainder reproduce
whole-reserve totals (minimum remainder −2e-12).

## Results (4,426 assessable reserves; OLS slope of totals, 2013–2024)

- Gross increase +2,709, gross decrease −2,231, net +479 (product units × km² per year).
- Concentration: 30 reserves supply 50% of the gross increase, 115 supply 80%,
  and 192 supply 90%. The top 44 (1%) supply 58%.
- Reserves within 2 km of light detected in 2013 supply 98.1% of the gross
  increase; reserves more than 20 km away hold 43% of area and supply 0.8%.
- Reserves over 1,000 km² hold 88% of area and 32% of the gross increase.
- Kosciuszko National Park supplies 77% of the net increase and 14% of the
  gross. Its Sen slope on mean radiance ranks 303rd of 420 positive trends.
  Two clusters that were dark in 2019 hold 96.5% of its 2019–2024 pixel-level
  increase: 35.783°S 148.414°E (70%) and 35.791°S 148.657°E (26%). These lie
  near the Snowy 2.0 Lobs Hole (main access tunnel) and Tantangara sites;
  locations are checked only against secondary sources so far.
- Barrow Island Nature Reserve has the largest decrease (−1,241; 56% of the
  gross decrease). Its 2016 radiance tripled at one cluster (20.779°S
  115.442°E), consistent with the Gorgon LNG plant, where production began in
  March 2016.
- Single-site increases inside other large reserves: Yellabinna (100% at
  30.870°S 132.220°E) and Anindilyakwa (77% at 13.988°S 136.454°E). Probable
  mine sites; not yet verified.
- Only 6 of the top 20 reserves by total change are also in the top 20 by mean
  trend; 12 of the top 20 by total are outside the top 100 by mean.
- Edge, estate-wide: of 284 brightening reserves with an interior beyond 1 km,
  255 have most of their increase in the outer kilometre, which is 9.5% of
  their area; the outer kilometre carries 57% of their summed increase. The 29
  interior-dominated cases are mostly Indigenous Protected Areas plus
  Kosciuszko and Yellabinna.
- Product steps: lit pixels in assessable reserves rose from 7,151 to 14,664.
  Reserves with a lit-pixel jump of 30% or more numbered 39 in 2016–2017, 18 in
  2019–2020 and 26 in 2022–2023, against 0–9 in other transitions. Of 420
  positive Sen slopes, 319 (76%) stay positive after removing level shifts at
  2017 and 2023, 254 (60%) after removing 2017, 2020 and 2023, and 332 (79%)
  are positive within 2017–2022 alone.

## Caveats

- Totals inherit the product's 10-unit floor, background masking and spectral
  limits; sub-floor light is invisible.
- OLS on totals is sensitive to single-year spikes (Barrow Island 2016); the
  2013–2021 slopes and period differences are reported as sensitivity.
- Net-change ratios (for example, the outer-km share of net change) are
  unstable because gross gains and losses nearly cancel; use gross or
  reserve-level splits.
- The outer kilometre includes light bleeding in from outside (about a 750 m
  footprint), so edge statements locate measured change in a boundary zone,
  not its source.
- Cluster locations coincide with mapped development sites; attribution in
  the paper needs primary sources. Light inside Indigenous Protected Areas
  often comes from communities and permitted land uses and must not be framed
  as encroachment.

## Files

`analysis/brightening_budget.py` (budget), `analysis/brightening_hotspots.py`
(Zenodo COG windows, pixel clusters), `analysis/render_brightening_budget.py`
(figure). Outputs: `summary.json` (with input SHA-256), `reserve_budget.csv`,
`concentration_curve.csv`, `top20_contributors.csv`, `budget_by_*.csv`,
`hotspots.json`, `fig_brightening_budget.png`.

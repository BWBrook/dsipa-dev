# Exploratory edge-band follow-up

Generated: 2026-09-19T06:03:27.208544+00:00

This is an exploratory follow-up to the accepted 1--5 km sensitivity audit. It reconstructs a matched cohort of 1,341 reserves, adds the exact 0--1 km ring, and reports annual zero/nonzero status. All ring summaries use the project thresholds of 10 valid pixels per year and 8 valid years. Sen slopes are reported separately by spatial support and are not treated as additive.

The matched cohort contains 1,341 reserves. The 0--1 km ring is available for 1,341 of them. Of the original Q1 reserves, 85 lose a positive sign in the 1--5 km band and 27 retain it. All 85 Q1 losses have exactly zero band slope, but only 73 are all-zero annual histories; the remainder have nonzero annual histories whose median pairwise slope is zero. The Q1 losses have summed polygon area 66,435.592 km2, or 10.33% of all positive whole-reserve polygon area and 3.88% of eligible-reserve polygon area. Their median band slope is 0, median whole slope is 0.0104112, and median polygon area is 132.759 km2; corresponding Q1-kept medians are 0.0310559, 0.0562566, and 203.891 km2. This is a spatial-support comparison, not proof that change is boundary-localised.

## Whole, 0--1 km, and 1--5 km signs

whole_sign ring_0_1km_sign ring_1_5km_sign    n
      zero            zero            zero 1178
  positive        positive            zero  100
  positive        positive        positive   38
  negative        negative            zero    9
  positive            zero            zero    7
  positive            zero        positive    4
  negative        negative        negative    2
  negative            zero            zero    1
  positive            zero        negative    1
      zero        negative            zero    1

## Annual zero/nonzero status

   ring            status    n  median_n_years
0--1 km   all_annual_zero 1100            12.0
0--1 km has_positive_year  241            12.0
1--5 km   all_annual_zero 1270            12.0
1--5 km has_positive_year   71            12.0

A zero Sen slope is not equivalent to an all-zero annual series. The annual status table separates all-zero histories from histories containing at least one positive year.

Among the 100 whole-positive reserves with a positive 0--1 km sign and zero 1--5 km sign, 86 are all-zero annual 1--5 km histories and 14 contain nonzero annual values.

## Positive whole-reserve area by slope tercile

whole_slope_tercile   n      area_km2  slope_min  slope_median  slope_max  area_share_positive_whole
             T1_low 140 637619.968147   0.000034      0.006127   0.039954                   0.991470
          T2_middle 140   4094.263805   0.040323      0.142879   0.309959                   0.006366
            T3_high 140   1391.407825   0.310390      0.676394   8.149718                   0.002164

Tercile cutpoints are 0.0401998331 and 0.31010277 product-scaled units per year. Values equal to a quantile boundary are assigned to the lower tercile. Ties at the boundaries: 0 and 0.

Area is summed protected-area polygon area and can double-count overlapping designations; it is not unique illuminated land area. Missing 5--10 km summaries indicate unavailable valid raster summaries under the threshold, not geometric absence of the ring. The annual summaries are descriptive and do not establish whether zero/nonzero patterns reflect product processing or environmental change.

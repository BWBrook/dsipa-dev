# Layer A sanity dashboard

Generated: 2026-05-25 03:35 UTC

Minimum valid pixels: 10
Alternative threshold: 50

## Invariants

valid_fraction within [0,1]: True
valid_pixel_count >= 0: True
mean >= 0 (ignoring NaN): True
frac_gt0 within [0,1] (ignoring NaN): True
p95 >= median >= min (valid rows): True

## Anchor checks (explicit bright/dark contexts)

Anchors are defined from PA/radiance evidence, not from nearest-city medians. This avoids the earlier failure mode where many remote PAs were still assigned to a major city label.

- Urban-adjacent inside PAs (<=20 km): n=63, mean median=22.903, mean p95=112.769, fraction mean>0=0.889, median distance=12.9 km
- Remote inside PAs (>=300 km): n=1520, mean median=0.000, mean p95=0.167, fraction mean>0=0.098, median distance=478.9 km
- Top non-zero inside PAs by 2024 mean (top 50): n=50, mean median=41.630, mean p95=132.143, fraction mean>0=1.000, median distance=18.4 km
- Top non-zero 1 km buffer contexts by 2024 mean (top 50): n=50, mean median=230.196, mean p95=619.566, fraction mean>0=1.000, median distance=15.1 km

Top inside bright-context rows (2024):

    pa_id                         NAME STATE    mean   p95  frac_gt0  distance_km nearest_city
 WA_27575                     Neerabup    WA 190.339 418.0       1.0       33.304        Perth
  WA_1720                   Kings Park    WA 158.750 392.0       1.0        3.021        Perth
 VIC_4007 Craigieburn Grassland N.C.R.   VIC 145.714 320.0       1.0       21.694    Melbourne
 WA_48327                Canning River    WA 115.556 211.0       1.0        8.869        Perth
 WA_48325                   Swan River    WA 113.434 382.5       1.0        4.210        Perth
NSW_N0083                    Lane Cove   NSW 113.333 352.0       1.0       13.997       Sydney
   ACT_09       Jerrabomberra Wetlands   ACT 107.692 166.0       1.0        4.185     Canberra
 WA_21708               Lake Joondalup    WA  95.200 214.0       1.0       24.606        Perth

Anchor sanity verdicts:

- urban p95 > remote p95: True (112.769 vs 0.167)
- bright-context median > remote p95: True (41.630 vs 0.167)

## Sensitivity checks

Mean vs median correlation (inside): 0.938
Fraction inside with >= 10 valid pixels: 0.398
Fraction inside with >= 50 valid pixels: 0.197

## Floor/selection summary (inside)

Inside rows with >= 10 valid pixels: n=53112
Fraction mean==0: 0.895
Fraction median==0: 0.973
Fraction frac_gt0==0: 0.895
Fraction p95==0: 0.939

Fraction with non-zero exposure by distance band + area quartile:

    distance_band area_quartile  n_pa  mean_gt0  median_gt0  frac_gt0_gt0  p95_gt0
    mid_100_300km            Q3   951     0.035       0.012         0.035    0.034
    mid_100_300km            Q4  1307     0.090       0.003         0.090    0.027
    peri_20_100km            Q3   297     0.169       0.107         0.169    0.168
    peri_20_100km            Q4   288     0.315       0.076         0.315    0.204
remote_300km_plus            Q3   367     0.044       0.008         0.044    0.038
remote_300km_plus            Q4  1153     0.089       0.003         0.089    0.023
     urban_0_20km            Q3    35     0.824       0.686         0.824    0.819
     urban_0_20km            Q4    28     0.946       0.714         0.946    0.905

## Ring missingness

ring_index
0     80496
1    116472
2    129000

Fraction of PA-years with complete ring coverage: 0.087

## Stratified inside vs buffer (median of means)

Bands: urban<=20 km, peri=20–100 km, mid=100–300 km, remote>=300 km; area quartiles computed across all PAs.

### Stratified inside vs buffer (1 km, land_unprotected) — year 2024

    distance_band area_quartile  buffer_1.0km_mean  inside_mean  inside_minus_buffer_1.0km
    mid_100_300km            Q3              0.000        0.000                      0.000
    mid_100_300km            Q4              0.000        0.000                      0.000
    peri_20_100km            Q3              0.000        0.000                      0.000
    peri_20_100km            Q4              0.000        0.000                      0.000
remote_300km_plus            Q3              0.000        0.000                      0.000
remote_300km_plus            Q4              0.000        0.000                      0.000
     urban_0_20km            Q3             51.713       25.926                    -25.787
     urban_0_20km            Q4             39.857       22.891                    -16.966

### Stratified inside vs buffer (5 km, land_unprotected) — year 2024

    distance_band area_quartile  buffer_5.0km_mean  inside_mean  inside_minus_buffer_5.0km
    mid_100_300km            Q3              0.000        0.000                      0.000
    mid_100_300km            Q4              0.000        0.000                      0.000
    peri_20_100km            Q3              0.000        0.000                      0.000
    peri_20_100km            Q4              0.149        0.000                     -0.149
remote_300km_plus            Q3              0.000        0.000                      0.000
remote_300km_plus            Q4              0.000        0.000                      0.000
     urban_0_20km            Q3             70.764       25.926                    -44.838
     urban_0_20km            Q4             54.723       22.891                    -31.832


## Conditional inside vs buffer (urban proximity)

Conditional inside vs buffer (1 km, land_unprotected; year 2024)
- PAs within 20 km of city: n=58, fraction buffer>inside=0.914
- Non-zero subset (inside>0 or buffer>0): n=54, fraction buffer>inside=0.981
Plot: layerA_sensitivity_mean_vs_median.png
# Layer A sanity dashboard

Generated: 2026-01-04 01:14 UTC

Minimum valid pixels: 10
Alternative threshold: 50

## Invariants

valid_fraction within [0,1]: True
valid_pixel_count >= 0: True
mean >= 0 (ignoring NaN): True
frac_gt0 within [0,1] (ignoring NaN): True
p95 >= median >= min (valid rows): True

## Anchor checks (inside mean radiance, by distance bands)

Year 2013: urban (<=20 km) median=15.185, remote (>=300 km) median=0.000
Year 2018: urban (<=20 km) median=21.389, remote (>=300 km) median=0.000
Year 2024: urban (<=20 km) median=22.903, remote (>=300 km) median=0.000

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
# Layer A sanity dashboard

Generated: 2026-01-02 02:29 UTC

Minimum valid pixels: 10
Alternative threshold: 50

## Invariants

valid_fraction within [0,1]: True
valid_pixel_count >= 0: True
mean >= 0 (ignoring NaN): True

## Anchor checks (inside mean radiance, by distance bands)

Year 2013: urban (<=20 km) median=15.185, remote (>=300 km) median=0.000
Year 2018: urban (<=20 km) median=21.389, remote (>=300 km) median=0.000
Year 2024: urban (<=20 km) median=22.903, remote (>=300 km) median=0.000

## Sensitivity checks

Mean vs median correlation (inside): 0.938
Fraction inside with >= 10 valid pixels: 0.398
Fraction inside with >= 50 valid pixels: 0.197

## Ring missingness

ring_index
0     80496
1    116820
2    129168

## Stratified inside vs buffer (median of means)

Bands: urban<=20 km, peri=20–100 km, mid=100–300 km, remote>=300 km; area quartiles computed across all PAs.

### Stratified inside vs buffer (1 km) — year 2024

    distance_band area_quartile  buffer_1.0km_mean  inside_mean  inside_minus_buffer_1.0km
    mid_100_300km            Q3              0.000        0.000                      0.000
    mid_100_300km            Q4              0.000        0.000                      0.000
    peri_20_100km            Q3              0.000        0.000                      0.000
    peri_20_100km            Q4              0.000        0.000                      0.000
remote_300km_plus            Q3              0.000        0.000                      0.000
remote_300km_plus            Q4              0.000        0.000                      0.000
     urban_0_20km            Q3             50.702       25.926                    -24.776
     urban_0_20km            Q4             39.149       22.891                    -16.258

### Stratified inside vs buffer (5 km) — year 2024

    distance_band area_quartile  buffer_5.0km_mean  inside_mean  inside_minus_buffer_5.0km
    mid_100_300km            Q3              0.000        0.000                      0.000
    mid_100_300km            Q4              0.000        0.000                      0.000
    peri_20_100km            Q3              0.051        0.000                     -0.051
    peri_20_100km            Q4              0.199        0.000                     -0.199
remote_300km_plus            Q3              0.000        0.000                      0.000
remote_300km_plus            Q4              0.000        0.000                      0.000
     urban_0_20km            Q3             69.847       25.926                    -43.921
     urban_0_20km            Q4             50.619       22.891                    -27.728

Plot: layerA_sensitivity_mean_vs_median.png
# Layer A sanity dashboard

Generated: 2026-01-01 09:53 UTC

Minimum valid pixels: 10
Alternative threshold: 50

## Invariants

valid_fraction within [0,1]: True
valid_pixel_count >= 0: True
mean >= 0 (ignoring NaN): True

## Anchor checks

Year 2013: urban median=15.185, remote median=0.000
Year 2018: urban median=21.389, remote median=0.000
Year 2024: urban median=22.903, remote median=0.000

## Sensitivity checks

Mean vs median correlation (inside): 0.938
Fraction inside with >= 10 valid pixels: 0.398
Fraction inside with >= 50 valid pixels: 0.197

## Ring missingness

ring_index
0     80496
1    116820
2    129168

Plot: layerA_sensitivity_mean_vs_median.png
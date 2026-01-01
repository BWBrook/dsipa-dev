# National Layer A coverage and sanity report

Generated: 2026-01-01 09:52 UTC

## Raster metadata (per year)
- 2013: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2014: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2015: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2016: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2017: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2018: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2019: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2020: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2021: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2022: dtype=int16, nodata=-32768.0, scale=10.0, offset=0.0
- 2023: dtype=int16, nodata=-32768.0, scale=10.0, offset=0.0
- 2024: dtype=int16, nodata=-32768.0, scale=10.0, offset=0.0

Minimum valid pixels per zone: 10

## Coverage by zone (fraction with valid pixels)

Note: buffer_km=-1 denotes inside-zone rows.
 year   zone  buffer_km  valid_ok
 2013 buffer        1.0  0.998742
 2013 buffer        5.0  0.998742
 2013 inside       -1.0  0.397557
 2014 buffer        1.0  0.998742
 2014 buffer        5.0  0.998742
 2014 inside       -1.0  0.397557
 2015 buffer        1.0  0.998742
 2015 buffer        5.0  0.998742
 2015 inside       -1.0  0.397557
 2016 buffer        1.0  0.998742
 2016 buffer        5.0  0.998742
 2016 inside       -1.0  0.397557
 2017 buffer        1.0  0.998742
 2017 buffer        5.0  0.998742
 2017 inside       -1.0  0.397557
 2018 buffer        1.0  0.998742
 2018 buffer        5.0  0.998742
 2018 inside       -1.0  0.397557
 2019 buffer        1.0  0.998742
 2019 buffer        5.0  0.998742
 2019 inside       -1.0  0.397557
 2020 buffer        1.0  0.998742
 2020 buffer        5.0  0.998742
 2020 inside       -1.0  0.397557
 2021 buffer        1.0  0.998742
 2021 buffer        5.0  0.998742
 2021 inside       -1.0  0.397557
 2022 buffer        1.0  0.998742
 2022 buffer        5.0  0.998742
 2022 inside       -1.0  0.397557
 2023 buffer        1.0  0.998742
 2023 buffer        5.0  0.998742
 2023 inside       -1.0  0.397557
 2024 buffer        1.0  0.998742
 2024 buffer        5.0  0.998742
 2024 inside       -1.0  0.397557

## Coverage by ring (fraction with valid pixels)

 year  ring_index  valid_ok
 2013           0  0.397467
 2013           1  0.125573
 2013           2  0.033145
 2014           0  0.397467
 2014           1  0.125573
 2014           2  0.033145
 2015           0  0.397467
 2015           1  0.125573
 2015           2  0.033145
 2016           0  0.397467
 2016           1  0.125573
 2016           2  0.033145
 2017           0  0.397467
 2017           1  0.125573
 2017           2  0.033145
 2018           0  0.397467
 2018           1  0.125573
 2018           2  0.033145
 2019           0  0.397467
 2019           1  0.125573
 2019           2  0.033145
 2020           0  0.397467
 2020           1  0.125573
 2020           2  0.033145
 2021           0  0.397467
 2021           1  0.125573
 2021           2  0.033145
 2022           0  0.397467
 2022           1  0.125573
 2022           2  0.033145
 2023           0  0.397467
 2023           1  0.125573
 2023           2  0.033145
 2024           0  0.397467
 2024           1  0.125573
 2024           2  0.033145

## Anchor checks (inside mean)

Year 2013:
- Urban-adjacent (<=20 km): n=377, median mean=15.185
- Remote (>=300 km): n=2738, median mean=0.000
- Top city medians: Adelaide=0.000, Brisbane=0.000, Canberra=0.000

Year 2018:
- Urban-adjacent (<=20 km): n=377, median mean=21.389
- Remote (>=300 km): n=2738, median mean=0.000
- Top city medians: Adelaide=0.000, Brisbane=0.000, Canberra=0.000

Year 2024:
- Urban-adjacent (<=20 km): n=377, median mean=22.903
- Remote (>=300 km): n=2738, median mean=0.000
- Top city medians: Adelaide=0.000, Brisbane=0.000, Canberra=0.000


## Inside vs buffer sanity

Fraction with buffer1 mean > inside mean: 0.153 (n=53112)

Plot: national_layerA_distributions.png
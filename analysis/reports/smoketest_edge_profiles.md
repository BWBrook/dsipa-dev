# Smoke-test edge profile report

Generated: 2026-01-01 07:47 UTC

## Raster metadata (per year)
- 2013: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2018: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2024: dtype=int16, nodata=-32768.0, scale=10.0, offset=0.0

Note: Statistics computed on raw stored values (no scale/offset applied).

## Summary by ring

                 mean                                                median                                    valid_pixel_count                                                  
                count   mean    std  min    25%    50%    75%    max  count mean  std  min  25%  50%  75%  max             count     mean      std   min   25%   50%    75%    max
year ring_index                                                                                                                                                                   
2013 0            3.0  0.067  0.116  0.0  0.000  0.000  0.101  0.201    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  234.000  314.457  45.0  52.5  60.0  328.5  597.0
     1            3.0  0.000  0.000  0.0  0.000  0.000  0.000  0.000    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  185.667  312.949   1.0   5.0   9.0  278.0  547.0
     2            0.0    NaN    NaN  NaN    NaN    NaN    NaN    NaN    0.0  NaN  NaN  NaN  NaN  NaN  NaN  NaN               3.0    0.000    0.000   0.0   0.0   0.0    0.0    0.0
2018 0            3.0  0.186  0.170  0.0  0.111  0.222  0.279  0.335    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  234.000  314.457  45.0  52.5  60.0  328.5  597.0
     1            3.0  0.000  0.000  0.0  0.000  0.000  0.000  0.000    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  185.667  312.949   1.0   5.0   9.0  278.0  547.0
     2            0.0    NaN    NaN  NaN    NaN    NaN    NaN    NaN    0.0  NaN  NaN  NaN  NaN  NaN  NaN  NaN               3.0    0.000    0.000   0.0   0.0   0.0    0.0    0.0
2024 0            3.0  0.024  0.023  0.0  0.014  0.028  0.036  0.044    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  234.000  314.457  45.0  52.5  60.0  328.5  597.0
     1            3.0  0.000  0.000  0.0  0.000  0.000  0.000  0.000    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  185.667  312.949   1.0   5.0   9.0  278.0  547.0
     2            0.0    NaN    NaN  NaN    NaN    NaN    NaN    NaN    0.0  NaN  NaN  NaN  NaN  NaN  NaN  NaN               3.0    0.000    0.000   0.0   0.0   0.0    0.0    0.0

## Low pixel-count warnings (<10)

         pa_id triad_role  year  ring_index  valid_pixel_count
     TAS_50483 urban_edge  2013           2                  0
QLD_0117LZI001     remote  2013           1                  1
QLD_0117LZI001     remote  2013           2                  0
     NSW_N0856 peri_urban  2013           1                  9
     NSW_N0856 peri_urban  2013           2                  0
     TAS_50483 urban_edge  2018           2                  0
QLD_0117LZI001     remote  2018           1                  1
QLD_0117LZI001     remote  2018           2                  0
     NSW_N0856 peri_urban  2018           1                  9
     NSW_N0856 peri_urban  2018           2                  0
     TAS_50483 urban_edge  2024           2                  0
QLD_0117LZI001     remote  2024           1                  1
QLD_0117LZI001     remote  2024           2                  0
     NSW_N0856 peri_urban  2024           1                  9
     NSW_N0856 peri_urban  2024           2                  0

Note: rings with zero valid pixels across all triad PAs: [2].

Plot: smoketest_edge_profiles.png
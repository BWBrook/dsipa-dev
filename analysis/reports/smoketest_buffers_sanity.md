# Smoke-test radiance buffers sanity report

Generated: 2026-01-03 10:39 UTC

## Raster metadata (per year)
- 2013: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2018: dtype=int16, nodata=-32768.0, scale=1.0, offset=0.0
- 2024: dtype=int16, nodata=-32768.0, scale=10.0, offset=0.0

Note: Summary statistics are computed on scaled values (scale/offset metadata applied).

## Summary by zone

             mean                                                 median                                    valid_pixel_count                                                         
            count   mean    std  min    25%    50%    75%     max  count mean  std  min  25%  50%  75%  max             count     mean       std    min     25%    50%     75%     max
year zone                                                                                                                                                                             
2013 buffer   6.0  2.160  4.762  0.0  0.000  0.000  0.841  11.837    6.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               6.0  973.667  1055.094  104.0  266.25  754.5  1057.5  2967.0
     inside   3.0  0.035  0.061  0.0  0.000  0.000  0.052   0.105    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  419.667   627.396   46.0   57.50   69.0   606.5  1144.0
2018 buffer   6.0  2.190  4.685  0.0  0.002  0.040  1.046  11.689    6.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               6.0  973.667  1055.094  104.0  266.25  754.5  1057.5  2967.0
     inside   3.0  0.131  0.115  0.0  0.087  0.175  0.196   0.217    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  419.667   627.396   46.0   57.50   69.0   606.5  1144.0
2024 buffer   6.0  2.410  5.241  0.0  0.002  0.040  1.011  13.054    6.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               6.0  973.667  1055.094  104.0  266.25  754.5  1057.5  2967.0
     inside   3.0  0.194  0.221  0.0  0.074  0.149  0.292   0.435    3.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0               3.0  419.667   627.396   46.0   57.50   69.0   606.5  1144.0

## Anchor check (inside mean by triad role)

 year  peri_urban  remote  urban_edge
 2013         0.0   0.000       0.105
 2018         0.0   0.217       0.175
 2024         0.0   0.435       0.149

## Low pixel-count warnings (<10)

None

Plot: smoketest_buffers_summary.png
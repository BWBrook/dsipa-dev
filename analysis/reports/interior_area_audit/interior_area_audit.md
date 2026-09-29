# Interior-band and area sensitivity audit

Generated: 2026-09-19T06:03:23.518376+00:00

The original 1 km land-unprotected paired cohort is held fixed. Whole-reserve and 1 km-buffer slopes are taken from the manifest-provided (spatial-correction-20260919) trend table; only the exact 1--5 km ring slope is calculated here using the project Theil--Sen estimator, 10 valid pixels per year, and at least 8 valid years.

The exact 1--5 km ring is present in the manifest-provided (spatial-correction-20260919) edge table: **True**. The original paired cohort contains **4,253** PAs; **1,341** have a matched ring slope and **2,912** are excluded from ring transitions. All exclusions lacked a usable ring-year summary; no retained row had between 1 and 7 usable ring years.

## Quadrant transitions

original_quadrant ring_quadrant    n      area_km2  share_of_ring_matched_n  share_of_ring_matched_area
               Q1            Q1   27 139252.377649                 0.020134                    0.082874
               Q1            Q2    0      0.000000                 0.000000                    0.000000
               Q1            Q3    0      0.000000                 0.000000                    0.000000
               Q1            Q4   85  66435.591541                 0.063386                    0.039538
               Q2            Q1    0      0.000000                 0.000000                    0.000000
               Q2            Q2   15 214927.722779                 0.011186                    0.127911
               Q2            Q3   23 218984.686262                 0.017151                    0.130326
               Q2            Q4    0      0.000000                 0.000000                    0.000000
               Q3            Q1    0      0.000000                 0.000000                    0.000000
               Q3            Q2    0      0.000000                 0.000000                    0.000000
               Q3            Q3 1103 868013.028337                 0.822521                    0.516587
               Q3            Q4    0      0.000000                 0.000000                    0.000000
               Q4            Q1    0      0.000000                 0.000000                    0.000000
               Q4            Q2    0      0.000000                 0.000000                    0.000000
               Q4            Q3    0      0.000000                 0.000000                    0.000000
               Q4            Q4   88 172671.950810                 0.065623                    0.102763

Q1 means positive buffer and positive interior slope; Q2 means non-positive buffer and positive interior slope; Q3 means both non-positive; Q4 means positive buffer and non-positive interior slope. Areas are summed polygon areas and may double-count overlapping designations; they are not unique illuminated land areas.

## Whole-polygon area summary

         category     n     area_km2  share_of_all_ids  share_of_all_polygon_area  share_of_eligible_polygon_area
 all_geometry_ids 11133 1.713991e+06          1.000000                   1.000000                             NaN
       ineligible  6707 3.130681e+03          0.602443                   0.001827                             NaN
         positive   420 6.431056e+05          0.037726                   0.375209                             NaN
         negative    37 2.501910e+04          0.003323                   0.014597                             NaN
             zero  3969 1.042736e+06          0.356508                   0.608367                             NaN
eligible_negative    37 2.501910e+04          0.003323                   0.014597                        0.014624
    eligible_zero  3969 1.042736e+06          0.356508                   0.608367                        0.609480
eligible_positive   420 6.431056e+05          0.037726                   0.375209                        0.375896

The area summary is descriptive and preserves the study's reserve-level classification. A positive reserve-level slope does not imply that the whole polygon brightened uniformly.

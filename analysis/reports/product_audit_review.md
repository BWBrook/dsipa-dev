# Product-continuity and spatial-support audit — 17 September 2026

The specific hypothesis of a 2022 first-detection jump is not supported by the
observed diagnostics. This is a bounded descriptive conclusion, not validation
of homogeneous processing or environmental onset. The 78 late-positive series
remain product observations requiring investigation.

The 2021 and 2022 raw encodings differ, but the observed decoded low-end lattice
is identical: positive codes in the 2020–2021 window are multiples of 10 with
scale 1, whereas 2022–2024 use integer codes with scale 10. Both have minimum
positive value 10. The 2013 minimum is also 10, but one high code (434) prevents
asserting an identical lattice for every pixel in that earlier layer. Scale
metadata alone would have given the wrong inference about coarser quantisation.

The EOG 2022 source is a mixed Suomi-NPP/NOAA-20 V2.2 masked composite, with
changed low-coverage and background handling. The retained 2023–2024 source
names identify Suomi-NPP masked V2 inputs without specifying the minor version.
Earlier processing code supports V2.1 lineage for 2013–2021 but does not fully
reproduce the later deposit. See `product_lineage_review.md` and raw TIFF tags.

## Comparisons and their limits

- Inside first detections: 2021 13/3,877 (0.335%); 2022 14/3,864 (0.362%);
  2023 31/3,850 (0.805%); 2024 33/3,819 (0.864%). The 2022–2024 counts sum to the existing 78
  post-2021 first-positive cases. The largest earlier inside fraction was in
  2017 (53/3,982; 1.331%); this audit does not attribute that historical peak.
- Fixed >20 km-from-2013-light stratum: 2021 3/1,242; 2022 2/1,239;
  2023 1/1,237; 2024 6/1,236. Small event counts and shrinking risk sets matter.
- Both buffer widths have lower first-positive fractions in 2022 than 2021.
  Their cohorts are defined independently of inside eligibility, and overlapping
  buffers are not independent ecological replicates.
- On 149,331,864 pixels valid throughout 2020–2024 in the common rectangle,
  zero-to-positive transitions number 31,475 / 28,035 / 57,328 / 36,764 for
  2021 / 2022 / 2023 / 2024. The rectangle includes ocean and non-reserve land;
  it is a storage/product check, not an estimate of illuminated land area.
- Of the 14 inside first detections in 2022, 10 are positive in 2023 and 11
  in 2024. Thirteen have maximum decoded pixel value 10 in 2022, one 20.
  Near-floor values are common before the boundary too (51.4% of positive
  2021 window pixels and 51.8% of 2022 pixels take the lowest positive code).
- Only four estate IDs have changing valid-pixel counts. Excluding them leaves
  every 2022 distance-stratum result unchanged. Count stability does not prove
  identical pixel identities. The far-event distances in 2021 and 2022 are
  sufficiently beyond 20 km that a one-cell distance convention cannot change
  the far comparison; near/middle boundaries remain finite-resolution proxies.

The initial distance proposal leaked historical detections into their own
reference mask. The documented prospective amendment uses only 2013 light.
Neither distance, intermittency nor persistence uniquely identifies processing
versus environment. The audit contains no area-adjusted causal model or
calibrated test; no inference depends on exchangeability of the distance groups.

## Spatial support

The 1–5 km band is eligible in 1,205/3,858 originally paired reserves. Among
positive whole-reserve cases with a usable band, 23/91 Q1 and 9/28 Q2 retain
positive band slopes (32/119). Positive whole-reserve signs often do not persist
into that band, but this does not locate the change at a boundary: variation
within 0–1 km, beyond 5 km, isolated pixels and measurement support can all
contribute. Optical spillover is not identified. See the exact transition table
and area accounting in `interior_area_audit/`.

## Review and disposition

A bounded independent scientific review accepted the numerical comparisons and
required correction of the initial encoding-versus-quantum interpretation and
of overly strong boundary-localisation wording. Both were corrected before
acceptance. The frozen protocol hash accompanies the manifest. Targeted tests
cover first-event risk-set handling, missing histories and the band estimator.

An external anchor was authorised if necessary. It was not required for the
retained product-descriptive claims because the specific 2022 excess was absent.
Live EOG and NASA access probes found authentication requirements and no local
credentials; no account or external raster download was created. Environmental
onset claims would require further corroboration, regardless of model agreement.

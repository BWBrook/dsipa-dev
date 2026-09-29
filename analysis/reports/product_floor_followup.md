# Observed positive-pixel floor follow-up

Date: 18 September 2026

## Scientific conclusion

The minimum positive metadata-decoded pixel value observed in the fixed
Australian audit rectangle is **10 in every annual raster from 2013 through
2024**. Completing the previously unscanned 2014–2019 years therefore removes
the remaining empirical gap in the low-end storage check.

This is an observed floor in the retained Hengl/OpenGeoHub rasters. It is not a
calibrated sensor detection limit, an EOG masking threshold, or evidence that
all positive pixels lie on one common lattice. It also does not imply that a
protected-area or buffer mean must be at least 10.

## Evidence

The follow-up scanned the same 17,554 × 8,507 pixel window used in the accepted
product-continuity audit: columns 66,196–83,749 and rows 23,228–31,734 of each
global raster. The 149,331,878-cell rectangle contains surrounding non-reserve
land and ocean as well as protected areas. It is a product-storage diagnostic,
not the sampling frame for an ecological estimand.

| Year | Metadata scale | Minimum positive stored | Minimum positive decoded | Positive pixels | Decoded values off multiples of 10 |
|---:|---:|---:|---:|---:|---:|
| 2013 | 1 | 10 | 10 | 233,197 | 1 pixel: 434 |
| 2014 | 1 | 10 | 10 | 231,534 | 0 |
| 2015 | 1 | 10 | 10 | 231,254 | 0 |
| 2016 | 1 | 10 | 10 | 228,371 | 0 |
| 2017 | 1 | 10 | 10 | 282,032 | 0 |
| 2018 | 1 | 10 | 10 | 287,230 | 0 |
| 2019 | 1 | 10 | 10 | 293,163 | 4 pixels: 5,894; 17,714; 18,964; 25,534 |
| 2020 | 1 | 10 | 10 | 325,424 | 0 |
| 2021 | 1 | 10 | 10 | 338,602 | 0 |
| 2022 | 10 | 1 | 10 | 345,118 | 0 |
| 2023 | 10 | 1 | 10 | 390,418 | 0 |
| 2024 | 10 | 1 | 10 | 402,212 | 0 |

The 2013 and 2020–2024 rows come from the accepted
`product_raster_histograms.csv`; the new 2014–2019 rows are in
`product_floor_summary.csv`. Each off-lattice value occurred in one pixel and
was far above the floor. These exceptions do not alter the common minimum, but
they rule out claiming that every pre-2022 positive value is a multiple of 10.

## What the floor does and does not mean

For 2013–2021, scale 1 and integer storage make one-unit codes possible, yet no
positive code below 10 was observed in this Australian window. For 2022–2024,
the minimum raw code is 1 and metadata scale 10 decodes it to 10. Metadata
encoding and observed support are therefore distinct: the scale change did not
create a change in the observed minimum positive decoded value.

The result does not reveal why values below 10 are absent. The EOG source is a
background-masked annual composite, and the OpenGeoHub deposit also rescales
and integer-encodes it. The available provenance does not separate the
contributions of EOG masking, source precision, OpenGeoHub rescaling and
rounding to this floor.

Polygon means can validly fall between 0 and 10. They average positive and zero
pixels, so one decoded floor pixel among many valid pixels yields a positive
mean below the pixel floor. Accordingly, a late-positive reserve mean below 10
is not an off-lattice pixel and does not contradict this diagnostic.

## Units and provenance boundary

The [EOG Annual VNL documentation](https://eogdata.mines.edu/products/vnl/)
labels the native annual `average-masked` band as radiance in nW cm^-2 sr^-1.
The [Zenodo v0.4 record](https://zenodo.org/records/17294744) says only that the
original Annual VNL V2 values were converted from a 0–200 scale to a 0–2000
scale. That conversion statement does not explicitly assign physical units to
the retained 0–2000 numbers, and the deposit does not provide a complete final
COG-construction path. It would therefore be unsupported to equate a decoded
value of 10 with 1 nW cm^-2 sr^-1. The manuscript's term **product-scaled
radiance** remains the defensible unit description.

## Reproducibility receipt

The read-only scan ran on `deep-server` in tmux session
`dsipa-product-floor-20260918`, using the accepted Goal 012 source rasters at
`/data/codex/repos/dsipa-dev-goal012-20260723T115300Z`. It completed normally in
12.86 seconds. No accepted input or earlier audit output was modified.

- Script: `analysis/product_floor_scan.py`; SHA-256
  `b383bd6f8658b7af01fa54b2cd88d364284ce1e4a8f7a56fe19cb4ca957fe5e1`
- Runtime: Python 3.12.3, NumPy 2.3.5, pandas 2.3.3, rasterio 1.4.4
- Six input SHA-256 values were checked against the accepted
  `product_raster_metadata.json` before interpretation.
- New outputs: `product_floor_summary.csv`, `product_floor_exceptions.csv` and
  `product_floor_manifest.json`.
- Remote receipt: `/data/codex/scratch/dsipa-product-floor-20260918/`

The new output hashes and exact input identities are recorded in
`product_floor_manifest.json`.

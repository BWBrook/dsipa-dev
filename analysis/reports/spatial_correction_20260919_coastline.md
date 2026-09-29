# Coastline/land-mask source decision for the DSIPA spatial correction

**Decision date:** 19 September 2026  
**Scope:** source selection and acquisition only; no accepted input or scientific
result was replaced in this work.

## Scientific decision

Use **Australian Coastline 50K 2024, version 1-1, Split polygons** as the terrestrial
polygon source for the corrected 1 km and 5 km surrounding-land supports. It is
an AIMS/eAtlas product made under the Australian Government National
Environmental Science Program, has a stable DOI, and is licensed CC BY 4.0.
Use its individual native polygons and spatial index for local clipping; do not
construct a national dissolved union. The Split polygons are the Full geometry
cut on a 2-degree grid and materially reduce repeated access to the very large
mainland feature.

- Dataset: Hammerton, M. & Lawrey, E. (2024), *Australian Coastline 50K 2024
  (NESP MaC 3.17, AIMS)*, version 1-1, eAtlas,
  <https://doi.org/10.26274/qfy8-hj59>.
- Primary catalogue/metadata mirror:
  <https://researchdata.edu.au/australian-coastline-50k-317-aims/4021616>.
- Direct Split v1-1 archive:
  <https://nextcloud.eatlas.org.au/s/DcGmpS3F5KZjgAG/download?path=%2FV1-1%2F&files=Split>.
- Licence: Creative Commons Attribution 4.0 International.
- Required attribution: `Hammerton, M., & Lawrey, E. (2024). Australian
  Coastline 50K 2024 (NESP MaC 3.17, AIMS) (Version 1-1) [Data set]. eAtlas.
  https://doi.org/10.26274/qfy8-hj59`.

This choice corrects the Natural Earth 1:110 million scale mismatch while
keeping the measurement target explicit: annual radiance in the portions of
fixed 2024 CAPAD 1 km and 5 km outward bands classified as terrestrial and not
covered by another protected-area polygon. The PA-year is the analytical unit;
the coastline polygon defines observation support and is not an independent
ecological response or replicate.

## Why this source fits the estimand

The product consists of closed land polygons derived from 10 m Sentinel-2
imagery acquired from January 2022 through June 2024. The authors selected
above-mean-sea-level observations, thresholded NDWI, vectorised at an
interpolated 5 m grid, smoothed the polygons, and applied a 0.00003-degree
simplification. Its shoreline is intended to approximate mean high water. The
authors report that manual comparison with high-resolution imagery placed 90%
of polygons within 20 m, apart from isolated failures. That positional scale is
small relative to the 1 km and 5 km DSIPA bands and is materially better matched
to small islands and peninsulas than the former Natural Earth source.

The Split polygon source is an ESRI shapefile in EPSG:4326 with 30,061 `Polygon`
features. Its only non-geometry field is `FID`. The observed extent is
96.816626–167.997936 degrees east and 43.743047–9.039797 degrees south. The
implementation should transform locally selected polygons to the analysis CRS,
repair only demonstrably invalid geometries, clip them to each PA's finite
analysis window, and union only those local pieces. The coastline source must
be intersected with the corrected outward buffer before subtracting CAPAD
tenure.

The underlying processes remain distinct:

- CAPAD 2024 represents the fixed protected-tenure sampling frame.
- The AIMS product represents a 2022–2024 remotely sensed approximation to a
  high-water terrestrial boundary.
- Annual night-light cells represent the radiance observation process.
- The land mask therefore reduces ocean contamination; it does not turn the
  surrounding contrast into a causal measure of ALAN encroachment or historical
  land-cover change.

## Alternatives checked

### GEODATA COAST 100K 2004 — rejected as the primary mask

Geoscience Australia's official product has a well-defined shoreline: mean
high water, the seaward edge of mangroves, indefinite coast, and straight
closing lines across narrow inlets and rivers. It is nationally uniform and
derived primarily from the 1:100,000 National Topographic Map Series. However,
its catalogue states that Australian external territories are not shown, its
source currency varies with the underlying map sheets, maintenance is not
planned, and it was issued in 2004. These are direct disadvantages for the
accepted CAPAD estate, which includes Christmas Island, Norfolk/Phillip Island
and Pulu Keeling records. Product metadata and downloads are at
<https://pid.geoscience.gov.au/dataset/ga/61395>.

### DEA Coastlines — rejected as the direct land mask

Geoscience Australia's DEA Coastlines v3.1.0 is the more accurate official
shoreline product: annual approximately mean-sea-level lines, 1988–2025,
7–10 m reported validation accuracy, ongoing updates and CC BY 4.0 licensing.
It is designed as annual shoreline linework, however, rather than closed land
polygons; linework can be discontinuous around rivers and other complex coastal
features. Converting one annual layer to a watertight continental land polygon
would add a substantial, separate reconstruction problem and new topology
assumptions. It is valuable as an independent sensitivity check at selected
coasts, but is not the simplest defensible input to the current correction.
Official product documentation is at
<https://knowledge.dea.ga.gov.au/data/product/dea-coastlines/>.

## Acquisition and identity

The public archive was downloaded on 19 September 2026 only to:

`deep-server-ts:/data/codex/scratch/dsipa-spatial-correction-20260919/coastline/`

The run used `tmux`; no accepted repository input was mutated. Reproducible
acquisition and coverage screening are implemented in
`analysis/acquire_corrected_coastline.py`. The Full/Split pilot and documented
exception screen are reproducible with
`analysis/compare_aims_coastline_full_split.py` and
`analysis/screen_aims_coastline_exceptions.py`, respectively.

| Object | Size (bytes) | SHA-256 |
|---|---:|---|
| Split v1-1 ZIP | 81,355,896 | `c6046a756c8ac67f04ae99155265ee04b34d1dcbfa39fb1b0c479f6bb2b6a7cd` |
| Split polygon `.shp` component | 39,878,560 | `744cfeb492e3c0fb0aa66f2807b97406c4658c8470662f9b436fbb949d24e337` |
| Split polygon `.dbf` component | — | `d9c056b6926ef72768b896c151534813a83d3daa1842a543feea88965ecc59d7` |
| Split polygon `.shx` component | — | `bd44e99a439788aa29513e25259cee3dcf6f763a185a977171fee7639a84d864` |
| Full v1-1 ZIP | 40,425,498 | `cdbabe24373863c06eaa5a1e76643ea6aebfafe34abfcd0e188c05de1a60882f` |
| `.shp` component | 39,824,856 | `c6384a82cfe0edfee8447a111f1238021f6e4c4875fb417df46b43b670b7e242` |
| `.dbf` component | — | `59602d1736f5f1c3cca203185e02dd1f75e9745389300f2d02fd099ef4f62223` |
| `.shx` component | — | `a4029cad23d717cbc542d2515f90a422c9ccef34110f87795434ec106fb9e50d` |
| `.prj` component | — | `a02a27b1d1982c8516d83398e85a3c8b1aef1713c13ef4d84d7bde17430c07c4` |

## CAPAD coverage checks

Intersection areas below use EPSG:6933 only as a cross-region equal-area
screen. They compare the unchanged accepted
`pa_geometries_v0_3_0.gpkg` with the new source and are not corrected ALAN
results.

| CAPAD ID | Reserve | State | AIMS overlap fraction | Representative point on land |
|---|---|---|---:|---|
| `WA_39584` | Henderson | WA | 1.0000 | yes |
| `WA_05225` | Torndirrup | WA | 0.9752 | yes |
| `NSW_LHI` | Lord Howe Island | NSW | 0.9899 | yes |
| `CWTH_05` | Christmas Island | EXT | 0.9666 | yes |
| `CWTH_07` | Norfolk Island Botanic Gardens | EXT | 1.0000 | yes |
| `CWTH_08` | Norfolk Island (Mt Pitt) | EXT | 0.9989 | yes |
| `CWTH_09` | Norfolk Island (Phillip Island) | EXT | 0.9877 | yes |
| `CWTH_10` | Pulu Keeling | EXT | 0.9943 | yes |

The Full and Split sources were then compared after local union and clipping to
the corrected 5 km windows around all eight rows above. All eight symmetric
difference areas were exactly 0 square metres. Absolute area difference was 0
for seven windows and `1.49e-08` square metres for Henderson, a floating-point
round-off discrepancy with zero symmetric difference. This verifies the
producer's statement that Split changes feature partitioning rather than land
geometry for the pilot windows.

The accepted CAPAD geometry file contains no Macquarie Island protected-area
record. Fourteen of its 19 `STATE=EXT` records are Antarctic protected areas;
the five non-Antarctic records are exactly the five Commonwealth records listed
above. Macquarie Island therefore creates no missing DSIPA analytical unit in
the accepted sampling frame, although a future CAPAD release adding it would
require a source supplement because the AIMS file stops at 43.743 degrees south.

The complete non-Antarctic CAPAD screen and fail-closed gap list are stored in
the isolated run directory as `national_pa_land_coverage_screen.csv` and
`coverage_gap_ids.csv`. Of 11,119 non-Antarctic accepted rows, six have zero
intersection with the AIMS land polygons:

- `CWTH_IPA12`, Ugul Malu Kawal (0.433 km2);
- `QLD_0289BDI001`, Bird Island (0.00214 km2);
- `QLD_0925HMA001`, Ex-HMAS Brisbane (0.353 km2);
- `VIC_698`, Lawrence Rocks W.R. (0.0645 km2);
- `WA_36056`, Investigator Island (0.413 km2); and
- `WA_44673`, Unnamed WA44673 (0.00111 km2).

These are the actual source-coverage gap IDs. Ex-HMAS Brisbane is a submerged
artificial-reef reserve, so its absence from a terrestrial mask is expected and
it should not be made eligible by patching the mask. The remaining five require
local source comparison before deciding whether a supplementary authoritative
island polygon is justified; until then their corrected surrounding-land
support must fail closed.

None of the six appears in the accepted `pa_trends_v0_3_0.csv`, the four
coauthor examples, or the uncertainty watchlists. They therefore have no
accepted ten-pixel whole-reserve or buffer trend and are not a current headline
example. The bounded production disposition is to record an explicit
`coastline_coverage_absent` status and exclude only their land-dependent
surrounding/product-buffer rows. Do not encode zero. Preserve unchanged inside
and land-independent inward-ring outputs.

Another 48 rows intersect AIMS land but have a representative point outside the
land polygon. Many are wetlands, estuaries, narrow coastal reserves or multipart
islands. This representative-point flag is a diagnostic, not proof of missing
coverage, and must not itself exclude a PA. Per-PA land-intersection area and
raster-cell eligibility remain the relevant production checks.

### Documented-error proximity screen

The v1-1 metadata names bridge-filled or otherwise misrepresented waters at
Bribie Island, Swan River, Collins Pool, Brisbane Water, Mooney Mooney Creek,
Parramatta River and Brisbane River, plus local mapped errors near Lloyd Island
and Olive River. Approved-name points came from Geoscience Australia's
[Composite Gazetteer of Australia](https://pid.geoscience.gov.au/dataset/ga/150710);
the Lloyd and Olive coordinates also match the coordinates in the AIMS errata.
This is a point-within-5-km screening test, not a delineation of each entire
erroneous waterbody.

The screen found CAPAD 5 km proximity at every named location except Collins
Pool. The affected-candidate IDs are:

- Bribie Island/Sandstone Point: `QLD_0532BBI001`, `QLD_0619BKL001`.
- Swan River: `WA_48325`.
- Brisbane Water: `NSW_N0005`, `NSW_N0006`, `NSW_N0584`, `NSW_N0585`,
  `NSW_N0704`, `NSW_N0920`.
- Mooney Mooney Creek: `NSW_N0006`, `NSW_N0086`, `NSW_N0302`, `NSW_N0935`.
- Parramatta River: `NSW_N0083`, `NSW_N0599`, `NSW_N0645`, `NSW_N0879`.
- Brisbane River: `QLD_0576FLY001`.
- Lloyd Island/noisy adjacent coast: `QLD_1073KUY001`.
- Olive River mouth: `QLD_4239AMU001`.

These IDs should carry a `known_coastline_exception=true` diagnostic in the
corrected extraction and receive visual/local shoreline review if their
eligibility or sign category changes. The Collins Pool gazetteer point was
42.9 km from the nearest accepted PA, so that documented error cannot affect a
5 km support at that reference location.

## Limitations and required production checks

This source is a defensible measurement correction, not a perfect coastline.
Its documented limitations should remain visible in the Methods and run
manifest:

- The mapped tidal level varies spatially because tide filtering was applied
  per Sentinel scene rather than per pixel; the boundary only approximately
  represents mean high water.
- Turbid water, shallow gently sloping shores, breaking waves, dense seagrass,
  sun glint and cloud limitations can create false or missing land.
- Bridges can close rivers and ocean-connected bays; jetties and oil rigs can
  be classified as land. Named errata include several bridged estuaries and up
  to 100 m local noise near Lloyd Island in far north Queensland.
- Features smaller than 200 square metres were removed. The source is unsuitable
  for deciding the existence of every rock or tiny cay, although those features
  are well below the effective DSIPA raster support unless aggregated.
- A static 2022–2024 mask is being applied to all 2013–2024 radiance years.
  This is coherent with the fixed-estate descriptive estimand, but real
  accretion, erosion or reclamation can create local temporal mismatch.
- AIMS uses approximate mean high water, while DEA uses approximately mean sea
  level and GEODATA 100K uses a cartographic mean-high-water convention with
  inlet closing rules. Boundary differences are expected around intertidal
  flats, estuaries and mangroves.

Production must fail closed on archive hash, CRS, feature count and required
components. It should record per-PA raw buffer area, land-clipped area,
unprotected-land area, valid raster-cell count and eligibility. Flag very low
land fractions, all source-coverage gaps, invalid geometry repairs, and cases
whose category or eligibility changes from the accepted run. A targeted
sensitivity against DEA Coastlines or high-resolution imagery is warranted for
headline coastal examples and any reserve whose inference changes materially;
it is not necessary to reconstruct a second national mask before the corrected
run.

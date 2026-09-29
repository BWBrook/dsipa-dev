# Spatial correction protocol — 19 September 2026

Written before examining corrected national radiance results. This is a
post-review correction, not a preregistered original analysis.

## Supports and precision

Retain the accepted repaired/dissolved CAPAD polygons in EPSG:3577 without
boundary simplification. Distances remain projected distances in that CRS,
as in the stated original method; this is not a geodesic-distance analysis.
Construct circular buffers/erosions with 128 segments per quadrant. The maximum
arc-to-chord deviation is r[1-cos(pi/(4q))], below 0.19 m at 10 km and below
0.019 m at 1 km. This numerical precision does not imply comparable coastline,
CAPAD, sensor or geolocation accuracy. Preserve rasterio's existing default
pixel-selection convention and the ten-valid-pixel/eight-year eligibility rules.

Test the concave-boundary counterexample, narrow boundary features, estate
exclusion and analytical area. Before national extraction, compare 128 and 256
segments at the reviewer examples and a fixed-seed sample, inspecting actual
pixel support and 2024 statistics. Any changed eligibility or sign in this pilot
requires investigation of the selected cells, not automatic acceptance of the
lower precision. Record residual numerical differences and their scale.

## Separating effects

Preserve the accepted Goal 012 annual tables and whole-reserve observations.
Use three comparisons: accepted geometry plus old mask (archived baseline),
corrected geometry plus old mask (geometry-only), and corrected geometry plus
validated replacement coastline (corrected primary). Interior bands require only
the geometry correction. The coastline source and coverage decisions are recorded
separately before interpreting corrected annual results.

Compute all twelve years for affected supports. Compare annual valid-pixel
counts and means, eight-year eligibility, Theil-Sen slopes and paired categories.
Report losses and gains, absolute and relative slope changes, coastal cases,
matched interior-band membership and sign transitions. Retain the whole-reserve
count and area results only after proving their annual inputs unchanged.
Revisit illustrative categories if their new signs no longer match the labels;
do not select cases to conceal a changed conclusion.

## Coastline and coverage

Use public land polygons with resolution appropriate to kilometre buffers and
explicit island coverage. Record shoreline convention, reference date, licence,
source URLs, archive/member checksums and coverage exceptions. A modern fixed
shoreline is a spatial analysis support, not an annual historical coastline.
Never silently substitute a missing island with its protected-area boundary.
Quantify coverage gaps before national interpretation and document exclusions
or authoritative supplements explicitly.

## Reproducibility and interpretation

Run in an isolated deep-server directory with persistent tmux logs. Record code,
inputs, configuration and output identities. Keep schema version 0.3.0 because
column definitions are unchanged; identify the new analysis independently as
spatial-correction-20260919. Never overwrite the sealed old baseline or conflate
its reference contract with the corrected analysis. Reconcile downstream scripts
against a versioned corrected-input manifest, retaining fail-closed identity checks.
A private candidate is the deliverable; publication and submission remain gated.

## Preflight decisions (before national extraction)

The pilot included 73 reserves: the named review cases, 36 fixed-seed random
reserves and 24 reserves whose archived 1–5 km band contained 9–11 valid pixels
(overlap removed). Pure geometric pixel membership was compared independently
of nodata. All twelve rasters have exactly the same CRS, transform and dimensions.
Among 365 supports, three 5 km raw buffers differed by one cell at q128 versus
q256; no 1 km buffer or interior band differed and no eligibility changed. Two
changed supports were zero in every year at both precisions. The third positive
slope changed from 0.005106672719 to 0.005105513955 units/year (0.023%); its sign
was unchanged. Accept q128 with these residual numerical differences disclosed.
The eight-reserve all-year extraction pilot completed without errors in 17 s.

Use AIMS Coast50K2024 v1-1 Split polygons: the source Full geometry split on a
2-degree grid. Eight named Full/Split local unions had zero symmetric difference.
The complete non-Antarctic CAPAD screen identified six polygons with no AIMS land
intersection. None enters the accepted whole-reserve trend set or paper examples.
Exclude their land-dependent surrounding observations explicitly as unavailable;
do not encode observed zero. Retain their land-independent inside and interior
bands. Raw-buffer diagnostic observations remain available. The six IDs are
CWTH_IPA12, QLD_0289BDI001, QLD_0925HMA001, VIC_698, WA_36056 and WA_44673.
Fourteen Antarctic CAPAD records fall outside the raster footprint; record this
separately from coastline gaps. Representative points off land are diagnostics,
not grounds to reject multipart or coastal wetland polygons.

Source and precision receipts are retained under the dated isolated run. Raster
errors now propagate with PA/support/year context; only geometrically empty or
out-of-raster support is an ordinary unavailable observation. Assembly requires
exact keyed equality of every unchanged inside column, including missingness.

## Extraction amendment: polygon-only overlay supports

The first national attempt failed explicitly for Wilinggin (CWTH_IPA58), rather
than silently returning missing observations. Land/estate clipping produced a
GeometryCollection containing polygons and zero-area remnants. Rasterio's
transformed window calculation for that collection used erroneous pixel bounds.
Normalise every derived support to its polygonal components; discard point/line
remnants, which have no land area. A synthetic georeferenced-raster test verifies
identical area and sampled cells to the pure polygon, including nested collections.
The extraction error still propagates for any real read/window failure. Preserve
the failed attempt in `national/`, restart the full extraction in `national_v2/`,
and use no partial result from the failed attempt in the corrected analysis.
This amendment is motivated by a demonstrated representation failure, not by the
resulting slope signs. The complete protocol and source hashes travel with v2.

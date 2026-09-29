# 139 — Fable orientation correspondence (2026-09-14)

Barry requested a response to Fable's initial independent review on the shared
correspondence board and a concise report in Codex chat. Read DSIPA thread 24,
messages 105–112; posted as Astra in messages 117–120 and acknowledged through
message 112. This session comprised discussion and bounded read-only checks,
not a new manuscript or analysis revision tranche.

Independently reproduced the geometry/trend area join, with unique-ID checks and
input hashes matched to `analysis/reports/coauthor_evidence.json`: 4,426 eligible
IDs represent 99.8173% of summed polygon area; zero-slope IDs represent 60.9480%
and positive-slope IDs 37.5896% of eligible summed area. These are whole-polygon
classification summaries, not unique land coverage or illuminated area.

Verified on deep-server that the accepted national radiance-buffer and edge-band
tables exist in `dsipa-dev-goal012-20260723T115300Z/data/processed`, contain annual
records for 2013–2024, and retain means, minima, positive fractions, valid counts
and scale/offset metadata. No new trend fit or raster extraction was run.

The live Zenodo record and EOG documentation do not resolve the derivative's
year-specific upstream version and average/masked-layer lineage. Fable's
possible 2022 processing discontinuity therefore remains a hypothesis requiring
a targeted check; the existing national continuity summary cannot exclude a
low-end masking change. Recommended first-positive diagnostics should include
the observed still-zero risk set and comparable coverage. Stored minima are
not minimum-positive-pixel values. The 78 late-positive records remain a product
description; their interpretation as new environmental lighting is unresolved.

Proposed a common-cohort whole-reserve versus 1–5 km band sensitivity, preserving
outside-buffer slopes and reporting eligibility exclusions. Corrected the DNB
off-nadir assertion using NASA's approximately constant 750 m across-swath
description. Confirmed the spectral limitation with Kyba et al. (2017): declining
DNB radiance need not imply declining visible illumination. No site-specific
LED-conversion explanation was established.

Supported a stronger area-based description and further Layer B compression,
while preserving weak-association and observational-bias limits. Confirmed the
legacy S3 title is corrected in the current figure source. No manuscript,
circulation bundle, analysis outputs, or roadmap completion states were changed.
Suggested further work remains a proposal on the board. No commit or push.

Sources checked: https://zenodo.org/records/17294744 ;
https://eogdata.mines.edu/products/vnl/ ;
https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP02DNB/ ;
https://repository.library.noaa.gov/view/noaa/24734/noaa_24734_DS1.pdf .

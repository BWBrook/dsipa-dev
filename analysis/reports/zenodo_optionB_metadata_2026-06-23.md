# Zenodo Option B Metadata Draft

Status: blocked draft only. Do not upload this metadata, mint or reserve a DOI,
or cite a DOI from this checkout.

Generated: 2026-06-23 UTC by `nightlight` for Goal 010.

## Record Title

Layer A protected-area dark-sky integrity outputs for DSIPA-NBS, Australia,
2013-2024

## Creators And Contributors

- Barry W. Brook, University of Tasmania
- DSIPA-NBS project contributors as recorded in the source repository and
  manuscript metadata

Creator/contributor order and ORCID/institutional details must be confirmed in
the later external-upload/DOI-mint goal before any archive record is published.

## Description

This draft describes the approved Option B archive payload for the DSIPA-NBS
paper. The payload is intended to support the primary Layer A analysis of
artificial light at night inside and around Australian protected areas. It is
limited to processed Layer A national outputs and their checksum manifest.

The current Goal 010 staging pass is blocked because eight of the nine approved
Layer A payload files are absent from the local checkout and from the checked
DSIPA-owned remote evidence-store paths. This metadata is therefore not ready
for external upload.

## Related Source

- Source repository: DSIPA-NBS local action checkout at
  `/Users/bwbrook/papers/dsipa-dev`
- Release commit for this blocked staging pass: `b1c1539`
- DOI status: pending; no DOI has been minted or reserved.

## Licence And Provenance Notes

- Layer A outputs are derived from CAPAD, IBRA, and Zenodo/OpenGeoHub
  nightlights inputs, with provenance recorded in `data/README.md`.
- The draft archive route is Zenodo-style, but no external archive record
  exists yet.
- Raw ALA downloads and row-level processed ALA occurrence tables are not part
  of this payload and remain restricted/excluded by default.
- Layer B manuscript-facing materials remain derived summaries, reports,
  figures, and provenance ledgers only.

## Intended File List

The intended Option B payload is:

- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `data/processed/pa_trends_v0_3_0.csv`
- `data/processed/pa_risk_rankings_v0_3_0.csv`
- `data/processed/pa_geometries_v0_3_0.csv`
- `data/processed/pa_geometries_v0_3_0.gpkg`
- `data/processed/pa_ibra_assignment_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`

File sizes, checksums, and current recovery status are recorded in:

- `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.md`
- `analysis/reports/optionB_layerA_archive_manifest_2026-06-23.json`

## Exclusions

The following are explicitly excluded from the Option B archive payload:

- raw ALA downloads;
- row-level processed ALA occurrence tables;
- generated science artefact folders not listed in the manifest;
- manuscript build outputs, release packages, GitHub releases, DOI scaffolds,
  and publication submission materials.

## Upload Readiness

Not ready. The later external-upload/DOI-mint goal should not be opened until
the eight missing approved Layer A payload files are recovered from a concrete
source or regenerated under a separate explicitly authorized science/data goal.

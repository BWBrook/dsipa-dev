# Release-input reconciliation scout — 2026-09-19

Bounded, read-only mechanical reconciliation for M3 in
`analysis/reports/astra_adversarial_review_20260918.md`. No source, data,
manuscript, guards, or orchestration files were changed. The historical public
deposit remains a historical identity; this report does not certify release
validity, freeze final output hashes, or adjudicate the parent geometry/mask
corrections.

## Sources and provenance

- Accepted source tree: `/data/codex/repos/dsipa-dev-goal012-20260723T115300Z`
  on `deep-server-ts`, Git `1b39dcc1403a40c3962f04c922bb612c41f83a8f`.
- Public record queried: Zenodo `21524637`, DOI
  `10.5281/zenodo.21524637`, via `https://zenodo.org/api/records/21524637`.
- Public payload scratch: `/data/codex/scratch/dsipa-release-reconciliation-20260919`
  on `deep-server-ts`; files were fetched from the record's per-file content
  URLs. No credentials or republication actions were used.
- The accepted checkout was already dirty before this inspection (tracked
  pipeline/report/source changes and untracked Goal 012 reproducibility files);
  no changes were made by this scout.

## Public manifest and README facts

The live Zenodo record contains 12 files: nine processed payloads plus
`README.md`, `manifest.json`, and `SHA256SUMS`. The public `manifest.json`
reports schema `1.0.0`, payload count 9, total payload size 265,783,139 bytes,
and accepted candidate provenance `source_goal=011-layerA-preservation-
reproduction`, source run `20260723T062202Z-goal011-layerA-preservation`, and
accepted source commit `7f46a00f74c32881034f0129728b3d80eedd2442`.

The README explicitly classifies three payloads as non-exact: radiance is
byte-different with no detected primary drift but historical row equality
unproven; edge profiles have bounded threshold-sensitive drift; and the GPKG
is byte-different with accepted within-run semantic identity but historical
feature equality unproven. It says no source code is included.

Relevant public SHA-256 values from `SHA256SUMS` / manifest and accepted
Goal 012 values are:

| File | Public bytes / rows | Public SHA-256 | Accepted Goal 012 SHA-256 | Direct comparison |
|---|---:|---|---|---|
| `pa_radiance_buffers_national_v0_3_0.csv` | 96,268,937 / 900,768 data rows | `6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61` | `63e95fb30b0bdebc6c74d23f08666ab9cfe0ef408d27744f12fbb029a8b92ec1` | keys identical; compared numeric fields exactly equal after key sort |
| `pa_edge_profiles_national_v0_3_0.csv` | 25,255,793 / 400,788 data rows | `baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812` | `ddb9c9f5678f9da10b70754d3c9319ea30bfe7203d3c80c8f8f298ed2cf5783b` | keys identical; all common values compared equal in targeted check |
| `pa_geometries_v0_3_0.csv` | 1,768,417 / 11,133 data rows | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | exact SHA and row/key dimensions |
| `pa_geometries_v0_3_0.gpkg` | 132,571,136 bytes | `6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9` | `da843f551bf1863dc5d1930ecb657491f73d69827b25007a0c55c9019721d0e6` | bytes differ; no feature-level comparison run |

The public and accepted radiance tables both have shape `(900768, 9)` for the
selected columns. Their sorted composite keys
`(pa_id, zone, buffer_km, buffer_type, year)` are in identical order and set;
`mean`, `max`, `frac_gt0`, and `valid_pixel_count` have zero differing values
and maximum absolute difference `0.0`. This establishes equality for those
fields and keys, while retaining the distinct byte identities. The edge table
shapes are both `(400788, 18)` and the composite keys
`(pa_id, ring_inner_km, ring_outer_km, year)` have identical sets; the targeted
common-column comparison found no value differences. The geometry CSV shapes
are both `(11133, 19)` with identical `pa_id/NAME/STATE` key sets and the
public SHA matches the accepted SHA.

The public manifest itself records radiance and edge as
`reference_contract_classification=canonical_ordering_change_semantically_exact`,
despite its separate historical classifications. For the GPKG it records
`goal011_classification=byte_different_within_run_semantic_identity` (the
exact wording should be taken from the live manifest if used downstream).

## Current guards and orchestration

The accepted-input guards are distributed across current audit scripts:

- `analysis/coauthor_evidence.py:25-31,59-63` hard-codes SHA-256 values for
  radiance, trends, risk rankings, and geometry CSV, hashes each input, and
  raises `ValueError("Accepted input hash mismatch: ...")` on mismatch. It
  also asserts 4,426 trend rows, 3,969 zero and 420 positive inside slopes,
  3,858 rankings, quadrant counts `[305, 55, 3308, 190]`, and four example
  cases.
- `analysis/audit_product_continuity.py:148-149` hard-asserts the accepted
  radiance SHA (`63e95f...`) and later requires 4,426 trend rows.
- `analysis/audit_interior_area.py:233-270` reads accepted trends, edge
  profiles, and geometry CSV; records input/output SHA-256 and byte sizes;
  checks the exact 1–5 km ring and the 1,205 matched cohort.
- `analysis/audit_edge_followup.py:242-351` reads accepted trends, edge, and
  geometry CSV; records input/output SHA-256 and byte sizes; reconstructs the
  same 1,205-reserve cohort and 0–1/1–5 km summaries.
- `analysis/run_full_pipeline.sh:27-79` runs the generic geometry, Layer A,
  Layer B, figures, validation, tests, and build sequence. It does not call
  `coauthor_evidence.py`, `audit_product_continuity.py`,
  `audit_interior_area.py`, or `audit_edge_followup.py`, and it does not
  expose a route that maps the public Zenodo payloads to the accepted-input
  audit contract.
- `analysis/deep_server_tmux_run.sh:125-326` wraps the generic full-pipeline
  run in tmux and records source/output inventories, but likewise does not
  orchestrate the current accepted-input audit sequence.

Therefore, current code can reproduce the stored accepted audit only when the
private Goal 012 input identities are supplied. The public deposit can support
the targeted table-level checks above, but its distinct radiance/GPKG bytes
cannot pass all current hard-coded guards as a drop-in input set.

## Narrow unresolved points

1. The radiance table's key/value equality was checked for all rows and the
   selected numeric fields, but byte-level differences were not decomposed
   into ordering/formatting causes beyond the manifest classification.
2. The edge comparison checked all common columns through key-aligned values
   in the available CSVs; no independent threshold or historical-source
   adjudication was attempted.
3. The GPKG was hash-compared only. Feature-level semantic comparison needs a
   geospatial-aware check and should be done by the higher-tier agent before
   any claim about interchangeability.
4. The parent agent's current geometry and land-mask corrections are outside
   this scout; old public data must remain labelled historical.

## Suggested private artifact set for review (not a release decision)

Keep a private, immutable review bundle containing: the exact accepted Goal
012 tables and GPKG; the public Zenodo `README.md`, `manifest.json`, and
`SHA256SUMS`; the public-to-accepted comparison report and command transcript;
the current audit scripts (`coauthor_evidence.py`, `audit_product_continuity.py`,
`audit_interior_area.py`, `audit_edge_followup.py`) with their protocol files;
the pinned `pyproject.toml`/lockfile and package build metadata; the manuscript
and figure/table source inputs required by the current review; and a manifest
that records both identities without replacing either one. Do not call this
set a public release or freeze its output hashes until the geometry/mask work,
current audit orchestration, and higher-tier release decision are complete.

## Checks run

Commands were read-only except for downloads into the authorized isolated
scratch directory:

```text
ssh deep-server-ts 'git rev-parse HEAD; find data/processed -maxdepth 1 ...'
curl -fsSL https://zenodo.org/api/records/21524637 ...
ssh deep-server-ts 'curl -fsSL https://zenodo.org/api/records/21524637/files/<name>/content -o /data/codex/scratch/dsipa-release-reconciliation-20260919/<name>'
ssh deep-server-ts 'sha256sum <accepted and public files>; wc -l <public CSVs>'
ssh deep-server-ts 'pandas key-set and key-aligned value comparison for radiance, edge, and geometry CSVs'
```

Outcomes are recorded above. No tests, builds, manuscript generation, remote
compute job, or source-tree mutation was performed.

## Complete identity comparison (follow-up)

The reproducible checker is
`analysis/compare_baseline_input_identities.py`. It reads both CSVs with
`pandas.read_csv(float_precision="round_trip")`, sorts by declared stable
keys, compares every column with explicit missing-value handling, and compares
the GPKGs after sorting by `pa_id`. The remote run used the Goal 012 virtual
environment because system Python lacked GeoPandas.

Command:

```text
/data/codex/repos/dsipa-dev-goal012-20260723T115300Z/.venv/bin/python \
  compare_baseline_input_identities.py \
  --accepted /data/codex/repos/dsipa-dev-goal012-20260723T115300Z/data/processed \
  --public /data/codex/scratch/dsipa-release-reconciliation-20260919 \
  --output comparison.json
```

Complete results were written to
`/data/codex/scratch/dsipa-release-reconciliation-20260919/comparison.json`.
For both radiance (`900,768 x 18`) and edge (`400,788 x 18`), stable-key
order and sets matched exactly. Every column had zero differing parsed values;
all numeric maximum absolute differences were `0.0`. Missingness was also
identical: radiance had 133,596 missing `buffer_km` values and 93,204 missing
values in each of `mean`, `median`, `min`, `max`, `std`, `frac_gt0`, and `p95`;
edge had 325,908 missing values in each of those seven summary columns. No
differing-ID examples exist.

The all-field GPKG comparison found both datasets `EPSG:3577`, shape
`11,133 x 20`, identical `pa_id` sets and order, and zero differences in every
non-geometry attribute, including 11,133 jointly missing `NRS_MPA` values.
All 11,133 geometries passed per-key Shapely topological `equals`; there were
zero differing IDs. Concatenated per-feature normalized-WKB SHA-256 was
identical for both files:
`914143b296ec9a7fae4aa4363dd517d1daa49883cf7c1aebf52b39109b703484`.
The container byte hashes remain different (`da843f...` accepted versus
`6ea584...` public), so semantic identity does not erase distinct file
identities.

The checker was run remotely only; local WSL system Python lacks GeoPandas.

## Corrected downstream run (2026-09-19)

After the remote `national_v2` extraction emitted `{"stage": "complete"}`
and its extraction manifest, the downstream synthesis and manuscript-audit
orchestration ran in persistent tmux on `deep-server-ts`. The first audit
attempt exposed a manifest-key bug: `product_baseline_distances.csv` had been
recorded under a path-prefixed key, while the product-continuity contract
requires the basename. The manifest was corrected to include the basename,
SHA-256 `7b317b0c232d54d167a27f8a8e003cb4c71dbbc8e9781cca1edd9806865b78f3`,
and 178,745 bytes; the complete rerun then exited 0. The transient failed
attempt did not alter accepted inputs.

Synthesis reports show 4,426 inside series with 420 positive, 37 negative, and
3,969 zero inside slopes. Paired quadrant counts were baseline `305/55/3308/190`
(Q1–Q4), geometry-only `339/65/3430/238`, and corrected
`347/70/3587/249`; corrected paired cohort size was 4,253. The corrected
inside series is invariant in count and sign totals relative to the accepted
inside trend contract.

Remote outputs were staged locally under
`analysis/reports/spatial_correction_20260919/`, with manuscript-audit outputs
also copied to the canonical flat locations `coauthor_evidence/`,
`product_continuity/`, `interior_area_audit/`, and `edge_followup/`. All nine
corrected processed files, including the 132,571,136-byte GPKG, are in
`spatial_correction_20260919/data_processed/`. The run input manifest is
`spatial_correction_input_manifest.json`; it records ten input identities,
including the baseline-distance file, extraction manifest SHA-256
`30a5296981afcf279288d8f8090693c9602270a805f5c380455c99bc80e13c73`, and
synthesis script SHA-256
`b47547dd15541b254bdb1379d5c6364596c48bd3a6a4740b7229e65a1fe45a77`.

## Public-baseline preparation route

`analysis/prepare_public_spatial_baseline.py` now provides the bounded private
staging route. It accepts an isolated public-payload directory, a new empty
output directory, an immutable VIIRS raster directory, and an immutable
Natural Earth cache directory. It verifies the four spatial payload hashes
against the live Zenodo identities, copies those payloads into
`data/processed/`, and symlinks the large raster/cache trees by default (or
copies them with `--copy-large-inputs`). It writes
`PUBLIC_BASELINE_MANIFEST.json` with every allowlisted payload hash plus every
file hash in the raster and Natural Earth trees, and a README that labels the
result as private preparation. It refuses a non-empty output directory or any
payload hash mismatch.

Example remote usage after the isolated downloads and immutable source paths
are present:

```text
uv run python analysis/prepare_public_spatial_baseline.py \
  --public-dir /data/codex/scratch/dsipa-release-reconciliation-20260919 \
  --output-dir /data/codex/scratch/dsipa-public-spatial-baseline-20260919 \
  --raster-dir /data/codex/repos/dsipa-dev-goal012-20260723T115300Z/data/raw/nightlights_zenodo_v0_4 \
  --natural-earth-dir /data/codex/repos/dsipa-dev-goal012-20260723T115300Z/data/raw/ne_110m_land
```

The corrected extraction still requires the project’s spatial dependencies,
the public VIIRS v0.4 raw raster source, and the legacy Natural Earth cache;
this utility stages and records those dependencies but does not invoke
`run_spatial_correction.py` or alter accepted data. Focused tests are in
`tests/python/test_prepare_public_spatial_baseline.py` and pass (`2 passed`).

The parent agent additionally verified zero differences in loaded per-key raw
GPKG WKB; the independent comparison above also found all 11,133 Shapely
topological equalities and identical normalized-WKB aggregate hashes.

## Executed public-baseline reproduction check

The final preparation utility includes all nine published processed payloads,
validates all twelve upstream raster MD5 identities, and reconstructs the
legacy Natural Earth union from its pinned public archive. Its reconstructed
WKB hash matched the accepted cache exactly. A separate parent comparison of
loaded public and accepted PA geometries found zero per-key raw WKB differences.

Eight named reserves were then re-extracted from the public baseline with the
corrected engine. All 576 corrected surrounding rows and 288 interior-band rows
matched the national extraction exactly in every field, including pixel counts
and annual statistics (missingness retained; CSV dtype differences ignored).
The tested identifiers were ACT_03, CWTH_IPA58, NSW_LHI, NSW_N1142,
QLD_0239GRP001, WA_05225, WA_27575 and WA_39584. This is a targeted reproduction
check; the full baseline equality audit covers the complete input cohort.

Receipts: `public_reproduction_validation.json`,
`public_raster_identity_validation.json` and `PUBLIC_BASELINE_MANIFEST.json`
in the dated correction evidence packet. The executed public pilot preceded the
addition of an explicit upstream MD5 validation to the preparation utility; those
twelve identities were subsequently checked separately and passed. No extraction
algorithm changed between those steps.

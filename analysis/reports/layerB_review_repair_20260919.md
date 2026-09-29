# Layer B review repairs and invalid-sample audit

Date: 19 September 2026

This bounded repair addresses the authorised m1, m2 and m3 findings in
`analysis/reports/astra_adversarial_review_20260918.md`. It does not refit the
accepted Layer B models, regenerate manuscript/SI files, alter raw data, or
change the scientific estimand.

## Completed repairs

### m1: occurrence deduplication wording

The implementation was already a defensible species-record analysis and was
left unchanged. The exact Methods wording supplied to the parent is:

> After quality filters, records were deduplicated using a species--1-km
> projected grid-cell--event-date key. The species key uses the `species`
> column when that column is present, and otherwise uses `scientificName`;
> missing names are assigned `unknown`. The event-date key is the normalized
> year--month--day value, with missing month or day represented as `00`. The
> fallback is column-level rather than row-level. Consequently, records for
> different species in the same cell on the same date remain separate, while
> repeated records for one species and cell-date key are retained once across
> input chunks.

The implementation is in `src/python/dsipa/layerB_data.py:468-491`; the new
regression test confirms that two species sharing a cell and date remain two
records.

### m2: invalid ALAN sample handling

`src/python/dsipa/layerB_model.py:_sample_raster` now:

- rejects nonfinite coordinates and coordinates whose raster row/column is
  outside the dataset support;
- samples the stored raster code and masks raster nodata, negative raw codes,
  and nonfinite raw values before applying metadata scale and offset; and
- retains valid raw zero and positive codes as observed values, with finite
  decoded results only.

Invalid samples therefore become missing and are removed by the existing
feature-frame finite-value filter. They cannot become the valid zero-light
covariate category through scale/offset decoding.

### m3: model contract and metric wording

The classifier settings are explicit in `layerB_model.py`: L2 penalty, `C=1`,
`liblinear` solver, `max_iter=200`, and no predictor standardisation. The
report now states that AUC and log loss are arithmetic means of held-out fold
metrics. The exact contrast wording supplied to the parent is:

> The two-part ALAN model uses an `any_light` indicator contrasting ALAN = 0
> with ALAN > 0, together with `log1p(ALAN)` as an intensity term interpreted
> per one-unit increase among observations with ALAN > 0. Predictors are not
> standardised. Logistic regression uses an L2 penalty with `C = 1`, the
> `liblinear` solver and `max_iter = 200`. Reported AUC and log loss are the
> arithmetic means of the held-out fold metrics; fold variability is a model
> stability summary rather than inferential uncertainty.

## Archived-input impact audit

The audit was run read-only on `deep-server` in tmux, using the accepted tree
`/data/codex/repos/dsipa-dev-goal012-20260723T115300Z` at commit
`1b39dcc1403a40c3962f04c922bb612c41f83a8f`. The remote audit directory was
`/data/codex/scratch/dsipa-layerb-correction-20260919`.

Command:

```text
/data/codex/repos/dsipa-dev-goal012-20260723T115300Z/.venv/bin/python \
  /data/codex/scratch/dsipa-layerb-correction-20260919/audit_layerB_invalid_samples.py \
  /data/codex/repos/dsipa-dev-goal012-20260723T115300Z \
  --output /data/codex/scratch/dsipa-layerb-correction-20260919/audit.json \
  --scan-rasters --hash-rasters
```

The accepted tree contains no row-level ALA input or cached feature frame with
an `alan` column. It contains only summary products, so affected observations
cannot be counted for the primary, within-block shuffle, within-IBRA-by-year
shuffle, or all-provider sensitivity scopes. The preserved summary reports the
nominal primary groups as 50,281 microbat and 50,281 passerine records and the
sensitivity groups as 56,883 each, but it cannot identify which records sampled
invalid raster codes.

The full archived raster scan found 58,045 negative non-nodata raw codes across
the twelve global annual rasters, including 160 in 2022, 132 in 2023 and 3,299
in 2024. It found 3,077,222,400 nodata codes and no nonfinite stored values.
These counts are global raster counts, not accepted Australian occurrence
sample counts, so they do not establish that a published feature was affected.
They do establish that a zero-affected-record claim cannot be made from the
available archive alone.

### Query domain and spatial-support check

The ALA acquisition code does not add a latitude/longitude bounding box. Its
stored query filters are `year:[2013 TO 2024]`, `taxonRank:species`,
`occurrenceStatus:present`, `coordinateUncertaintyInMeters:[0 TO 1000]`, and
`country:Australia`, followed by the taxon filters for Chiroptera excluding
Pteropodidae and Passeriformes. The accepted model then retains points inside
the archived CAPAD union or within its 10 km buffer (after the model's 1 km
geometry simplification), and samples the matching annual raster.

To narrow the impact question without ALA rows, I ran a read-only spatial
inventory against the archived CAPAD geometry GPKG on deep-server. The audit
used EPSG:3577 distances and a conservative half-cell margin for 500 m raster
cells; it counted raw negative and nodata cells whose centres could support a
point inside the PA-plus-10 km domain. The unsimplified CAPAD geometry support
contained 10 negative cells in total: 5 in 2013, 1 in 2019, and 4 in 2021.
There were zero nodata cells in this support for every year. The scale-10
rasters for 2022--2024 contained zero negative or nodata support cells. Thus
the spatial product check rules out a support-wide no-data footprint and rules
out invalid raw cells for the 2022--2024 support, but it cannot prove that the
accepted ALA records did or did not land on the ten historical negative cells.
The country filter and the PA adjacency filter are both population filters;
neither supplies the missing row-level coordinates.

The spatial audit command was:

```text
/data/codex/repos/dsipa-dev-goal012-20260723T115300Z/.venv/bin/python \
  /data/codex/scratch/dsipa-layerb-correction-20260919/audit_layerB_spatial_invalid_support.py \
  /data/codex/repos/dsipa-dev-goal012-20260723T115300Z \
  --output /data/codex/scratch/dsipa-layerb-correction-20260919/spatial_audit.json
```

## Historical-path search and reconstruction route

The repository's acquisition log and provenance table identify the only
preserved raw-input names as
`microbats_20260104T020628Z.zip` and
`diurnal_birds_20260104T020701Z.zip`, under the ignored
`data/raw/ala_occurrences/` path. The corresponding processed occurrence tables
were under the ignored `data/processed/layerB/` path. The January PI-review ZIPs
explicitly excluded large raw/processed caches, and the later release policy
excluded raw and row-level ALA data.

I searched the named DSIPA locations read-only: the Goal 011, Goal 012,
coauthor and Mac-sync remote checkouts; `/data/codex/artifacts/dsipa`; the
DSIPA scratch directories; and the Mac Mini's expected DSIPA paper/work paths.
The remote checkouts contain the four-row model-input summary and occurrence
summary only. No exact raw ZIP, row-level occurrence table, feature frame, or
`data/raw/ala_occurrences`/`data/processed/layerB` directory was present in
those locations. No ALA query or download was issued during this search.

The best reconstruction path is therefore conditional on recovering one of the
two original ZIPs from an external backup or licensed ALA account. If recovered,
the exact route is: verify the recorded SHA-256 and query-period/proxy
definitions; run the existing filter and species--cell--date deduplication
pipeline at the accepted code state; resample the archived nightlights with
the repaired raw-domain validity mask; and compare the resulting feature keys
and invalid-sample counts for primary dr368, both shuffle scopes, and the
all-provider sensitivity. If the ZIPs cannot be recovered, the accepted
feature-level impact is not reconstructable without a new authorised ALA
acquisition, and the refit gate remains unresolved.

Audit hashes:

- script: `0eb25087fa7904a44fc988024e714e7f386a5bbd966edfb278f4e4cf181808f3`
- remote JSON output: `1c23d32fe94572fb1e831f75d0faa9233f366f097521ad870467c57b736aee6b`
- remote log: `19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061`
- spatial-support script: `e0727c8421bdc365c4934be2287003c857f1511478f2d7d32a50e097fdb6c83f`
- spatial-support JSON output: `ce0ce52f7fd0224fe5f8823e6bf43237be5dc32464658e310acdc2d7fd963852`
- archived CAPAD geometry GPKG: `da843f551bf1863dc5d1930ecb657491f73d69827b25007a0c55c9019721d0e6`
- accepted PA-union cache fingerprint: `f40dd0ba92c65b4f81aed5b9689d13f6535d2bcd3b18980a3bb15a4e5173976d`

## Refit decision

No refit was performed. The refit gate is **unresolved**: the accepted
feature-level affected count cannot be reconstructed from the archived inputs,
and the full raster scan shows that invalid negative raw codes exist in the
source product. A future refit is required if an authorised reconstruction of
the accepted occurrence features finds one or more sampled invalid codes; the
current evidence is insufficient to declare the existing model unaffected.

## Verification

The following checks passed:

- `.venv/bin/pytest -q tests/python/test_layerB_sampling.py tests/python/test_layerB_filters.py`
  — 23 tests passed when run with the Layer B test glob.
- `PYTHONPATH=. .venv/bin/pytest -rA` — full suite passed: 129 passed and 7
  skipped because optional regenerated national outputs are absent.
- `.venv/bin/python -m py_compile src/python/dsipa/layerB_model.py
  analysis/audit_layerB_invalid_samples.py
  analysis/audit_layerB_spatial_invalid_support.py` — passed.
- `git diff --check` — passed.
- A synthetic report smoke test confirmed that the explicit classifier,
  contrast and fold-mean statements are emitted.

The accepted model outputs and manuscript/SI sources were not regenerated.

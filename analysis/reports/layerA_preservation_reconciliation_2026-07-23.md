# Layer A Preservation Reconciliation

Generated: 2026-07-23 UTC

Status: **independently accepted as scientifically concordant for all primary
conclusions and as the archive candidate; non-exact payload with immaterial
secondary edge drift**.

## Run Identity

- Commit: `7f46a00f74c32881034f0129728b3d80eedd2442`
- Tree: `c82ebdda83c987d2e1dcc79fb2dba2759f9d7739`
- Run id: `20260723T062202Z-goal011-layerA-preservation`
- Remote artefact:
  `/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation`
- Pipeline terminal status: `failed`, exit code 1
- Scientific source integrity: unchanged

The pipeline failure was a clean-checkout QA prerequisite defect: two ignored
triad GPKG fixtures were absent. National outputs were complete. A bounded
validation repair generated the fixtures, after which full pytest passed 49
tests and package build passed.

## Input Identity

- CAPAD: 14,403 raw features; semantic hash
  `148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf`.
- IBRA: 89 features; semantic hash
  `3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332`.
- Zenodo/OpenGeoHub v0.4: all 12 annual code-pinned MD5 values matched.
- Natural Earth 110m land: marker `4.1.0`, 69,700 bytes, SHA-256
  `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`.

Natural Earth is version-reacquirable but not historically byte-pinned.

## Output Reconciliation

| Output | Current SHA-256 | Historical comparison |
| --- | --- | --- |
| `pa_radiance_buffers_national_v0_3_0.csv` | `6564e2145f2cb94e5d2d1df2fbca8c0c663b5cd4b68d2bfe72fefadfa3cc5c61` | different; historical row-level equality unproven |
| `pa_edge_profiles_national_v0_3_0.csv` | `baf902714e4308a50e6c594db0e2f1d58872b39e03cb88605047f24bdeb06812` | different; bounded secondary threshold drift |
| `pa_buffer_validity_v0_3_0.csv` | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | exact |
| `pa_trends_v0_3_0.csv` | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | exact |
| `pa_risk_rankings_v0_3_0.csv` | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | exact |
| `pa_geometries_v0_3_0.csv` | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | exact |
| `pa_geometries_v0_3_0.gpkg` | `6ea584b1f90fdab82b31fd4861f9c81a7ca1bef03142204579e85e295f3033c9` | different container; historical feature equality unproven |
| `pa_ibra_assignment_v0_3_0.csv` | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | exact |
| `pa_trend_bootstrap_summary_v0_3_0.csv` | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | exact |

All CSV schemas are `0.3.0`; all tested stable keys have zero duplicate rows.
The geometry CSV has 11,133 PAs. The pipeline GPKG and the independently
input-gated GPKG have identical columns, attributes, CRS, and geometry WKB
after PA sorting.

## Primary Science

| Quantity | Accepted | Regenerated | Result |
| --- | ---: | ---: | --- |
| PA universe | 11,133 | 11,133 | match |
| Eligible baseline/trend subset | 4,426 | 4,426 | match |
| 2024 zero inside mean | 3,844 | 3,844 | match |
| Exact-zero inside slopes | 3,969 | 3,969 | match |
| Positive inside slopes | 420 | 420 | match |
| Retention denominator | 3,858 | 3,858 | match |
| Q1 concurrent brightening | 305 | 305 | match |
| Q2 internal brightening | 55 | 55 | match |
| Q3 stable/non-detect | 3,308 | 3,308 | match |
| Q4 external pressure | 190 | 190 | match |
| Complete rings | 383 | 383 | match |

The trends, risk rankings, bootstrap summary, trend distribution, retention
quadrant, edge profile, uncertainty forest, and dominance outputs are
historically byte-identical where pinned. The regenerated baseline map matches
the later accepted Stage 2 map hash rather than the superseded older evidence
hash.

## Bounded Edge Difference

The canonical `dsipa.layerA_edge_decision` generator completed successfully
and was preserved separately. It found:

- 0-1 km valid PAs: 4,425, unchanged;
- 1-5 km valid PAs: 1,432 versus accepted 1,427;
- 5-10 km valid PAs: 383, unchanged;
- complete-ring PAs: 383, unchanged; and
- ring-1 non-null PA-years: 116,412 versus accepted 116,472.

The practical effect sizes are small:

- +5 PAs is +0.35% relative to the accepted 1,427 and +0.045 percentage
  points of the 11,133-PA universe;
- -60 non-null PA-years is -0.052% relative to 116,472; and
- conditional non-zero shares remain 18.02%, 9.40%, and 3.66% across the
  three rings.

Thirty current 2024 ring-1 PAs have exactly 10 valid pixels, and 129 have
8-12. With the source tree unchanged, CAPAD/IBRA semantic identities matched,
all 12 raster MD5s matched, and geometry CSV exact, a near-threshold
rasterization or runtime-environment effect is more plausible than source
change. The historical edge payload is unavailable, so the exact affected PA
set and causal mechanism cannot be proved.

## Classification

- Exact historical hash: 6/9.
- Radiance: byte-different with no detected primary scientific drift;
  historical row-level equality unproven.
- Edge profiles: bounded secondary scientific/threshold drift.
- Geometry GPKG: byte-different container with exact within-run
  attribute/WKB semantics; historical feature-level equality unproven.
- Primary scientific conclusions: concordant.

This is not an exact reproduction. Independent scientific rereview accepted
the edge difference as immaterial to the paper conclusions and accepted the
regenerated payload as the archive candidate. No further Goal 011 science is
required.

## Release Requirements

DOI upload remains on hold only until:

1. canonical release surfaces use 1,432 and 12.9% for 1-5 km ring feasibility,
   while this reconciliation preserves the historical 1,427 versus
   regenerated 1,432 comparison;
2. clean-checkout QA generates or includes the triad fixtures before the full
   test/build sequence; and
3. archive metadata labels the payload a concordant non-exact reproduction
   and retains the unresolved historical row-level radiance and feature-level
   GPKG limitations.

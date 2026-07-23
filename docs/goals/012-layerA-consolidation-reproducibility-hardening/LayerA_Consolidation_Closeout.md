# Goal 012 Layer A Consolidation Closeout

Date: 2026-07-23 UTC

Status: **COMPLETE; one national computation, one bounded existing-output
continuation, no commit or push**.

## Conclusion

Goal 012 hardened the accepted Layer A path without changing its science. The
single authorised national computation completed all Layer A analysis and
report generation, then the original harness terminated at fail-closed output
validation because six files had the correct duplicate-free column-name sets
in a different order from the schema declarations.

The original failed status and log remain preserved. Independent review found
no P0/P1 scientific issue and confirmed that all schema differences were
ordering-only. One narrowly adjudicated repair changed CSV and GPKG attribute
validation from tuple-order identity to duplicate-safe name-multiset equality.
A continuation then ran only validation, tests, build, and Goal 011
reconciliation against the existing outputs. It did not rerun any national
analysis.

The continuation passed. All nine outputs retained identical pre/post SHA-256
values, reconcile semantically with Goal 011, and reproduce every frozen
headline. The generated canonical report artefacts show 1,432 and 12.9%;
1,427 remains only in explicit historical reconciliation.

## Source And Run Identity

- Local branch: `main`.
- Local start/final HEAD and `origin/main`:
  `1b39dcc1403a40c3962f04c922bb612c41f83a8f`.
- Remote base HEAD:
  `1b39dcc1403a40c3962f04c922bb612c41f83a8f`.
- Remote isolated checkout:
  `/data/codex/repos/dsipa-dev-goal012-20260723T115300Z`.
- Actual national run id:
  `20260723T120648Z-goal012-layerA-consolidation`.
- Run scratch:
  `/data/codex/scratch/dsipa/20260723T120648Z-goal012-layerA-consolidation`.
- Complete artefact:
  `/data/codex/artifacts/dsipa/20260723T120648Z-goal012-layerA-consolidation`.
- Original pipeline terminal state: `failed`, exit code 1, preserved unchanged.
- Continuation terminal state: `passed`, exit code 0.
- Refreshed root `SHA256SUMS`: 43 entries, zero verification failures,
  index SHA-256
  `776f061cafc01f293509c0d25a367fe35443912543027ccd0875fcc5e45dad73`.

The earlier environment-only invocation
`20260723T115300Z-goal012-layerA-consolidation` stopped before input
preparation or Layer A computation because the base environment lacked
`build`. The orchestrator ruled it a preflight rather than the national
regression. The repaired no-compute environment proof is preserved at
`/data/codex/artifacts/dsipa/20260723T120648Z-goal012-layerA-consolidation-environment-preflight`.

## Implemented Scope

- One contract at `settings/layerA_reference_contract_v0_3_0.json` for frozen
  inputs, outputs, stable keys, headlines, and the 1,427/1,432 reconciliation.
- Fail-closed CAPAD, IBRA, Natural Earth, VIIRS, output, key, and headline
  validation.
- Checksum-first Natural Earth preparation and fingerprinted PA, land, and
  land-unprotected union caches.
- Stable canonical serialization for radiance, edge, and buffer-validity
  statewise and merged outputs.
- Offline text GeoJSON triad fixtures with real geometry and buffer tests.
- A self-locating runner, locked dev environment, explicit Layer A remote mode,
  ordered accepted reports, and pre/post validation.
- Duplicate-safe column-name multiset validation. Permuted columns pass;
  missing, extra, and duplicate names fail for CSV and GPKG attributes.

No Layer B module, manuscript, schema definition, dependency declaration,
scientific threshold, writer, generated national output, or accepted report was
edited in the salvage repair.

## Local And Fresh Validation

- Final focused reproducibility suite: 27 passed.
- Final full local suite: 70 passed, 9 expected large-output skips.
- Final source-only archive suite with dead HTTP proxies: 70 passed, 9 expected
  skips.
- Fresh triad test file: 4 passed; geometry and buffer checks both ran, not
  skipped.
- Shell syntax for both runners: passed.
- `git diff --check`: passed.
- Pre-run local wheel:
  `b39275e9ec8845ce138bf79d4031d4d0e957f60e0dee6bfadfe72c3977d6aa81`.
- Pre-run local sdist:
  `516da668b838ec65a18d25306df719d2f7b615da3c43d1a334a03354b4e3668c`.

The final source-only run used the existing locked project interpreter with
`PYTHONPATH` directed at an unpacked `git archive` plus the reviewed overlay.
An attempted cold offline `uv sync` could not find cached `pyogrio==0.12.1`;
this is an environment-bootstrap cache limitation, not a test-network
dependency. The test run itself used dead proxies and passed.

## National Run And Original Failure

The one actual computation used:

```text
DSIPA_SKIP_LAYERB=1
DSIPA_WORKERS=12
DSIPA_STATES=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT
analysis/run_full_pipeline.sh
```

Input validation passed before computation:

- CAPAD: 14,403 features; semantic SHA-256
  `148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf`.
- IBRA: 89 features; semantic SHA-256
  `3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332`.
- Natural Earth: 69,700 bytes; SHA-256
  `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`.
- All 12 VIIRS annual files matched their pinned MD5 values.

All ten state codes completed five statewise artefacts each. The pipeline ran
the Layer A science and accepted report modules, explicitly skipped Layer B,
and failed only when the original validator compared ordered column tuples:

```text
ContractError: Column mismatch:
data/processed/pa_radiance_buffers_national_v0_3_0.csv
```

`continuation/column-audit-before.json` records actual and expected ordered
columns for all nine files. Five CSVs and the GPKG had `tuple_equal=false`;
all nine had `name_multiset_equal=true`, no duplicate names, and empty
missing/extra lists. Three CSVs already matched tuple order. Thus the failure
was a validator/schema-order assumption, not scientific or schema-content
drift.

## Existing-Output Continuation

Only these two repaired sources were refreshed remotely:

- `src/python/dsipa/layerA_reproducibility.py`
- `tests/python/test_layerA_reproducibility.py`

The continuation ran from 01:59:32 to 02:00:11 Australia/Hobart time:

1. `validate-outputs` on the existing nine files: passed.
2. Full remote pytest: 79 passed, no failures.
3. Wheel and sdist build: passed.
4. All-nine reconcile against the Goal 011 checkout: passed.
5. Pre/post output SHA-256 comparison: identical.

Continuation build hashes:

- wheel:
  `5a0aa062df3886b9030714ad68ac00029ffaa62417af6a035fe418227b69b90d`;
- sdist:
  `1d119b2f6eac212d40a6fcacf7af1cbbe3f71f0bfb63ce95c2c7482aab4e6a63`.

## Nine-Output Evidence

| Output | Rows | Goal 012 SHA-256 | Ordering | Goal 011 |
| --- | ---: | --- | ---: | --- |
| `pa_radiance_buffers_national_v0_3_0.csv` | 900,768 | `63e95fb...2ec1` | 0 descents | semantic exact |
| `pa_edge_profiles_national_v0_3_0.csv` | 400,788 | `ddb9c9f...783b` | 0 descents | semantic exact |
| `pa_buffer_validity_v0_3_0.csv` | 22,266 | `c64b042...11f7f` | 0 descents | semantic exact |
| `pa_trends_v0_3_0.csv` | 53,112 | `d7d33e9...ff1f` | 0 descents | byte exact |
| `pa_risk_rankings_v0_3_0.csv` | 3,858 | `554c02e...367a` | 0 descents | byte exact |
| `pa_geometries_v0_3_0.csv` | 11,133 | `781e80b...695b` | 0 descents | byte exact |
| `pa_geometries_v0_3_0.gpkg` | 11,133 | `da843f5...d0e6` | n/a | attribute/CRS/WKB exact |
| `pa_ibra_assignment_v0_3_0.csv` | 11,098 | `3f0d8f7...82cf` | 0 descents | byte exact |
| `pa_trend_bootstrap_summary_v0_3_0.csv` | 4,426 | `cd3c165...8920` | 0 descents | byte exact |

The three canonical-order CSVs differ from Goal 011 only because Goal 012
removes 1,941, 845, and the corresponding buffer-validity key descents. The
GPKG differs only in container metadata; attributes, CRS, and WKB geometries
are exact. The other five CSVs are byte-identical. Exact full hashes are in
`continuation/output-sha256-before.txt`,
`continuation/output-sha256-after.txt`,
`continuation/layerA-output-validation.json`, and
`continuation/reconciliation.json`.

## Headlines And Reports

All frozen values match:

- protected-area universe: 11,133;
- eligible trend subset: 4,426;
- zero 2024 inside mean: 3,844;
- exact-zero inside slopes: 3,969;
- positive inside slopes: 420;
- retention denominator: 3,858;
- Q1/Q2/Q3/Q4: 305/55/3,308/190;
- complete rings: 383; and
- ring-1 valid: 1,432 / 0.12862660558699363, rendered as 12.9%.

The preserved generated report artefacts contain 1,432 and 12.9% in
`layerA_denominators_and_censoring.{csv,md}`,
`layerA_edge_profile_decision.{csv,md}`, and
`layerA_table1_candidate.md`. No generated canonical report contains 1,427 or
12.8%. Historical 1,427 appears only in the reference contract's explicit
reconciliation record.

## Evidence Layout

The artefact root preserves the original command, environment, source overlay,
input validation, nine outputs, seven reports, failed status, and checksum
index. `continuation/` separately preserves:

- original failed log and status copies;
- exact pre/post output hashes;
- pre-repair column audit for all nine files;
- repaired-source hashes before and after overlay;
- cache and fingerprint hashes;
- output validation and Goal 011 reconciliation JSON;
- full continuation log and terminal status; and
- wheel/sdist outputs and hashes.

## Residual Risk And Recommendation

No scientific drift, missing/extra/duplicate column, key defect, semantic
difference, GPKG attribute/CRS/WKB difference, headline mismatch, or output
mutation was found. The only material residual limitation is that the original
pipeline status remains honestly failed because the validator defect was
discovered after the single allowed computation. The separate continuation
proves the repaired gates on those exact unchanged outputs.

Recommendation: accept Goal 012 as a scientifically concordant, reproducibly
validated Layer A closeout, retain the transparent two-status evidence model,
and keep commit, push, DOI, upload, and publication actions gated on explicit
orchestrator/Barry approval.

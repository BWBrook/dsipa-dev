# Goal 011 Layer A Preservation Closeout

Status: **terminal concordant but non-exact reproduction; independently
accepted as the archive candidate**.

Generated: 2026-07-23 UTC.

## Identity

- Local repo: `/Users/bwbrook/papers/dsipa-dev`
- Local branch: `main`
- Local HEAD and `origin/main`:
  `7f46a00f74c32881034f0129728b3d80eedd2442`
- Accepted tree: `c82ebdda83c987d2e1dcc79fb2dba2759f9d7739`
- Remote host: `deep-server` via `deep-server-ts`
- Run id: `20260723T062202Z-goal011-layerA-preservation`
- Remote repo:
  `/data/codex/repos/dsipa-dev-goal011-20260723T062202Z`
- Remote artefact:
  `/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation`
- Remote scratch:
  `/data/codex/scratch/dsipa/20260723T062202Z-goal011-layerA-preservation`

## Input Gate

The fail-closed gate passed:

- CAPAD: 14,403 raw features; accepted semantic PA hash matched.
- IBRA: 89 features; accepted semantic IBRA hash matched.
- Nightlights: all 12 Zenodo/OpenGeoHub v0.4 annual files passed their
  code-pinned MD5 values.
- Natural Earth: marker `4.1.0`, 69,700 bytes, SHA-256
  `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`.

Natural Earth remains version-reacquirable but not historically byte-pinned.
The accepted source archive had 354 entries and SHA-256
`a0e9b77fb4f6e75d9dac9477a8fa6877b2956e8351e8b142531d7bdf6518b02e`.

## Terminal Outcome

The unchanged pipeline ran with:

```text
DSIPA_SKIP_LAYERB=1
DSIPA_WORKERS=12
DSIPA_STATES=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT
analysis/run_full_pipeline.sh
```

It ended terminal `failed` with exit code 1. All national computation,
trends, uncertainty, vulnerability, report, and figure stages completed. QA
then found two absent ignored triad GPKG fixtures in the clean source archive:
47 tests passed and 2 failed, and `set -e` prevented the build.

The authorized validation-only repair generated the missing fixtures with the
existing triad module. Full pytest then passed 49 tests in 6.89 seconds, and
the existing build command produced both wheel and sdist. No source,
scientific configuration, threshold, schema, or manuscript file was edited.

## Nine-File Result

All nine approved outputs are preserved in the remote artefact.

| Output | Result |
| --- | --- |
| Radiance buffers CSV | Byte-different; no detected primary scientific drift; historical row equality unproven |
| Edge profiles CSV | Bounded secondary threshold-sensitive drift |
| Buffer validity CSV | Historical SHA-256 exact |
| Trends CSV | Historical SHA-256 exact |
| Risk rankings CSV | Historical SHA-256 exact |
| Geometry CSV | Historical SHA-256 exact |
| Geometry GPKG | Byte-different container; no detected within-run semantic geometry drift; historical feature equality unproven |
| IBRA assignment CSV | Historical SHA-256 exact |
| Bootstrap summary CSV | Historical SHA-256 exact |

Six of nine historical hashes match exactly.

## Scientific Reconciliation

Every accepted primary headline value matches the regenerated payload:

| Quantity | Regenerated |
| --- | ---: |
| PA universe | 11,133 |
| Eligible baseline/trend subset | 4,426 |
| 2024 zero inside mean | 3,844/4,426 |
| Exact-zero inside slopes | 3,969/4,426 |
| Positive inside slopes | 420/4,426 |
| Retention denominator | 3,858 |
| Q1/Q2/Q3/Q4 | 305/55/3,308/190 |
| Complete rings | 383 |

The edge diagnostic has one bounded secondary difference. The canonical
edge-decision output changes 1-5 km valid PAs from 1,427 to 1,432, while
ring-1 non-null PA-years change from 116,472 to 116,412. Complete-ring n=383,
the primary science, the edge figure, and conditional non-zero shares of
18.02%, 9.40%, and 3.66% are unchanged. The +5 PAs equal +0.35% relative to
1,427 and +0.045 percentage points of the 11,133-PA universe. The -60 non-null
PA-years equal -0.052% of 116,472. Thirty current ring-1 PAs are exactly on
the 10-pixel threshold, so near-threshold rasterization/environment
sensitivity is the best current explanation. This is an inference, not a
proved cause.

The radiance CSV cannot be called row-identical because the historical payload
is unavailable, even though its size, schema/grain, primary downstream hashes,
and all primary headlines are concordant. The regenerated GPKG is
attribute/WKB-identical to the independently input-gated copy from this run,
but the historical GPKG is also unavailable.

## Decision

Independent scientific rereview accepted Goal 011, found the edge difference
immaterial to the paper conclusions, and accepted the regenerated payload as
the archive candidate. No further Goal 011 science is required.

DOI upload remains on hold only until:

1. canonical release surfaces use 1,432 and 12.9% for 1-5 km ring feasibility,
   while reconciliation retains the historical 1,427 versus regenerated
   1,432 comparison;
2. clean-checkout QA generates or includes the triad fixtures before the full
   test/build sequence; and
3. archive metadata states that this is a concordant non-exact reproduction
   and retains the unresolved historical row-level radiance and feature-level
   GPKG limitations.

Do not rerun merely to chase bytes. A new scientific run is justified only by
recovered historical payloads or a deliberate environment-pinning experiment.

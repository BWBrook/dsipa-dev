# Layer A Preservation Reproduction

Date: 2026-07-23 UTC

## Outcome

Goal 011 completed a terminal controlled preservation run at accepted commit
`7f46a00f74c32881034f0129728b3d80eedd2442`.

The exact source and fail-closed input gate passed. All nine approved Layer A
outputs were regenerated and preserved at:

```text
/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation
```

The pipeline ended `failed` with exit code 1 because QA expected two ignored
triad fixtures absent from the clean source archive. The national analysis had
completed. A validation-only repair generated the fixtures; full pytest then
passed 49 tests and the package build succeeded. No scientific source,
configuration, method, threshold, schema, or manuscript content was changed.

## Reconciliation

Six of nine outputs match their historical SHA-256 exactly: buffer validity,
trends, risk rankings, geometry CSV, IBRA assignment, and bootstrap summary.

All accepted primary science matches:

- PA universe 11,133;
- eligible subset 4,426;
- 2024 zero inside mean 3,844;
- zero slopes 3,969 and positive slopes 420;
- retention denominator 3,858;
- quadrants 305, 55, 3,308, and 190; and
- complete rings 383.

The edge CSV has bounded secondary threshold-sensitive drift: 1-5 km valid PAs
are 1,432 versus accepted 1,427, while ring-1 non-null PA-years are 60 lower.
Complete-ring n and the edge figure are unchanged. Thirty current PAs sit
exactly on the 10-pixel cutoff. The practical differences are +0.35% relative
to 1,427, +0.045 percentage points of the 11,133-PA universe, and -0.052% of
116,472 non-null PA-years. Conditional non-zero shares remain 18.02%, 9.40%,
and 3.66%.

The radiance CSV is byte-different with no detected primary scientific drift,
but historical row-level equality cannot be proved. The geometry GPKG is
byte-different but matches the independent input-gate copy in attributes and
geometry WKB; historical feature-level equality also cannot be proved.

## Decision

Independent scientific rereview accepted Goal 011 as a concordant but
non-exact preservation reproduction, judged the edge difference immaterial to
the paper conclusions, and accepted the regenerated payload as the archive
candidate. No further Goal 011 science is required.

DOI upload remains on hold only until canonical release surfaces use 1,432 and
12.9% while reconciliation preserves old versus new, clean-checkout QA
generates or includes the triad fixtures, and archive metadata records the
concordant non-exact result plus the historical radiance/GPKG limitations.

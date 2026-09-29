# Corrected render plumbing — 19 September 2026

This tranche adds bounded rendering support for the spatial correction
analysis. `analysis/render_coauthor_figures.py` now accepts an explicit
`--input-manifest` and validates every consumed data, report, trajectory and
edge-profile input by filename, byte count and SHA-256 under the declared
`--data-root`. `--spatial-correction` additionally requires the correction
summary and records the corrected analysis identity in the render receipt.

Historical rendering retains the accepted inside-series and paired-quadrant
guards. Manifest mode retains the unchanged inside invariants (4,426 rows,
420 positive slopes, 3,969 zero slopes and 78 complete late-positive series)
while deriving paired and Q1–Q4 counts from the supplied corrected risk table.
Trajectory captions use the observed slope signs and record any change from
the four historical labels. The aggregate edge-profile figure is rendered
from the supplied edge table with an explicit output path and is included in
the render manifest. The Layer B report remains a required rendering input.

`analysis/build_coauthor_tables.py` now derives S4/S5 cohort denominators from
the preserved audit summaries, checks that the positive tercile table still
contains 420 records, labels the S2 indicator coefficient correctly, and can
append optional Table S6 with baseline, geometry-only and corrected paired
quadrant counts from `spatial_correction_summary.json`. S6 is explicitly
labelled as historical-support sensitivity rather than the original correct
estimation.

Verification on the local checkout:

- `python3 -m py_compile` passed for the two builders and the edge-profile
  figure module.
- Focused tests passed: 11 tests in the renderer, input-contract and corrected
  plumbing test modules.
- Both command-line help screens expose `--input-manifest` and/or
  `--spatial-correction`.
- No manuscript figures or generated manuscript text were written by this
  plumbing change.

The corrected national input manifest and corrected summary variant-count
payload remain parent-run inputs. The S6 renderer accepts either a top-level
`variants` map or the equivalent comparison receipt when it includes explicit
baseline category counts.

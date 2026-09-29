# Layer A edge/penetration decision report

Generated: 2026-09-19 05:50 UTC

This report resolves the Stage 2 edge/penetration critique. The current edge figure should be retained as a feasibility-limited diagnostic using ring feasibility plus conditional non-zero share, not interpreted as a definitive penetration-gradient test.

## Ring feasibility and conditional signal

| ring_index | ring_inner_km | ring_outer_km | valid_pa_n | valid_pa_fraction | complete_pa_n | complete_pa_fraction | complete_frac_gt0_median | complete_frac_gt0_mean | complete_nonzero_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | 0.000 | 1.000 | 4426.000 | 0.398 | 369.000 | 0.033 | 0.000 | 0.002 | 0.176 |
| 1.000 | 1.000 | 5.000 | 1398.000 | 0.126 | 369.000 | 0.033 | 0.000 | 0.001 | 0.089 |
| 2.000 | 5.000 | 10.000 | 369.000 | 0.033 | 369.000 | 0.033 | 0.000 | 0.003 | 0.035 |

## Decision

Retain the existing ring widths (0-1, 1-5, 5-10 km) for this manuscript pass and do not add adaptive rings in Stage 2. Complete-ring coverage is too small for a new adaptive analysis to become a primary result without substantial revalidation. The figure/caption should state that median `frac_gt0` is zero under floor domination and that the plotted conditional non-zero share is a diagnostic, not proof of absence or presence of edge effects.

## Validation notes

- Ring valid fractions are within [0,1].
- Complete-ring fractions are within [0,1].
- Complete-ring median frac_gt0 is zero in all rings, so median profiles are not interpretable as absence of edge effect.
- Complete-ring coverage is <5% of the PA universe, so edge profiles are feasibility-limited diagnostics.

# 102 Layer B modelling (WP0.16) — complete

Date: 2026-01-05

## Summary
- Implemented `dsipa.layerB_model` for provider-matched modelling, spatial blocking, falsification, and sensitivity run.
- Added Layer B model input summary schema + tests, and updated schema reference + figure inventory.

## Outputs generated
- `analysis/reports/layerB_modelling_report.md`
- `manuscript/figures/fig_layerB_alan_effects.png`
- `data/processed/layerB_model_input_summary_v0_3_0.csv`

## Notes
- Primary run uses provider-matched dr368 for microbats vs passerines.
- Sensitivity run subsamples passerines with `--sensitivity-sample-rate 0.1` for runtime feasibility; full multi-provider sensitivity should be re-run when compute permits.
- Falsification uses within-block ALAN shuffling.

## Update (2026-01-05)
- Ran `dsipa.layerB_model` with `--sensitivity-sample-rate 0.1`; generated report, figure, and input summary.
- Updated schema reference, figure inventory, and Layer B go/no-go report.
- Tests pass (`uv run pytest`); built sdist + wheel (`uv run python -m build`).
- Roadmap updated to mark WP0.16 complete; canonical artefact will be rebuilt on clean HEAD.

## Update (2026-01-05, later)
- Re-ran sensitivity at full scale (`--sensitivity-sample-rate 1.0`), updating the modelling report, figure, and model input summary.
- Updated interpretation notes and data checksum to reflect the full sensitivity run.

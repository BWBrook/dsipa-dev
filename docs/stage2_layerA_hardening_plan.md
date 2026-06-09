# Stage 2 Layer A hardening plan

Status: closeout ready, opened 2026-05-25 after Stage 1 matrix acceptance; S2.9 validation completed 2026-05-25 and awaiting user signoff.

## Baseline

- Stage 1 matrix: accepted by the user on 2026-05-25.
- DSIPA code baseline: `main` at `dab3ddb`.
- Current worktree state at Stage 2 opening: Stage 1/2 planning documents are uncommitted; no science outputs have been changed in this Stage 2 pass yet.
- Evidence snapshot: `deep-server` reconciliation shows 38/38 expected files present and checksum verified.
- Layer A evidence schema: `v0.3.0`.

## Objective

Resolve the Stage 2 Layer A items from `docs/stage1_critique_resolution_matrix.md` before any Stage 3 Layer B reconciliation or Stage 4 manuscript rewrite:

- A01: denominator and subset clarity.
- A02: "missing" versus "ineligible" terminology.
- A03: floor/censoring as a central result.
- A04: defensible bright/dark anchor checks.
- A05: valid-buffer conditioning for external-pressure claims.
- A06: interpretable inside-vs-buffer sanity checks under floor domination.
- A07: edge/penetration figure misread risk.
- A08: adaptive/min-area ring decision.
- A09: trend threshold sensitivity.
- A10: uncertainty-aware ranking/watchlist interpretation.
- A11: retention quadrant denominator and selection rule.
- A12: manuscript-ready Table S1 watchlists.
- A13: simplified dominance summary decision.
- A14: manuscript-ready Table 1 feasibility/censoring denominators.

Also apply the Stage 2 parts of R03, R07, R08, M02, and M05: tmux-safe heavy runs, canonical artefacts, result/artefact review cycles, and evidence-traceable tables/captions.

## Non-goals

- Do not revise Layer B except to avoid breaking shared reports or build steps.
- Do not perform the Stage 4 full manuscript rewrite.
- Do not resolve final external archive/DOI release gates.
- Do not rerun the full national raster pipeline unless Stage 2 checks show it is necessary. Most Stage 2 work should be possible from the verified `v0.3.0` processed Layer A tables.

## Source artefacts

Primary inputs:

- `data/processed/pa_geometries_v0_3_0.csv`
- `data/processed/pa_geometries_v0_3_0.gpkg`
- `data/processed/pa_radiance_buffers_national_v0_3_0.csv`
- `data/processed/pa_edge_profiles_national_v0_3_0.csv`
- `data/processed/pa_buffer_validity_v0_3_0.csv`
- `data/processed/pa_trends_v0_3_0.csv`
- `data/processed/pa_risk_rankings_v0_3_0.csv`
- `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv`
- `analysis/reports/national_layerA_coverage_and_sanity.md`
- `analysis/reports/layerA_sanity_dashboard.md`
- `analysis/reports/trends_methods_and_sanity.md`
- `analysis/reports/risk_rankings_and_quadrants.md`
- `analysis/reports/pa_trend_uncertainty.md`
- `analysis/reports/pa_trend_dominance_matrix.csv`
- `manuscript/text/tables.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_figures.md`

## Compute strategy

Default to the Mac mini for table/report work that only reads processed CSV/GPKG files.

Use `deep-server` under `tmux` for any multi-hour raster regeneration or full-pipeline validation. From the Mac mini, the harness defaults to the Tailscale SSH alias `deep-server-ts` and the synced scratch checkout at `/data/codex/repos/dsipa-dev-mac-sync`:

```bash
analysis/deep_server_tmux_run.sh --mode custom --run-id 20260525T000000Z-stage2-layerA --command 'uv run python -m dsipa.layerA_sanity && uv run python -m dsipa.trends && uv run python -m dsipa.trend_uncertainty && uv run python -m dsipa.vulnerability_model && uv run python -m dsipa.figures_layerA'
```

For dirty Mac working-tree runs that must be exercised remotely before commit,
sync a scratch copy first and point the tmux harness at it:

```bash
analysis/sync_to_deep_server.sh
analysis/deep_server_tmux_run.sh --mode custom --command 'uv run python -m pytest -rs'
```

If the statewise raster pipeline must be rerun, use the existing harness rather than an interactive shell:

```bash
analysis/deep_server_tmux_run.sh --mode full --run-id 20260525T000000Z-stage2-full --workers 16
```

Worker policy:

- Start with 16 workers for geospatial/raster-heavy statewise work; increase only after inspecting memory and I/O in the run snapshot.
- Do not assume 64 CPUs means 64 safe geospatial workers. Raster windows, geometry operations, and Python process memory can make 16-24 workers a better first ceiling on 128 GB RAM.
- For sensitivity work based on existing processed tables, prefer single-process or modest local parallelism; the bottleneck is not raster sampling.

## Work packages

### S2.1 Stage gate and acceptance bookkeeping

Mark Stage 1 as accepted, update `docs/stage_overview.md`, and open the Stage 2 log.

Acceptance:

- Stage 1 checklist marks user acceptance.
- Stage overview shows Stage 1 complete and Stage 2 active.
- `docs/log/121_stage2_layerA_hardening.md` records the opening state.

### S2.2 Denominator and censoring table engine

Resolve A01, A03, A11, and A14 by creating a single source of truth for Layer A denominators, eligibility, zero mass, and selection rules.

Expected outputs:

- A generated report/table under `analysis/reports/`, for example `layerA_denominators_and_censoring.md` plus a CSV/JSON companion if useful.
- Updated `manuscript/text/tables.md` with Table 1 values only after validation.

Acceptance:

- Counts reconcile the PA universe, 2024 inside eligibility, trend eligibility, retention quadrant eligibility, and ring feasibility.
- Zero-mass values are reported for baseline inside mean and primary inside trend slopes.
- Values are generated from data, not hand-invented from narrative memory.
- Tests or sanity assertions fail on denominator drift.

### S2.3 Figure-label and caption hygiene

Resolve A02 and support M02 by removing misleading "missing" terminology for protected areas that fail minimum-pixel eligibility.

Expected outputs:

- Updated `src/python/dsipa/figures_layerA.py` if source titles still emit "missing".
- Regenerated affected figure(s), if needed.
- Updated captions if any stale wording remains.

Acceptance:

- Paper-facing figure/caption language distinguishes ineligible protected areas from true missing data.
- `rg` over current paper-facing files finds no stale "missing" language for the eligibility panel unless explicitly defined.

### S2.4 Anchor and sanity dashboard hardening

Resolve A04 and A06 by replacing the weak nearest-city median check with defensible bright/dark anchors and a clearer inside-vs-buffer sanity story.

Expected outputs:

- Updated `analysis/reports/layerA_sanity_dashboard.md` and/or a companion anchor report.
- Code changes in `src/python/dsipa/layerA_sanity.py` if anchor generation is embedded there.

Acceptance:

- Bright anchors are defined by explicit criteria, such as urban-adjacent protected areas or known high-radiance PA/buffer contexts.
- Dark anchors are defined by remote/interior criteria.
- The report explains floor domination and does not rely on a misleading all-PA aggregate to support external-pressure interpretation.

### S2.5 Buffer-validity sensitivity

Resolve A05 and reinforce A11 by testing how external-pressure and quadrant statements behave under stricter buffer-validity criteria.

Expected outputs:

- A buffer-validity sensitivity report/table under `analysis/reports/`.
- If useful, a compact supplementary table or Methods note.

Acceptance:

- Primary retention/quadrant counts are compared against stricter valid-buffer subsets.
- Selection rules are explicit: `land_unprotected`, 1 km buffer, minimum valid years, minimum valid pixels, and any additional validity thresholds.
- If conclusions are sensitive, manuscript claims are narrowed accordingly.

### S2.6 Trend threshold sensitivity

Resolve A09 by checking sensitivity to valid-pixel and valid-year thresholds.

Expected outputs:

- A threshold-sensitivity report/table under `analysis/reports/`.
- Optional plot only if it clarifies a real decision.

Acceptance:

- At minimum compare the primary rule (`>=10` valid pixels, `>=8` valid years) with a small grid of stricter/looser alternatives.
- Report headline sample sizes, zero-slope fractions, positive-slope counts, and retention quadrant counts where computable.
- Decide whether the primary thresholds remain justified.

### S2.7 Edge/penetration figure decision

Resolve A07 and A08 by deciding whether the current edge figure is a feasibility-limited diagnostic or needs a different statistic/panel.

Expected outputs:

- Updated figure/caption if required.
- Decision note in `docs/decisions.md` if adaptive rings or minimum-area filters are rejected or adopted.

Acceptance:

- No paper-facing text implies that median-zero edge profiles prove no edge effect.
- Complete-ring subset size and zero-inflation are explicit.
- Adaptive/min-area decision is recorded.

### S2.8 Watchlist and uncertainty integration

Resolve A10, A12, and A13 by integrating bootstrap uncertainty into the risk/watchlist presentation.

Expected outputs:

- A generated Table S1 or source table under `manuscript/text/supplementary_tables.md`.
- A report/table joining category-safe rankings to bootstrap CIs/probability summaries.
- A simplified dominance summary if it improves interpretability.

Acceptance:

- Watchlists include PA ID/name/state/IBRA where available, slopes, retention index, and uncertainty fields.
- Text avoids over-precise rank claims.
- Dominance heatmap is either supported by a simplified summary or explicitly kept as an advanced diagnostic only.

### S2.9 Result and artefact review cycle

Resolve R07 and R08 for Stage 2.

Expected outputs:

- Canonical Stage 2 artefact folder, for example `artefacts/stage2_layerA_hardening/`.
- Manifest/README identifying git state, source data checksums, commands, outputs, and known caveats.
- Updates to `docs/interpretation_notes.md` for any new or materially changed main Layer A results.

Acceptance:

- `git diff --check` passes.
- Relevant Layer A tests pass.
- Full test/build gate is run unless explicitly deferred with a reason.
- Stage 2 log records sanity verdicts, not just command success.

## Proposed execution order

1. S2.1 acceptance bookkeeping.
2. S2.3 quick terminology fix for "missing" versus "ineligible".
3. S2.2 denominator/censoring table engine and Table 1.
4. S2.4 anchor/sanity dashboard hardening.
5. S2.5 buffer-validity sensitivity.
6. S2.6 trend threshold sensitivity.
7. S2.7 edge/penetration decision and figure/caption update.
8. S2.8 watchlist uncertainty integration and Table S1.
9. S2.9 artefact packaging, interpretation notes, validation, and closeout.

## Validation bundle

Minimum local validation after Stage 2 code/table changes:

```bash
git diff --check
uv run pytest tests/python/test_trends.py tests/python/test_risk_rankings.py tests/python/test_trend_uncertainty.py -q
uv run pytest -rs
uv build --out-dir /tmp/dsipa-build-stage2
```

Domain validation:

- Denominator report matches known invariants and explains every main Layer A `n`.
- Baseline figure and caption use ineligible/minimum-pixel terminology.
- Bright/dark anchor report passes a plain-language sanity inspection.
- Buffer-validity sensitivity does not silently change the interpretation, or any change is carried into manuscript constraints.
- Trend threshold sensitivity supports or revises the primary threshold decision.
- Edge figure/caption cannot be read as "no edge effect" without the feasibility caveat.
- Watchlists include uncertainty and avoid over-precise ranking.

## Stage 2 exit gate

Stage 2 can close only when all of the following are true:

- A01-A14 are marked resolved, superseded, or explicitly deferred with a reason.
- Table 1 and Table S1 are populated from validated evidence.
- Any regenerated figures have updated captions and interpretation notes.
- Stage 2 artefacts and logs exist.
- Required tests/build/domain sanity checks pass or are explicitly deferred with a justified reason.
- The closeout report recommends whether Stage 3 can start.

# Decisions (irreversible or costly to change)

Add new rows as decisions are made; do not delete old ones.
Mark superseded items in **Status** (active / superseded / reverted) rather than removing them.

| Date (UTC) | Decision ID | Decision            | Rationale / evidence | Status | Links (log/commit/artefact) |
| ---------- | ----------- | ------------------- | -------------------- | ------ | --------------------------- |
| 2026-01-01 | DEC-001     | Python 3.12 + uv-managed environment; package via pyproject/setuptools | Matches repo guidance; uv available; enables reproducible builds/tests | active | docs/log/000_bootstrap.md |
| 2026-01-01 | DEC-002     | CAPAD 2024 via DCCEEW ArcGIS REST; include terrestrial PAs only for Layer A core | CAPAD 2024 is current national compilation; REST service supports reproducible access; terrestrial focus avoids marine ALAN confounds | active | analysis/reports/data_inventory.md |
| 2026-01-01 | DEC-003     | VIIRS DNB annual VNL v2.2 (EOG), using median-masked radiance band | Annual global series with documented methods; median-masked reduces transient outliers; public-domain source | superseded | analysis/reports/data_inventory.md |
| 2026-01-01 | DEC-003     | Zenodo 10.5281/zenodo.17294744 (Hengl v0.4), annual average VIIRS layer; 2013–2024 core years; smoke-test years 2013/2018/2024; apply raster scale/offset metadata to pixel values (scale=10 for 2022–2024, scale=1 for earlier years) | Open CC-BY data without auth; matches VIIRS annual series; avoids EOG OpenID gate; scale metadata required for year-to-year comparability | active | docs/log/060_national_run.md |
| 2026-01-01 | DEC-004     | Use EPSG:3577 (GDA94 / Australian Albers) for distance/buffer operations | Equal-area projection suitable for national-scale Australia distances | active | analysis/reports/triad_qa_manifest.json |
| 2026-01-01 | DEC-005     | Smoke-test buffers: 1 km + 5 km outside; rings: 0–1, 1–5, 5–10 km inside | Provides near-edge and interior gradients for QA while keeping compute light | active | analysis/reports/triad_qa_manifest.json |
| 2026-01-01 | DEC-008     | Output schema v0.1.0 defined for smoke-test Layer A tables (triad index/rings/buffers, PA geometries, radiance buffers, edge profiles); schema changes require version bump and full rerun | Locks column definitions before national scaling; avoids silent schema drift | active | analysis/reports/output_schema_reference.md |
| 2026-01-01 | DEC-006     | Minimum valid pixel threshold for radiance metrics = 10 pixels; rows below threshold are flagged in reports and treated as missing in trend estimation | Prevents unstable summaries for tiny geometries or rings | active | docs/log/050_scale_policy.md |
| 2026-01-01 | DEC-007     | Trend estimator = Theil-Sen on median radiance; require >=8 valid years; retention index = inside slope minus buffer slope (1 km, 5 km) | Robust to outliers; interpretable inside-vs-outside comparison | superseded | docs/log/070_trends.md |
| 2026-01-01 | DEC-010     | Stable protected-area ID = CAPAD PA_ID; dissolve multipart features by PA_ID | PA_ID is unique within CAPAD 2024; dissolving yields one geometry per PA | active | analysis/reports/pa_geometry_qc.md |
| 2026-01-02 | DEC-009     | Layer B go/no-go = conditional-go; focal taxa = microbats (Chiroptera excluding Pteropodidae); negative controls = diurnal birds + diurnal reptiles; bias strategy = target-group background + spatial blocking + falsification checks | Keeps Layer B conservative and falsifiable while aligning with ALAN sensitivity hypothesis | active | docs/layerB_gonogo.json; analysis/reports/layerB_gonogo.md |
| 2026-01-02 | DEC-011     | Do not exclude micro-area PAs at baseline; retain min_valid_pixels=10 and apply trend completeness filters; treat area <0.01 km2 and median valid pixels <10 as sensitivity-only filters for later modelling | Raising thresholds would drop most PAs; micro-area group is small and can be handled in sensitivity analyses | active | docs/log/085_layerB_gonogo.md |
| 2026-01-02 | DEC-012     | Trend estimator = Theil-Sen on mean radiance (primary) with median trends retained as robustness; require >=8 valid years; retention indices computed on mean slopes | Mean avoids zero-median quantization while preserving robust median as sensitivity check | active | docs/log/090_layerA_metric_corrections.md |
| 2026-01-02 | DEC-013     | Replace OLS “vulnerability coefficients” with risk/retention results: ranked risk tables + quadrant plot; optional classifier only if evaluated out-of-sample | Aligns outputs to dark-sky integrity hypothesis and avoids unstable collinear coefficients | active | docs/log/090_layerA_metric_corrections.md |
| 2026-01-02 | DEC-014     | Bump output schema_version to v0.2.0 for Layer A metric corrections (mean trends + expanded risk table fields) | Schema changes require a version bump and migration of processed outputs | active | docs/log/090_layerA_metric_corrections.md |
| 2026-01-02 | DEC-015     | Buffer validity decomposition: compute raw vs land vs land_unprotected buffers using Natural Earth landmask; treat land_unprotected as the primary “outside” buffer for retention analyses | Outside buffers can include ocean or other protected areas; land + unprotected masks reduce confounding when interpreting encroachment | active | docs/log/095_layerA_validity_censoring.md |
| 2026-01-02 | DEC-016     | Add censoring-aware exposure metrics (frac_gt0 and p95) alongside mean/median for inside/buffer summaries and trends | Mean/median are dominated by floor effects at 500 m; additional metrics provide detectable variation while staying interpretable | active | docs/log/095_layerA_validity_censoring.md |
| 2026-01-02 | DEC-017     | Bump output schema_version to v0.3.0 for buffer validity + censoring-aware metrics | Adds new columns (buffer_type, frac_gt0, p95, buffer validity table) requiring full rerun | active | docs/log/095_layerA_validity_censoring.md |
| 2026-01-02 | DEC-018     | Record CAPAD service snapshot metadata + hashed geometry signature in `data/raw/capad_snapshot` during PA processing | ArcGIS REST services are mutable; snapshot metadata provides a reproducibility anchor without storing raw features in git | active | docs/log/095_layerA_validity_censoring.md |
| 2026-01-02 | DEC-019     | Add cached union geometries + optional statewise runner for Layer A metrics to control runtime | National raster summaries are slow; cached unions and statewise merge enable resumable, auditable runs without changing outputs | active | docs/log/095_layerA_validity_censoring.md |
| 2026-01-02 | DEC-020     | Buffer validity overlap metrics computed on land-masked overlap (land_union \ PAs); effective_land_area_km2 equals land-unprotected area | Aligns overlap metric with land-only ALAN interpretation and avoids per-buffer intersections with full PA union | active | docs/log/096_layerA_performance.md |
| 2026-01-02 | DEC-021     | Simplify PA geometries by 500 m tolerance + use buffer resolution=1 (quadrant segments) for buffer/ring construction | 500 m raster resolution permits pixel-scale simplification; reduces buffer/ring compute time substantially | active | docs/log/096_layerA_performance.md |
| 2026-01-03 | DEC-022     | Do not track `artefacts/` in git; artefacts live locally and are archived to Zenodo for paper release | Artefacts are large and reproducible from pipeline; keeping them out of git avoids snapshot/size warnings while preserving reproducibility | active | docs/log/097_gate_0_5_2.md |
| 2026-01-03 | DEC-023     | Do not track national-scale `data/processed` outputs in git; keep smoke-test fixtures only | National outputs are large and reproducible; store them in Zenodo and skip tests when absent to keep the repo lightweight | active | docs/log/098_repo_hygiene.md |
| 2026-01-04 | DEC-024     | Include JBT and EXT in Layer A statewise runs so “national” matches all CAPAD terrestrial PAs | Avoid denominator mismatch (11133 vs 11112) and remove external-territory omissions in figures/reports | active | docs/log/099_pa_universe_harmonisation.md |
| 2026-01-04 | DEC-025     | Layer B downloads stored under `data/raw/ala_occurrences` and processed outputs under `data/processed/layerB` (ignored); negative-control proxies use Passeriformes (birds) and Squamata (reptiles) as diurnal groups | Keeps large occurrence data out of git; operationalises DEC-009 with tractable taxon filters | active | docs/log/100_layerB_data_acquisition.md |
| 2026-01-04 | DEC-026     | Proceed with Layer B using microbats + passerines only; defer diurnal reptiles control due to ALA download failures | ALA `occurrences/download` returns 500 for Squamata queries; proceed with primary control rather than block WP0.15; revisit if service recovers | active | docs/log/100_layerB_data_acquisition.md |
| 2026-01-04 | DEC-027     | Treat ALA occurrence downloads as mixed-provider licences; maintain a licence/provenance ledger and avoid blanket “CC-BY” claims | `citation.csv` includes CC BY‑NC and provider-specific conditions; publication requires explicit attribution | active | docs/log/101_layerB_qc_hardening.md |
| 2026-01-04 | DEC-028     | Primary Layer B analysis will be provider‑matched (NSW BioNet dr368) for microbats vs passerines; full multi‑provider dataset reserved for sensitivity | Microbats are ~89% NSW BioNet; provider-matched control is needed for interpretable comparisons and supports a NSW‑bounded case study | active | docs/log/101_layerB_qc_hardening.md |
| 2026-01-05 | DEC-029     | WP0.16 modelling constraints: two‑part ALAN covariates, spatial blocking (50 km default), and explicit falsification via ALAN shuffles | Zero‑inflated ALAN exposure and sampling bias require two‑part predictors and out‑of‑block evaluation; falsification guards against spurious effects | active | docs/log/101_layerB_qc_hardening.md |
| 2026-01-05 | DEC-030     | WP0.16 sensitivity run subsamples passerines at 10% (`--sensitivity-sample-rate 0.1`) for runtime feasibility; rerun full sensitivity when compute permits | Full multi‑provider scan exceeded practical runtime; subsampling keeps sensitivity descriptive while primary inference remains provider‑matched | superseded | docs/log/102_layerB_modelling.md |
| 2026-01-05 | DEC-031     | WP0.16 sensitivity run executed at full scale (`--sensitivity-sample-rate 1.0`) after compute became available | Provides a complete multi‑provider sensitivity check while keeping provider‑matched primary inference unchanged | active | docs/log/102_layerB_modelling.md |
| 2026-01-06 | DEC-032     | Layer A trend uncertainty quantified via IBRA7 region cluster bootstrap with moving-block time resampling (block_len=3, n_boot=300) | IBRA regions are ecologically coherent spatial units; clustered resampling mitigates spatial autocorrelation while block resampling handles temporal dependence at low cost | active | docs/log/106_layerA_trend_uncertainty.md |
| 2026-01-06 | DEC-033     | Layer B robustness: IBRA‑stratified occurrence summaries; falsification by shuffling ALAN within IBRA×year; heterogeneity check on log1p(ALAN) for regions with ≥500 records per class | Adds ecologically meaningful stratification and a reviewer‑friendly falsification; minimum counts avoid unstable IBRA‑specific fits | active | docs/log/107_layerB_ibra_robustness.md |
| 2026-05-14 | DEC-034     | Use `deep-server` tmux harness for heavy single-host DSIPA reruns and evidence reconciliation; keep run logs under `/data/codex/scratch/dsipa` and durable copied artefacts under `/data/codex/artifacts/dsipa` | The WSL control-plane can shut down during long runs; `deep-server` has 64 logical CPUs, 125 GiB RAM, existing complete DSIPA evidence outputs, and no scheduler, so tmux plus explicit run directories is the safest single-host pattern | active | docs/log/108_remote_harness_evidence_reconciliation.md; analysis/deep_server_tmux_run.sh |
| 2026-05-25 | DEC-035     | Retain fixed interior edge rings (0-1, 1-5, 5-10 km) for Stage 2 and do not add adaptive/min-area rings in this manuscript pass; frame the edge figure as a feasibility-limited diagnostic | Complete-ring coverage is only 383 PAs (3.4% of the PA universe), complete-ring median `frac_gt0` is zero in all rings, and a new adaptive-ring result would need substantial revalidation before it could become primary evidence | active | docs/log/121_stage2_layerA_hardening.md; analysis/reports/layerA_edge_profile_decision.md |
| 2026-05-29 | DEC-036     | Pin DSIPA local development to Python 3.12 (`>=3.12,<3.13`) with `.python-version`, uv sync, and a Mac bootstrap/readiness wrapper | The migrated WSL `.venv` was unusable on macOS and open-ended `>=3.12` allowed drift to newer/yanked packages; Python 3.12 is the repo contract and matches prior validation | active | docs/log/122_macos_readiness_makedoc.md; Makefile; analysis/bootstrap_macos.sh; analysis/check_macos_readiness.py |
| 2026-05-29 | DEC-037     | Build manuscript outputs through the external Mac `makedoc` checkout at `/Users/bwbrook/work/makedoc` using repo-local `settings/build.yaml`, `references/refs.yaml`, CSL, and author metadata | Keeps final manuscript assembly reproducible while reusing the maintained local build engine; avoids stale WSL `/mnt/c` and `/home` wrapper assumptions | active | docs/log/122_macos_readiness_makedoc.md; settings/build.yaml; analysis/makedoc.sh |
| 2026-05-29 | DEC-038     | For dirty Mac working-tree HPC runs, rsync a scratch checkout to `/data/codex/repos/dsipa-dev-mac-sync` via `deep-server-ts` and make that scratch checkout the default remote harness target | The direct campus SSH route can time out from the Mac mini, while the Tailscale alias is live; the scratch target allows remote validation of uncommitted Mac changes without disturbing durable evidence artefacts | active | docs/log/122_macos_readiness_makedoc.md; analysis/sync_to_deep_server.sh; analysis/deep_server_tmux_run.sh |

---

## Decision templates (DSIPA-NBS)

### DEC-001 — Primary language + environment
- Decision:
- Rationale:
- Status:

### DEC-002 — Protected area dataset version and inclusion rules
Examples of choices to record:
- CAPAD version/date
- terrestrial-only vs include marine
- minimum polygon area thresholds (if any)
- how overlapping polygons are handled (dissolve vs retain)

### DEC-003 — Night-lights product and preprocessing choices
Examples:
- product source and version
- annual vs monthly composites
- handling of negative/zero values
- any masking rules

### DEC-004 — Spatial reference system strategy
Examples:
- whether outputs use an equal-area projection
- whether pixel-area weighting is applied in geographic coordinates
- how buffers/rings are computed (distance metric assumptions)

### DEC-005 — Buffer and ring definitions
Record:
- outside buffer widths and distances
- inside ring widths
- whether rings are defined by Euclidean distance, geodesic distance, or raster distance transform

### DEC-006 — Radiance summary statistics
Record:
- median vs trimmed mean vs mean
- how outliers are treated
- how missing pixels are handled

### DEC-007 — Trend estimator and classification thresholds
Record:
- robust slope estimator
- uncertainty quantification approach
- thresholds for “brightening” vs “stable”

### DEC-008 — Output schema + schema_version policy
Record:
- filenames and required columns
- schema_version bump rules
- migration/testing requirements

### DEC-009 (optional) — Layer B: focal taxa and bias-control strategy
Record:
- taxa selection
- negative controls
- bias-control design and why it is defensible

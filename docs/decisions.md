# Decisions (irreversible or costly to change)

Add new rows as decisions are made; do not delete old ones.
Mark superseded items in **Status** (active / superseded / reverted) rather than removing them.

| Date (UTC) | Decision ID | Decision            | Rationale / evidence | Status | Links (log/commit/artefact) |
| ---------- | ----------- | ------------------- | -------------------- | ------ | --------------------------- |
| 2026-01-01 | DEC-001     | Python 3.12 + uv-managed environment; package via pyproject/setuptools | Matches repo guidance; uv available; enables reproducible builds/tests | active | docs/log/000_bootstrap.md |
| 2026-01-01 | DEC-002     | CAPAD 2024 via DCCEEW ArcGIS REST; include terrestrial PAs only for Layer A core | CAPAD 2024 is current national compilation; REST service supports reproducible access; terrestrial focus avoids marine ALAN confounds | active | analysis/reports/data_inventory.md |
| 2026-01-01 | DEC-003     | VIIRS DNB annual VNL v2.2 (EOG), using median-masked radiance band | Annual global series with documented methods; median-masked reduces transient outliers; public-domain source | superseded | analysis/reports/data_inventory.md |
| 2026-01-01 | DEC-003     | Zenodo 10.5281/zenodo.17294744 (Hengl v0.4), annual average VIIRS layer; 2013–2024 core years; smoke-test years 2013/2018/2024; use raw stored values pending scale clarification (metadata shows scale=10 only in 2024) | Open CC-BY data without auth; matches VIIRS annual series; avoids EOG OpenID gate | active | docs/log/035_radiance_buffers_smoketest.md |
| 2026-01-01 | DEC-004     | Use EPSG:3577 (GDA94 / Australian Albers) for distance/buffer operations | Equal-area projection suitable for national-scale Australia distances | active | analysis/reports/triad_qa_manifest.json |
| 2026-01-01 | DEC-005     | Smoke-test buffers: 1 km + 5 km outside; rings: 0–1, 1–5, 5–10 km inside | Provides near-edge and interior gradients for QA while keeping compute light | active | analysis/reports/triad_qa_manifest.json |
| 2026-01-01 | DEC-008     | Output schema v0.1.0 defined for smoke-test Layer A tables (triad index/rings/buffers, PA geometries, radiance buffers, edge profiles); schema changes require version bump and full rerun | Locks column definitions before national scaling; avoids silent schema drift | active | analysis/reports/output_schema_reference.md |
| 2026-01-01 | DEC-010     | Stable protected-area ID = CAPAD PA_ID; dissolve multipart features by PA_ID | PA_ID is unique within CAPAD 2024; dissolving yields one geometry per PA | active | analysis/reports/pa_geometry_qc.md |

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

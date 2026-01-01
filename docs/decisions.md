# Decisions (irreversible or costly to change)

Add new rows as decisions are made; do not delete old ones.
Mark superseded items in **Status** (active / superseded / reverted) rather than removing them.

| Date (UTC) | Decision ID | Decision            | Rationale / evidence | Status | Links (log/commit/artefact) |
| ---------- | ----------- | ------------------- | -------------------- | ------ | --------------------------- |
| _[fill]_   | _DEC-001_   | _[what was chosen]_ | _[why]_              | active | _[paths]_                   |

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

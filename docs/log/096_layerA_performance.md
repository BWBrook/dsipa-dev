# 096 Layer A performance tuning (statewise rerun)

Date: 2026-01-02

## Summary
- Reworked buffer validity overlap to use land-masked protected overlap (land_union \ PAs) and cached the land-unprotected union.
- Vectorized buffer/ring construction, added geometry simplification (500 m) and lower buffer resolution (quadrant segments=1).
- Added ring construction short-circuiting for small PAs using safe inradius/area thresholds.

## Notes
- Changes are intended to keep geometry operations aligned with 500 m raster resolution while reducing runtime.
- Statewise rerun is required for consistency; ongoing after performance updates.

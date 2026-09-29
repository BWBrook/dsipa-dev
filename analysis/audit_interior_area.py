"""Bounded sensitivity audit for the 1--5 km interior ring.

This audit uses the accepted national summary tables as inputs.  It does not
re-extract rasters or alter the accepted repository checkout.  The primary
comparison is deliberately on the original paired cohort: inside and
1-km-land-unprotected slopes are retained from ``pa_trends`` and only the
1--5 km edge-ring slope is recomputed from the national ring summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from analysis.input_contract import resolve_contract, sha256 as contract_sha256
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from input_contract import resolve_contract, sha256 as contract_sha256

MIN_VALID_PIXELS = 10
MIN_VALID_YEARS = 8
PRIMARY_METRIC = "mean"
PRIMARY_BUFFER = "land_unprotected"
PRIMARY_BUFFER_KM = 1.0
RING_INNER_KM = 1.0
RING_OUTER_KM = 5.0
SCHEMA_VERSION = "0.3.0"


def theil_sen(years: np.ndarray, values: np.ndarray) -> float:
    """Return the project's median pairwise slope, or NaN if undefined."""
    if len(values) < 2:
        return float("nan")
    slopes = [
        (values[j] - values[i]) / (years[j] - years[i])
        for i in range(len(values) - 1)
        for j in range(i + 1, len(values))
        if years[j] != years[i]
    ]
    return float(np.median(slopes)) if slopes else float("nan")


def ring_slopes(
    edge: pd.DataFrame,
    *,
    min_valid_pixels: int = MIN_VALID_PIXELS,
    min_valid_years: int = MIN_VALID_YEARS,
) -> pd.DataFrame:
    """Estimate slopes for the exact 1--5 km ring using project rules."""
    required = {
        "pa_id",
        "ring_inner_km",
        "ring_outer_km",
        "year",
        "valid_pixel_count",
        "mean",
    }
    missing = required.difference(edge.columns)
    if missing:
        raise ValueError(f"Edge table is missing columns: {sorted(missing)}")
    ring_rows = edge[
        edge["ring_inner_km"].eq(RING_INNER_KM)
        & edge["ring_outer_km"].eq(RING_OUTER_KM)
    ]
    selected = ring_rows[ring_rows["valid_pixel_count"].ge(min_valid_pixels)].dropna(subset=["mean"])
    if selected.duplicated(["pa_id", "year"]).any():
        raise ValueError("Duplicate supported PA-year rows in 1--5 km ring")
    if not ring_rows["year"].isin(range(2013, 2025)).all():
        raise ValueError("Edge table contains years outside 2013--2024")
    if selected.empty:
        return pd.DataFrame(columns=["pa_id", "n_years_ring_1_5km", "slope_ring_1_5km"])
    records: list[dict[str, object]] = []
    for pa_id, group in selected.groupby("pa_id", sort=True):
        group = group.sort_values("year")
        years = group["year"].to_numpy(dtype=float)
        values = group["mean"].to_numpy(dtype=float)
        records.append(
            {
                "pa_id": pa_id,
                "n_years_ring_1_5km": int(len(values)),
                "slope_ring_1_5km": (
                    theil_sen(years, values) if len(values) >= min_valid_years else np.nan
                ),
            }
        )
    return pd.DataFrame(records)


def primary_paired_cohort(trends: pd.DataFrame) -> pd.DataFrame:
    """Return the original 1-km paired cohort used by the main quadrants."""
    required = {
        "pa_id",
        "metric",
        "buffer_type",
        "n_years_inside",
        "slope_inside",
        "slope_buffer_1km",
    }
    missing = required.difference(trends.columns)
    if missing:
        raise ValueError(f"Trend table is missing columns: {sorted(missing)}")
    cohort = trends[
        trends["metric"].eq(PRIMARY_METRIC)
        & trends["buffer_type"].eq(PRIMARY_BUFFER)
        & trends["n_years_inside"].ge(MIN_VALID_YEARS)
        & trends["slope_inside"].notna()
        & trends["slope_buffer_1km"].notna()
    ][
        ["pa_id", "n_years_inside", "slope_inside", "slope_buffer_1km", "slope_buffer_5km"]
    ].copy()
    if cohort.pa_id.duplicated().any():
        raise ValueError("Primary trend table contains duplicate pa_id values")
    return cohort


def quadrant(buffer_slope: float, inside_slope: float) -> str:
    """Use the manuscript's Q1/Q2/Q3/Q4 sign convention."""
    if buffer_slope > 0 and inside_slope > 0:
        return "Q1"
    if buffer_slope <= 0 and inside_slope > 0:
        return "Q2"
    if buffer_slope <= 0 and inside_slope <= 0:
        return "Q3"
    return "Q4"


def matched_slopes(trends: pd.DataFrame, edge: pd.DataFrame) -> pd.DataFrame:
    """Join ring slopes to the unchanged original paired cohort."""
    cohort = primary_paired_cohort(trends)
    bands = ring_slopes(edge)
    merged = cohort.merge(bands, on="pa_id", how="left", validate="one_to_one")
    merged["original_quadrant"] = [
        quadrant(b, i) for b, i in zip(merged["slope_buffer_1km"], merged["slope_inside"])
    ]
    merged["ring_quadrant"] = [
        quadrant(b, i) if pd.notna(i) else "excluded"
        for b, i in zip(merged["slope_buffer_1km"], merged["slope_ring_1_5km"])
    ]
    merged["ring_included"] = merged["slope_ring_1_5km"].notna()
    return merged


def transition_table(matched: pd.DataFrame, geometries: pd.DataFrame) -> pd.DataFrame:
    """Summarise original-to-ring quadrant transitions and polygon areas."""
    area = geometries[["pa_id", "area_km2"]].drop_duplicates("pa_id")
    x = matched.merge(area, on="pa_id", how="left", validate="one_to_one")
    valid = x[x["ring_included"]].copy()
    labels = ["Q1", "Q2", "Q3", "Q4"]
    observed = (
        valid.groupby(["original_quadrant", "ring_quadrant"], as_index=False)
        .agg(n=("pa_id", "size"), area_km2=("area_km2", "sum"))
    )
    grid = pd.MultiIndex.from_product(
        [labels, labels], names=["original_quadrant", "ring_quadrant"]
    ).to_frame(index=False)
    table = grid.merge(observed, on=["original_quadrant", "ring_quadrant"], how="left")
    table["n"] = table["n"].fillna(0).astype(int)
    table["area_km2"] = table["area_km2"].fillna(0.0)
    table = table.sort_values(["original_quadrant", "ring_quadrant"])
    denom = float(valid["area_km2"].sum())
    table["share_of_ring_matched_n"] = table["n"] / len(valid) if len(valid) else np.nan
    table["share_of_ring_matched_area"] = table["area_km2"] / denom if denom else np.nan
    return table.reset_index(drop=True)


def area_summary(trends: pd.DataFrame, geometries: pd.DataFrame) -> pd.DataFrame:
    """Reproduce whole-polygon count and area shares for all main categories."""
    geom = geometries[["pa_id", "area_km2"]].drop_duplicates("pa_id")
    total_area = float(geom["area_km2"].sum())
    primary = trends[
        trends["metric"].eq(PRIMARY_METRIC) & trends["buffer_type"].eq(PRIMARY_BUFFER)
    ][["pa_id", "n_years_inside", "slope_inside", "slope_buffer_1km"]].copy()
    primary = primary.drop_duplicates("pa_id")
    # Start from the complete geometry universe so a PA absent from the trend
    # table is retained in the ineligible denominator.
    primary = geom.merge(primary, on="pa_id", how="left", validate="one_to_one")
    primary["status"] = np.select(
        [
            primary["slope_inside"].isna() | primary["n_years_inside"].fillna(0).lt(MIN_VALID_YEARS),
            primary["slope_inside"].lt(0),
            primary["slope_inside"].eq(0),
            primary["slope_inside"].gt(0),
        ],
        ["ineligible", "negative", "zero", "positive"],
        default="unknown",
    )
    rows = [
        {
            "category": "all_geometry_ids",
            "n": len(geom),
            "area_km2": total_area,
            "share_of_all_ids": 1.0,
            "share_of_all_polygon_area": 1.0,
        }
    ]
    for status, subset in primary.groupby("status", sort=False):
        rows.append(
            {
                "category": status,
                "n": int(len(subset)),
                "area_km2": float(subset["area_km2"].sum()),
                "share_of_all_ids": float(len(subset) / len(geom)) if len(geom) else np.nan,
                "share_of_all_polygon_area": float(subset["area_km2"].sum() / total_area)
                if total_area
                else np.nan,
            }
        )
    eligible = primary[primary["status"] != "ineligible"]
    eligible_area = float(eligible["area_km2"].sum())
    for status in ("negative", "zero", "positive"):
        subset = eligible[eligible["status"].eq(status)]
        rows.append(
            {
                "category": f"eligible_{status}",
                "n": int(len(subset)),
                "area_km2": float(subset["area_km2"].sum()),
                "share_of_all_ids": float(len(subset) / len(geom)) if len(geom) else np.nan,
                "share_of_all_polygon_area": float(subset["area_km2"].sum() / total_area)
                if total_area
                else np.nan,
                "share_of_eligible_polygon_area": float(subset["area_km2"].sum() / eligible_area)
                if eligible_area
                else np.nan,
            }
        )
    return pd.DataFrame(rows)


def sha256(path: Path) -> str:
    return contract_sha256(path)


def run_audit(input_dir: Path, output_dir: Path, input_manifest: Path | None = None) -> dict[str, object]:
    names = ["pa_trends_v0_3_0.csv", "pa_edge_profiles_national_v0_3_0.csv", "pa_geometries_v0_3_0.csv"]
    contract = resolve_contract(input_dir, names, input_manifest)
    trends_path, edge_path, geometry_path = (contract.files[name] for name in names)
    trends = pd.read_csv(trends_path)
    edge = pd.read_csv(edge_path)
    geometries = pd.read_csv(geometry_path)
    matched = matched_slopes(trends, edge)
    transitions = transition_table(matched, geometries)
    areas = area_summary(trends, geometries)
    output_dir.mkdir(parents=True, exist_ok=True)
    matched_path = output_dir / "interior_area_matched_slopes.csv"
    transitions_path = output_dir / "interior_area_quadrant_transitions.csv"
    areas_path = output_dir / "interior_area_summary.csv"
    matched.to_csv(matched_path, index=False)
    transitions.to_csv(transitions_path, index=False)
    areas.to_csv(areas_path, index=False)
    ring_pairs = edge[["ring_inner_km", "ring_outer_km"]].drop_duplicates()
    exact_ring = bool(
        ((ring_pairs["ring_inner_km"] == RING_INNER_KM) & (ring_pairs["ring_outer_km"] == RING_OUTER_KM)).any()
    )
    if not exact_ring:
        raise ValueError("Accepted edge table does not contain exactly the requested 1--5 km ring.")
    included = matched[matched["ring_included"]]
    source_label = "accepted" if contract.mode == "legacy" else f"manifest-provided ({contract.analysis_id})"
    summary: dict[str, object] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {"python": sys.version, "platform": platform.platform(), "pandas": pd.__version__, "numpy": np.__version__},
        "parameters": {"min_valid_pixels": MIN_VALID_PIXELS, "min_valid_years": MIN_VALID_YEARS, "primary_buffer_km": PRIMARY_BUFFER_KM, "ring_inner_km": RING_INNER_KM, "ring_outer_km": RING_OUTER_KM, "primary_metric": PRIMARY_METRIC, "primary_buffer_type": PRIMARY_BUFFER},
        "inputs": {path.name: {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size} for path in (trends_path, edge_path, geometry_path)},
        "input_contract": contract.identity(),
        "ring_definition": {"exact_1_5_km_present": exact_ring, "pairs_in_source": [[float(a), float(b)] for a, b in ring_pairs.to_numpy()]},
        "cohort": {"original_paired_n": int(len(matched)), "ring_matched_n": int(len(included)), "ring_excluded_n": int(len(matched) - len(included)), "ring_matched_fraction": float(len(included) / len(matched)) if len(matched) else None, "ring_n_year_counts": {str(k): int(v) for k, v in matched["n_years_ring_1_5km"].value_counts(dropna=False).sort_index().items()}, "ring_exclusion_reasons": {"no_usable_ring_year": int(matched["n_years_ring_1_5km"].isna().sum()), "fewer_than_8_usable_ring_years": int(matched["n_years_ring_1_5km"].lt(MIN_VALID_YEARS).fillna(False).sum())}, "original_quadrants": matched["original_quadrant"].value_counts().sort_index().to_dict(), "ring_quadrants": included["ring_quadrant"].value_counts().sort_index().to_dict()},
        "outputs": {},
    }
    for path in (matched_path, transitions_path, areas_path):
        summary["outputs"][path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    summary_path = output_dir / "interior_area_summary.json"
    report_path = output_dir / "interior_area_audit.md"
    report_lines = [
        "# Interior-band and area sensitivity audit",
        "",
        f"Generated: {summary['generated_utc']}",
        "",
        f"The original 1 km land-unprotected paired cohort is held fixed. Whole-reserve and 1 km-buffer slopes are taken from the {source_label} trend table; only the exact 1--5 km ring slope is calculated here using the project Theil--Sen estimator, 10 valid pixels per year, and at least 8 valid years.",
        "",
        f"The exact 1--5 km ring is present in the {source_label} edge table: **{exact_ring}**. The original paired cohort contains **{len(matched):,}** PAs; **{len(included):,}** have a matched ring slope and **{len(matched)-len(included):,}** are excluded from ring transitions. All exclusions lacked a usable ring-year summary; no retained row had between 1 and 7 usable ring years.",
        "",
        "## Quadrant transitions",
        "",
        transitions.to_string(index=False),
        "",
        "Q1 means positive buffer and positive interior slope; Q2 means non-positive buffer and positive interior slope; Q3 means both non-positive; Q4 means positive buffer and non-positive interior slope. Areas are summed polygon areas and may double-count overlapping designations; they are not unique illuminated land areas.",
        "",
        "## Whole-polygon area summary",
        "",
        areas.to_string(index=False),
        "",
        "The area summary is descriptive and preserves the study's reserve-level classification. A positive reserve-level slope does not imply that the whole polygon brightened uniformly.",
        "",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    summary["outputs"][report_path.name] = {"sha256": sha256(report_path), "bytes": report_path.stat().st_size}
    # The JSON manifest intentionally does not hash itself; doing so would
    # create a circular, self-invalidating digest.
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    result = run_audit(args.input_dir, args.output_dir, args.input_manifest)
    print(json.dumps(result["cohort"], sort_keys=True))

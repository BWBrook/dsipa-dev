"""Exploratory follow-up to the 1--5 km interior-band audit.

This script is deliberately separate from the accepted interior-area audit.
It uses the accepted national summary tables read-only to extend the same
1,205-reserve 1--5 km matched cohort with the 0--1 km edge-ring summary,
annual zero/nonzero status, and descriptive area stratification.  It does not
re-extract rasters or treat Sen slopes as additive across rings.
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
RING_0_1 = (0.0, 1.0)
RING_1_5 = (1.0, 5.0)


def theil_sen(years: np.ndarray, values: np.ndarray) -> float:
    """Return the project median pairwise slope, or NaN if undefined."""
    if len(values) < 2:
        return float("nan")
    slopes = [
        (values[j] - values[i]) / (years[j] - years[i])
        for i in range(len(values) - 1)
        for j in range(i + 1, len(values))
        if years[j] != years[i]
    ]
    return float(np.median(slopes)) if slopes else float("nan")


def ring_annual(edge: pd.DataFrame, inner: float, outer: float) -> pd.DataFrame:
    """Return supported annual ring means and status flags for one ring."""
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
        edge["ring_inner_km"].eq(inner)
        & edge["ring_outer_km"].eq(outer)
    ]
    selected = ring_rows[ring_rows["valid_pixel_count"].ge(MIN_VALID_PIXELS)].dropna(subset=["mean"])
    if selected.duplicated(["pa_id", "year"]).any():
        raise ValueError(f"Duplicate supported PA-year rows in {inner:g}--{outer:g} km ring")
    if not ring_rows["year"].isin(range(2013, 2025)).all():
        raise ValueError("Edge table contains years outside 2013--2024")
    if selected.empty:
        return pd.DataFrame(
            columns=[
                "pa_id",
                "year",
                "mean",
                "n_years_ring",
                "annual_zero",
                "annual_nonzero",
                "annual_positive",
                "all_annual_zero",
                "any_annual_nonzero",
                "any_annual_positive",
            ]
        )
    selected = selected[["pa_id", "year", "mean"]].copy()
    counts = selected.groupby("pa_id")["year"].transform("size")
    selected["n_years_ring"] = counts.astype(int)
    selected["annual_zero"] = selected["mean"].eq(0)
    selected["annual_nonzero"] = selected["mean"].ne(0)
    selected["annual_positive"] = selected["mean"].gt(0)
    selected["all_annual_zero"] = selected.groupby("pa_id")["annual_zero"].transform("all")
    selected["any_annual_nonzero"] = selected.groupby("pa_id")["annual_nonzero"].transform("any")
    selected["any_annual_positive"] = selected.groupby("pa_id")["annual_positive"].transform("any")
    return selected.sort_values(["pa_id", "year"]).reset_index(drop=True)


def ring_slopes(annual: pd.DataFrame, label: str) -> pd.DataFrame:
    """Calculate ring slopes and retain annual status for each PA."""
    if annual.empty:
        return pd.DataFrame(columns=["pa_id", f"n_years_{label}", f"slope_{label}"])
    rows: list[dict[str, object]] = []
    for pa_id, group in annual.groupby("pa_id", sort=True):
        group = group.sort_values("year")
        years = group["year"].to_numpy(dtype=float)
        values = group["mean"].to_numpy(dtype=float)
        rows.append(
            {
                "pa_id": pa_id,
                f"n_years_{label}": int(len(group)),
                f"slope_{label}": (
                    theil_sen(years, values) if len(group) >= MIN_VALID_YEARS else np.nan
                ),
                f"all_annual_zero_{label}": bool(group["annual_zero"].all()),
                f"any_annual_nonzero_{label}": bool(group["annual_nonzero"].any()),
                f"any_annual_positive_{label}": bool(group["annual_positive"].any()),
            }
        )
    return pd.DataFrame(rows)


def primary_paired(trends: pd.DataFrame) -> pd.DataFrame:
    """Reconstruct the original 1 km paired cohort from accepted trends."""
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
    paired = trends[
        trends["metric"].eq(PRIMARY_METRIC)
        & trends["buffer_type"].eq(PRIMARY_BUFFER)
        & trends["n_years_inside"].ge(MIN_VALID_YEARS)
        & trends["slope_inside"].notna()
        & trends["slope_buffer_1km"].notna()
    ][["pa_id", "n_years_inside", "slope_inside", "slope_buffer_1km"]].copy()
    if paired.pa_id.duplicated().any():
        raise ValueError("Primary trend table contains duplicate pa_id values")
    return paired


def sign(value: float) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "zero"


def matched_cohort(trends: pd.DataFrame, edge: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build the same 1--5 km matched cohort and extend it with 0--1 km."""
    paired = primary_paired(trends)
    if paired.pa_id.duplicated().any():
        raise ValueError("Primary trend table contains duplicate pa_id values")
    band_1_5 = ring_annual(edge, *RING_1_5)
    band_0_1 = ring_annual(edge, *RING_0_1)
    slopes_1_5 = ring_slopes(band_1_5, "ring_1_5km")
    slopes_0_1 = ring_slopes(band_0_1, "ring_0_1km")
    matched = paired.merge(slopes_1_5, on="pa_id", how="inner", validate="one_to_one")
    matched = matched[matched["slope_ring_1_5km"].notna()].copy()
    matched = matched.merge(slopes_0_1, on="pa_id", how="left", validate="one_to_one")
    for column, source in {
        "whole_slope": "slope_inside",
        "buffer_1km_slope": "slope_buffer_1km",
    }.items():
        matched[column] = matched[source]
    matched["whole_sign"] = matched["whole_slope"].map(sign)
    matched["ring_0_1km_sign"] = matched["slope_ring_0_1km"].map(
        lambda value: sign(value) if pd.notna(value) else "unavailable"
    )
    matched["ring_1_5km_sign"] = matched["slope_ring_1_5km"].map(sign)
    return matched, band_1_5


# Existing focused tests and downstream table tooling import this historical
# helper name.  The implementation is now cohort-size agnostic.
matched_1205 = matched_cohort


def area_terciles(trends: pd.DataFrame, geometries: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    """Summarise all positive whole-reserve slopes by value-based tercile."""
    geom = geometries[["pa_id", "area_km2"]].drop_duplicates("pa_id")
    positive = trends[
        trends["metric"].eq(PRIMARY_METRIC)
        & trends["buffer_type"].eq(PRIMARY_BUFFER)
        & trends["n_years_inside"].ge(MIN_VALID_YEARS)
        & trends["slope_inside"].gt(0)
    ][["pa_id", "slope_inside"]].drop_duplicates("pa_id")
    positive = positive.merge(geom, on="pa_id", how="left", validate="one_to_one")
    q1, q2 = (float(positive["slope_inside"].quantile(q)) for q in (1 / 3, 2 / 3))
    # Values equal to a boundary remain in the lower group. This preserves
    # equal values together and means group counts need not be exactly equal.
    positive["whole_slope_tercile"] = np.select(
        [positive["slope_inside"].le(q1), positive["slope_inside"].le(q2)],
        ["T1_low", "T2_middle"],
        default="T3_high",
    )
    total_area = float(positive["area_km2"].sum())
    summary = (
        positive.groupby("whole_slope_tercile", as_index=False)
        .agg(
            n=("pa_id", "size"),
            area_km2=("area_km2", "sum"),
            slope_min=("slope_inside", "min"),
            slope_median=("slope_inside", "median"),
            slope_max=("slope_inside", "max"),
        )
    )
    summary["area_share_positive_whole"] = summary["area_km2"] / total_area
    details = {
        "n_positive": int(len(positive)),
        "total_positive_area_km2": total_area,
        "q1_boundary": q1,
        "q2_boundary": q2,
        "ties_at_q1": int(positive["slope_inside"].eq(q1).sum()),
        "ties_at_q2": int(positive["slope_inside"].eq(q2).sum()),
        "tie_rule": "Values equal to a quantile boundary are assigned to the lower tercile.",
    }
    return summary, {"details": details, "classified": positive}


def annual_status_summary(annual: pd.DataFrame, label: str) -> pd.DataFrame:
    """Aggregate annual zero/nonzero statuses without equating zero slope to all-zero."""
    if annual.empty:
        return pd.DataFrame()
    by_pa = annual.groupby("pa_id").agg(
        n_years=("year", "size"),
        all_annual_zero=("annual_zero", "all"),
        any_annual_nonzero=("annual_nonzero", "any"),
        any_annual_positive=("annual_positive", "any"),
    )
    by_pa["status"] = np.select(
        [by_pa["all_annual_zero"], by_pa["any_annual_positive"]],
        ["all_annual_zero", "has_positive_year"],
        default="nonzero_without_positive",
    )
    out = (
        by_pa.reset_index()
        .groupby("status", as_index=False)
        .agg(n=("pa_id", "size"), median_n_years=("n_years", "median"))
    )
    out.insert(0, "ring", label)
    return out


def sha256(path: Path) -> str:
    return contract_sha256(path)


def run(input_dir: Path, output_dir: Path, input_manifest: Path | None = None) -> dict[str, object]:
    names = ["pa_trends_v0_3_0.csv", "pa_edge_profiles_national_v0_3_0.csv", "pa_geometries_v0_3_0.csv"]
    contract = resolve_contract(input_dir, names, input_manifest)
    paths = dict(zip(("trends", "edge", "geometries"), (contract.files[name] for name in names)))
    trends = pd.read_csv(paths["trends"])
    edge = pd.read_csv(paths["edge"])
    geometries = pd.read_csv(paths["geometries"])
    if geometries["pa_id"].duplicated().any():
        raise ValueError("Geometry table contains duplicate PA identifiers")
    matched, annual_1_5 = matched_cohort(trends, edge)
    annual_0_1 = ring_annual(edge, *RING_0_1)
    if contract.mode == "legacy" and len(matched) != 1205:
        raise ValueError(f"Expected the accepted 1,205-reserve cohort, got {len(matched)}")
    cohort_ids = set(matched["pa_id"])
    annual_1_5 = annual_1_5[annual_1_5["pa_id"].isin(cohort_ids)].copy()
    annual_0_1 = annual_0_1[annual_0_1["pa_id"].isin(cohort_ids)].copy()
    matched_path = output_dir / "edge_followup_band_slopes.csv"
    annual_path = output_dir / "edge_followup_annual_status.csv"
    tercile_path = output_dir / "edge_followup_positive_terciles.csv"
    geometry_check_path = output_dir / "edge_followup_geometry_check.csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    matched.to_csv(matched_path, index=False)
    annual_status = pd.concat(
        [annual_status_summary(annual_0_1, "0--1 km"), annual_status_summary(annual_1_5, "1--5 km")],
        ignore_index=True,
    )
    annual_status.to_csv(annual_path, index=False)
    terciles, tercile_meta = area_terciles(trends, geometries)
    terciles.to_csv(tercile_path, index=False)
    geom = geometries[["pa_id", "area_km2"]].drop_duplicates("pa_id")
    geometry_check = geometries.nlargest(15, "area_km2")[
        [column for column in ["pa_id", "NAME", "STATE", "area_km2"] if column in geometries.columns]
    ].copy()
    geometry_check.insert(0, "area_rank", range(1, len(geometry_check) + 1))
    geometry_check.to_csv(geometry_check_path, index=False)
    eligible_trends = trends[
        trends["metric"].eq(PRIMARY_METRIC)
        & trends["buffer_type"].eq(PRIMARY_BUFFER)
        & trends["n_years_inside"].ge(MIN_VALID_YEARS)
        & trends["slope_inside"].notna()
    ][["pa_id"]].drop_duplicates("pa_id")
    eligible_area = float(eligible_trends.merge(geom, on="pa_id", how="left")["area_km2"].sum())
    matched_area = matched.merge(geom, on="pa_id", how="left", validate="one_to_one")
    positive_band = matched_area[matched_area["whole_slope"].gt(0)]
    # Q1 is defined by positive surrounding (the unchanged 1 km slope) and
    # positive whole-reserve slope. Keep its loss separate from Q2 losses.
    q1_lost = matched_area[(matched_area["buffer_1km_slope"] > 0) & (matched_area["whole_sign"] == "positive") & (matched_area["ring_1_5km_sign"] != "positive")]
    q1_kept = matched_area[(matched_area["buffer_1km_slope"] > 0) & (matched_area["whole_sign"] == "positive") & (matched_area["ring_1_5km_sign"] == "positive")]
    q2_lost = matched_area[(matched_area["buffer_1km_slope"] <= 0) & (matched_area["whole_sign"] == "positive") & (matched_area["ring_1_5km_sign"] != "positive")]
    positive_edge_zero_band = positive_band[
        (positive_band["ring_0_1km_sign"] == "positive")
        & (positive_band["ring_1_5km_sign"] == "zero")
    ]
    positive_total_area = float(tercile_meta["details"]["total_positive_area_km2"])
    report = output_dir / "edge_followup_report.md"
    report.write_text(
        "\n".join(
            [
                "# Exploratory edge-band follow-up",
                "",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                "",
                f"This is an exploratory follow-up to the accepted 1--5 km sensitivity audit. It reconstructs a matched cohort of {len(matched):,} reserves, adds the exact 0--1 km ring, and reports annual zero/nonzero status. All ring summaries use the project thresholds of 10 valid pixels per year and 8 valid years. Sen slopes are reported separately by spatial support and are not treated as additive.",
                "",
                f"The matched cohort contains {len(matched):,} reserves. The 0--1 km ring is available for {matched['slope_ring_0_1km'].notna().sum():,} of them. Of the original Q1 reserves, {len(q1_lost):,} lose a positive sign in the 1--5 km band and {len(q1_kept):,} retain it. All {int(q1_lost['slope_ring_1_5km'].eq(0).sum())} Q1 losses have exactly zero band slope, but only {int(q1_lost['all_annual_zero_ring_1_5km'].sum())} are all-zero annual histories; the remainder have nonzero annual histories whose median pairwise slope is zero. The Q1 losses have summed polygon area {q1_lost['area_km2'].sum():,.3f} km2, or {q1_lost['area_km2'].sum() / positive_total_area:.2%} of all positive whole-reserve polygon area and {q1_lost['area_km2'].sum() / eligible_area:.2%} of eligible-reserve polygon area. Their median band slope is {q1_lost['slope_ring_1_5km'].median():.6g}, median whole slope is {q1_lost['whole_slope'].median():.6g}, and median polygon area is {q1_lost['area_km2'].median():.3f} km2; corresponding Q1-kept medians are {q1_kept['slope_ring_1_5km'].median():.6g}, {q1_kept['whole_slope'].median():.6g}, and {q1_kept['area_km2'].median():.3f} km2. This is a spatial-support comparison, not proof that change is boundary-localised.",
                "",
                "## Whole, 0--1 km, and 1--5 km signs",
                "",
                matched[["whole_sign", "ring_0_1km_sign", "ring_1_5km_sign"]].value_counts(dropna=False).rename("n").reset_index().to_string(index=False),
                "",
                "## Annual zero/nonzero status",
                "",
                annual_status.to_string(index=False),
                "",
                "A zero Sen slope is not equivalent to an all-zero annual series. The annual status table separates all-zero histories from histories containing at least one positive year.",
                "",
                f"Among the {len(positive_edge_zero_band)} whole-positive reserves with a positive 0--1 km sign and zero 1--5 km sign, {int(positive_edge_zero_band['all_annual_zero_ring_1_5km'].sum())} are all-zero annual 1--5 km histories and {int(positive_edge_zero_band['any_annual_nonzero_ring_1_5km'].sum())} contain nonzero annual values.",
                "",
                "## Positive whole-reserve area by slope tercile",
                "",
                terciles.to_string(index=False),
                "",
                f"Tercile cutpoints are {tercile_meta['details']['q1_boundary']:.9g} and {tercile_meta['details']['q2_boundary']:.9g} product-scaled units per year. {tercile_meta['details']['tie_rule']} Ties at the boundaries: {tercile_meta['details']['ties_at_q1']} and {tercile_meta['details']['ties_at_q2']}.",
                "",
                "Area is summed protected-area polygon area and can double-count overlapping designations; it is not unique illuminated land area. Missing 5--10 km summaries indicate unavailable valid raster summaries under the threshold, not geometric absence of the ring. The annual summaries are descriptive and do not establish whether zero/nonzero patterns reflect product processing or environmental change.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    summary: dict[str, object] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "exploratory": True,
        "script": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__))},
        "software": {"python": sys.version, "platform": platform.platform(), "pandas": pd.__version__, "numpy": np.__version__},
        "parameters": {"min_valid_pixels": MIN_VALID_PIXELS, "min_valid_years": MIN_VALID_YEARS, "ring_0_1_km": RING_0_1, "ring_1_5_km": RING_1_5, "primary_buffer_type": PRIMARY_BUFFER},
        "inputs": {path.name: {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size} for path in paths.values()},
        "input_contract": contract.identity(),
        "cohort": {"same_1_5_km_matched_n": int(len(matched)), "ring_0_1_slope_available_n": int(matched["slope_ring_0_1km"].notna().sum()), "positive_whole_matched_n": int(len(positive_band)), "positive_0_1_positive_1_5_zero_n": int(len(positive_edge_zero_band)), "positive_0_1_positive_1_5_zero_all_zero_n": int(positive_edge_zero_band["all_annual_zero_ring_1_5km"].sum()), "positive_0_1_positive_1_5_zero_nonzero_history_n": int(positive_edge_zero_band["any_annual_nonzero_ring_1_5km"].sum()), "q1_lost_n": int(len(q1_lost)), "q1_kept_n": int(len(q1_kept)), "q1_lost_ring_zero_slope_n": int(q1_lost["slope_ring_1_5km"].eq(0).sum()), "q1_lost_all_zero_1_5_n": int(q1_lost["all_annual_zero_ring_1_5km"].sum()), "q1_lost_area_km2": float(q1_lost["area_km2"].sum()), "q1_lost_share_all_positive_area": float(q1_lost["area_km2"].sum() / positive_total_area), "q1_lost_share_eligible_area": float(q1_lost["area_km2"].sum() / eligible_area), "q1_lost_median_ring_slope": float(q1_lost["slope_ring_1_5km"].median()), "q1_lost_median_whole_slope": float(q1_lost["whole_slope"].median()), "q1_lost_median_area_km2": float(q1_lost["area_km2"].median()), "q1_kept_median_ring_slope": float(q1_kept["slope_ring_1_5km"].median()), "q1_kept_median_whole_slope": float(q1_kept["whole_slope"].median()), "q1_kept_median_area_km2": float(q1_kept["area_km2"].median()), "q2_lost_n": int(len(q2_lost)), "q2_lost_ring_zero_slope_n": int(q2_lost["slope_ring_1_5km"].eq(0).sum()), "q2_lost_all_zero_1_5_n": int(q2_lost["all_annual_zero_ring_1_5km"].sum())},
        "geometry_check": {"n_rows": int(len(geometries)), "n_unique_pa_id": int(geometries["pa_id"].nunique()), "duplicate_pa_id_n": int(geometries["pa_id"].duplicated().sum()), "all_polygon_area_km2": float(geom["area_km2"].sum()), "eligible_polygon_area_km2": eligible_area, "positive_polygon_area_km2": positive_total_area, "largest_rows_output": geometry_check_path.name},
        "terciles": tercile_meta["details"],
        "outputs": {},
    }
    for path in (matched_path, annual_path, tercile_path, geometry_check_path, report):
        summary["outputs"][path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    manifest = output_dir / "edge_followup_summary.json"
    manifest.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.input_dir, args.output_dir, args.input_manifest)["cohort"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Independently replay the 18 October 2026 descriptive brightening budget.

Run from the project environment, without network access:
    .venv/bin/python analysis/reports/brightening_budget_audit_20261018.py

This script reads the corrected annual summaries and geometries directly. It
does not import the budget implementation or read its derived outputs. Only
the requested JSON receipt is written. The source summaries are modest local
files; no raster extraction, model fitting, or remote computation is performed.

Scope: approximate area-integrated product signal over each year's valid
pixels. Overlapping designations remain counted in each reserve. A positive
band contribution is the positive part of that band's fitted OLS slope, not a
positive pixel change, annual increment, physical emitted light, or ecological
exposure. Stable counts do not prove stable valid-pixel identities.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import geopandas as gpd
import numpy as np
import pandas as pd


YEARS = np.arange(2013, 2025)
SPHERICAL_RADIUS_KM = 6371.0088
CELL_DEGREES = 1 / 240
EQUATOR_CELL_KM2 = (SPHERICAL_RADIUS_KM * np.pi / 180 * CELL_DEGREES) ** 2
NUMERICAL_ZERO = 1e-9
PERIODS = ("full_2013_2024", "pre_2013_2021", "late_minus_early")


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def pivot(frame: pd.DataFrame, column: str, ids: pd.Index) -> pd.DataFrame:
    """Retain a common explicit order of identifiers and calendar years."""
    return frame.pivot(index="pa_id", columns="year", values=column).loc[ids, YEARS]


def measure(annual: pd.DataFrame, period: str) -> pd.Series:
    """Compute OLS directly, or a difference between two three-year means.

    Subtracting the first annual value before the OLS dot product makes an
    exactly constant series exactly zero and avoids large-intercept rounding.
    Values below 1e-9 are numerical zeros, not an ecological-effect threshold.
    """
    values = annual.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Annual summaries must be complete and finite")
    if period == "late_minus_early":
        result = values[:, -3:].mean(axis=1) - values[:, :3].mean(axis=1)
    else:
        years = YEARS if period == "full_2013_2024" else YEARS[:9]
        values = values[:, :len(years)]
        time = years - years.mean()
        result = (values - values[:, [0]]) @ time / (time @ time)
    result[np.abs(result) < NUMERICAL_ZERO] = 0.0
    return pd.Series(result, index=annual.index)


def budget_for_period(
    whole: pd.DataFrame, outer: pd.DataFrame, remainder: pd.DataFrame, period: str
) -> tuple[dict, pd.Series]:
    w, o, r = (measure(frame, period) for frame in (whole, outer, remainder))
    reserve_positive = w.clip(lower=0).sum()
    outer_positive = o.clip(lower=0).sum()
    remainder_positive = r.clip(lower=0).sum()
    band_positive = outer_positive + remainder_positive
    return {
        "reserve_net": float(w.sum()),
        "reserve_gross_positive": float(reserve_positive),
        "reserve_gross_negative": float(w.clip(upper=0).sum()),
        "outer_net": float(o.sum()),
        "remainder_net": float(r.sum()),
        "outer_gross_positive": float(outer_positive),
        "remainder_gross_positive": float(remainder_positive),
        "band_gross_positive": float(band_positive),
        "band_gross_negative": float(o.clip(upper=0).sum() + r.clip(upper=0).sum()),
        "band_minus_reserve_gross": float(band_positive - reserve_positive),
        "outer_share_band_gross": float(outer_positive / band_positive),
        "max_per_reserve_additivity_error": float((w - o - r).abs().max()),
        "reserve_positive_n": int((w > 0).sum()),
        "reserve_negative_n": int((w < 0).sum()),
    }, r


def latitude_slope_bounds(
    pixel_totals: pd.DataFrame, low_area: pd.Series, high_area: pd.Series
) -> tuple[float, float]:
    """Bound positive OLS contributions without assuming uniform light.

    Every annual nonnegative pixel sum is multiplied by an area between the
    minimum and maximum spherical cell areas over its reserve's latitude
    extent. Positive and negative OLS time coefficients must be bounded in
    opposite directions. Simply rescaling an already fitted slope would not
    bound error when annual contributions cancel. These conservative bounds
    allow annual light to occur anywhere within that latitude extent; they do
    not require access to individual pixel histories. The tiny negative
    whole-minus-outer residuals from subtraction rounding are clipped to zero.

    This bounds latitude variation in the adopted spherical approximation;
    it does not bound ellipsoidal or raster-boundary discretisation error.
    """
    time = YEARS - YEARS.mean()
    weights = time / (time @ time)
    values = pixel_totals.clip(lower=0).to_numpy()
    positive_terms = values @ np.maximum(weights, 0)
    negative_terms = values @ np.minimum(weights, 0)
    lower = positive_terms * low_area.to_numpy() + negative_terms * high_area.to_numpy()
    upper = positive_terms * high_area.to_numpy() + negative_terms * low_area.to_numpy()
    return float(np.maximum(lower, 0).sum()), float(np.maximum(upper, 0).sum())


def replay(root: Path) -> dict:
    paths = {
        "trends": root / "data/processed/pa_trends_v0_3_0.csv",
        "annual_inside": root / "data/processed/pa_radiance_buffers_national_v0_3_0.csv",
        "annual_bands": root / "data/processed/pa_edge_profiles_national_v0_3_0.csv",
        "geometries": root / "data/processed/pa_geometries_v0_3_0.gpkg",
    }
    manifest_path = root / "analysis/reports/spatial_correction_render_input_manifest.json"
    accepted = json.loads(manifest_path.read_text())["files"]
    identities = {}
    for role, path in paths.items():
        digest = sha256(path)
        expected = accepted[path.name]["sha256"]
        if digest != expected:
            raise ValueError(f"Corrected-input identity mismatch: {path}")
        identities[role] = {
            "path": str(path), "sha256": digest, "bytes": path.stat().st_size,
            "matches_corrected_manifest": True,
        }

    trends = pd.read_csv(paths["trends"])
    trends = trends[
        trends.metric.eq("mean") & trends.buffer_type.eq("land_unprotected")
    ].set_index("pa_id")
    if trends.index.has_duplicates:
        raise ValueError("Duplicate primary trend identifiers")
    ids = trends.index[trends.slope_inside.notna()].sort_values()
    if not trends.loc[ids, "n_years_inside"].ge(8).all():
        raise ValueError("Selected trends violate the original temporal eligibility rule")

    geometry = gpd.read_file(paths["geometries"], columns=["pa_id", "area_km2"])
    geometry = geometry.set_index("pa_id").loc[ids]
    if geometry.index.has_duplicates or geometry.crs.to_epsg() != 3577:
        raise ValueError("Unexpected geometry identifiers or coordinate reference system")
    latitude = geometry.geometry.centroid.to_crs(4326).y
    cell_area = EQUATOR_CELL_KM2 * np.cos(np.radians(latitude))

    annual = pd.read_csv(paths["annual_inside"], usecols=[
        "pa_id", "zone", "year", "valid_pixel_count", "mean",
    ])
    annual = annual[annual.zone.eq("inside")]
    bands = pd.read_csv(paths["annual_bands"], usecols=[
        "pa_id", "ring_index", "ring_inner_km", "ring_outer_km", "year",
        "valid_pixel_count", "mean",
    ])
    bands = bands[bands.ring_index.eq(0)]
    if not (bands.ring_inner_km.eq(0) & bands.ring_outer_km.eq(1)).all():
        raise ValueError("Ring zero is not consistently the 0-1 km interior band")
    count, outer_count = (pivot(frame, "valid_pixel_count", ids) for frame in (annual, bands))
    mean, outer_mean = (pivot(frame, "mean", ids) for frame in (annual, bands))
    if not (count.ge(10).all().all() and outer_count.ge(10).all().all()):
        raise ValueError("Whole or outer annual support is below ten valid pixels")
    pixel_total, outer_pixels = mean * count, outer_mean * outer_count
    remainder_pixels = pixel_total - outer_pixels
    remainder_count = count - outer_count
    if remainder_count.lt(0).any().any() or remainder_pixels.min().min() < -1e-8:
        raise ValueError("Substantial negative whole-minus-outer remainder")
    whole = pixel_total.mul(cell_area, axis=0)
    outer = outer_pixels.mul(cell_area, axis=0)
    remainder = remainder_pixels.mul(cell_area, axis=0)

    results = {
        "audit_id": "brightening-budget-independent-replay-20261018",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__))},
        "software": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "geopandas": gpd.__version__},
        "inputs": identities,
        "corrected_input_manifest": {"path": str(manifest_path), "sha256": sha256(manifest_path)},
        "scope": {
            "signal": "Approximate area-integrated product signal over annual valid pixel support",
            "overlap": "Each protected-area designation counted separately; overlapping pixels can repeat",
            "gross_positive": "Positive part of each fitted reserve or band contribution, as labelled",
            "ols_units": "product units x km2 per year",
            "period_difference_units": "product units x km2",
            "period_difference": "mean(2022-2024) minus mean(2013-2015)",
            "area_reference_year": 2024,
            "remainder": "Whole reserve minus its 0-1 km band; includes all support beyond 1 km",
            "count_stability": "Equal annual counts do not prove identical valid-pixel identities",
            "causality": "No attribution to light sources, product changes, or ecological exposure",
            "numerical_zero_tolerance": NUMERICAL_ZERO,
        },
    }
    for period in PERIODS:
        results[period], remainder_slopes = budget_for_period(whole, outer, remainder, period)
        if period == "full_2013_2024":
            ordered = remainder_slopes.clip(lower=0).sort_values(ascending=False)
            cumulative = ordered.cumsum() / ordered.sum()
            results[period]["beyond_1km_top10"] = [
                {"pa_id": name, "positive_contribution": float(value),
                 "share": float(value / ordered.sum())}
                for name, value in ordered.head(10).items()
            ]
            results[period]["beyond_1km_reserves_for_50_80_percent"] = [
                int((cumulative < threshold).sum() + 1) for threshold in (0.5, 0.8)
            ]

    whole_area = (count[2024] * cell_area).sum()
    outer_area = (outer_count[2024] * cell_area).sum()
    results["sampled_area"] = {
        "whole_2024_km2": float(whole_area), "outer_2024_km2": float(outer_area),
        "outer_share": float(outer_area / whole_area),
        "eligible_summed_polygon_area_km2": float(geometry.area_km2.sum()),
        "note": "Raster-cell area and polygon area are distinct denominators",
    }
    interior = remainder_count.min(axis=1).ge(10)
    stable = count.nunique(axis=1).eq(1) & outer_count.nunique(axis=1).eq(1)
    results["support"] = {
        "eligible_n": len(ids), "complete_12_year_inside_n": int(mean.notna().all(axis=1).sum()),
        "complete_12_year_outer_n": int(outer_mean.notna().all(axis=1).sum()),
        "interior_definition": "At least ten valid remainder pixels in every year, 2013-2024",
        "interior_n": int(interior.sum()), "interior_stable_n": int((interior & stable).sum()),
        "stable_all_n": int(stable.sum()), "unstable_ids": list(ids[~stable]),
        "minimum_annual_remainder_total": float(remainder.min().min()),
    }
    for label, mask in (("all_stable", stable), ("interior", interior),
                        ("interior_stable", interior & stable)):
        section, _ = budget_for_period(whole.loc[mask], outer.loc[mask], remainder.loc[mask], PERIODS[0])
        w, o = (measure(frame.loc[mask], PERIODS[0]) for frame in (whole, outer))
        section.update({"n": int(mask.sum()), "outer_signed_share_in_whole_positive":
                        float(o[w > 0].sum() / w[w > 0].sum())})
        results[label] = section

    results["unweighted_cells"] = {}
    for period in PERIODS:
        section, rest = budget_for_period(pixel_total, outer_pixels, remainder_pixels, period)
        section["kosciuszko_beyond_share"] = float(rest["NSW_N0018"] / rest.clip(lower=0).sum())
        results["unweighted_cells"][period] = section
    results["unweighted_cells"]["area_share_by_cell_count"] = float(outer_count[2024].sum() / count[2024].sum())
    results["unweighted_cells"]["units"] = "product units x pixel count; no geographic-area weighting"

    bounds = geometry.to_crs(4326).bounds
    # All these Australian reserve extents lie south of the equator.
    if not bounds.maxy.lt(0).all():
        raise ValueError("Latitude-bound calculation assumes southern-hemisphere extents")
    maximum_absolute_latitude = bounds[["miny", "maxy"]].abs().max(axis=1)
    minimum_absolute_latitude = bounds[["miny", "maxy"]].abs().min(axis=1)
    low_area = EQUATOR_CELL_KM2 * np.cos(np.radians(maximum_absolute_latitude))
    high_area = EQUATOR_CELL_KM2 * np.cos(np.radians(minimum_absolute_latitude))
    relative_bound = np.maximum(abs(low_area / cell_area - 1), abs(high_area / cell_area - 1))
    outer_low, outer_high = latitude_slope_bounds(outer_pixels, low_area, high_area)
    rest_low, rest_high = latitude_slope_bounds(remainder_pixels, low_area, high_area)
    results["latitude_extent_bounds"] = {
        "spherical_radius_km": SPHERICAL_RADIUS_KM, "cell_degrees": CELL_DEGREES,
        "method": "Bound annual nonnegative cell sums by reserve latitude extrema; reverse area bounds for negative OLS coefficients before clipping each slope at zero",
        "limitations": "Conservative latitude-only bounds within the adopted spherical approximation, not bounds for ellipsoidal or raster-boundary error",
        "max_cell_area_relative_error_bound": float(relative_bound.max()),
        "median_cell_area_relative_error_bound": float(relative_bound.median()),
        "kosciuszko_cell_area_relative_error_bound": float(relative_bound["NSW_N0018"]),
        "outer_gross_low": outer_low, "outer_gross_high": outer_high,
        "remainder_gross_low": rest_low, "remainder_gross_high": rest_high,
        "outer_share_low": outer_low / (outer_low + rest_high),
        "outer_share_high": outer_high / (outer_high + rest_low),
    }

    mean_ols, integral_ols = (measure(frame, PERIODS[0]) for frame in (mean, whole))
    integral_top20, mean_top20 = set(integral_ols.nlargest(20).index), set(mean_ols.nlargest(20).index)
    outside100 = integral_top20 - set(mean_ols.nlargest(100).index)
    results["matched_ols_ranks"] = {
        "description": "Same OLS estimator and same 2013-2024 cohort; reserve mean versus approximate area integral",
        "top20_overlap_n": len(integral_top20 & mean_top20),
        "top20_overlap_ids": sorted(integral_top20 & mean_top20),
        "integral_top20_outside_mean_top100_n": len(outside100),
        "integral_top20_outside_mean_top100_ids": sorted(outside100),
        "kosciuszko_mean_ols_rank": float(mean_ols.rank(ascending=False)["NSW_N0018"]),
        "kosciuszko_integral_ols_rank": float(integral_ols.rank(ascending=False)["NSW_N0018"]),
    }

    # Acceptance checks preserve the independently reported audit numbers.
    # Inputs are already checked against the corrected spatial manifest above.
    checks = {
        "eligible_4426": len(ids) == 4426,
        "interior_1398_stable_1395": int(interior.sum()) == 1398 and int((interior & stable).sum()) == 1395,
        "stable_4422": int(stable.sum()) == 4422,
        "band_outer_share": np.isclose(results[PERIODS[0]]["outer_share_band_gross"], 0.7200208817637812, rtol=0, atol=1e-12),
        "sampled_area_share": np.isclose(results["sampled_area"]["outer_share"], 0.1370442445106165, rtol=0, atol=1e-12),
        "pre_outer_share": np.isclose(results[PERIODS[1]]["outer_share_band_gross"], 0.8250490504069652, rtol=0, atol=1e-12),
        "period_outer_share": np.isclose(results[PERIODS[2]]["outer_share_band_gross"], 0.714651851603955, rtol=0, atol=1e-12),
        "net_full": np.isclose(results[PERIODS[0]]["reserve_net"], 478.9471876315347, rtol=0, atol=1e-8),
        "net_pre": np.isclose(results[PERIODS[1]]["reserve_net"], -537.8416855726414, rtol=0, atol=1e-8),
        "beyond_reach_2_7": results[PERIODS[0]]["beyond_1km_reserves_for_50_80_percent"] == [2, 7],
        "matched_ols_ranks": len(integral_top20 & mean_top20) == 6 and len(outside100) == 12,
        "additivity": all(results[p]["max_per_reserve_additivity_error"] < 1e-8 for p in PERIODS),
    }
    results["acceptance_checks"] = {name: bool(passed) for name, passed in checks.items()}
    if not all(checks.values()):
        raise AssertionError(f"Audit acceptance failed: {results['acceptance_checks']}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().with_suffix(".json"))
    args = parser.parse_args()
    results = replay(args.root.resolve())
    args.out.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"output": str(args.out), "all_acceptance_checks_passed": True,
                      "outer_band_positive_share": results[PERIODS[0]]["outer_share_band_gross"],
                      "outer_sampled_area_share": results["sampled_area"]["outer_share"],
                      "latitude_bound": [results["latitude_extent_bounds"]["outer_share_low"],
                                         results["latitude_extent_bounds"]["outer_share_high"]]}, indent=2))


if __name__ == "__main__":
    main()

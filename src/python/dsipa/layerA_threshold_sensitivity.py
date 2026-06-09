"""Layer A trend-threshold sensitivity summaries."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.paths import find_repo_root
from dsipa.schema import RADIANCE_BUFFERS_NATIONAL_CSV
from dsipa.trends import _theil_sen

REPORT_PATH = "analysis/reports/layerA_trend_threshold_sensitivity.md"
CSV_PATH = "analysis/reports/layerA_trend_threshold_sensitivity.csv"
PRIMARY_METRIC = "mean"
PRIMARY_BUFFER_TYPE = "land_unprotected"
PRIMARY_BUFFER_KM = 1.0
PIXEL_THRESHOLDS = (5, 10, 20, 50)
YEAR_THRESHOLDS = (6, 8, 10)


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _compute_slopes(
    df: pd.DataFrame,
    *,
    min_valid_pixels: int,
    min_valid_years: int,
    zone: str,
    buffer_km: float | None = None,
    buffer_type: str | None = None,
) -> pd.DataFrame:
    if zone == "inside":
        subset = df[df["zone"] == "inside"].copy()
    else:
        subset = df[
            (df["zone"] == "buffer")
            & (df["buffer_km"] == buffer_km)
            & (df["buffer_type"] == buffer_type)
        ].copy()

    subset = subset[subset["valid_pixel_count"] >= min_valid_pixels]
    subset = subset.dropna(subset=[PRIMARY_METRIC])
    records = []
    for pa_id, group in subset.groupby("pa_id"):
        years = group["year"].to_numpy(dtype=float)
        values = group[PRIMARY_METRIC].to_numpy(dtype=float)
        if len(values) < min_valid_years:
            continue
        slope, _ = _theil_sen(years, values)
        records.append({"pa_id": pa_id, "n_years": int(len(values)), "slope": slope})
    return pd.DataFrame.from_records(records)


def _quadrants(joined: pd.DataFrame) -> dict[str, int]:
    if joined.empty:
        return {"q1": 0, "q2": 0, "q3": 0, "q4": 0}
    x = joined["slope_buffer_1km"]
    y = joined["slope_inside"]
    return {
        "q1": int(((x > 0) & (y > 0)).sum()),
        "q2": int(((x <= 0) & (y > 0)).sum()),
        "q3": int(((x <= 0) & (y <= 0)).sum()),
        "q4": int(((x > 0) & (y <= 0)).sum()),
    }


def summarise_threshold(
    df: pd.DataFrame,
    *,
    min_valid_pixels: int,
    min_valid_years: int,
) -> dict[str, object]:
    inside = _compute_slopes(
        df,
        min_valid_pixels=min_valid_pixels,
        min_valid_years=min_valid_years,
        zone="inside",
    ).rename(columns={"slope": "slope_inside", "n_years": "n_years_inside"})
    buffer1 = _compute_slopes(
        df,
        min_valid_pixels=min_valid_pixels,
        min_valid_years=min_valid_years,
        zone="buffer",
        buffer_km=PRIMARY_BUFFER_KM,
        buffer_type=PRIMARY_BUFFER_TYPE,
    ).rename(columns={"slope": "slope_buffer_1km", "n_years": "n_years_buffer_1km"})

    joined = inside.merge(buffer1, on="pa_id", how="inner")
    q = _quadrants(joined)
    n_inside = len(inside)
    n_quadrant = len(joined)
    n_zero = int((inside["slope_inside"] == 0).sum()) if n_inside else 0
    n_positive = int((inside["slope_inside"] > 0).sum()) if n_inside else 0
    return {
        "min_valid_pixels": min_valid_pixels,
        "min_valid_years": min_valid_years,
        "inside_trend_n": n_inside,
        "inside_zero_slope_n": n_zero,
        "inside_positive_slope_n": n_positive,
        "inside_zero_slope_fraction": np.nan if n_inside == 0 else n_zero / n_inside,
        "inside_positive_slope_fraction": np.nan if n_inside == 0 else n_positive / n_inside,
        "quadrant_n": n_quadrant,
        "quadrant_fraction_of_inside": np.nan if n_inside == 0 else n_quadrant / n_inside,
        "q1_concurrent_brightening": q["q1"],
        "q2_internal_brightening": q["q2"],
        "q3_stable_non_detect": q["q3"],
        "q4_external_pressure": q["q4"],
        "q1_fraction": np.nan if n_quadrant == 0 else q["q1"] / n_quadrant,
        "q4_fraction": np.nan if n_quadrant == 0 else q["q4"] / n_quadrant,
        "median_inside_slope": inside["slope_inside"].median() if n_inside else np.nan,
        "median_buffer_slope": joined["slope_buffer_1km"].median() if n_quadrant else np.nan,
    }


def build_sensitivity(
    df: pd.DataFrame,
    *,
    pixel_thresholds: tuple[int, ...] = PIXEL_THRESHOLDS,
    year_thresholds: tuple[int, ...] = YEAR_THRESHOLDS,
) -> pd.DataFrame:
    rows = []
    for min_valid_pixels in pixel_thresholds:
        for min_valid_years in year_thresholds:
            rows.append(
                summarise_threshold(
                    df,
                    min_valid_pixels=min_valid_pixels,
                    min_valid_years=min_valid_years,
                )
            )
    return pd.DataFrame(rows)


def validate_sensitivity(summary: pd.DataFrame) -> list[str]:
    notes = []
    if summary.empty:
        raise ValueError("Threshold sensitivity summary is empty.")
    for _, row in summary.iterrows():
        if row["quadrant_n"] > row["inside_trend_n"]:
            raise ValueError("Quadrant denominator exceeds inside trend denominator.")
        q_sum = int(
            row["q1_concurrent_brightening"]
            + row["q2_internal_brightening"]
            + row["q3_stable_non_detect"]
            + row["q4_external_pressure"]
        )
        if q_sum != int(row["quadrant_n"]):
            raise ValueError("Quadrants do not sum to quadrant_n.")
        if row["inside_zero_slope_n"] + row["inside_positive_slope_n"] > row["inside_trend_n"]:
            raise ValueError("Zero + positive slope counts exceed inside trend denominator.")
    notes.append("Quadrant counts sum to each scenario denominator.")
    notes.append("Quadrant denominators are nested within inside trend denominators.")
    notes.append("Inside zero + positive slope counts do not exceed inside trend denominators.")
    return notes


def _fmt(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, (int, np.integer)):
        return f"{int(value):,}"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.3f}"
    return str(value)


def _markdown_table(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(_fmt(row[column]) for column in columns) + " |"
        for _, row in df.iterrows()
    ]
    return "\n".join([header, separator, *body])


def render_report(summary: pd.DataFrame, notes: list[str]) -> str:
    compact = summary[
        [
            "min_valid_pixels",
            "min_valid_years",
            "inside_trend_n",
            "inside_zero_slope_fraction",
            "inside_positive_slope_n",
            "inside_positive_slope_fraction",
            "quadrant_n",
            "q1_concurrent_brightening",
            "q2_internal_brightening",
            "q3_stable_non_detect",
            "q4_external_pressure",
            "q1_fraction",
            "q4_fraction",
        ]
    ].copy()
    primary = summary[
        (summary["min_valid_pixels"] == 10) & (summary["min_valid_years"] == 8)
    ]
    lines = [
        "# Layer A trend-threshold sensitivity",
        "",
        f"Generated: {_now_utc()}",
        "",
        (
            "Sensitivity grid for primary Layer A trend rules. Slopes use Theil-Sen on inside "
            "`mean` radiance and 1 km `land_unprotected` buffer `mean` radiance."
        ),
        "",
        "## Scenario summary",
        "",
        _markdown_table(compact),
        "",
    ]
    if not primary.empty:
        p = primary.iloc[0]
        lines.extend(
            [
                "## Primary rule cross-check",
                "",
                (
                    f"Primary rule (`>=10` valid pixels, `>=8` valid years): "
                    f"inside trend n={int(p['inside_trend_n']):,}, "
                    f"zero-slope fraction={p['inside_zero_slope_fraction']:.3f}, "
                    f"positive-slope n={int(p['inside_positive_slope_n']):,}, "
                    f"quadrant n={int(p['quadrant_n']):,}."
                ),
                "",
            ]
        )
    lines.extend(["## Validation notes", ""])
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    return "\n".join(lines)


def load_inputs(root: Path) -> pd.DataFrame:
    return pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV)


def write_outputs(root: Path, summary: pd.DataFrame, notes: list[str]) -> None:
    (root / CSV_PATH).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(root / CSV_PATH, index=False)
    (root / REPORT_PATH).write_text(render_report(summary, notes), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Build Layer A trend-threshold sensitivity report.")


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    root = find_repo_root()
    df = load_inputs(root)
    summary = build_sensitivity(df)
    notes = validate_sensitivity(summary)
    write_outputs(root, summary, notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

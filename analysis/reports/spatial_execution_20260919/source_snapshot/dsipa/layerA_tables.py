"""Layer A denominator, censoring, and manuscript table summaries."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.paths import find_repo_root
from dsipa.schema import (
    EDGE_PROFILES_NATIONAL_CSV,
    PA_BUFFER_VALIDITY_CSV,
    PA_GEOMETRIES_CSV,
    PA_RISK_RANKINGS_CSV,
    PA_TRENDS_CSV,
    RADIANCE_BUFFERS_NATIONAL_CSV,
)

MIN_VALID_PIXELS = 10
MIN_VALID_YEARS = 8
PRIMARY_BUFFER_TYPE = "land_unprotected"
PRIMARY_METRIC = "mean"
BASELINE_YEAR = 2024
REPORT_PATH = "analysis/reports/layerA_denominators_and_censoring.md"
CSV_PATH = "analysis/reports/layerA_denominators_and_censoring.csv"
TABLE1_CANDIDATE_PATH = "analysis/reports/layerA_table1_candidate.md"


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _percent(n: int | float, denominator: int | float | None) -> float:
    if denominator in (None, 0) or pd.isna(denominator):
        return np.nan
    return float(n) / float(denominator)


def _row(
    *,
    key: str,
    label: str,
    n: int,
    denominator_n: int | None,
    selection_rule: str,
    notes: str,
) -> dict[str, object]:
    return {
        "key": key,
        "label": label,
        "n": int(n),
        "denominator_n": "" if denominator_n is None else int(denominator_n),
        "percent": _percent(n, denominator_n),
        "selection_rule": selection_rule,
        "notes": notes,
    }


def _primary_trends(trends: pd.DataFrame) -> pd.DataFrame:
    return trends[
        (trends["metric"] == PRIMARY_METRIC)
        & (trends["buffer_type"] == PRIMARY_BUFFER_TYPE)
        & (trends["n_years_inside"] >= MIN_VALID_YEARS)
    ].copy()


def _quadrant_counts(risk: pd.DataFrame) -> dict[str, int]:
    if risk.empty:
        return {"q1": 0, "q2": 0, "q3": 0, "q4": 0}
    x = risk["slope_buffer_1km"]
    y = risk["slope_inside"]
    return {
        "q1": int(((x > 0) & (y > 0)).sum()),
        "q2": int(((x <= 0) & (y > 0)).sum()),
        "q3": int(((x <= 0) & (y <= 0)).sum()),
        "q4": int(((x > 0) & (y <= 0)).sum()),
    }


def build_denominator_rows(
    *,
    geoms: pd.DataFrame,
    radiance: pd.DataFrame,
    edge_profiles: pd.DataFrame,
    buffer_validity: pd.DataFrame,
    trends: pd.DataFrame,
    risk: pd.DataFrame,
) -> pd.DataFrame:
    """Build the single source-of-truth denominator/censoring table."""
    total_pas = int(geoms["pa_id"].nunique())
    inside_2024 = radiance[
        (radiance["zone"] == "inside") & (radiance["year"] == BASELINE_YEAR)
    ].copy()
    inside_2024_valid = inside_2024[inside_2024["valid_pixel_count"] >= MIN_VALID_PIXELS]
    n_inside_eligible = int(inside_2024_valid["pa_id"].nunique())
    n_inside_ineligible = max(total_pas - n_inside_eligible, 0)
    n_inside_zero = int((inside_2024_valid["mean"] == 0).sum())

    primary = _primary_trends(trends)
    n_trend = int(primary["slope_inside"].notna().sum())
    trend_valid = primary[primary["slope_inside"].notna()]
    n_trend_zero = int((trend_valid["slope_inside"] == 0).sum())
    n_trend_positive = int((trend_valid["slope_inside"] > 0).sum())
    n_buffer1_trend = int(primary["slope_buffer_1km"].notna().sum())
    n_buffer5_trend = int(primary["slope_buffer_5km"].notna().sum())

    buffer_2024 = radiance[
        (radiance["zone"] == "buffer")
        & (radiance["year"] == BASELINE_YEAR)
        & (radiance["buffer_type"] == PRIMARY_BUFFER_TYPE)
        & (radiance["buffer_km"] == 1.0)
    ].copy()
    n_buffer1_2024_valid = int(
        buffer_2024.loc[buffer_2024["valid_pixel_count"] >= MIN_VALID_PIXELS, "pa_id"].nunique()
    )

    buffer1_validity = buffer_validity[buffer_validity["buffer_km"] == 1.0].copy()
    n_buffer1_land_ge50 = int((buffer1_validity["land_fraction"] >= 0.5).sum())
    n_buffer1_overlap_le25 = int((buffer1_validity["protected_overlap_fraction"] <= 0.25).sum())

    risk_n = int(len(risk))
    quadrants = _quadrant_counts(risk)

    edge_2024 = edge_profiles[edge_profiles["year"] == BASELINE_YEAR].copy()
    ring_counts = (
        edge_2024[edge_2024["valid_pixel_count"] >= MIN_VALID_PIXELS]
        .groupby("ring_index")["pa_id"]
        .nunique()
        .to_dict()
    )
    ring_meta = (
        edge_profiles[["ring_index", "ring_inner_km", "ring_outer_km"]]
        .drop_duplicates()
        .sort_values("ring_index")
    )
    n_rings = int(edge_profiles["ring_index"].nunique())
    complete_ring_counts = (
        edge_2024[edge_2024["valid_pixel_count"] >= MIN_VALID_PIXELS]
        .groupby("pa_id")["ring_index"]
        .nunique()
    )
    n_complete_rings = int((complete_ring_counts == n_rings).sum())

    rows = [
        _row(
            key="pa_universe",
            label="Protected-area universe",
            n=total_pas,
            denominator_n=total_pas,
            selection_rule="Dissolved CAPAD PA_ID universe.",
            notes="Base denominator for Layer A.",
        ),
        _row(
            key="inside_2024_eligible",
            label=f"Inside baseline eligible ({BASELINE_YEAR})",
            n=n_inside_eligible,
            denominator_n=total_pas,
            selection_rule=f"Inside PA, {BASELINE_YEAR}, valid pixels >= {MIN_VALID_PIXELS}.",
            notes="Eligible for stable baseline inside radiance mapping.",
        ),
        _row(
            key="inside_2024_ineligible",
            label=f"Inside baseline ineligible ({BASELINE_YEAR})",
            n=n_inside_ineligible,
            denominator_n=total_pas,
            selection_rule=f"Inside PA, {BASELINE_YEAR}, valid pixels < {MIN_VALID_PIXELS}.",
            notes="Ineligible under the minimum-pixel rule, not necessarily missing source data.",
        ),
        _row(
            key="inside_2024_zero_mean",
            label=f"Inside baseline zero mean ({BASELINE_YEAR})",
            n=n_inside_zero,
            denominator_n=n_inside_eligible,
            selection_rule="Eligible inside baseline rows with mean radiance == 0.",
            notes="Primary baseline floor/censoring indicator.",
        ),
        _row(
            key="inside_trend_eligible",
            label="Inside trend eligible",
            n=n_trend,
            denominator_n=total_pas,
            selection_rule=(
                f"Primary metric={PRIMARY_METRIC}, buffer={PRIMARY_BUFFER_TYPE}, "
                f"inside valid years >= {MIN_VALID_YEARS}."
            ),
            notes="Eligible for primary inside Theil-Sen trend estimates.",
        ),
        _row(
            key="inside_trend_zero_slope",
            label="Inside trend exactly zero slope",
            n=n_trend_zero,
            denominator_n=n_trend,
            selection_rule="Primary inside trend slope == 0.",
            notes="Primary trend floor/censoring indicator.",
        ),
        _row(
            key="inside_trend_positive_slope",
            label="Inside trend positive slope",
            n=n_trend_positive,
            denominator_n=n_trend,
            selection_rule="Primary inside trend slope > 0.",
            notes="Non-zero brightening subset for primary trends.",
        ),
        _row(
            key="buffer1_2024_valid",
            label=f"1 km unprotected-land buffer valid ({BASELINE_YEAR})",
            n=n_buffer1_2024_valid,
            denominator_n=total_pas,
            selection_rule=(
                f"Buffer 1 km, {PRIMARY_BUFFER_TYPE}, {BASELINE_YEAR}, "
                f"valid pixels >= {MIN_VALID_PIXELS}."
            ),
            notes="Baseline buffer availability for external-pressure context.",
        ),
        _row(
            key="buffer1_trend_eligible",
            label="1 km unprotected-land buffer trend eligible",
            n=n_buffer1_trend,
            denominator_n=n_trend,
            selection_rule="Primary trend rows with non-missing 1 km buffer slope.",
            notes="Buffer trend availability among inside-trend-eligible PAs.",
        ),
        _row(
            key="buffer5_trend_eligible",
            label="5 km unprotected-land buffer trend eligible",
            n=n_buffer5_trend,
            denominator_n=n_trend,
            selection_rule="Primary trend rows with non-missing 5 km buffer slope.",
            notes="Wider-buffer trend availability among inside-trend-eligible PAs.",
        ),
        _row(
            key="buffer1_land_ge50",
            label="1 km buffer land fraction >= 0.5",
            n=n_buffer1_land_ge50,
            denominator_n=total_pas,
            selection_rule="Buffer validity table, 1 km raw buffer land fraction >= 0.5.",
            notes="Candidate stricter-valid-buffer sensitivity condition.",
        ),
        _row(
            key="buffer1_overlap_le25",
            label="1 km buffer protected overlap <= 0.25",
            n=n_buffer1_overlap_le25,
            denominator_n=total_pas,
            selection_rule="Buffer validity table, 1 km protected-overlap fraction <= 0.25.",
            notes="Candidate stricter-valid-buffer sensitivity condition.",
        ),
        _row(
            key="retention_quadrant_eligible",
            label="Retention/quadrant eligible",
            n=risk_n,
            denominator_n=n_trend,
            selection_rule="Primary inside trend plus non-missing 1 km buffer trend and covariates.",
            notes="Denominator for retention quadrant and category-safe risk rankings.",
        ),
        _row(
            key="quadrant_q1_concurrent_brightening",
            label="Q1 concurrent inside and buffer brightening",
            n=quadrants["q1"],
            denominator_n=risk_n,
            selection_rule="Buffer slope > 0 and inside slope > 0.",
            notes="Concurrent brightening subset.",
        ),
        _row(
            key="quadrant_q2_internal_brightening",
            label="Q2 internal brightening with stable/non-detect buffer",
            n=quadrants["q2"],
            denominator_n=risk_n,
            selection_rule="Buffer slope <= 0 and inside slope > 0.",
            notes="Internal brightening subset.",
        ),
        _row(
            key="quadrant_q3_stable_or_non_detect",
            label="Q3 stable/non-detect inside and buffer",
            n=quadrants["q3"],
            denominator_n=risk_n,
            selection_rule="Buffer slope <= 0 and inside slope <= 0.",
            notes="Stable or non-detect subset under primary thresholds.",
        ),
        _row(
            key="quadrant_q4_external_pressure",
            label="Q4 external pressure without inside brightening",
            n=quadrants["q4"],
            denominator_n=risk_n,
            selection_rule="Buffer slope > 0 and inside slope <= 0.",
            notes="External-pressure subset under primary thresholds.",
        ),
    ]

    for _, ring in ring_meta.iterrows():
        ring_index = int(ring["ring_index"])
        label = f"Inside ring {ring_index} valid ({ring['ring_inner_km']:.0f}-{ring['ring_outer_km']:.0f} km)"
        rows.append(
            _row(
                key=f"ring{ring_index}_2024_valid",
                label=label,
                n=int(ring_counts.get(ring_index, 0)),
                denominator_n=total_pas,
                selection_rule=(
                    f"Inside ring {ring_index}, {BASELINE_YEAR}, "
                    f"valid pixels >= {MIN_VALID_PIXELS}."
                ),
                notes="Ring feasibility denominator for edge/penetration analysis.",
            )
        )

    rows.append(
        _row(
            key="complete_rings_2024",
            label=f"Complete ring set ({BASELINE_YEAR})",
            n=n_complete_rings,
            denominator_n=total_pas,
            selection_rule=(
                f"All {n_rings} inside rings have valid pixels >= {MIN_VALID_PIXELS} "
                f"in {BASELINE_YEAR}."
            ),
            notes="Conditional denominator for complete-ring edge profile summaries.",
        )
    )

    out = pd.DataFrame(rows)
    return out[
        ["key", "label", "n", "denominator_n", "percent", "selection_rule", "notes"]
    ]


def validate_rows(rows: pd.DataFrame) -> list[str]:
    """Return human-readable validation notes and raise on hard failures."""
    notes = []
    keyed = rows.set_index("key")

    def n(key: str) -> int:
        return int(keyed.loc[key, "n"])

    total = n("pa_universe")
    if total <= 0:
        raise ValueError("PA universe must be positive.")
    if n("inside_2024_eligible") + n("inside_2024_ineligible") != total:
        raise ValueError("Inside eligible + ineligible does not equal PA universe.")
    if n("inside_trend_eligible") > total:
        raise ValueError("Inside trend eligibility exceeds PA universe.")
    if n("retention_quadrant_eligible") > n("inside_trend_eligible"):
        raise ValueError("Retention denominator exceeds inside trend denominator.")
    for key in rows["key"]:
        denominator = keyed.loc[key, "denominator_n"]
        if denominator != "" and n(key) > int(denominator):
            raise ValueError(f"{key} exceeds its denominator.")

    notes.append("PA universe is positive.")
    notes.append("Inside eligible + ineligible equals PA universe.")
    notes.append("Inside trend and retention denominators are nested correctly.")
    notes.append("All counts are <= their stated denominators.")
    return notes


def _fmt_count(value: object) -> str:
    if value == "" or pd.isna(value):
        return ""
    return f"{int(value):,}"


def _fmt_percent(value: object) -> str:
    if pd.isna(value):
        return ""
    return f"{float(value) * 100:.1f}%"


def _md_cell(value: object) -> str:
    text = "" if pd.isna(value) else str(value)
    return text.replace("\n", " ").replace("|", "\\|")


def _markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    view = df[columns].copy()
    if "n" in view:
        view["n"] = view["n"].map(_fmt_count)
    if "denominator_n" in view:
        view["denominator_n"] = view["denominator_n"].map(_fmt_count)
    if "percent" in view:
        view["percent"] = view["percent"].map(_fmt_percent)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(_md_cell(row[column]) for column in columns) + " |"
        for _, row in view.iterrows()
    ]
    return "\n".join([header, separator, *body])


def render_report(rows: pd.DataFrame, validation_notes: list[str]) -> str:
    lines = [
        "# Layer A denominators and censoring",
        "",
        f"Generated: {_now_utc()}",
        "",
        "Primary settings:",
        "",
        f"- Baseline year: {BASELINE_YEAR}",
        f"- Minimum valid pixels: {MIN_VALID_PIXELS}",
        f"- Minimum valid years: {MIN_VALID_YEARS}",
        f"- Primary metric: `{PRIMARY_METRIC}`",
        f"- Primary buffer type: `{PRIMARY_BUFFER_TYPE}`",
        "",
        "## Denominator table",
        "",
        _markdown_table(
            rows,
            ["key", "label", "n", "denominator_n", "percent", "selection_rule", "notes"],
        ),
        "",
        "## Validation notes",
        "",
    ]
    lines.extend(f"- {note}" for note in validation_notes)
    lines.append("")
    return "\n".join(lines)


def render_table1_candidate(rows: pd.DataFrame) -> str:
    table_keys = [
        "pa_universe",
        "inside_2024_eligible",
        "inside_2024_ineligible",
        "inside_2024_zero_mean",
        "inside_trend_eligible",
        "inside_trend_zero_slope",
        "inside_trend_positive_slope",
        "retention_quadrant_eligible",
        "quadrant_q1_concurrent_brightening",
        "quadrant_q2_internal_brightening",
        "quadrant_q3_stable_or_non_detect",
        "quadrant_q4_external_pressure",
        "ring0_2024_valid",
        "ring1_2024_valid",
        "ring2_2024_valid",
        "complete_rings_2024",
    ]
    subset = rows[rows["key"].isin(table_keys)].copy()
    subset["order"] = subset["key"].map({key: idx for idx, key in enumerate(table_keys)})
    subset = subset.sort_values("order").drop(columns=["order"])
    lines = [
        "**Table 1. Feasibility, censoring, and denominators for the DSIPA Layer A audit.**",
        "",
        _markdown_table(
            subset,
            ["label", "n", "denominator_n", "percent", "selection_rule", "notes"],
        ),
        "",
        (
            "Counts use the `v0.3.0` processed Layer A evidence. Percentages are relative to "
            "the stated denominator, so rows intentionally mix PA-universe, trend-eligible, "
            "retention-eligible, and ring-complete denominators."
        ),
        "",
    ]
    return "\n".join(lines)


def load_inputs(root: Path) -> dict[str, pd.DataFrame]:
    return {
        "geoms": pd.read_csv(root / PA_GEOMETRIES_CSV),
        "radiance": pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV),
        "edge_profiles": pd.read_csv(root / EDGE_PROFILES_NATIONAL_CSV),
        "buffer_validity": pd.read_csv(root / PA_BUFFER_VALIDITY_CSV),
        "trends": pd.read_csv(root / PA_TRENDS_CSV),
        "risk": pd.read_csv(root / PA_RISK_RANKINGS_CSV),
    }


def write_outputs(root: Path, rows: pd.DataFrame, validation_notes: list[str]) -> None:
    report_path = root / REPORT_PATH
    csv_path = root / CSV_PATH
    table_path = root / TABLE1_CANDIDATE_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    rows.to_csv(csv_path, index=False)
    report_path.write_text(render_report(rows, validation_notes), encoding="utf-8")
    table_path.write_text(render_table1_candidate(rows), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Layer A denominator/censoring tables.")
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    root = find_repo_root()
    inputs = load_inputs(root)
    rows = build_denominator_rows(**inputs)
    validation_notes = validate_rows(rows)
    write_outputs(root, rows, validation_notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Layer A buffer-validity sensitivity for retention/external-pressure claims."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.paths import find_repo_root
from dsipa.schema import PA_BUFFER_VALIDITY_CSV, PA_RISK_RANKINGS_CSV

REPORT_PATH = "analysis/reports/layerA_buffer_validity_sensitivity.md"
CSV_PATH = "analysis/reports/layerA_buffer_validity_sensitivity.csv"
PRIMARY_BUFFER_KM = 1.0
LAND_FRACTION_THRESHOLD = 0.5
OVERLAP_THRESHOLD = 0.25


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _quadrants(df: pd.DataFrame) -> dict[str, int]:
    if df.empty:
        return {"q1": 0, "q2": 0, "q3": 0, "q4": 0}
    x = df["slope_buffer_1km"]
    y = df["slope_inside"]
    return {
        "q1": int(((x > 0) & (y > 0)).sum()),
        "q2": int(((x <= 0) & (y > 0)).sum()),
        "q3": int(((x <= 0) & (y <= 0)).sum()),
        "q4": int(((x > 0) & (y <= 0)).sum()),
    }


def _scenario_rows(df: pd.DataFrame, label: str, mask: pd.Series) -> dict[str, object]:
    subset = df[mask].copy()
    q = _quadrants(subset)
    n = len(subset)
    return {
        "scenario": label,
        "n": n,
        "retained_fraction": np.nan if len(df) == 0 else n / len(df),
        "q1_concurrent_brightening": q["q1"],
        "q2_internal_brightening": q["q2"],
        "q3_stable_non_detect": q["q3"],
        "q4_external_pressure": q["q4"],
        "q1_fraction": np.nan if n == 0 else q["q1"] / n,
        "q2_fraction": np.nan if n == 0 else q["q2"] / n,
        "q3_fraction": np.nan if n == 0 else q["q3"] / n,
        "q4_fraction": np.nan if n == 0 else q["q4"] / n,
        "inside_positive_count": int((subset["slope_inside"] > 0).sum()),
        "buffer_positive_count": int((subset["slope_buffer_1km"] > 0).sum()),
        "median_inside_slope": subset["slope_inside"].median(),
        "median_buffer_slope": subset["slope_buffer_1km"].median(),
        "median_retention_index_1km": subset["retention_index_1km"].median(),
        "land_fraction_min": subset["land_fraction"].min(),
        "land_fraction_median": subset["land_fraction"].median(),
        "protected_overlap_fraction_max": subset["protected_overlap_fraction"].max(),
        "protected_overlap_fraction_median": subset["protected_overlap_fraction"].median(),
    }


def build_sensitivity(risk: pd.DataFrame, buffer_validity: pd.DataFrame) -> pd.DataFrame:
    validity = buffer_validity[buffer_validity["buffer_km"] == PRIMARY_BUFFER_KM].copy()
    merged = risk.merge(validity, on="pa_id", how="left", validate="one_to_one")
    land_ok = merged["land_fraction"] >= LAND_FRACTION_THRESHOLD
    overlap_ok = merged["protected_overlap_fraction"] <= OVERLAP_THRESHOLD
    has_validity = merged["land_fraction"].notna() & merged["protected_overlap_fraction"].notna()

    rows = [
        _scenario_rows(merged, "primary_retention_quadrant", pd.Series(True, index=merged.index)),
        _scenario_rows(merged, f"has_{PRIMARY_BUFFER_KM:.0f}km_buffer_validity", has_validity),
        _scenario_rows(merged, f"land_fraction_ge_{LAND_FRACTION_THRESHOLD:.2f}", land_ok),
        _scenario_rows(merged, f"protected_overlap_le_{OVERLAP_THRESHOLD:.2f}", overlap_ok),
        _scenario_rows(
            merged,
            f"land_ge_{LAND_FRACTION_THRESHOLD:.2f}_and_overlap_le_{OVERLAP_THRESHOLD:.2f}",
            land_ok & overlap_ok,
        ),
    ]
    return pd.DataFrame(rows)


def validate_sensitivity(summary: pd.DataFrame) -> list[str]:
    notes = []
    primary_n = int(summary.loc[summary["scenario"] == "primary_retention_quadrant", "n"].iloc[0])
    if primary_n <= 0:
        raise ValueError("Primary retention/quadrant denominator must be positive.")
    for _, row in summary.iterrows():
        q_sum = int(
            row["q1_concurrent_brightening"]
            + row["q2_internal_brightening"]
            + row["q3_stable_non_detect"]
            + row["q4_external_pressure"]
        )
        if q_sum != int(row["n"]):
            raise ValueError(f"Quadrants do not sum to n for {row['scenario']}.")
        if row["n"] > primary_n:
            raise ValueError(f"{row['scenario']} exceeds primary n.")
    notes.append("All scenario counts are nested within the primary retention/quadrant denominator.")
    notes.append("Quadrant counts sum to each scenario denominator.")
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
            "scenario",
            "n",
            "retained_fraction",
            "q1_concurrent_brightening",
            "q2_internal_brightening",
            "q3_stable_non_detect",
            "q4_external_pressure",
            "q1_fraction",
            "q4_fraction",
            "median_inside_slope",
            "median_buffer_slope",
            "median_retention_index_1km",
        ]
    ].copy()
    lines = [
        "# Layer A buffer-validity sensitivity",
        "",
        f"Generated: {_now_utc()}",
        "",
        "Primary retention/quadrant analyses use 1 km `land_unprotected` buffer trends. "
        "This sensitivity checks whether headline quadrant counts are stable when conditioning "
        "on stricter raw-buffer land fraction and protected-overlap criteria.",
        "",
        "## Scenario summary",
        "",
        _markdown_table(compact),
        "",
        "## Validation notes",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    return "\n".join(lines)


def load_inputs(root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    return pd.read_csv(root / PA_RISK_RANKINGS_CSV), pd.read_csv(root / PA_BUFFER_VALIDITY_CSV)


def write_outputs(root: Path, summary: pd.DataFrame, notes: list[str]) -> None:
    (root / CSV_PATH).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(root / CSV_PATH, index=False)
    (root / REPORT_PATH).write_text(render_report(summary, notes), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Build Layer A buffer-validity sensitivity report.")


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    root = find_repo_root()
    risk, buffer_validity = load_inputs(root)
    summary = build_sensitivity(risk, buffer_validity)
    notes = validate_sensitivity(summary)
    write_outputs(root, summary, notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

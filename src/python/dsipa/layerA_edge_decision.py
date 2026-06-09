"""Layer A edge/penetration feasibility and interpretation decision report."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.paths import find_repo_root
from dsipa.schema import EDGE_PROFILES_NATIONAL_CSV

REPORT_PATH = "analysis/reports/layerA_edge_profile_decision.md"
CSV_PATH = "analysis/reports/layerA_edge_profile_decision.csv"
BASELINE_YEAR = 2024
MIN_VALID_PIXELS = 10


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def build_edge_summary(df: pd.DataFrame) -> pd.DataFrame:
    year_df = df[df["year"] == BASELINE_YEAR].copy()
    n_total = int(df["pa_id"].nunique())
    n_rings = int(df["ring_index"].nunique())
    valid = year_df[year_df["valid_pixel_count"] >= MIN_VALID_PIXELS].copy()
    complete_counts = valid.groupby("pa_id")["ring_index"].nunique()
    complete_ids = set(complete_counts[complete_counts == n_rings].index)
    complete = valid[valid["pa_id"].isin(complete_ids)].copy()

    rows = []
    ring_meta = (
        df[["ring_index", "ring_inner_km", "ring_outer_km"]]
        .drop_duplicates()
        .sort_values("ring_index")
    )
    for _, ring in ring_meta.iterrows():
        ring_index = int(ring["ring_index"])
        valid_ring = valid[valid["ring_index"] == ring_index]
        complete_ring = complete[complete["ring_index"] == ring_index]
        rows.append(
            {
                "ring_index": ring_index,
                "ring_inner_km": float(ring["ring_inner_km"]),
                "ring_outer_km": float(ring["ring_outer_km"]),
                "valid_pa_n": int(valid_ring["pa_id"].nunique()),
                "valid_pa_fraction": np.nan if n_total == 0 else valid_ring["pa_id"].nunique() / n_total,
                "complete_pa_n": int(len(complete_ids)),
                "complete_pa_fraction": np.nan if n_total == 0 else len(complete_ids) / n_total,
                "complete_frac_gt0_median": complete_ring["frac_gt0"].median(),
                "complete_frac_gt0_mean": complete_ring["frac_gt0"].mean(),
                "complete_frac_gt0_p95": complete_ring["frac_gt0"].quantile(0.95),
                "complete_nonzero_share": (complete_ring["frac_gt0"] > 0).mean(),
                "complete_mean_radiance_median": complete_ring["mean"].median(),
                "complete_mean_radiance_mean": complete_ring["mean"].mean(),
            }
        )
    return pd.DataFrame(rows)


def validate_edge_summary(summary: pd.DataFrame) -> list[str]:
    if summary.empty:
        raise ValueError("Edge summary is empty.")
    if not summary["valid_pa_fraction"].between(0, 1).all():
        raise ValueError("Ring valid fractions outside [0,1].")
    if not summary["complete_pa_fraction"].between(0, 1).all():
        raise ValueError("Complete-ring fractions outside [0,1].")
    notes = [
        "Ring valid fractions are within [0,1].",
        "Complete-ring fractions are within [0,1].",
    ]
    if (summary["complete_frac_gt0_median"] == 0).all():
        notes.append("Complete-ring median frac_gt0 is zero in all rings, so median profiles are not interpretable as absence of edge effect.")
    if summary["complete_pa_fraction"].max() < 0.05:
        notes.append("Complete-ring coverage is <5% of the PA universe, so edge profiles are feasibility-limited diagnostics.")
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
            "ring_index",
            "ring_inner_km",
            "ring_outer_km",
            "valid_pa_n",
            "valid_pa_fraction",
            "complete_pa_n",
            "complete_pa_fraction",
            "complete_frac_gt0_median",
            "complete_frac_gt0_mean",
            "complete_nonzero_share",
        ]
    ].copy()
    lines = [
        "# Layer A edge/penetration decision report",
        "",
        f"Generated: {_now_utc()}",
        "",
        (
            "This report resolves the Stage 2 edge/penetration critique. The current edge figure "
            "should be retained as a feasibility-limited diagnostic using ring feasibility plus "
            "conditional non-zero share, not interpreted as a definitive penetration-gradient test."
        ),
        "",
        "## Ring feasibility and conditional signal",
        "",
        _markdown_table(compact),
        "",
        "## Decision",
        "",
        (
            "Retain the existing ring widths (0-1, 1-5, 5-10 km) for this manuscript pass and "
            "do not add adaptive rings in Stage 2. Complete-ring coverage is too small for a "
            "new adaptive analysis to become a primary result without substantial revalidation. "
            "The figure/caption should state that median `frac_gt0` is zero under floor domination "
            "and that the plotted conditional non-zero share is a diagnostic, not proof of absence "
            "or presence of edge effects."
        ),
        "",
        "## Validation notes",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    return "\n".join(lines)


def load_inputs(root: Path) -> pd.DataFrame:
    return pd.read_csv(root / EDGE_PROFILES_NATIONAL_CSV)


def write_outputs(root: Path, summary: pd.DataFrame, notes: list[str]) -> None:
    (root / CSV_PATH).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(root / CSV_PATH, index=False)
    (root / REPORT_PATH).write_text(render_report(summary, notes), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Build Layer A edge profile decision report.")


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    root = find_repo_root()
    df = load_inputs(root)
    summary = build_edge_summary(df)
    notes = validate_edge_summary(summary)
    write_outputs(root, summary, notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

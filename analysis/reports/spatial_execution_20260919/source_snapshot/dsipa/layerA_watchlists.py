"""Layer A uncertainty-aware watchlists and dominance summaries."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.paths import find_repo_root
from dsipa.schema import PA_GEOMETRIES_CSV, PA_RISK_RANKINGS_CSV, PA_TREND_BOOTSTRAP_SUMMARY_CSV

WATCHLIST_CSV = "analysis/reports/layerA_watchlists_uncertainty.csv"
WATCHLIST_REPORT = "analysis/reports/layerA_watchlists_uncertainty.md"
DOMINANCE_MATRIX_CSV = "analysis/reports/pa_trend_dominance_matrix.csv"
DOMINANCE_SUMMARY_CSV = "analysis/reports/layerA_dominance_summary.csv"
DOMINANCE_SUMMARY_REPORT = "analysis/reports/layerA_dominance_summary.md"
SUPPLEMENTARY_TABLES = "manuscript/text/supplementary_tables.md"


@dataclass(frozen=True)
class WatchlistCategory:
    key: str
    label: str
    rank_col: str
    definition: str


CATEGORIES = (
    WatchlistCategory(
        key="inside_brightening",
        label="Inside brightening",
        rank_col="rank_inside_brightening",
        definition="inside slope > 0; ranked by inside slope",
    ),
    WatchlistCategory(
        key="external_pressure",
        label="External pressure",
        rank_col="rank_external_pressure_1km",
        definition="1 km unprotected-land buffer slope > 0 and inside slope <= 0; ranked by buffer slope",
    ),
    WatchlistCategory(
        key="internalisation",
        label="Internalisation",
        rank_col="rank_internalisation_1km",
        definition="inside slope > 0 and inside slope > 1 km buffer slope; ranked by inside-minus-buffer gap",
    ),
)

WATCHLIST_COLUMNS = [
    "category_key",
    "category",
    "category_rank",
    "pa_id",
    "name",
    "state",
    "ibra_code",
    "ibra_name",
    "area_km2",
    "distance_km",
    "slope_inside",
    "slope_buffer_1km",
    "slope_buffer_5km",
    "retention_index_1km",
    "retention_index_5km",
    "inside_slope_full",
    "inside_slope_median",
    "inside_slope_ci_low",
    "inside_slope_ci_high",
    "inside_prob_slope_gt0",
    "inside_n_boot",
    "rank_source",
    "definition",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


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


def _merge_uncertainty(risk: pd.DataFrame, bootstrap: pd.DataFrame) -> pd.DataFrame:
    boot_cols = [
        "pa_id",
        "ibra_code",
        "ibra_name",
        "slope_full",
        "slope_median",
        "slope_ci_low",
        "slope_ci_high",
        "prob_slope_gt0",
        "n_boot",
    ]
    missing = [col for col in boot_cols if col not in bootstrap.columns]
    if missing:
        raise ValueError(f"Bootstrap summary missing columns: {missing}")
    merged = risk.merge(
        bootstrap[boot_cols].rename(
            columns={
                "slope_full": "inside_slope_full",
                "slope_median": "inside_slope_median",
                "slope_ci_low": "inside_slope_ci_low",
                "slope_ci_high": "inside_slope_ci_high",
                "prob_slope_gt0": "inside_prob_slope_gt0",
                "n_boot": "inside_n_boot",
            }
        ),
        on="pa_id",
        how="left",
        validate="many_to_one",
    )
    return merged


def build_watchlists(
    risk: pd.DataFrame,
    bootstrap: pd.DataFrame,
    *,
    top_n: int = 20,
    categories: tuple[WatchlistCategory, ...] = CATEGORIES,
) -> pd.DataFrame:
    merged = _merge_uncertainty(risk, bootstrap)
    rows = []
    for category in categories:
        if category.rank_col not in merged.columns:
            raise ValueError(f"Risk rankings missing rank column: {category.rank_col}")
        subset = (
            merged[merged[category.rank_col].notna()]
            .sort_values(category.rank_col)
            .head(top_n)
            .copy()
        )
        subset.insert(0, "category_key", category.key)
        subset.insert(1, "category", category.label)
        subset.insert(2, "category_rank", subset[category.rank_col].astype(int))
        subset["rank_source"] = category.rank_col
        subset["definition"] = category.definition
        rows.append(subset)

    out = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    for column in WATCHLIST_COLUMNS:
        if column not in out.columns:
            out[column] = np.nan
    return out[WATCHLIST_COLUMNS]


def validate_watchlists(watchlists: pd.DataFrame, *, top_n: int = 20) -> list[str]:
    if watchlists.empty:
        raise ValueError("Watchlist table is empty.")
    missing = [col for col in WATCHLIST_COLUMNS if col not in watchlists.columns]
    if missing:
        raise ValueError(f"Watchlist table missing columns: {missing}")

    notes = []
    for category in CATEGORIES:
        subset = watchlists[watchlists["category_key"] == category.key]
        if subset.empty:
            raise ValueError(f"No rows for watchlist category: {category.key}")
        if len(subset) > top_n:
            raise ValueError(f"Too many rows for watchlist category: {category.key}")
        if not subset["category_rank"].is_monotonic_increasing:
            raise ValueError(f"Ranks are not sorted for category: {category.key}")

    inside = watchlists[watchlists["category_key"] == "inside_brightening"]
    if not (inside["slope_inside"] > 0).all():
        raise ValueError("Inside-brightening watchlist contains non-positive inside slopes.")
    external = watchlists[watchlists["category_key"] == "external_pressure"]
    if not ((external["slope_buffer_1km"] > 0) & (external["slope_inside"] <= 0)).all():
        raise ValueError("External-pressure watchlist violates quadrant definition.")
    internal = watchlists[watchlists["category_key"] == "internalisation"]
    if not ((internal["slope_inside"] > 0) & (internal["retention_index_1km"] > 0)).all():
        raise ValueError("Internalisation watchlist violates retention definition.")

    probs = watchlists["inside_prob_slope_gt0"].dropna()
    if not probs.between(0, 1).all():
        raise ValueError("Bootstrap probabilities outside [0,1].")
    notes.append("Category filters match the risk-ranking definitions.")
    notes.append("Category ranks are sorted and capped at the requested top N.")
    notes.append("Bootstrap probability fields are bounded in [0,1].")
    missing_uncertainty = int(watchlists["inside_slope_median"].isna().sum())
    if missing_uncertainty:
        notes.append(f"Warning: {missing_uncertainty} watchlist rows lack inside-slope bootstrap uncertainty.")
    else:
        notes.append("All watchlist rows have inside-slope bootstrap uncertainty.")
    return notes


def build_dominance_summary(
    dominance: pd.DataFrame,
    risk: pd.DataFrame,
    bootstrap: pd.DataFrame,
    geoms: pd.DataFrame | None = None,
) -> pd.DataFrame:
    if dominance.empty:
        raise ValueError("Dominance matrix is empty.")
    if list(dominance.index.astype(str)) != list(dominance.columns.astype(str)):
        raise ValueError("Dominance matrix row and column IDs differ.")
    values = dominance.astype(float)
    if not ((values >= 0) & (values <= 1)).all().all():
        raise ValueError("Dominance probabilities outside [0,1].")

    risk_idx = risk.set_index("pa_id")
    boot = bootstrap.rename(
        columns={
            "slope_full": "inside_slope_full",
            "slope_median": "inside_slope_median",
            "slope_ci_low": "inside_slope_ci_low",
            "slope_ci_high": "inside_slope_ci_high",
            "prob_slope_gt0": "inside_prob_slope_gt0",
            "n_boot": "inside_n_boot",
        }
    ).set_index("pa_id")
    geoms_idx = pd.DataFrame()
    if geoms is not None and not geoms.empty:
        geom_cols = [col for col in ["pa_id", "NAME", "STATE"] if col in geoms.columns]
        if set(["pa_id", "NAME", "STATE"]).issubset(geom_cols):
            geoms_idx = geoms[["pa_id", "NAME", "STATE"]].set_index("pa_id")

    records = []
    ids = [str(v) for v in values.index]
    for pa_id in ids:
        row = values.loc[pa_id].drop(index=pa_id)
        risk_meta = risk_idx.loc[pa_id] if pa_id in risk_idx.index else pd.Series(dtype=object)
        boot_meta = boot.loc[pa_id] if pa_id in boot.index else pd.Series(dtype=object)
        geom_meta = geoms_idx.loc[pa_id] if pa_id in geoms_idx.index else pd.Series(dtype=object)
        name = risk_meta.get("name", np.nan)
        if pd.isna(name):
            name = geom_meta.get("NAME", np.nan)
        state = risk_meta.get("state", np.nan)
        if pd.isna(state):
            state = geom_meta.get("STATE", np.nan)
        records.append(
            {
                "pa_id": pa_id,
                "name": name,
                "state": state,
                "ibra_code": boot_meta.get("ibra_code", risk_meta.get("ibra_code", np.nan)),
                "slope_inside": risk_meta.get("slope_inside", boot_meta.get("inside_slope_full", np.nan)),
                "inside_slope_median": boot_meta.get("inside_slope_median", np.nan),
                "inside_slope_ci_low": boot_meta.get("inside_slope_ci_low", np.nan),
                "inside_slope_ci_high": boot_meta.get("inside_slope_ci_high", np.nan),
                "inside_prob_slope_gt0": boot_meta.get("inside_prob_slope_gt0", np.nan),
                "dominance_mean_vs_others": row.mean(),
                "dominance_min_vs_others": row.min(),
                "dominance_gt_0_75_count": int((row > 0.75).sum()),
                "dominance_gt_0_90_count": int((row > 0.90).sum()),
                "dominance_ambiguous_40_60_count": int(((row >= 0.40) & (row <= 0.60)).sum()),
            }
        )
    out = pd.DataFrame.from_records(records)
    return out.sort_values("dominance_mean_vs_others", ascending=False).reset_index(drop=True)


def validate_dominance_summary(summary: pd.DataFrame) -> list[str]:
    if summary.empty:
        raise ValueError("Dominance summary is empty.")
    prob_cols = [
        "dominance_mean_vs_others",
        "dominance_min_vs_others",
        "inside_prob_slope_gt0",
    ]
    for col in prob_cols:
        values = summary[col].dropna()
        if not values.between(0, 1).all():
            raise ValueError(f"{col} outside [0,1].")
    return [
        "Dominance matrix is square and bounded in [0,1].",
        "Dominance summary reports mean/min pairwise dominance and ambiguous-pair counts.",
    ]


def _display_watchlists(watchlists: pd.DataFrame) -> pd.DataFrame:
    display = watchlists.copy()
    display["inside_slope_95ci"] = display.apply(
        lambda row: (
            ""
            if pd.isna(row["inside_slope_ci_low"]) or pd.isna(row["inside_slope_ci_high"])
            else f"{row['inside_slope_ci_low']:.3f} to {row['inside_slope_ci_high']:.3f}"
        ),
        axis=1,
    )
    return display[
        [
            "category",
            "category_rank",
            "name",
            "pa_id",
            "state",
            "ibra_code",
            "area_km2",
            "slope_inside",
            "slope_buffer_1km",
            "retention_index_1km",
            "inside_slope_95ci",
            "inside_prob_slope_gt0",
        ]
    ].rename(
        columns={
            "category_rank": "rank",
            "name": "PA name",
            "pa_id": "PA_ID",
            "state": "state",
            "ibra_code": "IBRA",
            "area_km2": "area_km2",
            "slope_inside": "inside_slope",
            "slope_buffer_1km": "buffer_1km_slope",
            "retention_index_1km": "retention_1km",
            "inside_prob_slope_gt0": "P_inside_slope_gt0",
        }
    )


def render_watchlist_report(watchlists: pd.DataFrame, notes: list[str], *, top_n: int) -> str:
    lines = [
        "# Layer A uncertainty-aware watchlists",
        "",
        f"Generated: {_now_utc()}",
        "",
        (
            "Category-safe protected-area watchlists joined to the IBRA-cluster moving-block "
            "bootstrap. Uncertainty columns describe inside-protected-area mean-radiance slopes; "
            "buffer and retention columns are point estimates from the risk-ranking table."
        ),
        "",
        f"Top N per category: {top_n}",
        "",
        "## Validation notes",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    for category in CATEGORIES:
        subset = watchlists[watchlists["category_key"] == category.key]
        lines.extend(
            [
                f"## {category.label}",
                "",
                category.definition,
                "",
                _markdown_table(_display_watchlists(subset)),
                "",
            ]
        )
    return "\n".join(lines)


def render_dominance_report(summary: pd.DataFrame, notes: list[str]) -> str:
    display = summary[
        [
            "pa_id",
            "name",
            "state",
            "inside_slope_median",
            "inside_prob_slope_gt0",
            "dominance_mean_vs_others",
            "dominance_min_vs_others",
            "dominance_gt_0_75_count",
            "dominance_gt_0_90_count",
            "dominance_ambiguous_40_60_count",
        ]
    ].copy()
    return "\n".join(
        [
            "# Layer A dominance summary",
            "",
            f"Generated: {_now_utc()}",
            "",
            (
                "Simplified companion to the pairwise dominance heatmap. Rows are top brightening "
                "PAs from the bootstrap dominance matrix; dominance probabilities compare each PA "
                "against the other PAs in that matrix."
            ),
            "",
            "## Summary table",
            "",
            _markdown_table(display),
            "",
            "## Validation notes",
            "",
            *[f"- {note}" for note in notes],
            "",
        ]
    )


def render_supplementary_table_s1(watchlists: pd.DataFrame, *, top_n: int) -> str:
    return "\n".join(
        [
            "**Table S1. Protected-area watchlists, category-safe and uncertainty-aware.**",
            "",
            (
                "Watchlists are ranked within category, not as a single combined risk score. "
                "Slopes are Theil-Sen trends in scaled VIIRS radiance units per year for 2013-2024. "
                "The 95% interval and probability columns are from the IBRA-cluster moving-block "
                "bootstrap for inside-protected-area mean-radiance slopes; buffer and retention "
                "columns are point estimates. These lists are intended for triage and hypothesis "
                "generation, not precise rank ordering."
            ),
            "",
            _markdown_table(_display_watchlists(watchlists)),
        ]
    )


def update_supplementary_tables(root: Path, table_s1: str) -> None:
    path = root / SUPPLEMENTARY_TABLES
    text = path.read_text(encoding="utf-8")
    start = text.index("**Table S1.")
    end = text.index("**Table S2.", start)
    updated = text[:start] + table_s1.rstrip() + "\n\n" + text[end:]
    path.write_text(updated, encoding="utf-8")


def load_inputs(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    risk = pd.read_csv(root / PA_RISK_RANKINGS_CSV)
    bootstrap = pd.read_csv(root / PA_TREND_BOOTSTRAP_SUMMARY_CSV)
    dominance = pd.read_csv(root / DOMINANCE_MATRIX_CSV, index_col=0)
    dominance.index = dominance.index.astype(str)
    dominance.columns = dominance.columns.astype(str)
    geoms = pd.read_csv(root / PA_GEOMETRIES_CSV)
    return risk, bootstrap, dominance, geoms


def write_outputs(
    root: Path,
    watchlists: pd.DataFrame,
    watchlist_notes: list[str],
    dominance_summary: pd.DataFrame,
    dominance_notes: list[str],
    *,
    top_n: int,
    update_supplement: bool,
) -> None:
    for path in [
        root / WATCHLIST_CSV,
        root / WATCHLIST_REPORT,
        root / DOMINANCE_SUMMARY_CSV,
        root / DOMINANCE_SUMMARY_REPORT,
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)

    watchlists.to_csv(root / WATCHLIST_CSV, index=False)
    (root / WATCHLIST_REPORT).write_text(
        render_watchlist_report(watchlists, watchlist_notes, top_n=top_n),
        encoding="utf-8",
    )
    dominance_summary.to_csv(root / DOMINANCE_SUMMARY_CSV, index=False)
    (root / DOMINANCE_SUMMARY_REPORT).write_text(
        render_dominance_report(dominance_summary, dominance_notes),
        encoding="utf-8",
    )
    if update_supplement:
        update_supplementary_tables(root, render_supplementary_table_s1(watchlists, top_n=top_n))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Layer A uncertainty-aware watchlists.")
    parser.add_argument("--top-n", type=int, default=20, help="Rows per watchlist category.")
    parser.add_argument(
        "--skip-supplement",
        action="store_true",
        help="Do not update manuscript/text/supplementary_tables.md.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    risk, bootstrap, dominance, geoms = load_inputs(root)
    watchlists = build_watchlists(risk, bootstrap, top_n=args.top_n)
    watchlist_notes = validate_watchlists(watchlists, top_n=args.top_n)
    dominance_summary = build_dominance_summary(dominance, risk, bootstrap, geoms)
    dominance_notes = validate_dominance_summary(dominance_summary)
    write_outputs(
        root,
        watchlists,
        watchlist_notes,
        dominance_summary,
        dominance_notes,
        top_n=args.top_n,
        update_supplement=not args.skip_supplement,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Trend estimation and retention indices (WP0.11)."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import PA_TRENDS_CSV, RADIANCE_BUFFERS_NATIONAL_CSV, SCHEMA_VERSION
REPORT_PATH = "analysis/reports/trends_methods_and_sanity.md"
FIGURE_PATH = "manuscript/figures/fig_layerA_trend_distribution.png"

MIN_VALID_PIXELS = 10
MIN_VALID_YEARS = 8


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _theil_sen(years: np.ndarray, values: np.ndarray) -> tuple[float, float]:
    n = len(values)
    if n < 2:
        return np.nan, np.nan
    slopes = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            if years[j] == years[i]:
                continue
            slopes.append((values[j] - values[i]) / (years[j] - years[i]))
    if not slopes:
        return np.nan, np.nan
    slope = float(np.median(slopes))
    intercept = float(np.median(values - slope * years))
    return slope, intercept


def _compute_trends(df: pd.DataFrame, buffer_km: float | None) -> pd.DataFrame:
    if buffer_km is None:
        subset = df[df["zone"] == "inside"].copy()
    else:
        subset = df[(df["zone"] == "buffer") & (df["buffer_km"] == buffer_km)].copy()

    subset = subset[subset["valid_pixel_count"] >= MIN_VALID_PIXELS]
    subset = subset.dropna(subset=["median"])

    records = []
    for pa_id, group in subset.groupby("pa_id"):
        years = group["year"].to_numpy(dtype=float)
        values = group["median"].to_numpy(dtype=float)
        if len(values) < MIN_VALID_YEARS:
            slope, intercept = np.nan, np.nan
        else:
            slope, intercept = _theil_sen(years, values)
        records.append(
            {
                "pa_id": pa_id,
                "n_years": int(len(values)),
                "slope": slope,
                "intercept": intercept,
            }
        )
    return pd.DataFrame(records)


def build_trends(df: pd.DataFrame) -> pd.DataFrame:
    inside = _compute_trends(df, buffer_km=None).rename(
        columns={
            "n_years": "n_years_inside",
            "slope": "slope_inside",
            "intercept": "intercept_inside",
        }
    )
    buffer1 = _compute_trends(df, buffer_km=1.0).rename(
        columns={
            "n_years": "n_years_buffer_1km",
            "slope": "slope_buffer_1km",
            "intercept": "intercept_buffer_1km",
        }
    )
    buffer5 = _compute_trends(df, buffer_km=5.0).rename(
        columns={
            "n_years": "n_years_buffer_5km",
            "slope": "slope_buffer_5km",
            "intercept": "intercept_buffer_5km",
        }
    )

    trends = inside.merge(buffer1, on="pa_id", how="left").merge(buffer5, on="pa_id", how="left")
    trends["schema_version"] = SCHEMA_VERSION
    trends["method"] = "theil_sen"
    trends["metric"] = "median"
    trends["retention_index_1km"] = trends["slope_inside"] - trends["slope_buffer_1km"]
    trends["retention_index_5km"] = trends["slope_inside"] - trends["slope_buffer_5km"]
    return trends


def write_outputs(trends: pd.DataFrame, root: Path) -> Path:
    out_path = root / PA_TRENDS_CSV
    out_path.parent.mkdir(parents=True, exist_ok=True)
    trends.to_csv(out_path, index=False)
    return out_path


def write_report(trends: pd.DataFrame, df: pd.DataFrame, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    summary = trends[["slope_inside", "slope_buffer_1km", "slope_buffer_5km"]].describe().round(4)
    year_means = (
        df[df["zone"] == "inside"].groupby("year")["median"].mean().round(4)
    )
    year_diffs = year_means.diff().dropna()

    lines = [
        "# Trend methods and sanity report",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Method: Theil-Sen (median pairwise slopes); metric=median radiance; min years={MIN_VALID_YEARS}",
        f"Minimum valid pixels per year: {MIN_VALID_PIXELS}",
        "",
        "## Trend summary (slopes per year)",
        "",
        summary.to_string(),
        "",
        "## Mean inside median radiance by year",
        "",
        year_means.to_string(),
        "",
        "## Year-to-year differences (inside median mean)",
        "",
        year_diffs.to_string(),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_figure(trends: pd.DataFrame, fig_path: Path) -> None:
    import matplotlib.pyplot as plt

    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(trends["slope_inside"].dropna(), bins=50, color="#4C72B0", alpha=0.85)
    ax.set_xlabel("Inside slope (scaled units per year)")
    ax.set_ylabel("PA count")
    ax.set_title("Distribution of inside trends")
    fig.tight_layout()
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)


def write_artefact(
    *,
    trends_path: Path,
    report_path: Path,
    fig_path: Path,
    root: Path,
) -> Path:
    artefact_dir = root / "artefacts" / "wp0_11_trends"
    artefact_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(trends_path, artefact_dir / trends_path.name)
    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(fig_path, artefact_dir / fig_path.name)

    manifest = build_manifest(
        run_id="wp0_11_trends",
        wp="WP0.11",
        root=root,
        outputs=[trends_path.name, report_path.name, fig_path.name],
        notes="WP0.11 trend estimation outputs",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.11 trends artefact. Contains trend table, methods report, and distribution figure.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compute trends and retention indices (WP0.11).")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    df = pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV)
    trends = build_trends(df)

    trends_path = write_outputs(trends, root)
    report_path = root / REPORT_PATH
    fig_path = root / FIGURE_PATH
    write_report(trends, df, report_path)
    write_figure(trends, fig_path)

    if not args.skip_artefact:
        write_artefact(
            trends_path=trends_path,
            report_path=report_path,
            fig_path=fig_path,
            root=root,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

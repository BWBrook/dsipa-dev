"""Trend estimation and retention indices (WP0.11b)."""

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
YEARLY_PLOT_PATH = "analysis/reports/trends_yearly_means.png"

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


def _compute_trends(df: pd.DataFrame, buffer_km: float | None, metric: str) -> pd.DataFrame:
    if buffer_km is None:
        subset = df[df["zone"] == "inside"].copy()
    else:
        subset = df[(df["zone"] == "buffer") & (df["buffer_km"] == buffer_km)].copy()

    subset = subset[subset["valid_pixel_count"] >= MIN_VALID_PIXELS]
    subset = subset.dropna(subset=[metric])

    records = []
    for pa_id, group in subset.groupby("pa_id"):
        years = group["year"].to_numpy(dtype=float)
        values = group[metric].to_numpy(dtype=float)
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
    frames = []
    for metric in ("mean", "median"):
        inside = _compute_trends(df, buffer_km=None, metric=metric).rename(
            columns={
                "n_years": "n_years_inside",
                "slope": "slope_inside",
                "intercept": "intercept_inside",
            }
        )
        buffer1 = _compute_trends(df, buffer_km=1.0, metric=metric).rename(
            columns={
                "n_years": "n_years_buffer_1km",
                "slope": "slope_buffer_1km",
                "intercept": "intercept_buffer_1km",
            }
        )
        buffer5 = _compute_trends(df, buffer_km=5.0, metric=metric).rename(
            columns={
                "n_years": "n_years_buffer_5km",
                "slope": "slope_buffer_5km",
                "intercept": "intercept_buffer_5km",
            }
        )

        trends = inside.merge(buffer1, on="pa_id", how="left").merge(buffer5, on="pa_id", how="left")
        trends["schema_version"] = SCHEMA_VERSION
        trends["method"] = "theil_sen"
        trends["metric"] = metric
        trends["retention_index_1km"] = trends["slope_inside"] - trends["slope_buffer_1km"]
        trends["retention_index_5km"] = trends["slope_inside"] - trends["slope_buffer_5km"]
        frames.append(trends)

    return pd.concat(frames, ignore_index=True)


def write_outputs(trends: pd.DataFrame, root: Path) -> Path:
    out_path = root / PA_TRENDS_CSV
    out_path.parent.mkdir(parents=True, exist_ok=True)
    trends.to_csv(out_path, index=False)
    return out_path


def _yearly_summary(df: pd.DataFrame, metric: str) -> pd.Series:
    return df[df["zone"] == "inside"].groupby("year")[metric].mean()


def write_report(trends: pd.DataFrame, df: pd.DataFrame, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Trend methods and sanity report",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Method: Theil-Sen (median pairwise slopes); primary metric=mean; min years={MIN_VALID_YEARS}",
        f"Minimum valid pixels per year: {MIN_VALID_PIXELS}",
        "",
    ]

    for metric in ("mean", "median"):
        subset = trends[trends["metric"] == metric]
        summary = subset[["slope_inside", "slope_buffer_1km", "slope_buffer_5km"]].describe().round(4)
        zero_frac = (subset["slope_inside"].fillna(0.0) == 0.0).mean()
        nonzero = subset["slope_inside"][subset["slope_inside"].fillna(0.0) != 0.0]
        nonzero_summary = nonzero.describe().round(4)
        lines.extend(
            [
                f"## Trend summary ({metric})",
                "",
                summary.to_string(),
                "",
                f"Fraction of exactly-zero inside slopes ({metric}): {zero_frac:.3f}",
                "",
                "Non-zero inside slope summary:",
                nonzero_summary.to_string(),
                "",
            ]
        )

    year_means = _yearly_summary(df, "mean").round(4)
    year_medians = _yearly_summary(df, "median").round(4)
    year_diffs = year_means.diff().dropna()

    lines.extend(
        [
            "## Mean inside radiance by year (mean vs median)",
            "",
            year_means.to_string(),
            "",
            year_medians.to_string(),
            "",
            "## Year-to-year differences (inside mean)",
            "",
            year_diffs.to_string(),
            "",
            f"Plot: {Path(YEARLY_PLOT_PATH).name}",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_yearly_plot(df: pd.DataFrame, plot_path: Path) -> None:
    import matplotlib.pyplot as plt

    plot_path.parent.mkdir(parents=True, exist_ok=True)
    mean_series = _yearly_summary(df, "mean")
    median_series = _yearly_summary(df, "median")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(mean_series.index, mean_series.values, marker="o", label="Mean")
    ax.plot(median_series.index, median_series.values, marker="o", label="Median")
    ax.set_xlabel("Year")
    ax.set_ylabel("Inside radiance (scaled)")
    ax.set_title("Inside radiance by year (mean vs median)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)


def write_figure(trends: pd.DataFrame, fig_path: Path) -> None:
    import matplotlib.pyplot as plt

    fig_path.parent.mkdir(parents=True, exist_ok=True)
    mean_slopes = trends[trends["metric"] == "mean"]["slope_inside"].dropna()
    nonzero = mean_slopes[mean_slopes != 0]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(mean_slopes, bins=50, color="#4C72B0", alpha=0.85)
    axes[0].set_xlabel("Inside slope (mean)")
    axes[0].set_ylabel("PA count")
    axes[0].set_title("Inside trends (mean)")

    axes[1].hist(nonzero, bins=50, color="#DD8452", alpha=0.85)
    axes[1].set_xlabel("Inside slope (mean, non-zero)")
    axes[1].set_ylabel("PA count")
    axes[1].set_title("Inside trends (non-zero)")

    fig.suptitle("Distribution of inside trends (mean radiance)")
    fig.tight_layout()
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)


def write_artefact(
    *,
    trends_path: Path,
    report_path: Path,
    fig_path: Path,
    yearly_plot_path: Path,
    root: Path,
) -> Path:
    artefact_dir = root / "artefacts" / "wp0_11b_trends_mean"
    artefact_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(trends_path, artefact_dir / trends_path.name)
    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(fig_path, artefact_dir / fig_path.name)
    shutil.copyfile(yearly_plot_path, artefact_dir / yearly_plot_path.name)

    manifest = build_manifest(
        run_id="wp0_11b_trends_mean",
        wp="WP0.11b",
        root=root,
        outputs=[trends_path.name, report_path.name, fig_path.name, yearly_plot_path.name],
        notes="WP0.11b trend estimation outputs (mean primary)",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.11b trends artefact. Contains trend table, methods report, and figures.\n",
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
    yearly_plot_path = root / YEARLY_PLOT_PATH
    write_report(trends, df, report_path)
    write_figure(trends, fig_path)
    write_yearly_plot(df, yearly_plot_path)

    if not args.skip_artefact:
        write_artefact(
            trends_path=trends_path,
            report_path=report_path,
            fig_path=fig_path,
            yearly_plot_path=yearly_plot_path,
            root=root,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

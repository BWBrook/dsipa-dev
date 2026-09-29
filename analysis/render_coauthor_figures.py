"""Render the RSEC co-author figure set from accepted processed outputs.

The runner is intentionally a rendering layer: it reads existing CSV/GPKG and
tracked modelling-report values, and does not recompute trends or models.
``--data-root`` may be the repository root, ``data/``, or ``data/processed``.
Outputs are written below ``--output-root/manuscript/figures``.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import sys
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_REPO = Path(__file__).resolve().parents[1]
if str(SCRIPT_REPO / "src/python") not in sys.path:
    sys.path.insert(0, str(SCRIPT_REPO / "src/python"))

from dsipa.figures_layerA import (
    BASELINE_FIG,
    EDGE_FIG,
    MIN_VALID_PIXELS,
    plot_baseline_map,
    plot_edge_profiles,
)
from dsipa.vulnerability_model import write_figure as write_quadrant_figure
try:
    from analysis.input_contract import InputContract, load_manifest
except ImportError:  # direct execution from the analysis directory
    from input_contract import InputContract, load_manifest
try:
    from analysis.coauthor_evidence import describe_zero_series
except ImportError:  # direct execution from the analysis directory
    from coauthor_evidence import describe_zero_series


TRENDS_NAME = "pa_trends_v0_3_0.csv"
RADIANCE_NAME = "pa_radiance_buffers_national_v0_3_0.csv"
RISK_NAME = "pa_risk_rankings_v0_3_0.csv"
GEOMETRY_CSV_NAME = "pa_geometries_v0_3_0.csv"
GEOMETRY_GPKG_NAME = "pa_geometries_v0_3_0.gpkg"
BOOTSTRAP_NAME = "pa_trend_bootstrap_summary_v0_3_0.csv"
LAYERB_REPORT = "layerB_modelling_report.md"
EXAMPLE_SERIES_NAME = "coauthor_example_series.csv"

FIGURE_DIR = Path("manuscript/figures")
TREND_FIG = "fig_layerA_trend_distribution.png"
QUADRANT_FIG = "fig_layerA_retention_quadrant.png"
TRAJECTORY_FIG = "fig_layerA_example_trajectories.png"
LAYERB_FIG = "fig_layerB_alan_effects.png"
FOREST_FIG = "fig_layerA_trend_uncertainty_forest.png"
CORRECTION_SUMMARY_NAME = "spatial_correction_summary.json"

PRIMARY_BUFFER = "land_unprotected"
PRIMARY_METRIC = "mean"
TRAJECTORIES = {
    "WA_27575": "Neerabup",
    "WA_39584": "Henderson",
    "ACT_03": "Black Mountain",
    "NSW_N1142": "Bungonia",
}

TRAJECTORY_LABELS = {
    "WA_27575": "Q1: both slopes positive",
    "WA_39584": "Q2: inside only positive",
    "ACT_03": "Q3: neither slope positive",
    "NSW_N1142": "Q4: surrounding only positive",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_versions() -> dict[str, str | None]:
    names = ("numpy", "pandas", "geopandas", "matplotlib", "shapely", "rasterio", "scipy")
    return {
        name: _distribution_version(name)
        for name in names
    }


def _distribution_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _write_render_manifest(
    output_root: Path,
    *,
    inputs: dict[str, Path],
    outputs: dict[str, Path],
    input_contract: InputContract | None = None,
    render_receipt: dict[str, object] | None = None,
) -> Path:
    source_paths = {
        "analysis/render_coauthor_figures.py": Path(__file__).resolve(),
        "analysis/coauthor_evidence.py": SCRIPT_REPO / "analysis" / "coauthor_evidence.py",
        "src/python/dsipa/figures_layerA.py": SCRIPT_REPO / "src/python" / "dsipa" / "figures_layerA.py",
        "src/python/dsipa/vulnerability_model.py": SCRIPT_REPO / "src/python" / "dsipa" / "vulnerability_model.py",
    }
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "packages": _package_versions(),
        "inputs": {
            label: {"path": str(path), "sha256": _sha256(path), "bytes": path.stat().st_size}
            for label, path in inputs.items()
        },
        "source_files": {
            label: {"path": str(path), "sha256": _sha256(path)}
            for label, path in source_paths.items()
        },
        "outputs": {
            label: {"path": str(path), "sha256": _sha256(path)}
            for label, path in outputs.items()
        },
        "analysis": {
            "render_only": True,
            "models_refit": False,
            "trends_refit": False,
            "note": "Figures rendered from accepted processed outputs and tracked report values.",
        },
    }
    if input_contract is not None:
        manifest["input_contract"] = {
            **input_contract.identity(),
            "files": {
                name: {"path": str(path), "sha256": _sha256(path), "bytes": path.stat().st_size}
                for name, path in input_contract.files.items()
            },
        }
    if render_receipt is not None:
        manifest["render_receipt"] = render_receipt
    manifest_path = output_root / "reports" / "render_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def _resolve(data_root: Path, relative: str) -> Path:
    """Resolve an accepted output under common data-root conventions."""
    rel = Path(relative)
    candidates = [
        data_root / rel,
        data_root / "data" / "processed" / rel.name,
        data_root / "processed" / rel.name,
        data_root / "analysis" / "reports" / rel.name,
        data_root / rel.name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Could not resolve {relative} below --data-root={data_root}; "
        f"tried {', '.join(str(p) for p in candidates)}"
    )


def _manifest_contract(
    data_root: Path,
    input_manifest: Path,
    *,
    include_correction: bool,
    include_layer_b: bool = True,
) -> InputContract:
    """Validate every file this renderer will consume in manifest mode.

    Manifest keys are deliberately normalised to basenames.  The explicit
    root remains the only allowed path prefix; the subdirectories below it
    merely describe the standard corrected-run layout.
    """
    names = [
        TRENDS_NAME,
        RADIANCE_NAME,
        RISK_NAME,
        GEOMETRY_CSV_NAME,
        GEOMETRY_GPKG_NAME,
        BOOTSTRAP_NAME,
        EXAMPLE_SERIES_NAME,
        "pa_edge_profiles_national_v0_3_0.csv",
    ]
    if include_layer_b:
        names.append(LAYERB_REPORT)
    if include_correction:
        names.append(CORRECTION_SUMMARY_NAME)
    subdirectories = {
        TRENDS_NAME: Path("data/processed") / TRENDS_NAME,
        RADIANCE_NAME: Path("data/processed") / RADIANCE_NAME,
        RISK_NAME: Path("data/processed") / RISK_NAME,
        GEOMETRY_CSV_NAME: Path("data/processed") / GEOMETRY_CSV_NAME,
        GEOMETRY_GPKG_NAME: Path("data/processed") / GEOMETRY_GPKG_NAME,
        BOOTSTRAP_NAME: Path("data/processed") / BOOTSTRAP_NAME,
        "pa_edge_profiles_national_v0_3_0.csv": Path("data/processed") / "pa_edge_profiles_national_v0_3_0.csv",
        EXAMPLE_SERIES_NAME: Path("analysis/reports") / EXAMPLE_SERIES_NAME,
        CORRECTION_SUMMARY_NAME: Path("analysis/reports") / CORRECTION_SUMMARY_NAME,
    }
    if include_layer_b:
        subdirectories[LAYERB_REPORT] = Path("analysis/reports") / LAYERB_REPORT
    overrides = {name: data_root / subdirectories[name] for name in names}
    return load_manifest(input_manifest, data_root, names, path_overrides=overrides)


def _primary_trends(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"pa_id", "slope_inside", "slope_buffer_1km", "n_years_inside"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Trend table missing required columns: {sorted(missing)}")
    out = df[(df["metric"] == PRIMARY_METRIC) & (df["buffer_type"] == PRIMARY_BUFFER)].copy()
    # Fig. 2 is the inside-trend distribution and retains all inside-eligible
    # rows. The paired buffer requirement applies only to the quadrant and
    # trajectory displays.
    out = out.dropna(subset=["slope_inside"])
    if out.empty:
        raise ValueError("No primary trend rows available for figure rendering.")
    return out


def _zero_slope_breakdown(trends: pd.DataFrame, radiance_path: Path) -> tuple[dict[str, int], int]:
    """Classify exact-zero Theil-Sen rows by their annual series shape."""
    radiance = pd.read_csv(radiance_path)
    inside = radiance[
        (radiance["zone"] == "inside") & (radiance["valid_pixel_count"] >= MIN_VALID_PIXELS)
    ].copy()
    zero_ids = set(trends.loc[trends["slope_inside"].eq(0), "pa_id"].astype(str))
    wide = inside.pivot(index="pa_id", columns="year", values="mean").reindex(index=list(zero_ids))
    flags = describe_zero_series(wide)
    complete = flags["complete_12_years"]
    counts = {
        "All annual values zero": int((complete & flags["all_observed_zero"]).sum()),
        "Constant non-zero": int((complete & ~flags["any_variation"] & ~flags["all_observed_zero"]).sum()),
        "Varying": int((complete & flags["any_variation"]).sum()),
    }
    late_positive = int(flags["late_positive_complete"].sum())
    return counts, late_positive


def _validate_accepted_evidence(
    trends: pd.DataFrame,
    risk: pd.DataFrame,
    radiance_path: Path,
    *,
    manifest_mode: bool = False,
) -> dict[str, object]:
    """Validate fixed inside invariants and return the paired-cohort receipt.

    Historical mode retains the accepted Goal 012 paired and quadrant guards.
    Corrected manifest mode keeps the unchanged inside-series invariants but
    derives paired and quadrant counts from the supplied risk table.
    """
    if len(trends) != 4426 or trends["pa_id"].nunique() != 4426:
        raise ValueError(f"Expected 4,426 accepted inside trend rows, found {len(trends):,}.")
    if int(trends["slope_inside"].eq(0).sum()) != 3969:
        raise ValueError("Accepted inside trend zero-slope count is not 3,969.")
    if int(trends["slope_inside"].gt(0).sum()) != 420:
        raise ValueError("Accepted inside trend positive-slope count is not 420.")
    if risk["pa_id"].duplicated().any():
        raise ValueError("Risk table contains duplicate pa_id values.")
    if not manifest_mode and (len(risk) != 3858 or risk["pa_id"].nunique() != 3858):
        raise ValueError(f"Expected 3,858 accepted paired rows, found {len(risk):,}.")
    x, y = risk["slope_buffer_1km"], risk["slope_inside"]
    if x.isna().any() or y.isna().any():
        raise ValueError("Risk table contains unavailable slopes in the paired cohort.")
    quadrant_counts = [
        int(((x > 0) & (y > 0)).sum()),
        int(((x <= 0) & (y > 0)).sum()),
        int(((x <= 0) & (y <= 0)).sum()),
        int(((x > 0) & (y <= 0)).sum()),
    ]
    if not manifest_mode and quadrant_counts != [305, 55, 3308, 190]:
        raise ValueError(f"Accepted quadrant counts changed: {quadrant_counts}.")
    breakdown, late_positive = _zero_slope_breakdown(trends, radiance_path)
    if breakdown != {"All annual values zero": 3786, "Constant non-zero": 3, "Varying": 180}:
        raise ValueError(f"Accepted zero-slope annual-series breakdown changed: {breakdown}.")
    if late_positive != 78:
        raise ValueError(f"Accepted late-positive zero-slope count changed: {late_positive}.")
    return {
        "inside_rows": int(len(trends)),
        "inside_positive": int(trends["slope_inside"].gt(0).sum()),
        "inside_zero": int(trends["slope_inside"].eq(0).sum()),
        "zero_slope_late_positive": int(late_positive),
        "paired_rows": int(len(risk)),
        "quadrant_counts": dict(zip(("Q1", "Q2", "Q3", "Q4"), quadrant_counts)),
    }


def plot_trend_distribution(
    trends: pd.DataFrame, output_path: Path, *, radiance_path: Path | None = None
) -> Path:
    """Draw the full slope sign mass and non-zero tails without clipping."""
    import matplotlib.pyplot as plt

    slopes = pd.to_numeric(trends["slope_inside"], errors="coerce").dropna().to_numpy()
    if slopes.size == 0:
        raise ValueError("Trend distribution requires at least one finite slope.")
    if not np.isfinite(slopes).all():
        raise ValueError("Trend distribution contains non-finite slopes.")
    negative = int((slopes < 0).sum())
    zero = int((slopes == 0).sum())
    positive = int((slopes > 0).sum())

    if radiance_path is not None:
        fig = plt.figure(figsize=(7.5, 6.2), constrained_layout=True)
        grid = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.25])
        axes = [fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[1, :]), fig.add_subplot(grid[0, 1])]
    else:
        fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5), constrained_layout=True)
    sign_labels = ["Negative", "Exactly zero", "Positive"]
    sign_counts = [negative, zero, positive]
    bars = axes[0].bar(sign_labels, sign_counts, color=["#4C72B0", "#BDBDBD", "#C44E52"])
    axes[0].set_ylabel("Protected-area count")
    axes[0].set_title("Slope sign counts")
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].bar_label(bars, fmt="%d", padding=3)
    axes[0].set_ylim(0, max(sign_counts) * 1.18 if sign_counts else 1)

    nonzero = slopes[slopes != 0]
    if nonzero.size:
        # Symmetric bins retain the full negative and positive tails while the
        # exact-zero mass is represented explicitly in the left panel.
        max_abs = float(np.max(np.abs(nonzero)))
        edges = np.linspace(-max_abs, max_abs, 31)
        axes[1].hist(nonzero, bins=edges, color="#DD8452", alpha=0.88, edgecolor="white")
        axes[1].axvline(0, color="black", linewidth=0.8)
        axes[1].set_xlim(-max_abs, max_abs)
    axes[1].set_xlabel("Inside slope (scaled product units/yr)")
    axes[1].set_ylabel("Protected-area count")
    axes[1].set_title(f"Non-zero slopes (n={len(nonzero):,}; full range shown)")
    if radiance_path is not None:
        breakdown, late_positive = _zero_slope_breakdown(trends, radiance_path)
        labels = ["Zero\nthroughout", "Constant\npositive", "Varying"]
        values = list(breakdown.values())
        bars = axes[2].bar(labels, values, color=["#BDBDBD", "#969696", "#DD8452"])
        axes[2].bar_label(bars, fmt="%d", padding=3)
        axes[2].set_ylim(0, max(values) * 1.18 if values else 1)
        axes[2].set_ylabel("Protected-area count")
        axes[2].set_title(f"Exact-zero slopes (n={zero:,})")
        axes[2].tick_params(axis="x", rotation=0)
        axes[2].text(
            0.98,
            0.98,
            f"Late positive after 2021: {late_positive}\n(subset of varying)",
            transform=axes[2].transAxes,
            ha="right",
            va="top",
            fontsize=8,
            bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
        )
    fig.suptitle(f"Inside-protected-area trends (n={len(slopes):,})")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def _extract_report_section(report: str, heading: str) -> str:
    marker = f"## {heading}"
    start = report.find(marker)
    if start < 0:
        raise ValueError(f"Missing modelling-report section: {heading}")
    rest = report[start + len(marker) :]
    next_heading = rest.find("\n## ")
    return rest if next_heading < 0 else rest[:next_heading]


def _parse_coefficient_table(section: str, *, section_name: str) -> dict[str, tuple[float, float]]:
    match = re.search(
        r"### Coefficients \(log-odds\)\s+feature\s+mean_log_odds\s+std_log_odds\s+"
        r"odds_ratio\s+ci95_low\s+ci95_high\s+(.*?)(?=\n### |\n## |\Z)",
        section,
        flags=re.S,
    )
    if not match:
        raise ValueError(f"Missing strict coefficient table in section: {section_name}")
    rows: dict[str, tuple[float, float]] = {}
    for line in match.group(1).splitlines():
        fields = line.split()
        if not fields:
            continue
        if len(fields) != 6 or fields[0] not in {"any_light", "log1p_alan"}:
            raise ValueError(f"Unexpected coefficient row in {section_name!r}: {line!r}")
        rows[fields[0]] = (float(fields[1]), float(fields[2]))
    if set(rows) != {"any_light", "log1p_alan"}:
        raise ValueError(f"Coefficient table in {section_name!r} did not contain both features.")
    return rows


def _parse_auc(section: str, *, section_name: str) -> float:
    match = re.search(r"\n(?:run|primary|shuffled|ibra_shuffled|sensitivity)\s+([0-9]+\.[0-9]+)", section)
    if not match:
        # The primary table has a row label of 'primary' under a header; the
        # generic pattern above is intentionally strict about a numeric AUC.
        raise ValueError(f"Missing AUC in modelling-report section: {section_name}")
    return float(match.group(1))


def parse_layerb_report(path: Path) -> list[dict[str, object]]:
    """Parse the tracked report and return means, fold SDs, and AUCs."""
    report = path.read_text(encoding="utf-8")
    sections = [
        ("Primary (provider-matched) results", "Provider-matched association"),
        ("Falsification (ALAN shuffled within blocks)", "Block-shuffle benchmark"),
        ("Falsification (ALAN shuffled within IBRA × year)", "IBRA × year shuffle benchmark"),
        ("Sensitivity (multi-provider)", "Multi-provider sensitivity"),
    ]
    rows = []
    for heading, label in sections:
        section = _extract_report_section(report, heading)
        coeffs = _parse_coefficient_table(section, section_name=heading)
        auc = _parse_auc(section, section_name=heading)
        rows.append({"label": label, "auc": auc, "coefficients": coeffs})
    return rows


def plot_layerb_effects(results: list[dict[str, object]], output_path: Path) -> Path:
    import matplotlib.pyplot as plt

    labels = [str(row["label"]) for row in results]
    y = np.arange(len(labels))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
    features = [
        ("any_light", "Detectable ALAN (any_light)"),
        ("log1p_alan", "ALAN intensity when detected (log1p(ALAN))"),
    ]
    for ax, (feature, title) in zip(axes, features):
        means = np.array([float(row["coefficients"][feature][0]) for row in results])
        sds = np.array([float(row["coefficients"][feature][1]) for row in results])
        ax.errorbar(means, y, xerr=sds, fmt="o", color="#2C5F85", ecolor="#6E8FA8", capsize=3)
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_title(title)
        ax.set_xlabel("Mean log-odds coefficient ±1 SD across folds")
        ax.grid(axis="x", alpha=0.2)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([f"{label}\nAUC {float(row['auc']):.3f}" for label, row in zip(labels, results)], fontsize=8)
    axes[1].tick_params(axis="y", left=False, labelleft=False)
    fig.suptitle("Occurrence-record association and neutral ALAN benchmarks")
    fig.text(0.5, 0.01, "Bars show fold variability (±1 SD); AUC values are held-out discrimination summaries.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_bootstrap_forest(summary_path: Path, geometry_csv: Path | None, output_path: Path, *, top_n: int = 20) -> Path:
    import matplotlib.pyplot as plt

    summary = pd.read_csv(summary_path)
    needed = {"pa_id", "slope_median", "slope_ci_low", "slope_ci_high"}
    if not needed.issubset(summary.columns):
        raise ValueError(f"Bootstrap summary missing columns: {sorted(needed - set(summary.columns))}")
    df = summary.dropna(subset=list(needed)).sort_values("slope_median", ascending=False).head(top_n).copy()
    if df.empty:
        raise ValueError("No bootstrap rows available for sensitivity forest.")
    if geometry_csv and geometry_csv.exists():
        geoms = pd.read_csv(geometry_csv)[["pa_id", "NAME", "STATE"]]
        df = df.merge(geoms, on="pa_id", how="left")
    labels = [
        f"{row.NAME} ({row.STATE})" if pd.notna(getattr(row, "NAME", np.nan)) else str(row.pa_id)
        for row in df.itertuples(index=False)
    ]
    y = np.arange(len(df))
    fig, ax = plt.subplots(figsize=(9, 0.35 * len(df) + 1.7))
    ax.hlines(y, df["slope_ci_low"], df["slope_ci_high"], color="#3B6EA5", lw=2)
    ax.scatter(df["slope_median"], y, color="#1F4E79", zorder=3)
    ax.axvline(0, color="black", lw=0.8, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Inside mean radiance slope (scaled product units/yr)")
    ax.set_title(f"Top {len(df)} areas: temporal-resampling sensitivity")
    ax.text(0.99, 0.01, "Lines: 2.5th–97.5th percentile range across resampling draws", transform=ax.transAxes, ha="right", va="bottom", fontsize=8)
    ax.invert_yaxis()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


def plot_trajectories(
    radiance_path: Path,
    trends: pd.DataFrame,
    output_path: Path,
    *,
    q3_pa_id: str = "ACT_03",
) -> Path:
    import matplotlib.pyplot as plt

    selected = dict(TRAJECTORIES)
    if q3_pa_id != "ACT_03":
        selected.pop("ACT_03")
        selected[q3_pa_id] = q3_pa_id
    selected_ids = list(selected)
    radiance = pd.read_csv(radiance_path)
    required = {"pa_id", "year", "zone", "buffer_type", "buffer_km", "mean", "valid_pixel_count"}
    if not required.issubset(radiance.columns):
        raise ValueError(f"Radiance table missing columns: {sorted(required - set(radiance.columns))}")
    rows = trends.set_index("pa_id")
    missing = [pa_id for pa_id in selected_ids if pa_id not in rows.index]
    if missing:
        raise ValueError(f"Selected trajectory IDs absent from trend table: {missing}")
    fig, axes = plt.subplots(2, 2, figsize=(8.0, 6.2), sharex=True)
    label_changes: list[dict[str, object]] = []
    for ax, pa_id in zip(axes.ravel(), selected_ids):
        name = selected[pa_id]
        sub = radiance[radiance["pa_id"].astype(str) == pa_id].copy()
        sub = sub[sub["valid_pixel_count"] >= MIN_VALID_PIXELS]
        inside = sub[sub["zone"] == "inside"].sort_values("year")
        buffer = sub[(sub["zone"] == "buffer") & (sub["buffer_type"] == PRIMARY_BUFFER) & (sub["buffer_km"] == 1.0)].sort_values("year")
        if inside.empty or buffer.empty:
            raise ValueError(f"Selected trajectory {pa_id} lacks inside or 1 km buffer observations.")
        ax.plot(inside["year"], inside["mean"], marker="o", color="#1F4E79", label="Inside PA")
        ax.plot(buffer["year"], buffer["mean"], marker="o", color="#D95F02", label="Surrounding unprotected land (1 km)")
        row = rows.loc[pa_id]
        category = _quadrant_label(float(row.slope_buffer_1km), float(row.slope_inside))
        expected = TRAJECTORY_LABELS.get(pa_id)
        label_changes.append(
            {
                "pa_id": pa_id,
                "expected": expected,
                "actual": category,
                "changed": expected is not None and expected != category,
            }
        )
        ax.set_title(
            f"{name} ({pa_id.split('_')[0]}) — {category.replace(' slopes', '').replace(' slope', '')}\n"
            f"Inside {row.slope_inside:.3g}; surrounding {row.slope_buffer_1km:.3g}; "
            f"valid years {int(row.n_years_inside)} / {int(row.n_years_buffer_1km)}",
            fontsize=9,
            pad=7,
        )
        ax.set_ylabel("Mean radiance (scaled product units)", fontsize=8.5)
        ax.grid(alpha=0.2)
    for ax in axes[-1]:
        ax.set_xlabel("Year")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.945), ncol=2, frameon=False, fontsize=8.5)
    fig.suptitle("Illustrative inside and surrounding radiance trajectories", y=0.99, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.93), h_pad=1.2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    # The renderer reads this receipt through the return value rather than
    # encoding labels in the figure filename or mutating the source table.
    plot_trajectories.last_receipt = {"label_changes": label_changes}  # type: ignore[attr-defined]
    return output_path


def _quadrant_label(buffer_slope: float, inside_slope: float) -> str:
    if not np.isfinite(buffer_slope) or not np.isfinite(inside_slope):
        raise ValueError("Trajectory category requires finite inside and surrounding slopes.")
    if buffer_slope > 0 and inside_slope > 0:
        return "Q1: both slopes positive"
    if buffer_slope <= 0 and inside_slope > 0:
        return "Q2: inside only positive"
    if buffer_slope <= 0 and inside_slope <= 0:
        return "Q3: neither slope positive"
    return "Q4: surrounding only positive"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render accepted DSIPA outputs for RSEC co-author review.")
    parser.add_argument("--data-root", type=Path, required=True, help="Repository, data, or data/processed root containing accepted outputs.")
    parser.add_argument("--output-root", type=Path, required=True, help="Root under which manuscript/figures is written.")
    parser.add_argument("--q3-pa-id", default="ACT_03", help="Fixed Q3 trajectory exemplar (default: ACT_03).")
    parser.add_argument(
        "--input-manifest",
        type=Path,
        help="Explicit corrected-run manifest; validates every consumed input below --data-root.",
    )
    parser.add_argument(
        "--spatial-correction",
        action="store_true",
        help="Render corrected spatial outputs and require spatial_correction_summary.json.",
    )
    parser.add_argument(
        "--omit-layer-b",
        action="store_true",
        help="Render the active Layer A candidate without Layer B report or figure inputs.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    data_root = args.data_root.resolve()
    output_root = args.output_root.resolve()
    contract = None
    if args.input_manifest is not None:
        contract = _manifest_contract(
            data_root,
            args.input_manifest.resolve(),
            include_correction=args.spatial_correction,
            include_layer_b=not args.omit_layer_b,
        )
        trends_path = contract.files[TRENDS_NAME]
        radiance_path = contract.files[RADIANCE_NAME]
        risk_path = contract.files[RISK_NAME]
        geometry_csv = contract.files[GEOMETRY_CSV_NAME]
        geometry_gpkg = contract.files[GEOMETRY_GPKG_NAME]
        bootstrap_path = contract.files[BOOTSTRAP_NAME]
        report_path = contract.files.get(LAYERB_REPORT)
        trajectory_path = contract.files[EXAMPLE_SERIES_NAME]
        edge_profile_path = contract.files["pa_edge_profiles_national_v0_3_0.csv"]
        correction_summary_path = (
            contract.files[CORRECTION_SUMMARY_NAME] if args.spatial_correction else None
        )
    else:
        trends_path = _resolve(data_root, TRENDS_NAME)
        radiance_path = _resolve(data_root, RADIANCE_NAME)
        risk_path = _resolve(data_root, RISK_NAME)
        geometry_csv = _resolve(data_root, GEOMETRY_CSV_NAME)
        geometry_gpkg = _resolve(data_root, GEOMETRY_GPKG_NAME)
        bootstrap_path = _resolve(data_root, BOOTSTRAP_NAME)
        report_path = None if args.omit_layer_b else _resolve(data_root, LAYERB_REPORT)
        try:
            trajectory_path = _resolve(data_root, EXAMPLE_SERIES_NAME)
        except FileNotFoundError:
            trajectory_path = radiance_path
        edge_profile_path = _resolve(data_root, "pa_edge_profiles_national_v0_3_0.csv")
        correction_summary_path = (
            _resolve(data_root, CORRECTION_SUMMARY_NAME) if args.spatial_correction else None
        )
    figure_dir = output_root / FIGURE_DIR

    trends = _primary_trends(trends_path)
    risk = pd.read_csv(risk_path)
    receipt = _validate_accepted_evidence(
        trends, risk, radiance_path, manifest_mode=contract is not None
    )
    rendered = {
        "baseline_map": plot_baseline_map(
            data_root,
            output_root,
            radiance_path=radiance_path,
            geometry_path=geometry_gpkg,
        ),
        "trend_distribution": plot_trend_distribution(
            trends, figure_dir / TREND_FIG, radiance_path=radiance_path
        ),
        "retention_quadrant": figure_dir / QUADRANT_FIG,
        "example_trajectories": figure_dir / TRAJECTORY_FIG,
        "temporal_resampling_sensitivity": figure_dir / FOREST_FIG,
        "edge_profiles": figure_dir / Path(EDGE_FIG).name,
    }
    if not args.omit_layer_b:
        rendered["layerb_association"] = figure_dir / LAYERB_FIG
    write_quadrant_figure(risk, rendered["retention_quadrant"])
    plot_trajectories(trajectory_path, trends, rendered["example_trajectories"], q3_pa_id=args.q3_pa_id)
    if not args.omit_layer_b:
        if report_path is None:
            raise ValueError("Layer B report is required unless --omit-layer-b is set.")
        plot_layerb_effects(parse_layerb_report(report_path), rendered["layerb_association"])
    plot_bootstrap_forest(bootstrap_path, geometry_csv, rendered["temporal_resampling_sensitivity"])
    plot_edge_profiles(
        data_root,
        edge_profile_path=edge_profile_path,
        output_path=rendered["edge_profiles"],
    )
    input_paths = {
        "trends": trends_path,
        "radiance": radiance_path,
        "risk": risk_path,
        "geometry_csv": geometry_csv,
        "geometry_gpkg": geometry_gpkg,
        "bootstrap_summary": bootstrap_path,
        "edge_profiles": edge_profile_path,
    }
    if not args.omit_layer_b:
        if report_path is None:
            raise ValueError("Layer B report is required unless --omit-layer-b is set.")
        input_paths["layerb_report"] = report_path
    if trajectory_path != radiance_path:
        input_paths["trajectory_example_series"] = trajectory_path
    if correction_summary_path is not None:
        input_paths["spatial_correction_summary"] = correction_summary_path
    receipt["trajectory_label_changes"] = getattr(plot_trajectories, "last_receipt", {}).get(
        "label_changes", []
    )
    receipt["spatial_correction"] = bool(args.spatial_correction)
    receipt["omit_layer_b"] = bool(args.omit_layer_b)
    receipt["analysis_id"] = contract.analysis_id if contract is not None else "goal012-accepted"
    _write_render_manifest(
        output_root,
        inputs=input_paths,
        outputs=rendered,
        input_contract=contract,
        render_receipt=receipt,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

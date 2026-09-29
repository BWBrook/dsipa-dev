"""Generate Layer B figures (WP0.16)."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dsipa.paths import find_repo_root

MICROBATS_PATH = "data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz"
BIRDS_PATH = "data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz"

FIGURE_EXPOSURE = "manuscript/figures/fig_layerB_exposure_summary.png"
FIGURE_COUNTS = "manuscript/figures/fig_layerB_occurrence_counts.png"
FIGURE_DENSITY = "manuscript/figures/fig_layerB_occurrence_density.png"
EXPOSURE_JSON = "analysis/reports/layerB_exposure_qc.json"

STATE_ORDER = [
    ("Australian Capital Territory", "ACT"),
    ("New South Wales", "NSW"),
    ("Northern Territory", "NT"),
    ("Queensland", "QLD"),
    ("South Australia", "SA"),
    ("Tasmania", "TAS"),
    ("Victoria", "VIC"),
    ("Western Australia", "WA"),
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def plot_exposure_summary(root: Path) -> Path:
    exposure_path = root / EXPOSURE_JSON
    if not exposure_path.exists():
        raise FileNotFoundError(f"Missing exposure summary: {exposure_path}")

    data = json.loads(exposure_path.read_text(encoding="utf-8"))
    groups = [("microbats", "Microbats"), ("diurnal_birds", "Diurnal birds")]
    strata = [
        ("inside", "Inside PAs"),
        ("within_10km", "Within 10 km"),
        ("outside", "Outside 10 km"),
    ]

    x = np.arange(len(strata))
    width = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    colors = ["#4C72B0", "#DD8452"]

    for i, (group_key, label) in enumerate(groups):
        offset = (i - 0.5) * width
        zero_vals = [data[group_key][key]["zero_fraction"] for key, _ in strata]
        p95_vals = [data[group_key][key]["p95"] for key, _ in strata]
        axes[0].bar(x + offset, zero_vals, width, label=label, color=colors[i], alpha=0.85)
        axes[1].bar(x + offset, p95_vals, width, label=label, color=colors[i], alpha=0.85)

    labels = [label for _, label in strata]
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=15)
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("Zero fraction (ALAN = 0)")
    axes[0].set_title("Exposure zero mass")
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=15)
    axes[1].set_ylabel("ALAN p95 (scaled)")
    axes[1].set_title("Exposure p95 (scaled)")
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle("Layer B exposure summary (microbats vs diurnal birds)")
    fig.tight_layout()

    out_path = root / FIGURE_EXPOSURE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def _aggregate_counts(path: Path) -> tuple[dict[tuple[str, int], int], int]:
    counts: dict[tuple[str, int], int] = defaultdict(int)
    total = 0
    usecols = ["year", "stateProvince"]
    for chunk in pd.read_csv(path, usecols=usecols, chunksize=200_000):
        years = pd.to_numeric(chunk["year"], errors="coerce")
        states = chunk["stateProvince"].fillna("Unknown").astype(str)
        mask = years.notna()
        if not mask.any():
            continue
        chunk = chunk.loc[mask].copy()
        years = years.loc[mask].astype(int)
        total += len(chunk)
        grouped = (
            chunk.assign(year=years, state=states)
            .groupby(["state", "year"])
            .size()
        )
        for (state, year), count in grouped.items():
            counts[(state, int(year))] += int(count)
    return counts, total


def plot_occurrence_counts(root: Path) -> Path:
    micro_path = root / MICROBATS_PATH
    bird_path = root / BIRDS_PATH
    micro_counts, micro_total = _aggregate_counts(micro_path)
    bird_counts, bird_total = _aggregate_counts(bird_path)

    years = sorted(
        {year for (_, year) in micro_counts.keys()} | {year for (_, year) in bird_counts.keys()}
    )
    state_names = [name for name, _ in STATE_ORDER]
    state_labels = [code for _, code in STATE_ORDER]

    def build_matrix(counts: dict[tuple[str, int], int]) -> np.ndarray:
        mat = np.zeros((len(state_names), len(years)), dtype=float)
        for i, state in enumerate(state_names):
            for j, year in enumerate(years):
                mat[i, j] = counts.get((state, year), 0)
        return mat

    micro_mat = build_matrix(micro_counts)
    bird_mat = build_matrix(bird_counts)
    vmax = np.log10(max(micro_mat.max(), bird_mat.max()) + 1.0) if years else 1.0

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True, constrained_layout=True)
    for ax, mat, title, total in [
        (axes[0], micro_mat, f"Microbats (n={micro_total:,})", micro_total),
        (axes[1], bird_mat, f"Diurnal birds (n={bird_total:,})", bird_total),
    ]:
        im = ax.imshow(
            np.log10(mat + 1.0),
            aspect="auto",
            cmap="viridis",
            vmin=0,
            vmax=vmax,
            origin="upper",
        )
        ax.set_xticks(np.arange(len(years)))
        ax.set_xticklabels(years, rotation=45, fontsize=8)
        ax.set_yticks(np.arange(len(state_labels)))
        ax.set_yticklabels(state_labels, fontsize=8)
        ax.set_title(title)
        ax.set_xlabel("Year")

    axes[0].set_ylabel("State")
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.85, pad=0.02)
    cbar.set_label("log10(count + 1)")
    fig.suptitle("Layer B occurrences by year and state (filtered + deduped)")

    out_path = root / FIGURE_COUNTS
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def _reservoir_sample(path: Path, sample_n: int, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    rng = np.random.default_rng(seed)
    lons: list[float] = []
    lats: list[float] = []
    seen = 0
    usecols = ["decimalLongitude", "decimalLatitude"]
    for chunk in pd.read_csv(path, usecols=usecols, chunksize=200_000):
        lon = pd.to_numeric(chunk["decimalLongitude"], errors="coerce")
        lat = pd.to_numeric(chunk["decimalLatitude"], errors="coerce")
        mask = lon.notna() & lat.notna()
        if not mask.any():
            continue
        lon = lon[mask].to_numpy()
        lat = lat[mask].to_numpy()
        for x, y in zip(lon, lat):
            seen += 1
            if len(lons) < sample_n:
                lons.append(float(x))
                lats.append(float(y))
            else:
                j = rng.integers(0, seen)
                if j < sample_n:
                    lons[j] = float(x)
                    lats[j] = float(y)
    return np.array(lons), np.array(lats), seen


def plot_occurrence_density(root: Path) -> Path:
    micro_path = root / MICROBATS_PATH
    bird_path = root / BIRDS_PATH
    micro_lons, micro_lats, micro_total = _reservoir_sample(micro_path, sample_n=200_000, seed=42)
    bird_lons, bird_lats, bird_total = _reservoir_sample(bird_path, sample_n=300_000, seed=43)

    combined_lons = np.concatenate([micro_lons, bird_lons])
    combined_lats = np.concatenate([micro_lats, bird_lats])
    if len(combined_lons) == 0:
        raise RuntimeError("No coordinates available for density plot.")

    lon_min, lon_max = np.quantile(combined_lons, [0.005, 0.995])
    lat_min, lat_max = np.quantile(combined_lats, [0.005, 0.995])
    extent = (lon_min, lon_max, lat_min, lat_max)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True, sharey=True, constrained_layout=True)
    for ax, lons, lats, title in [
        (axes[0], micro_lons, micro_lats, f"Microbats (sample={len(micro_lons):,})"),
        (axes[1], bird_lons, bird_lats, f"Diurnal birds (sample={len(bird_lons):,})"),
    ]:
        hb = ax.hexbin(
            lons,
            lats,
            gridsize=60,
            cmap="magma",
            bins="log",
            mincnt=1,
            extent=extent,
        )
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        fig.colorbar(hb, ax=ax, shrink=0.85, pad=0.02)

    fig.suptitle("Layer B occurrence density (filtered + deduped)")

    out_path = root / FIGURE_DENSITY
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer B figures.")
    return parser


def main(argv: list[str] | None = None) -> int:
    _ = build_parser().parse_args(argv)
    root = find_repo_root()
    plot_exposure_summary(root)
    plot_occurrence_counts(root)
    plot_occurrence_density(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

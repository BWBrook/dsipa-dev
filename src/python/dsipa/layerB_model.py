"""Layer B modelling + falsification (WP0.16)."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from shapely import wkb
from shapely.geometry import Point
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import GroupKFold

from dsipa.layerB_data import normalize_columns
from dsipa.manifest import build_manifest, write_manifest
from dsipa.nightlights import CORE_YEARS, download_year
from dsipa.paths import find_repo_root
from dsipa.schema import LAYERB_MODEL_INPUT_SUMMARY_CSV, SCHEMA_VERSION


PA_UNION_CACHE = f"data/processed/cache/pa_union_v{SCHEMA_VERSION.replace('.', '_')}.wkb"


@dataclass
class DatasetResult:
    name: str
    df: pd.DataFrame
    summary: dict[str, object]


@dataclass
class ModelResult:
    name: str
    metrics: pd.DataFrame
    coefficients: pd.DataFrame


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _git_dirty(root: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:  # pragma: no cover
        return False
    return bool(result.stdout.strip())


def _ensure_clean_tree(root: Path, allow_dirty: bool) -> None:
    if allow_dirty:
        return
    if _git_dirty(root):
        raise SystemExit("Working tree is dirty; commit or use --allow-dirty to proceed.")


def _load_union(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing cached union geometry: {path}")
    return wkb.loads(path.read_bytes())


def _vectorized_contains(geom, xs: np.ndarray, ys: np.ndarray, points=None) -> np.ndarray:
    try:
        import shapely

        pts = points if points is not None else shapely.points(xs, ys)
        return shapely.contains(geom, pts)
    except Exception:
        from shapely.prepared import prep

        prepared = prep(geom)
        return np.array([prepared.contains(Point(x, y)) for x, y in zip(xs, ys)])


def _block_ids(x: np.ndarray, y: np.ndarray, block_km: float) -> np.ndarray:
    block_m = block_km * 1000.0
    bx = np.floor(x / block_m).astype(int)
    by = np.floor(y / block_m).astype(int)
    return np.char.add(np.char.add(bx.astype(str), "_"), by.astype(str))


class ReservoirSampler:
    def __init__(self, n: int | None, rng: np.random.Generator) -> None:
        self.n = n
        self.rng = rng
        self.items: list[dict[str, object]] = []
        self.seen = 0

    def add(self, item: dict[str, object]) -> None:
        self.seen += 1
        if self.n is None:
            self.items.append(item)
            return
        if len(self.items) < self.n:
            self.items.append(item)
            return
        idx = self.rng.integers(0, self.seen)
        if idx < self.n:
            self.items[idx] = item

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.items)


def _iter_occurrence_chunks(path: Path, chunksize: int = 200_000) -> Iterable[pd.DataFrame]:
    reader = pd.read_csv(path, dtype=str, compression="gzip", chunksize=chunksize)
    for chunk in reader:
        yield normalize_columns(chunk)


def _sample_raster(dataset, lons: np.ndarray, lats: np.ndarray) -> np.ndarray:
    coords = list(zip(lons, lats))
    values = np.array([val[0] for val in dataset.sample(coords)], dtype=float)
    scale = dataset.scales[0] if dataset.scales else None
    offset = dataset.offsets[0] if dataset.offsets else None
    scale_value = 1.0 if scale is None else float(scale)
    offset_value = 0.0 if offset is None else float(offset)
    values = values * scale_value + offset_value
    nodata = dataset.nodata
    if nodata is not None:
        values = np.where(values == nodata, np.nan, values)
    return values


def _collect_features(
    *,
    path: Path,
    group: str,
    provider_filter: str | None,
    pa_union,
    buffer_km: float,
    block_km: float,
    nightlights_dir: Path,
    seed: int,
    sample_n: int | None,
    sample_rate: float,
    simplify_m: float,
) -> DatasetResult:
    rng = np.random.default_rng(seed)
    sampler = ReservoirSampler(sample_n, rng)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
    pa_union_s = pa_union.simplify(simplify_m, preserve_topology=True) if simplify_m > 0 else pa_union
    pa_buffer = pa_union_s.buffer(buffer_km * 1000.0)

    total = 0
    providers = set()

    if not 0 < sample_rate <= 1:
        raise ValueError("sample_rate must be within (0, 1].")

    for chunk in _iter_occurrence_chunks(path):
        if provider_filter is not None and "dataResourceUid" in chunk.columns:
            chunk = chunk[chunk["dataResourceUid"] == provider_filter]

        chunk["decimalLatitude"] = pd.to_numeric(chunk["decimalLatitude"], errors="coerce")
        chunk["decimalLongitude"] = pd.to_numeric(chunk["decimalLongitude"], errors="coerce")
        chunk = chunk.dropna(subset=["decimalLatitude", "decimalLongitude", "year"])

        total += len(chunk)
        if chunk.empty:
            continue

        years_arr = pd.to_numeric(chunk["year"], errors="coerce").astype("Int64")
        valid_years = years_arr.notna() & years_arr.isin(list(CORE_YEARS))
        chunk = chunk.loc[valid_years].copy()
        years_arr = years_arr.loc[valid_years].astype(int).to_numpy()
        if chunk.empty:
            continue

        if sample_rate < 1.0:
            keep = rng.random(len(chunk)) < sample_rate
            if not keep.any():
                continue
            chunk = chunk.loc[keep].copy()
            years_arr = years_arr[keep]

        lons = chunk["decimalLongitude"].to_numpy()
        lats = chunk["decimalLatitude"].to_numpy()
        x, y = transformer.transform(lons, lats)
        try:
            import shapely

            points = shapely.points(x, y)
        except Exception:
            points = None
        inside_mask = _vectorized_contains(pa_union_s, x, y, points=points)
        within_mask = _vectorized_contains(pa_buffer, x, y, points=points) & ~inside_mask

        scope_mask = inside_mask | within_mask
        if not scope_mask.any():
            continue

        chunk = chunk.loc[scope_mask].copy()
        lons = lons[scope_mask]
        lats = lats[scope_mask]
        x = x[scope_mask]
        y = y[scope_mask]
        years_arr = years_arr[scope_mask]
        inside_mask = inside_mask[scope_mask]

        if "dataResourceUid" in chunk.columns:
            provider_vals = chunk["dataResourceUid"].astype(str).to_numpy()
        else:
            provider_vals = np.array(["unknown"] * len(chunk))

        for i in range(len(years_arr)):
            record = {
                "group": group,
                "year": int(years_arr[i]),
                "lon": float(lons[i]),
                "lat": float(lats[i]),
                "x": float(x[i]),
                "y": float(y[i]),
                "stratum": "inside" if inside_mask[i] else "within_10km",
                "provider": str(provider_vals[i]),
            }
            sampler.add(record)

        providers.update(set(provider_vals))

    df = sampler.to_frame()
    if df.empty:
        raise RuntimeError(f"No records retained for {group} (provider={provider_filter}).")

    df["block_id"] = _block_ids(df["x"].to_numpy(), df["y"].to_numpy(), block_km)
    df["alan"] = np.nan
    raster_cache: dict[int, rasterio.DatasetReader] = {}
    for year in sorted(df["year"].unique()):
        idx = df["year"] == year
        if not idx.any():
            continue
        if year not in raster_cache:
            raster = download_year(year, nightlights_dir)
            raster_cache[year] = rasterio.open(raster.path)
        values = _sample_raster(raster_cache[year], df.loc[idx, "lon"], df.loc[idx, "lat"])
        df.loc[idx, "alan"] = values

    for dataset in raster_cache.values():
        dataset.close()

    df = df[np.isfinite(df["alan"])].copy()
    df["any_light"] = (df["alan"] > 0).astype(int)
    df["log1p_alan"] = np.where(df["alan"] > 0, np.log1p(df["alan"]), 0.0)
    df = df[
        [
            "group",
            "year",
            "alan",
            "any_light",
            "log1p_alan",
            "stratum",
            "block_id",
            "provider",
        ]
    ]

    inside_fraction = (df["stratum"] == "inside").mean() if len(df) else np.nan
    within_fraction = (df["stratum"] == "within_10km").mean() if len(df) else np.nan
    zero_fraction = (df["alan"] == 0).mean() if len(df) else np.nan
    summary = {
        "group": group,
        "provider_filter": provider_filter or "all",
        "records_retained": len(df),
        "records_seen": total,
        "inside_fraction": inside_fraction,
        "within_fraction": within_fraction,
        "zero_fraction": zero_fraction,
        "years_min": int(df["year"].min()) if len(df) else np.nan,
        "years_max": int(df["year"].max()) if len(df) else np.nan,
        "providers_included": ",".join(sorted(providers)) if providers else "unknown",
    }
    return DatasetResult(name=f"{group}_{provider_filter or 'all'}", df=df, summary=summary)


def _balanced_sample(df_a: pd.DataFrame, df_b: pd.DataFrame, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    n = min(len(df_a), len(df_b))
    if len(df_a) > n:
        df_a = df_a.sample(n=n, random_state=seed)
    if len(df_b) > n:
        df_b = df_b.sample(n=n, random_state=seed + 1)
    return df_a, df_b


def _run_model(
    df: pd.DataFrame,
    *,
    name: str,
    block_km: float,
    seed: int,
) -> ModelResult:
    features = ["any_light", "log1p_alan"]
    X = df[features].to_numpy()
    y = (df["group"] == "microbats").astype(int).to_numpy()
    groups = df["block_id"].to_numpy()

    unique_blocks = np.unique(groups)
    n_splits = min(5, len(unique_blocks))
    if n_splits < 3:
        raise RuntimeError("Insufficient spatial blocks for cross-validation.")

    cv = GroupKFold(n_splits=n_splits)
    metrics = []
    coeffs = []
    for fold, (train_idx, test_idx) in enumerate(cv.split(X, y, groups=groups), start=1):
        model = LogisticRegression(max_iter=200, solver="liblinear")
        model.fit(X[train_idx], y[train_idx])
        probs = model.predict_proba(X[test_idx])[:, 1]
        y_test = y[test_idx]

        auc = roc_auc_score(y_test, probs) if len(np.unique(y_test)) > 1 else np.nan
        loss = log_loss(y_test, probs, labels=[0, 1])
        metrics.append({"run": name, "fold": fold, "auc": auc, "log_loss": loss})
        coeffs.append(
            {
                "run": name,
                "fold": fold,
                "intercept": model.intercept_[0],
                "any_light": model.coef_[0][0],
                "log1p_alan": model.coef_[0][1],
            }
        )

    metrics_df = pd.DataFrame(metrics)
    coeffs_df = pd.DataFrame(coeffs)
    return ModelResult(name=name, metrics=metrics_df, coefficients=coeffs_df)


def _summarize_coefficients(coeffs: pd.DataFrame) -> pd.DataFrame:
    summary = []
    for feature in ["any_light", "log1p_alan"]:
        values = coeffs[feature].to_numpy()
        mean = np.nanmean(values)
        std = np.nanstd(values, ddof=1) if len(values) > 1 else np.nan
        summary.append(
            {
                "feature": feature,
                "mean_log_odds": mean,
                "std_log_odds": std,
                "odds_ratio": math.exp(mean) if math.isfinite(mean) else np.nan,
                "ci95_low": mean - 1.96 * std if math.isfinite(std) else np.nan,
                "ci95_high": mean + 1.96 * std if math.isfinite(std) else np.nan,
            }
        )
    return pd.DataFrame(summary)


def _shuffle_within_blocks(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = df.copy()
    shuffled = []
    for _, block_df in df.groupby("block_id"):
        alan_vals = block_df["alan"].to_numpy()
        rng.shuffle(alan_vals)
        block_df = block_df.copy()
        block_df["alan"] = alan_vals
        block_df["any_light"] = (alan_vals > 0).astype(int)
        block_df["log1p_alan"] = np.where(alan_vals > 0, np.log1p(alan_vals), 0.0)
        shuffled.append(block_df)
    return pd.concat(shuffled, ignore_index=True)


def write_model_report(
    *,
    path: Path,
    primary: ModelResult,
    primary_summary: pd.DataFrame,
    primary_metrics: pd.DataFrame,
    shuffle: ModelResult,
    shuffle_summary: pd.DataFrame,
    shuffle_metrics: pd.DataFrame,
    sensitivity: ModelResult,
    sensitivity_summary: pd.DataFrame,
    sensitivity_metrics: pd.DataFrame,
    input_summary: pd.DataFrame,
    block_km: float,
    provider: str,
    sensitivity_sample_rate: float,
) -> None:
    n_folds = int(primary_metrics["fold"].nunique())
    lines = [
        "# Layer B modelling report (WP0.16)",
        "",
        f"Generated: {_now_utc()}",
        "",
        "## Primary design",
        f"- Provider-matched: {provider}",
        f"- Spatial blocking: {block_km:.0f} km",
        f"- Evaluation: GroupKFold ({n_folds} folds) on spatial blocks",
        "- Response: microbats (1) vs passerines (0) case-control classification",
        "- Control design: passerines as target-group background (provider-matched)",
        "- ALAN covariates: any_light indicator + log1p(ALAN) conditional on >0",
        "- Scope: records inside protected areas or within 10 km buffers",
        f"- Sensitivity birds sample rate: {sensitivity_sample_rate:.2f}",
        "",
        "## Model input summary",
        input_summary.to_string(index=False),
        "",
        "## Primary (provider-matched) results",
        "### Coefficients (log-odds)",
        primary_summary.to_string(index=False),
        "",
        "### Cross-validated metrics",
        primary_metrics.groupby("run")[["auc", "log_loss"]].mean().to_string(),
        "",
        "## Falsification (ALAN shuffled within blocks)",
        "### Coefficients (log-odds)",
        shuffle_summary.to_string(index=False),
        "",
        "### Cross-validated metrics",
        shuffle_metrics.groupby("run")[["auc", "log_loss"]].mean().to_string(),
        "",
        "## Sensitivity (multi-provider)",
        "### Coefficients (log-odds)",
        sensitivity_summary.to_string(index=False),
        "",
        "### Cross-validated metrics",
        sensitivity_metrics.groupby("run")[["auc", "log_loss"]].mean().to_string(),
        "",
        "## Interpretation (what we can/can't conclude)",
        "- This is a provider-matched, spatially blocked presence-only case-control signal test (not a population trend).",
        "- The ALAN two-part covariates reduce sensor-floor dominance; inference is limited to relative differences between microbats and passerines within dr368.",
        "- If shuffled ALAN retains similar coefficients or predictive performance, the model is capturing sampling bias rather than an ALAN-linked signal.",
        "- Sensitivity results on the multi-provider dataset are descriptive only and should not be used for primary inference.",
        "- Any effect should be interpreted as an association in occurrence records, not causal impact.",
        "",
    ]
    if sensitivity_sample_rate < 1.0:
        lines.extend(
            [
                "Note:",
                "- The sensitivity run uses a random subsample of passerine records for runtime feasibility.",
                "- Microbats use the full filtered dataset; passerines are subsampled to match scale.",
                "- Full multi-provider reruns should use --sensitivity-sample-rate 1.0 when resources permit.",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_input_summary(path: Path, rows: list[dict[str, object]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def write_figure(
    path: Path,
    primary: pd.DataFrame,
    shuffle: pd.DataFrame,
    sensitivity: pd.DataFrame,
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    x_positions = {"any_light": 0, "log1p_alan": 1}
    offsets = {"primary": -0.2, "shuffled": 0.0, "sensitivity": 0.2}
    styles = {
        "primary": {"color": "#1b9e77", "label": "Primary (dr368)"},
        "shuffled": {"color": "#d95f02", "label": "Shuffled ALAN"},
        "sensitivity": {"color": "#7570b3", "label": "Sensitivity (all providers)"},
    }

    for name, df in [("primary", primary), ("shuffled", shuffle), ("sensitivity", sensitivity)]:
        for _, row in df.iterrows():
            x = x_positions[row["feature"]] + offsets[name]
            ax.errorbar(
                x,
                row["mean_log_odds"],
                yerr=[[row["mean_log_odds"] - row["ci95_low"]], [row["ci95_high"] - row["mean_log_odds"]]],
                fmt="o",
                color=styles[name]["color"],
                label=styles[name]["label"] if row["feature"] == "any_light" else None,
            )

    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["any_light", "log1p_alan"])
    ax.set_ylabel("Log-odds coefficient (microbats vs passerines)")
    ax.set_title("Layer B ALAN effects (provider-matched primary + falsification)")
    ax.legend(frameon=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Layer B modelling (WP0.16).")
    parser.add_argument(
        "--microbats-path",
        default="data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz",
    )
    parser.add_argument(
        "--birds-path",
        default="data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz",
    )
    parser.add_argument("--provider", default="dr368", help="Provider UID for primary run.")
    parser.add_argument("--block-km", type=float, default=50.0)
    parser.add_argument("--buffer-km", type=float, default=10.0)
    parser.add_argument("--simplify-m", type=float, default=1000.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--sensitivity-sample-rate",
        type=float,
        default=1.0,
        help="Random subsample rate for sensitivity runs (0-1].",
    )
    parser.add_argument(
        "--nightlights-dir",
        default="data/raw/nightlights_zenodo_v0_4",
        help="Directory for nightlights rasters.",
    )
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    parser.add_argument(
        "--artefact-only",
        action="store_true",
        help="Only (re)write artefact/manifest from existing outputs.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow artefact generation with a dirty git tree.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    report_path = root / "analysis" / "reports" / "layerB_modelling_report.md"
    figure_path = root / "manuscript" / "figures" / "fig_layerB_alan_effects.png"
    summary_path = root / LAYERB_MODEL_INPUT_SUMMARY_CSV

    if args.artefact_only:
        if not args.skip_artefact:
            _ensure_clean_tree(root, args.allow_dirty)
            artefact_dir = root / "artefacts" / "wp0_16_layerB_modelling"
            artefact_dir.mkdir(parents=True, exist_ok=True)
            for path in (report_path, figure_path, summary_path):
                if path.exists():
                    shutil.copyfile(path, artefact_dir / path.name)
            manifest = build_manifest(
                run_id="wp0_16_layerB_modelling",
                wp="WP0.16",
                root=root,
                outputs=[report_path.name, figure_path.name, summary_path.name],
                inputs=["Atlas of Living Australia", "CAPAD 2024", "Zenodo nightlights v0.4"],
                require_clean=True,
                notes="WP0.16 Layer B modelling artefact",
            )
            write_manifest(artefact_dir / "MANIFEST.json", manifest)
            (artefact_dir / "README.txt").write_text(
                "WP0.16 Layer B modelling artefact.\n", encoding="utf-8"
            )
        return 0

    pa_union = _load_union(root / PA_UNION_CACHE)
    microbats_path = root / args.microbats_path
    birds_path = root / args.birds_path
    nightlights_dir = root / args.nightlights_dir

    micro_primary = _collect_features(
        path=microbats_path,
        group="microbats",
        provider_filter=args.provider,
        pa_union=pa_union,
        buffer_km=args.buffer_km,
        block_km=args.block_km,
        nightlights_dir=nightlights_dir,
        seed=args.seed,
        sample_n=None,
        sample_rate=1.0,
        simplify_m=args.simplify_m,
    )
    birds_primary = _collect_features(
        path=birds_path,
        group="diurnal_birds",
        provider_filter=args.provider,
        pa_union=pa_union,
        buffer_km=args.buffer_km,
        block_km=args.block_km,
        nightlights_dir=nightlights_dir,
        seed=args.seed + 1,
        sample_n=len(micro_primary.df),
        sample_rate=1.0,
        simplify_m=args.simplify_m,
    )
    micro_primary.df, birds_primary.df = _balanced_sample(
        micro_primary.df, birds_primary.df, args.seed
    )
    primary_df = pd.concat([micro_primary.df, birds_primary.df], ignore_index=True)

    micro_sens = _collect_features(
        path=microbats_path,
        group="microbats",
        provider_filter=None,
        pa_union=pa_union,
        buffer_km=args.buffer_km,
        block_km=args.block_km,
        nightlights_dir=nightlights_dir,
        seed=args.seed + 2,
        sample_n=None,
        sample_rate=1.0,
        simplify_m=args.simplify_m,
    )
    birds_sens = _collect_features(
        path=birds_path,
        group="diurnal_birds",
        provider_filter=None,
        pa_union=pa_union,
        buffer_km=args.buffer_km,
        block_km=args.block_km,
        nightlights_dir=nightlights_dir,
        seed=args.seed + 3,
        sample_n=len(micro_sens.df),
        sample_rate=args.sensitivity_sample_rate,
        simplify_m=args.simplify_m,
    )
    micro_sens.df, birds_sens.df = _balanced_sample(micro_sens.df, birds_sens.df, args.seed + 3)
    sens_df = pd.concat([micro_sens.df, birds_sens.df], ignore_index=True)

    primary = _run_model(primary_df, name="primary", block_km=args.block_km, seed=args.seed)
    shuffled_df = _shuffle_within_blocks(primary_df, args.seed + 9)
    shuffle = _run_model(shuffled_df, name="shuffled", block_km=args.block_km, seed=args.seed)
    sensitivity = _run_model(sens_df, name="sensitivity", block_km=args.block_km, seed=args.seed)

    primary_summary = _summarize_coefficients(primary.coefficients)
    shuffle_summary = _summarize_coefficients(shuffle.coefficients)
    sensitivity_summary = _summarize_coefficients(sensitivity.coefficients)

    input_rows = []
    for run_name, dataset, sample_rate in [
        ("primary_dr368", micro_primary.df, 1.0),
        ("primary_dr368", birds_primary.df, 1.0),
        ("sensitivity_all", micro_sens.df, 1.0),
        ("sensitivity_all", birds_sens.df, args.sensitivity_sample_rate),
    ]:
        input_rows.append(
            {
                "schema_version": SCHEMA_VERSION,
                "run": run_name,
                "group": dataset["group"].iloc[0],
                "n_records": len(dataset),
                "providers": ",".join(sorted(dataset["provider"].unique())),
                "years_min": int(dataset["year"].min()),
                "years_max": int(dataset["year"].max()),
                "inside_fraction": (dataset["stratum"] == "inside").mean(),
                "within_fraction": (dataset["stratum"] == "within_10km").mean(),
                "zero_fraction": (dataset["alan"] == 0).mean(),
                "block_km": args.block_km,
                "buffer_km": args.buffer_km,
                "sample_rate": sample_rate,
            }
        )
    input_summary = write_input_summary(summary_path, input_rows)

    write_model_report(
        path=report_path,
        primary=primary,
        primary_summary=primary_summary,
        primary_metrics=primary.metrics,
        shuffle=shuffle,
        shuffle_summary=shuffle_summary,
        shuffle_metrics=shuffle.metrics,
        sensitivity=sensitivity,
        sensitivity_summary=sensitivity_summary,
        sensitivity_metrics=sensitivity.metrics,
        input_summary=input_summary,
        block_km=args.block_km,
        provider=args.provider,
        sensitivity_sample_rate=args.sensitivity_sample_rate,
    )

    write_figure(figure_path, primary_summary, shuffle_summary, sensitivity_summary)

    if not args.skip_artefact:
        _ensure_clean_tree(root, args.allow_dirty)
        artefact_dir = root / "artefacts" / "wp0_16_layerB_modelling"
        artefact_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(report_path, artefact_dir / report_path.name)
        shutil.copyfile(figure_path, artefact_dir / figure_path.name)
        shutil.copyfile(summary_path, artefact_dir / summary_path.name)
        manifest = build_manifest(
            run_id="wp0_16_layerB_modelling",
            wp="WP0.16",
            root=root,
            outputs=[report_path.name, figure_path.name, summary_path.name],
            inputs=["Atlas of Living Australia", "CAPAD 2024", "Zenodo nightlights v0.4"],
            require_clean=True,
            notes="WP0.16 Layer B modelling artefact",
        )
        write_manifest(artefact_dir / "MANIFEST.json", manifest)
        (artefact_dir / "README.txt").write_text(
            "WP0.16 Layer B modelling artefact.\n", encoding="utf-8"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

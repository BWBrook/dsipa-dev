"""Layer A sanity dashboard (WP0.10b)."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import EDGE_PROFILES_NATIONAL_CSV, PA_GEOMETRIES_GPKG, RADIANCE_BUFFERS_NATIONAL_CSV
from dsipa.triad import CITY_POINTS

try:
    from shapely import make_valid
except ImportError:  # pragma: no cover
    from shapely.validation import make_valid  # type: ignore

REPORT_PATH = "analysis/reports/layerA_sanity_dashboard.md"
PLOT_PATH = "analysis/reports/layerA_sensitivity_mean_vs_median.png"

MIN_VALID_PIXELS = 10
ALT_VALID_PIXELS = 50


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _build_city_gdf() -> gpd.GeoDataFrame:
    rows = [(name, Point(lon, lat)) for name, lon, lat in CITY_POINTS]
    return gpd.GeoDataFrame(rows, columns=["city", "geometry"], crs="EPSG:4326").to_crs("EPSG:3577")


def _assign_distance_band(distance_km: float) -> str:
    if distance_km <= 20.0:
        return "urban_0_20km"
    if distance_km <= 100.0:
        return "peri_20_100km"
    if distance_km >= 300.0:
        return "remote_300km_plus"
    return "mid_100_300km"


def _assign_area_quartiles(area_km2: pd.Series) -> pd.Series:
    try:
        return pd.qcut(area_km2, q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    except ValueError:
        ranked = area_km2.rank(method="first")
        return pd.qcut(ranked, q=4, labels=["Q1", "Q2", "Q3", "Q4"])


def _attach_city_distance(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    gdf = gdf.to_crs("EPSG:3577").copy()
    gdf["centroid"] = gdf.geometry.centroid
    cities = _build_city_gdf()
    city_geoms = cities.geometry.to_list()
    city_names = cities["city"].to_list()
    nearest_city = []
    nearest_dist_km = []
    for geom in gdf["centroid"]:
        distances = [geom.distance(city_geom) for city_geom in city_geoms]
        idx = int(np.argmin(distances))
        nearest_city.append(city_names[idx])
        nearest_dist_km.append(distances[idx] / 1000.0)
    gdf["nearest_city"] = nearest_city
    gdf["distance_km"] = nearest_dist_km
    gdf["distance_band"] = gdf["distance_km"].apply(_assign_distance_band)
    gdf["area_quartile"] = _assign_area_quartiles(gdf["area_km2"])
    return gdf[["pa_id", "nearest_city", "distance_km", "distance_band", "area_quartile", "area_km2"]]


def _invariant_checks(df: pd.DataFrame) -> list[str]:
    lines = ["## Invariants", ""]
    lines.append(f"valid_fraction within [0,1]: {((df['valid_fraction'] >= 0) & (df['valid_fraction'] <= 1)).all()}")
    lines.append(f"valid_pixel_count >= 0: {(df['valid_pixel_count'] >= 0).all()}")
    lines.append(f"mean >= 0 (ignoring NaN): {(df['mean'].dropna() >= 0).all()}")
    return lines


def _anchor_checks(df_inside: pd.DataFrame, pa_meta: pd.DataFrame) -> list[str]:
    lines = ["## Anchor checks (inside mean radiance, by distance bands)", ""]
    merged = df_inside.merge(pa_meta, on="pa_id", how="left")
    years = [2013, 2018, 2024]
    for year in years:
        subset = merged[merged["year"] == year]
        urban = subset[subset["distance_km"] <= 20.0]
        remote = subset[subset["distance_km"] >= 300.0]
        lines.append(
            f"Year {year}: urban (<=20 km) median={urban['mean'].median():.3f}, remote (>=300 km) median={remote['mean'].median():.3f}"
        )
    return lines


def _sensitivity_checks(df_inside: pd.DataFrame) -> list[str]:
    lines = ["## Sensitivity checks", ""]
    corr = df_inside[["mean", "median"]].dropna().corr().iloc[0, 1]
    lines.append(f"Mean vs median correlation (inside): {corr:.3f}")
    for threshold in [MIN_VALID_PIXELS, ALT_VALID_PIXELS]:
        frac = (df_inside["valid_pixel_count"] >= threshold).mean()
        lines.append(f"Fraction inside with >= {threshold} valid pixels: {frac:.3f}")
    return lines


def _stratified_inside_vs_buffer(
    radiance_df: pd.DataFrame,
    pa_meta: pd.DataFrame,
    *,
    year: int,
    buffer_km: float,
) -> list[str]:
    subset = radiance_df[
        (radiance_df["year"] == year)
        & (
            (radiance_df["zone"] == "inside")
            | ((radiance_df["zone"] == "buffer") & (radiance_df["buffer_km"] == buffer_km))
        )
    ].copy()
    subset = subset[subset["valid_pixel_count"] >= MIN_VALID_PIXELS]
    merged = subset.merge(pa_meta, on="pa_id", how="left")
    grouped = (
        merged.groupby(["distance_band", "area_quartile", "zone"], observed=True)["mean"]
        .median()
        .unstack("zone")
        .rename(columns={"inside": "inside_mean", "buffer": f"buffer_{buffer_km}km_mean"})
    )
    grouped = grouped.dropna(subset=["inside_mean", f"buffer_{buffer_km}km_mean"])
    grouped[f"inside_minus_buffer_{buffer_km}km"] = (
        grouped["inside_mean"] - grouped[f"buffer_{buffer_km}km_mean"]
    )
    grouped = grouped.reset_index().sort_values(["distance_band", "area_quartile"])
    lines = [
        f"### Stratified inside vs buffer ({buffer_km:.0f} km) — year {year}",
        "",
        grouped.round(3).to_string(index=False),
        "",
    ]
    return lines


def _write_plot(df_inside: pd.DataFrame, plot_path: Path) -> None:
    import matplotlib.pyplot as plt

    plot_path.parent.mkdir(parents=True, exist_ok=True)
    subset = df_inside[df_inside["year"] == 2024].dropna(subset=["mean", "median"])
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(subset["mean"], subset["median"], s=6, alpha=0.4, color="#2C7FB8")
    ax.set_xlabel("Mean radiance (scaled)")
    ax.set_ylabel("Median radiance (scaled)")
    ax.set_title("Inside mean vs median (2024)")
    fig.tight_layout()
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)


def write_report(
    *,
    report_path: Path,
    plot_path: Path,
    radiance_df: pd.DataFrame,
    ring_df: pd.DataFrame,
    pa_meta: pd.DataFrame,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    inside = radiance_df[radiance_df["zone"] == "inside"].copy()
    lines = [
        "# Layer A sanity dashboard",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Minimum valid pixels: {MIN_VALID_PIXELS}",
        f"Alternative threshold: {ALT_VALID_PIXELS}",
        "",
    ]
    lines.extend(_invariant_checks(radiance_df))
    lines.append("")
    lines.extend(_anchor_checks(inside, pa_meta))
    lines.append("")
    lines.extend(_sensitivity_checks(inside))
    lines.append("")
    ring_missing = ring_df[ring_df["valid_pixel_count"] < MIN_VALID_PIXELS]
    lines.append("## Ring missingness")
    lines.append("")
    lines.append(
        ring_missing.groupby("ring_index")["pa_id"].count().to_string()
        if not ring_missing.empty
        else "No ring rows below threshold."
    )
    lines.append("")
    lines.append("## Stratified inside vs buffer (median of means)")
    lines.append("")
    lines.append(
        "Bands: urban<=20 km, peri=20–100 km, mid=100–300 km, remote>=300 km; area quartiles computed across all PAs."
    )
    lines.append("")
    lines.extend(_stratified_inside_vs_buffer(radiance_df, pa_meta, year=2024, buffer_km=1.0))
    lines.extend(_stratified_inside_vs_buffer(radiance_df, pa_meta, year=2024, buffer_km=5.0))
    lines.append(f"Plot: {plot_path.name}")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_artefact(report_path: Path, plot_path: Path, root: Path) -> Path:
    artefact_dir = root / "artefacts" / "wp0_10b_layerA_sanity"
    artefact_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(plot_path, artefact_dir / plot_path.name)

    manifest = build_manifest(
        run_id="wp0_10b_layerA_sanity",
        wp="WP0.10b",
        root=root,
        outputs=[report_path.name, plot_path.name],
        notes="WP0.10b Layer A sanity dashboard",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.10b Layer A sanity artefact. Contains sanity dashboard and sensitivity plot.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer A sanity dashboard (WP0.10).")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    radiance_df = pd.read_csv(root / RADIANCE_BUFFERS_NATIONAL_CSV)
    ring_df = pd.read_csv(root / EDGE_PROFILES_NATIONAL_CSV)
    pa_gdf = gpd.read_file(root / PA_GEOMETRIES_GPKG)
    pa_meta = _attach_city_distance(pa_gdf)

    report_path = root / REPORT_PATH
    plot_path = root / PLOT_PATH
    _write_plot(radiance_df[radiance_df["zone"] == "inside"], plot_path)
    write_report(
        report_path=report_path,
        plot_path=plot_path,
        radiance_df=radiance_df,
        ring_df=ring_df,
        pa_meta=pa_meta,
    )

    if not args.skip_artefact:
        write_artefact(report_path, plot_path, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

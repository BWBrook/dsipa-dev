"""Independently replay and plot the bounded Kosciuszko 2019–2024 case study.

Run with the project environment from the repository root. The first run reads
only the two COG windows covering NSW_N0018 and caches the decoded windows,
geometry, support masks, accepted annual series and source metadata. Subsequent
``--offline`` runs reproduce the audit and figure without network or source CSV
access. No inferred lighting-source or ecological-effect attribution is made.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MaxNLocator, MultipleLocator
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask, geometry_window
from rasterio.transform import array_bounds
from scipy import ndimage
import scipy
from shapely import from_wkb, to_wkb
from shapely.geometry import mapping


PA_ID = "NSW_N0018"
YEARS = (2019, 2024)
URL = (
    "https://zenodo.org/records/17294744/files/"
    "nightlights.average_viirs.v21_m_500m_s_{y}0101_{y}1231_go_epsg4326_v20250904.tif"
)
REPORT = Path("analysis/reports/kosciuszko_case_20261018.json")
CACHE = REPORT.with_suffix(".npz")
FIGURE = Path("manuscript/figures/fig_kosciuszko_case")
MONITOR_URL = (
    "https://www.snowyhydro.com.au/wp-content/uploads/2025/02/"
    "S2-FGJV-ENV-REP-0116A.pdf"
)
SITES = [
    {"name": "Lobs Hole", "lon": 148.416, "lat": -35.785,
     "point": "EPL5", "printed_page": 7,
     "description": "Yarrangobilly River, upstream of exploratory tunnel and construction pad"},
    {"name": "Tantangara", "lon": 148.659, "lat": -35.790,
     "point": "EPL32", "printed_page": 8,
     "description": "Tantangara Reservoir, Tantangara Intake, downstream of construction works"},
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def array_digest(array: np.ndarray) -> str:
    """Hash shape, dtype and canonical contiguous bytes, with stable NaNs."""
    array = np.array(array, copy=True, order="C")
    if np.issubdtype(array.dtype, np.floating):
        array[np.isnan(array)] = np.nan
    header = json.dumps({"shape": array.shape, "dtype": array.dtype.str}, sort_keys=True)
    return hashlib.sha256(header.encode() + b"\n" + array.tobytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def acquire(root: Path) -> dict:
    geometry_path = root / "data/processed/pa_geometries_v0_3_0.gpkg"
    radiance_path = root / "data/processed/pa_radiance_buffers_national_v0_3_0.csv"
    frame = gpd.read_file(geometry_path, where=f"pa_id = '{PA_ID}'").to_crs(4326)
    assert len(frame) == 1, "Expected one accepted Kosciuszko geometry"
    geom = frame.geometry.iloc[0]
    assert geom.is_valid and not geom.is_empty
    arrays = {}
    sources = {}
    reference_grid = None
    # This independent read uses outward-rounded geometry_window, rather than
    # borrowing the hotspot script's rounded bounding-window reader.
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
                      CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
                      GDAL_HTTP_TIMEOUT=45, GDAL_HTTP_MAX_RETRY=2):
        for year in YEARS:
            url = URL.format(y=year)
            started = utc_now()
            with rasterio.open(f"/vsicurl/{url}") as source:
                assert source.crs.to_epsg() == 4326
                assert source.transform.b == 0 and source.transform.d == 0
                window = geometry_window(source, [mapping(geom)])
                transform = source.window_transform(window)
                raw = source.read(1, window=window, masked=True)
                scale, offset = float(source.scales[0]), float(source.offsets[0])
                assert np.isfinite(scale) and np.isfinite(offset) and scale > 0
                valid = (~np.ma.getmaskarray(raw)) & np.isfinite(raw.data) & (raw.data >= 0)
                decoded = raw.data.astype("<f8") * scale + offset
                decoded[~valid] = np.nan
                grid = {"shape": list(decoded.shape), "crs": source.crs.to_string(),
                        "full_transform": list(source.transform),
                        "window_transform": list(transform),
                        "window": [int(window.col_off), int(window.row_off),
                                   int(window.width), int(window.height)]}
                if reference_grid is None:
                    reference_grid = grid
                else:
                    assert grid == reference_grid, "Endpoint rasters must share exactly the same grid"
                arrays[f"radiance_{year}"] = decoded
                arrays[f"valid_{year}"] = valid
                sources[str(year)] = {
                    "url": url, "access_started_utc": started,
                    "access_completed_utc": utc_now(), "scale": scale, "offset": offset,
                    "nodata": source.nodata, "raw_dtype": str(raw.dtype),
                    "full_raster_shape": [source.height, source.width],
                    "grid": grid, "dataset_tags": source.tags(), "band_tags": source.tags(1),
                    "raw_window_sha256": array_digest(raw.data),
                    "decoded_window_sha256": array_digest(decoded),
                    "valid_mask_sha256": array_digest(valid),
                }
                print(f"Read {year}: {decoded.shape}, scale={scale:g}, offset={offset:g}", flush=True)
    arrays["inside"] = geometry_mask([mapping(geom)], out_shape=arrays["radiance_2019"].shape,
                                     transform=transform, all_touched=False, invert=True)
    columns = ["pa_id", "zone", "year", "mean", "valid_pixel_count"]
    chunks = []
    for chunk in pd.read_csv(radiance_path, usecols=columns, chunksize=100000,
                             float_precision="round_trip"):
        chunks.append(chunk[(chunk.pa_id == PA_ID) & (chunk.zone == "inside")])
    annual = pd.concat(chunks).sort_values("year")
    assert annual.year.tolist() == list(range(2013, 2025)), "Expected one row per year"
    assert annual[["mean", "valid_pixel_count"]].notna().all().all()
    arrays["annual_year"] = annual.year.to_numpy(dtype="<i8")
    arrays["annual_mean"] = annual["mean"].to_numpy(dtype="<f8")
    arrays["annual_valid_count"] = annual.valid_pixel_count.to_numpy(dtype="<i8")
    arrays["geometry_wkb"] = np.frombuffer(to_wkb(geom), dtype=np.uint8)
    arrays["transform"] = np.asarray(list(transform), dtype="<f8")
    provenance = {
        "pa_id": PA_ID, "name": str(frame.NAME.iloc[0]), "geometry_crs": "EPSG:4326",
        "geometry_bounds": list(geom.bounds), "sources": sources,
        "local_inputs": {str(path.relative_to(root)): sha256_file(path)
                         for path in (geometry_path, radiance_path)},
        "array_sha256": {key: array_digest(value) for key, value in arrays.items()},
        "mask_rule": "Raster-centre polygon inclusion; native nodata/mask, nonfinite and negative raw values excluded before scale plus offset",
    }
    arrays["provenance"] = np.asarray(json.dumps(provenance, sort_keys=True))
    np.savez_compressed(root / CACHE, **arrays)
    return arrays


def load_cache(root: Path) -> dict:
    with np.load(root / CACHE, allow_pickle=False) as cache:
        arrays = {key: cache[key] for key in cache.files}
    provenance = json.loads(str(arrays["provenance"]))
    for key, expected in provenance["array_sha256"].items():
        assert array_digest(arrays[key]) == expected, f"Cached array changed: {key}"
    return arrays


def audit(arrays: dict) -> tuple[dict, np.ndarray]:
    before, after, inside = arrays["radiance_2019"], arrays["radiance_2024"], arrays["inside"]
    assert before.shape == after.shape == inside.shape
    common = inside & arrays["valid_2019"] & arrays["valid_2024"]
    assert np.isfinite(before[common]).all() and np.isfinite(after[common]).all()
    delta = np.zeros(before.shape, dtype="<f8")
    delta[common] = after[common] - before[common]
    positive, number = ndimage.label(delta > 0, structure=np.ones((3, 3), dtype=int))
    transform = rasterio.Affine(*arrays["transform"][:6])
    clusters = []
    for label in range(1, number + 1):
        selected = positive == label
        rows, cols = np.nonzero(selected)
        change = float(delta[selected].sum())
        x = np.average(cols + 0.5, weights=delta[selected])
        y = np.average(rows + 0.5, weights=delta[selected])
        lon, lat = transform * (x, y)
        clusters.append({"label": label, "cells": int(selected.sum()), "change": change,
                         "sum_2019": float(before[selected].sum()),
                         "sum_2024": float(after[selected].sum()),
                         "change_weighted_centroid_lon": float(lon),
                         "change_weighted_centroid_lat": float(lat)})
    clusters.sort(key=lambda item: -item["change"])
    sums = {str(year): float(arrays[f"radiance_{year}"][inside & arrays[f"valid_{year}"]].sum())
            for year in YEARS}
    gross_increase = float(delta[delta > 0].sum())
    gross_decrease = float(delta[delta < 0].sum())
    top_two = sum(item["change"] for item in clusters[:2])
    expected = {"2019": 1220.0, "2024": 26970.0}
    assert sums == expected, ("Whole-reserve endpoint mismatch", sums)
    assert gross_increase == 26110.0 and gross_decrease == -360.0
    assert top_two == 25180.0 and [item["cells"] for item in clusters[:2]] == [378, 176]
    assert sums["2024"] - sums["2019"] == gross_increase + gross_decrease
    annual_sums = arrays["annual_mean"] * arrays["annual_valid_count"]
    endpoint_checks = {}
    for year in YEARS:
        index = list(arrays["annual_year"]).index(year)
        count = int((inside & arrays[f"valid_{year}"]).sum())
        assert count == int(arrays["annual_valid_count"][index])
        difference = float(annual_sums[index] - sums[str(year)])
        # A decimal CSV mean times its integer count need not be bit-exact.
        assert abs(difference) <= 1e-8, ("Accepted mean×count mismatch", year, difference)
        endpoint_checks[str(year)] = {"raster_sum": sums[str(year)],
                                     "accepted_mean_times_count": float(annual_sums[index]),
                                     "difference": difference, "valid_cells": count}
    assert int(common.sum()) == int(inside.sum()), "Case requires complete common endpoint support"
    report = {
        "schema_version": "1.0", "pa_id": PA_ID,
        "units": "product cell-sum: sum of metadata-scaled cell values, without area weighting; not physical light output",
        "support": {"window_cells": int(inside.size), "inside_cells": int(inside.sum()),
                    "common_valid_inside_cells": int(common.sum()),
                    "valid_inside_by_year": {str(y): int((inside & arrays[f"valid_{y}"]).sum()) for y in YEARS},
                    "valid_support_change_cells": int((inside & (arrays["valid_2019"] != arrays["valid_2024"])).sum()),
                    "positive_change_cells": int((delta > 0).sum()),
                    "negative_change_cells": int((delta < 0).sum()),
                    "zero_change_cells": int((common & (delta == 0)).sum())},
        "whole_reserve_sums": sums, "gross_positive_change": gross_increase,
        "gross_negative_change": gross_decrease, "net_change": gross_increase + gross_decrease,
        "positive_cluster_connectivity": "8-neighbour; strictly positive decoded endpoint difference",
        "positive_clusters": clusters, "top_two_change": top_two,
        "top_two_share_of_gross_positive_change": top_two / gross_increase,
        "endpoint_checks": endpoint_checks,
        "annual_trajectory": [{"year": int(y), "mean": float(mean), "valid_cells": int(n),
                               "product_cell_sum": float(total)}
                              for y, mean, n, total in zip(arrays["annual_year"], arrays["annual_mean"],
                                                         arrays["annual_valid_count"], annual_sums)],
        "site_context": {"source": MONITOR_URL, "points": SITES,
                         "qualification": "Official monitoring points near construction areas; not light-source positions or causal attribution"},
    }
    return report, positive


def draw_boundary(ax, geometry, **kwargs):
    polygons = list(geometry.geoms) if geometry.geom_type == "MultiPolygon" else [geometry]
    for polygon in polygons:
        for ring in [polygon.exterior, *polygon.interiors]:
            x, y = ring.xy
            ax.plot(x, y, **kwargs)


def render(root: Path, arrays: dict, report: dict, labels: np.ndarray) -> dict:
    geom = from_wkb(arrays["geometry_wkb"].tobytes())
    transform = rasterio.Affine(*arrays["transform"][:6])
    selected = np.isin(labels, [item["label"] for item in report["positive_clusters"][:2]])
    rows, cols = np.nonzero(selected)
    west, north = transform * (cols.min(), rows.min())
    east, south = transform * (cols.max() + 1, rows.max() + 1)
    zoom = [west - 0.045, east + 0.045, south - 0.045, north + 0.055]
    full_bounds = array_bounds(*arrays["inside"].shape, transform)
    extent = [full_bounds[0], full_bounds[2], full_bounds[1], full_bounds[3]]
    cell_rows, cell_cols = np.indices(arrays["inside"].shape)
    cell_lon = transform.c + (cell_cols + 0.5) * transform.a
    cell_lat = transform.f + (cell_rows + 0.5) * transform.e
    visible = (arrays["inside"] & (cell_lon >= zoom[0]) & (cell_lon <= zoom[1])
               & (cell_lat >= zoom[2]) & (cell_lat <= zoom[3]))
    maximum = max(float(arrays[f"radiance_{y}"][visible].max()) for y in YEARS)
    vmax = np.ceil(maximum / 100) * 100
    palette = LinearSegmentedColormap.from_list("radiance", ["#ffffff", "#ffe6a5", "#ef9637", "#bc3c23", "#680b22"])
    palette.set_bad("#e6e8eb")
    norm = Normalize(0, vmax)
    ink, muted = "#23313d", "#66727c"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                         "axes.labelcolor": ink, "text.color": ink,
                         "axes.edgecolor": muted, "xtick.color": muted, "ytick.color": muted,
                         "pdf.fonttype": 42, "ps.fonttype": 42})
    fig = plt.figure(figsize=(7.2, 5.15))
    # Geographic aspect fixes each map's height. Explicit positions avoid
    # wasting a large grid row above the shared colour bar.
    axes = [fig.add_axes([left, 0.615, 0.405, 0.30]) for left in (0.10, 0.57)]
    for ax, year, letter in zip(axes, YEARS, "ab"):
        data = np.ma.array(arrays[f"radiance_{year}"], mask=~arrays["inside"] | ~arrays[f"valid_{year}"])
        im = ax.imshow(data, extent=extent, origin="upper", cmap=palette, norm=norm,
                       interpolation="nearest", rasterized=True)
        draw_boundary(ax, geom, color="#5f6b75", lw=0.6, zorder=3)
        ax.set_xlim(zoom[:2])
        ax.set_ylim(zoom[2:])
        ax.set_aspect(1 / np.cos(np.radians(np.mean(zoom[2:]))))
        ax.xaxis.set_major_locator(MultipleLocator(0.1))
        ax.yaxis.set_major_locator(MultipleLocator(0.05))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1f}°E"))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{abs(y):.2f}°S"))
        ax.tick_params(labelsize=7, length=2.5, pad=2)
        ax.set_title(f"{letter}  {year}", loc="left", fontweight="bold", fontsize=10, pad=6)
        for site in SITES:
            ax.plot(site["lon"], site["lat"], marker="+", color=ink, ms=5, mew=0.8, zorder=5)
            ax.annotate(site["name"], (site["lon"], site["lat"]), xytext=(0, -27),
                        textcoords="offset points", ha="center", va="top", fontsize=7.5,
                        arrowprops={"arrowstyle": "-", "color": ink, "lw": 0.6},
                        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1, "alpha": 0.88},
                        zorder=6)
    axes[1].tick_params(labelleft=False)
    # Locator ties the northern zoom to the complete reserve, avoiding an
    # implication that the mapped neighbourhood is the whole park.
    locator = axes[0].inset_axes([0.025, 0.52, 0.16, 0.43])
    draw_boundary(locator, geom, color=muted, lw=0.4)
    gx0, gy0, gx1, gy1 = geom.bounds
    locator.set_xlim(gx0 - 0.06, gx1 + 0.06)
    locator.set_ylim(gy0 - 0.06, gy1 + 0.06)
    locator.set_aspect(1 / np.cos(np.radians((gy0 + gy1) / 2)))
    locator.add_patch(Rectangle((zoom[0], zoom[2]), zoom[1] - zoom[0], zoom[3] - zoom[2],
                                facecolor="#e7a35e", alpha=0.5, edgecolor="#8c501d", lw=0.7))
    locator.set_xticks([])
    locator.set_yticks([])
    for spine in locator.spines.values():
        spine.set_visible(False)
    color_ax = fig.add_axes([0.10, 0.525, 0.875, 0.019])
    bar = fig.colorbar(im, cax=color_ax, orientation="horizontal")
    bar.set_label("Product-scaled radiance (product units; same scale in both years)", fontsize=8, labelpad=2)
    bar.ax.tick_params(labelsize=7, length=2)
    bar.outline.set_linewidth(0.4)
    trajectory = fig.add_axes([0.10, 0.13, 0.875, 0.29])
    years = arrays["annual_year"]
    totals = arrays["annual_mean"] * arrays["annual_valid_count"]
    trajectory.plot(years, totals, color="#1f4e79", lw=1.8, marker="o", ms=3.7, zorder=3)
    for year, offset in [(2019, (0, 11)), (2024, (-4, 9))]:
        value = totals[list(years).index(year)]
        trajectory.scatter([year], [value], s=32, facecolor="white", edgecolor="#1f4e79", zorder=4)
        trajectory.annotate(f"{int(round(value)):,}", (year, value), xytext=offset,
                            textcoords="offset points", ha="right" if year == 2024 else "center",
                            fontsize=8)
    trajectory.set_title("c  Whole-reserve annual trajectory", loc="left", fontweight="bold", fontsize=10, pad=8)
    trajectory.set_ylabel("Product cell-sum", fontsize=8)
    trajectory.set_xlabel("Year", labelpad=3)
    trajectory.set_xticks(years)
    trajectory.set_xlim(2012.8, 2024.35)
    trajectory.set_ylim(0, max(totals) * 1.2)
    trajectory.yaxis.set_major_locator(MaxNLocator(4))
    trajectory.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    trajectory.tick_params(labelsize=7.5, length=3)
    trajectory.spines[["top", "right"]].set_visible(False)
    trajectory.grid(axis="y", color="#e3e6e8", lw=0.6, zorder=0)
    fig.text(0.10, 0.975, "Kosciuszko: concentrated change near two construction areas",
             fontsize=11, fontweight="bold", ha="left", va="top")
    fig.text(0.10, 0.025, "Maps: northern reserve; grey = outside reserve; white = recorded zero.  + = documented monitoring location.",
             fontsize=7, color=muted)
    outputs = {}
    for suffix in (".png", ".pdf"):
        path = root / FIGURE.with_suffix(suffix)
        metadata = {"Creator": "DSIPA independent Kosciuszko case audit"}
        if suffix == ".pdf":
            metadata.update({"CreationDate": None, "ModDate": None})
        fig.savefig(path, dpi=300, facecolor="white", metadata=metadata)
        outputs[str(path.relative_to(root))] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    plt.close(fig)
    return {"extent_lonlat": zoom, "colour_limits": [0, float(vmax)],
            "colour_scale": "linear; zero retained", "width_inches": 7.2,
            "height_inches": 5.15, "maximum_displayed_value": maximum,
            "display_clips_positive_values": bool(maximum > vmax), "outputs": outputs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--offline", action="store_true", help="Use cached windows; no network or original input files")
    args = parser.parse_args()
    root = args.root.resolve()
    if not args.offline:
        acquire(root)
    arrays = load_cache(root)
    report, clusters = audit(arrays)
    report["source_provenance"] = json.loads(str(arrays["provenance"]))
    report["cache"] = {"path": str(CACHE), "sha256": sha256_file(root / CACHE),
                       "bytes": (root / CACHE).stat().st_size}
    report["execution"] = {
        "completed_utc": utc_now(), "offline": args.offline,
        "script_sha256": sha256_file(Path(__file__)),
        "git_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "rasterio": rasterio.__version__,
                     "GDAL": rasterio.__gdal_version__, "geopandas": gpd.__version__,
                     "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
    }
    report["figure"] = render(root, arrays, report, clusters)
    (root / REPORT).write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: report[key] for key in ("support", "whole_reserve_sums", "gross_positive_change",
                                                   "gross_negative_change", "top_two_change",
                                                   "top_two_share_of_gross_positive_change", "endpoint_checks")}, indent=2))


if __name__ == "__main__":
    main()

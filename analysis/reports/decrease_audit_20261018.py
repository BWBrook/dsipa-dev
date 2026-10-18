#!/usr/bin/env python3
"""Independent R3 audit of decreases, fixed exclusions, and small hotspot windows.

Normal replay is offline and uses the audit's saved NPZ windows:
  .venv/bin/python analysis/reports/decrease_audit_20261018.py
To acquire the initial bounded windows explicitly:
  .venv/bin/python analysis/reports/decrease_audit_20261018.py --fetch-windows

Only this audit's JSON, Markdown, optional NPZ, and requested Figure S7 PNG/PDF
are written. No implementation
from brightening_budget.py or brightening_hotspots.py is imported. The five
excluded reserves are selected once by the most negative full-period OLS
slopes; exactly that set is removed from the shorter period. This is a post-hoc
concentration diagnostic, not an unbiased estimate of background brightening.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import Window, from_bounds
from scipy.ndimage import label


YEARS = np.arange(2013, 2025)
CASES = {"WA_11648": (2015, 2016), "WA_2803": (2013, 2024),
         "SA_0011": (2013, 2024), "WA_33174": (2013, 2024)}
URL = ("https://zenodo.org/records/17294744/files/"
       "nightlights.average_viirs.v21_m_500m_s_{y}0101_{y}1231_go_epsg4326_v20250904.tif")
MAX_CELLS_PER_WINDOW = 150_000


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def array_sha(array: np.ndarray) -> str:
    return hashlib.sha256(np.nan_to_num(array, nan=-1).tobytes()).hexdigest()


def slopes(frame: pd.DataFrame, years: np.ndarray) -> pd.Series:
    values = frame.loc[:, years].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Expected complete finite annual series")
    centered_year = years - years.mean()
    estimate = (values - values[:, [0]]) @ centered_year / (centered_year @ centered_year)
    estimate[np.abs(estimate) < 1e-9] = 0
    return pd.Series(estimate, index=frame.index)


def acquire_windows(geometry: gpd.GeoDataFrame, cache: Path, geometry_hash: str,
                    inspected_snapshot: dict) -> None:
    """Read only integer covering windows, with explicit per-window cell bounds.

    Floor each starting offset and ceil each stopping offset. Rounding a
    fractional window's length to the nearest integer can omit polygon cells.
    No whole raster is read. GDAL reads the COG tiles intersecting each window.
    """
    arrays = {}
    metadata = {"accessed_utc": datetime.now(timezone.utc).isoformat(),
                "geometry_sha256": geometry_hash, "max_cells_per_window": MAX_CELLS_PER_WINDOW,
                "remote_identity_limit": "Only requested windows were fetched; full remote file hashes were not recomputed",
                "inspected_snapshot": inspected_snapshot, "cases": {}}
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
                      CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
                      GDAL_HTTP_TIMEOUT="30", GDAL_HTTP_MAX_RETRY="1", GDAL_HTTP_RETRY_DELAY="1"):
        for pa_id, years in CASES.items():
            geom = geometry.loc[pa_id].geometry
            record = {"rasters": []}
            common_transform = None
            for year in years:
                url = URL.format(y=year)
                with rasterio.open("/vsicurl/" + url) as source:
                    if source.crs.to_epsg() != 4326:
                        raise ValueError("Unexpected raster coordinate system")
                    fractional = from_bounds(*geom.bounds, source.transform)
                    col0, row0 = math.floor(fractional.col_off), math.floor(fractional.row_off)
                    col1 = math.ceil(fractional.col_off + fractional.width)
                    row1 = math.ceil(fractional.row_off + fractional.height)
                    window = Window(col0, row0, col1 - col0, row1 - row0)
                    if window.width * window.height > MAX_CELLS_PER_WINDOW:
                        raise ValueError(f"Window exceeds bounded audit limit: {pa_id}")
                    raw = source.read(1, window=window).astype(np.float64)
                    transform = source.window_transform(window)
                    invalid = ~np.isfinite(raw) | (raw < 0)
                    if source.nodata is not None:
                        invalid |= raw == source.nodata
                    decoded = raw * source.scales[0] + source.offsets[0]
                    decoded[invalid] = np.nan
                    if common_transform is None:
                        common_transform = transform
                        inside = geometry_mask([geom], out_shape=decoded.shape,
                                               transform=transform, all_touched=False, invert=True)
                        arrays[pa_id + "_inside"] = inside
                    elif common_transform != transform or inside.shape != decoded.shape:
                        raise ValueError("Paired raster windows do not have identical grids")
                    arrays[f"{pa_id}_{year}"] = decoded
                    record["rasters"].append({
                        "year": year, "url": url, "scale": source.scales[0],
                        "offset": source.offsets[0], "nodata": source.nodata,
                        "window": [col0, row0, int(window.width), int(window.height)],
                        "transform": list(transform)[:6], "crs": str(source.crs),
                        "decoded_sha256": array_sha(decoded),
                    })
                print(f"Read bounded audit window {pa_id} {year}: {decoded.shape}", flush=True)
            metadata["cases"][pa_id] = record
    arrays["_metadata_json"] = np.array(json.dumps(metadata))
    np.savez_compressed(cache, **arrays)


def inspect_clusters(cache: Path, original: dict, annual: pd.DataFrame,
                     counts: pd.DataFrame, geometry_hash: str) -> tuple[dict, dict]:
    result = {}
    with np.load(cache, allow_pickle=False) as saved:
        metadata = json.loads(str(saved["_metadata_json"]))
        if metadata["geometry_sha256"] != geometry_hash:
            raise ValueError("Audit window cache uses different protected-area geometries")
        for pa_id, (y0, y1) in CASES.items():
            a0, a1 = (saved[f"{pa_id}_{year}"] for year in (y0, y1))
            inside = saved[pa_id + "_inside"]
            valid0, valid1 = inside & np.isfinite(a0), inside & np.isfinite(a1)
            common = valid0 & valid1
            difference = np.where(common, a1 - a0, 0.0)
            positive = float(difference[difference > 0].sum())
            negative = float(difference[difference < 0].sum())
            record = {
                "years": [y0, y1], "inside_cells": int(inside.sum()),
                "common_valid_cells": int(common.sum()),
                "valid_from_only": int((valid0 & ~valid1).sum()),
                "valid_to_only": int((valid1 & ~valid0).sum()),
                "sum_from": float(a0[valid0].sum()), "sum_to": float(a1[valid1].sum()),
                "common_sum_from": float(a0[common].sum()), "common_sum_to": float(a1[common].sum()),
                "gross_positive_pixel_difference": positive,
                "gross_negative_pixel_difference": negative,
                "net_common_difference": positive + negative,
                "canonical_counts": [int(counts.loc[pa_id, year]) for year in (y0, y1)],
                "canonical_sums": [float(annual.loc[pa_id, year]) for year in (y0, y1)],
                "reported_legacy_common_count": original[pa_id]["common_valid_cells"],
                "legacy_crop_omitted_cells": int(common.sum()) - original[pa_id]["common_valid_cells"],
                "clusters_ge_200": [],
                "reported_window_hash_checks": [],
            }
            if record["canonical_counts"] != [int(valid0.sum()), int(valid1.sum())]:
                raise AssertionError(f"Covering window counts differ from canonical pipeline: {pa_id}")
            if not np.allclose(record["canonical_sums"], [record["sum_from"], record["sum_to"]], rtol=0, atol=1e-7):
                raise AssertionError(f"Covering window sums differ from canonical pipeline: {pa_id}")
            # Recreate the inspected script's smaller saved windows from our
            # covering windows, checking exact decoded hashes and omitted mass.
            for i, (year, array) in enumerate(((y0, a0), (y1, a1))):
                full_window = metadata["cases"][pa_id]["rasters"][i]["window"]
                reported = original[pa_id]["rasters"][i]
                old = reported["window"]
                c, r = old[0] - full_window[0], old[1] - full_window[1]
                if c < 0 or r < 0 or c + old[2] > array.shape[1] or r + old[3] > array.shape[0]:
                    raise ValueError("Reported crop is not contained in independent covering window")
                cropped = array[r:r + old[3], c:c + old[2]]
                keep = np.zeros(inside.shape, dtype=bool)
                keep[r:r + old[3], c:c + old[2]] = True
                omitted = inside & ~keep & np.isfinite(array)
                check = {
                    "year": year, "decoded_sha256": array_sha(cropped),
                    "matches_reported_hash": array_sha(cropped) == reported["decoded_sha256"],
                    "omitted_valid_cells": int(omitted.sum()),
                    "omitted_sum": float(array[omitted].sum()),
                }
                if not check["matches_reported_hash"]:
                    raise AssertionError(f"Public window differs from reported decoded hash: {pa_id} {year}")
                record["reported_window_hash_checks"].append(check)
            transform = rasterio.Affine(*metadata["cases"][pa_id]["rasters"][0]["transform"])
            for sign, denominator in ((1, positive), (-1, negative)):
                labels, number = label(sign * difference > 0, structure=np.ones((3, 3), dtype=int))
                for component in range(1, number + 1):
                    mask = labels == component
                    change = float(difference[mask].sum())
                    if abs(change) < 200:
                        continue
                    rows, cols = np.nonzero(mask)
                    weights = difference[mask] / change
                    lon, lat = transform * (float(cols @ weights) + .5, float(rows @ weights) + .5)
                    record["clusters_ge_200"].append({
                        "sign": sign, "change": change, "share_same_sign_gross": change / denominator,
                        "pixels": int(mask.sum()), "lat": lat, "lon": lon,
                        "sum_from": float(a0[mask].sum()), "sum_to": float(a1[mask].sum()),
                    })
            record["clusters_ge_200"].sort(key=lambda x: -abs(x["change"]))
            expected = original[pa_id]["clusters"]
            actual = record["clusters_ge_200"]
            record["cluster_changes_match_reported"] = (
                len(expected) == len(actual)
                and all(e["sign"] == a["sign"] and e["change"] == a["change"]
                        and e["pixels"] == a["pixels"]
                        and np.isclose(e["share"], a["share_same_sign_gross"], rtol=0, atol=1e-12)
                        for e, a in zip(expected, actual))
            )
            if not record["cluster_changes_match_reported"]:
                raise AssertionError(f"Independent connected clusters differ: {pa_id}")
            result[pa_id] = record
    return result, metadata


def run(root: Path, stem: Path, fetch: bool) -> dict:
    source_paths = {
        "trends": root / "data/processed/pa_trends_v0_3_0.csv",
        "annual": root / "data/processed/pa_radiance_buffers_national_v0_3_0.csv",
        "geometries": root / "data/processed/pa_geometries_v0_3_0.gpkg",
    }
    manifest = root / "analysis/reports/spatial_correction_render_input_manifest.json"
    accepted = json.loads(manifest.read_text())["files"]
    inputs = {}
    for key, path in source_paths.items():
        digest = sha256(path)
        if digest != accepted[path.name]["sha256"]:
            raise ValueError(f"Corrected input hash mismatch: {path}")
        inputs[key] = {"path": str(path), "sha256": digest}
    hotspot_path = root / "analysis/reports/brightening_budget/hotspots.json"
    hotspot_code = root / "analysis/brightening_hotspots.py"
    output_bytes = hotspot_path.read_bytes()
    code_bytes = hotspot_code.read_bytes()
    inspected_snapshot = {
        "output": json.loads(output_bytes),
        "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
        "script_sha256": hashlib.sha256(code_bytes).hexdigest(),
        "script_text": code_bytes.decode(),
    }

    trends = pd.read_csv(source_paths["trends"])
    selected = trends.metric.eq("mean") & trends.buffer_type.eq("land_unprotected") & trends.slope_inside.notna()
    ids = trends.loc[selected, "pa_id"].sort_values()
    if ids.duplicated().any():
        raise ValueError("Duplicate primary identifiers")
    geometry = gpd.read_file(source_paths["geometries"], columns=["pa_id", "NAME", "STATE"]).set_index("pa_id").loc[ids]
    cell_area = (6371.0088 * np.pi / 180 / 240) ** 2 * np.cos(np.radians(geometry.geometry.centroid.to_crs(4326).y))
    annual = pd.read_csv(source_paths["annual"], usecols=[
        "pa_id", "zone", "year", "valid_pixel_count", "mean", "frac_gt0"])
    annual = annual[annual.zone.eq("inside")]
    def pivot(column):
        return annual.pivot(index="pa_id", columns="year", values=column).loc[ids, YEARS]
    count, mean, fraction = (pivot(column) for column in ("valid_pixel_count", "mean", "frac_gt0"))
    raw_totals = mean * count
    integrated = raw_totals.mul(cell_area, axis=0)
    full, pre = slopes(integrated, YEARS), slopes(integrated, YEARS[:9])
    five = full.nsmallest(5).index
    negative_total = float(full.clip(upper=0).sum())
    named = []
    for name in five:
        named.append({"pa_id": name, "name": geometry.loc[name, "NAME"],
                      "state": geometry.loc[name, "STATE"],
                      "ols_2013_2024": float(full[name]), "ols_2013_2021": float(pre[name]),
                      "share_full_period_negative_slopes": float(full[name] / negative_total),
                      "stable_inside_pixel_count": bool(count.loc[name].nunique() == 1)})
    exclusions = {}
    for key, removed in (("all", []), ("exclude_fixed_five", list(five)),
                         ("exclude_fixed_five_and_kosciuszko", [*five, "NSW_N0018"])):
        exclusions[key] = {"excluded_ids": removed, "retained_n": len(ids) - len(removed),
                           "net_2013_2024": float(full.drop(removed).sum()),
                           "net_2013_2021": float(pre.drop(removed).sum())}
    expected_ids = ["WA_11648", "WA_2803", "SA_0011", "WA_33174", "QLD_NR234"]
    if list(five) != expected_ids:
        raise AssertionError("The independently selected five-decrease cohort changed")

    cache = stem.with_suffix(".npz")
    if fetch:
        acquire_windows(geometry.loc[list(CASES)].to_crs(4326), cache,
                        inputs["geometries"]["sha256"], inspected_snapshot)
    if not cache.exists():
        raise FileNotFoundError("Run once with --fetch-windows to create the bounded independent raster cache")
    # Preserve the inspected version even if its author repairs it concurrently.
    # Offline replay compares with that captured version, not a moving target.
    with np.load(cache, allow_pickle=False) as saved:
        inspected_snapshot = json.loads(str(saved["_metadata_json"]))["inspected_snapshot"]
    original = inspected_snapshot["output"]
    clusters, raster_metadata = inspect_clusters(cache, original, raw_totals, count, inputs["geometries"]["sha256"])
    # The snapshot itself is retained in the NPZ; avoid repeating its full text
    # and output in the human-readable JSON receipt.
    raster_metadata = {key: value for key, value in raster_metadata.items() if key != "inspected_snapshot"}
    chosen_ids = [*five, "NSW_N0018"]
    histories = {name: {int(year): {"decoded_pixel_sum": float(raw_totals.loc[name, year]),
                                  "valid_pixels": int(count.loc[name, year]),
                                  "positive_pixels": int(round((fraction * count).loc[name, year]))}
                        for year in YEARS} for name in chosen_ids}
    barrow = clusters["WA_11648"]
    murujuga = clusters["WA_2803"]
    wording = {
        "barrow_endpoint_ratio_2016_over_2015": barrow["sum_to"] / barrow["sum_from"],
        "barrow_endpoint_percent_increase": 100 * (barrow["sum_to"] / barrow["sum_from"] - 1),
        "barrow_largest_positive_cluster_fraction_gross_positive": barrow["clusters_ge_200"][0]["share_same_sign_gross"],
        "barrow_largest_positive_cluster_fraction_net": barrow["clusters_ge_200"][0]["change"] / barrow["net_common_difference"],
        "murujuga_endpoint_percent_decrease": 100 * (1 - murujuga["sum_to"] / murujuga["sum_from"]),
        "murujuga_largest_negative_cluster_fraction_gross_negative": murujuga["clusters_ge_200"][0]["share_same_sign_gross"],
        "thevenard_zero_years": [int(y) for y in YEARS if abs(raw_totals.loc["WA_33174", y]) < 1e-8],
        "thevenard_reappearance_2018_2019": [float(raw_totals.loc["WA_33174", y]) for y in (2018, 2019)],
    }
    checks = {
        "fixed_five_ids": list(five) == expected_ids,
        "five_share": np.isclose(full.loc[five].sum() / negative_total, .9491161549364829, rtol=0, atol=1e-12),
        "exclude_five_full": np.isclose(exclusions["exclude_fixed_five"]["net_2013_2024"], 2595.9514382460966, rtol=0, atol=1e-8),
        "exclude_five_pre": np.isclose(exclusions["exclude_fixed_five"]["net_2013_2021"], 1921.7373634653343, rtol=0, atol=1e-8),
        "also_exclude_kosciuszko_full": np.isclose(exclusions["exclude_fixed_five_and_kosciuszko"]["net_2013_2024"], 2226.17866947818, rtol=0, atol=1e-8),
        "also_exclude_kosciuszko_pre": np.isclose(exclusions["exclude_fixed_five_and_kosciuszko"]["net_2013_2021"], 1878.609428431283, rtol=0, atol=1e-8),
        "independent_clusters_match": all(record["cluster_changes_match_reported"] for record in clusters.values()),
        "legacy_omitted_pixels_zero": all(check["omitted_sum"] == 0 for record in clusters.values() for check in record["reported_window_hash_checks"]),
    }
    if not all(checks.values()):
        raise AssertionError(f"Audit checks failed: {checks}")
    return {
        "audit_id": "decreases-r3-independent-20261018", "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__))},
        "software": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
                     "geopandas": gpd.__version__, "rasterio": rasterio.__version__},
        "canonical_inputs": inputs, "corrected_manifest_sha256": sha256(manifest),
        "inspected_hotspot_outputs": {"path": str(hotspot_path), "sha256": inspected_snapshot["output_sha256"],
                                      "reported_accessed_utc": original.get("_accessed_utc")},
        "inspected_hotspot_script": {"path": str(hotspot_code), "sha256": inspected_snapshot["script_sha256"]},
        "independent_window_cache": {"path": str(cache), "sha256": sha256(cache), "bytes": cache.stat().st_size},
        "raster_reads": raster_metadata,
        "units": {"OLS": "approximate product units x km2 per year over annual valid support; repeated designations retained",
                  "hotspot": "unweighted sums of decoded pixel values and paired endpoint pixel differences"},
        "gross_negative_full_period": negative_total,
        "five_share_gross_negative": float(full.loc[five].sum() / negative_total),
        "fixed_five_selected_by_full_period": named, "exclusions": exclusions,
        "annual_histories": histories, "independent_cluster_replay": clusters,
        "wording_checks": wording, "acceptance_checks": {name: bool(value) for name, value in checks.items()},
        "limitations": [
            "Exclusions were selected post hoc by the strongest negative full-period outcomes; shorter-period reuse is a fixed-cohort sensitivity, not independent confirmation of broad brightening.",
            "This audit verifies product observations and spatial concentration, not facility identities, operational causes, or ecological exposure.",
            "Endpoint clusters use different periods across reserves and cannot be interpreted as spatial decompositions of the full-period OLS slope.",
            "The 2013-2024 endpoint comparisons span product-source changes; the Barrow 2015-2016 spike is within the earlier period but that does not establish homogeneous processing.",
            "A 2021 rise precedes the documented 2022 source change but does not exclude all processing effects; spatial concentration alone does not rule them out.",
            "Thevenard has positive observations again in 2018 and 2019; a zero 2024 endpoint does not show persistent absence since oil production ended.",
            "Cluster selection is eight-neighbour connectivity of same-sign common-valid differences; reported clusters have absolute change at least 200, while denominators include all same-sign pixel changes.",
        ],
    }


def markdown(result: dict) -> str:
    lines = ["# Independent audit of decreases and fixed exclusions — 18 October 2026", "",
             "The corrected annual summaries reproduce the exclusion arithmetic. Independent bounded raster-window reads reproduce the cluster magnitudes and shares, while detecting a crop-support defect in the inspected hotspot script.", "",
             "## Fixed five reserves", "",
             "Selection uses the five most negative 2013–2024 whole-reserve integrated OLS slopes. The identical set is excluded from both periods.", "",
             "| Reserve | ID | 2013–2024 slope | 2013–2021 slope | Share of full-period negative slopes |",
             "|---|---|---:|---:|---:|"]
    for row in result["fixed_five_selected_by_full_period"]:
        lines.append(f"| {row['name']} | {row['pa_id']} | {row['ols_2013_2024']:.6f} | {row['ols_2013_2021']:.6f} | {row['share_full_period_negative_slopes']:.4%} |")
    lines.extend(["", f"Combined share: **{result['five_share_gross_negative']:.6%}**. All five inside count series are constant. Strzelecki is third; Thevenard is fourth.", "",
                  "| Cohort | Retained reserves | Net 2013–2024 | Net 2013–2021 |", "|---|---:|---:|---:|"])
    for name, row in result["exclusions"].items():
        lines.append(f"| {name} | {row['retained_n']} | {row['net_2013_2024']:+.6f} | {row['net_2013_2021']:+.6f} |")
    w = result["wording_checks"]
    lines.extend(["", "## Cluster and wording checks", "",
                  f"- Barrow Island's whole-reserve sum was 74,690 in 2015 and 207,180 in 2016: **{w['barrow_endpoint_ratio_2016_over_2015']:.6f} times**, or +{w['barrow_endpoint_percent_increase']:.3f}%. Use ‘nearly tripled’. The +144,300 cluster supplies **{w['barrow_largest_positive_cluster_fraction_gross_positive']:.6%}** of gross positive pixel differences (+144,440), and {w['barrow_largest_positive_cluster_fraction_net']:.6%} of the net jump (+132,490). It is not 100% of net change.",
                  f"- Murujuga falls from 76,060 to 10,510 between 2013 and 2024: **{w['murujuga_endpoint_percent_decrease']:.6f}%**. Its −63,070 cluster supplies **{w['murujuga_largest_negative_cluster_fraction_gross_negative']:.6%}** of gross negative differences (−65,570); other pixels increase by 20.",
                  "- Thevenard falls from 3,370 in 2013 to zero in 2024. It is zero in 2016–2017, positive again in 2018 (200) and 2019 (70), then zero in 2020–2024. The endpoint cannot establish permanent cessation of measured light in 2014.",
                  "- Barrow's 2016 peak is followed by decreases and rebounds, not monotonic decline. Strzelecki's 2015 spike (10,800) also strongly affects its fitted trend.", "",
                  "## Window-support defect and independent verification", "",
                  "The inspected hotspot script uses floor-offset/nearest-length window rounding. This can crop away polygon-selected cells. The independent replay floors starts and ceils stops, matching canonical counts. All omitted cells were zero at the compared endpoints; the reported cluster quantities survive correction.", "",
                  "| Reserve ID | Reported common cells | Correct covering-window common cells | Omitted cells | Omitted endpoint sums |",
                  "|---|---:|---:|---:|---|"])
    for name, row in result["independent_cluster_replay"].items():
        omitted = [check["omitted_sum"] for check in row["reported_window_hash_checks"]]
        lines.append(f"| {name} | {row['reported_legacy_common_count']} | {row['common_valid_cells']} | {row['legacy_crop_omitted_cells']} | {omitted} |")
    lines.extend(["", "All eight cropped decoded-array hashes reproduce the inspected output hashes; covering-window annual sums and counts reproduce the corrected pipeline. Scale and offset are applied before differencing; all four pairs have no endpoint-only valid cells. Current output endpoints therefore coincide with common-support sums. In general, the inspected script's endpoint totals are per-year-valid totals, whereas its difference denominators use common support.", "",
                  "## Interpretation limits", ""])
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.extend(["", "No primary-source facility verification was performed by this audit. Claims about Gorgon, Karratha Gas Plant, construction or decommissioning require their separate source and location checks. The cited Woodside account concerns 2025, outside the analysis period, and cannot establish the cause of the 2013–2024 decrease.", "",
                  "## Supplementary Figure S7", "",
                  "The wrapper also renders `manuscript/figures/fig_decrease_histories.png` and `.pdf` directly from the corrected annual summaries. Separate panels show Barrow Island, Murujuga and Thevenard Island (full-period decreasing ranks 1, 2 and 4), with independent linear vertical scales, visible zeros and a 2022 source-change marker. These cases were selected after inspecting the results; no industrial events or causal explanations are annotated. Thevenard's 2018–2019 return to positive values and both larger reserves' rebounds remain visible. Figure hashes and the 36 plotted observations are recorded in the JSON receipt.", "",
                  "## Reproduction", "", "Run `analysis/reports/decrease_audit_20261018.py` with the project Python environment. Default replay uses the saved NPZ and makes no network requests. `--fetch-windows` explicitly reacquires eight bounded windows (each below 150,000 cells). Input identities, requested windows, scales, transforms, array hashes, access times and acceptance checks are retained in the JSON receipt.", ""])
    return "\n".join(lines)


def render_histories(result: dict, root: Path) -> dict:
    """Render the requested S7 from canonical observations, without event labels."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    from PIL import Image

    selected = [("WA_11648", "Barrow Island", 1),
                ("WA_2803", "Murujuga", 2),
                ("WA_33174", "Thevenard Island", 4)]
    ink, muted, grid, blue = "#1f1f1f", "#5f5f5f", "#e3e3e3", "#1f4e79"
    style = {"font.size": 8.5, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "axes.spines.top": False,
             "axes.spines.right": False, "pdf.fonttype": 42, "ps.fonttype": 42}
    figure_stem = root / "manuscript/figures/fig_decrease_histories"
    plotted = {}
    with plt.rc_context(style):
        figure, axes = plt.subplots(1, 3, figsize=(9.5, 3.45), constrained_layout=True)
        for panel, axis, (pa_id, name, rank) in zip("abc", axes, selected):
            rows = result["annual_histories"][pa_id]
            values = np.array([rows[int(year)]["decoded_pixel_sum"] for year in YEARS])
            if len(values) != 12 or not np.isfinite(values).all() or values.min() < -1e-8:
                raise AssertionError("Invalid annual values for S7")
            axis.axhline(0, color=muted, lw=.65, zorder=1)
            axis.axvline(2022, color=muted, ls="--", lw=.8, alpha=.8, zorder=1)
            axis.plot(YEARS, values, color=blue, marker="o", markersize=3.5,
                      markeredgecolor="white", markeredgewidth=.35, lw=1.25, zorder=3)
            axis.set_title(f"{panel}  {name}", loc="left", color=ink, fontsize=10, pad=8)
            axis.text(.98, .96, f"Decrease rank {rank}", transform=axis.transAxes,
                      ha="right", va="top", fontsize=8, color=muted,
                      bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})
            axis.set_xlim(2012.6, 2024.4)
            axis.set_xticks([2013, 2016, 2019, 2022, 2024])
            axis.set_ylim(-.04 * values.max(), 1.10 * values.max())
            axis.yaxis.set_major_locator(MaxNLocator(nbins=5, min_n_ticks=4))
            axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
            axis.grid(axis="y", color=grid, lw=.6)
            axis.set_xlabel("Year")
            plotted[pa_id] = {
                "name": name, "full_period_decrease_rank": rank,
                "years": YEARS.tolist(), "decoded_pixel_sums": values.tolist(),
                "valid_pixel_counts": [rows[int(year)]["valid_pixels"] for year in YEARS],
                "zero_years": [int(year) for year, value in zip(YEARS, values) if abs(value) < 1e-8],
            }
        axes[0].text(2021.75, .85, "2022 source change", transform=axes[0].get_xaxis_transform(),
                     rotation=90, ha="right", va="top", color=muted, fontsize=7.5)
        figure.supylabel("Sum of decoded pixel values (product units)", fontsize=9)
        figure.savefig(figure_stem.with_suffix(".png"), dpi=300, facecolor="white")
        figure.savefig(figure_stem.with_suffix(".pdf"), facecolor="white")
        plt.close(figure)
    with Image.open(figure_stem.with_suffix(".png")) as bitmap:
        png_size = list(bitmap.size)
    return {
        "intended_number": "S7", "matplotlib_version": matplotlib.__version__,
        "selection": "Post-inspection named cases, ranks 1, 2 and 4 among full-period decreases",
        "scale": "Independent linear vertical scales with visible zero baseline",
        "annotation": "2022 product-source change only; no industrial-event or causal annotations",
        "plotted_observations": plotted, "png_dimensions": png_size,
        "qa_checks": {"canonical_observations_plotted": 36,
                      "complete_years_per_panel": 12,
                      "independent_linear_vertical_scales": True,
                      "zero_baseline_with_lower_margin": True},
        "visual_qa": {"status": "pending_after_regeneration"},
        "files": [{"path": str(figure_stem.with_suffix(suffix)),
                   "sha256": sha256(figure_stem.with_suffix(suffix))}
                  for suffix in (".png", ".pdf")],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--fetch-windows", action="store_true")
    args = parser.parse_args()
    stem = Path(__file__).resolve().with_suffix("")
    result = run(args.root.resolve(), stem, args.fetch_windows)
    result["figure_s7"] = render_histories(result, args.root.resolve())
    stem.with_suffix(".json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    stem.with_suffix(".md").write_text(markdown(result))
    print(json.dumps({"outputs": [str(stem.with_suffix(s)) for s in (".json", ".md", ".npz")],
                      "acceptance_checks": result["acceptance_checks"],
                      "exclusions": result["exclusions"]}, indent=2))


if __name__ == "__main__":
    main()

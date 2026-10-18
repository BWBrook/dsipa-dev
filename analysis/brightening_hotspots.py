"""Locate pixel clusters behind large reserve-level changes in measured radiance.

Reads windows of the published Hengl/OpenGeoHub v0.4 annual COGs directly from
Zenodo, applies the same centre-based polygon selection and scale metadata as
the pipeline, and reports connected clusters of pixel change between two years.
Descriptive only: cluster locations are compared with mapped features
elsewhere, not inferred here.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds
from scipy import ndimage

URL = ("/vsicurl/https://zenodo.org/records/17294744/files/nightlights.average_viirs.v21_m_500m_s_"
       "{y}0101_{y}1231_go_epsg4326_v20250904.tif")
CASES = {"NSW_N0018": (2019, 2024), "WA_11648": (2015, 2016), "SA_0247": (2016, 2024),
         "CWTH_IPA20": (2013, 2024), "WA_2803": (2013, 2024), "SA_0011": (2013, 2024),
         "WA_33174": (2013, 2024)}


def read(geom, year):
    minx, miny, maxx, maxy = geom.bounds
    url = URL.format(y=year)
    with rasterio.open(url) as ds:
        w = from_bounds(minx, miny, maxx, maxy, ds.transform).round_offsets().round_lengths()
        raw = ds.read(1, window=w).astype(float)
        tr = ds.window_transform(w)
        invalid = (raw == ds.nodata) | (raw < 0)
        a = raw * ds.scales[0] + ds.offsets[0]
        a[invalid] = np.nan
        meta = {"url": url.removeprefix("/vsicurl/"), "scale": ds.scales[0], "offset": ds.offsets[0],
                "window": [int(w.col_off), int(w.row_off), int(w.width), int(w.height)],
                "transform": list(tr)[:6], "decoded_sha256": hashlib.sha256(np.nan_to_num(a, nan=-1).tobytes()).hexdigest()}
        return a, tr, meta


def clusters(geom, y0, y1, min_sum):
    a0, tr, m0 = read(geom, y0)
    a1, tr1, m1 = read(geom, y1)
    assert a0.shape == a1.shape and tr == tr1, "paired windows must share grid"
    inside = ~geometry_mask([geom], out_shape=a1.shape, transform=tr, all_touched=False)
    common = inside & np.isfinite(a0) & np.isfinite(a1)
    d = np.where(common, a1 - a0, 0.0)
    out = {"year_from": y0, "year_to": y1, "rasters": [m0, m1],
           "inside_cells": int(inside.sum()), "common_valid_cells": int(common.sum()),
           "valid_from_only": int((inside & np.isfinite(a0) & ~np.isfinite(a1)).sum()),
           "valid_to_only": int((inside & ~np.isfinite(a0) & np.isfinite(a1)).sum()),
           "inside_sum_from": float(np.nansum(a0[inside])), "inside_sum_to": float(np.nansum(a1[inside])),
           "gross_increase": float(d[d > 0].sum()), "gross_decrease": float(d[d < 0].sum()), "clusters": []}
    for sign in (1, -1):
        lab, n = ndimage.label(sign * d > 0, structure=np.ones((3, 3)))
        total = out["gross_increase"] if sign > 0 else out["gross_decrease"]
        for k in range(1, n + 1):
            m = lab == k
            s = d[m].sum()
            if abs(s) < min_sum:
                continue
            rr, cc = np.nonzero(m)
            wy, wx = (d[m] * rr).sum() / s, (d[m] * cc).sum() / s
            lon, lat = tr * (wx + 0.5, wy + 0.5)
            out["clusters"].append({"sign": sign, "change": float(s), "share": float(s / total),
                                    "pixels": int(m.sum()), "lat": round(float(lat), 4),
                                    "lon": round(float(lon), 4), "sum_from": float(np.nansum(a0[m])),
                                    "sum_to": float(np.nansum(a1[m]))})
    out["clusters"].sort(key=lambda c: -abs(c["change"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path, default=Path("analysis/reports/brightening_budget/hotspots.json"))
    ap.add_argument("--min-sum", type=float, default=200.0)
    a = ap.parse_args()
    g = gpd.read_file(a.root / "data/processed/pa_geometries_v0_3_0.gpkg",
                      where="pa_id IN ({})".format(",".join(f"'{k}'" for k in CASES))).to_crs(4326)
    res = {}
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif"):
        for _, row in g.iterrows():
            y0, y1 = CASES[row.pa_id]
            res[row.pa_id] = {"name": row.NAME, **clusters(row.geometry, y0, y1, a.min_sum)}
            c = res[row.pa_id]
            print(f"{row.NAME}: {y0}->{y1} inside {c['inside_sum_from']:.0f}->{c['inside_sum_to']:.0f}")
            for cl in c["clusters"][:4]:
                print(f"   {cl['change']:+9.0f} ({cl['share']:.0%}) px={cl['pixels']} at {cl['lat']},{cl['lon']}")
    res["_accessed_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    a.out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

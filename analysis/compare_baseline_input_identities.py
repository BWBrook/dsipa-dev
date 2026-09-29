#!/usr/bin/env python3
"""Compare public and accepted baseline CSV/GPKG identities read-only."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

CSV_KEYS = {
    "pa_radiance_buffers_national_v0_3_0.csv": ["pa_id", "zone", "buffer_km", "buffer_type", "year"],
    "pa_edge_profiles_national_v0_3_0.csv": ["pa_id", "ring_inner_km", "ring_outer_km", "year"],
}

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def csv_compare(a: Path, b: Path, keys: list[str]) -> dict:
    x = pd.read_csv(a, float_precision="round_trip")
    y = pd.read_csv(b, float_precision="round_trip")
    result = {"accepted_shape": list(x.shape), "public_shape": list(y.shape),
              "columns_equal": list(x.columns) == list(y.columns),
              "accepted_sha256": sha(a), "public_sha256": sha(b), "columns": {}}
    if list(x.columns) != list(y.columns):
        result["accepted_columns"] = list(x.columns); result["public_columns"] = list(y.columns)
    x = x.sort_values(keys, kind="mergesort").reset_index(drop=True)
    y = y.sort_values(keys, kind="mergesort").reset_index(drop=True)
    result["keys"] = keys
    result["key_order_equal"] = bool(x[keys].astype("string").equals(y[keys].astype("string")))
    result["key_set_equal"] = bool(set(map(tuple, x[keys].astype("string").to_numpy())) == set(map(tuple, y[keys].astype("string").to_numpy())))
    result["duplicate_keys"] = {"accepted": int(x.duplicated(keys).sum()), "public": int(y.duplicated(keys).sum())}
    for c in x.columns.intersection(y.columns):
        xa, ya = x[c], y[c]
        both_missing = xa.isna() & ya.isna()
        if pd.api.types.is_numeric_dtype(xa) and pd.api.types.is_numeric_dtype(ya):
            diff = (xa - ya).abs()
            finite = diff[~both_missing & np.isfinite(diff)]
            neq = (~both_missing & (xa != ya))
            entry = {"kind": "numeric", "different": int(neq.sum()), "both_missing": int(both_missing.sum()), "max_abs_diff": float(finite.max()) if len(finite) else 0.0}
        else:
            neq = ~(both_missing | xa.astype("string").eq(ya.astype("string")))
            entry = {"kind": "text", "different": int(neq.sum()), "both_missing": int(both_missing.sum())}
        if entry["different"]:
            ids = x.loc[neq, keys].astype(str).head(5).to_dict("records")
            entry["examples"] = ids
        result["columns"][c] = entry
    return result

def gpkg_compare(a: Path, b: Path) -> dict:
    import geopandas as gpd
    x, y = gpd.read_file(a), gpd.read_file(b)
    key = "pa_id"
    x = x.sort_values(key, kind="mergesort").reset_index(drop=True)
    y = y.sort_values(key, kind="mergesort").reset_index(drop=True)
    out = {"accepted_sha256": sha(a), "public_sha256": sha(b), "accepted_shape": list(x.shape), "public_shape": list(y.shape),
           "crs_equal": bool(x.crs == y.crs), "accepted_crs": x.crs.to_string(), "public_crs": y.crs.to_string(),
           "pa_id_set_equal": set(x[key]) == set(y[key]), "pa_id_order_equal": x[key].tolist() == y[key].tolist(),
           "duplicate_pa_id": {"accepted": int(x[key].duplicated().sum()), "public": int(y[key].duplicated().sum())}, "attributes": {}}
    for c in x.columns:
        if c == x.geometry.name: continue
        xa, ya = x[c], y[c]
        miss = xa.isna() & ya.isna(); neq = ~(miss | xa.astype("string").eq(ya.astype("string")))
        out["attributes"][c] = {"different": int(neq.sum()), "both_missing": int(miss.sum())}
        if neq.any(): out["attributes"][c]["examples"] = x.loc[neq, [key, c]].head(5).astype(str).to_dict("records")
    geq = [bool(g1.equals(g2)) for g1, g2 in zip(x.geometry, y.geometry)]
    out["geometry"] = {"topological_equals_different": int(sum(not z for z in geq)), "topological_equals_all": bool(all(geq))}
    out["geometry"]["different_examples"] = x.loc[[not z for z in geq], [key]].head(5)[key].tolist()
    out["geometry"]["accepted_normalized_wkb_sha256"] = hashlib.sha256(b"".join(g.normalize().wkb for g in x.geometry)).hexdigest()
    out["geometry"]["public_normalized_wkb_sha256"] = hashlib.sha256(b"".join(g.normalize().wkb for g in y.geometry)).hexdigest()
    return out

def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--accepted", type=Path, required=True); p.add_argument("--public", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(); out = {"csv": {n: csv_compare(args.accepted / n, args.public / n, k) for n, k in CSV_KEYS.items()}, "gpkg": gpkg_compare(args.accepted / "pa_geometries_v0_3_0.gpkg", args.public / "pa_geometries_v0_3_0.gpkg")}
    args.output.write_text(json.dumps(out, indent=2) + "\n"); print(json.dumps(out, indent=2))
if __name__ == "__main__": main()

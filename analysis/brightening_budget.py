"""Additive budget of measured radiance change across assessable protected areas.

Sen slopes cannot be summed across reserves or spatial bands. Total measured
radiance can: annual inside mean x valid pixels x cell area, in product units
x km2. OLS slopes and period differences of these totals are additive, so they
show where the estate-wide change sits. Descriptive only; reads accepted
corrected outputs and writes nothing outside the output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.stats import theilslopes

YEARS = np.arange(2013, 2025)
PRE = np.arange(2013, 2022)
CELL_KM2_AT_EQUATOR = (6371.0088 * np.pi / 180 / 240) ** 2
SIZE_BINS = [0, 1, 10, 100, 1000, np.inf]
SIZE_LABELS = ["<1", "1-10", "10-100", "100-1,000", ">1,000"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ols_slope(mat, years):
    y = mat[:, : len(years)]
    y = y - y.mean(axis=1, keepdims=True)
    x = years - years.mean()
    slope = (y * x).sum(axis=1) / (x**2).sum()
    return np.where(np.abs(slope) < 1e-9, 0.0, slope)


def measures(total):
    m = total.to_numpy()
    return pd.DataFrame(
        {
            "slope_2013_2024": ols_slope(m, YEARS),
            "slope_2013_2021": ols_slope(m, PRE),
            "diff_late_minus_early": m[:, -3:].mean(1) - m[:, :3].mean(1),
        },
        index=total.index,
    )


def totals(df, ids, cell_area):
    mean = df.pivot(index="pa_id", columns="year", values="mean").reindex(ids)[YEARS]
    count = df.pivot(index="pa_id", columns="year", values="valid_pixel_count").reindex(ids)[YEARS]
    return mean * count.mul(cell_area, axis=0), count


def share_table(budget, key, area):
    rows = []
    net = budget.slope_2013_2024.sum()
    gross = budget.slope_2013_2024.clip(lower=0).sum()
    net_pre = budget.slope_2013_2021.sum()
    for k, g in budget.groupby(key, observed=True):
        rows.append(
            {
                key: k,
                "reserves": len(g),
                "area_share": area.loc[g.index].sum() / area.sum(),
                "net_increase_share": g.slope_2013_2024.sum() / net,
                "gross_increase_share": g.slope_2013_2024.clip(lower=0).sum() / gross,
                "net_increase_share_2013_2021": g.slope_2013_2021.sum() / net_pre,
            }
        )
    return pd.DataFrame(rows)


def remove_level_shifts(values, steps):
    y = np.asarray(values, dtype=float).copy()
    for s in steps:
        k = s - YEARS[0]
        y[k:] -= y[k] - y[k - 1]
    return y


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path, default=Path("analysis/reports/brightening_budget"))
    a = ap.parse_args()
    root, out = a.root, a.out
    out.mkdir(parents=True, exist_ok=True)
    inputs = {
        "trends": root / "data/processed/pa_trends_v0_3_0.csv",
        "radiance": root / "data/processed/pa_radiance_buffers_national_v0_3_0.csv",
        "edges": root / "data/processed/pa_edge_profiles_national_v0_3_0.csv",
        "geometries": root / "data/processed/pa_geometries_v0_3_0.gpkg",
        "distances": root / "analysis/reports/product_baseline_distances.csv",
    }

    t = pd.read_csv(inputs["trends"])
    t = t[(t.metric == "mean") & (t.buffer_type == "land_unprotected")].set_index("pa_id")
    ids = t.index[t.slope_inside.notna()].sort_values()
    sen_in, sen_buf = t.loc[ids, "slope_inside"], t.loc[ids, "slope_buffer_1km"]
    cat = pd.Series("unpaired", index=ids)
    paired = sen_buf.notna()
    cat[paired & (sen_in > 0) & (sen_buf > 0)] = "Q1"
    cat[paired & (sen_in > 0) & (sen_buf <= 0)] = "Q2"
    cat[paired & (sen_in <= 0) & (sen_buf <= 0)] = "Q3"
    cat[paired & (sen_in <= 0) & (sen_buf > 0)] = "Q4"

    g = gpd.read_file(inputs["geometries"], columns=["pa_id", "area_km2"]).set_index("pa_id")
    g = g.loc[ids]
    lat = g.geometry.centroid.to_crs(4326).y
    cell_area = CELL_KM2_AT_EQUATOR * np.cos(np.radians(lat))
    area = g.area_km2

    cols = ["pa_id", "zone", "buffer_km", "buffer_type", "year", "valid_pixel_count", "mean", "frac_gt0"]
    r = pd.read_csv(inputs["radiance"], usecols=cols)
    whole_t, whole_n = totals(r[r.zone == "inside"], ids, cell_area)
    buf = r[(r.zone == "buffer") & (r.buffer_type == "land_unprotected") & (r.buffer_km == 1.0)]
    buf_t, _ = totals(buf, ids, cell_area)
    e = pd.read_csv(inputs["edges"], usecols=["pa_id", "ring_index", "year", "valid_pixel_count", "mean"])
    outer_t, outer_n = totals(e[e.ring_index == 0], ids, cell_area)

    assert whole_t.notna().all().all(), "eligible whole-reserve series must be complete"
    outer_ok = outer_t.notna().all(axis=1)
    rest_t = whole_t - outer_t
    rest_n = whole_n - outer_n
    min_rest_total = float(rest_t[outer_ok].min().min())

    W = measures(whole_t)
    budget = W.join(pd.DataFrame({"category": cat, "area_km2": area, "latitude": lat,
                                  "valid_pixels_2024": whole_n[2024], "sen_inside": sen_in}))
    budget["size_class"] = pd.cut(area, SIZE_BINS, labels=SIZE_LABELS, right=False)
    dist = pd.read_csv(inputs["distances"]).set_index("pa_id").reindex(ids)
    budget["distance_2013_light"] = dist.stratum
    budget.to_csv(out / "reserve_budget.csv", float_format="%.6g")

    s = budget.slope_2013_2024
    net, gross_pos, gross_neg = s.sum(), s.clip(lower=0).sum(), s.clip(upper=0).sum()
    order = s.sort_values(ascending=False)
    cum = order.clip(lower=0).cumsum() / gross_pos
    area_cum = area.loc[order.index].cumsum() / area.sum()
    lorenz = pd.DataFrame({"rank": np.arange(1, len(order) + 1), "pa_id": order.index,
                           "slope_2013_2024": order.values, "cum_gross_share": cum.values,
                           "cum_area_share": area_cum.values})
    lorenz.to_csv(out / "concentration_curve.csv", index=False, float_format="%.6g")
    names = gpd.read_file(inputs["geometries"], columns=["pa_id", "NAME", "STATE"],
                          ignore_geometry=True).set_index("pa_id")
    top = lorenz.head(20).join(names, on="pa_id").join(budget[["area_km2", "category", "sen_inside"]], on="pa_id")
    top.to_csv(out / "top20_contributors.csv", index=False, float_format="%.6g")

    pre = budget.slope_2013_2021
    pre_order = pre.sort_values(ascending=False)
    pre_gross = pre.clip(lower=0).sum()

    def topk(k):
        sel = order.index[:k]
        return {"k": k, "gross_share": float(s.loc[sel].clip(lower=0).sum() / gross_pos),
                "net_share": float(s.loc[sel].sum() / net),
                "area_share": float(area.loc[sel].sum() / area.sum()),
                "gross_share_2013_2021_same_reserves": float(pre.loc[sel].clip(lower=0).sum() / pre_gross),
                "gross_share_2013_2021_own_top": float(pre_order.iloc[:k].clip(lower=0).sum() / pre_gross),
                "top_k_overlap_with_2013_2021_top": int(len(set(sel) & set(pre_order.index[:k])))}

    def reach(q):
        k = int((cum < q).sum() + 1)
        return {"gross_share": q, "reserves_needed": k,
                "area_share": float(area.loc[order.index[:k]].sum() / area.sum())}

    tables = {
        "size_class": share_table(budget, "size_class", area),
        "distance_2013_light": share_table(budget, "distance_2013_light", area),
        "category": share_table(budget, "category", area),
    }
    for name, tab in tables.items():
        tab.to_csv(out / f"budget_by_{name}.csv", index=False, float_format="%.6g")

    interior = outer_ok & (rest_n.min(axis=1) >= 10)
    stable_counts = (whole_n.nunique(axis=1) == 1) & (outer_n.nunique(axis=1) == 1)
    def edge_stats(mask):
        O, Wm = measures(outer_t[mask]), measures(whole_t[mask])
        cells_outer = (outer_n[mask][2024] * cell_area[mask]).sum()
        cells_whole = (whole_n[mask][2024] * cell_area[mask]).sum()
        pos = Wm.slope_2013_2024 > 0
        share = O.slope_2013_2024[pos] / Wm.slope_2013_2024[pos]
        return {"reserves": int(mask.sum()),
                "outer_km_area_share": float(cells_outer / cells_whole),
                "positive_whole_reserves": int(pos.sum()),
                "outer_km_area_share_in_positive_reserves": float(
                    (outer_n[mask][2024] * cell_area[mask])[pos].sum() / (whole_n[mask][2024] * cell_area[mask])[pos].sum()),
                "interior_dominated_positive_reserves": sorted(share.index[share <= 0.5]),
                "outer_km_share_of_increase_in_positive_reserves": float(
                    O.slope_2013_2024[pos].sum() / Wm.slope_2013_2024[pos].sum()),
                "median_reserve_outer_share_in_positive_reserves": float(share.median()),
                "positive_reserves_with_majority_of_increase_in_outer_km": int((share > 0.5).sum())}

    M = r[r.zone == "inside"].pivot(index="pa_id", columns="year", values="mean").reindex(ids)[YEARS]
    pos_ids = sen_in.index[sen_in > 0]
    step_sets = {"2017": (2017,), "2023": (2023,), "2017+2023": (2017, 2023), "2017+2020+2023": (2017, 2020, 2023)}
    step_sens = {k: int(sum(theilslopes(remove_level_shifts(M.loc[i], v), YEARS)[0] > 0 for i in pos_ids))
                 for k, v in step_sets.items()}
    step_sens["within_2017_2022_only"] = int(sum(
        theilslopes(M.loc[i, 2017:2022].to_numpy(), np.arange(2017, 2023))[0] > 0 for i in pos_ids))
    frac = r[r.zone == "inside"].pivot(index="pa_id", columns="year", values="frac_gt0").reindex(ids)[YEARS]
    lit = (frac * whole_n).fillna(0)
    jumps = {f"{y - 1}-{y}": int(((lit[y] / lit[y - 1].replace(0, np.nan) >= 1.3) & (lit[y - 1] >= 20)).sum())
             for y in YEARS[1:]}
    mean_rank = sen_in[sen_in > 0].rank(ascending=False)
    top_total, top_mean = set(order.index[:20]), set(mean_rank.nsmallest(20).index)
    kosc = "NSW_N0018"

    Ob, Rb = measures(outer_t), measures(rest_t)
    def band_split(col):
        go, gr = Ob[col].clip(lower=0).sum(), Rb[col].clip(lower=0).sum()
        return float(go / (go + gr))
    rest_pos = Rb.slope_2013_2024.clip(lower=0).sort_values(ascending=False)
    rest_cum = rest_pos.cumsum() / rest_pos.sum()
    ipa = [i for i in ids if "IPA" in i]
    band_budget = {
        "outer_km_area_share_all_assessable": float((outer_n[2024] * cell_area).sum() / (whole_n[2024] * cell_area).sum()),
        "outer_km_share_of_band_level_gross_increase": band_split("slope_2013_2024"),
        "outer_km_share_of_band_level_gross_increase_2013_2021": band_split("slope_2013_2021"),
        "outer_km_share_of_band_level_gross_increase_period_difference": band_split("diff_late_minus_early"),
        "beyond_1km_reserves_for_50_80_pct": [int((rest_cum < q).sum() + 1) for q in (0.5, 0.8)],
        "beyond_1km_top10": [{"pa_id": i, "share": float(rest_pos[i] / rest_pos.sum())} for i in rest_pos.index[:10]],
        "ipa": {"reserves": len(ipa), "area_share": float(area[ipa].sum() / area.sum()),
                "share_of_beyond_1km_gross_increase": float(Rb.slope_2013_2024[ipa].clip(lower=0).sum() / rest_pos.sum()),
                "share_of_outer_km_gross_increase": float(Ob.slope_2013_2024[ipa].clip(lower=0).sum()
                                                          / Ob.slope_2013_2024.clip(lower=0).sum())},
    }

    B = measures(buf_t[paired & buf_t.notna().all(axis=1)])
    Wp = W.loc[B.index]
    summary = {
        "inputs": {k: {"path": str(v), "sha256": sha256(v)} for k, v in inputs.items()},
        "units": "OLS slope of area-integrated product radiance over the sampled valid support (product units x km2 per year); not physical emitted light; cell area = 15 arc-second cell scaled by cos(centroid latitude); overlapping designations are counted in each reserve",
        "eligible_reserves": int(len(ids)),
        "cell_area_check_median_area_per_valid_pixel_km2_reserves_over_100km2": float(
            (area / whole_n[2024])[area > 100].median()),
        "cell_area_model_median_km2_same_reserves": float(cell_area[area > 100].median()),
        "net_slope": float(net), "gross_positive": float(gross_pos), "gross_negative": float(gross_neg),
        "net_slope_2013_2021": float(pre.sum()),
        "reserves_with_positive_ols_slope": int((s > 0).sum()),
        "reserves_with_negative_ols_slope": int((s < 0).sum()),
        "top_k": [topk(k) for k in (1, 5, 10, 20, 44, 443)],
        "reach": [reach(q) for q in (0.5, 0.8, 0.9)],
        "large_reserves_over_1000km2": {
            "reserves": int((area >= 1000).sum()),
            "area_share": float(area[area >= 1000].sum() / area.sum()),
            "net_share": float(s[area >= 1000].sum() / net),
            "gross_share": float(s[area >= 1000].clip(lower=0).sum() / gross_pos)},
        "outer_km_all_reserves_with_complete_band": edge_stats(outer_ok),
        "outer_km_reserves_with_interior_beyond_1km": edge_stats(interior),
        "interior_definition": "at least 10 valid pixels beyond the outer 1 km band in every year",
        "outer_km_reserves_with_interior_stable_counts": edge_stats(interior & stable_counts),
        "reserves_with_changing_valid_counts": sorted(whole_n.index[~stable_counts]),
        "gross_negative_top_k_share": {k: float(s.sort_values().iloc[:k].clip(upper=0).sum() / gross_neg)
                                       for k in (1, 5, 10, 30)},
        "outer_band_excluded_incomplete": int((~outer_ok).sum()),
        "band_budget": band_budget,
        "estate_total_by_year": {int(y): float(v) for y, v in whole_t.sum().items()},
        "lit_pixels_by_year": {int(y): float(v) for y, v in lit.sum().items()},
        "reserves_with_30pct_lit_pixel_jump": jumps,
        "positive_sen_slopes": int(len(pos_ids)),
        "positive_sen_slopes_surviving_level_shift_removal": step_sens,
        "top20_overlap_total_vs_mean_slope": sorted(top_total & top_mean),
        "top20_total_outside_top100_mean": sorted(top_total - set(mean_rank.nsmallest(100).index)),
        "kosciuszko": {"mean_slope_rank_among_positive": int(mean_rank[kosc]),
                       "share_of_net": float(s[kosc] / net), "share_of_gross": float(s[kosc] / gross_pos)},
        "largest_decrease": {"pa_id": s.idxmin(), "slope": float(s.min()),
                             "share_of_gross_decrease": float(s.min() / gross_neg)},
        "min_rest_total_check": min_rest_total,
        "surroundings_1km": {
            "paired_reserves_complete": int(len(B)),
            "sum_buffer_slope": float(B.slope_2013_2024.sum()),
            "sum_inside_slope_same_reserves": float(Wp.slope_2013_2024.sum()),
            "note": "1 km buffers of neighbouring reserves can overlap, so buffer totals may double count",
        },
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "inputs"}, indent=1))
    for name, tab in tables.items():
        print(f"\n{name}\n", tab.round(4).to_string(index=False))
    print("\n", top.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

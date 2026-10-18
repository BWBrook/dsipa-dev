"""Render a candidate national map of reserve contributions to the radiance budget."""
import argparse
from pathlib import Path

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

UP, DOWN, INK, MUTED, LAND = "#c2410c", "#1d4ed8", "#1f1f1f", "#5f5f5f", "#d9d9d6"
LABELS = {"NSW_N0018": ("Kosciuszko", (14, -10)), "WA_11648": ("Barrow Island", (-70, 14)),
          "WA_2803": ("Murujuga", (8, 12)), "WA_33174": ("Thevenard Island", (-92, -4)),
          "SA_0247": ("Yellabinna", (8, 8)), "CWTH_IPA20": ("Anindilyakwa", (8, 6)),
          "WA_27575": ("Neerabup", (-62, -6)), "CWTH_IPA51": ("Southern Tanami", (8, 6))}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--dir", type=Path, default=Path("analysis/reports/brightening_budget"))
    a = ap.parse_args()
    b = pd.read_csv(a.dir / "reserve_budget.csv", index_col=0)
    g = gpd.read_file(a.root / "data/processed/pa_geometries_v0_3_0.gpkg", columns=["pa_id"]).set_index("pa_id")
    shapes = g.geometry.simplify(2000).to_crs(4326)
    cent = g.loc[b.index].geometry.centroid.to_crs(4326)
    b["lon"], b["lat"] = cent.x, cent.y
    s = b.slope_2013_2024
    nz = b[s != 0].copy()
    scale = 260 / np.sqrt(np.abs(s).max())
    nz["size"] = np.sqrt(np.abs(nz.slope_2013_2024)) * scale + 3

    fig, ax = plt.subplots(figsize=(7.2, 6.2), constrained_layout=True)
    shapes.plot(ax=ax, color=LAND, linewidth=0)
    for sign, colour in ((-1, DOWN), (1, UP)):
        d = nz[np.sign(nz.slope_2013_2024) == sign].sort_values("size", ascending=False)
        ax.scatter(d.lon, d.lat, s=d["size"], facecolor=colour, alpha=0.55, edgecolor="white", lw=0.6, zorder=3)
    for pid, (name, off) in LABELS.items():
        x, y = b.loc[pid, ["lon", "lat"]]
        ax.annotate(name, (x, y), xytext=off, textcoords="offset points", fontsize=8, color=INK,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6), zorder=4)
    ax.set_xlim(112, 154.5)
    ax.set_ylim(-44.5, -10)
    ax.set_aspect(1 / np.cos(np.radians(27)))
    ax.set_axis_off()
    ref = [100, 1000]
    handles = [Line2D([], [], marker="o", ls="", markersize=np.sqrt(np.sqrt(v) * scale + 3),
                      markerfacecolor=UP, alpha=0.55, markeredgecolor="white") for v in ref]
    handles += [Line2D([], [], marker="o", ls="", markersize=7, markerfacecolor=DOWN, alpha=0.55,
                       markeredgecolor="white")]
    ax.legend(handles, ["Increase, 100", "Increase, 1,000", "Decrease (same size scale)"], frameon=False, loc="lower left",
              fontsize=8, title="Integrated OLS slope 2013–2024\n(product units × km² per year)",
              title_fontsize=8, labelspacing=1.4)
    up, down = (s > 0).sum(), (s < 0).sum()
    ax.set_title(f"Where measured radiance rose ({up} reserves) and fell ({down}), 2013–2024",
                 loc="left", fontsize=10, color=INK)
    fig.savefig(a.dir / "fig_brightening_map.png", dpi=300)


if __name__ == "__main__":
    main()

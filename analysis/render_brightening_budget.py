"""Render the candidate brightening-budget figure from the budget outputs."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator
import pandas as pd

INK, MUTED, GRID, ACCENT, POINT = "#1f1f1f", "#5f5f5f", "#e3e3e3", "#1f4e79", "#b8b8b8"
LABELS = {"NSW_N0018": "Kosciuszko", "WA_27575": "Neerabup", "VIC_4007": "Craigieburn",
          "SA_0247": "Yellabinna", "CWTH_IPA20": "Anindilyakwa", "CWTH_IPA51": "Southern Tanami",
          "NSW_N0030": "Royal", "WA_48325": "Swan River"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=Path("analysis/reports/brightening_budget"))
    a = ap.parse_args()
    b = pd.read_csv(a.dir / "reserve_budget.csv", index_col=0)
    c = pd.read_csv(a.dir / "concentration_curve.csv")
    c = c[c.slope_2013_2024 > 0]
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3), constrained_layout=True)

    ax1.plot(c["rank"], c.cum_gross_share, color=ACCENT, lw=2, label="Increase in measured light")
    ax1.plot(c["rank"], c.cum_area_share, color=MUTED, lw=1.5, ls="--", label="Reserve area")
    k50 = int((c.cum_gross_share < 0.5).sum() + 1)
    ax1.plot([k50, k50, 1], [0, 0.5, 0.5], color=MUTED, lw=0.8, ls=":")
    ax1.annotate(f"{k50} reserves supply\nhalf the increase", (k50, 0.5), xytext=(k50 * 1.6, 0.32),
                 fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax1.annotate("Kosciuszko alone", (1, c.cum_gross_share.iloc[0]), xytext=(1.25, 0.24), fontsize=8,
                 color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax1.set_xscale("log")
    ax1.xaxis.set_major_locator(FixedLocator([1, 10, 100, 500]))
    ax1.xaxis.set_minor_locator(NullLocator())
    ax1.set_xticklabels(["1", "10", "100", "500"])
    ax1.set_xlim(0.9, len(c) * 1.1)
    ax1.set_ylim(0, 1.02)
    ax1.set_xlabel("Reserves ranked by contribution (log scale)")
    ax1.set_ylabel("Cumulative share")
    ax1.grid(color=GRID, lw=0.6)
    ax1.legend(frameon=False, loc="upper left", fontsize=8)
    ax1.set_title("a  Concentration of the increase", loc="left", fontsize=9.5, color=INK)

    p = b[(b.sen_inside > 0) & (b.slope_2013_2024 > 0)].copy()
    p["rank_mean"] = p.sen_inside.rank(ascending=False)
    p["rank_total"] = p.slope_2013_2024.rank(ascending=False)
    ax2.scatter(p.rank_mean, p.rank_total, s=10, color=POINT, edgecolor="white", lw=0.3, zorder=2)
    n = len(p)
    ax2.plot([1, n], [1, n], color=MUTED, lw=0.8, ls=":", zorder=1)
    for pid, name in LABELS.items():
        if pid in p.index:
            x, y = p.loc[pid, ["rank_mean", "rank_total"]]
            ax2.scatter([x], [y], s=26, color=ACCENT, edgecolor="white", lw=0.6, zorder=3)
            ax2.annotate(name, (x, y), xytext=(4, 2), textcoords="offset points", fontsize=7.5, color=INK)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    for axis in (ax2.xaxis, ax2.yaxis):
        axis.set_major_locator(FixedLocator([1, 10, 100, 400]))
        axis.set_minor_locator(NullLocator())
    ax2.set_xticklabels(["1", "10", "100", "400"])
    ax2.set_yticklabels(["1", "10", "100", "400"])
    ax2.set_xlim(n * 1.3, 0.8)
    ax2.set_ylim(n * 1.3, 0.8)
    ax2.set_xlabel("Rank by reserve-average trend")
    ax2.set_ylabel("Rank by change in total light")
    ax2.grid(color=GRID, lw=0.6)
    ax2.set_title(f"b  Two metrics, two lists ({n} reserves)", loc="left", fontsize=9.5, color=INK)
    fig.savefig(a.dir / "fig_brightening_budget.png", dpi=300)


if __name__ == "__main__":
    main()

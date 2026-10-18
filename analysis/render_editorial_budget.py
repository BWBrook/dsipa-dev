"""Render the reviewed additive budget and matched-estimator comparison.

Uses the accepted annual means for OLS-mean ranks and the candidate budget's
reserve contributions. Numerical claims are independently replayed by
brightening_budget_audit_20261018.py. No fitted uncertainty is implied.
"""
from pathlib import Path
import argparse
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    args = parser.parse_args()
    root = args.root
    candidate = root / 'analysis/reports/brightening_budget'
    budget = pd.read_csv(candidate / 'reserve_budget.csv', index_col=0)
    curve = pd.read_csv(candidate / 'concentration_curve.csv')
    summary = json.loads((candidate / 'summary.json').read_text())
    annual_path = root / 'data/processed/pa_radiance_buffers_national_v0_3_0.csv'
    r = pd.read_csv(annual_path, usecols=['pa_id', 'zone', 'year', 'mean'])
    years = np.arange(2013, 2025)
    means = r[r.zone == 'inside'].pivot(index='pa_id', columns='year', values='mean').reindex(budget.index)[years]
    y = means.to_numpy()
    x = years - years.mean()
    slopes = ((y - y.mean(axis=1, keepdims=True)) * x).sum(axis=1) / (x*x).sum()
    slopes[np.abs(slopes) < 1e-9] = 0
    rank_mean = pd.Series(slopes, index=budget.index).rank(ascending=False)
    rank_total = budget.slope_2013_2024.rank(ascending=False)
    pos = (slopes > 0) & (budget.slope_2013_2024 > 0)
    p = pd.DataFrame({'mean_rank': rank_mean[pos], 'total_rank': rank_total[pos]})
    assert int(p.loc['NSW_N0018', 'mean_rank']) == 286
    assert int(p.loc['NSW_N0018', 'total_rank']) == 1

    ink, muted, grid, blue, orange = '#202124', '#5e6268', '#e5e7eb', '#246288', '#b9792e'
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'axes.labelcolor': ink, 'text.color': ink, 'xtick.color': muted,
                         'ytick.color': muted, 'axes.edgecolor': muted,
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig = plt.figure(figsize=(7.2, 5.6), layout='constrained')
    grid_spec = fig.add_gridspec(2, 2, height_ratios=[1.05, 1.8])
    a = fig.add_subplot(grid_spec[0, :])
    b = fig.add_subplot(grid_spec[1, 0])
    c = fig.add_subplot(grid_spec[1, 1])
    audit = json.loads((root / 'analysis/reports/brightening_budget_audit_20261018.json').read_text())
    share = [100*audit['full_2013_2024']['outer_share_band_gross'], 100*audit['interior']['outer_share_band_gross']]
    area = [100*summary['band_budget']['outer_km_area_share_all_assessable'],
            100*summary['outer_km_reserves_with_interior_beyond_1km']['outer_km_area_share']]
    yy = np.array([1.0, 0.0])
    a.barh(yy + .14, area, height=.25, color='#aab3bc', label='Sampled area')
    a.barh(yy - .14, share, height=.25, color=blue, label='Positive band contributions')
    for y0, v1, v2 in zip(yy, area, share):
        a.text(v1 + 1, y0 + .14, f'{v1:.1f}%', va='center', fontsize=8)
        a.text(v2 + 1, y0 - .14, f'{v2:.1f}%', va='center', fontsize=8)
    a.set_yticks(yy, ['All assessable reserves\n(n = 4,426)', 'Supported deeper interior\n(n = 1,398)'])
    a.set_xlim(0, 100)
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_xlabel('Share in the outermost kilometre (%)')
    a.set_title('a  Boundary contribution depends on reserve geometry', loc='left', fontweight='bold', fontsize=9)
    a.legend(loc='lower right', frameon=False, fontsize=8)
    a.grid(axis='x', color=grid, linewidth=.6)
    a.set_axisbelow(True)
    a.spines['left'].set_visible(False)
    a.tick_params(axis='y', length=0)

    curve = curve[curve.slope_2013_2024 > 0]
    b.plot(curve['rank'], 100*curve.cum_gross_share, color=blue, lw=2)
    b.axhline(50, color=muted, ls=':', lw=.8)
    b.scatter([30, 115], [100*curve.iloc[29].cum_gross_share, 100*curve.iloc[114].cum_gross_share], color=blue, s=20, zorder=3)
    b.annotate('30 reserves: 50%', (30, 50), xytext=(3, 61), fontsize=8,
               arrowprops={'arrowstyle':'-', 'color':muted, 'lw':.6})
    b.annotate('115 reserves: 80%', (115, 80), xytext=(8, 91), fontsize=8,
               arrowprops={'arrowstyle':'-', 'color':muted, 'lw':.6})
    b.set_xscale('log'); b.set_xlim(.9, 650); b.set_ylim(0, 102)
    b.xaxis.set_major_locator(FixedLocator([1, 10, 100, 500])); b.xaxis.set_minor_locator(NullLocator())
    b.set_xticklabels(['1','10','100','500'])
    b.set_xlabel('Reserve contribution rank (log scale)')
    b.set_ylabel('Cumulative positive contribution (%)')
    b.set_title('b  Concentration among reserves', loc='left', fontweight='bold', fontsize=9)
    b.grid(color=grid, linewidth=.6)

    c.scatter(p.mean_rank, p.total_rank, color='#aeb8c1', s=10, edgecolors='white', linewidth=.25, zorder=2)
    c.plot([1, 560], [1, 560], ls=':', color=muted, lw=.8, zorder=1)
    c.scatter([286], [1], color=orange, s=32, edgecolors='white', linewidth=.5, zorder=3)
    c.annotate('Kosciuszko\n286th → 1st', (286, 1), xytext=(55, 3.6), fontsize=8, color=ink,
               arrowprops={'arrowstyle':'-', 'color':orange, 'lw':.8})
    c.set_xscale('log'); c.set_yscale('log')
    c.set_xlim(.75, 720); c.set_ylim(720, .75)
    for axis in (c.xaxis, c.yaxis):
        axis.set_major_locator(FixedLocator([1, 10, 100, 500])); axis.set_minor_locator(NullLocator())
    c.set_xticklabels(['1','10','100','500']); c.set_yticklabels(['1','10','100','500'])
    c.set_xlabel('Rank by mean OLS slope')
    c.set_ylabel('Rank by integrated OLS slope')
    c.set_title('c  Same estimator, different scale', loc='left', fontweight='bold', fontsize=9)
    c.grid(color=grid, linewidth=.6)
    destination = root / 'manuscript/figures/fig_editorial_budget'
    for ext in ('png', 'pdf'):
        fig.savefig(destination.with_suffix('.'+ext), dpi=300, facecolor='white')
    print(f'{destination}: {len(p)} positive pairs; Kosciuszko ranks 286 and 1')


if __name__ == '__main__':
    main()

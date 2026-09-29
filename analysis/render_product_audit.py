#!/usr/bin/env python3
"""Render descriptive product-audit curves with separately scaled distance panels."""
from pathlib import Path
import argparse
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
parser.add_argument('--reports-dir', type=Path)
args = parser.parse_args()
root = args.root
p = args.reports_dir or root / 'analysis/reports'
(root / 'manuscript/figures').mkdir(parents=True, exist_ok=True)
h = pd.read_csv(p / 'product_hazards.csv')
d = pd.read_csv(p / 'product_distance_hazards.csv')
fig, axes = plt.subplots(2, 2, figsize=(9.4, 6.5), layout='constrained')
axes = axes.ravel()
colors = ['#0072B2', '#D55E00', '#009E73']
for key, label, color in zip(['inside', 'buffer_1km', 'buffer_5km'],
                            ['Inside reserve', '1 km surrounding', '5 km surrounding'], colors):
    x = h[h.zone.eq(key)]
    axes[0].plot(x.year, 100*x.hazard, 'o-', ms=4, label=label, color=color)
axes[0].legend(frameon=False, fontsize=8)
for ax, key, color in zip(axes[1:], ['near_<2km', 'middle_2_to_20km', 'far_>20km'], colors):
    x = d[d.stratum.eq(key)]
    ax.plot(x.year, 100*x.hazard, 'o-', ms=4, color=color)
for ax, title in zip(axes, ['a  Complete-series zone cohorts', 'b  Inside: <2 km from 2013 light',
                           'c  Inside: 2–20 km from 2013 light', 'd  Inside: >20 km from 2013 light']):
    for year in [2017, 2023]:
        ax.axvline(year, color='.7', lw=1, zorder=0)
    ax.axvline(2022, color='.35', ls=':', lw=1, zorder=0)
    ax.set(xlabel='Year', ylabel='First-positive fraction (%)', title=title)
    ax.set_xticks([2014, 2017, 2020, 2022, 2024])
    ax.set_ylim(bottom=0)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=.15)
fig.suptitle('Solid guides: 2017 pulse and 2023 increase; dotted guide: 2022 source boundary', fontsize=10)
out = root / 'manuscript/figures/fig_product_first_detections.png'
fig.savefig(out, dpi=300)
plt.close(fig)
def sha(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()
(p / 'product_figure_manifest.json').write_text(json.dumps(dict(matplotlib=matplotlib.__version__, pandas=pd.__version__,
    inputs={x:sha(p/x) for x in ['product_hazards.csv', 'product_distance_hazards.csv']},
    script_sha256=sha(Path(__file__)), output_sha256=sha(out)), indent=2)+'\n')

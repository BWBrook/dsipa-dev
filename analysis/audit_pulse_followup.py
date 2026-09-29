"""Post-review descriptive onset/persistence check; no independent onset test."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'analysis/reports'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports-dir', type=Path, default=P)
    args = parser.parse_args()
    reports = args.reports_dir
    source = reports / 'product_annual_series.csv'
    x = pd.read_csv(source)
    assert not x.duplicated(['zone', 'pa_id']).any()
    rows = []
    for zone, group in x.groupby('zone'):
        for year in range(2014, 2025):
            onset = group[group.first_positive_year.eq(year)]
            n = len(onset)
            positive_next = int(onset[f'mean_{year+1}'].gt(0).sum()) if year < 2024 else None
            rows.append(dict(zone=zone, first_year=year, n_first=n,
                             n_positive_next_year=positive_next,
                             next_year_fraction=positive_next/n if n and positive_next is not None else None))
    out = reports / 'product_onset_persistence.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    inside = x[x.zone.eq('inside')]
    late = inside[inside.first_positive_year.ge(2022)]
    assert len(late) == 78
    result = dict(analysis_status='Exploratory follow-up after Fable messages 207-208; descriptive only.',
                  late_positive_n=len(late), first_2023_2024=int(late.first_positive_year.ge(2023).sum()),
                  inputs={source.name:sha(source)}, outputs={out.name:sha(out)},
                  script_sha256=sha(Path(__file__)), python=platform.python_version(), pandas=pd.__version__)
    (reports / 'product_pulse_followup_manifest.json').write_text(json.dumps(result, indent=2)+'\n')

if __name__ == '__main__':
    main()

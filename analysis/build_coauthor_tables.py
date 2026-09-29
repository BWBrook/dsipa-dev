#!/usr/bin/env python3
"""Render compact SI tables from preserved, tracked summary evidence."""
from pathlib import Path
import argparse
import json
import pandas as pd


def _audit_counts(reports):
    """Read S4/S5 denominators from the preserved audit receipts."""
    interior = json.loads(
        (reports / 'interior_area_audit/interior_area_summary.json').read_text(encoding='utf-8')
    )['cohort']
    edge = json.loads(
        (reports / 'edge_followup/edge_followup_summary.json').read_text(encoding='utf-8')
    )['cohort']
    counts = {
        'matched': int(interior['ring_matched_n']),
        'excluded': int(interior['ring_excluded_n']),
        'positive': int(edge['positive_whole_matched_n']),
    }
    if counts['matched'] + counts['excluded'] != int(interior['original_paired_n']):
        raise ValueError('Interior audit cohort counts do not reconcile.')
    return counts


def _correction_table(summary_path, *, table_label='S6'):
    """Render optional S6 from corrected support-count receipts."""
    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    variants = summary.get('variants')
    if not isinstance(variants, dict):
        bg = summary.get('baseline_to_geometry', {})
        bc = summary.get('baseline_to_corrected', {})
        gc = summary.get('geometry_to_corrected', {})
        variants = {
            'Baseline': {'paired': bg.get('old_paired'), 'quadrants': bg.get('old_categories')},
            'Geometry-only': {'paired': bg.get('new_paired'), 'quadrants': bg.get('categories')},
            'Corrected': {
                'paired': bc.get('new_paired', gc.get('new_paired')),
                'quadrants': bc.get('categories', gc.get('categories')),
            },
        }
    rows = []
    for label in ('Baseline', 'Geometry-only', 'Corrected'):
        item = variants.get(label) or variants.get(label.lower().replace('-', '_'))
        if not isinstance(item, dict):
            raise ValueError(f'Spatial correction summary lacks {label} variant.')
        paired = item.get('paired', item.get('paired_n'))
        quadrants = item.get('quadrants', item.get('quadrant_counts'))
        if paired is None or not isinstance(quadrants, dict):
            raise ValueError(f'Spatial correction summary lacks paired/Q1-Q4 counts for {label}.')
        values = [int(quadrants.get(q, 0)) for q in ('Q1', 'Q2', 'Q3', 'Q4')]
        if sum(values) != int(paired):
            raise ValueError(f'{label} quadrant counts do not sum to paired count.')
        rows.append(f'| {label} | {int(paired):,} | ' + ' | '.join(f'{v:,}' for v in values) + ' |')
    return [
        f'**Table {table_label}. Historical-support sensitivity of paired categories after spatial correction.**',
        '',
        'The archived baseline used coarse buffer geometry and land masking. The geometry-only comparison corrects boundaries and arc precision; the corrected analysis also replaces the land source. Each row uses its own eligible cohort.',
        '',
        '| Support | Paired reserves | Q1 | Q2 | Q3 | Q4 |',
        '| --- | ---: | ---: | ---: | ---: | ---: |',
        *rows,
    ]


def _interior_correction_table(summary_path):
    summary = json.loads(summary_path.read_text())
    lines = ['', '**B. Old–corrected 1–5 km band eligibility and sign agreement.**', '',
        'Old and new refer to the archived and corrected supports. Common counts require a usable band slope in both versions. Changed signs are counted only among those common reserves. The fixed paired cohort holds inside–surrounding eligibility constant; the joint cohort allows surrounding eligibility to change.', '',
        '| Cohort | Old | New | Common | Gained | Lost | Changed signs |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for key, label in [('all_reserves','All reserves'),('fixed_common_paired','Fixed paired cohort'),('joint_paired_and_band','Joint paired and band')]:
        row = summary[key]
        if row['old_eligible'] != row['common'] + row['lost'] or row['new_eligible'] != row['common'] + row['gained']:
            raise ValueError('Interior correction eligibility does not reconcile')
        lines.append('| ' + label + ' | ' + ' | '.join(f"{row[k]:,}" for k in ['old_eligible','new_eligible','common','gained','lost','sign_changed_common']) + ' |')
    return lines


def audit_tables(root, *, omit_layer_b=False):
    """Render the audit tables from their full-precision descriptive outputs."""
    reports = root / 'analysis/reports'
    h = pd.read_csv(reports / 'product_hazards.csv')
    h = h[h.zone.eq('inside')].set_index('year')
    d = pd.read_csv(reports / 'product_distance_hazards.csv').set_index(['year', 'stratum'])
    lines = [
        "```{=latex}\n\\clearpage\n```\n\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```",
        "",
        f'**Table {"S2" if omit_layer_b else "S3"}. Annual first-positive inside observations by fixed distance from 2013 detected light.**',
        '',
        'Entries are first-positive reserves / reserves still at risk. All histories contain 12 valid annual summaries and begin at zero in 2013. Fractions describe product transitions, not ecological onset.',
        '',
        '| Year | All inside | <2 km | 2–20 km | >20 km |',
        '| ----: | --------: | --------: | --------: | --------: |',
    ]
    for year in range(2014, 2025):
        rows = [h.loc[year]] + [d.loc[(year, key)] for key in ['near_<2km', 'middle_2_to_20km', 'far_>20km']]
        vals = [f'{int(row.first_positive):,}/{int(row.at_risk):,}' for row in rows]
        lines.append('| ' + str(year) + ' | ' + ' | '.join(vals) + ' |')
    counts = _audit_counts(reports)
    lines += ['', '', f'**Table {"S3" if omit_layer_b else "S4"}. Category transitions after replacing the whole-reserve mean with the 1–5 km interior band.**', '',
        f'The 1 km unprotected-land surrounding slope is unchanged. Columns show band-based categories; rows show original whole-reserve categories. The common cohort contains {counts["matched"]:,} reserves, of which {counts["positive"]:,} originally had a positive inside slope. The {counts["excluded"]:,} excluded reserves had no usable band-year summary. Counts measure sensitivity to spatial support and do not identify the source of radiance.', '',
        '| Original | Q1 | Q2 | Q3 | Q4 | Total |',
        '| -------- | --: | --: | --: | --: | --: |']
    t = pd.read_csv(reports / 'interior_area_audit/interior_area_quadrant_transitions.csv')
    t = t.pivot(index='original_quadrant', columns='ring_quadrant', values='n')
    for q in ['Q1', 'Q2', 'Q3', 'Q4']:
        vals = t.loc[q].tolist()
        lines.append('| ' + q + ' | ' + ' | '.join(f'{int(v):,}' for v in vals + [sum(vals)]) + ' |')
    vals = t.sum().tolist()
    lines.append('| Total | ' + ' | '.join(f'{int(v):,}' for v in vals + [sum(vals)]) + ' |')
    edge = reports / 'edge_followup'
    lines += ['', '```{=latex}\n\\clearpage\n```\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```', '',
        f'**Table {"S4" if omit_layer_b else "S5"}. Magnitude and spatial support of positive whole-reserve slopes.**', '',
        '**A. Full eligible positive-slope cohort.** Terciles use whole-reserve slopes, with equal-count groups where possible and no ties at the two boundaries. Area is summed whole-polygon area; it may double-count designations and is not illuminated area. Slopes are product-scaled units per year.', '',
        '| Slope tercile | n | Slope range | Median slope | Share of positive-class area (%) |',
        '| --- | ---: | ---: | ---: | ---: |']
    terciles = pd.read_csv(edge / 'edge_followup_positive_terciles.csv')
    positive_total = int(terciles['n'].sum())
    if positive_total != 420:
        raise ValueError(f'Expected 420 positive whole-reserve tercile records, found {positive_total}.')
    lines[lines.index('**A. Full eligible positive-slope cohort.** Terciles use whole-reserve slopes, with equal-count groups where possible and no ties at the two boundaries. Area is summed whole-polygon area; it may double-count designations and is not illuminated area. Slopes are product-scaled units per year.')] = f'**A. Full eligible positive-slope cohort ({positive_total:,} reserves).** Terciles use whole-reserve slopes, with equal-count groups where possible and no ties at the two boundaries. Area is summed whole-polygon area; it may double-count designations and is not illuminated area. Slopes are product-scaled units per year.'
    for row, label in zip(terciles.itertuples(), ['Lowest', 'Middle', 'Highest']):
        lines.append(f'| {label} | {row.n} | {row.slope_min:.6f}–{row.slope_max:.6f} | {row.slope_median:.6f} | {100*row.area_share_positive_whole:.2f} |')
    lines += ['', f'**B. Positive whole-reserve slopes within the matched {counts["matched"]:,}-reserve cohort ({counts["positive"]:,} reserves).** Both bands retain the same annual pixel and temporal thresholds. Separate median pairwise slopes are not additive. A zero slope need not mean an all-zero annual series.', '',
        '| 0–1 km slope | 1–5 km slope | n |', '| --- | --- | ---: |']
    x = pd.read_csv(edge / 'edge_followup_band_slopes.csv')
    x = x[x.whole_sign.eq('positive')]
    groups = x.groupby(['ring_0_1km_sign', 'ring_1_5km_sign']).size().sort_values(ascending=False)
    for (a, b), n in groups.items():
        lines.append(f'| {a.capitalize()} | {b.capitalize()} | {n} |')
    lines += ['', 'These review-stage descriptive comparisons assess magnitude and spatial support. They do not identify physical light sources, ecological effects or the cause of product non-detection.']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--spatial-correction', action='store_true',
                        help='Append Table S6 from spatial_correction_summary.json.')
    parser.add_argument('--omit-layer-b', action='store_true',
                        help='Build the active Layer A candidate without Layer B Table S2.')
    args = parser.parse_args()
    root = args.root
    watch = pd.read_csv(root / 'analysis/reports/layerA_watchlists_uncertainty.csv')
    assert len(watch) == 60
    provisional=set()
    if args.spatial_correction:
        screening=pd.read_csv(root/'analysis/reports/reserve_screening_results.csv')
        provisional=set(screening.loc[screening.provisional_surrounding_comparison,'pa_id'])
    s1_intro = ('Each set contains the first 20 entries in its preserved source order. Sets A, B and C are ordered by descending inside slope, surrounding slope, and inside-minus-surrounding difference, respectively. Set A requires a positive inside slope; B a positive surrounding and non-positive inside slope; C a positive inside slope exceeding the surrounding slope. These are illustrative high-magnitude subsets of those metrics, not management priorities. All slopes and ranges use scaled product units per year. The range is the 2.5th-97.5th percentiles of the independently resampled inside slopes, not a confidence interval. The final column is the fraction of those slopes greater than zero; the denominator varies with IBRA selection (Supporting Methods S1). Full identifiers, IBRA assignments, areas and draw counts are retained in the accompanying source table.')
    if args.spatial_correction:
        s1_intro += ' A dagger marks a surrounding comparison that is provisional because the site is near a documented coastline-source exception; local map validation is required. Inside slopes and temporal resampling are unchanged by this flag.'
    parts = ['## Supplementary Tables',
        '**Table S1. Selected protected areas with full-period slopes and marginal temporal sensitivity.**',
        s1_intro]
    groups = [('inside_brightening', 'A. Positive inside slopes'),
              ('external_pressure', 'B. Positive surrounding slopes with non-positive inside slopes'),
              ('internalisation', 'C. Positive inside-minus-surrounding contrasts')]
    for key, title in groups:
        frame = watch[watch.category_key.eq(key)].sort_values('category_rank')
        assert len(frame) == 20
        if key == 'external_pressure':
            parts.append('```{=latex}\n\\clearpage\n```')
        parts.extend([f'### {title}',
            '| Reserve (state) | Inside | Surrounding | Difference | Resampling range | Positive fraction |',
            '| -------------------------------- | -----------: | -------------: | -----------: | ----------------------- | ------------: |'])
        for row in frame.itertuples():
            label=row.name + ('†' if row.pa_id in provisional else '')
            parts.append(f'| {label} ({row.state}) | {row.slope_inside:.3f} | {row.slope_buffer_1km:.3f} | {row.retention_index_1km:.3f} | {row.inside_slope_ci_low:.3f} to {row.inside_slope_ci_high:.3f} | {row.inside_prob_slope_gt0:.3f} |')
        parts.append('')
    if not args.omit_layer_b:
        parts.extend([
            '```{=latex}\n\\clearpage\n```\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```',
            '**Table S2. Occurrence-record classification and illustrative ALAN-shuffle benchmarks.**',
            'Coefficients are fold means +/- fold SD, describing model variation rather than confidence intervals. Primary and shuffle rows use the balanced NSW BioNet sample inside protected areas or within 10 km. Each shuffle is one seeded realisation, not a sampled null distribution. The all-provider comparison is descriptive. Values are preserved from the model report generated on 2026-01-06.',
            '| Design | Records per class | Indicator coefficient | Intensity coefficient | AUC | Log loss |',
            '| -------------------------------- | ------------: | ---------------------- | ---------------------- | --------: | ----------: |',
            '| NSW BioNet primary | 50,281 | 1.316 +/- 0.128 | -0.354 +/- 0.024 | 0.545 | 0.689 |',
            '| Within-block shuffle | 50,281 | 0.202 +/- 0.086 | -0.027 +/- 0.021 | 0.505 | 0.695 |',
            '| Within-IBRA-by-year shuffle | 50,281 | 0.163 +/- 0.063 | -0.001 +/- 0.008 | 0.517 | 0.695 |',
            '| All-provider sensitivity | 56,883 | 0.732 +/- 0.330 | -0.332 +/- 0.094 | 0.557 | 0.700 |',
            '',
            'At a positive product value r, the fitted log-odds contrast with zero equals the indicator coefficient plus the intensity coefficient multiplied by log(1+r). In the primary sample, 27.8% of microbat and 25.7% of passerine records were inside protected areas; zero-ALAN fractions were 65.7% and 65.1%. These describe the pre-shuffle model input after scope restriction and balancing, not population prevalence. Shuffling changes exposure-label pairing. Provider matching does not align survey protocol, acoustic-detector use, habitat, access or taxon-specific detectability.',
        ])
    # Keep adjacent table rows together; separate paragraphs and table blocks.
    output = []
    for part in parts:
        if output and not (part.startswith('|') and output[-1].startswith('|')):
            output.append('')
        output.append(part)
    rendered='\n'.join(output).rstrip() + '\n\n' + audit_tables(root, omit_layer_b=args.omit_layer_b) + '\n'
    if args.spatial_correction:
        correction_path=root/'analysis/reports/spatial_correction_summary.json'
        if not correction_path.is_file():
            raise FileNotFoundError(f'Missing requested spatial correction summary: {correction_path}')
        correction_label = 'S5' if args.omit_layer_b else 'S6'
        interior_path=root/'analysis/reports/interior_correction/interior_correction_summary.json'
        lines = _correction_table(correction_path, table_label=correction_label)
        lines[4:4] = ['**A. Paired inside–surrounding categories.**', '']
        lines += _interior_correction_table(interior_path)
        rendered += '\n```{=latex}\n\\clearpage\n```\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n' + '\n'.join(lines) + '\n'
    (root/'manuscript/text/supplementary_tables.md').write_text(rendered)


if __name__ == '__main__':
    main()

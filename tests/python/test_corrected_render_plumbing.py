import hashlib
import json
from pathlib import Path

import pytest

from analysis.build_coauthor_tables import _correction_table, audit_tables
from analysis.render_coauthor_figures import _manifest_contract, _quadrant_label, build_parser


def _write_manifest(root: Path, *, include_report: bool = True) -> Path:
    names = [
        'pa_trends_v0_3_0.csv',
        'pa_radiance_buffers_national_v0_3_0.csv',
        'pa_risk_rankings_v0_3_0.csv',
        'pa_geometries_v0_3_0.csv',
        'pa_geometries_v0_3_0.gpkg',
        'pa_trend_bootstrap_summary_v0_3_0.csv',
        'coauthor_example_series.csv',
        'pa_edge_profiles_national_v0_3_0.csv',
    ]
    if include_report:
        names.append('layerB_modelling_report.md')
    entries = {}
    for name in names:
        relative = (
            Path('analysis/reports') / name
            if name in {'coauthor_example_series.csv', 'layerB_modelling_report.md'}
            else Path('data/processed') / name
        )
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(name.encode())
        entries[name] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
    manifest = root / 'input_manifest.json'
    manifest.write_text(json.dumps({'analysis_id': 'spatial-correction-20260919', 'files': entries}))
    return manifest


def test_manifest_contract_requires_every_consumed_report(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path, include_report=False)
    with pytest.raises(ValueError, match='layerB_modelling_report.md'):
        _manifest_contract(tmp_path, manifest, include_correction=False)


def test_manifest_contract_omits_layerb_report_for_candidate(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path, include_report=False)
    contract = _manifest_contract(
        tmp_path, manifest, include_correction=False, include_layer_b=False
    )
    assert 'layerB_modelling_report.md' not in contract.files


def test_manifest_contract_validates_corrected_inputs(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    # The correction summary is consumed only when the corresponding mode is
    # requested, so its absence is a deliberate fail-closed error.
    with pytest.raises(ValueError, match='spatial_correction_summary.json'):
        _manifest_contract(tmp_path, manifest, include_correction=True)

    correction = tmp_path / 'analysis/reports/spatial_correction_summary.json'
    correction.write_text('{}')
    entries = json.loads(manifest.read_text())
    entries['files']['spatial_correction_summary.json'] = {
        'sha256': hashlib.sha256(correction.read_bytes()).hexdigest(),
        'bytes': correction.stat().st_size,
    }
    manifest.write_text(json.dumps(entries))
    contract = _manifest_contract(tmp_path, manifest, include_correction=True)
    assert contract.analysis_id == 'spatial-correction-20260919'
    assert contract.files['spatial_correction_summary.json'] == correction


def test_trajectory_label_uses_actual_signs() -> None:
    assert _quadrant_label(0.2, -0.1) == 'Q4: surrounding only positive'
    assert _quadrant_label(-0.1, 0.2) == 'Q2: inside only positive'


def test_candidate_flags_and_table_renumbering() -> None:
    args = build_parser().parse_args(['--data-root', '.', '--output-root', '.', '--omit-layer-b'])
    assert args.omit_layer_b is True
    rendered = audit_tables(Path('.'), omit_layer_b=True)
    assert '**Table S2. Annual first-positive' in rendered
    assert '**Table S3. Category transitions' in rendered
    assert '**Table S4. Magnitude and spatial support' in rendered
    assert 'Occurrence-record classification and illustrative ALAN-shuffle benchmarks' not in rendered


def test_correction_table_reports_support_variants(tmp_path: Path) -> None:
    summary = tmp_path / 'corrected-summary-test.json'
    summary.write_text(json.dumps({'variants': {
        'Baseline': {'paired': 3, 'quadrants': {'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 0}},
        'Geometry-only': {'paired': 2, 'quadrants': {'Q1': 0, 'Q2': 1, 'Q3': 1, 'Q4': 0}},
        'Corrected': {'paired': 2, 'quadrants': {'Q1': 0, 'Q2': 0, 'Q3': 1, 'Q4': 1}},
    }}))
    lines = _correction_table(summary)
    assert any('| Corrected | 2 | 0 | 0 | 1 | 1 |' in line for line in lines)
    assert any('Each row uses its own eligible cohort' in line for line in lines)

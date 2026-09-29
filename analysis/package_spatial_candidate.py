#!/usr/bin/env python3
"""Package the current private spatial candidate with an explicit allowlist."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

DATA = ['pa_buffer_validity_v0_3_0.csv','pa_edge_profiles_national_v0_3_0.csv','pa_geometries_v0_3_0.csv','pa_geometries_v0_3_0.gpkg','pa_ibra_assignment_v0_3_0.csv','pa_radiance_buffers_national_v0_3_0.csv','pa_risk_rankings_v0_3_0.csv','pa_trend_bootstrap_summary_v0_3_0.csv','pa_trends_v0_3_0.csv']
SCRIPTS = ['run_spatial_correction','acquire_corrected_coastline','check_spatial_precision','screen_aims_coastline_exceptions','compare_aims_coastline_full_split','synthesise_spatial_correction','run_manuscript_audits','compare_baseline_input_identities','prepare_public_spatial_baseline','audit_product_continuity','audit_interior_area','audit_edge_followup','audit_pulse_followup','coauthor_evidence','input_contract','compare_spatial_interior_correction','render_coauthor_figures','render_product_audit','build_coauthor_tables','render_rsec_sources','render_rsec_pdf_layout','normalize_rsec_docx','annotate_makedoc_manifest','export_reserve_screening','package_spatial_candidate']
TESTS = ['annotate_makedoc_manifest','layerA_spatial_support','input_contract','corrected_render_plumbing','buffer_validity','prepare_public_spatial_baseline','audit_product_continuity','audit_interior_area','audit_edge_followup','coauthor_evidence','spatial_correction_comparison','trends','pa_geometry','risk_rankings']
FIGURES = ['layerA_baseline_map','layerA_trend_distribution','layerA_retention_quadrant','layerA_example_trajectories','layerA_edge_profiles_aggregate','layerA_trend_uncertainty_forest','product_first_detections']
REPORTS = ['spatial_correction_acceptance_review_20260919.md','spatial_document_qa_20260919.md','spatial_private_package_validation.json','layerB_review_repair_20260919.md','spatial_correction_summary.json','spatial_correction_input_manifest.json','spatial_correction_render_input_manifest.json','spatial_schema_amendment.json','spatial_correction_support_validation_20260919.md','spatial_correction_support_validation_20260919.json','spatial_candidate_audit_orchestration_manifest.json','spatial_correction_20260919_protocol.md','spatial_correction_20260919_coastline.md','spatial_public_reproduction_validation.json','spatial_public_raster_identity_validation.json','spatial_known_coastline_exceptions.csv','spatial_coast_exception_gains.png','spatial_coast_exception_gains_receipt.json','coastline_exception_sensitivity.json','reserve_screening_results.csv','coauthor_evidence.json','coauthor_example_series.csv','layerA_watchlists_uncertainty.csv','layerA_denominators_and_censoring.csv','layerA_edge_profile_decision.csv','render_manifest.json','product_figure_manifest.json','release_input_reconciliation_20260919.md']
PRODUCT = ['annual_series.csv','audit_manifest.json','baseline_distances.csv','cohort_coverage.csv','distance_hazards.csv','distance_hazards_stable_count.csv','distance_state_context.csv','first_positive_2022.csv','hazards.csv','inside_distance_series.csv','inside_support.csv','onset_persistence.csv','pulse_followup_manifest.json','pixel_transitions.csv','raster_histograms.csv','raster_metadata.json','floor_summary.csv','floor_manifest.json','floor_exceptions.csv','lineage_review.md']
DIRS = ['src/python/dsipa','tests/fixtures','manuscript/text','csl','analysis/reports/interior_area_audit','analysis/reports/edge_followup','analysis/reports/interior_correction','analysis/reports/spatial_execution_20260919']


def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def collect(root):
    names=['pyproject.toml','uv.lock','LICENSE','analysis/makedoc.sh','settings/build.yaml','settings/layerA_reference_contract_v0_3_0.json','references/refs.yaml','manuscript/authors.yaml','manuscript/submission/rsec/submission_authors.yaml','manuscript/submission/rsec/supplementary_frontmatter.md','manuscript/submission/rsec/final_read_guide.md','manuscript/submission/rsec/submission_counts.md','manuscript/submission/rsec/figure_production_inventory.md','docs/spatial_reproduction_20260919.md']
    names += ['analysis/'+s+'.py' for s in SCRIPTS]
    names += ['tests/python/test_'+s+'.py' for s in TESTS]
    names += ['data/processed/'+n for n in DATA]
    names += ['manuscript/figures/fig_'+n+'.png' for n in FIGURES]
    names += ['analysis/reports/'+n for n in REPORTS]
    names += ['analysis/reports/product_'+n for n in PRODUCT]
    names += ['analysis/reports/'+variant+'_'+kind+'.csv' for variant in ['baseline_to_geometry','geometry_to_corrected','baseline_to_corrected'] for kind in ['category_transitions','reserve_changes']]
    errors=['Missing mandatory file: '+n for n in names if not (root/n).is_file()]
    for n in DIRS:
        if not (root/n).is_dir():errors.append('Missing mandatory directory: '+n)
    paths={root/n for n in names if (root/n).is_file()}
    for n in DIRS:
        paths.update(p for p in (root/n).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    for n in ['run_contract.json','extraction_manifest.json','raster_manifest.json','geometry_diagnostics.json','runtime_manifest.json','part_completion_validation.json','source_snapshot/run_spatial_correction.py','source_snapshot/dsipa/layerA_national.py']:
        if not (root/'analysis/reports/spatial_execution_20260919'/n).is_file():errors.append('Missing execution receipt: '+n)
    if errors:raise ValueError('\n'.join(errors))
    return sorted(paths)


README = '''# DSIPA corrected spatial candidate — private, 19 September 2026

This package contains the corrected analysis inputs, source, reserve-level
screening results and audit evidence. It is prepared for private review, not
published software or data. The public Zenodo dataset identifies the earlier
baseline; corrected surrounding and inward-band results are held here.

Start with `docs/spatial_reproduction_20260919.md`. Install Python 3.12 and use
`uv sync --extra dev`, then `uv run python -m pytest`. For the reserve-level
results, use `analysis/reports/reserve_screening_results.csv`: it includes
eligibility and provisional coastline flags. Nine paired comparisons require
local coastline validation; their exclusion sensitivity accompanies the table.

To check the supplied derived evidence without downloading rasters:

```bash
uv run python analysis/run_manuscript_audits.py --data-dir data/processed --input-manifest analysis/reports/spatial_correction_render_input_manifest.json --output-dir /tmp/dsipa-reproduced-audits --existing-product-audit analysis/reports
uv run python analysis/render_coauthor_figures.py --data-root . --output-root /tmp/dsipa-reproduced-figures --input-manifest analysis/reports/spatial_correction_render_input_manifest.json --spatial-correction --omit-layer-b
```

`analysis/reports/spatial_execution_20260919/` preserves the executed national
runner, engine and input/output/runtime contracts. Current source additionally
normalizes polygonal components before buffering, directs the legacy CLI away
from the primary pipeline, accepts verified public baseline byte identities,
and restores the buffer-validity schema-version column. The normalization
spot-check proves identical affected pixels; the metadata amendment proves
unchanged analytical fields. The original extraction remains sealed separately.

Raw night-light rasters, raw ALA records, private correspondence and Git history
are excluded. Optional numerical Layer B is absent from the paper; historical
research code may remain in the library but is not a claimed reproduced result.
Makedoc is an external build dependency at `$HOME/work/makedoc`; the accompanying
reading bundle carries the PDFs and editable Word files. Public release and
submission require separate authorisation. Check file integrity with
`sha256sum -c SHA256SUMS`.
'''
MAKEFILE = '''SHELL := /bin/bash
MAKEDOC_ROOT ?= $(HOME)/work/makedoc
PROFILE ?= submission
.PHONY: test build ms-check ms-build
test:
\tuv run python -m pytest
build:
\tuv build
ms-check:
\tMAKEDOC_ROOT=$(MAKEDOC_ROOT) PROFILE=$(PROFILE) analysis/makedoc.sh check
ms-build:
\tMAKEDOC_ROOT=$(MAKEDOC_ROOT) PROFILE=$(PROFILE) analysis/makedoc.sh all
'''


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output',type=Path,required=True);p.add_argument('--dry-run',action='store_true');p.add_argument('--validate',action='store_true');a=p.parse_args();root=a.root.resolve();files=collect(root)
    print(json.dumps({'files':len(files)+2,'bytes':sum(f.stat().st_size for f in files),'output':str(a.output)},indent=2))
    if a.dry_run or not a.validate:return
    if a.output.exists() and any(a.output.iterdir()):raise ValueError('Refusing nonempty candidate directory')
    for f in files:
        dst=a.output/f.relative_to(root);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dst)
    (a.output/'README.md').write_text(README);(a.output/'Makefile').write_text(MAKEFILE)
    records=[{'path':str(f.relative_to(a.output)),'bytes':f.stat().st_size,'sha256':digest(f)} for f in sorted(a.output.rglob('*')) if f.is_file()]
    (a.output/'SHA256SUMS').write_text(''.join(f"{v['sha256']}  {v['path']}\n" for v in records))
    (a.output/'FILE_MANIFEST.json').write_text(json.dumps({'analysis_id':'spatial-correction-20260919','status':'private candidate','files':records},indent=2)+'\n')

if __name__=='__main__':main()

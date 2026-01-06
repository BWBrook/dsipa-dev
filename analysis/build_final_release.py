"""Build final release artefact folder (WP0.18)."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root

OUTPUTS = [
    "analysis/reports/reproducibility_audit.md",
    "analysis/reports/figure_inventory.md",
    "analysis/reports/risk_rankings_and_quadrants.md",
    "analysis/reports/trends_methods_and_sanity.md",
    "analysis/reports/pa_trend_uncertainty.md",
    "analysis/reports/pa_trend_dominance_matrix.csv",
    "analysis/reports/layerB_modelling_report.md",
    "analysis/reports/layerB_qc_extended.md",
    "analysis/reports/layerB_scope_coverage.md",
    "analysis/reports/layerB_exposure_qc.md",
    "analysis/reports/layerB_gonogo.md",
    "analysis/reports/layerB_ibra_summary.md",
    "analysis/reports/layerB_ibra_effects.csv",
    "analysis/reports/output_schema_reference.md",
    "data/processed/layerB_model_input_summary_v0_3_0.csv",
    "data/processed/layerB_ibra_summary_v0_3_0.csv",
    "data/processed/pa_ibra_assignment_v0_3_0.csv",
    "data/processed/pa_trend_bootstrap_summary_v0_3_0.csv",
    "manuscript/text/manuscript_draft.md",
    "manuscript/figures/fig_layerA_baseline_map.png",
    "manuscript/figures/fig_layerA_trend_distribution.png",
    "manuscript/figures/fig_layerA_retention_quadrant.png",
    "manuscript/figures/fig_layerA_edge_profiles_aggregate.png",
    "manuscript/figures/fig_layerA_trend_uncertainty_forest.png",
    "manuscript/figures/fig_layerA_trend_dominance.png",
    "manuscript/figures/fig_layerB_alan_effects.png",
    "manuscript/figures/fig_layerB_exposure_summary.png",
    "manuscript/figures/fig_layerB_occurrence_counts.png",
    "manuscript/figures/fig_layerB_occurrence_density.png",
    "manuscript/figures/fig_layerB_ibra_intensity_forest.png",
]


def main() -> int:
    root = find_repo_root()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    artefact_dir = root / "artefacts" / f"final_release_{stamp}"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for rel in OUTPUTS:
        src = root / rel
        if not src.exists():
            continue
        shutil.copyfile(src, artefact_dir / src.name)
        copied.append(src.name)

    manifest = build_manifest(
        run_id=f"final_release_{stamp}",
        wp="WP0.18",
        root=root,
        outputs=copied,
        inputs=["CAPAD 2024", "Zenodo nightlights v0.4", "ALA occurrence downloads"],
        require_clean=True,
        notes="Final reproducibility artefact pack (WP0.18)",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "Final reproducibility artefact pack for DSIPA-NBS (WP0.18).\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Evidence inventory and reproducibility-audit helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from dsipa.paths import find_repo_root


DEFAULT_MD = "analysis/reports/evidence_reconciliation.md"
DEFAULT_JSON = "analysis/reports/evidence_reconciliation.json"
DEFAULT_AUDIT = "analysis/reports/reproducibility_audit.md"
DEFAULT_MAX_HASH_MB = 512


@dataclass(frozen=True)
class ExpectedFile:
    path: str
    group: str
    required: bool = True
    expected_sha256: str | None = None
    note: str = ""
    normalize_crlf: bool = False


EXPECTED_FILES: tuple[ExpectedFile, ...] = (
    ExpectedFile(
        "data/processed/pa_geometries_v0_3_0.csv",
        "Layer A core",
        expected_sha256="781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b",
    ),
    ExpectedFile(
        "data/processed/pa_geometries_v0_3_0.gpkg",
        "Layer A core",
        expected_sha256="0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11",
    ),
    ExpectedFile(
        "data/processed/pa_radiance_buffers_national_v0_3_0.csv",
        "Layer A core",
        expected_sha256="493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e",
    ),
    ExpectedFile(
        "data/processed/pa_edge_profiles_national_v0_3_0.csv",
        "Layer A core",
        expected_sha256="9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888",
    ),
    ExpectedFile(
        "data/processed/pa_buffer_validity_v0_3_0.csv",
        "Layer A core",
        expected_sha256="407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25",
    ),
    ExpectedFile(
        "data/processed/pa_trends_v0_3_0.csv",
        "Layer A trends",
        expected_sha256="d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f",
    ),
    ExpectedFile(
        "data/processed/pa_risk_rankings_v0_3_0.csv",
        "Layer A trends",
        expected_sha256="554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a",
    ),
    ExpectedFile(
        "data/processed/pa_ibra_assignment_v0_3_0.csv",
        "Layer A uncertainty",
        expected_sha256="3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf",
    ),
    ExpectedFile(
        "data/processed/pa_trend_bootstrap_summary_v0_3_0.csv",
        "Layer A uncertainty",
        expected_sha256="cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920",
    ),
    ExpectedFile(
        "data/processed/layerB_occurrence_summary_v0_3_0.csv",
        "Layer B",
        expected_sha256="ec7746a882675b4955b7d455cddae2f9851bde55d16900cf6b32979346f77474",
    ),
    ExpectedFile(
        "data/processed/layerB_ala_license_ledger_v0_3_0.csv",
        "Layer B",
        expected_sha256="a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0",
        note="Checksum is computed after CRLF-to-LF normalization because ALA citation fields contain embedded line endings that vary across checkouts.",
        normalize_crlf=True,
    ),
    ExpectedFile(
        "data/processed/layerB_model_input_summary_v0_3_0.csv",
        "Layer B",
        expected_sha256="f42e9fea29dea812f54e4e9a02fafa3c7d6382e499d20e31b267b84be9346575",
    ),
    ExpectedFile(
        "data/processed/layerB_ibra_summary_v0_3_0.csv",
        "Layer B",
        expected_sha256="ed117aadd0c700c8dd0c7180714112fd212567f4b1ec56d0c8464f2e77d00a0d",
    ),
    ExpectedFile(
        "data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz",
        "Layer B large ignored",
        note="Ignored by git; needed to rerun Layer B modelling without re-downloading ALA.",
    ),
    ExpectedFile(
        "data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz",
        "Layer B large ignored",
        note="Ignored by git; needed to rerun Layer B modelling without re-downloading ALA.",
    ),
    ExpectedFile("analysis/reports/national_layerA_coverage_and_sanity.md", "Reports"),
    ExpectedFile("analysis/reports/trends_methods_and_sanity.md", "Reports"),
    ExpectedFile("analysis/reports/risk_rankings_and_quadrants.md", "Reports"),
    ExpectedFile("analysis/reports/pa_trend_uncertainty.md", "Reports"),
    ExpectedFile("analysis/reports/pa_trend_dominance_matrix.csv", "Reports"),
    ExpectedFile("analysis/reports/layerB_modelling_report.md", "Reports"),
    ExpectedFile("analysis/reports/layerB_qc_extended.md", "Reports"),
    ExpectedFile("analysis/reports/layerB_scope_coverage.md", "Reports"),
    ExpectedFile("analysis/reports/layerB_ibra_summary.md", "Reports"),
    ExpectedFile("analysis/reports/layerB_ibra_effects.csv", "Reports"),
    ExpectedFile("analysis/reports/figure_inventory.md", "Reports"),
    ExpectedFile("analysis/reports/output_schema_reference.md", "Reports"),
    ExpectedFile("manuscript/figures/fig_layerA_baseline_map.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerA_trend_distribution.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerA_retention_quadrant.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerA_edge_profiles_aggregate.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerA_trend_uncertainty_forest.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerA_trend_dominance.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerB_alan_effects.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerB_exposure_summary.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerB_occurrence_counts.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerB_occurrence_density.png", "Figures"),
    ExpectedFile("manuscript/figures/fig_layerB_ibra_intensity_forest.png", "Figures"),
)

PINNED_SHA256: dict[str, str] = {
    "data/processed/pa_geometries_v0_3_0.csv": "781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b",
    "data/processed/pa_geometries_v0_3_0.gpkg": "0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11",
    "data/processed/pa_radiance_buffers_national_v0_3_0.csv": "493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e",
    "data/processed/pa_edge_profiles_national_v0_3_0.csv": "9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888",
    "data/processed/pa_buffer_validity_v0_3_0.csv": "407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25",
    "data/processed/pa_trends_v0_3_0.csv": "d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f",
    "data/processed/pa_risk_rankings_v0_3_0.csv": "554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a",
    "data/processed/pa_ibra_assignment_v0_3_0.csv": "3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf",
    "data/processed/pa_trend_bootstrap_summary_v0_3_0.csv": "cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920",
    "data/processed/layerB_occurrence_summary_v0_3_0.csv": "ec7746a882675b4955b7d455cddae2f9851bde55d16900cf6b32979346f77474",
    "data/processed/layerB_ala_license_ledger_v0_3_0.csv": "a751d630e01520698f4f81f0afcbb5ad0bf72b6ec53bc510e746b0c644885ac0",
    "data/processed/layerB_model_input_summary_v0_3_0.csv": "f42e9fea29dea812f54e4e9a02fafa3c7d6382e499d20e31b267b84be9346575",
    "data/processed/layerB_ibra_summary_v0_3_0.csv": "ed117aadd0c700c8dd0c7180714112fd212567f4b1ec56d0c8464f2e77d00a0d",
    "data/processed/layerB/microbats_occurrences_filtered_v0_3_0.csv.gz": "19e87ebda5e61cd0eb08a2824f85d63fe5dfc870527cd0ac9f21c00e38f1c007",
    "data/processed/layerB/diurnal_birds_occurrences_filtered_v0_3_0.csv.gz": "b4de14ec88af0a34c82553078d3a8c9b01c664413fde0262fe050fefed6e12ba",
    "analysis/reports/national_layerA_coverage_and_sanity.md": "1f9e23239f88750c4ee1b63b46632af7822a30a6ecd577f7a8c0c0ebb5cffcd9",
    "analysis/reports/trends_methods_and_sanity.md": "6934a40b182750a74ba4c04cb242f1f67967a55f723b64177d410c2303084d2f",
    "analysis/reports/risk_rankings_and_quadrants.md": "271a6a8580bfcd072ad42b44b9382346dcb74ca9225b68d5ea1eb3d04f2ca316",
    "analysis/reports/pa_trend_uncertainty.md": "8b0822635086a2eb804467105c84963fc3b79d9a882ceb5dec8d8f001da8ad06",
    "analysis/reports/pa_trend_dominance_matrix.csv": "ce322c5110ad47336c001b521322f64c745c016e8af93909df8aa3f9e603cfb8",
    "analysis/reports/layerB_modelling_report.md": "77381d7108b18146dd28ff194b9e31dcf45908e6dc355d83908ebb1cde8cc63a",
    "analysis/reports/layerB_qc_extended.md": "1673e75bf596f31bda178ac0908bd1dfa258d75b0d9da98451e98b6eae7e2fbb",
    "analysis/reports/layerB_scope_coverage.md": "62e0f8beaea79cd3186cd39a978bade5c3998d46e4b693a19efa77a95a0a1c3a",
    "analysis/reports/layerB_ibra_summary.md": "e09e152899605583cd7c3ce16b1a778bc5a107583d0e719609fd37c2e2d50b57",
    "analysis/reports/layerB_ibra_effects.csv": "2b9b14e678cb8e3819e50f26845a130ab2e4444dc0bedcf041f61a572d7454b1",
    "analysis/reports/figure_inventory.md": "4748110e45e40fda53129fb8370754ad64adf8e4fb7b344db9e45321370ebc1d",
    "analysis/reports/output_schema_reference.md": "7d2b00aa0a74b4b738424fce6ae4288cd6f15362007733a1349e5c97b8d79c8f",
    "manuscript/figures/fig_layerA_baseline_map.png": "e30a5fc53d419b7c8a8220ae827b19f9b73466c04bfb40e131ebabb8d54786c3",
    "manuscript/figures/fig_layerA_trend_distribution.png": "8b662196b40609c6978bf191c59e708478f1942bc1734a80ac7f360b25dec97e",
    "manuscript/figures/fig_layerA_retention_quadrant.png": "f80cfd0e40874e9a34e2b4bd6c4a16adfc20302ed759cd1ab4f8d782a0827df2",
    "manuscript/figures/fig_layerA_edge_profiles_aggregate.png": "e098405d6c03c53d97dc53c3b1a43ed04bd33c4a56bdd9fd2fac43904fc6339e",
    "manuscript/figures/fig_layerA_trend_uncertainty_forest.png": "9a2fca733e46f401c32c0606d50d54d1089e4f24f83fd86d71bd38f638a67f26",
    "manuscript/figures/fig_layerA_trend_dominance.png": "de53c292ddd22278e16da374c0166ced7f37ce2510fa5ad410ec325711eeee1d",
    "manuscript/figures/fig_layerB_alan_effects.png": "6a01c40b070aaaae71387963a0b0326ef4ee32336ead43b21f2c7af2f85f58f8",
    "manuscript/figures/fig_layerB_exposure_summary.png": "c5fa067e759fe0f3dcb5b837ef5b888c7636f65723c14335f74f9069b48c028e",
    "manuscript/figures/fig_layerB_occurrence_counts.png": "fefd4a827ac5af543a2f184624dbfe385591c185748550aefcbad909f5ed3025",
    "manuscript/figures/fig_layerB_occurrence_density.png": "e15d7ce82a6748f5be23c63c873406240c85b1df9dc0ce36039102fb40c43c16",
    "manuscript/figures/fig_layerB_ibra_intensity_forest.png": "eb80460408620d61e144b572d9dd9d89e4a15aa143003d85e37ca922c99eda40",
}


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def _sha256(path: Path, *, normalize_crlf: bool = False) -> str:
    if normalize_crlf:
        data = path.read_bytes().replace(b"\r\n", b"\n")
        return hashlib.sha256(data).hexdigest()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_record(root: Path, spec: ExpectedFile, max_hash_bytes: int) -> dict:
    path = root / spec.path
    expected_sha256 = spec.expected_sha256 or PINNED_SHA256.get(spec.path)
    record = asdict(spec)
    record["expected_sha256"] = expected_sha256
    record.update(
        {
            "present": path.exists(),
            "size_bytes": None,
            "sha256": None,
            "hash_status": "missing",
            "status": "missing" if spec.required else "optional_missing",
        }
    )
    if not path.exists():
        return record

    size = path.stat().st_size
    record["size_bytes"] = size
    if path.is_file() and size <= max_hash_bytes:
        digest = _sha256(path, normalize_crlf=spec.normalize_crlf)
        record["sha256"] = digest
        expected = record["expected_sha256"]
        if expected is None:
            record["hash_status"] = "not_pinned"
            record["status"] = "present"
        elif digest == expected:
            record["hash_status"] = "match"
            record["status"] = "verified"
        else:
            record["hash_status"] = "mismatch"
            record["status"] = "mismatch"
    else:
        record["hash_status"] = "skipped_large_or_not_file"
        record["status"] = "present_unhashed"
    return record


def build_inventory(
    root: Path,
    *,
    expected_files: Iterable[ExpectedFile] = EXPECTED_FILES,
    max_hash_mb: int = DEFAULT_MAX_HASH_MB,
) -> dict:
    max_hash_bytes = max_hash_mb * 1024 * 1024
    files = [_file_record(root, spec, max_hash_bytes) for spec in expected_files]
    required = [item for item in files if item["required"]]
    missing = [item for item in required if item["status"] == "missing"]
    mismatches = [item for item in required if item["status"] == "mismatch"]
    manifest_count = len(list((root / "artefacts").glob("*/MANIFEST.json")))
    dirty = bool(_run_git(root, "status", "--porcelain") or "")
    return {
        "generated_utc": _now_utc(),
        "root": str(root),
        "host": platform.node(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "git": {
            "commit": _run_git(root, "rev-parse", "HEAD"),
            "branch": _run_git(root, "branch", "--show-current"),
            "dirty": dirty,
        },
        "summary": {
            "expected_files": len(files),
            "required_files": len(required),
            "present_files": sum(1 for item in files if item["present"]),
            "verified_files": sum(1 for item in files if item["status"] == "verified"),
            "missing_required": len(missing),
            "checksum_mismatches": len(mismatches),
            "artefact_manifest_count": manifest_count,
        },
        "files": files,
    }


def _format_size(size: int | None) -> str:
    if size is None:
        return "-"
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GiB"


def render_inventory_markdown(inventory: dict) -> str:
    summary = inventory["summary"]
    git = inventory["git"]
    lines = [
        "# Evidence reconciliation",
        "",
        f"Generated: {inventory['generated_utc']}",
        f"Host: `{inventory['host']}`",
        f"Repo root: `{inventory['root']}`",
        f"Git: `{git['branch']}` @ `{git['commit']}`; dirty={git['dirty']}",
        "",
        "## Summary",
        "",
        f"- Expected files: {summary['expected_files']}",
        f"- Required files: {summary['required_files']}",
        f"- Present files: {summary['present_files']}",
        f"- Checksum-verified files: {summary['verified_files']}",
        f"- Missing required files: {summary['missing_required']}",
        f"- Checksum mismatches: {summary['checksum_mismatches']}",
        f"- Artefact manifests found: {summary['artefact_manifest_count']}",
        "",
    ]

    missing = [item for item in inventory["files"] if item["required"] and item["status"] == "missing"]
    mismatches = [
        item for item in inventory["files"] if item["required"] and item["status"] == "mismatch"
    ]
    if missing or mismatches:
        lines.extend(["## Required Attention", ""])
        for item in missing:
            lines.append(f"- Missing: `{item['path']}`")
        for item in mismatches:
            lines.append(f"- Checksum mismatch: `{item['path']}`")
        lines.append("")
    else:
        lines.extend(["## Required Attention", "", "- None for the expected evidence set.", ""])

    hash_notes = [item for item in inventory["files"] if item["normalize_crlf"] and item["note"]]
    if hash_notes:
        lines.extend(["## Hash Notes", ""])
        for item in hash_notes:
            lines.append(f"- `{item['path']}`: {item['note']}")
        lines.append("")

    lines.extend(
        [
            "## File Inventory",
            "",
            "| Group | Path | Status | Size | SHA-256 | Expected |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for item in inventory["files"]:
        sha = item["sha256"] or "-"
        expected = item["expected_sha256"] or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    item["group"],
                    f"`{item['path']}`",
                    item["status"],
                    _format_size(item["size_bytes"]),
                    sha,
                    expected,
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def render_reproducibility_audit(inventory: dict) -> str:
    git = inventory["git"]
    summary = inventory["summary"]
    dirty_text = "dirty" if git["dirty"] else "clean"
    pinned = [item for item in inventory["files"] if item["expected_sha256"]]
    lines = [
        "# Reproducibility audit",
        "",
        f"Generated: {inventory['generated_utc']}",
        "",
        "## Repo state",
        f"- Git commit: `{git['commit']}`",
        f"- Branch: `{git['branch']}`",
        f"- Working tree: {dirty_text}",
        f"- Evidence host: `{inventory['host']}`",
        "",
        "## Evidence reconciliation",
        f"- Report: `{DEFAULT_MD}`",
        f"- JSON: `{DEFAULT_JSON}`",
        f"- Expected files: {summary['expected_files']}",
        f"- Present files: {summary['present_files']}",
        f"- Checksum-verified files: {summary['verified_files']}",
        f"- Missing required files: {summary['missing_required']}",
        f"- Checksum mismatches: {summary['checksum_mismatches']}",
        f"- Artefact manifests found: {summary['artefact_manifest_count']}",
        "",
        "## One-command full rerun",
        "Full pipeline script (Layer A + Layer B + tests + build):",
        "",
        "```bash",
        "analysis/run_full_pipeline.sh",
        "```",
        "",
        "Key environment variables:",
        "- `DSIPA_REPO_ROOT` (optional): redirect outputs to a clean directory.",
        "- `DSIPA_WORKERS` (optional): number of workers for statewise Layer A.",
        "- `DSIPA_STATES` (optional): comma-separated state list.",
        "- `ALA_DOWNLOAD_EMAIL` + `ALA_DOWNLOAD_REASON` (required for Layer B downloads), or set `DSIPA_SKIP_LAYERB=1` to skip Layer B.",
        "",
        "## Expected runtime class",
        "- Layer A national statewise run (buffers + rings, 2013-2024): multi-hour to multi-day, depending on cache state and worker count.",
        "- Layer A trend/vulnerability/figures: minutes to about 1 hour.",
        "- Layer A trend uncertainty (IBRA bootstrap): about 5-10 minutes at n_boot=300.",
        "- Layer B downloads + QC: minutes, usually network-bound.",
        "- Layer B modelling + IBRA summary/falsification: about 1-2 hours.",
        "- Tests + build: under 5 minutes on the control plane.",
        "",
        "## Deep-server harness",
        "Use tmux for remote runs so laptop sleep/shutdown does not interrupt work:",
        "",
        "```bash",
        "analysis/deep_server_tmux_run.sh --mode evidence",
        "analysis/deep_server_tmux_run.sh --mode full --workers 12",
        "```",
        "",
        "Default remote run roots:",
        "- `/home/bwbrook/papers/dsipa-dev` for the current evidence snapshot.",
        "- `/data/codex/scratch/dsipa/<RUN_ID>` for logs and run-local files.",
        "- `/data/codex/artifacts/dsipa/<RUN_ID>` for durable copied artefacts.",
        "",
        "## Verification checklist",
        "Verify the reconciled evidence snapshot with pinned SHA-256 values:",
        "",
        "```bash",
    ]
    for index, item in enumerate(pinned):
        suffix = " \\" if index < len(pinned) - 1 else ""
        lines.append(f"sha256sum {item['path']}{suffix}" if index == 0 else f"  {item['path']}{suffix}")
    lines.extend(["```", "", "Expected hashes (sha256):"])
    for item in pinned:
        lines.append(f"- `{item['path']}`: `{item['expected_sha256']}`")
    hash_notes = [item for item in inventory["files"] if item["normalize_crlf"] and item["note"]]
    if hash_notes:
        lines.extend(["", "Checksum notes:"])
        for item in hash_notes:
            lines.append(f"- `{item['path']}`: {item['note']}")
    lines.extend(
        [
            "",
            "## Tests and builds",
            "- `uv run pytest`",
            "- `uv build`",
            "",
            "## Schema versioning",
            "- Current schema version: `v0.3.0`.",
            "- Output schema reference: `analysis/reports/output_schema_reference.md`.",
            "",
            "## Release caveat",
            "Large derived tables and raw occurrence downloads remain outside git. Before paper release, upload the required large files and a checksum manifest to the external archive, then record the DOI/access date in `data/README.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(
    inventory: dict,
    *,
    md_path: Path,
    json_path: Path,
    audit_path: Path | None,
) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_inventory_markdown(inventory), encoding="utf-8")
    json_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if audit_path is not None:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(render_reproducibility_audit(inventory), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inventory DSIPA evidence outputs.")
    parser.add_argument("--output-md", default=DEFAULT_MD)
    parser.add_argument("--output-json", default=DEFAULT_JSON)
    parser.add_argument("--audit-md", default=DEFAULT_AUDIT)
    parser.add_argument("--write-audit", action="store_true")
    parser.add_argument("--max-hash-mb", type=int, default=DEFAULT_MAX_HASH_MB)
    parser.add_argument("--fail-on-missing", action="store_true")
    parser.add_argument("--fail-on-mismatch", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    inventory = build_inventory(root, max_hash_mb=args.max_hash_mb)
    write_outputs(
        inventory,
        md_path=root / args.output_md,
        json_path=root / args.output_json,
        audit_path=(root / args.audit_md) if args.write_audit else None,
    )
    missing = inventory["summary"]["missing_required"]
    mismatches = inventory["summary"]["checksum_mismatches"]
    if args.fail_on_missing and missing:
        return 1
    if args.fail_on_mismatch and mismatches:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

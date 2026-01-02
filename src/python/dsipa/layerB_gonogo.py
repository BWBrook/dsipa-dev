"""Layer B go/no-go decision report (WP0.14)."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root

DEFAULT_CONFIG = "docs/layerB_gonogo.json"
REPORT_PATH = "analysis/reports/layerB_gonogo.md"

REQUIRED_KEYS = {
    "version",
    "decision_date_utc",
    "status",
    "scope",
    "focal_taxa",
    "negative_controls",
    "bias_strategy",
    "go_no_go_criteria",
    "data_sources",
    "notes",
}

ALLOWED_STATUS = {"go", "conditional-go", "no-go"}


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _require_keys(data: dict[str, Any], keys: set[str], label: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        raise ValueError(f"Missing required {label} keys: {', '.join(missing)}")


def _join_list(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(values)


def load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    _require_keys(data, REQUIRED_KEYS, "config")

    status = data.get("status")
    if status not in ALLOWED_STATUS:
        raise ValueError(f"status must be one of {sorted(ALLOWED_STATUS)}")

    scope = data.get("scope", {})
    _require_keys(scope, {"spatial", "temporal_years"}, "scope")
    if not isinstance(scope["temporal_years"], list) or len(scope["temporal_years"]) != 2:
        raise ValueError("scope.temporal_years must be a 2-item list [start_year, end_year]")

    for field in ["focal_taxa", "negative_controls", "go_no_go_criteria", "data_sources", "notes"]:
        if not isinstance(data[field], list) or not data[field]:
            raise ValueError(f"{field} must be a non-empty list")

    for item in data["focal_taxa"]:
        _require_keys(item, {"group", "rationale", "expected_response"}, "focal_taxa item")

    for item in data["negative_controls"]:
        _require_keys(item, {"group", "rationale", "expected_response"}, "negative_controls item")

    bias = data.get("bias_strategy", {})
    _require_keys(
        bias,
        {"filters", "background", "sampling_covariates", "spatial_blocking_km", "sensitivity_checks", "falsification_checks"},
        "bias_strategy",
    )

    return data


def render_report(config: dict[str, Any]) -> str:
    scope = config["scope"]
    bias = config["bias_strategy"]

    lines = [
        "# Layer B go/no-go decision (WP0.14)",
        "",
        f"Generated: {_now_utc()}",
        f"Decision date: {config['decision_date_utc']}",
        f"Status: {config['status']}",
        f"Config version: {config['version']}",
        "",
        "## Scope",
        f"- Spatial: {scope['spatial']}",
        f"- Temporal years: {scope['temporal_years'][0]}–{scope['temporal_years'][1]}",
        "",
        "## Go/no-go criteria",
        *[f"- {criterion}" for criterion in config["go_no_go_criteria"]],
        "",
        "## Focal taxa",
        "| Group | Rationale | Inclusions/exclusions | Expected response |",
        "| --- | --- | --- | --- |",
    ]

    for item in config["focal_taxa"]:
        inclusions = _join_list(item.get("inclusions"))
        exclusions = _join_list(item.get("exclusions"))
        lines.append(
            f"| {item['group']} | {item['rationale']} | Inclusions: {inclusions}<br>Exclusions: {exclusions} | {item['expected_response']} |"
        )

    lines.extend(
        [
            "",
            "## Negative controls",
            "| Group | Rationale | Expected response |",
            "| --- | --- | --- |",
        ]
    )

    for item in config["negative_controls"]:
        lines.append(
            f"| {item['group']} | {item['rationale']} | {item['expected_response']} |"
        )

    lines.extend(
        [
            "",
            "## Bias-control strategy",
            "### Filters",
            *[f"- {entry}" for entry in bias["filters"]],
            "",
            "### Background sampling",
            f"- {bias['background']}",
            "",
            "### Sampling covariates",
            *[f"- {entry}" for entry in bias["sampling_covariates"]],
            "",
            f"### Spatial blocking",
            f"- Block size: {bias['spatial_blocking_km']} km",
            "",
            "### Sensitivity checks",
            *[f"- {entry}" for entry in bias["sensitivity_checks"]],
            "",
            "### Falsification checks",
            *[f"- {entry}" for entry in bias["falsification_checks"]],
            "",
            "## Planned data sources",
            *[f"- {entry}" for entry in config["data_sources"]],
            "",
            "## Notes",
            *[f"- {entry}" for entry in config["notes"]],
            "",
        ]
    )

    return "\n".join(lines)


def write_report(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_artefact(report_path: Path, config_path: Path, root: Path) -> Path:
    artefact_dir = root / "artefacts" / "wp0_14_layerB_gonogo"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(report_path, artefact_dir / report_path.name)
    shutil.copyfile(config_path, artefact_dir / config_path.name)

    manifest = build_manifest(
        run_id="wp0_14_layerB_gonogo",
        wp="WP0.14",
        root=root,
        outputs=[report_path.name, config_path.name],
        notes="WP0.14 Layer B go/no-go decision artefact",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.14 Layer B go/no-go artefact. Contains decision report and config.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer B go/no-go report (WP0.14).")
    parser.add_argument(
        "--config",
        type=str,
        default=DEFAULT_CONFIG,
        help="Path to layerB_gonogo.json config file.",
    )
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    config_path = (root / args.config).resolve()
    config = load_config(config_path)

    report_path = root / REPORT_PATH
    content = render_report(config)
    write_report(report_path, content)

    if not args.skip_artefact:
        write_artefact(report_path, config_path, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

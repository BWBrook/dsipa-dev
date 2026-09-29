"""Generate output schema reference documentation (WP0.8)."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import OUTPUT_SCHEMAS, SCHEMA_VERSION


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _render_schema(schema) -> list[str]:
    lines = [
        f"## {schema.key}",
        "",
        f"File: `{schema.filename}`",
        f"Format: {schema.file_type}",
        "",
        schema.description,
        "",
        "| Column | Type | Units | Description |",
        "| --- | --- | --- | --- |",
    ]
    for col in schema.columns:
        lines.append(
            f"| {col.name} | {col.dtype} | {col.units} | {col.description} |"
        )
    if schema.notes:
        lines.extend(["", "Notes:"])
        for note in schema.notes:
            lines.append(f"- {note}")
    lines.append("")
    return lines


def write_schema_reference(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Output schema reference",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Schema version: {SCHEMA_VERSION}",
        "",
        "Migration policy: Any change to required columns or their meaning requires a schema_version bump and a full rerun. No automatic migration is provided.",
        "",
    ]
    for schema in OUTPUT_SCHEMAS:
        lines.extend(_render_schema(schema))
    path.write_text("\n".join(lines), encoding="utf-8")


def write_artefact(report_path: Path, root: Path) -> Path:
    artefact_dir = root / "artefacts" / "wp0_8_schema_reference"
    artefact_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(report_path, artefact_dir / report_path.name)

    manifest = build_manifest(
        run_id="wp0_8_schema_reference",
        wp="WP0.8",
        root=root,
        outputs=[report_path.name],
        notes="WP0.8 output schema reference",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.8 schema reference artefact. Contains output_schema_reference.md and manifest.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write output schema reference documentation.")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    report_path = root / "analysis" / "reports" / "output_schema_reference.md"
    write_schema_reference(report_path)

    if not args.skip_artefact:
        write_artefact(report_path, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

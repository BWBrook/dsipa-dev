"""Generate a figure inventory report (WP0.13)."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from dsipa.paths import find_repo_root


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def write_inventory(report_path: Path, figures_dir: Path) -> Path:
    figures = sorted(
        [p for p in figures_dir.iterdir() if p.is_file() and not p.name.startswith(".")]
    )
    lines = [
        "# Figure inventory",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Directory: {figures_dir}",
        "",
        "| Figure | Size (KB) |",
        "| --- | --- |",
    ]
    for fig in figures:
        size_kb = fig.stat().st_size / 1024.0
        lines.append(f"| {fig.name} | {size_kb:.1f} |")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write a figure inventory report.")
    parser.add_argument(
        "--report-path",
        default="analysis/reports/figure_inventory.md",
        help="Path for the inventory report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    figures_dir = root / "manuscript" / "figures"
    report_path = root / args.report_path
    write_inventory(report_path, figures_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

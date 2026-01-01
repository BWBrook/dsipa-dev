"""Run entrypoint for DSIPA-NBS."""

from __future__ import annotations

import argparse
from pathlib import Path

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root


def _sanitise_run_id(run_id: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in run_id)
    return cleaned.strip("_") or "run"


def run(
    *,
    run_id: str,
    work_package: str,
    out_dir: Path,
    root: Path | None = None,
) -> Path:
    root = root or find_repo_root()
    run_id = _sanitise_run_id(run_id)
    out_dir = out_dir.expanduser().resolve()
    run_dir = out_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    placeholder_path = run_dir / "placeholder.txt"
    placeholder_path.write_text(
        "DSIPA-NBS bootstrap artefact.\n",
        encoding="utf-8",
    )

    outputs = [placeholder_path.name]
    manifest = build_manifest(
        run_id=run_id,
        wp=work_package,
        root=root,
        outputs=outputs,
        notes="WP0.1 bootstrap placeholder output",
    )
    write_manifest(run_dir / "MANIFEST.json", manifest)

    readme_path = run_dir / "README.txt"
    readme_path.write_text(
        "Bootstrap artefact for DSIPA-NBS (WP0.1).\n"
        "Contains a placeholder output and a run manifest.\n",
        encoding="utf-8",
    )

    return run_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run DSIPA-NBS pipeline entrypoint.")
    parser.add_argument(
        "--run-id",
        default="wp0_1_bootstrap",
        help="Run identifier used for the artefact folder name.",
    )
    parser.add_argument(
        "--work-package",
        default="WP0.1",
        help="Work package identifier recorded in the manifest.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for artefacts (default: <repo>/artefacts).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root = find_repo_root()
    out_dir = Path(args.out_dir) if args.out_dir else root / "artefacts"
    run(
        run_id=args.run_id,
        work_package=args.work_package,
        out_dir=out_dir,
        root=root,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

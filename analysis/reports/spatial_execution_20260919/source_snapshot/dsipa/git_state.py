"""Git working-tree state helpers for generated artefact paths."""

from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class GitStatusEntry:
    code: str
    path: str


def repo_relative_path(path: str | Path, root: Path) -> str:
    candidate = Path(path)
    if candidate.is_absolute():
        candidate = Path(os.path.relpath(candidate.resolve(), root.resolve()))
    return candidate.as_posix().removeprefix("./")


def _parse_porcelain_line(line: str) -> GitStatusEntry:
    code = line[:2]
    path = line[3:] if len(line) > 3 else ""
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return GitStatusEntry(code=code, path=path.strip('"'))


def git_status_entries(root: Path) -> list[GitStatusEntry] | None:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--no-renames",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return [
        _parse_porcelain_line(line)
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def git_is_dirty(root: Path) -> bool | None:
    entries = git_status_entries(root)
    if entries is None:
        return None
    return bool(entries)


def unexpected_status_entries(
    root: Path,
    expected_paths: Iterable[str | Path],
) -> list[GitStatusEntry] | None:
    entries = git_status_entries(root)
    if entries is None:
        return None
    expected = {repo_relative_path(path, root) for path in expected_paths}
    return [entry for entry in entries if entry.path not in expected]


def _format_entries(entries: Iterable[GitStatusEntry]) -> str:
    return ", ".join(f"{entry.code} {entry.path}" for entry in entries)


def ensure_clean_before_mutation(
    root: Path,
    *,
    allow_dirty: bool = False,
    context: str = "DSIPA artefact generation",
) -> None:
    if allow_dirty:
        return
    unexpected = unexpected_status_entries(root, ())
    if unexpected is None:
        raise SystemExit(f"{context}: cannot inspect Git working tree; refusing to proceed.")
    if unexpected:
        raise SystemExit(
            f"{context}: working tree has unexplained changes before output "
            f"generation: {_format_entries(unexpected)}. Commit or remove them, "
            "or use --allow-dirty only for a documented dirty-run handoff."
        )


def ensure_only_expected_changes(
    root: Path,
    *,
    expected_paths: Iterable[str | Path],
    allow_dirty: bool = False,
    context: str = "DSIPA artefact generation",
) -> None:
    if allow_dirty:
        return
    unexpected = unexpected_status_entries(root, expected_paths)
    if unexpected is None:
        raise SystemExit(f"{context}: cannot inspect Git working tree; refusing to proceed.")
    if unexpected:
        raise SystemExit(
            f"{context}: working tree has unexpected changes after output "
            f"generation: {_format_entries(unexpected)}. Expected only: "
            f"{', '.join(sorted(repo_relative_path(path, root) for path in expected_paths))}."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check DSIPA git working-tree state.")
    parser.add_argument("command", choices=["require-clean"])
    parser.add_argument("--context", default="DSIPA run")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.command == "require-clean":
        ensure_clean_before_mutation(root, context=args.context)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

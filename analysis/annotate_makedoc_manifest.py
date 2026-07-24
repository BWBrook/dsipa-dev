#!/usr/bin/env python3
"""Add DSIPA source and Makedoc tool identities to a build manifest."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="DSIPA Makedoc YAML config.")
    parser.add_argument("--profile", required=True, help="Build profile name.")
    parser.add_argument("--source-root", required=True, help="DSIPA repository root.")
    parser.add_argument(
        "--build-tool-root", required=True, help="Upstream Makedoc repository root."
    )
    return parser.parse_args()


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"git {' '.join(args)} failed for {root}: {detail}")
    return result.stdout.strip()


def git_identity(root: Path) -> dict[str, Any]:
    resolved = root.expanduser().resolve()
    if not resolved.is_dir():
        raise ValueError(f"repository root does not exist: {resolved}")
    return {
        "root": str(resolved),
        "sha": _git(resolved, "rev-parse", "HEAD"),
        "branch": _git(resolved, "rev-parse", "--abbrev-ref", "HEAD"),
        "dirty": bool(
            _git(resolved, "status", "--porcelain", "--untracked-files=all")
        ),
    }


def manifest_path(config_path: Path, profile_name: str) -> Path:
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read build config {config_path}: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError(f"build config is not a mapping: {config_path}")
    profiles = config.get("profiles")
    profile = profiles.get(profile_name) if isinstance(profiles, dict) else None
    if not isinstance(profile, dict):
        raise ValueError(f"profile not found in build config: {profile_name}")
    output_dir = profile.get("output_dir")
    output_stem = profile.get("output_stem")
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise ValueError(f"profile {profile_name} has no output_dir")
    if not isinstance(output_stem, str) or not output_stem.strip():
        raise ValueError(f"profile {profile_name} has no output_stem")
    directory = Path(output_dir).expanduser()
    if not directory.is_absolute():
        directory = config_path.parent / directory
    return directory.resolve() / f"{output_stem}_build_manifest.json"


def annotate_manifest(
    *,
    config_path: Path,
    profile_name: str,
    source_root: Path,
    build_tool_root: Path,
) -> Path:
    path = manifest_path(config_path.resolve(), profile_name)
    if not path.is_file():
        raise ValueError(f"successful Makedoc build manifest is missing: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read Makedoc build manifest {path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ValueError(f"Makedoc build manifest is not a JSON object: {path}")
    upstream_git = manifest.get("git")
    if not isinstance(upstream_git, dict):
        raise ValueError(f"Makedoc build manifest has no upstream git object: {path}")

    manifest["repository_provenance"] = {
        "annotated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": git_identity(source_root),
        "build_tool": git_identity(build_tool_root),
    }
    if manifest.get("git") != upstream_git:
        raise ValueError("internal error: upstream Makedoc git identity changed")

    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(
            json.dumps(manifest, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def main() -> int:
    args = parse_args()
    try:
        path = annotate_manifest(
            config_path=Path(args.config),
            profile_name=args.profile,
            source_root=Path(args.source_root),
            build_tool_root=Path(args.build_tool_root),
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Annotated build manifest: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

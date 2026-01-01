"""Run manifest helpers."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any


def _safe_version(dist_name: str) -> str | None:
    try:
        return metadata.version(dist_name)
    except metadata.PackageNotFoundError:
        return None


def _git_commit(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def _git_dirty(root: Path) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return None


def build_manifest(
    *,
    run_id: str,
    wp: str,
    root: Path,
    outputs: list[str],
    notes: str | None = None,
) -> dict[str, Any]:
    """Create a minimal run manifest."""
    return {
        "run_id": run_id,
        "work_package": wp,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": {
            "commit": _git_commit(root),
            "dirty": _git_dirty(root),
        },
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "packages": {
            "dsipa-nbs": _safe_version("dsipa-nbs"),
            "pytest": _safe_version("pytest"),
        },
        "outputs": outputs,
        "notes": notes or "placeholder bootstrap artefact",
    }


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

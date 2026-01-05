"""Run manifest helpers."""

from __future__ import annotations

import hashlib
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


def _hash_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    *,
    run_id: str,
    wp: str,
    root: Path,
    outputs: list[str],
    notes: str | None = None,
    inputs: list[str] | None = None,
    require_clean: bool = False,
) -> dict[str, Any]:
    """Create a run manifest with reproducibility metadata."""
    dirty = _git_dirty(root)
    warnings: list[str] = []
    if require_clean and dirty:
        warnings.append("git working tree is dirty; manuscript artefact may be non-canonical")
    packages = {
        name: _safe_version(name)
        for name in (
            "dsipa-nbs",
            "geopandas",
            "numpy",
            "pandas",
            "pyproj",
            "rasterio",
            "shapely",
            "matplotlib",
            "pytest",
            "scikit-learn",
        )
    }
    data_readme = root / "data" / "README.md"
    return {
        "run_id": run_id,
        "work_package": wp,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": {
            "commit": _git_commit(root),
            "dirty": dirty,
            "clean_required": require_clean,
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
        "packages": packages,
        "inputs": inputs or [],
        "outputs": outputs,
        "data_manifest": {
            "path": str(data_readme),
            "sha256": _hash_file(data_readme),
        },
        "notes": notes or "placeholder bootstrap artefact",
        "warnings": warnings,
    }


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

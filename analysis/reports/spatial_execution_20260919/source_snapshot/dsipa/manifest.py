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

from dsipa.git_state import git_is_dirty, repo_relative_path, unexpected_status_entries


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
    expected_dirty_paths: list[str | Path] | None = None,
) -> dict[str, Any]:
    """Create a run manifest with reproducibility metadata."""
    dirty = git_is_dirty(root)
    expected_relative = [
        repo_relative_path(path, root) for path in expected_dirty_paths or []
    ]
    warnings: list[str] = []
    if require_clean:
        if dirty is None:
            warnings.append("unable to inspect Git working tree")
        elif dirty:
            unexpected = unexpected_status_entries(root, expected_dirty_paths or [])
            if unexpected is None:
                warnings.append("unable to inspect Git working tree")
            elif expected_dirty_paths and unexpected == []:
                warnings.append(
                    "git working tree contains only expected generated output changes"
                )
            else:
                warnings.append(
                    "git working tree is dirty; manuscript artefact may be non-canonical"
                )
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
            "expected_dirty_paths": expected_relative,
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

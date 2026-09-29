"""Filesystem helpers for DSIPA-NBS."""

from __future__ import annotations

import os
from pathlib import Path


def find_repo_root(start: str | Path | None = None) -> Path:
    """Locate repo root by searching for pyproject.toml or .git."""
    env_root = os.environ.get("DSIPA_REPO_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    cursor = Path(start or Path.cwd()).expanduser().resolve()
    candidates = [cursor, *cursor.parents]
    for path in candidates:
        if (path / "pyproject.toml").exists() or (path / ".git").exists():
            return path
    raise FileNotFoundError("Could not locate repo root (pyproject.toml or .git).")

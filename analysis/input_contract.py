"""Shared input-manifest validation for bounded DSIPA audit scripts.

The corrected spatial products intentionally retain the ``v0_3_0`` column
schema.  Their identity therefore comes from an explicit manifest
``analysis_id`` and per-file byte/hash records.  Legacy callers may omit the
manifest and retain the historical checks in each audit.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class InputContract:
    """Validated inputs and identity for one legacy or manifest-mode run."""

    mode: str
    analysis_id: str
    manifest_path: Path | None
    manifest_sha256: str | None
    files: dict[str, Path]

    def identity(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "analysis_id": self.analysis_id,
            "manifest_path": str(self.manifest_path) if self.manifest_path else None,
            "manifest_sha256": self.manifest_sha256,
        }


def _normalise_entry(name: str, value: object) -> tuple[str, int]:
    if not isinstance(value, Mapping):
        raise ValueError(f"Manifest entry for {name!r} must be an object")
    digest = value.get("sha256")
    size = value.get("bytes")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest.lower()):
        raise ValueError(f"Manifest entry for {name!r} has invalid sha256")
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise ValueError(f"Manifest entry for {name!r} has invalid bytes")
    return digest.lower(), size


def load_manifest(path: Path, data_dir: Path, required: Iterable[str], *, path_overrides: Mapping[str, Path] | None = None) -> InputContract:
    """Validate all required files listed by *path* beneath *data_dir*.

    The contract deliberately maps names to ``data_dir / name``.  This keeps a
    run relocatable and prevents a manifest from silently redirecting an audit
    to an unrelated absolute path.
    """
    path = path.resolve()
    data_dir = data_dir.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Input manifest not found: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid input manifest JSON: {path}") from exc
    if not isinstance(manifest, Mapping):
        raise ValueError("Input manifest must be a JSON object")
    analysis_id = manifest.get("analysis_id")
    files = manifest.get("files")
    if not isinstance(analysis_id, str) or not analysis_id:
        raise ValueError("Input manifest requires a non-empty analysis_id")
    if not isinstance(files, Mapping):
        raise ValueError("Input manifest requires a files object")

    resolved: dict[str, Path] = {}
    for name in required:
        if name not in files:
            raise ValueError(f"Input manifest omits required file: {name}")
        digest, size = _normalise_entry(name, files[name])
        candidate = Path((path_overrides or {}).get(name, data_dir / name)).resolve()
        if not path_overrides or name not in path_overrides:
            try:
                candidate.relative_to(data_dir)
            except ValueError as exc:
                raise ValueError(f"Required input escapes data directory: {name}") from exc
        if not candidate.is_file():
            raise FileNotFoundError(f"Manifest input missing: {candidate}")
        actual_size = candidate.stat().st_size
        actual_digest = sha256(candidate)
        if actual_size != size:
            raise ValueError(f"Manifest byte-count mismatch for {name}: expected {size}, got {actual_size}")
        if actual_digest != digest:
            raise ValueError(f"Manifest sha256 mismatch for {name}: expected {digest}, got {actual_digest}")
        resolved[name] = candidate
    return InputContract(
        mode="manifest",
        analysis_id=analysis_id,
        manifest_path=path,
        manifest_sha256=sha256(path),
        files=resolved,
    )


def legacy_contract(paths: Mapping[str, Path], expected: Mapping[str, str] | None = None, *, analysis_id: str = "goal012-accepted") -> InputContract:
    """Check legacy paths and optional historical hashes."""
    resolved: dict[str, Path] = {}
    for name, path in paths.items():
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(path)
        if expected and name in expected:
            actual = sha256(path)
            if actual != expected[name]:
                raise ValueError(f"Accepted input hash mismatch: {name}")
        resolved[name] = path
    return InputContract("legacy", analysis_id, None, None, resolved)


def validate_manifest(path: Path, data_dir: Path, required: Iterable[str], *, path_overrides: Mapping[str, Path] | None = None) -> InputContract:
    """Public alias for callers that want an explicitly named validation step."""
    return load_manifest(path, data_dir, required, path_overrides=path_overrides)


def resolve_contract(data_dir: Path, required: Iterable[str], manifest: Path | None = None, expected: Mapping[str, str] | None = None) -> InputContract:
    """Choose explicit-manifest or legacy validation."""
    paths = {name: Path(data_dir) / name for name in required}
    if manifest is not None:
        return load_manifest(manifest, Path(data_dir), required)
    return legacy_contract(paths, expected)

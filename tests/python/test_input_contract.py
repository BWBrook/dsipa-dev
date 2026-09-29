from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[2] / "analysis"))
from input_contract import load_manifest


def _manifest(path: Path, payload: bytes) -> Path:
    data = path.parent / "example.csv"
    data.write_bytes(payload)
    path.write_text(
        json.dumps(
            {
                "analysis_id": "spatial-correction-20260919",
                "files": {
                    "example.csv": {
                        "sha256": hashlib.sha256(payload).hexdigest(),
                        "bytes": len(payload),
                    }
                },
            }
        )
    )
    return path


def test_manifest_validates_identity_and_file_digest(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path / "manifest.json", b"pa_id\na\n")
    contract = load_manifest(manifest, tmp_path, ["example.csv"])
    assert contract.analysis_id == "spatial-correction-20260919"
    assert contract.files["example.csv"].read_bytes() == b"pa_id\na\n"
    assert contract.identity()["manifest_sha256"] == hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_manifest_rejects_changed_file(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path / "manifest.json", b"original")
    (tmp_path / "example.csv").write_bytes(b"changed")
    with pytest.raises(ValueError, match="(byte-count|sha256) mismatch"):
        load_manifest(manifest, tmp_path, ["example.csv"])

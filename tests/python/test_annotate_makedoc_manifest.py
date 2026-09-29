import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
import yaml

_spec = importlib.util.spec_from_file_location("annotate_makedoc_manifest", Path(__file__).parents[2] / "analysis/annotate_makedoc_manifest.py")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
annotate_manifest, git_identity = _module.annotate_manifest, _module.git_identity

def _setup(tmp_path: Path):
    source = tmp_path / "source"; tool = tmp_path / "tool"; output = tmp_path / "build"
    source.mkdir(); tool.mkdir(); output.mkdir()
    payload = source / "README.md"; payload.write_text("archive\n")
    record = {"path": "README.md", "bytes": payload.stat().st_size, "sha256": hashlib.sha256(payload.read_bytes()).hexdigest()}
    (source / "FILE_MANIFEST.json").write_text(json.dumps({"schema_version": "test", "files": [record]}))
    tool_payload = tool / "README.md"; tool_payload.write_text("makedoc\n")
    tool_record = {"path": "README.md", "bytes": tool_payload.stat().st_size, "sha256": hashlib.sha256(tool_payload.read_bytes()).hexdigest()}
    (tool / "FILE_MANIFEST.json").write_text(json.dumps({"schema_version": "test", "files": [tool_record]}))
    config = tmp_path / "build.yaml"; config.write_text(yaml.safe_dump({"profiles": {"test": {"output_dir": str(output), "output_stem": "doc"}}}))
    manifest = output / "doc_build_manifest.json"; manifest.write_text(json.dumps({"git": {"upstream": "kept"}}))
    return source, tool, config, manifest

def test_git_free_archive_identity_and_annotation(tmp_path: Path):
    source, tool, config, manifest = _setup(tmp_path)
    identity = git_identity(source)
    assert identity["mode"] == "curated_archive" and identity["files_verified"] == 1
    annotate_manifest(config_path=config, profile_name="test", source_root=source, build_tool_root=tool)
    result = json.loads(manifest.read_text())
    assert result["repository_provenance"]["source"]["mode"] == "curated_archive"
    assert result["git"] == {"upstream": "kept"}

def test_git_free_archive_rejects_missing_or_corrupt_receipt(tmp_path: Path):
    source, _, _, _ = _setup(tmp_path)
    (source / "README.md").write_text("changed\n")
    with pytest.raises(ValueError, match="hash mismatch"):
        git_identity(source)
    (source / "FILE_MANIFEST.json").unlink()
    with pytest.raises(ValueError, match="receipt missing"):
        git_identity(source)

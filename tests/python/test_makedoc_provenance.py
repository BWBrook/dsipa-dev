import json
import os
import subprocess
from pathlib import Path

import pytest

from dsipa.paths import find_repo_root


REPO_ROOT = find_repo_root()
WRAPPER = REPO_ROOT / "analysis/makedoc.sh"


def _run(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _git_repo(path: Path) -> None:
    path.mkdir(parents=True)
    _run("git", "init", "-b", "main", cwd=path)
    _run("git", "config", "user.email", "tests@example.invalid", cwd=path)
    _run("git", "config", "user.name", "DSIPA tests", cwd=path)
    (path / "tracked.txt").write_text("initial\n", encoding="utf-8")
    _run("git", "add", "tracked.txt", cwd=path)
    _run("git", "commit", "-m", "initial", cwd=path)


def _git_identity(path: Path) -> dict[str, object]:
    return {
        "root": str(path.resolve()),
        "sha": _run("git", "rev-parse", "HEAD", cwd=path).stdout.strip(),
        "branch": _run(
            "git", "rev-parse", "--abbrev-ref", "HEAD", cwd=path
        ).stdout.strip(),
        "dirty": bool(_run("git", "status", "--porcelain", cwd=path).stdout.strip()),
    }


def _write_config(source_root: Path) -> tuple[Path, Path]:
    config = source_root / "settings/build.yaml"
    output_dir = source_root / "build/draft"
    output_dir.mkdir(parents=True)
    config.parent.mkdir(parents=True)
    config.write_text(
        """default_profile: draft
profiles:
  draft:
    output_dir: ../build/draft
    output_stem: manuscript
""",
        encoding="utf-8",
    )
    return config, output_dir / "manuscript_build_manifest.json"


def _write_manifest(path: Path, tool_root: Path) -> dict[str, object]:
    upstream_git = {
        "sha": _git_identity(tool_root)["sha"],
        "branch": "main",
        "dirty": False,
    }
    manifest = {
        "generated_at_utc": "2026-07-24T00:00:00+00:00",
        "git": upstream_git,
        "profile": {"name": "draft"},
        "repository_provenance": {
            "source": {"sha": "stale-source"},
            "build_tool": {"sha": "stale-tool"},
        },
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return upstream_git


def _fake_make(tmp_path: Path) -> tuple[Path, Path]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    log = tmp_path / "make.log"
    make = fake_bin / "make"
    make.write_text(
        """#!/usr/bin/env bash
set -u
printf '%s\n' "$*" >> "$FAKE_MAKE_LOG"
exit "${FAKE_MAKE_STATUS:-0}"
""",
        encoding="utf-8",
    )
    make.chmod(0o755)
    return fake_bin, log


def _wrapper_env(
    source_root: Path,
    tool_root: Path,
    config: Path,
    fake_bin: Path,
    log: Path,
    status: int = 0,
) -> dict[str, str]:
    return {
        **os.environ,
        "PATH": f"{fake_bin}:{os.environ['PATH']}",
        "MAKEDOC_ROOT": str(tool_root),
        "DSIPA_MAKEDOC_CONFIG": str(config),
        "PROFILE": "draft",
        "FAKE_MAKE_LOG": str(log),
        "FAKE_MAKE_STATUS": str(status),
        "DSIPA_SOURCE_ROOT": str(source_root),
    }


@pytest.mark.parametrize("target", ["check", "all"])
def test_success_refreshes_dual_provenance_when_upstream_manifest_is_unchanged(
    tmp_path: Path, target: str
) -> None:
    source_root = tmp_path / "source"
    tool_root = tmp_path / "makedoc"
    _git_repo(source_root)
    _git_repo(tool_root)
    config, manifest_path = _write_config(source_root)
    upstream_git = _write_manifest(manifest_path, tool_root)
    (source_root / "tracked.txt").write_text("dirty source\n", encoding="utf-8")
    fake_bin, log = _fake_make(tmp_path)

    result = subprocess.run(
        ["bash", str(WRAPPER), target],
        cwd=source_root,
        capture_output=True,
        text=True,
        env=_wrapper_env(source_root, tool_root, config, fake_bin, log),
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["git"] == upstream_git
    assert manifest["repository_provenance"]["source"] == _git_identity(source_root)
    assert manifest["repository_provenance"]["build_tool"] == _git_identity(tool_root)
    assert manifest["repository_provenance"]["annotated_at_utc"]
    assert f"PROFILE=draft {target}" in log.read_text(encoding="utf-8")


def test_upstream_failure_is_propagated_and_manifest_is_not_annotated(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source"
    tool_root = tmp_path / "makedoc"
    _git_repo(source_root)
    _git_repo(tool_root)
    config, manifest_path = _write_config(source_root)
    _write_manifest(manifest_path, tool_root)
    before = manifest_path.read_bytes()
    fake_bin, log = _fake_make(tmp_path)

    result = subprocess.run(
        ["bash", str(WRAPPER), "check"],
        cwd=source_root,
        capture_output=True,
        text=True,
        env=_wrapper_env(
            source_root, tool_root, config, fake_bin, log, status=37
        ),
    )

    assert result.returncode == 37
    assert manifest_path.read_bytes() == before
    assert "PROFILE=draft check" in log.read_text(encoding="utf-8")


def test_successful_non_build_target_does_not_annotate(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    tool_root = tmp_path / "makedoc"
    _git_repo(source_root)
    _git_repo(tool_root)
    config, manifest_path = _write_config(source_root)
    _write_manifest(manifest_path, tool_root)
    before = manifest_path.read_bytes()
    fake_bin, log = _fake_make(tmp_path)

    result = subprocess.run(
        ["bash", str(WRAPPER), "validate-config"],
        cwd=source_root,
        capture_output=True,
        text=True,
        env=_wrapper_env(source_root, tool_root, config, fake_bin, log),
    )

    assert result.returncode == 0
    assert manifest_path.read_bytes() == before


def test_successful_check_fails_closed_when_manifest_is_missing(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    tool_root = tmp_path / "makedoc"
    _git_repo(source_root)
    _git_repo(tool_root)
    config, manifest_path = _write_config(source_root)
    manifest_path.unlink(missing_ok=True)
    fake_bin, log = _fake_make(tmp_path)

    result = subprocess.run(
        ["bash", str(WRAPPER), "check"],
        cwd=source_root,
        capture_output=True,
        text=True,
        env=_wrapper_env(source_root, tool_root, config, fake_bin, log),
    )

    assert result.returncode != 0
    assert "manifest" in result.stderr.lower()

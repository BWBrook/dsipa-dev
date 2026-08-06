import subprocess
from pathlib import Path

from dsipa.manifest import build_manifest
from dsipa.paths import find_repo_root


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.org"],
        cwd=path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "DSIPA Test"],
        cwd=path,
        check=True,
    )
    (path / "README.md").write_text("baseline\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "baseline"],
        cwd=path,
        check=True,
        capture_output=True,
    )


def test_build_manifest_contains_core_keys():
    manifest = build_manifest(
        run_id="unit-test",
        wp="WP0.1",
        root=find_repo_root(),
        outputs=["placeholder.txt"],
    )

    assert manifest["run_id"] == "unit-test"
    assert manifest["work_package"] == "WP0.1"
    assert "created_utc" in manifest
    assert "python" in manifest
    assert "platform" in manifest
    assert "packages" in manifest
    assert "data_manifest" in manifest
    assert "inputs" in manifest
    assert "warnings" in manifest
    assert manifest["outputs"] == ["placeholder.txt"]


def test_manifest_records_expected_only_changes_with_relative_paths(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    expected = tmp_path / "analysis" / "reports" / "layerB_data_qc.md"
    expected.parent.mkdir(parents=True)
    expected.write_text("generated\n", encoding="utf-8")

    manifest = build_manifest(
        run_id="expected-only",
        wp="WP0.15",
        root=tmp_path,
        outputs=[expected.name],
        require_clean=True,
        expected_dirty_paths=[expected],
    )

    assert manifest["git"]["dirty"] is True
    assert manifest["git"]["expected_dirty_paths"] == [
        "analysis/reports/layerB_data_qc.md"
    ]
    assert manifest["warnings"] == [
        "git working tree contains only expected generated output changes"
    ]


def test_manifest_warns_when_unexpected_changes_are_present(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    expected = tmp_path / "analysis" / "reports" / "layerB_data_qc.md"
    expected.parent.mkdir(parents=True)
    expected.write_text("generated\n", encoding="utf-8")
    (tmp_path / "unexpected.txt").write_text("surprise\n", encoding="utf-8")

    manifest = build_manifest(
        run_id="unexpected",
        wp="WP0.15",
        root=tmp_path,
        outputs=[expected.name],
        require_clean=True,
        expected_dirty_paths=[expected],
    )

    assert manifest["warnings"] == [
        "git working tree is dirty; manuscript artefact may be non-canonical"
    ]


def test_manifest_warns_when_git_state_cannot_be_inspected(tmp_path: Path) -> None:
    manifest = build_manifest(
        run_id="not-a-repository",
        wp="WP0.15",
        root=tmp_path,
        outputs=[],
        require_clean=True,
    )

    assert manifest["git"]["dirty"] is None
    assert manifest["warnings"] == ["unable to inspect Git working tree"]

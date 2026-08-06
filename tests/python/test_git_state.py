import subprocess
from pathlib import Path

import pytest

from dsipa.git_state import (
    ensure_clean_before_mutation,
    ensure_only_expected_changes,
    git_is_dirty,
    unexpected_status_entries,
)


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
    subprocess.run(["git", "commit", "-m", "baseline"], cwd=path, check=True, capture_output=True)


def test_clean_before_mutation_rejects_unexpected_dirty_repo(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    (tmp_path / "README.md").write_text("changed\n", encoding="utf-8")

    with pytest.raises(SystemExit, match="unexplained changes before output generation"):
        ensure_clean_before_mutation(tmp_path, context="fixture")


def test_clean_before_mutation_rejects_known_upstream_outputs(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = tmp_path / "analysis" / "reports" / "layerB_data_qc.md"
    report.parent.mkdir(parents=True)
    report.write_text("generated\n", encoding="utf-8")

    with pytest.raises(SystemExit, match="unexplained changes before output generation"):
        ensure_clean_before_mutation(tmp_path, context="fixture")


def test_clean_before_mutation_fails_closed_when_git_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable(*args, **kwargs):
        raise FileNotFoundError("git")

    monkeypatch.setattr("dsipa.git_state.subprocess.run", unavailable)

    with pytest.raises(SystemExit, match="cannot inspect Git working tree"):
        ensure_clean_before_mutation(tmp_path, context="fixture")


def test_only_expected_changes_rejects_extra_file(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    expected = tmp_path / "analysis" / "reports" / "layerB_data_qc.md"
    expected.parent.mkdir(parents=True)
    expected.write_text("generated\n", encoding="utf-8")
    unexpected = tmp_path / "analysis" / "reports" / "extra.md"
    unexpected.write_text("surprise\n", encoding="utf-8")

    entries = unexpected_status_entries(tmp_path, [expected])
    assert entries is not None
    assert [entry.path for entry in entries] == ["analysis/reports/extra.md"]

    with pytest.raises(SystemExit, match="unexpected changes after output generation"):
        ensure_only_expected_changes(
            tmp_path,
            expected_paths=[expected],
            context="fixture",
        )


def test_only_expected_changes_accepts_layerb_outputs(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    expected = [
        tmp_path / "data" / "processed" / "layerB_occurrence_summary_v0_3_0.csv",
        tmp_path / "analysis" / "reports" / "layerB_data_qc.md",
    ]
    for path in expected:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("generated\n", encoding="utf-8")

    ensure_only_expected_changes(
        tmp_path,
        expected_paths=expected,
        context="fixture",
    )


def test_only_expected_changes_fails_closed_when_git_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable(*args, **kwargs):
        raise subprocess.CalledProcessError(128, ["git", "status"])

    monkeypatch.setattr("dsipa.git_state.subprocess.run", unavailable)

    with pytest.raises(SystemExit, match="cannot inspect Git working tree"):
        ensure_only_expected_changes(
            tmp_path,
            expected_paths=[tmp_path / "expected.txt"],
            context="fixture",
        )


def test_expected_destination_does_not_hide_renamed_source(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    source = tmp_path / "README.md"
    destination = tmp_path / "expected.md"
    source.rename(destination)

    entries = unexpected_status_entries(tmp_path, [destination])

    assert entries is not None
    assert [(entry.code, entry.path) for entry in entries] == [(" D", "README.md")]

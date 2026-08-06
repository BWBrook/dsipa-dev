import os
import subprocess
from pathlib import Path

from dsipa.paths import find_repo_root


def test_remote_layerA_dry_run_is_explicit_and_offline():
    root = find_repo_root()
    result = subprocess.run(
        [
            "bash",
            "analysis/deep_server_tmux_run.sh",
            "--mode",
            "layerA",
            "--workers",
            "12",
            "--states",
            "ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT",
            "--dry-run",
        ],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "DSIPA_DEEP_HOST": "must-not-be-contacted"},
    )
    assert "mode=layerA" in result.stdout
    assert "DSIPA_SKIP_LAYERB=1" in result.stdout
    assert "workers=12" in result.stdout
    assert "states=ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT" in result.stdout
    assert "command=analysis/run_full_pipeline.sh" in result.stdout


def test_pipeline_self_locates_and_checks_offline_fixture():
    script = (find_repo_root() / "analysis/run_full_pipeline.sh").read_text(encoding="utf-8")
    assert 'dirname -- "${BASH_SOURCE[0]}"' in script
    assert "tests/fixtures/layerA_triad/triad_geometries.geojson" in script
    assert "uv sync --extra dev --frozen" in script
    assert "export UV_NO_SYNC=1" in script
    assert "import build, pytest" in script
    assert script.index("uv sync --extra dev --frozen") < script.index("import build, pytest")
    assert script.index("import build, pytest") < script.index("dsipa.pa_geometry")
    assert "validate-inputs" in script
    assert script.index("validate-inputs") < script.index("dsipa.layerA_statewise")
    assert script.index("validate-outputs") < script.index("uv run pytest -rs")
    report_modules = [
        "dsipa.layerA_tables",
        "dsipa.layerA_buffer_sensitivity",
        "dsipa.layerA_threshold_sensitivity",
        "dsipa.layerA_edge_decision",
        "dsipa.layerA_watchlists --skip-supplement",
    ]
    positions = [script.index(module) for module in report_modules]
    assert positions == sorted(positions)


def test_pipeline_provisions_locked_dev_environment_before_any_analysis(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$UV_FAKE_LOG"
if [[ "$1" == "sync" ]]; then
  [[ "$*" == "sync --extra dev --frozen" ]]
  touch "$UV_FAKE_MARKER"
  exit 0
fi
if [[ "$1" == "run" ]]; then
  [[ -f "$UV_FAKE_MARKER" ]]
  [[ "${UV_NO_SYNC:-}" == "1" ]]
  [[ "$*" == *"import build, pytest"* ]]
  exit 23
fi
exit 99
""",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)
    log = tmp_path / "uv.log"
    marker = tmp_path / "dev-synced"
    result = subprocess.run(
        ["bash", "analysis/run_full_pipeline.sh"],
        cwd=find_repo_root(),
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PATH": f"{fake_bin}:{os.environ['PATH']}",
            "UV_FAKE_LOG": str(log),
            "UV_FAKE_MARKER": str(marker),
        },
    )
    assert result.returncode == 23
    assert log.read_text(encoding="utf-8").splitlines() == [
        "sync --extra dev --frozen",
        "run python -c import build, pytest",
    ]


def test_pipeline_runs_clean_start_gate_and_limits_dirty_handoff(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$UV_FAKE_LOG"
exit 0
""",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)
    log = tmp_path / "uv.log"

    result = subprocess.run(
        ["bash", "analysis/run_full_pipeline.sh"],
        cwd=find_repo_root(),
        check=True,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PATH": f"{fake_bin}:{os.environ['PATH']}",
            "UV_FAKE_LOG": str(log),
            "ALA_DOWNLOAD_EMAIL": "offline@example.org",
            "ALA_DOWNLOAD_REASON": "offline-test",
        },
    )
    commands = log.read_text(encoding="utf-8").splitlines()

    clean_gate = "run python -m dsipa.git_state require-clean --context run_full_pipeline clean-start gate"
    validate_contract = "run python -m dsipa.layerA_reproducibility validate-contract"
    assert commands.index(clean_gate) < commands.index(validate_contract)
    assert [command for command in commands if "--allow-dirty" in command] == [
        "run python -m dsipa.layerB_data --download-retries 5 --allow-dirty",
        "run python -m dsipa.layerB_qc --groups microbats,diurnal_birds --allow-dirty",
        "run python -m dsipa.layerB_model --provider dr368 --allow-dirty",
    ]

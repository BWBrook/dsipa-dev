"""Check DSIPA macOS control-plane readiness."""

from __future__ import annotations

import argparse
import importlib
import platform
import shlex
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


REQUIRED_TOOLS = ("uv", "git", "pandoc", "xelatex", "tmux", "ssh", "rsync", "sha256sum")
REQUIRED_IMPORTS = ("dsipa", "geopandas", "rasterio", "sklearn", "numpy", "pandas")


@dataclass
class Check:
    status: str
    label: str
    detail: str


def run(cmd: list[str], *, cwd: Path, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def add(checks: list[Check], status: str, label: str, detail: str) -> None:
    checks.append(Check(status=status, label=label, detail=detail))


def repo_root() -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd())
    if result.returncode != 0:
        raise SystemExit("Could not locate git repo root")
    return Path(result.stdout.strip())


def check_python(checks: list[Check], root: Path) -> None:
    if sys.version_info[:2] == (3, 12):
        add(checks, "PASS", "Python runtime", f"{platform.python_version()} at {sys.executable}")
    else:
        add(checks, "FAIL", "Python runtime", f"Expected Python 3.12, got {platform.python_version()}")

    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    requires_python = pyproject.get("project", {}).get("requires-python", "")
    if "3.12" in requires_python and "<3.13" in requires_python:
        add(checks, "PASS", "Python version bound", requires_python)
    else:
        add(checks, "FAIL", "Python version bound", f"Unexpected requires-python: {requires_python}")

    python_version_file = root / ".python-version"
    if python_version_file.exists() and python_version_file.read_text(encoding="utf-8").strip() == "3.12":
        add(checks, "PASS", ".python-version", "Pinned to 3.12")
    else:
        add(checks, "FAIL", ".python-version", "Missing or not pinned to 3.12")

    for module in REQUIRED_IMPORTS:
        try:
            importlib.import_module(module)
        except Exception as exc:
            add(checks, "FAIL", f"Import {module}", repr(exc))
        else:
            add(checks, "PASS", f"Import {module}", "ok")


def check_tools(checks: list[Check]) -> None:
    for tool in REQUIRED_TOOLS:
        path = shutil.which(tool)
        if path:
            add(checks, "PASS", f"Tool {tool}", path)
        else:
            add(checks, "FAIL", f"Tool {tool}", "not found on PATH")


def check_makedoc(checks: list[Check], root: Path, makedoc_root: Path) -> None:
    required = [
        root / "settings" / "build.yaml",
        root / "references" / "refs.yaml",
        root / "csl" / "cambridge-university-press-author-date-cambridge-a.csl",
        root / "manuscript" / "authors.yaml",
        root / "manuscript" / "text" / "references.md",
        root / "analysis" / "makedoc.sh",
    ]
    for path in required:
        if path.exists():
            add(checks, "PASS", f"File {path.relative_to(root)}", "present")
        else:
            add(checks, "FAIL", f"File {path.relative_to(root)}", "missing")

    if (makedoc_root / "Makefile").exists():
        add(checks, "PASS", "makedoc checkout", str(makedoc_root))
    else:
        add(checks, "FAIL", "makedoc checkout", f"Makefile not found under {makedoc_root}")
        return

    result = run(
        [
            "make",
            "-C",
            str(makedoc_root),
            f"CONFIG={root / 'settings' / 'build.yaml'}",
            "PROFILE=draft",
            "validate-config",
        ],
        cwd=root,
        timeout=60,
    )
    if result.returncode == 0:
        add(checks, "PASS", "makedoc validate-config", "draft profile validates")
    else:
        add(checks, "FAIL", "makedoc validate-config", result.stdout.strip()[-1000:])


def check_hpc(
    checks: list[Check],
    root: Path,
    *,
    deep_host: str,
    deep_repo: str,
    check_ssh: bool,
) -> None:
    for rel in ("analysis/deep_server_tmux_run.sh", "analysis/sync_to_deep_server.sh"):
        path = root / rel
        if not path.exists():
            add(checks, "FAIL", rel, "missing")
            continue
        result = run(["bash", "-n", str(path)], cwd=root)
        if result.returncode == 0:
            add(checks, "PASS", rel, "bash syntax ok")
        else:
            add(checks, "FAIL", rel, result.stdout.strip())

    if not check_ssh:
        add(
            checks,
            "WARN",
            "deep-server SSH",
            f"{deep_host} not probed; run with --check-ssh for live route",
        )
        return

    remote_probe = (
        "hostname && test -d /data/codex && "
        f"test -d {shlex.quote(deep_repo)} && "
        "(command -v uv >/dev/null 2>&1 || test -x \"$HOME/.local/bin/uv\") && "
        "command -v tmux >/dev/null 2>&1"
    )
    result = run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=8",
            deep_host,
            remote_probe,
        ],
        cwd=root,
        timeout=15,
    )
    if result.returncode == 0:
        detail = result.stdout.strip().replace("\n", "; ")
        add(checks, "PASS", "deep-server SSH", f"{deep_host}: {detail}; repo={deep_repo}")
    else:
        add(checks, "FAIL", "deep-server SSH", f"{deep_host}: {result.stdout.strip()[-1000:]}")


def render(checks: list[Check]) -> str:
    lines = [
        "# macOS readiness report",
        "",
        f"Host platform: `{platform.platform()}`",
        f"Python: `{platform.python_version()}`",
        "",
        "| Status | Check | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        detail = check.detail.replace("|", "\\|").replace("\n", "<br>")
        lines.append(f"| {check.status} | {check.label} | {detail} |")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--makedoc-root",
        default="/Users/bwbrook/work/makedoc",
        help="Local makedoc checkout path.",
    )
    parser.add_argument(
        "--deep-host",
        default="deep-server-ts",
        help="SSH alias for the deep-server route.",
    )
    parser.add_argument(
        "--deep-repo",
        default="/data/codex/repos/dsipa-dev-mac-sync",
        help="Remote DSIPA checkout path to verify when --check-ssh is used.",
    )
    parser.add_argument("--check-ssh", action="store_true", help="Probe deep-server SSH route.")
    parser.add_argument("--write-report", action="store_true", help="Write analysis/reports/macos_readiness.md.")
    args = parser.parse_args(argv)

    root = repo_root()
    checks: list[Check] = []

    if platform.system() == "Darwin":
        add(checks, "PASS", "Host OS", "Darwin/macOS")
    else:
        add(checks, "WARN", "Host OS", platform.platform())

    check_python(checks, root)
    check_tools(checks)
    check_makedoc(checks, root, Path(args.makedoc_root))
    check_hpc(
        checks,
        root,
        deep_host=args.deep_host,
        deep_repo=args.deep_repo,
        check_ssh=args.check_ssh,
    )

    report = render(checks)
    print(report)
    if args.write_report:
        out = root / "analysis" / "reports" / "macos_readiness.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")

    return 1 if any(check.status == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())

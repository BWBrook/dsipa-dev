#!/usr/bin/env python3
"""Extend Makedoc's PDF layout for RSEC manuscript tables."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


UPSTREAM_ENV = "DSIPA_MAKEDOC_UPSTREAM_LAYOUT_RENDER"
LANDSCAPE_PACKAGE = "\\usepackage{pdflscape}"
TABLE_LAYOUT_LINES = (
    "\\usepackage{etoolbox}",
    "\\usepackage{setspace}",
    "\\AtBeginEnvironment{longtable}{\\singlespacing}",
)
RSEC_PROFILES = {"submission", "supplementary"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="settings/build.yaml")
    parser.add_argument("--profile", default="")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def _extend_layout(content: str, profile: str) -> str:
    if profile not in RSEC_PROFILES:
        return content
    if content and not content.endswith("\n"):
        content += "\n"
    additions: list[str] = []
    if profile == "supplementary" and LANDSCAPE_PACKAGE not in content:
        additions.extend(
            [
                "% RSEC Supporting Information landscape table support",
                LANDSCAPE_PACKAGE,
            ]
        )
    missing_table_lines = [line for line in TABLE_LAYOUT_LINES if line not in content]
    if missing_table_lines:
        additions.append("% RSEC compact table spacing; body spacing is unchanged")
        additions.extend(missing_table_lines)
    if not additions:
        return content
    return content + "\n".join(additions) + "\n"


def main() -> int:
    args = parse_args()
    upstream_raw = os.environ.get(UPSTREAM_ENV, "").strip()
    upstream = Path(upstream_raw) if upstream_raw else None
    output = Path(args.output)

    if upstream is None or not upstream.is_file():
        print(f"Error: {UPSTREAM_ENV} must name the upstream layout renderer.", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_raw = tempfile.mkstemp(
        prefix=f".{output.name}.",
        suffix=".tmp",
        dir=output.parent,
    )
    os.close(fd)
    temporary = Path(temporary_raw)

    command = [
        sys.executable,
        str(upstream),
        "--config",
        args.config,
        "--output",
        str(temporary),
    ]
    if args.profile:
        command.extend(["--profile", args.profile])

    try:
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            return result.returncode

        content = temporary.read_text(encoding="utf-8")
        content = _extend_layout(content, args.profile.strip())
        encoded = content.encode("utf-8")

        if output.is_file() and output.read_bytes() == encoded:
            return 0

        temporary.write_bytes(encoded)
        os.replace(temporary, output)
        return 0
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())

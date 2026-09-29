#!/usr/bin/env python3
"""Run the bounded manuscript audits against one explicit input contract.

The orchestration layer only coordinates the existing audits.  It does not
recompute raster products or alter the input directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

try:
    from analysis.input_contract import load_manifest, sha256
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from input_contract import load_manifest, sha256


def run(args: argparse.Namespace) -> dict[str, object]:
    if args.raw_dir is None and args.existing_product_audit is None:
        raise ValueError("Provide --raw-dir or --existing-product-audit for product continuity")
    required = [
        "pa_radiance_buffers_national_v0_3_0.csv",
        "pa_trends_v0_3_0.csv",
        "pa_risk_rankings_v0_3_0.csv",
        "pa_geometries_v0_3_0.csv",
        "pa_edge_profiles_national_v0_3_0.csv",
    ]
    contract = load_manifest(args.input_manifest, args.data_dir, required)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scripts = [
        ("coauthor_evidence", "coauthor_evidence.py", args.output_dir / "coauthor_evidence"),
        ("product_continuity", "audit_product_continuity.py", args.output_dir / "product_continuity"),
        ("interior_area", "audit_interior_area.py", args.output_dir / "interior_area"),
        ("edge_followup", "audit_edge_followup.py", args.output_dir / "edge_followup"),
    ]
    commands: list[dict[str, object]] = []
    for name, script, destination in scripts:
        command = [
            sys.executable,
            str(Path(__file__).resolve().with_name(script)),
            "--input-manifest",
            str(args.input_manifest),
        ]
        if name == "coauthor_evidence":
            command += ["--data-dir", str(args.data_dir), "--output-dir", str(destination)]
        else:
            command += ["--input-dir", str(args.data_dir), "--output-dir", str(destination)] if name != "product_continuity" else ["--data-dir", str(args.data_dir), "--output-dir", str(destination)]
        if name == "product_continuity":
            if args.raw_dir is not None:
                command += ["--raw-dir", str(args.raw_dir)]
            else:
                command += ["--existing-product-audit", str(args.existing_product_audit)]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        record = {"name": name, "command": command, "returncode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]}
        commands.append(record)
        if completed.returncode:
            raise RuntimeError(f"{name} failed with exit code {completed.returncode}: {completed.stderr[-1000:]}")
    pulse_command = [sys.executable, str(Path(__file__).resolve().with_name("audit_pulse_followup.py")),
                     "--reports-dir", str(args.output_dir / "product_continuity")]
    pulse = subprocess.run(pulse_command, check=True, capture_output=True, text=True)
    commands.append({"name": "pulse_followup", "command": pulse_command, "returncode": pulse.returncode})
    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input_contract": contract.identity(),
        "commands": commands,
        "output_dir": str(args.output_dir.resolve()),
    }
    (args.output_dir / "orchestration_manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--existing-product-audit", type=Path)
    result = run(parser.parse_args())
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

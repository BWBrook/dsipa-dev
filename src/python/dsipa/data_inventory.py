"""Generate a minimal data inventory report for Layer A sources."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root


def render_report() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return """# Data inventory (Layer A)

Generated: {timestamp}

## Protected areas — CAPAD 2024 (DCCEEW)

- Snapshot date: 30 June 2024 (CAPAD 2024 compilation).
- Access: GIS data via DCCEEW ArcGIS REST services (CAPAD MapServer/FeatureServer).
- License: CC-BY (Creative Commons Attribution).
- Coverage: terrestrial + marine in a single layer; Sea Country IPAs included in marine reporting.
- Planned inclusion rule (Layer A core): terrestrial protected areas only (filter on NRS_PA flag).
- Known caveats: interim protected areas included; attributes are contributed by multiple jurisdictions.

Source URLs:
- https://www.dcceew.gov.au/environment/land/nrs/science/capad/2024
- https://gis.environment.gov.au/gispubmap/rest/services/ogc_services/CAPAD/MapServer

## Night lights — VIIRS annual average (Zenodo v0.4, Hengl/OpenGeoHub)

- Provider: OpenGeoHub (Hengl et al.), Zenodo record v0.4.
- Coverage: annual global time series (2000–2024). VIIRS-based years start 2012; core analysis uses 2013–2024.
- Resolution/CRS: 500 m (COG) in EPSG:4326.
- Variable: annual average VIIRS composite (`nightlights.average_viirs.v21_*`).
- Scaling: record notes values scaled from 0–200 to 0–2000; apply raster scale/offset metadata during metric computation (2022–2024 files report scale=10).
- Smoke-test years (WP0.6): 2013, 2018, 2024.
- Known caveats: 2012 is partial-year for VIIRS; exclude from trends.

Source URLs:
- https://doi.org/10.5281/zenodo.17294744
- https://zenodo.org/records/17294744
""".format(timestamp=timestamp)


def write_report(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(), encoding="utf-8")
    return path


def write_artefact(
    *,
    run_id: str,
    work_package: str,
    report_path: Path,
    artefact_dir: Path,
    root: Path,
) -> Path:
    artefact_dir.mkdir(parents=True, exist_ok=True)
    report_copy = artefact_dir / report_path.name
    shutil.copyfile(report_path, report_copy)

    manifest = build_manifest(
        run_id=run_id,
        wp=work_package,
        root=root,
        outputs=[report_copy.name],
        notes="WP0.3 data inventory report",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.3 data inventory artefact. Contains the data inventory report and manifest.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Layer A data inventory report.")
    parser.add_argument(
        "--report-path",
        default=None,
        help="Path for data inventory report (default: analysis/reports/data_inventory.md).",
    )
    parser.add_argument(
        "--artefact-dir",
        default=None,
        help="Artefact output directory (default: artefacts/wp0_3_data_sources).",
    )
    parser.add_argument("--run-id", default="wp0_3_data_sources")
    parser.add_argument("--work-package", default="WP0.3")
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Only write the report, not the artefact folder.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()

    report_path = Path(args.report_path) if args.report_path else root / "analysis" / "reports" / "data_inventory.md"
    report_path = write_report(report_path)

    if not args.skip_artefact:
        artefact_dir = Path(args.artefact_dir) if args.artefact_dir else root / "artefacts" / "wp0_3_data_sources"
        write_artefact(
            run_id=args.run_id,
            work_package=args.work_package,
            report_path=report_path,
            artefact_dir=artefact_dir,
            root=root,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

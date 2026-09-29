#!/usr/bin/env python3
"""Stage a verified private spatial baseline from public payloads and immutable inputs.

The command only reads source directories and creates a new baseline directory.
Public processed payloads are copied; large raster and Natural Earth inputs are
symlinked by default and recorded by hash, preserving their source identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

REFERENCE_CONTRACT = Path(__file__).resolve().parents[1] / "settings/layerA_reference_contract_v0_3_0.json"
PUBLIC_HASHES = {Path(item["path"]).name: item["sha256"]
                 for item in json.loads(REFERENCE_CONTRACT.read_text())["outputs"]}
LEGACY_LAND_SHA256 = "2eb7cea010a462e4d830ce779567d0d626b2355e4f444259616eae765be93b77"


def build_legacy_land_cache(archive: Path, destination: Path) -> None:
    """Recreate the historical sensitivity mask from its pinned public archive."""
    import geopandas as gpd
    import shapely
    from dsipa.layerA_national import _safe_geom
    expected = json.loads(REFERENCE_CONTRACT.read_text())["inputs"]["natural_earth"]["sha256"]
    if sha256(archive) != expected:
        raise ValueError("Natural Earth archive hash mismatch")
    land = gpd.read_file(f"zip://{archive.resolve()}").to_crs("EPSG:3577")
    geoms = land.geometry.apply(_safe_geom)
    result = _safe_geom(geoms[~geoms.is_empty].union_all())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(shapely.to_wkb(result))
    if sha256(destination) != LEGACY_LAND_SHA256:
        raise ValueError("Reconstructed historical land cache differs from accepted identity")


def validate_rasters(directory: Path) -> dict:
    expected = json.loads(REFERENCE_CONTRACT.read_text())["inputs"]["viirs"]["md5_by_year"]
    verified = {}
    for year, digest in expected.items():
        matches = list(directory.glob(f"*_{year}0101_*.tif"))
        if len(matches) != 1:
            raise ValueError(f"Expected one raster for {year}, got {len(matches)}")
        with matches[0].open("rb") as stream:
            observed = hashlib.file_digest(stream, "md5").hexdigest()
        if observed != digest:
            raise ValueError(f"Raster source identity mismatch for {year}")
        verified[year] = {"file": matches[0].name, "md5": observed}
    return verified


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--public-dir", type=Path, required=True, help="isolated Zenodo payload directory")
    p.add_argument("--output-dir", type=Path, required=True, help="new private baseline directory")
    p.add_argument("--raster-dir", type=Path, required=True, help="immutable accepted VIIRS raster directory")
    p.add_argument("--natural-earth-dir", type=Path, required=True, help="immutable legacy Natural Earth cache directory")
    p.add_argument("--copy-large-inputs", action="store_true", help="copy raster/cache trees instead of symlinking")
    args = p.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit(f"refusing non-empty output directory: {args.output_dir}")
    for source in (args.public_dir, args.raster_dir, args.natural_earth_dir):
        if not source.is_dir(): raise SystemExit(f"missing directory: {source}")
    processed = args.output_dir / "data" / "processed"
    processed.mkdir(parents=True)
    entries = {}
    for name, expected in PUBLIC_HASHES.items():
        source = args.public_dir / name
        if not source.is_file(): raise SystemExit(f"missing allowlisted public payload: {source}")
        observed = sha256(source)
        if observed != expected: raise SystemExit(f"public hash mismatch for {name}: {observed}")
        target = processed / name; shutil.copy2(source, target)
        entries[f"data/processed/{name}"] = {"source": str(source), "mode": "copy", "bytes": target.stat().st_size, "sha256": sha256(target), "expected_sha256": expected}
    raster_identities = validate_rasters(args.raster_dir)
    for label, source in (("data/raw/nightlights_zenodo_v0_4", args.raster_dir), ("data/raw/ne_110m_land", args.natural_earth_dir)):
        target = args.output_dir / label
        if args.copy_large_inputs: shutil.copytree(source, target)
        else: target.parent.mkdir(parents=True, exist_ok=True); target.symlink_to(source, target_is_directory=True)
        files = []
        for item in sorted(source.rglob("*")):
            if item.is_file(): files.append({"relative": str(item.relative_to(source)), "bytes": item.stat().st_size, "sha256": sha256(item)})
        entries[label] = {"source": str(source), "mode": "copy" if args.copy_large_inputs else "symlink", "files": files}
    cache = processed / "cache/land_union_ne_110m.wkb"
    build_legacy_land_cache(args.natural_earth_dir / "ne_110m_land.zip", cache)
    entries["data/processed/cache/land_union_ne_110m.wkb"] = {
        "source": "reconstructed from pinned public Natural Earth archive",
        "sha256": sha256(cache), "bytes": cache.stat().st_size}
    manifest = {"schema_version": "public-spatial-baseline-1.0.0", "public_record": "Zenodo 21524637", "verified_rasters": raster_identities, "public_payloads": entries, "raster_source": str(args.raster_dir), "natural_earth_source": str(args.natural_earth_dir), "immutability": "source trees are read-only inputs; output is a new staging directory", "next_command": "run corrected extraction with --baseline pointing at this directory and record the correction run manifest"}
    (args.output_dir / "PUBLIC_BASELINE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (args.output_dir / "README.md").write_text("# Private public spatial baseline\n\nStaged from Zenodo 21524637 processed payloads plus immutable raster and Natural Earth source trees. See `PUBLIC_BASELINE_MANIFEST.json` for allowlisted hashes and source paths. This is a private preparation artefact, not a publication release.\n")
    print(json.dumps({"output": str(args.output_dir), "payloads": len(PUBLIC_HASHES), "large_input_mode": "copy" if args.copy_large_inputs else "symlink"}, indent=2))

if __name__ == "__main__": main()

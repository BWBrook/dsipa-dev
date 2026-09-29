"""Contract-driven reproducibility checks for the frozen Layer A analysis."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd

from dsipa import schema
from dsipa.landmask import LANDMASK_SHP, LANDMASK_URL
from dsipa.nightlights import EXPECTED_MD5, download_year, filename_for_year, md5sum
from dsipa.paths import find_repo_root

REFERENCE_CONTRACT = "settings/layerA_reference_contract_v0_3_0.json"
CONTRACT_VERSION = "layerA-reference-v1"
CACHE_CONTRACT_VERSION = "layerA-union-cache-v1"


class ContractError(RuntimeError):
    """Raised when the frozen reference contract or its evidence does not match."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_reference_contract(path: Path | None = None) -> dict[str, Any]:
    contract_path = path or (find_repo_root() / REFERENCE_CONTRACT)
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"Cannot load Layer A reference contract: {contract_path}") from exc
    validate_reference_contract(contract)
    return contract


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def validate_reference_contract(contract: dict[str, Any]) -> None:
    _require(contract.get("contract_version") == CONTRACT_VERSION, "Wrong contract version.")
    _require(
        contract.get("analysis_schema_version") == schema.SCHEMA_VERSION,
        "Wrong analysis schema version.",
    )
    years = contract.get("period", {}).get("years")
    _require(years == list(range(2013, 2025)), "Contract must cover every year from 2013 to 2024.")
    _require(len(contract.get("states", [])) == 10, "Contract must contain the ten state codes.")

    viirs = contract.get("inputs", {}).get("viirs", {}).get("md5_by_year", {})
    expected_md5 = {str(year): value for year, value in EXPECTED_MD5.items()}
    _require(viirs == expected_md5, "Contract VIIRS MD5 values differ from the code-pinned values.")

    outputs = contract.get("outputs")
    _require(isinstance(outputs, list) and len(outputs) == 9, "Contract must list nine outputs.")
    paths = [item.get("path") for item in outputs]
    _require(len(set(paths)) == 9 and all(paths), "Output paths must be present and unique.")
    valid_schema_keys = set(schema.OUTPUT_SCHEMAS_BY_KEY) | {"pa_geometries_gpkg"}
    _require(
        all(item.get("schema_key") in valid_schema_keys for item in outputs),
        "Output schema key is missing or unknown.",
    )
    classifications = {
        "exact",
        "canonical_ordering_change_semantically_exact",
        "container_metadata_may_differ_semantics_exact",
    }
    for output in outputs:
        _require(output.get("classification") in classifications, "Unknown output classification.")
        _require(isinstance(output.get("rows"), int) and output["rows"] > 0, "Invalid output row count.")
        _require(
            isinstance(output.get("sha256"), str) and len(output["sha256"]) == 64,
            "Invalid output SHA-256.",
        )

    keys = contract.get("stable_keys", {})
    expected_keys = {
        "pa_radiance_buffers_national": [
            "pa_id",
            "year",
            "zone",
            "buffer_km",
            "buffer_type",
        ],
        "pa_edge_profiles_national": ["pa_id", "year", "ring_index"],
        "pa_buffer_validity": ["pa_id", "buffer_km"],
    }
    _require(keys == expected_keys, "Stable-key contract is incomplete or changed.")

    required_headlines = {
        "pa_universe",
        "inside_trend_eligible",
        "inside_2024_zero_mean",
        "inside_trend_zero_slope",
        "inside_trend_positive_slope",
        "retention_quadrant_eligible",
        "quadrant_q1_concurrent_brightening",
        "quadrant_q2_internal_brightening",
        "quadrant_q3_stable_or_non_detect",
        "quadrant_q4_external_pressure",
        "complete_rings_2024",
        "ring1_2024_valid",
        "ring1_2024_valid_fraction",
    }
    _require(
        set(contract.get("headlines", {})) == required_headlines,
        "Frozen headline set is incomplete or changed.",
    )
    reconciliation = contract.get("historical_reconciliation", {})
    _require(
        reconciliation.get("historical_value") == 1427
        and reconciliation.get("accepted_current_value") == 1432,
        "Historical 1427 versus accepted 1432 reconciliation is missing.",
    )
    _require(
        contract.get("cache_contract", {}).get("version") == CACHE_CONTRACT_VERSION,
        "Cache-contract version is missing or changed.",
    )


def stable_sort_frame(frame: pd.DataFrame, keys: list[str] | tuple[str, ...]) -> pd.DataFrame:
    missing = [key for key in keys if key not in frame.columns]
    if missing:
        raise ContractError(f"Stable sort keys missing from table: {missing}")
    return frame.sort_values(
        list(keys),
        kind="mergesort",
        na_position="last",
        ignore_index=True,
    )


def ordering_descents(frame: pd.DataFrame, keys: list[str] | tuple[str, ...]) -> int:
    ordered = stable_sort_frame(frame, keys)
    current = frame.reset_index(drop=True)
    return int(sum(not current[col].equals(ordered[col]) for col in keys) > 0)


def cache_sidecar_path(cache_path: Path) -> Path:
    return cache_path.with_suffix(cache_path.suffix + ".fingerprint.json")


def _cache_payload(
    cache_path: Path,
    *,
    algorithm: str,
    input_fingerprints: dict[str, str],
) -> dict[str, Any]:
    return {
        "cache_contract_version": CACHE_CONTRACT_VERSION,
        "algorithm": algorithm,
        "input_fingerprints": dict(sorted(input_fingerprints.items())),
        "cache_filename": cache_path.name,
        "cache_sha256": sha256_file(cache_path),
    }


def write_cache_fingerprint(
    cache_path: Path,
    *,
    algorithm: str,
    input_fingerprints: dict[str, str],
) -> Path:
    sidecar = cache_sidecar_path(cache_path)
    payload = _cache_payload(
        cache_path,
        algorithm=algorithm,
        input_fingerprints=input_fingerprints,
    )
    sidecar.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sidecar


def cache_is_reusable(
    cache_path: Path,
    *,
    algorithm: str,
    input_fingerprints: dict[str, str],
) -> bool:
    sidecar = cache_sidecar_path(cache_path)
    if not cache_path.is_file() or not sidecar.is_file():
        return False
    try:
        actual = json.loads(sidecar.read_text(encoding="utf-8"))
        expected = _cache_payload(
            cache_path,
            algorithm=algorithm,
            input_fingerprints=input_fingerprints,
        )
    except (OSError, json.JSONDecodeError):
        return False
    return actual == expected


def accepted_input_fingerprints(contract: dict[str, Any] | None = None) -> dict[str, str]:
    reference = contract or load_reference_contract()
    inputs = reference["inputs"]
    return {
        "capad_semantic_sha256": inputs["capad"]["semantic_sha256"],
        "ibra_semantic_sha256": inputs["ibra"]["semantic_sha256"],
        "natural_earth_sha256": inputs["natural_earth"]["sha256"],
    }


def _latest_snapshot(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    paths = sorted(root.glob(spec["snapshot_glob"]))
    if not paths:
        raise ContractError(f"No input snapshot matches {spec['snapshot_glob']}.")
    try:
        return json.loads(paths[-1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"Malformed input snapshot: {paths[-1]}") from exc


def prepare_accepted_inputs(root: Path, contract: dict[str, Any]) -> None:
    _prepare_pinned_landmask(root, contract["inputs"]["natural_earth"])
    viirs_dir = root / contract["inputs"]["viirs"]["directory"]
    for year in contract["period"]["years"]:
        download_year(year, viirs_dir)


def _validate_archive(path: Path, spec: dict[str, Any]) -> None:
    _require(path.is_file(), f"Natural Earth archive missing: {path}")
    _require(path.stat().st_size == spec["size_bytes"], "Natural Earth size mismatch.")
    _require(sha256_file(path) == spec["sha256"], "Natural Earth SHA-256 mismatch.")


def _prepare_pinned_landmask(root: Path, spec: dict[str, Any]) -> Path:
    archive_path = root / spec["archive_path"]
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if not archive_path.exists():
        temporary = archive_path.with_suffix(archive_path.suffix + ".tmp")
        urllib.request.urlretrieve(LANDMASK_URL, temporary)
        try:
            _validate_archive(temporary, spec)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
        temporary.replace(archive_path)
    else:
        _validate_archive(archive_path, spec)

    destination = archive_path.parent.resolve()
    with zipfile.ZipFile(archive_path, "r") as archive:
        for member in archive.infolist():
            member_path = (destination / member.filename).resolve()
            _require(
                member_path == destination or destination in member_path.parents,
                f"Unsafe Natural Earth archive member: {member.filename}",
            )
        archive.extractall(destination)
    shapefile = destination / LANDMASK_SHP
    _require(shapefile.is_file(), f"Natural Earth shapefile missing after extraction: {shapefile}")
    return shapefile


def validate_input_identities(root: Path, contract: dict[str, Any]) -> dict[str, Any]:
    evidence: dict[str, Any] = {}
    for name in ("capad", "ibra"):
        spec = contract["inputs"][name]
        snapshot = _latest_snapshot(root, spec)
        actual_count = snapshot.get("feature_count")
        actual_hash = snapshot.get(spec["snapshot_hash_field"])
        _require(actual_count == spec["feature_count"], f"{name.upper()} feature count mismatch.")
        _require(actual_hash == spec["semantic_sha256"], f"{name.upper()} semantic hash mismatch.")
        evidence[name] = {
            "feature_count": actual_count,
            "semantic_sha256": actual_hash,
            "status": "passed",
        }

    natural_earth = contract["inputs"]["natural_earth"]
    archive_path = root / natural_earth["archive_path"]
    _validate_archive(archive_path, natural_earth)
    evidence["natural_earth"] = {
        "size_bytes": archive_path.stat().st_size,
        "sha256": sha256_file(archive_path),
        "status": "passed",
    }

    viirs_spec = contract["inputs"]["viirs"]
    viirs_dir = root / viirs_spec["directory"]
    viirs_evidence = {}
    for year_text, expected in viirs_spec["md5_by_year"].items():
        path = viirs_dir / filename_for_year(int(year_text))
        _require(path.is_file(), f"VIIRS file missing for {year_text}: {path}")
        actual = md5sum(path)
        _require(actual == expected, f"VIIRS MD5 mismatch for {year_text}.")
        viirs_evidence[year_text] = actual
    evidence["viirs"] = {"files": viirs_evidence, "status": "passed"}
    return evidence


def _csv_schema_columns(schema_key: str) -> tuple[str, ...]:
    return schema.OUTPUT_SCHEMAS_BY_KEY[schema_key].column_names


def _load_output_frames(root: Path) -> dict[str, pd.DataFrame]:
    paths = {
        "geoms": schema.PA_GEOMETRIES_CSV,
        "radiance": schema.RADIANCE_BUFFERS_NATIONAL_CSV,
        "edge_profiles": schema.EDGE_PROFILES_NATIONAL_CSV,
        "buffer_validity": schema.PA_BUFFER_VALIDITY_CSV,
        "trends": schema.PA_TRENDS_CSV,
        "risk": schema.PA_RISK_RANKINGS_CSV,
    }
    return {name: pd.read_csv(root / path) for name, path in paths.items()}


def _headline_values(root: Path) -> dict[str, int | float]:
    from dsipa.layerA_tables import build_denominator_rows

    frames = _load_output_frames(root)
    rows = build_denominator_rows(**frames).set_index("key")
    headline_keys = [
        "pa_universe",
        "inside_trend_eligible",
        "inside_2024_zero_mean",
        "inside_trend_zero_slope",
        "inside_trend_positive_slope",
        "retention_quadrant_eligible",
        "quadrant_q1_concurrent_brightening",
        "quadrant_q2_internal_brightening",
        "quadrant_q3_stable_or_non_detect",
        "quadrant_q4_external_pressure",
        "complete_rings_2024",
        "ring1_2024_valid",
    ]
    values: dict[str, int | float] = {key: int(rows.loc[key, "n"]) for key in headline_keys}
    values["ring1_2024_valid_fraction"] = float(rows.loc["ring1_2024_valid", "percent"])
    return values


def validate_outputs(root: Path, contract: dict[str, Any]) -> dict[str, Any]:
    output_evidence = []
    stable_keys = contract["stable_keys"]
    for spec in contract["outputs"]:
        path = root / spec["path"]
        _require(path.is_file(), f"Required output missing: {spec['path']}")
        actual_sha = sha256_file(path)
        schema_key = spec["schema_key"]
        if path.suffix == ".csv":
            frame = pd.read_csv(path)
            _require(len(frame) == spec["rows"], f"Row-count mismatch: {spec['path']}")
            expected_columns = _csv_schema_columns(schema_key)
            _require(
                Counter(frame.columns) == Counter(expected_columns),
                f"Column mismatch: {spec['path']}",
            )
            _require(
                set(frame["schema_version"].astype(str)) == {schema.SCHEMA_VERSION},
                f"Schema-version mismatch: {spec['path']}",
            )
            keys = stable_keys.get(schema_key)
            descents = 0
            if keys:
                _require(
                    not frame.duplicated(subset=keys).any(),
                    f"Duplicate stable keys: {spec['path']}",
                )
                descents = ordering_descents(frame, keys)
                _require(descents == 0, f"Non-canonical stable-key order: {spec['path']}")
            if spec["classification"] == "exact":
                _require(actual_sha == spec["sha256"], f"Exact output hash mismatch: {spec['path']}")
        else:
            frame = gpd.read_file(path)
            _require(len(frame) == spec["rows"], f"Row-count mismatch: {spec['path']}")
            _require(
                Counter(col for col in frame.columns if col != "geometry")
                == Counter(_csv_schema_columns("pa_geometries")),
                f"GPKG attribute schema mismatch: {spec['path']}",
            )
            descents = None
        output_evidence.append(
            {
                "path": spec["path"],
                "rows": spec["rows"],
                "sha256": actual_sha,
                "reference_sha256": spec["sha256"],
                "classification": spec["classification"],
                "ordering_descents": descents,
                "status": "passed",
            }
        )

    actual_headlines = _headline_values(root)
    for key, expected in contract["headlines"].items():
        actual = actual_headlines[key]
        if isinstance(expected, float):
            _require(abs(float(actual) - expected) < 1e-12, f"Headline mismatch: {key}")
        else:
            _require(actual == expected, f"Headline mismatch: {key}")
    return {
        "status": "passed",
        "outputs": output_evidence,
        "headlines": actual_headlines,
    }


def _canonical_csv(frame: pd.DataFrame, keys: list[str] | None) -> pd.DataFrame:
    if keys:
        frame = stable_sort_frame(frame, keys)
    return frame.reset_index(drop=True)


def reconcile_outputs(
    root: Path,
    baseline_root: Path,
    contract: dict[str, Any],
) -> dict[str, Any]:
    results = []
    for spec in contract["outputs"]:
        current = root / spec["path"]
        baseline = baseline_root / spec["path"]
        _require(baseline.is_file(), f"Comparison output missing: {baseline}")
        if current.suffix == ".csv":
            keys = contract["stable_keys"].get(spec["schema_key"])
            left = _canonical_csv(pd.read_csv(current), keys)
            right = _canonical_csv(pd.read_csv(baseline), keys)
            try:
                pd.testing.assert_frame_equal(
                    left,
                    right,
                    check_dtype=False,
                    check_exact=True,
                    check_like=False,
                )
            except AssertionError as exc:
                raise ContractError(f"Semantic CSV mismatch: {spec['path']}") from exc
            semantic_equal = True
        else:
            left = gpd.read_file(current).sort_values("pa_id").reset_index(drop=True)
            right = gpd.read_file(baseline).sort_values("pa_id").reset_index(drop=True)
            left_attrs = pd.DataFrame(left.drop(columns="geometry"))
            right_attrs = pd.DataFrame(right.drop(columns="geometry"))
            try:
                pd.testing.assert_frame_equal(
                    left_attrs,
                    right_attrs,
                    check_dtype=False,
                    check_exact=True,
                )
            except AssertionError as exc:
                raise ContractError(f"GPKG attribute mismatch: {spec['path']}") from exc
            _require(left.crs == right.crs, f"GPKG CRS mismatch: {spec['path']}")
            _require(
                [geom.wkb if geom is not None else None for geom in left.geometry]
                == [geom.wkb if geom is not None else None for geom in right.geometry],
                f"GPKG geometry mismatch: {spec['path']}",
            )
            semantic_equal = True
        results.append(
            {
                "path": spec["path"],
                "current_sha256": sha256_file(current),
                "baseline_sha256": sha256_file(baseline),
                "byte_equal": sha256_file(current) == sha256_file(baseline),
                "semantic_equal": semantic_equal,
            }
        )
    return {"status": "passed", "outputs": results, "headlines": _headline_values(root)}


def _write_evidence(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-contract")

    inputs = subparsers.add_parser("validate-inputs")
    inputs.add_argument("--prepare", action="store_true")
    inputs.add_argument("--evidence", type=Path)

    outputs = subparsers.add_parser("validate-outputs")
    outputs.add_argument("--evidence", type=Path)

    reconcile = subparsers.add_parser("reconcile")
    reconcile.add_argument("--baseline", type=Path, required=True)
    reconcile.add_argument("--evidence", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    contract = load_reference_contract(root / REFERENCE_CONTRACT)
    if args.command == "validate-contract":
        payload = {"status": "passed", "contract": REFERENCE_CONTRACT}
    elif args.command == "validate-inputs":
        if args.prepare:
            prepare_accepted_inputs(root, contract)
        payload = validate_input_identities(root, contract)
        _write_evidence(args.evidence, payload)
    elif args.command == "validate-outputs":
        payload = validate_outputs(root, contract)
        _write_evidence(args.evidence, payload)
    else:
        payload = reconcile_outputs(root, args.baseline, contract)
        _write_evidence(args.evidence, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

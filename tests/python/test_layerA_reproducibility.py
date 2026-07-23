import copy
import hashlib
import json
from pathlib import Path
import zipfile

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point
from shapely import wkb

from dsipa import schema
from dsipa.layerA_reproducibility import (
    ContractError,
    _prepare_pinned_landmask,
    cache_is_reusable,
    cache_sidecar_path,
    load_reference_contract,
    ordering_descents,
    stable_sort_frame,
    validate_input_identities,
    validate_outputs,
    validate_reference_contract,
    write_cache_fingerprint,
)
from dsipa.layerA_statewise import _merge_tables
from dsipa.nightlights import filename_for_year
from dsipa.paths import find_repo_root


def _contract():
    return load_reference_contract(
        find_repo_root() / "settings/layerA_reference_contract_v0_3_0.json"
    )


def test_reference_contract_is_valid():
    validate_reference_contract(_contract())


@pytest.mark.parametrize(
    "mutate",
    [
        lambda c: c.update(contract_version="wrong"),
        lambda c: c.update(analysis_schema_version="9.9.9"),
        lambda c: c["period"].update(years=c["period"]["years"][:-1]),
        lambda c: c["outputs"].append(copy.deepcopy(c["outputs"][0])),
        lambda c: c.update(stable_keys={}),
        lambda c: c.update(headlines={}),
        lambda c: c.update(historical_reconciliation={}),
        lambda c: c["outputs"][0].update(classification="unknown"),
        lambda c: c["outputs"][0].update(sha256="not-a-hash"),
    ],
)
def test_reference_contract_mutations_fail_closed(mutate):
    contract = copy.deepcopy(_contract())
    mutate(contract)
    with pytest.raises(ContractError):
        validate_reference_contract(contract)


def test_stable_serialization_is_repeatable_and_value_preserving():
    original = pd.DataFrame(
        {
            "pa_id": ["b", "a", "a", "b"],
            "year": [2024, 2024, 2023, 2023],
            "zone": ["inside", "buffer", "inside", "buffer"],
            "buffer_km": [None, 1.0, None, 1.0],
            "buffer_type": ["inside", "raw", "inside", "raw"],
            "value": [4.0, 2.0, 1.0, 3.0],
        }
    )
    keys = ["pa_id", "year", "zone", "buffer_km", "buffer_type"]
    first = stable_sort_frame(original.sample(frac=1, random_state=1), keys)
    second = stable_sort_frame(original.sample(frac=1, random_state=2), keys)
    pd.testing.assert_frame_equal(first, second)
    assert ordering_descents(first, keys) == 0
    assert sorted(first["value"]) == sorted(original["value"])
    assert list(first.columns) == list(original.columns)


def test_state_merge_is_independent_of_state_path_order(tmp_path):
    keys = ["pa_id", "year", "ring_index"]
    left = pd.DataFrame(
        {"pa_id": ["b"], "year": [2024], "ring_index": [0], "value": [2.0]}
    )
    right = pd.DataFrame(
        {"pa_id": ["a"], "year": [2024], "ring_index": [0], "value": [1.0]}
    )
    left_path = tmp_path / "left.csv"
    right_path = tmp_path / "right.csv"
    left.to_csv(left_path, index=False)
    right.to_csv(right_path, index=False)
    first = _merge_tables([left_path, right_path], keys)
    second = _merge_tables([right_path, left_path], keys)
    pd.testing.assert_frame_equal(first, second)
    assert first["pa_id"].tolist() == ["a", "b"]


def test_input_identity_gate_positive_and_mismatch(tmp_path):
    capad_dir = tmp_path / "data/raw/capad_snapshot"
    ibra_dir = tmp_path / "data/raw/ibra_snapshot"
    ne_dir = tmp_path / "data/raw/ne_110m_land"
    viirs_dir = tmp_path / "data/raw/nightlights"
    for path in (capad_dir, ibra_dir, ne_dir, viirs_dir):
        path.mkdir(parents=True)

    (capad_dir / "capad_snapshot_20260723.json").write_text(
        json.dumps({"feature_count": 2, "semantic": "capad-ok"}),
        encoding="utf-8",
    )
    (ibra_dir / "ibra_snapshot_20260723.json").write_text(
        json.dumps({"feature_count": 3, "semantic": "ibra-ok"}),
        encoding="utf-8",
    )
    ne_bytes = b"natural-earth"
    (ne_dir / "land.zip").write_bytes(ne_bytes)
    md5_by_year = {}
    for year in range(2013, 2025):
        payload = f"viirs-{year}".encode()
        (viirs_dir / filename_for_year(year)).write_bytes(payload)
        md5_by_year[str(year)] = hashlib.md5(payload).hexdigest()
    contract = {
        "period": {"years": list(range(2013, 2025))},
        "inputs": {
            "capad": {
                "feature_count": 2,
                "semantic_sha256": "capad-ok",
                "snapshot_glob": "data/raw/capad_snapshot/*.json",
                "snapshot_hash_field": "semantic",
            },
            "ibra": {
                "feature_count": 3,
                "semantic_sha256": "ibra-ok",
                "snapshot_glob": "data/raw/ibra_snapshot/*.json",
                "snapshot_hash_field": "semantic",
            },
            "natural_earth": {
                "archive_path": "data/raw/ne_110m_land/land.zip",
                "size_bytes": len(ne_bytes),
                "sha256": hashlib.sha256(ne_bytes).hexdigest(),
            },
            "viirs": {
                "directory": "data/raw/nightlights",
                "md5_by_year": md5_by_year,
            },
        },
    }
    evidence = validate_input_identities(tmp_path, contract)
    assert all(item["status"] == "passed" for item in evidence.values())

    mismatch = copy.deepcopy(contract)
    mismatch["inputs"]["capad"]["semantic_sha256"] = "changed"
    with pytest.raises(ContractError, match="CAPAD semantic hash mismatch"):
        validate_input_identities(tmp_path, mismatch)


def _landmask_archive(path, payload=b"fresh-shapefile"):
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ne_110m_land.shp", payload)
        archive.writestr("ne_110m_land.dbf", b"fresh-dbf")
    data = path.read_bytes()
    return {
        "archive_path": "data/raw/ne_110m_land/ne_110m_land.zip",
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def test_pinned_landmask_reextracts_over_stale_members(tmp_path):
    land_dir = tmp_path / "data/raw/ne_110m_land"
    land_dir.mkdir(parents=True)
    archive_path = land_dir / "ne_110m_land.zip"
    spec = _landmask_archive(archive_path)
    shapefile = land_dir / "ne_110m_land.shp"
    shapefile.write_bytes(b"stale-shapefile")

    prepared = _prepare_pinned_landmask(tmp_path, spec)
    assert prepared.read_bytes() == b"fresh-shapefile"


def test_pinned_landmask_downloads_archive_even_when_stale_shapefile_exists(
    tmp_path,
    monkeypatch,
):
    source_archive = tmp_path / "source.zip"
    source_spec = _landmask_archive(source_archive, payload=b"downloaded-shapefile")
    land_dir = tmp_path / "data/raw/ne_110m_land"
    land_dir.mkdir(parents=True)
    (land_dir / "ne_110m_land.shp").write_bytes(b"stale-shapefile")

    def fake_download(_url, destination):
        Path(destination).write_bytes(source_archive.read_bytes())

    monkeypatch.setattr(
        "dsipa.layerA_reproducibility.urllib.request.urlretrieve",
        fake_download,
    )
    prepared = _prepare_pinned_landmask(tmp_path, source_spec)
    assert prepared.read_bytes() == b"downloaded-shapefile"
    assert (land_dir / "ne_110m_land.zip").is_file()


def test_pinned_landmask_rejects_bad_archive_before_overwriting_stale_member(tmp_path):
    land_dir = tmp_path / "data/raw/ne_110m_land"
    land_dir.mkdir(parents=True)
    archive_path = land_dir / "ne_110m_land.zip"
    spec = _landmask_archive(archive_path)
    spec["sha256"] = "0" * 64
    shapefile = land_dir / "ne_110m_land.shp"
    shapefile.write_bytes(b"stale-shapefile")

    with pytest.raises(ContractError, match="Natural Earth SHA-256 mismatch"):
        _prepare_pinned_landmask(tmp_path, spec)
    assert shapefile.read_bytes() == b"stale-shapefile"


def test_output_gate_positive_and_order_mismatch(tmp_path, monkeypatch):
    contract = copy.deepcopy(_contract())
    frames = {}
    for output in contract["outputs"]:
        output["path"] = f"outputs/{output['schema_key']}{Path(output['path']).suffix}"
        path = tmp_path / output["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test", encoding="utf-8")
        output["classification"] = "canonical_ordering_change_semantically_exact"
        output["rows"] = 2 if output["schema_key"] in contract["stable_keys"] else 1
        if path.suffix == ".csv":
            columns = list(schema.OUTPUT_SCHEMAS_BY_KEY[output["schema_key"]].column_names)
            frame = pd.DataFrame([{column: None for column in columns} for _ in range(output["rows"])])
            frame["schema_version"] = schema.SCHEMA_VERSION
            if output["schema_key"] == "pa_radiance_buffers_national":
                frame["pa_id"] = ["a", "b"]
                frame["year"] = [2024, 2024]
                frame["zone"] = ["inside", "inside"]
                frame["buffer_km"] = [None, None]
                frame["buffer_type"] = ["inside", "inside"]
            elif output["schema_key"] == "pa_edge_profiles_national":
                frame["pa_id"] = ["a", "b"]
                frame["year"] = [2024, 2024]
                frame["ring_index"] = [0, 0]
            elif output["schema_key"] == "pa_buffer_validity":
                frame["pa_id"] = ["a", "b"]
                frame["buffer_km"] = [1.0, 1.0]
            frames[path] = frame

    gpkg_columns = list(schema.PA_GEOMETRIES_COLUMNS)
    gpkg = gpd.GeoDataFrame(
        [{**{column: None for column in gpkg_columns}, "geometry": Point(0, 0)}],
        geometry="geometry",
        crs="EPSG:3577",
    )
    gpkg["schema_version"] = schema.SCHEMA_VERSION

    monkeypatch.setattr(
        "dsipa.layerA_reproducibility.pd.read_csv",
        lambda path: frames[Path(path)].copy(),
    )
    monkeypatch.setattr("dsipa.layerA_reproducibility.gpd.read_file", lambda _path: gpkg.copy())
    monkeypatch.setattr(
        "dsipa.layerA_reproducibility._headline_values",
        lambda _root: copy.deepcopy(contract["headlines"]),
    )

    evidence = validate_outputs(tmp_path, contract)
    assert evidence["status"] == "passed"

    radiance_path = next(
        path for path in frames if "pa_radiance_buffers_national" in path.name
    )
    frames[radiance_path] = frames[radiance_path].iloc[::-1].reset_index(drop=True)
    with pytest.raises(ContractError, match="Non-canonical stable-key order"):
        validate_outputs(tmp_path, contract)


@pytest.mark.parametrize("output_kind", ["csv", "gpkg"])
def test_output_gate_accepts_permuted_column_order(tmp_path, monkeypatch, output_kind):
    contract, frames, gpkg = _output_gate_fixture(tmp_path)
    if output_kind == "csv":
        csv_path = next(iter(frames))
        frames[csv_path] = frames[csv_path].loc[:, list(reversed(frames[csv_path].columns))]
    else:
        gpkg = gpkg.loc[:, list(reversed(gpkg.columns))]
    _patch_output_gate_reads(monkeypatch, frames, gpkg, contract)

    evidence = validate_outputs(tmp_path, contract)

    assert evidence["status"] == "passed"


@pytest.mark.parametrize("output_kind", ["csv", "gpkg"])
@pytest.mark.parametrize("mutation", ["missing", "extra", "duplicate"])
def test_output_gate_rejects_column_name_multiset_mismatch(
    tmp_path,
    monkeypatch,
    output_kind,
    mutation,
):
    contract, frames, gpkg = _output_gate_fixture(tmp_path)
    if output_kind == "csv":
        path = next(iter(frames))
        frame = frames[path]
        if mutation == "missing":
            frames[path] = frame.drop(columns=[frame.columns[-1]])
        elif mutation == "extra":
            frames[path] = frame.assign(unexpected_column=None)
        else:
            columns = list(frame.columns)
            columns[-1] = columns[0]
            frame.columns = columns
    else:
        attributes = [column for column in gpkg.columns if column != "geometry"]
        if mutation == "missing":
            gpkg = gpkg.drop(columns=[attributes[-1]])
        elif mutation == "extra":
            gpkg = gpkg.assign(unexpected_column=None)
        else:
            columns = list(gpkg.columns)
            columns[columns.index(attributes[-1])] = attributes[0]
            gpkg.columns = columns
    _patch_output_gate_reads(monkeypatch, frames, gpkg, contract)

    expected = "Column mismatch" if output_kind == "csv" else "GPKG attribute schema mismatch"
    with pytest.raises(ContractError, match=expected):
        validate_outputs(tmp_path, contract)


def _output_gate_fixture(tmp_path):
    contract = copy.deepcopy(_contract())
    frames = {}
    selected = []
    for output in contract["outputs"]:
        if output["schema_key"] not in {"pa_geometries", "pa_geometries_gpkg"}:
            continue
        output["path"] = f"outputs/{output['schema_key']}{Path(output['path']).suffix}"
        output["classification"] = "container_metadata_may_differ_semantics_exact"
        output["rows"] = 1
        path = tmp_path / output["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test", encoding="utf-8")
        selected.append(output)
        if path.suffix == ".csv":
            columns = list(schema.OUTPUT_SCHEMAS_BY_KEY["pa_geometries"].column_names)
            frame = pd.DataFrame([{column: None for column in columns}])
            frame["schema_version"] = schema.SCHEMA_VERSION
            frames[path] = frame
    contract["outputs"] = selected

    gpkg = gpd.GeoDataFrame(
        [
            {
                **{column: None for column in schema.PA_GEOMETRIES_COLUMNS},
                "geometry": Point(0, 0),
            }
        ],
        geometry="geometry",
        crs="EPSG:3577",
    )
    gpkg["schema_version"] = schema.SCHEMA_VERSION
    return contract, frames, gpkg


def _patch_output_gate_reads(monkeypatch, frames, gpkg, contract):
    monkeypatch.setattr(
        "dsipa.layerA_reproducibility.pd.read_csv",
        lambda path: frames[Path(path)].copy(),
    )
    monkeypatch.setattr("dsipa.layerA_reproducibility.gpd.read_file", lambda _path: gpkg.copy())
    monkeypatch.setattr(
        "dsipa.layerA_reproducibility._headline_values",
        lambda _root: copy.deepcopy(contract["headlines"]),
    )


def test_cache_fingerprint_reuse_and_fail_closed_mismatches(tmp_path):
    cache = tmp_path / "union.wkb"
    cache.write_bytes(wkb.dumps(Point(1, 2)))
    inputs = {"capad_semantic_sha256": "accepted"}
    algorithm = "union-v1"
    assert not cache_is_reusable(cache, algorithm=algorithm, input_fingerprints=inputs)

    write_cache_fingerprint(cache, algorithm=algorithm, input_fingerprints=inputs)
    assert cache_is_reusable(cache, algorithm=algorithm, input_fingerprints=inputs)
    assert not cache_is_reusable(
        cache,
        algorithm=algorithm,
        input_fingerprints={"capad_semantic_sha256": "changed"},
    )

    sidecar = cache_sidecar_path(cache)
    sidecar.write_text("{broken", encoding="utf-8")
    assert not cache_is_reusable(cache, algorithm=algorithm, input_fingerprints=inputs)

    write_cache_fingerprint(cache, algorithm=algorithm, input_fingerprints=inputs)
    cache.write_bytes(cache.read_bytes() + b"changed")
    assert not cache_is_reusable(cache, algorithm=algorithm, input_fingerprints=inputs)


def test_cache_fingerprint_sidecar_has_bounded_contract(tmp_path):
    cache = tmp_path / "land.wkb"
    cache.write_bytes(wkb.dumps(Point(0, 0)))
    sidecar = write_cache_fingerprint(
        cache,
        algorithm="land-union-v1",
        input_fingerprints={"natural_earth_sha256": "accepted"},
    )
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    assert set(payload) == {
        "cache_contract_version",
        "algorithm",
        "input_fingerprints",
        "cache_filename",
        "cache_sha256",
    }

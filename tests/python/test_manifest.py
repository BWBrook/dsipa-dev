from dsipa.manifest import build_manifest
from dsipa.paths import find_repo_root


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

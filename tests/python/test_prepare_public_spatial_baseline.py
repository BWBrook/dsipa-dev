import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location("prepare_public_spatial_baseline", Path(__file__).parents[2] / "analysis" / "prepare_public_spatial_baseline.py")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
PUBLIC_HASHES, main = _MODULE.PUBLIC_HASHES, _MODULE.main

def _payloads(root: Path, monkeypatch):
    for name in PUBLIC_HASHES:
        p = root / name; p.write_bytes((name + "\n").encode())
        monkeypatch.setitem(PUBLIC_HASHES, name, hashlib.sha256(p.read_bytes()).hexdigest())

def test_stages_allowlisted_payloads_and_symlinks(tmp_path, monkeypatch):
    public, raster, ne, out = (tmp_path / x for x in ("public", "raster", "ne", "out"))
    public.mkdir(); raster.mkdir(); ne.mkdir(); (raster / "a.tif").write_bytes(b"raster"); (ne / "README").write_bytes(b"ne")
    _payloads(public, monkeypatch)
    monkeypatch.setattr(_MODULE, "validate_rasters", lambda directory: {"verified": True})
    monkeypatch.setattr(_MODULE, "build_legacy_land_cache", lambda archive, target: (target.parent.mkdir(parents=True), target.write_bytes(b"verified cache")))
    monkeypatch.setattr("sys.argv", ["prepare", "--public-dir", str(public), "--output-dir", str(out), "--raster-dir", str(raster), "--natural-earth-dir", str(ne)])
    main()
    manifest = json.loads((out / "PUBLIC_BASELINE_MANIFEST.json").read_text())
    assert manifest["public_payloads"]["data/processed/pa_geometries_v0_3_0.gpkg"]["mode"] == "copy"
    assert (out / "data/raw/nightlights_zenodo_v0_4").is_symlink()

def test_refuses_hash_mismatch(tmp_path, monkeypatch):
    public, raster, ne, out = (tmp_path / x for x in ("public", "raster", "ne", "out"))
    public.mkdir(); raster.mkdir(); ne.mkdir()
    for name in PUBLIC_HASHES: (public / name).write_bytes(b"wrong")
    monkeypatch.setattr("sys.argv", ["prepare", "--public-dir", str(public), "--output-dir", str(out), "--raster-dir", str(raster), "--natural-earth-dir", str(ne)])
    with pytest.raises(SystemExit, match="public hash mismatch"):
        main()

from pathlib import Path
import zipfile

import pytest

from dsipa.layerB_data import (
    MIN_DATA_BYTES,
    _is_valid_zip,
    _validate_download_zip,
    find_valid_zips,
    iter_csv_chunks_from_zip,
)


def _write_zip(path: Path, files: dict[str, str]) -> Path:
    with zipfile.ZipFile(path, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return path


def _valid_csv() -> str:
    header = "occurrenceID,decimalLatitude\n"
    row = "test-occurrence," + ("1" * MIN_DATA_BYTES) + "\n"
    return header + row


def test_malformed_zip_payload_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "microbats_malformed.zip"
    path.write_bytes(b"not a zip payload")

    with pytest.raises(zipfile.BadZipFile):
        _validate_download_zip(path)
    assert not _is_valid_zip(path)


def test_zip_without_csv_is_rejected(tmp_path: Path) -> None:
    path = _write_zip(tmp_path / "microbats_no_csv.zip", {"readme.txt": "no data"})

    with pytest.raises(RuntimeError, match="No CSV files"):
        _validate_download_zip(path)
    assert not _is_valid_zip(path)


def test_too_small_data_csv_is_rejected(tmp_path: Path) -> None:
    path = _write_zip(tmp_path / "microbats_tiny.zip", {"data.csv": "id\n"})

    with pytest.raises(RuntimeError, match="sentinel/empty"):
        _validate_download_zip(path)
    assert not _is_valid_zip(path)


def test_large_data_csv_with_too_few_rows_is_rejected(tmp_path: Path) -> None:
    header_only = "occurrenceID," + ("x" * MIN_DATA_BYTES) + "\n"
    path = _write_zip(tmp_path / "microbats_header_only.zip", {"data.csv": header_only})

    with pytest.raises(RuntimeError, match="too few rows"):
        _validate_download_zip(path)
    assert not _is_valid_zip(path)


def test_minimally_valid_data_csv_is_accepted(tmp_path: Path) -> None:
    path = _write_zip(tmp_path / "microbats_valid.zip", {"data.csv": _valid_csv()})

    _validate_download_zip(path)
    assert _is_valid_zip(path)
    chunks = list(iter_csv_chunks_from_zip(path, chunksize=1))
    assert len(chunks) == 1
    assert chunks[0]["occurrenceID"].tolist() == ["test-occurrence"]


def test_find_valid_zips_filters_invalid_candidates(tmp_path: Path) -> None:
    valid_path = _write_zip(tmp_path / "microbats_20240101T000000Z.zip", {"data.csv": _valid_csv()})
    _write_zip(tmp_path / "microbats_20240102T000000Z.zip", {"data.csv": "id\n"})
    (tmp_path / "microbats_20240103T000000Z.zip").write_bytes(b"not a zip payload")
    _write_zip(tmp_path / "diurnal_birds_20240101T000000Z.zip", {"data.csv": _valid_csv()})

    assert find_valid_zips(tmp_path, "microbats") == [valid_path]

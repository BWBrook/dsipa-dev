"""Night-lights dataset helpers (Zenodo OpenGeoHub v0.4)."""

from __future__ import annotations

import hashlib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ZENODO_RECORD_ID = "17294744"
ZENODO_BASE = f"https://zenodo.org/records/{ZENODO_RECORD_ID}"
FILE_TEMPLATE = (
    "nightlights.average_viirs.v21_m_500m_s_{year}0101_{year}1231_go_epsg4326_v20250904.tif"
)

EXPECTED_MD5 = {
    2013: "b60fb30a5039aff28e943179ec797f3f",
    2014: "c9505d985dbfef015e4f23f3d0172f32",
    2015: "2dbb7b5930a218778636bea0eeb9afb1",
    2016: "a75f58ecdffb7c62e6af2a0464139551",
    2017: "380fcdc877f0213f023ee41372ff7894",
    2018: "b1818a74dd2bc41e7253a5df76533a9c",
    2019: "88933a6aa669fa863a998b92f9d25c92",
    2020: "2e2756b276a293dc4c2932c9ccb1f7e4",
    2021: "f200a2292de85badfbadb557621cdd6b",
    2022: "d0952d107adfd943478f1635a2eb987e",
    2023: "7108c72e049e2e718213816e3dad3ed2",
    2024: "0b976892d40c2d0d99177c727289eaf2",
}

CORE_YEARS = tuple(sorted(EXPECTED_MD5.keys()))


@dataclass(frozen=True)
class NightlightsFile:
    year: int
    path: Path
    md5: str | None


def filename_for_year(year: int) -> str:
    return FILE_TEMPLATE.format(year=year)


def url_for_year(year: int) -> str:
    return f"{ZENODO_BASE}/files/{filename_for_year(year)}?download=1"


def md5sum(path: Path) -> str:
    hash_md5 = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_year(year: int, dest_dir: Path) -> NightlightsFile:
    if year not in EXPECTED_MD5:
        raise ValueError(f"No expected checksum registered for year {year}.")

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename_for_year(year)

    if dest_path.exists():
        existing_md5 = md5sum(dest_path)
        if existing_md5 == EXPECTED_MD5[year]:
            return NightlightsFile(year=year, path=dest_path, md5=existing_md5)

    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    url = url_for_year(year)
    urllib.request.urlretrieve(url, tmp_path)

    downloaded_md5 = md5sum(tmp_path)
    if downloaded_md5 != EXPECTED_MD5[year]:
        tmp_path.unlink(missing_ok=True)
        raise RuntimeError(
            f"Checksum mismatch for {year}: expected {EXPECTED_MD5[year]}, got {downloaded_md5}"
        )

    tmp_path.replace(dest_path)
    return NightlightsFile(year=year, path=dest_path, md5=downloaded_md5)

"""Land mask helpers (Natural Earth)."""

from __future__ import annotations

import urllib.request
import zipfile
from pathlib import Path

LANDMASK_URL = "https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_land.zip"
LANDMASK_ARCHIVE = "ne_110m_land.zip"
LANDMASK_SHP = "ne_110m_land.shp"


def download_landmask(dest_dir: Path) -> Path:
    """Download and unpack the Natural Earth landmask shapefile if missing."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    shp_path = dest_dir / LANDMASK_SHP
    if shp_path.exists():
        return shp_path

    zip_path = dest_dir / LANDMASK_ARCHIVE
    if not zip_path.exists():
        urllib.request.urlretrieve(LANDMASK_URL, zip_path)

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(dest_dir)

    if not shp_path.exists():
        raise FileNotFoundError(f"Landmask shapefile not found after extraction: {shp_path}")
    return shp_path

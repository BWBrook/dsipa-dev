"""Layer B data acquisition + QC (WP0.15)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import requests
from pyproj import Transformer

from dsipa.manifest import build_manifest, write_manifest
from dsipa.paths import find_repo_root
from dsipa.schema import LAYERB_OCCURRENCE_SUMMARY_CSV, SCHEMA_VERSION

BASE_URL = "https://biocache.ala.org.au/ws"
DOWNLOAD_ENDPOINT = f"{BASE_URL}/occurrences/download"
SEARCH_ENDPOINT = f"{BASE_URL}/occurrences/search"
REASON_ENDPOINTS = (
    "https://logger.ala.org.au/service/logger/reasons",
    "https://logger.test.ala.org.au/service/logger/reasons",
)

DEFAULT_YEARS = (2013, 2024)
DEFAULT_UNCERTAINTY_M = 1000

DEFAULT_FIELDS = [
    "occurrenceID",
    "eventDate",
    "year",
    "month",
    "day",
    "decimalLatitude",
    "decimalLongitude",
    "coordinateUncertaintyInMeters",
    "scientificName",
    "taxonRank",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "species",
    "basisOfRecord",
    "occurrenceStatus",
    "establishmentMeans",
    "stateProvince",
    "dataResourceUid",
]

CANDIDATE_DATA_FILES = ("data.csv",)
MIN_DATA_BYTES = 1024
MIN_DATA_ROWS = 2

COLUMN_ALIASES = {
    "event date": "eventDate",
    "year": "year",
    "month": "month",
    "day": "day",
    "decimal latitude (wgs84)": "decimalLatitude",
    "decimal longitude (wgs84)": "decimalLongitude",
    "coordinate uncertainty in metres": "coordinateUncertaintyInMeters",
    "coordinate uncertainty in meters": "coordinateUncertaintyInMeters",
    "scientific name (intepreted)": "scientificName",
    "scientific name (interpreted)": "scientificName",
    "taxon rank": "taxonRank",
    "kingdom": "kingdom",
    "phylum": "phylum",
    "class": "class",
    "order": "order",
    "family": "family",
    "genus": "genus",
    "species": "species",
    "basis of record": "basisOfRecord",
    "occurrence status": "occurrenceStatus",
    "establishmentmeans": "establishmentMeans",
    "state - parsed": "stateProvince",
    "data resource id": "dataResourceUid",
}


@dataclass(frozen=True)
class TaxonQuery:
    key: str
    label: str
    q: str
    fq: tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class DownloadResult:
    query: TaxonQuery
    path: Path
    record_count: int | None
    response_status: int
    content_type: str | None
    downloaded_at: str


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _git_dirty(root: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:  # pragma: no cover
        return False
    return bool(result.stdout.strip())


def _ensure_clean_tree(root: Path, allow_dirty: bool) -> None:
    if allow_dirty:
        return
    if _git_dirty(root):
        raise SystemExit("Working tree is dirty; commit or use --allow-dirty to proceed.")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def _normalize_reason(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def fetch_reason_catalog() -> list[dict[str, object]]:
    for url in REASON_ENDPOINTS:
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            payload = resp.json()
        except Exception:
            continue

        if isinstance(payload, dict):
            payload = payload.get("reasons", [])
        if isinstance(payload, list):
            return payload
    return []


def resolve_reason_id(reason: str | None, reason_id: str | None) -> str:
    if reason_id:
        return str(reason_id).strip()
    if not reason:
        raise SystemExit("ALA download requires --reason or --reason-id (or env vars).")

    reason_norm = _normalize_reason(reason)
    if reason_norm.isdigit():
        return reason_norm

    reasons = fetch_reason_catalog()
    if not reasons:
        raise SystemExit(
            "Unable to fetch ALA download reasons; supply --reason-id explicitly."
        )

    exact = []
    partial = []
    for entry in reasons:
        name = _normalize_reason(str(entry.get("name", "")))
        entry_id = str(entry.get("id", "")).strip()
        if not name or not entry_id:
            continue
        if reason_norm == name:
            exact.append(entry)
        if reason_norm in name:
            partial.append(entry)

    candidates = exact or partial
    if candidates:
        if "research" in reason_norm:
            for entry in candidates:
                if "scientific research" in _normalize_reason(str(entry.get("name", ""))):
                    return str(entry.get("id"))
        if len(candidates) == 1:
            return str(candidates[0].get("id"))

    available = ", ".join(
        f"{entry.get('name')} (id={entry.get('id')})"
        for entry in reasons
        if entry.get("name") and entry.get("id")
    )
    raise SystemExit(
        "Unable to resolve ALA download reason. "
        f"Provide --reason-id; available reasons: {available}"
    )


def build_queries(year_start: int, year_end: int, uncertainty_m: int) -> list[TaxonQuery]:
    base_filters = [
        f"year:[{year_start} TO {year_end}]",
        "taxonRank:species",
        "occurrenceStatus:present",
        f"coordinateUncertaintyInMeters:[0 TO {uncertainty_m}]",
        "country:Australia",
    ]
    return [
        TaxonQuery(
            key="microbats",
            label="Microbats (Chiroptera excluding Pteropodidae)",
            q="*:*",
            fq=tuple(base_filters + ["order:Chiroptera", "-family:Pteropodidae"]),
            notes="Nocturnal focal taxa; excludes fruit bats.",
        ),
        TaxonQuery(
            key="diurnal_birds",
            label="Diurnal birds proxy (Passeriformes)",
            q="*:*",
            fq=tuple(base_filters + ["class:Aves", "order:Passeriformes"]),
            notes="Negative control proxy; Passeriformes used as diurnal birds.",
        ),
        TaxonQuery(
            key="diurnal_reptiles",
            label="Diurnal reptiles proxy (Squamata)",
            q="*:*",
            fq=tuple(base_filters + ["class:Reptilia", "order:Squamata"]),
            notes="Negative control proxy; Squamata used as diurnal reptiles.",
        ),
    ]


def fetch_count(query: TaxonQuery) -> int | None:
    params = {"q": query.q, "fq": list(query.fq), "pageSize": 0}
    try:
        resp = requests.get(SEARCH_ENDPOINT, params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        return int(payload.get("totalRecords")) if "totalRecords" in payload else None
    except Exception:
        return None


def _download_from_url(url: str, out_path: Path) -> tuple[int, str | None]:
    with requests.get(url, stream=True, timeout=60) as resp:
        content_type = resp.headers.get("Content-Type")
        resp.raise_for_status()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as handle:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    return resp.status_code, content_type


def download_occurrences(
    *,
    query: TaxonQuery,
    email: str,
    reason_id: str,
    out_dir: Path,
    fields: Iterable[str],
    retries: int = 3,
    backoff_s: int = 20,
) -> DownloadResult:
    params = {
        "q": query.q,
        "fq": list(query.fq),
        "email": email,
        "reasonTypeId": reason_id,
        "fields": ",".join(fields),
    }
    response = None
    for attempt in range(1, retries + 1):
        response = requests.get(DOWNLOAD_ENDPOINT, params=params, timeout=60, stream=True)
        if response.status_code >= 500 and attempt < retries:
            time.sleep(backoff_s * attempt)
            continue
        break
    if response is None:
        raise RuntimeError("Download request failed before receiving a response.")
    content_type = response.headers.get("Content-Type")
    downloaded_at = _now_utc()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{_slug(query.key)}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.zip"

    if response.status_code >= 400:
        text = response.text[:500]
        raise RuntimeError(f"Download request failed ({response.status_code}): {text}")

    if content_type and "zip" in content_type.lower():
        with out_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
        _validate_download_zip(out_path)
        return DownloadResult(
            query=query,
            path=out_path,
            record_count=None,
            response_status=response.status_code,
            content_type=content_type,
            downloaded_at=downloaded_at,
        )

    if content_type and "json" in content_type.lower():
        payload = response.json()
        download_url = payload.get("downloadUrl") or payload.get("url")
        if download_url:
            status, dl_type = _download_from_url(download_url, out_path)
            _validate_download_zip(out_path)
            return DownloadResult(
                query=query,
                path=out_path,
                record_count=payload.get("totalRecords"),
                response_status=status,
                content_type=dl_type,
                downloaded_at=downloaded_at,
            )
        raise RuntimeError(f"Unexpected JSON response: {payload}")

    text = response.text
    match = re.search(r"https?://[^\s]+", text)
    if match:
        status, dl_type = _download_from_url(match.group(0), out_path)
        _validate_download_zip(out_path)
        return DownloadResult(
            query=query,
            path=out_path,
            record_count=None,
            response_status=status,
            content_type=dl_type,
            downloaded_at=downloaded_at,
        )

    response_path = out_dir / f"{_slug(query.key)}_download_response.txt"
    response_path.write_text(text, encoding="utf-8")
    raise RuntimeError(
        "Download response did not contain a zip or URL. "
        f"Saved response to {response_path}."
    )


def _select_data_csv(zf: zipfile.ZipFile) -> str:
    csv_infos = [info for info in zf.infolist() if info.filename.lower().endswith(".csv")]
    if not csv_infos:
        raise RuntimeError("No CSV files found in ALA download.")

    for info in csv_infos:
        if info.filename.lower() in CANDIDATE_DATA_FILES:
            selected = info
            break
    else:
        selected = max(csv_infos, key=lambda info: info.file_size)

    if selected.file_size < MIN_DATA_BYTES:
        raise RuntimeError(
            f"ALA download appears to be a sentinel/empty file "
            f"({selected.filename} size={selected.file_size} bytes)."
        )

    with zf.open(selected.filename) as handle:
        rows = 0
        for _ in handle:
            rows += 1
            if rows >= MIN_DATA_ROWS:
                break
        if rows < MIN_DATA_ROWS:
            raise RuntimeError(
                f"ALA download data file has too few rows ({rows}); "
                "treating as failed download."
            )

    return selected.filename


def _validate_download_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as zf:
        _select_data_csv(zf)


def iter_csv_chunks_from_zip(path: Path, chunksize: int = 100_000) -> Iterable[pd.DataFrame]:
    with zipfile.ZipFile(path) as zf:
        name = _select_data_csv(zf)
        with zf.open(name) as handle:
            reader = pd.read_csv(handle, dtype=str, chunksize=chunksize)
            for chunk in reader:
                yield chunk


def _is_valid_zip(path: Path) -> bool:
    try:
        _validate_download_zip(path)
        return True
    except zipfile.BadZipFile:
        return False
    except RuntimeError:
        return False


def find_valid_zips(raw_dir: Path, key: str) -> list[Path]:
    candidates = sorted(raw_dir.glob(f"{_slug(key)}_*.zip"))
    return [path for path in candidates if _is_valid_zip(path)]


def find_latest_zip(raw_dir: Path, key: str) -> Path | None:
    candidates = find_valid_zips(raw_dir, key)
    return candidates[-1] if candidates else None


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    for col in df.columns:
        key = col.strip().lower()
        if key in COLUMN_ALIASES:
            rename[col] = COLUMN_ALIASES[key]
    if rename:
        return df.rename(columns=rename)
    return df


def _parse_event_date(df: pd.DataFrame) -> pd.Series:
    if "eventDate" in df.columns:
        parsed = pd.to_datetime(df["eventDate"], errors="coerce", utc=True)
        if parsed.notna().any():
            return parsed.dt.date.astype("string")
    year = _coerce_numeric(df.get("year", pd.Series([np.nan] * len(df))))
    month = _coerce_numeric(df.get("month", pd.Series([np.nan] * len(df))))
    day = _coerce_numeric(df.get("day", pd.Series([np.nan] * len(df))))
    dates = []
    for y, m, d in zip(year, month, day):
        if np.isnan(y):
            dates.append(pd.NA)
        else:
            m_val = int(m) if not np.isnan(m) else 0
            d_val = int(d) if not np.isnan(d) else 0
            dates.append(f"{int(y):04d}-{m_val:02d}-{d_val:02d}")
    return pd.Series(dates, dtype="string")


def apply_quality_filters(df: pd.DataFrame, uncertainty_m: int) -> pd.DataFrame:
    df = normalize_columns(df.copy())
    df["decimalLatitude"] = _coerce_numeric(df["decimalLatitude"])
    df["decimalLongitude"] = _coerce_numeric(df["decimalLongitude"])
    df["coordinateUncertaintyInMeters"] = _coerce_numeric(df["coordinateUncertaintyInMeters"])

    df = df.dropna(subset=["decimalLatitude", "decimalLongitude"])
    df = df[df["coordinateUncertaintyInMeters"].fillna(np.inf) <= uncertainty_m]

    if "taxonRank" in df.columns:
        df = df[df["taxonRank"].str.lower() == "species"]

    if "occurrenceStatus" in df.columns:
        df = df[df["occurrenceStatus"].str.lower().fillna("") != "absent"]

    if "establishmentMeans" in df.columns:
        bad = df["establishmentMeans"].str.lower().fillna("")
        mask = bad.str.contains("captive|cultivated|escape|escaped|feral|domesticated|managed")
        df = df[~mask]

    df["event_date_key"] = _parse_event_date(df)
    df = df[df["event_date_key"].notna()]
    return df


def dedupe_occurrences(df: pd.DataFrame, transformer: Transformer, seen: set[str]) -> pd.DataFrame:
    df = df.reset_index(drop=True)
    x, y = transformer.transform(
        df["decimalLongitude"].to_numpy(),
        df["decimalLatitude"].to_numpy(),
    )
    grid_x = np.floor(x / 1000.0).astype(int)
    grid_y = np.floor(y / 1000.0).astype(int)
    species = df.get("species", df.get("scientificName"))
    if species is None:
        species = pd.Series(["unknown"] * len(df))
    species = species.astype("string").fillna("unknown").to_numpy()
    dates = df["event_date_key"].astype("string").to_numpy()
    grid_x_str = grid_x.astype(str)
    grid_y_str = grid_y.astype(str)
    keep_mask = []
    for sp, date, gx, gy in zip(species, dates, grid_x_str, grid_y_str):
        key = f"{sp}|{date}|{gx}|{gy}"
        if key in seen:
            keep_mask.append(False)
        else:
            seen.add(key)
            keep_mask.append(True)
    return df.loc[keep_mask].copy()


def process_occurrences(
    *,
    query: TaxonQuery,
    raw_paths: Iterable[Path],
    processed_dir: Path,
    uncertainty_m: int,
) -> dict[str, object]:
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / f"{_slug(query.key)}_occurrences_filtered_v{SCHEMA_VERSION.replace('.', '_')}.csv.gz"

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
    seen: set[str] = set()

    counts = {
        "raw": 0,
        "filtered": 0,
        "dedup": 0,
        "unique_species": set(),
    }
    year_counts: dict[str, int] = {}
    state_counts: dict[str, int] = {}
    missing_uncertainty = 0

    first_chunk = True
    for raw_path in raw_paths:
        for chunk in iter_csv_chunks_from_zip(raw_path):
            chunk = normalize_columns(chunk)
            counts["raw"] += len(chunk)
            if "coordinateUncertaintyInMeters" in chunk.columns:
                missing_uncertainty += chunk["coordinateUncertaintyInMeters"].isna().sum()

            filtered = apply_quality_filters(chunk, uncertainty_m)
            if filtered.empty:
                continue
            counts["filtered"] += len(filtered)

            filtered = dedupe_occurrences(filtered, transformer, seen)
            if filtered.empty:
                continue
            counts["dedup"] += len(filtered)

            species = filtered.get("species", filtered.get("scientificName"))
            if species is not None:
                counts["unique_species"].update(species.dropna().unique())

            if "year" in filtered.columns:
                for value, subcount in filtered["year"].value_counts(dropna=True).items():
                    year_counts[str(value)] = year_counts.get(str(value), 0) + int(subcount)

            if "stateProvince" in filtered.columns:
                for value, subcount in filtered["stateProvince"].value_counts(dropna=True).items():
                    state_counts[str(value)] = state_counts.get(str(value), 0) + int(subcount)

            filtered["group"] = query.key
            filtered.to_csv(
                out_path,
                mode="wt" if first_chunk else "at",
                index=False,
                compression="gzip",
                header=first_chunk,
            )
            first_chunk = False

    return {
        "group": query.key,
        "label": query.label,
        "raw_records": counts["raw"],
        "filtered_records": counts["filtered"],
        "dedup_records": counts["dedup"],
        "unique_species": len(counts["unique_species"]),
        "missing_uncertainty_fraction": (missing_uncertainty / counts["raw"]) if counts["raw"] else np.nan,
        "year_counts": year_counts,
        "state_counts": state_counts,
        "output_path": str(out_path),
    }


def write_summary(summary_rows: list[dict[str, object]], out_path: Path) -> None:
    rows = []
    for row in summary_rows:
        rows.append(
            {
                "schema_version": SCHEMA_VERSION,
                "group": row["group"],
                "label": row["label"],
                "raw_records": row["raw_records"],
                "filtered_records": row["filtered_records"],
                "dedup_records": row["dedup_records"],
                "unique_species": row["unique_species"],
            }
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)


def write_qc_report(
    summary_rows: list[dict[str, object]],
    report_path: Path,
    queries: Iterable[TaxonQuery],
    uncertainty_m: int,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Layer B data QC",
        "",
        f"Generated: {_now_utc()}",
        "",
        f"Coordinate uncertainty filter: <= {uncertainty_m} m",
        "",
    ]

    lines.append("## Query definitions")
    lines.append("")
    for query in queries:
        lines.append(f"- {query.key}: {query.label}")
        lines.append(f"  - Notes: {query.notes}")
        lines.append(f"  - fq: {', '.join(query.fq)}")
    lines.append("")

    lines.append("## Summary counts")
    lines.append("")
    summary_df = pd.DataFrame(summary_rows)
    if not summary_df.empty:
        display = summary_df[["group", "raw_records", "filtered_records", "dedup_records", "unique_species"]]
        lines.append(display.to_string(index=False))
    else:
        lines.append("No summary rows available.")
    lines.append("")

    for row in summary_rows:
        lines.append(f"## {row['group']} yearly counts (post-dedup)")
        lines.append("")
        year_counts = row.get("year_counts", {})
        if year_counts:
            year_df = pd.DataFrame(sorted(year_counts.items()), columns=["year", "records"]).set_index("year")
            lines.append(year_df.to_string())
        else:
            lines.append("No yearly counts available.")
        lines.append("")

        lines.append(f"## {row['group']} state counts (post-dedup)")
        lines.append("")
        state_counts = row.get("state_counts", {})
        if state_counts:
            state_df = pd.DataFrame(sorted(state_counts.items()), columns=["state", "records"]).set_index("state")
            lines.append(state_df.to_string())
        else:
            lines.append("No state counts available.")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_artefact(
    *,
    summary_path: Path,
    report_path: Path,
    root: Path,
) -> Path:
    artefact_dir = root / "artefacts" / "wp0_15_layerB_data"
    artefact_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(summary_path, artefact_dir / summary_path.name)
    shutil.copyfile(report_path, artefact_dir / report_path.name)

    manifest = build_manifest(
        run_id="wp0_15_layerB_data",
        wp="WP0.15",
        root=root,
        outputs=[summary_path.name, report_path.name],
        inputs=["Atlas of Living Australia"],
        require_clean=True,
        notes="Layer B occurrence acquisition + QC outputs",
    )
    write_manifest(artefact_dir / "MANIFEST.json", manifest)

    (artefact_dir / "README.txt").write_text(
        "WP0.15 Layer B data acquisition artefact. Contains QC report and summary table.\n",
        encoding="utf-8",
    )
    return artefact_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Layer B data acquisition + QC (WP0.15).")
    parser.add_argument("--email", default=os.getenv("ALA_DOWNLOAD_EMAIL"), help="ALA download email.")
    parser.add_argument(
        "--reason",
        default=os.getenv("ALA_DOWNLOAD_REASON"),
        help="ALA download reason text (resolved to reasonTypeId).",
    )
    parser.add_argument("--reason-id", default=os.getenv("ALA_DOWNLOAD_REASON_ID"), help="ALA reasonTypeId.")
    parser.add_argument("--years", nargs=2, type=int, default=list(DEFAULT_YEARS))
    parser.add_argument("--uncertainty-m", type=int, default=DEFAULT_UNCERTAINTY_M)
    parser.add_argument(
        "--groups",
        default="microbats,diurnal_birds,diurnal_reptiles",
        help="Comma-separated group keys to process.",
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw/ala_occurrences",
        help="Directory for raw downloads.",
    )
    parser.add_argument(
        "--processed-dir",
        default="data/processed/layerB",
        help="Directory for processed Layer B outputs.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip ALA downloads and only process existing files.",
    )
    parser.add_argument(
        "--skip-process",
        action="store_true",
        help="Skip processing/QC (download only).",
    )
    parser.add_argument(
        "--skip-artefact",
        action="store_true",
        help="Skip writing the canonical artefact folder.",
    )
    parser.add_argument(
        "--artefact-only",
        action="store_true",
        help="Only (re)write artefact/manifest from existing outputs.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow artefact generation with a dirty git tree.",
    )
    parser.add_argument(
        "--download-retries",
        type=int,
        default=3,
        help="Retry download attempts on server errors.",
    )
    parser.add_argument(
        "--use-all-downloads",
        action="store_true",
        help="Process all valid downloads for each group (default: latest only).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_repo_root()
    summary_path = root / LAYERB_OCCURRENCE_SUMMARY_CSV
    report_path = root / "analysis" / "reports" / "layerB_data_qc.md"

    if args.artefact_only:
        if not summary_path.exists() or not report_path.exists():
            raise SystemExit("Missing Layer B summary/QC report; run without --artefact-only.")
        if not args.skip_artefact:
            _ensure_clean_tree(root, args.allow_dirty)
            write_artefact(summary_path=summary_path, report_path=report_path, root=root)
        return 0

    raw_dir = root / args.raw_dir
    processed_dir = root / args.processed_dir

    year_start, year_end = args.years
    queries = build_queries(year_start, year_end, args.uncertainty_m)
    group_keys = {key.strip() for key in args.groups.split(",") if key.strip()}
    queries = [q for q in queries if q.key in group_keys]
    if not queries:
        raise SystemExit("No queries selected; check --groups.")

    download_results: list[DownloadResult] = []
    if not args.skip_download:
        if not args.email:
            raise SystemExit("ALA download requires --email (or ALA_DOWNLOAD_EMAIL).")
        reason_id = resolve_reason_id(args.reason, args.reason_id)
        for query in queries:
            count = fetch_count(query)
            result = download_occurrences(
                query=query,
                email=args.email,
                reason_id=reason_id,
                out_dir=raw_dir,
                fields=DEFAULT_FIELDS,
                retries=args.download_retries,
            )
            download_results.append(
                DownloadResult(
                    query=query,
                    path=result.path,
                    record_count=count,
                    response_status=result.response_status,
                    content_type=result.content_type,
                    downloaded_at=result.downloaded_at,
                )
            )
            meta = {
                "query": query.__dict__,
                "record_count": count,
                "download_path": str(result.path),
                "sha256": _sha256(result.path),
                "downloaded_at": result.downloaded_at,
                "response_status": result.response_status,
                "content_type": result.content_type,
            }
            meta_path = raw_dir / f"{_slug(query.key)}_metadata.json"
            meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    if args.skip_process:
        return 0

    summary_rows = []
    for query in queries:
        if download_results:
            raw_paths = [res.path for res in download_results if res.query.key == query.key]
        else:
            if args.use_all_downloads:
                raw_paths = find_valid_zips(raw_dir, query.key)
            else:
                latest = find_latest_zip(raw_dir, query.key)
                raw_paths = [latest] if latest else []
        if not raw_paths:
            raise SystemExit(f"Missing raw download for {query.key}. Run without --skip-download.")
        summary = process_occurrences(
            query=query,
            raw_paths=raw_paths,
            processed_dir=processed_dir,
            uncertainty_m=args.uncertainty_m,
        )
        summary_rows.append(summary)

    write_summary(summary_rows, summary_path)

    write_qc_report(summary_rows, report_path, queries, args.uncertainty_m)

    if not args.skip_artefact:
        _ensure_clean_tree(root, args.allow_dirty)
        write_artefact(summary_path=summary_path, report_path=report_path, root=root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

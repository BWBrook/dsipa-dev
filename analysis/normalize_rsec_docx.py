#!/usr/bin/env python3
"""Normalize RSEC DOCX page geometry and table layout after Makedoc builds."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from xml.sax.saxutils import quoteattr

import yaml


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{WORD_NS}}}"
DOCUMENT_XML = "word/document.xml"
A4_WIDTH_TWIPS = 11906
A4_HEIGHT_TWIPS = 16838
TABLE_LINE_TWIPS = 240


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--docx", help="Override the profile DOCX path (primarily for tests).")
    return parser.parse_args()


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _positive_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a positive number")
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{label} must be a positive number")
    return number


def _load_profile(config_path: Path, profile_name: str) -> dict[str, object]:
    try:
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read build config {config_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("build config root must be a mapping")
    profiles = payload.get("profiles")
    profile = profiles.get(profile_name) if isinstance(profiles, dict) else None
    if not isinstance(profile, dict):
        raise ValueError(f"profile not found in build config: {profile_name}")
    return profile


def _profile_paths_and_margins(
    config_path: Path,
    profile_name: str,
    docx_override: str | None,
) -> tuple[Path, Path, dict[str, int]]:
    profile = _load_profile(config_path, profile_name)
    margins = profile.get("margins")
    if not isinstance(margins, dict):
        raise ValueError(f"profile {profile_name} margins must be a mapping")
    if _nonempty_string(margins.get("unit"), "margins.unit").lower() != "cm":
        raise ValueError("RSEC DOCX normalization requires margins.unit=cm")
    if _nonempty_string(margins.get("paper_size"), "margins.paper_size").lower() != "a4":
        raise ValueError("RSEC DOCX normalization requires margins.paper_size=a4")

    margin_twips = {
        side: round(_positive_number(margins.get(side), f"margins.{side}") / 2.54 * 1440)
        for side in ("top", "right", "bottom", "left")
    }
    if docx_override:
        docx_path = Path(docx_override).expanduser().resolve()
    else:
        output_dir_raw = _nonempty_string(profile.get("output_dir"), "output_dir")
        output_stem = _nonempty_string(profile.get("output_stem"), "output_stem")
        output_dir = Path(output_dir_raw).expanduser()
        if not output_dir.is_absolute():
            output_dir = config_path.parent / output_dir
        docx_path = (output_dir / f"{output_stem}.docx").resolve()
    output_stem = _nonempty_string(profile.get("output_stem"), "output_stem")
    manifest_path = docx_path.with_name(f"{output_stem}_build_manifest.json")
    return docx_path, manifest_path, margin_twips


def _namespace_declarations(xml_bytes: bytes) -> list[tuple[str, str]]:
    declarations: list[tuple[str, str]] = []
    import io

    for _, item in ET.iterparse(io.BytesIO(xml_bytes), events=("start-ns",)):
        prefix, uri = item
        pair = (prefix or "", uri)
        if pair not in declarations:
            declarations.append(pair)
    return declarations


def _serialize_with_namespaces(root: ET.Element, declarations: list[tuple[str, str]]) -> bytes:
    for prefix, uri in declarations:
        if prefix not in {"xml", "xmlns"}:
            try:
                ET.register_namespace(prefix, uri)
            except ValueError:
                continue
    serialized = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    declaration_end = serialized.find(b"?>")
    root_start = serialized.find(b"<", declaration_end + 2)
    root_end = serialized.find(b">", root_start)
    if root_start < 0 or root_end < 0:
        raise ValueError("invalid serialized document XML")
    start = serialized[root_start:root_end]
    additions: list[bytes] = []
    for prefix, uri in declarations:
        attribute = "xmlns" if not prefix else f"xmlns:{prefix}"
        marker = f" {attribute}=".encode()
        if marker not in start:
            additions.append(f" {attribute}={quoteattr(uri)}".encode())
    if additions:
        serialized = (
            serialized[:root_start]
            + start
            + b"".join(additions)
            + serialized[root_end:]
        )
    return serialized


def normalize_document_xml(xml_bytes: bytes, margins: dict[str, int]) -> bytes:
    declarations = _namespace_declarations(xml_bytes)
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise ValueError(f"invalid {DOCUMENT_XML}: {exc}") from exc

    body = root.find(f"{W}body")
    if body is None:
        raise ValueError(f"{DOCUMENT_XML} contains no document body")
    body_children = list(body)
    transparent_markers = {f"{W}bookmarkStart", f"{W}bookmarkEnd"}
    for index, paragraph in enumerate(body_children[:-1]):
        if paragraph.tag != f"{W}p":
            continue
        following_index = index + 1
        while (
            following_index < len(body_children)
            and body_children[following_index].tag in transparent_markers
        ):
            following_index += 1
        if following_index >= len(body_children):
            continue
        following = body_children[following_index]
        if following.tag != f"{W}p":
            continue
        breaks = paragraph.findall(f".//{W}br")
        has_text = any((node.text or "").strip() for node in paragraph.findall(f".//{W}t"))
        has_image = any(
            node.tag.rsplit("}", 1)[-1] in {"drawing", "pict", "object"}
            for node in paragraph.iter()
        )
        if (
            len(breaks) != 1
            or breaks[0].get(f"{W}type") != "page"
            or has_text
            or has_image
        ):
            continue
        following_properties = following.find(f"{W}pPr")
        if following_properties is None:
            following_properties = ET.Element(f"{W}pPr")
            following.insert(0, following_properties)
        page_break_before = following_properties.find(f"{W}pageBreakBefore")
        if page_break_before is None:
            page_break_before = ET.SubElement(
                following_properties, f"{W}pageBreakBefore"
            )
        page_break_before.set(f"{W}val", "1")
        body.remove(paragraph)

    sections = root.findall(f".//{W}sectPr")
    if not sections:
        raise ValueError(f"{DOCUMENT_XML} contains no section properties")
    for section in sections:
        page_size = section.find(f"{W}pgSz")
        if page_size is None:
            page_size = ET.Element(f"{W}pgSz")
            section.insert(0, page_size)
        page_size.set(f"{W}w", str(A4_WIDTH_TWIPS))
        page_size.set(f"{W}h", str(A4_HEIGHT_TWIPS))
        page_size.attrib.pop(f"{W}orient", None)

        page_margins = section.find(f"{W}pgMar")
        if page_margins is None:
            page_margins = ET.Element(f"{W}pgMar")
            section.append(page_margins)
        for side, value in margins.items():
            page_margins.set(f"{W}{side}", str(value))

    for row in root.findall(f".//{W}tr"):
        properties = row.find(f"{W}trPr")
        if properties is None:
            properties = ET.Element(f"{W}trPr")
            row.insert(0, properties)
        cannot_split = properties.find(f"{W}cantSplit")
        if cannot_split is None:
            cannot_split = ET.SubElement(properties, f"{W}cantSplit")
        cannot_split.set(f"{W}val", "1")

    available_width = A4_WIDTH_TWIPS - margins["left"] - margins["right"]
    if available_width <= 0:
        raise ValueError("left and right margins leave no positive A4 text width")
    for table in root.findall(f".//{W}tbl"):
        grid_columns = table.findall(f"{W}tblGrid/{W}gridCol")
        widths = [int(column.get(f"{W}w", "0")) for column in grid_columns]
        grid_width = sum(widths)
        if not grid_columns or grid_width <= available_width:
            continue
        scale = available_width / grid_width
        scaled_widths = [max(1, round(width * scale)) for width in widths]
        scaled_widths[-1] += available_width - sum(scaled_widths)
        for column, width in zip(grid_columns, scaled_widths, strict=True):
            column.set(f"{W}w", str(width))
        for cell_width in table.findall(f".//{W}tcPr/{W}tcW"):
            if cell_width.get(f"{W}type", "dxa") != "dxa":
                continue
            raw_width = cell_width.get(f"{W}w")
            if raw_width is None:
                continue
            cell_width.set(f"{W}w", str(max(1, round(int(raw_width) * scale))))
        table_width = table.find(f"{W}tblPr/{W}tblW")
        if table_width is not None and table_width.get(f"{W}type") == "dxa":
            table_width.set(f"{W}w", str(available_width))

    for cell in root.findall(f".//{W}tc"):
        for paragraph in cell.findall(f".//{W}p"):
            properties = paragraph.find(f"{W}pPr")
            if properties is None:
                properties = ET.Element(f"{W}pPr")
                paragraph.insert(0, properties)
            spacing = properties.find(f"{W}spacing")
            if spacing is None:
                spacing = ET.SubElement(properties, f"{W}spacing")
            spacing.set(f"{W}line", str(TABLE_LINE_TWIPS))
            spacing.set(f"{W}lineRule", "auto")

    # Keep the long main Table 1 note on the same page as its compact table.
    for paragraph in body.findall(f"{W}p"):
        text = "".join(node.text or "" for node in paragraph.findall(f".//{W}t"))
        if not text.startswith("Zone-year summaries require at least 10 valid pixels"):
            continue
        properties = paragraph.find(f"{W}pPr")
        if properties is None:
            properties = ET.Element(f"{W}pPr")
            paragraph.insert(0, properties)
        spacing = properties.find(f"{W}spacing")
        if spacing is None:
            spacing = ET.SubElement(properties, f"{W}spacing")
        spacing.set(f"{W}line", "360")
        spacing.set(f"{W}lineRule", "auto")

    return _serialize_with_namespaces(root, declarations)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _refresh_manifest(manifest_path: Path, docx_path: Path, margins: dict[str, int]) -> None:
    if not manifest_path.exists():
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read build manifest {manifest_path}: {exc}") from exc
    outputs = manifest.get("outputs") if isinstance(manifest, dict) else None
    if not isinstance(outputs, list):
        raise ValueError(f"build manifest has no outputs list: {manifest_path}")
    matches = [
        record
        for record in outputs
        if isinstance(record, dict)
        and isinstance(record.get("path"), str)
        and Path(record["path"]).expanduser().resolve() == docx_path
    ]
    if len(matches) != 1:
        raise ValueError(f"build manifest must contain exactly one DOCX output: {manifest_path}")
    matches[0].update(
        exists=True,
        size_bytes=docx_path.stat().st_size,
        sha256=_sha256(docx_path),
    )
    manifest["docx_postprocessing"] = {
        "tool": "analysis/normalize_rsec_docx.py",
        "paper_size": "a4",
        "margins_twips": margins,
        "available_text_width_twips": A4_WIDTH_TWIPS - margins["left"] - margins["right"],
        "table_cell_line_spacing_twips": TABLE_LINE_TWIPS,
        "main_table_note_line_spacing_twips": 360,
        "prevent_table_row_splitting": True,
    }
    temporary = manifest_path.with_name(f".{manifest_path.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, manifest_path)
    finally:
        temporary.unlink(missing_ok=True)


def normalize_docx(docx_path: Path, manifest_path: Path, margins: dict[str, int]) -> None:
    if not docx_path.is_file():
        raise ValueError(f"DOCX build artifact is missing: {docx_path}")
    try:
        with zipfile.ZipFile(docx_path, "r") as archive:
            members = archive.infolist()
            payloads = {member.filename: archive.read(member.filename) for member in members}
    except (OSError, zipfile.BadZipFile, KeyError) as exc:
        raise ValueError(f"cannot read DOCX {docx_path}: {exc}") from exc
    if DOCUMENT_XML not in payloads:
        raise ValueError(f"DOCX lacks {DOCUMENT_XML}: {docx_path}")
    payloads[DOCUMENT_XML] = normalize_document_xml(payloads[DOCUMENT_XML], margins)

    fd, temporary_raw = tempfile.mkstemp(
        prefix=f".{docx_path.name}.", suffix=".tmp", dir=docx_path.parent
    )
    os.close(fd)
    temporary = Path(temporary_raw)
    try:
        with zipfile.ZipFile(temporary, "w") as archive:
            for member in members:
                archive.writestr(member, payloads[member.filename])
        os.replace(temporary, docx_path)
        _refresh_manifest(manifest_path, docx_path, margins)
    except (OSError, zipfile.BadZipFile) as exc:
        raise ValueError(f"cannot write normalized DOCX {docx_path}: {exc}") from exc
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    try:
        config_path = Path(args.config).expanduser().resolve()
        docx_path, manifest_path, margins = _profile_paths_and_margins(
            config_path, args.profile, args.docx
        )
        normalize_docx(docx_path, manifest_path, margins)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Normalized RSEC DOCX: {docx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

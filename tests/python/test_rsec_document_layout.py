import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from dsipa.paths import find_repo_root

REPO_ROOT = find_repo_root()
sys.path.insert(0, str(REPO_ROOT))
from analysis.render_rsec_pdf_layout import (
    LANDSCAPE_PACKAGE,
    TABLE_LAYOUT_LINES,
    _extend_layout,
)


NORMALIZER = REPO_ROOT / "analysis/normalize_rsec_docx.py"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{WORD_NS}}}"


def _write_config(path: Path, *, left: object = 2.5) -> None:
    path.write_text(
        f"""default_profile: submission
profiles:
  submission:
    output_dir: build
    output_stem: paper
    margins:
      unit: cm
      paper_size: a4
      top: 2.0
      right: 2.5
      bottom: 2.0
      left: {left}
""",
        encoding="utf-8",
    )


def _document_xml() -> bytes:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{WORD_NS}">
  <w:body>
    <w:p><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr><w:r><w:t>Body</w:t></w:r></w:p>
    <w:p><w:r><w:br w:type="page"/></w:r></w:p>
    <w:bookmarkStart w:id="1" w:name="following"/>
    <w:p><w:r><w:t>Following content</w:t></w:r></w:p>
    <w:p><w:r><w:t>Retained content</w:t><w:br w:type="page"/></w:r></w:p>
    <w:p><w:r><w:t>After retained break</w:t></w:r></w:p>
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
    <w:tbl>
      <w:tblPr><w:tblW w:type="dxa" w:w="9360"/></w:tblPr>
      <w:tblGrid><w:gridCol w:w="4680"/><w:gridCol w:w="4680"/></w:tblGrid>
      <w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="4680"/></w:tcPr><w:p><w:pPr><w:spacing w:line="480"/></w:pPr><w:r><w:t>Cell</w:t></w:r></w:p></w:tc></w:tr>
    </w:tbl>
    <w:tbl>
      <w:tblGrid><w:gridCol w:w="4000"/><w:gridCol w:w="4000"/></w:tblGrid>
      <w:tr><w:tc><w:p><w:r><w:t>Narrow table</w:t></w:r></w:p></w:tc></w:tr>
    </w:tbl>
    <w:sectPr><w:pgSz w:w="12240" w:h="15840" w:orient="landscape"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
  </w:body>
</w:document>
'''.encode()


def _write_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", _document_xml())
        archive.writestr("marker.txt", b"preserved")


def _run(config: Path, docx: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(NORMALIZER),
            "--config",
            str(config),
            "--profile",
            "submission",
            "--docx",
            str(docx),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_pdf_extension_compacts_longtables_without_changing_body_spacing() -> None:
    upstream = "% upstream layout\n\\linespread{2}\n\\selectfont\n"

    submission = _extend_layout(upstream, "submission")
    supplementary = _extend_layout(upstream, "supplementary")

    assert submission.startswith(upstream)
    assert submission.count("\\linespread{2}") == 1
    assert submission.count("\\AtBeginEnvironment{longtable}{\\singlespacing}") == 1
    assert LANDSCAPE_PACKAGE not in submission
    assert LANDSCAPE_PACKAGE in supplementary
    assert _extend_layout(submission, "submission") == submission
    for line in TABLE_LAYOUT_LINES:
        assert supplementary.count(line) == 1


def test_docx_normalizer_applies_a4_margins_only_to_sections_and_tables(
    tmp_path: Path,
) -> None:
    config = tmp_path / "build.yaml"
    docx = tmp_path / "paper.docx"
    manifest = tmp_path / "paper_build_manifest.json"
    _write_config(config)
    _write_docx(docx)
    manifest.write_text(
        json.dumps(
            {
                "outputs": [
                    {
                        "path": str(docx),
                        "exists": True,
                        "size_bytes": 1,
                        "sha256": "stale",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = _run(config, docx)

    assert result.returncode == 0, result.stderr
    with zipfile.ZipFile(docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        assert archive.read("marker.txt") == b"preserved"
    sections = root.findall(f".//{W}sectPr")
    assert len(sections) == 2
    for section in sections:
        page_size = section.find(f"{W}pgSz")
        assert page_size is not None
        assert page_size.get(f"{W}w") == "11906"
        assert page_size.get(f"{W}h") == "16838"
        assert page_size.get(f"{W}orient") is None
        margins = section.find(f"{W}pgMar")
        assert margins is not None
        assert {side: margins.get(f"{W}{side}") for side in ("top", "right", "bottom", "left")} == {
            "top": "1134",
            "right": "1417",
            "bottom": "1134",
            "left": "1417",
        }

    body_paragraph = root.find(f"./{W}body/{W}p")
    assert body_paragraph is not None
    assert body_paragraph.find(f"{W}pPr/{W}spacing").get(f"{W}line") == "480"
    body_paragraphs = root.findall(f"./{W}body/{W}p")
    paragraph_by_text = {
        "".join(node.text or "" for node in paragraph.findall(f".//{W}t")): paragraph
        for paragraph in body_paragraphs
    }
    following = paragraph_by_text["Following content"]
    assert following.find(f"{W}pPr/{W}pageBreakBefore").get(f"{W}val") == "1"
    assert "".join(node.text or "" for node in following.findall(f".//{W}t")) == "Following content"
    retained = paragraph_by_text["Retained content"]
    retained_breaks = retained.findall(f".//{W}br")
    assert len(retained_breaks) == 1
    assert retained_breaks[0].get(f"{W}type") == "page"
    assert paragraph_by_text["After retained break"].find(
        f"{W}pPr/{W}pageBreakBefore"
    ) is None
    assert not any(
        not any((node.text or "").strip() for node in paragraph.findall(f".//{W}t"))
        and len(paragraph.findall(f".//{W}br")) == 1
        and paragraph.findall(f".//{W}br")[0].get(f"{W}type") == "page"
        for paragraph in body_paragraphs
    )
    cell_spacing = root.find(f".//{W}tc/{W}p/{W}pPr/{W}spacing")
    assert cell_spacing is not None
    assert cell_spacing.get(f"{W}line") == "240"
    assert cell_spacing.get(f"{W}lineRule") == "auto"
    cannot_split = root.find(f".//{W}tr/{W}trPr/{W}cantSplit")
    assert cannot_split is not None
    assert cannot_split.get(f"{W}val") == "1"
    tables = root.findall(f".//{W}tbl")
    grid_widths = [
        int(column.get(f"{W}w"))
        for column in tables[0].findall(f"{W}tblGrid/{W}gridCol")
    ]
    narrow_grid_widths = [
        int(column.get(f"{W}w"))
        for column in tables[1].findall(f"{W}tblGrid/{W}gridCol")
    ]
    assert grid_widths == [4536, 4536]
    assert sum(grid_widths) == 9072
    assert narrow_grid_widths == [4000, 4000]
    table_width = root.find(f".//{W}tblPr/{W}tblW")
    assert table_width is not None
    assert table_width.get(f"{W}w") == "9072"
    cell_width = root.find(f".//{W}tcPr/{W}tcW")
    assert cell_width is not None
    assert cell_width.get(f"{W}w") == "4536"

    refreshed = json.loads(manifest.read_text(encoding="utf-8"))
    output = refreshed["outputs"][0]
    assert output["size_bytes"] == docx.stat().st_size
    assert output["sha256"] == hashlib.sha256(docx.read_bytes()).hexdigest()
    assert refreshed["docx_postprocessing"]["table_cell_line_spacing_twips"] == 240
    assert refreshed["docx_postprocessing"]["available_text_width_twips"] == 9072


def test_docx_normalizer_fails_before_writing_for_invalid_margin_config(
    tmp_path: Path,
) -> None:
    config = tmp_path / "build.yaml"
    docx = tmp_path / "paper.docx"
    _write_config(config, left='"2.5"')
    _write_docx(docx)
    before = docx.read_bytes()

    result = _run(config, docx)

    assert result.returncode == 1
    assert "margins.left must be a positive number" in result.stderr
    assert docx.read_bytes() == before

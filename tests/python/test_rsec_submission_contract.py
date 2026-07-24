import os
import subprocess
import sys
from pathlib import Path

import yaml

from dsipa.paths import find_repo_root


REPO_ROOT = find_repo_root()
BUILD_CONFIG = REPO_ROOT / "settings/build.yaml"
LAYOUT_RENDERER = REPO_ROOT / "analysis/render_rsec_pdf_layout.py"
SUBMISSION_AUTHORS = (
    REPO_ROOT / "manuscript/submission/rsec/submission_authors.yaml"
)
SUPPLEMENTARY_TABLES = REPO_ROOT / "manuscript/text/supplementary_tables.md"
MAIN_TABLES = REPO_ROOT / "manuscript/text/tables.md"
SUPPLEMENTARY_FIGURES = REPO_ROOT / "manuscript/text/supplementary_figures.md"


def _config() -> dict[str, object]:
    return yaml.safe_load(BUILD_CONFIG.read_text(encoding="utf-8"))


def _fake_renderer(path: Path) -> None:
    path.write_text(
        """#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--config")
parser.add_argument("--profile", default="")
parser.add_argument("--output", required=True)
args = parser.parse_args()
status = int(os.environ.get("FAKE_RENDER_STATUS", "0"))
if status:
    raise SystemExit(status)
Path(args.output).write_text(
    os.environ.get("FAKE_LAYOUT_CONTENT", "% upstream layout\\n"),
    encoding="utf-8",
)
""",
        encoding="utf-8",
    )


def _run_layout(
    upstream: Path,
    output: Path,
    *,
    profile: str,
    content: str = "% upstream layout\n",
    status: int = 0,
) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "DSIPA_MAKEDOC_UPSTREAM_LAYOUT_RENDER": str(upstream),
        "FAKE_LAYOUT_CONTENT": content,
        "FAKE_RENDER_STATUS": str(status),
    }
    return subprocess.run(
        [
            sys.executable,
            str(LAYOUT_RENDERER),
            "--config",
            str(BUILD_CONFIG),
            "--profile",
            profile,
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_submission_uses_visible_placeholder_authors_without_changing_draft() -> None:
    profiles = _config()["profiles"]
    assert profiles["draft"]["author_metadata"] == "../manuscript/authors.yaml"
    assert (
        profiles["submission"]["author_metadata"]
        == "../manuscript/submission/rsec/submission_authors.yaml"
    )

    placeholder_text = SUBMISSION_AUTHORS.read_text(encoding="utf-8")
    assert "Barry W. Brook" not in placeholder_text
    assert "University of Tasmania" not in placeholder_text
    for required in (
        "author names and order",
        "affiliations",
        "corresponding author",
        "full address",
        "contact details",
    ):
        assert required in placeholder_text
    assert placeholder_text.count("[BARRY CONFIRM:") >= 4


def test_supplementary_profile_closes_landscape_before_figures() -> None:
    supplementary = _config()["profiles"]["supplementary"]
    assert supplementary["manuscript_sources"] == [
        "../manuscript/submission/rsec/supplementary_frontmatter.md",
        "../manuscript/text/supplementary_tables.md",
        "../manuscript/submission/rsec/supplementary_table_end.md",
        "../manuscript/text/supplementary_figures.md",
    ]


def test_supplementary_table_delimiters_encode_reviewed_column_widths() -> None:
    lines = SUPPLEMENTARY_TABLES.read_text(encoding="utf-8").splitlines()
    delimiter_lines = [
        line
        for line in lines
        if line.startswith("| ") and set(line.replace("|", "").replace(" ", "")) <= {"-", ":"}
    ]
    assert delimiter_lines == [
        "| ---------- | ------ | ------------- | ------------- | ---- | ---- | "
        "------- | ------- | -------- | -------- | ---------- | ---------- |",
        "| ------------ | ----------------- | ----: | ----: | -----: | -----: | "
        "-----: | -----: | ------: | ------: | ---: | ----: | -------------- |",
    ]


def test_main_table_delimiter_encodes_shared_pdf_docx_widths() -> None:
    lines = MAIN_TABLES.read_text(encoding="utf-8").splitlines()
    delimiter_lines = [
        line
        for line in lines
        if line.startswith("| ")
        and set(line.replace("|", "").replace(" ", "")) <= {"-", ":"}
    ]
    assert delimiter_lines == [
        "| ---------------------- | ----------: | ----------------: | -----------: | "
        "----------------------- | ------------------ |"
    ]


def test_supplementary_figures_use_reviewed_label_safe_width() -> None:
    figure_lines = [
        line
        for line in SUPPLEMENTARY_FIGURES.read_text(encoding="utf-8").splitlines()
        if line.startswith("![")
    ]
    assert len(figure_lines) == 7
    assert [line.rsplit("width=", 1)[1] for line in figure_lines] == [
        "85%}",
        "85%}",
        "85%}",
        "85%}",
        "85%}",
        "80%}",
        "85%}",
    ]


def test_layout_renderer_is_deterministic_and_adds_package_once(
    tmp_path: Path,
) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "layout.tex"
    _fake_renderer(upstream)

    first = _run_layout(upstream, output, profile="supplementary")
    assert first.returncode == 0, first.stderr
    first_bytes = output.read_bytes()
    second = _run_layout(upstream, output, profile="supplementary")

    assert second.returncode == 0, second.stderr
    assert output.read_bytes() == first_bytes
    assert output.read_text(encoding="utf-8").count("\\usepackage{pdflscape}") == 1

    existing = "% upstream layout\n\\usepackage{pdflscape}\n"
    result = _run_layout(
        upstream,
        output,
        profile="supplementary",
        content=existing,
    )
    assert result.returncode == 0, result.stderr
    assert output.read_text(encoding="utf-8") == existing


def test_layout_renderer_is_noop_for_other_profiles(tmp_path: Path) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "layout.tex"
    content = "% exact upstream draft layout\n"
    _fake_renderer(upstream)

    result = _run_layout(upstream, output, profile="draft", content=content)

    assert result.returncode == 0, result.stderr
    assert output.read_text(encoding="utf-8") == content


def test_layout_renderer_propagates_failure_without_replacing_output(
    tmp_path: Path,
) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "layout.tex"
    _fake_renderer(upstream)
    output.write_text("existing output\n", encoding="utf-8")

    result = _run_layout(upstream, output, profile="supplementary", status=37)

    assert result.returncode == 37
    assert output.read_text(encoding="utf-8") == "existing output\n"

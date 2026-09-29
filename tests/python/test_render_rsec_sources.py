import os
import subprocess
import sys
from pathlib import Path

from dsipa.paths import find_repo_root


REPO_ROOT = find_repo_root()
SOURCE_RENDERER = REPO_ROOT / "analysis/render_rsec_sources.py"


def _fake_upstream(path: Path, *, omit_symbol: str = "") -> None:
    definitions = {
        "main": '''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--profile", default="")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    status = int(os.environ.get("FAKE_RENDER_STATUS", "0"))
    if status:
        return status
    figures = [
        FigureBlock("First caption", "first.png", "#fig-example-s1 width=80%"),
        FigureBlock("Second caption", "second.png", "#fig-example-s2 width=75%"),
    ]
    rendered = build_figure_blocks(figures, "top", "pages")
    Path(args.output).write_text(rendered, encoding="utf-8")
    return 0
''',
        "build_figure_blocks": '''
def build_figure_blocks(figures, caption_position, placement):
    return "UPSTREAM FIGURE OUTPUT\\n"
''',
        "_ordered_main_and_supplementary_figures": '''
def _ordered_main_and_supplementary_figures(figures):
    return [], [(f"Fig. S{index}", figure) for index, figure in enumerate(figures, 1)]
''',
        "_page_break_block": '''
def _page_break_block():
    return "<PAGEBREAK>"
''',
        "_title_line": '''
def _title_line(label, figure):
    return f"**{label}.** {figure.title}"
''',
        "_image_without_caption_text": '''
def _image_without_caption_text(figure):
    return f"![]({figure.src}){{{figure.attrs}}}"
''',
    }
    body = '''#!/usr/bin/env python3
import argparse
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class FigureBlock:
    title: str
    src: str
    attrs: str

'''
    body += "\n".join(
        definition for name, definition in definitions.items() if name != omit_symbol
    )
    path.write_text(body, encoding="utf-8")


def _run_renderer(
    upstream: Path,
    output: Path,
    *,
    profile: str = "supplementary",
    status: int = 0,
) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "DSIPA_MAKEDOC_UPSTREAM_SOURCE_RENDER": str(upstream),
        "FAKE_RENDER_STATUS": str(status),
    }
    return subprocess.run(
        [
            sys.executable,
            str(SOURCE_RENDERER),
            "--config",
            "unused.yaml",
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


def test_supplementary_pages_have_complete_labels_and_captionless_images(
    tmp_path: Path,
) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "prepared.md"
    _fake_upstream(upstream)

    result = _run_renderer(upstream, output)

    assert result.returncode == 0, result.stderr
    rendered = output.read_text(encoding="utf-8")
    assert rendered.count("<PAGEBREAK>") == 2
    assert rendered.count("**Fig. S1.** First caption") == 1
    assert rendered.count("**Fig. S2.** Second caption") == 1
    assert "![](first.png){#fig-example-s1 width=80%}" in rendered
    assert "![](second.png){#fig-example-s2 width=75%}" in rendered
    assert "![First caption]" not in rendered
    assert "![Second caption]" not in rendered
    assert "## Supplementary Information" not in rendered
    assert "UPSTREAM FIGURE OUTPUT" not in rendered


def test_non_supplementary_profile_delegates_without_patch(tmp_path: Path) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "prepared.md"
    _fake_upstream(upstream)

    result = _run_renderer(upstream, output, profile="submission")

    assert result.returncode == 0, result.stderr
    assert output.read_text(encoding="utf-8") == "UPSTREAM FIGURE OUTPUT\n"


def test_upstream_failure_status_propagates(tmp_path: Path) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "prepared.md"
    _fake_upstream(upstream)

    result = _run_renderer(upstream, output, status=37)

    assert result.returncode == 37
    assert not output.exists()


def test_missing_upstream_contract_symbol_fails_closed(tmp_path: Path) -> None:
    upstream = tmp_path / "upstream.py"
    output = tmp_path / "prepared.md"
    _fake_upstream(upstream, omit_symbol="_title_line")

    result = _run_renderer(upstream, output)

    assert result.returncode == 1
    assert "lacks required callables: _title_line" in result.stderr
    assert not output.exists()

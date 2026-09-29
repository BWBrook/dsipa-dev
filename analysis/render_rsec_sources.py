#!/usr/bin/env python3
"""Adapt Makedoc source rendering for RSEC Supporting Information figures."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable


UPSTREAM_ENV = "DSIPA_MAKEDOC_UPSTREAM_SOURCE_RENDER"
SUPPLEMENTARY_PROFILE = "supplementary"
_REQUIRED_CALLABLES = (
    "main",
    "build_figure_blocks",
    "_ordered_main_and_supplementary_figures",
    "_page_break_block",
    "_title_line",
    "_image_without_caption_text",
)


def _requested_profile(argv: list[str]) -> str:
    for index, argument in enumerate(argv):
        if argument == "--profile":
            if index + 1 >= len(argv):
                return ""
            return argv[index + 1].strip()
        if argument.startswith("--profile="):
            return argument.split("=", 1)[1].strip()
    return ""


def _load_upstream(path: Path) -> ModuleType:
    module_name = "_dsipa_makedoc_prepare_markdown_sources"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load upstream source renderer: {path}")

    sys.path.insert(0, str(path.parent))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    finally:
        sys.path.pop(0)
    return module


def _require_upstream_contract(module: ModuleType) -> None:
    missing = [
        name for name in _REQUIRED_CALLABLES if not callable(getattr(module, name, None))
    ]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"upstream source renderer lacks required callables: {joined}")


def _supplementary_page_builder(module: ModuleType) -> Callable[..., str]:
    def build_figure_blocks(
        figures: list[object],
        caption_position: str,
        placement: str,
    ) -> str:
        del caption_position
        if not figures:
            return ""
        if placement != "pages":
            raise ValueError(
                "RSEC supplementary source rendering requires figures.placement=pages"
            )

        main_figures, supplementary_figures = (
            module._ordered_main_and_supplementary_figures(figures)
        )
        if main_figures:
            raise ValueError(
                "RSEC supplementary source rendering received a non-supplementary figure"
            )

        blocks = [
            (
                f"{module._page_break_block()}\n\n"
                f"{module._title_line(label, figure)}\n\n"
                f"{module._image_without_caption_text(figure)}"
            )
            for label, figure in supplementary_figures
        ]
        return "\n\n".join(blocks) + ("\n" if blocks else "")

    return build_figure_blocks


def main() -> int:
    upstream_raw = os.environ.get(UPSTREAM_ENV, "").strip()
    upstream_path = Path(upstream_raw) if upstream_raw else None
    if upstream_path is None or not upstream_path.is_file():
        print(f"Error: {UPSTREAM_ENV} must name the upstream source renderer.", file=sys.stderr)
        return 1

    try:
        upstream = _load_upstream(upstream_path)
        _require_upstream_contract(upstream)
        if _requested_profile(sys.argv[1:]) == SUPPLEMENTARY_PROFILE:
            upstream.build_figure_blocks = _supplementary_page_builder(upstream)
        return int(upstream.main())
    except (ImportError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path

from dsipa.layerB_gonogo import load_config, render_report, write_artefact, write_report
from dsipa.paths import find_repo_root


def test_layerB_gonogo_config_loads() -> None:
    root = find_repo_root()
    config = load_config(root / "docs" / "layerB_gonogo.json")
    assert config["status"] in {"go", "conditional-go", "no-go"}


def test_layerB_gonogo_report_renders(tmp_path: Path) -> None:
    root = find_repo_root()
    config = load_config(root / "docs" / "layerB_gonogo.json")
    content = render_report(config)
    assert "Go/no-go criteria" in content

    report_path = tmp_path / "layerB_gonogo.md"
    write_report(report_path, content)
    assert report_path.exists()


def test_layerB_gonogo_artefact(tmp_path: Path) -> None:
    root = find_repo_root()
    config_text = (root / "docs" / "layerB_gonogo.json").read_text(encoding="utf-8")

    config_path = tmp_path / "layerB_gonogo.json"
    config_path.write_text(config_text, encoding="utf-8")

    report_path = tmp_path / "layerB_gonogo.md"
    report_path.write_text("# Test report", encoding="utf-8")

    artefact_dir = write_artefact(report_path, config_path, tmp_path)
    assert (artefact_dir / "MANIFEST.json").exists()
    assert (artefact_dir / "README.txt").exists()
    assert (artefact_dir / report_path.name).exists()
    assert (artefact_dir / config_path.name).exists()

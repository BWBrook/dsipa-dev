from pathlib import Path

from dsipa.paths import find_repo_root
from dsipa.run import run


def test_run_creates_placeholder_and_manifest(tmp_path: Path):
    run_dir = run(
        run_id="test-run",
        work_package="WP0.1",
        out_dir=tmp_path,
        root=find_repo_root(),
    )

    assert (run_dir / "placeholder.txt").exists()
    assert (run_dir / "MANIFEST.json").exists()
    assert (run_dir / "README.txt").exists()

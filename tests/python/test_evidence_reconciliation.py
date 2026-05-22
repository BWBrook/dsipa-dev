from pathlib import Path

from dsipa.evidence_reconciliation import (
    ExpectedFile,
    build_inventory,
    render_inventory_markdown,
    render_reproducibility_audit,
)


def test_inventory_detects_present_verified_and_missing_files(tmp_path: Path):
    present = tmp_path / "present.txt"
    present.write_text("evidence\n", encoding="utf-8")

    inventory = build_inventory(
        tmp_path,
        expected_files=[
            ExpectedFile(
                "present.txt",
                "unit",
                expected_sha256="bdcf4c994585af6dd6cb1cfbff78bcc73ab27dc30a299db5bb83766ca05b5de4",
            ),
            ExpectedFile("missing.txt", "unit"),
        ],
    )

    assert inventory["summary"]["expected_files"] == 2
    assert inventory["summary"]["present_files"] == 1
    assert inventory["summary"]["verified_files"] == 1
    assert inventory["summary"]["missing_required"] == 1
    assert inventory["files"][0]["status"] == "verified"
    assert inventory["files"][1]["status"] == "missing"


def test_inventory_markdown_names_required_attention(tmp_path: Path):
    inventory = build_inventory(
        tmp_path,
        expected_files=[ExpectedFile("missing.txt", "unit")],
    )

    markdown = render_inventory_markdown(inventory)

    assert "# Evidence reconciliation" in markdown
    assert "Missing: `missing.txt`" in markdown


def test_reproducibility_audit_keeps_runtime_and_checksum_sections(tmp_path: Path):
    present = tmp_path / "present.txt"
    present.write_text("evidence\n", encoding="utf-8")
    inventory = build_inventory(
        tmp_path,
        expected_files=[
            ExpectedFile(
                "present.txt",
                "unit",
                expected_sha256="bdcf4c994585af6dd6cb1cfbff78bcc73ab27dc30a299db5bb83766ca05b5de4",
            )
        ],
    )

    audit = render_reproducibility_audit(inventory)

    assert "## Expected runtime class" in audit
    assert "## Verification checklist" in audit
    assert "`present.txt`: `bdcf4c994585af6dd6cb1cfbff78bcc73ab27dc30a299db5bb83766ca05b5de4`" in audit


def test_inventory_can_normalize_crlf_for_text_hashes(tmp_path: Path):
    ledger = tmp_path / "ledger.csv"
    ledger.write_bytes(b"a,b\r\n1,2\r\n")
    inventory = build_inventory(
        tmp_path,
        expected_files=[
            ExpectedFile(
                "ledger.csv",
                "unit",
                expected_sha256="492d5ea496056f1a6a6592241032fab764c321596317930b4fa0e1e8bc3b7470",
                note="normalised text",
                normalize_crlf=True,
            )
        ],
    )

    assert inventory["files"][0]["status"] == "verified"
    assert "normalised text" in render_inventory_markdown(inventory)

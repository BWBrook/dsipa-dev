from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from analysis.render_coauthor_figures import (
    _primary_trends,
    _write_render_manifest,
    _zero_slope_breakdown,
    parse_layerb_report,
    plot_trend_distribution,
)


def test_layerb_report_parser_reads_fold_sd_and_auc() -> None:
    report = Path("analysis/reports/layerB_modelling_report.md")
    rows = parse_layerb_report(report)

    assert [row["label"] for row in rows] == [
        "Provider-matched association",
        "Block-shuffle benchmark",
        "IBRA × year shuffle benchmark",
        "Multi-provider sensitivity",
    ]
    assert rows[0]["coefficients"]["any_light"] == (1.315818, 0.127743)
    assert rows[0]["auc"] == 0.544657


def test_trend_distribution_renders_all_sign_counts(tmp_path: Path) -> None:
    trends = pd.DataFrame({"slope_inside": [-4.0, -0.5, 0.0, 0.0, 1.0, 8.0]})
    output = plot_trend_distribution(trends, tmp_path / "trend.png")

    assert output.exists()
    assert output.stat().st_size > 0


def test_primary_trend_distribution_keeps_rows_with_missing_buffer(tmp_path: Path) -> None:
    path = tmp_path / "trends.csv"
    pd.DataFrame(
        {
            "pa_id": ["a", "b"],
            "metric": ["mean", "mean"],
            "buffer_type": ["land_unprotected", "land_unprotected"],
            "slope_inside": [0.0, 1.0],
            "slope_buffer_1km": [float("nan"), 2.0],
            "n_years_inside": [12, 12],
        }
    ).to_csv(path, index=False)
    assert len(_primary_trends(path)) == 2


def test_zero_series_late_positive_requires_complete_years(tmp_path: Path) -> None:
    rows = []
    series = {
        "all_zero": [0] * 12,
        "constant": [2] * 12,
        "late_positive": [0] * 9 + [0, 1, 0],
        "incomplete": [0] * 11,
    }
    for pa_id, values in series.items():
        years = range(2013, 2025) if pa_id != "incomplete" else [*range(2013, 2020), *range(2021, 2025)]
        rows.extend(
            {
                "pa_id": pa_id,
                "zone": "inside",
                "valid_pixel_count": 10,
                "year": year,
                "mean": value,
            }
            for year, value in zip(years, values)
        )
    path = tmp_path / "series.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    trends = pd.DataFrame({"pa_id": list(series), "slope_inside": [0.0] * 4})

    counts, late_positive = _zero_slope_breakdown(trends, path)

    assert counts == {"All annual values zero": 1, "Constant non-zero": 1, "Varying": 1}
    assert late_positive == 1


def test_render_manifest_records_hashes_and_render_only_flag(tmp_path: Path) -> None:
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "figure.png"
    input_path.write_text("accepted\n", encoding="utf-8")
    output_path.write_bytes(b"PNG placeholder")

    manifest_path = _write_render_manifest(
        tmp_path,
        inputs={"input": input_path},
        outputs={"figure": output_path},
    )

    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["analysis"] == {
        "models_refit": False,
        "note": "Figures rendered from accepted processed outputs and tracked report values.",
        "render_only": True,
        "trends_refit": False,
    }
    assert manifest["inputs"]["input"]["sha256"]
    assert manifest["outputs"]["figure"]["sha256"]
    assert set(manifest["packages"]) == {
        "numpy", "pandas", "geopandas", "matplotlib", "shapely", "rasterio", "scipy"
    }

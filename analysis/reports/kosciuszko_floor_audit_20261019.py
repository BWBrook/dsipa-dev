"""Offline, independent replay of the R3 review's high-value pixel claim.

Run from the repository root with:
    uv run python analysis/reports/kosciuszko_floor_audit_20261019.py

Only the adjacent JSON and Markdown receipts are written. No raster download,
existing audit import, scientific input edit, or manuscript edit is performed.
The illustrative mask counterexample is a logical test, not an EOG simulation.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
from zoneinfo import ZoneInfo

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).resolve()
CACHE = ROOT / "analysis/reports/kosciuszko_case_20261018.npz"
LOCAL_REFERENCES = [
    ROOT / "analysis/audit_kosciuszko_case.py",
    ROOT / "analysis/reports/editorial_claude_r3_review_20261019.md",
    ROOT / "analysis/reports/product_floor_followup.md",
    ROOT / "analysis/reports/product_lineage_review.md",
]
SOURCES = [
    {
        "title": "EOG Annual VNL V2 methodology and band definitions",
        "url": "https://eogdata.mines.edu/products/vnl/",
        "access_date": "2026-10-19",
        "evidence": "Background masking uses 3x3 data range and coverage-dependent thresholds; average-masked is the average with background masked. The documented original V2 method sets a per-cell multiyear threshold, not an unconstrained new threshold every year.",
    },
    {
        "title": "Elvidge et al. (2021), Annual Time Series of Global VIIRS Nighttime Lights Derived from Monthly Averages: 2012 to 2019",
        "url": "https://doi.org/10.3390/rs13050922",
        "access_date": "2026-10-19",
        "evidence": "Publisher-indexed abstract and methods describe median-based outlier removal, a spatial data-range mask, and filling retained lit cells with average radiance. Direct publisher retrieval returned HTTP 429; the indexed publisher text was available.",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def array_digest(value: np.ndarray) -> str:
    """Use the cache's documented shape/dtype/bytes digest convention."""
    value = np.array(value, copy=True, order="C")
    if np.issubdtype(value.dtype, np.floating):
        value[np.isnan(value)] = np.nan
    header = json.dumps({"shape": value.shape, "dtype": value.dtype.str}, sort_keys=True)
    return hashlib.sha256(header.encode() + b"\n" + value.tobytes()).hexdigest()


def main() -> None:
    with np.load(CACHE, allow_pickle=False) as archive:
        arrays = {key: archive[key] for key in archive.files}
    provenance = json.loads(str(arrays["provenance"]))
    checked_arrays = {}
    for key, expected in provenance["array_sha256"].items():
        observed = array_digest(arrays[key])
        assert observed == expected, (key, observed, expected)
        checked_arrays[key] = observed

    inside = arrays["inside"]
    before_grid, after_grid = arrays["radiance_2019"], arrays["radiance_2024"]
    common = inside & arrays["valid_2019"] & arrays["valid_2024"]
    assert before_grid.shape == after_grid.shape == inside.shape
    before, after = before_grid[common], after_grid[common]
    assert np.isfinite(before).all() and np.isfinite(after).all()
    assert np.all(before >= 0) and np.all(after >= 0)
    delta = after - before
    brightened = delta > 0
    positive_sum = float(delta[brightened].sum())
    negative_sum = float(delta[delta < 0].sum())

    rows = []
    for threshold in (10, 50, 100, 200):
        selected = brightened & (after >= threshold)
        contribution = float(delta[selected].sum())
        rows.append({
            "minimum_2024_value": threshold,
            "cells": int(selected.sum()),
            "positive_change_sum": contribution,
            "share_of_all_positive_change": contribution / positive_sum,
            "percent_of_all_positive_change": 100 * contribution / positive_sum,
            "recorded_zero_in_2019_cells": int((selected & (before == 0)).sum()),
            "maximum_2019_value": float(before[selected].max()),
        })

    # Acceptance criteria reproduce the review's arithmetic without importing it.
    assert int(common.sum()) == 39721
    assert int(brightened.sum()) == 642
    assert positive_sum == 26110 and negative_sum == -360
    assert [row["cells"] for row in rows] == [642, 102, 64, 37]
    assert [row["positive_change_sum"] for row in rows] == [26110, 19530, 16910, 13300]
    assert float(before.max()) == 40 and float(after.max()) == 610
    assert float(np.median(after[brightened])) == 10
    assert float(after.sum() - before.sum()) == positive_sum + negative_sum
    assert int(common.sum()) == int(inside.sum())

    annual_replay = {}
    for year, values in ((2019, before), (2024, after)):
        index = np.flatnonzero(arrays["annual_year"] == year).item()
        accepted_sum = float(arrays["annual_mean"][index] * arrays["annual_valid_count"][index])
        assert int(arrays["annual_valid_count"][index]) == len(values)
        assert abs(accepted_sum - float(values.sum())) < 1e-8
        annual_replay[str(year)] = {
            "cached_cell_sum": float(values.sum()),
            "accepted_mean_times_count": accepted_sum,
            "difference": float(values.sum()) - accepted_sum,
        }

    # Two hypothetical cells: high-valued target and stable 10-unit reference.
    # Q(A) is already encoded; D and T are arbitrary mask-statistic units.
    # This is a counterexample to an alleged mathematical impossibility only.
    unmasked_encoded = np.array([610.0, 10.0])
    mask_statistic = np.array([1.0, 3.0])
    thresholds = (2.0, 0.5)
    toy_before = unmasked_encoded * (mask_statistic >= thresholds[0])
    toy_after = unmasked_encoded * (mask_statistic >= thresholds[1])
    assert toy_before.tolist() == [0, 10]
    assert toy_after.tolist() == [610, 10]
    assert toy_before[toy_before > 0].min() == toy_after[toy_after > 0].min() == 10
    assert np.array_equal(toy_before % 10, np.zeros(2))
    assert np.array_equal(toy_after % 10, np.zeros(2))

    wording = (
        "The documented 2022 source change cannot by itself explain the rise already visible in 2021. "
        "The endpoint increase also extends well above the smallest positive encoded value: "
        "64 of the 642 cells that brightened between 2019 and 2024 reached at least 100 product units, "
        "contributing 64.8% of summed positive pixel differences; the 2024 maximum within the park was 610. "
        "This establishes that the increase is not confined to the ten-unit output floor, "
        "but does not exclude masking or other processing effects."
    )
    completed = datetime.now(timezone.utc)
    report = {
        "schema_version": "1.0",
        "completed_utc": completed.isoformat(),
        "completed_hobart": completed.astimezone(ZoneInfo("Australia/Hobart")).isoformat(),
        "purpose": "Independent offline arithmetic and inference audit of consequential claim 1 in the Claude R3 review",
        "verdict": "Numerical table reproduced; categorical exclusion of masking is unsupported",
        "provenance": {
            "git_commit_at_execution": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "script": {"path": str(SCRIPT.relative_to(ROOT)), "sha256": sha256(SCRIPT)},
            "cache": {"path": str(CACHE.relative_to(ROOT)), "sha256": sha256(CACHE), "bytes": CACHE.stat().st_size},
            "reviewed_local_reference_hashes": {str(p.relative_to(ROOT)): sha256(p) for p in LOCAL_REFERENCES},
            "verified_cached_array_hashes": checked_arrays,
            "cached_source_rasters": provenance["sources"],
            "cached_upstream_local_input_hashes": provenance["local_inputs"],
            "software": {"python": platform.python_version(), "numpy": np.__version__},
            "mode": "Offline numeric replay; primary methodology documentation consulted separately",
        },
        "definitions": {
            "support": "Raster-centre-selected inside cells valid in both cached 2019 and 2024 arrays; zeros are valid recorded non-detections",
            "delta": "decoded_2024 - decoded_2019",
            "brightened": "delta > 0",
            "threshold": "2024 decoded value >= listed threshold, restricted to brightened cells; thresholds are nested",
            "share_denominator": "sum(delta for delta > 0) = 26110 product units across 642 cells",
            "units": "Sum of metadata-decoded pixel differences, without area weights; not integrated radiance slope, net change, physical emission or ground illumination",
        },
        "support": {
            "window_cells": int(inside.size), "inside_cells": int(inside.sum()),
            "common_valid_inside_cells": int(common.sum()),
            "endpoint_support_change_cells": int((inside & (arrays["valid_2019"] != arrays["valid_2024"])).sum()),
            "positive_change_cells": int(brightened.sum()),
            "negative_change_cells": int((delta < 0).sum()),
            "unchanged_cells": int((delta == 0).sum()),
        },
        "endpoint_sums": annual_replay,
        "gross_positive_change": positive_sum,
        "gross_negative_change": negative_sum,
        "net_change": float(delta.sum()),
        "threshold_rows": rows,
        "diagnostics": {
            "maximum_inside_2019": float(before.max()),
            "maximum_inside_2024": float(after.max()),
            "maximum_entire_cache_window_2019": float(np.nanmax(before_grid)),
            "maximum_entire_cache_window_2024": float(np.nanmax(after_grid)),
            "median_2024_value_among_brightened_cells": float(np.median(after[brightened])),
            "brightened_cells_ending_at_10": int((brightened & (after == 10)).sum()),
            "positive_change_from_cells_ending_at_10": float(delta[brightened & (after == 10)].sum()),
            "positive_change_cells_with_delta_over_10": int((delta > 10).sum()),
            "positive_change_sum_with_delta_over_10": float(delta[delta > 10].sum()),
            "zero_to_positive_cells": int((brightened & (before == 0)).sum()),
            "zero_to_positive_change_sum": float(delta[brightened & (before == 0)].sum()),
        },
        "counterexample": {
            "model": "Y = M * Q(A), M = indicator(D >= T)",
            "interpretation": "Illustrative changing-mask counterexample; not fitted, not an exact EOG implementation and not evidence that this occurred",
            "unchanged_unmasked_encoded_values": unmasked_encoded.tolist(),
            "unchanged_mask_statistic": mask_statistic.tolist(),
            "before_after_thresholds": list(thresholds),
            "recorded_before": toy_before.tolist(),
            "recorded_after": toy_after.tolist(),
            "minimum_positive_both_periods": 10,
            "target_change_with_no_change_in_unmasked_value": 610,
            "constraint": "Official original V2 uses a fixed per-cell multiyear threshold; this toy permits a changed masking decision across processing regimes and does not claim undocumented year-by-year threshold adjustment within one implementation",
            "falsification": "Retrieve corresponding native pre-mask values and masks for the high-value cells. Low 2019 pre-mask values relative to 2024 would reject an unchanged-input mask-only account; high pre-mask 2019 values excluded by its mask would support it. Use matched processing and source identity to test broader product effects.",
        },
        "inference": {
            "supported": "Most summed positive endpoint change is contributed by values far above the observed minimum positive encoded value",
            "conditional_rounding_claim": "Under an explicitly bounded rounding-only model allowing at most 10 product units of endpoint difference per unchanged unmasked cell, the 184 cells with delta > 10 cannot arise from that model",
            "not_supported": "The ten-unit observed minimum is an upper bound on upstream masking thresholds or on values suppressed by the mask; all processing effects are excluded; environmental or construction-lighting attribution is proved",
            "identifiability": "Masked zero does not identify the corresponding pre-mask average. High retained 2024 values alone cannot recover it.",
        },
        "recommended_manuscript_wording": wording,
        "primary_methodology_sources": SOURCES,
    }
    output = SCRIPT.with_suffix(".json")
    output.write_text(json.dumps(report, indent=2) + "\n")

    lines = [
        "# Kosciuszko output-floor audit", "",
        f"Completed: {report['completed_hobart']}", "",
        "**Decision:** retain the high-value pixel table, but reject the proposed statement that masking cannot explain those values. The arithmetic is correct; that inference does not follow from it.", "",
        "## Independent numerical replay", "",
        "The cache's internal array hashes all pass. Common-valid, centre-selected inside support contains 39,721 cells: 642 increased, 30 decreased and 39,049 were unchanged. There are no endpoint-only valid inside cells. Direct sums replay the accepted annual mean multiplied by count within 1e-8: 1,220 in 2019 and 26,970 in 2024.", "",
        "Let delta = decoded_2024 - decoded_2019. The denominator is **26,110**, the sum of strictly positive deltas across **642** cells. Negative deltas sum to -360 and net change is 25,750. The following thresholds refer to the **2024 value**, are nested, and include only cells with delta > 0. They are unweighted endpoint cell sums, not the manuscript's area-weighted OLS contributions.", "",
        "| Minimum 2024 value | Brightened cells | Sum of positive differences | Share of all positive differences | Recorded zero in 2019 |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['minimum_2024_value']} | {row['cells']} | {row['positive_change_sum']:,.0f} | {row['percent_of_all_positive_change']:.4f}% | {row['recorded_zero_in_2019_cells']} |")
    lines += [
        "",
        "All 64 cells at or above 100 were zero in the 2019 product. The median 2024 value among brightened cells is 10; 448 cells end at 10 and supply 4,480/26,110 = 17.16% of positive change. There are 184 positive differences larger than 10, supplying 21,530/26,110 = 82.46%. Maxima are 40 and 610 **inside the park**. The entire rectangular cache has a 2019 maximum of 120, so avoid describing 40 as the maximum of the entire window.", "",
        "## What the calculation establishes", "",
        "The increase is not confined to the smallest positive output value. An explanation restricted to one-bin endpoint changes cannot reproduce the 184 differences larger than 10. This is a conditional statement about bounded rounding error, not a general statement about the full product pipeline. The mere observation of a ten-unit lattice does not identify the exact upstream rounding rule or its complete history.", "",
        "## Why it does not exclude masking", "",
        "EOG describes background classification using 3 x 3 data range and cloud-free coverage. The original V2 method derives a per-cell threshold using multiyear information. Its output band is an average with background cells masked; the threshold statistic is not simply the final encoded cell average. See the [official EOG methods and band definitions](https://eogdata.mines.edu/products/vnl/) and [Elvidge et al. (2021)](https://doi.org/10.3390/rs13050922).",
        "",
        "It follows that the smallest retained encoded value supplies no general upper bound on the threshold statistic or on an average discarded by the mask. A recorded zero can mean masking of a nonzero pre-mask value. The cached arrays do not retain that discarded value or the upstream mask diagnostics. The original method's attempt to keep thresholds constant across years is relevant evidence, but does not turn the output floor into such a bound or verify every transformation in the retained cross-version series.", "",
        "## Explicit counterexample and discriminating test", "",
        "Write Y = M Q(A), where A is a pre-mask average, Q is the encoding, and M is a binary retention mask. Let Q(A) be 610 for a target cell and 10 for an always-retained reference cell in both periods. Changing only the target mask from 0 to 1 produces [0, 10] -> [610, 10]: a 610-unit rise, the same ten-unit lattice, and the same smallest positive value. The script checks this exactly. A generic texture rule M = 1[D >= T], with fixed D = [1, 3] and T changing from 2 to 0.5, provides one implementation.", "",
        "These arbitrary mask-statistic units are not calibrated product or physical radiance units. This toy is not the EOG algorithm, does not claim that EOG changed thresholds independently each year, and is not evidence that masking caused the park's rise. It refutes the categorical logical claim that masking cannot reveal a large value while the output floor stays fixed.", "",
        "A discriminating test would compare the corresponding native pre-mask values and masks at the 64 high-value cells. Low pre-mask values in 2019 and high values in 2024 would reject the unchanged-input mask-only example; high 2019 values suppressed by its mask would support it. Consistent source identity and processing would be needed to test broader product effects. That extraction is outside this bounded audit and has not been run.", "",
        "## Recommended manuscript wording", "",
        "> " + wording, "",
        "Keep the table in Supporting Information if useful. Label its denominator explicitly. Do not replace the existing processing qualification with 'Nor can changes in masking or quantisation'.", "",
        "## Reproducibility and scope", "",
        "Run `uv run python analysis/reports/kosciuszko_floor_audit_20261019.py` from the repository root. The calculation imports no existing audit function and performs no network reads. JSON records input and reviewed-reference SHA-256 hashes, all verified array hashes, the cached source metadata, exact denominators, software versions and the executable counterexample. Primary methodology pages were consulted separately on 19 October 2026; direct article retrieval was rate limited, while publisher-indexed text and the EOG page were available.", "",
        f"- Cache SHA-256: `{sha256(CACHE)}`",
        f"- Script SHA-256: `{sha256(SCRIPT)}`",
        f"- JSON receipt SHA-256: `{sha256(output)}`",
        "- No remote rasters, native EOG masks or unmasked averages were acquired. This is an offline replay and inference check, not satellite-product validation.", "",
    ]
    SCRIPT.with_suffix(".md").write_text("\n".join(lines))
    print(json.dumps({"verdict": report["verdict"], "rows": rows,
                      "outputs": [str(output.relative_to(ROOT)), str(SCRIPT.with_suffix('.md').relative_to(ROOT))]}, indent=2))


if __name__ == "__main__":
    main()

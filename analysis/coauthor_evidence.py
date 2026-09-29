#!/usr/bin/env python3
"""Describe accepted annual series without re-estimating the national analysis.

Inputs are the preserved Goal 012 data/processed directory. Missing values
remain missing. The late-positive diagnostic requires all 12 annual values:
2013-2021 zero and at least one positive value in 2022-2024.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

try:
    from analysis.input_contract import InputContract, resolve_contract, sha256
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from input_contract import InputContract, resolve_contract, sha256

EXAMPLE_IDS = ("WA_27575", "WA_39584", "ACT_03", "NSW_N1142")
# Kept as a public compatibility mapping for existing figure/table tooling.
# Explicit corrected runs calculate categories from the actual slope signs.
EXAMPLES = {
    "WA_27575": "Both slopes positive",
    "WA_39584": "Inside only positive",
    "ACT_03": "Neither slope positive",
    "NSW_N1142": "Surrounding only positive",
}

# Accepted Goal 012 inputs, reconciled with the preserved source record.
EXPECTED_SHA256 = {
    "pa_radiance_buffers_national_v0_3_0.csv": "63e95fb30b0bdebc6c74d23f08666ab9cfe0ef408d27744f12fbb029a8b92ec1",
    "pa_trends_v0_3_0.csv": "d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f",
    "pa_risk_rankings_v0_3_0.csv": "554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a",
    "pa_geometries_v0_3_0.csv": "781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b",
}


def describe_zero_series(wide: pd.DataFrame) -> pd.DataFrame:
    """Return exact-value descriptive flags; unobserved years are never zeros."""
    wide = wide.reindex(columns=range(2013, 2025))
    complete = wide.notna().all(axis=1)
    return pd.DataFrame({
        "valid_years": wide.notna().sum(axis=1),
        "minimum": wide.min(axis=1),
        "maximum": wide.max(axis=1),
        "any_variation": wide.max(axis=1) > wide.min(axis=1),
        "all_observed_zero": wide.eq(0).sum(axis=1).eq(wide.notna().sum(axis=1)),
        "complete_12_years": complete,
        "late_positive_complete": complete & wide.loc[:, 2013:2021].eq(0).all(axis=1)
        & wide.loc[:, 2022:2024].gt(0).any(axis=1),
    })


def category_for_slopes(inside: float, surrounding: float) -> str:
    return {(True, True): "Both slopes positive", (True, False): "Inside only positive",
            (False, False): "Neither slope positive", (False, True): "Surrounding only positive"}[
                (inside > 0, surrounding > 0)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--input-manifest", type=Path)
    args = parser.parse_args()
    names = ["pa_radiance_buffers_national_v0_3_0.csv", "pa_trends_v0_3_0.csv",
             "pa_risk_rankings_v0_3_0.csv", "pa_geometries_v0_3_0.csv"]
    contract = resolve_contract(args.data_dir, names, args.input_manifest, EXPECTED_SHA256)
    paths = contract.files
    hashes = {name: sha256(path) for name, path in paths.items()}
    trends = pd.read_csv(paths[names[1]])
    trends = trends[(trends.metric == "mean") & (trends.buffer_type == "land_unprotected")]
    if trends.pa_id.duplicated().any():
        raise ValueError("Primary trends contain duplicate pa_id values")
    if not trends.n_years_inside.ge(8).all():
        raise ValueError("Primary trends contain fewer than 8 valid inside years")
    if contract.mode == "legacy":
        assert len(trends) == 4426
        assert trends.slope_inside.eq(0).sum() == 3969
        assert trends.slope_inside.gt(0).sum() == 420
    columns = ["pa_id", "zone", "buffer_km", "buffer_type", "year", "mean", "valid_pixel_count"]
    parts = []
    for chunk in pd.read_csv(paths[names[0]], usecols=columns, chunksize=100000):
        keep = chunk.zone.eq("inside") | (
            chunk.pa_id.isin(EXAMPLE_IDS) & chunk.zone.eq("buffer")
            & chunk.buffer_km.eq(1) & chunk.buffer_type.eq("land_unprotected"))
        parts.append(chunk.loc[keep].copy())
    annual = pd.concat(parts, ignore_index=True)
    if not annual.year.isin(range(2013, 2025)).all():
        raise ValueError("Radiance input contains years outside 2013--2024")
    if annual.valid_pixel_count.lt(0).any():
        raise ValueError("Radiance input contains negative valid pixel counts")
    annual.loc[annual.valid_pixel_count < 10, "mean"] = np.nan
    inside = annual[annual.zone.eq("inside")]
    if inside.duplicated(["pa_id", "year"]).any():
        raise ValueError("Inside radiance table contains duplicate PA-year rows")
    wide = inside.pivot(index="pa_id", columns="year", values="mean")
    flags = describe_zero_series(wide.loc[trends.loc[trends.slope_inside.eq(0), "pa_id"]])
    if not flags.valid_years.ge(8).all():
        raise ValueError("Inside series for zero-slope rows contain fewer than 8 valid years")
    ranks = pd.read_csv(paths[names[2]])
    if ranks.pa_id.duplicated().any():
        raise ValueError("Risk rankings contain duplicate pa_id values")
    if contract.mode == "legacy":
        assert len(ranks) == 3858
    qcounts = [int(((ranks.slope_inside > 0) & (ranks.slope_buffer_1km > 0)).sum()),
               int(((ranks.slope_inside > 0) & (ranks.slope_buffer_1km <= 0)).sum()),
               int(((ranks.slope_inside <= 0) & (ranks.slope_buffer_1km <= 0)).sum()),
               int(((ranks.slope_inside <= 0) & (ranks.slope_buffer_1km > 0)).sum())]
    if contract.mode == "legacy":
        assert qcounts == [305, 55, 3308, 190]
    examples = annual[annual.pa_id.isin(EXAMPLE_IDS)].merge(
        ranks[["pa_id", "name", "state", "slope_inside", "slope_buffer_1km"]], on="pa_id", validate="many_to_one")
    examples["category"] = [category_for_slopes(i, b) for i, b in zip(examples.slope_inside, examples.slope_buffer_1km)]
    if contract.mode == "legacy":
        assert len(examples) == 96
    if examples["mean"].isna().any():
        raise ValueError("Example series contains unsupported annual means")
    example_rows = ranks[ranks.pa_id.isin(EXAMPLE_IDS)]
    if set(example_rows.pa_id) != set(EXAMPLE_IDS):
        raise ValueError("Required coauthor example identifiers are missing")
    for row in example_rows.itertuples():
        actual = category_for_slopes(row.slope_inside, row.slope_buffer_1km)
        EXAMPLES[row.pa_id] = actual
    geoms = pd.read_csv(paths[names[3]])
    flags = flags.reset_index().merge(geoms[["pa_id", "NAME", "STATE"]], on="pa_id", validate="one_to_one")
    report = {
        "source": ("Preserved Goal 012 accepted outputs; no raster extraction or model refit"
                   if contract.mode == "legacy" else
                   "Manifest-provided corrected spatial summaries; no raster extraction or model refit"),
        "source_sha256": hashes,
        "input_contract": contract.identity(),
        "zero_sen_denominator": len(flags),
        "any_observed_annual_variation": int(flags.any_variation.sum()),
        "all_observed_annual_values_zero": int(flags.all_observed_zero.sum()),
        "constant_nonzero": int((~flags.any_variation & ~flags.all_observed_zero).sum()),
        "complete_12_year_series": int(flags.complete_12_years.sum()),
        "valid_year_counts": {str(k): int(v) for k, v in flags.valid_years.value_counts().sort_index().items()},
        "late_positive_complete": int(flags.late_positive_complete.sum()),
        "late_positive_definition": "All 12 years valid; 2013-2021 mean=0 and at least one 2022-2024 mean>0",
        "paired_sign_counts_q1_q2_q3_q4": qcounts,
        "example_selection": "Four illustrative cases selected for contrasting signs; Black Mountain deliberately illustrates two negative slopes. Not a representative sample or priority ranking.",
        "examples": [dict(record, category=EXAMPLES[record["pa_id"]]) for record in ranks.loc[ranks.pa_id.isin(EXAMPLE_IDS), ["pa_id", "name", "state", "slope_inside", "slope_buffer_1km"]].to_dict(orient="records")],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    flags.to_csv(args.output_dir / "zero_sen_series_diagnostic.csv", index=False)
    examples.sort_values(["pa_id", "zone", "year"]).to_csv(args.output_dir / "coauthor_example_series.csv", index=False)
    (args.output_dir / "coauthor_evidence.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

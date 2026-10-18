# Independent audit of decreases and fixed exclusions — 18 October 2026

The corrected annual summaries reproduce the exclusion arithmetic. Independent bounded raster-window reads reproduce the cluster magnitudes and shares, while detecting a crop-support defect in the inspected hotspot script.

## Fixed five reserves

Selection uses the five most negative 2013–2024 whole-reserve integrated OLS slopes. The identical set is excluded from both periods.

| Reserve | ID | 2013–2024 slope | 2013–2021 slope | Share of full-period negative slopes |
|---|---|---:|---:|---:|
| Barrow Island | WA_11648 | -1240.546920 | -1099.271200 | 55.6174% |
| Murujuga | WA_2803 | -766.806484 | -1194.356572 | 34.3782% |
| Strzelecki | SA_0011 | -59.851595 | -81.494261 | 2.6833% |
| Thevenard Island | WA_33174 | -29.135731 | -48.712996 | 1.3062% |
| Newlands | QLD_NR234 | -20.663521 | -35.744021 | 0.9264% |

Combined share: **94.911615%**. All five inside count series are constant. Strzelecki is third; Thevenard is fourth.

| Cohort | Retained reserves | Net 2013–2024 | Net 2013–2021 |
|---|---:|---:|---:|
| all | 4426 | +478.947188 | -537.841686 |
| exclude_fixed_five | 4421 | +2595.951438 | +1921.737363 |
| exclude_fixed_five_and_kosciuszko | 4420 | +2226.178669 | +1878.609428 |

## Cluster and wording checks

- Barrow Island's whole-reserve sum was 74,690 in 2015 and 207,180 in 2016: **2.773865 times**, or +177.387%. Use ‘nearly tripled’. The +144,300 cluster supplies **99.903074%** of gross positive pixel differences (+144,440), and 108.913880% of the net jump (+132,490). It is not 100% of net change.
- Murujuga falls from 76,060 to 10,510 between 2013 and 2024: **86.181962%**. Its −63,070 cluster supplies **96.187281%** of gross negative differences (−65,570); other pixels increase by 20.
- Thevenard falls from 3,370 in 2013 to zero in 2024. It is zero in 2016–2017, positive again in 2018 (200) and 2019 (70), then zero in 2020–2024. The endpoint cannot establish permanent cessation of measured light in 2014.
- Barrow's 2016 peak is followed by decreases and rebounds, not monotonic decline. Strzelecki's 2015 spike (10,800) also strongly affects its fitted trend.

## Window-support defect and independent verification

The inspected hotspot script uses floor-offset/nearest-length window rounding. This can crop away polygon-selected cells. The independent replay floors starts and ceils stops, matching canonical counts. All omitted cells were zero at the compared endpoints; the reported cluster quantities survive correction.

| Reserve ID | Reported common cells | Correct covering-window common cells | Omitted cells | Omitted endpoint sums |
|---|---:|---:|---:|---|
| WA_11648 | 1262 | 1263 | 1 | [0.0, 0.0] |
| WA_2803 | 259 | 259 | 0 | [0.0, 0.0] |
| SA_0011 | 43192 | 43238 | 46 | [0.0, 0.0] |
| WA_33174 | 109 | 110 | 1 | [0.0, 0.0] |

All eight cropped decoded-array hashes reproduce the inspected output hashes; covering-window annual sums and counts reproduce the corrected pipeline. Scale and offset are applied before differencing; all four pairs have no endpoint-only valid cells. Current output endpoints therefore coincide with common-support sums. In general, the inspected script's endpoint totals are per-year-valid totals, whereas its difference denominators use common support.

## Interpretation limits

- Exclusions were selected post hoc by the strongest negative full-period outcomes; shorter-period reuse is a fixed-cohort sensitivity, not independent confirmation of broad brightening.
- This audit verifies product observations and spatial concentration, not facility identities, operational causes, or ecological exposure.
- Endpoint clusters use different periods across reserves and cannot be interpreted as spatial decompositions of the full-period OLS slope.
- The 2013-2024 endpoint comparisons span product-source changes; the Barrow 2015-2016 spike is within the earlier period but that does not establish homogeneous processing.
- A 2021 rise precedes the documented 2022 source change but does not exclude all processing effects; spatial concentration alone does not rule them out.
- Thevenard has positive observations again in 2018 and 2019; a zero 2024 endpoint does not show persistent absence since oil production ended.
- Cluster selection is eight-neighbour connectivity of same-sign common-valid differences; reported clusters have absolute change at least 200, while denominators include all same-sign pixel changes.

No primary-source facility verification was performed by this audit. Claims about Gorgon, Karratha Gas Plant, construction or decommissioning require their separate source and location checks. The cited Woodside account concerns 2025, outside the analysis period, and cannot establish the cause of the 2013–2024 decrease.

## Supplementary Figure S7

The wrapper also renders `manuscript/figures/fig_decrease_histories.png` and `.pdf` directly from the corrected annual summaries. Separate panels show Barrow Island, Murujuga and Thevenard Island (full-period decreasing ranks 1, 2 and 4), with independent linear vertical scales, visible zeros and a 2022 source-change marker. These cases were selected after inspecting the results; no industrial events or causal explanations are annotated. Thevenard's 2018–2019 return to positive values and both larger reserves' rebounds remain visible. Figure hashes and the 36 plotted observations are recorded in the JSON receipt.

## Reproduction

Run `analysis/reports/decrease_audit_20261018.py` with the project Python environment. Default replay uses the saved NPZ and makes no network requests. `--fetch-windows` explicitly reacquires eight bounded windows (each below 150,000 cells). Input identities, requested windows, scales, transforms, array hashes, access times and acceptance checks are retained in the JSON receipt.

## Figure QA receipt

2026-10-18T20:10:56+11:00: inspected PNG and rasterized PDF; all 36 observations, zero values and Thevenard reappearance remain visible. A source-marker/rank-label collision was repaired. The PDF passed `qpdf --check`. Current figure hashes and detailed QA are in the JSON; regeneration resets visual QA pending a fresh check.

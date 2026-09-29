# Layer A uncertainty-aware watchlists

Generated: 2026-09-19 05:50 UTC

Category-safe protected-area watchlists joined to the IBRA-cluster moving-block bootstrap. Uncertainty columns describe inside-protected-area mean-radiance slopes; buffer and retention columns are point estimates from the risk-ranking table.

Top N per category: 20

## Validation notes

- Category filters match the risk-ranking definitions.
- Category ranks are sorted and capped at the requested top N.
- Bootstrap probability fields are bounded in [0,1].
- All watchlist rows have inside-slope bootstrap uncertainty.

## Inside brightening

inside slope > 0; ranked by inside slope

| category | rank | PA name | PA_ID | state | IBRA | area_km2 | inside_slope | buffer_1km_slope | retention_1km | inside_slope_95ci | P_inside_slope_gt0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inside brightening | 1 | Neerabup | WA_27575 | WA | SWA | 9.735 | 8.150 | 3.847 | 4.303 | 0.254 to 12.364 | 0.975 |
| Inside brightening | 2 | Craigieburn Grassland N.C.R. | VIC_4007 | VIC | SVP | 3.440 | 7.397 | 8.340 | -0.943 | 5.735 to 9.365 | 1.000 |
| Inside brightening | 3 | Torrens Island | SA_0038 | SA | EYB | 6.387 | 3.727 | 3.788 | -0.061 | 2.451 to 5.139 | 1.000 |
| Inside brightening | 4 | Wianamatta | NSW_N1123 | NSW | SYB | 7.371 | 3.333 | 3.348 | -0.014 | 2.332 to 4.390 | 0.993 |
| Inside brightening | 5 | Lane Cove | NSW_N0083 | NSW | SYB | 7.186 | 2.872 | 1.408 | 1.463 | 0.513 to 4.359 | 0.986 |
| Inside brightening | 6 | Lake Joondalup | WA_21708 | WA | SWA | 4.481 | 2.750 | 1.734 | 1.016 | 0.740 to 6.000 | 0.989 |
| Inside brightening | 7 | Unnamed WA53313 | WA_53313 | WA | SWA | 6.099 | 2.168 | 3.206 | -1.038 | 0.859 to 3.047 | 0.996 |
| Inside brightening | 8 | Windsor Downs | NSW_N0598 | NSW | SYB | 3.643 | 2.143 | 1.257 | 0.886 | 1.280 to 2.857 | 1.000 |
| Inside brightening | 9 | Goorooyarroo | ACT_33 | ACT | SEH | 8.290 | 2.004 | 0.833 | 1.171 | 1.224 to 3.197 | 1.000 |
| Inside brightening | 10 | Swan River | WA_48325 | WA | SWA | 29.989 | 1.935 | 1.995 | -0.060 | 1.044 to 2.490 | 0.996 |
| Inside brightening | 11 | Prospect | NSW_N0938 | NSW | SYB | 3.256 | 1.905 | 4.583 | -2.679 | 0.238 to 2.693 | 0.976 |
| Inside brightening | 12 | Worrigee | NSW_N0877 | NSW | SYB | 2.293 | 1.763 | 2.928 | -1.165 | 1.154 to 2.877 | 1.000 |
| Inside brightening | 13 | Henderson | WA_39584 | WA | SWA | 2.981 | 1.731 | 2.833 | -1.102 | -3.462 to 4.360 | 0.730 |
| Inside brightening | 14 | Charles Darwin | NT_PA115 | NT | DAC | 13.028 | 1.686 | 3.199 | -1.513 | 0.260 to 2.668 | 0.987 |
| Inside brightening | 15 | Goegrup Lake | WA_26351 | WA | SWA | 3.197 | 1.654 | 1.429 | 0.226 | 0.588 to 3.515 | 1.000 |
| Inside brightening | 16 | Molonglo River | ACT_53 | ACT | SEH | 12.073 | 1.614 | 2.412 | -0.798 | 1.162 to 1.972 | 1.000 |
| Inside brightening | 17 | Yiraaldiya | NSW_N1210 | NSW | SYB | 5.388 | 1.452 | 4.394 | -2.942 | -0.645 to 2.212 | 0.958 |
| Inside brightening | 18 | Cobbler Creek | SA_0244 | SA | FLB | 2.669 | 1.429 | 2.105 | -0.676 | 0.429 to 2.381 | 0.993 |
| Inside brightening | 19 | Daisy Hill | QLD_0966DSY001 | QLD | SEQ | 7.835 | 1.424 | 1.478 | -0.053 | 1.066 to 1.977 | 0.990 |
| Inside brightening | 20 | Black Hill | SA_0095 | SA | FLB | 7.597 | 1.369 | 1.223 | 0.146 | 1.132 to 1.905 | 1.000 |

## External pressure

1 km unprotected-land buffer slope > 0 and inside slope <= 0; ranked by buffer slope

| category | rank | PA name | PA_ID | state | IBRA | area_km2 | inside_slope | buffer_1km_slope | retention_1km | inside_slope_95ci | P_inside_slope_gt0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| External pressure | 1 | Poonthie Ruwe | SA_0569 | SA | MDD | 2.415 | 0.000 | 1.255 | -1.255 | 0.000 to 0.208 | 0.135 |
| External pressure | 2 | Mount Coolum | QLD_0596MCL001 | QLD | SEQ | 3.634 | -0.096 | 0.771 | -0.867 | -0.980 to 1.691 | 0.374 |
| External pressure | 3 | Long Reach | TAS_50387 | TAS | BEL | 3.232 | -0.825 | 0.755 | -1.579 | -2.893 to 1.038 | 0.125 |
| External pressure | 4 | Kinleyside | ACT_48 | ACT | SEH | 2.272 | -0.509 | 0.633 | -1.142 | -1.111 to 0.222 | 0.033 |
| External pressure | 5 | Barubbra Island | QLD_0278BRB001 | QLD | SEQ | 2.268 | 0.000 | 0.621 | -0.621 | 0.000 to 0.227 | 0.414 |
| External pressure | 6 | Lake Corringle W.R | VIC_459 | VIC | SEC | 9.220 | 0.000 | 0.610 | -0.610 | 0.000 to 0.000 | 0.000 |
| External pressure | 7 | Kuma | NSW_N0900 | NSW | SEH | 1.839 | 0.000 | 0.484 | -0.484 | 0.000 to 0.303 | 0.238 |
| External pressure | 8 | Bungonia | NSW_N1142 | NSW | SEH | 7.690 | 0.000 | 0.417 | -0.417 | 0.000 to 0.000 | 0.000 |
| External pressure | 9 | Twin Swamps | WA_27621 | WA | SWA | 1.553 | 0.000 | 0.415 | -0.415 | 0.000 to 0.000 | 0.000 |
| External pressure | 10 | Tiraki | NSW_N0975 | NSW | SYB | 6.127 | 0.000 | 0.329 | -0.329 | 0.000 to 0.000 | 0.000 |
| External pressure | 11 | Loch Luna | SA_0220 | SA | RIV | 20.697 | 0.000 | 0.307 | -0.307 | 0.000 to 0.051 | 0.246 |
| External pressure | 12 | Mapleton | QLD_1069MCP001 | QLD | SEQ | 3.595 | 0.000 | 0.301 | -0.301 | 0.000 to 0.000 | 0.000 |
| External pressure | 13 | Cotton Bush | TAS_21491 | TAS | TSR | 2.226 | 0.000 | 0.297 | -0.297 | 0.000 to 0.000 | 0.000 |
| External pressure | 14 | Bumbang I262 B.R | VIC_1328 | VIC | MDD | 5.624 | 0.000 | 0.297 | -0.297 | 0.000 to 0.000 | 0.003 |
| External pressure | 15 | Casvarina | TAS_12645 | TAS | TNS | 1.853 | 0.000 | 0.294 | -0.294 | 0.000 to 0.000 | 0.000 |
| External pressure | 16 | Onkaparinga River | SA_0241 | SA | FLB | 2.688 | -0.583 | 0.285 | -0.869 | -2.000 to 0.000 | 0.021 |
| External pressure | 17 | Mitchell River Silt Jetties G.L.R. | VIC_3630 | VIC | SCP | 2.702 | 0.000 | 0.260 | -0.260 | 0.000 to 0.000 | 0.000 |
| External pressure | 18 | Devilbend N.F.R. | VIC_4746 | VIC | SCP | 10.069 | 0.000 | 0.252 | -0.252 | 0.000 to 0.074 | 0.103 |
| External pressure | 19 | Middle Arm | TAS_50735 | TAS | FUR | 1.944 | 0.000 | 0.250 | -0.250 | 0.000 to 0.000 | 0.000 |
| External pressure | 19 | Goorooyarroo | NSW_N0433 | NSW | SEH | 3.118 | 0.000 | 0.250 | -0.250 | 0.000 to 0.096 | 0.056 |

## Internalisation

inside slope > 0 and inside slope > 1 km buffer slope; ranked by inside-minus-buffer gap

| category | rank | PA name | PA_ID | state | IBRA | area_km2 | inside_slope | buffer_1km_slope | retention_1km | inside_slope_95ci | P_inside_slope_gt0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Internalisation | 1 | Neerabup | WA_27575 | WA | SWA | 9.735 | 8.150 | 3.847 | 4.303 | 0.254 to 12.364 | 0.975 |
| Internalisation | 2 | Jerrabomberra Wetlands | ACT_09 | ACT | SEH | 2.058 | 0.363 | -2.934 | 3.298 | -2.308 to 1.863 | 0.550 |
| Internalisation | 3 | Red Hill | ACT_21 | ACT | SEH | 2.928 | 0.360 | -2.105 | 2.465 | -0.877 to 1.579 | 0.828 |
| Internalisation | 4 | Mulligans Flat | ACT_27 | ACT | SEH | 9.840 | 1.080 | -1.153 | 2.233 | 0.526 to 1.930 | 0.990 |
| Internalisation | 5 | Mount Whitfield | QLD_0470MWT001 | QLD | WET | 3.285 | 0.544 | -0.956 | 1.500 | 0.000 to 1.333 | 0.970 |
| Internalisation | 6 | Lane Cove | NSW_N0083 | NSW | SYB | 7.186 | 2.872 | 1.408 | 1.463 | 0.513 to 4.359 | 0.986 |
| Internalisation | 7 | Isaacs Ridge | ACT_08 | ACT | SEH | 3.668 | 0.500 | -0.886 | 1.386 | -0.500 to 1.375 | 0.646 |
| Internalisation | 8 | Goorooyarroo | ACT_33 | ACT | SEH | 8.290 | 2.004 | 0.833 | 1.171 | 1.224 to 3.197 | 1.000 |
| Internalisation | 9 | Richmond River | NSW_N0572 | NSW | SEQ | 2.509 | 0.698 | -0.377 | 1.075 | 0.000 to 1.667 | 0.933 |
| Internalisation | 10 | Lake Joondalup | WA_21708 | WA | SWA | 4.481 | 2.750 | 1.734 | 1.016 | 0.740 to 6.000 | 0.989 |
| Internalisation | 11 | Langwarrin Flora & Fauna Reserve | VIC_3365 | VIC | SCP | 2.154 | 1.071 | 0.143 | 0.929 | 0.000 to 1.667 | 0.968 |
| Internalisation | 12 | Windsor Downs | NSW_N0598 | NSW | SYB | 3.643 | 2.143 | 1.257 | 0.886 | 1.280 to 2.857 | 1.000 |
| Internalisation | 13 | Melrose | ACT_51 | ACT | SEH | 1.968 | 0.272 | -0.606 | 0.879 | -0.385 to 0.769 | 0.719 |
| Internalisation | 14 | Sydney Harbour | NSW_N0039 | NSW | SYB | 3.953 | 0.909 | 0.205 | 0.704 | -0.294 to 1.364 | 0.881 |
| Internalisation | 15 | Kuyunba | NT_PA57 | NT | MAC | 6.289 | 0.500 | -0.187 | 0.687 | 0.000 to 0.667 | 0.925 |
| Internalisation | 16 | Brian Burke Reserve | QLD_NR1921 | QLD | SEQ | 2.684 | 0.889 | 0.240 | 0.649 | 0.333 to 1.333 | 0.976 |
| Internalisation | 17 | Bullen Range | ACT_01 | ACT | SEH | 40.255 | 0.161 | -0.488 | 0.649 | 0.046 to 0.218 | 0.987 |
| Internalisation | 18 | Unnamed WA35283 | WA_35283 | WA | SWA | 2.707 | 0.577 | -0.034 | 0.611 | 0.000 to 1.111 | 0.902 |
| Internalisation | 19 | Stanwell Power Station | QLD_NR295 | QLD | BBS | 6.360 | 0.433 | -0.095 | 0.528 | 0.294 to 0.588 | 1.000 |
| Internalisation | 20 | Marshalls Creek | NSW_N0791 | NSW | SEQ | 1.536 | 0.281 | -0.244 | 0.525 | -0.455 to 0.909 | 0.754 |

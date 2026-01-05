# Layer B go/no-go decision (WP0.14)

Generated: 2026-01-05 00:10 UTC
Decision date: 2026-01-05
Status: GO for WP0.16 (provider-matched primary; multi-provider sensitivity only)
Config version: 0.3.0

## Scope
- Spatial: Australia; occurrences inside terrestrial protected areas and within 10 km buffers (assigned to nearest PA).
- Temporal years: 2013–2024

## Go/no-go criteria
- >= 5,000 focal records after filtering within spatial scope
- >= 15 focal species with >= 50 records each
- >= 80% of focal records have valid ALAN covariates
- >= 5,000 records for the primary negative control group after filtering
- Provider-matched control subset is feasible (dominant providers overlap between focal/control)
- Bias controls (target-group background, spatial blocking) are feasible at national or stated regional scale

## Focal taxa
| Group | Rationale | Inclusions/exclusions | Expected response |
| --- | --- | --- | --- |
| Microbats (Chiroptera excluding Pteropodidae) | Nocturnal insectivores with evidence of ALAN sensitivity; aligns with Layer A hypothesis. | Inclusions: Vespertilionidae, Molossidae, Hipposideridae, Rhinolophidae<br>Exclusions: Pteropodidae (fruit bats) | Negative association with ALAN or weaker positive association than controls. |

## Negative controls
| Group | Rationale | Expected response |
| --- | --- | --- |
| Diurnal birds (Aves; Passeriformes; provider-matched to focal data where possible) | High observer effort; expected to be neutral or positively associated with ALAN due to sampling bias. Primary control will be provider-matched to dominant focal-data providers. | Neutral/positive; if similar to focal taxa after provider-matching, interpret as bias. |
| Diurnal reptiles (Squamata; diurnal subset) | Field-observation driven; provides non-nocturnal control. Deferred due to ALA download failures (DEC-026). | Neutral/positive; strong negative would question ALAN-specific inference. |

## Bias-control strategy
### Filters
- Year 2013-2024 only
- Coordinate uncertainty <= 1000 m
- Remove captive/escaped/cultivated records
- Deduplicate per species per day per 1 km grid cell
- Exclude records without species-level identification

### Background sampling
- Target-group background sampled from all ALA records of the same class within the same time window and spatial scope.

### Sampling covariates
- Local record density (kernel of all ALA records)
- Distance to roads/settlements if available (optional)

### Spatial blocking
- Block size: 50 km

### Sensitivity checks
- Alternative ALAN summaries (mean vs median)
- Vary buffer radius (inside, 1 km, 5 km, 10 km)
- Exclude records within 5 km of major urban cores
- Temporal split (2013-2018 vs 2019-2024)

### Falsification checks
- Run identical models on negative controls
- Shuffle ALAN values within bioregions
- Provider-matched subset check (e.g., NSW BioNet-only)

## Planned data sources
- Atlas of Living Australia (ALA) occurrence downloads (mixed provider licences; see ledger)
- CAPAD 2024 protected areas (for spatial scope)
- Zenodo VIIRS night-lights (Layer A rasters)

## Notes
- Proceed to WP0.15 only if criteria are met; otherwise stop at descriptive summaries without causal language.
- Layer B is optional and contingent on negative-control results.
- If provider dominance is extreme, treat analysis as provider-/region-bounded case study.
- Primary inference uses provider-matched dr368 subset; full multi-provider run is sensitivity only.

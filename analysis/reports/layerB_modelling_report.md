# Layer B modelling report (WP0.16)

Generated: 2026-01-05 07:15 UTC

## Primary design
- Provider-matched: dr368
- Spatial blocking: 50 km
- Evaluation: GroupKFold (5 folds) on spatial blocks
- Response: microbats (1) vs passerines (0) case-control classification
- Control design: passerines as target-group background (provider-matched)
- ALAN covariates: any_light indicator + log1p(ALAN) conditional on >0
- Scope: records inside protected areas or within 10 km buffers
- Sensitivity birds sample rate: 1.00

## Model input summary
schema_version             run         group  n_records                                                                                                                                                                    providers  years_min  years_max  inside_fraction  within_fraction  zero_fraction  block_km  buffer_km  sample_rate
         0.3.0   primary_dr368     microbats      50281                                                                                                                                                                        dr368       2013       2024         0.278376         0.721624       0.657028      50.0       10.0          1.0
         0.3.0   primary_dr368 diurnal_birds      50281                                                                                                                                                                        dr368       2013       2024         0.256518         0.743482       0.651180      50.0       10.0          1.0
         0.3.0 sensitivity_all     microbats      56883                                                                     dr1097,dr1132,dr1411,dr2008,dr22510,dr2592,dr340,dr342,dr344,dr361,dr364,dr365,dr368,dr7703,dr7813,dr836       2013       2024         0.279715         0.720285       0.670446      50.0       10.0          1.0
         0.3.0 sensitivity_all diurnal_birds      56883 dr1010,dr1097,dr1099,dr1132,dr1411,dr16778,dr2009,dr22499,dr22510,dr2592,dr340,dr341,dr342,dr344,dr359,dr360,dr361,dr364,dr365,dr368,dr466,dr714,dr7706,dr7814,dr7965,dr9956       2013       2024         0.204683         0.795317       0.551043      50.0       10.0          1.0

## Primary (provider-matched) results
### Coefficients (log-odds)
   feature  mean_log_odds  std_log_odds  odds_ratio  ci95_low  ci95_high
 any_light       1.315818      0.127743    3.727798  1.065442   1.566194
log1p_alan      -0.354431      0.023846    0.701573 -0.401170  -0.307692

### Cross-validated metrics
              auc  log_loss
run                        
primary  0.544657    0.6892

## Falsification (ALAN shuffled within blocks)
### Coefficients (log-odds)
   feature  mean_log_odds  std_log_odds  odds_ratio  ci95_low  ci95_high
 any_light       0.202411      0.086377    1.224351  0.033113   0.371709
log1p_alan      -0.026923      0.021043    0.973436 -0.068168   0.014321

### Cross-validated metrics
               auc  log_loss
run                         
shuffled  0.505466  0.695243

## Sensitivity (multi-provider)
### Coefficients (log-odds)
   feature  mean_log_odds  std_log_odds  odds_ratio  ci95_low  ci95_high
 any_light       0.731746      0.330202    2.078707  0.084549   1.378943
log1p_alan      -0.331665      0.093925    0.717728 -0.515758  -0.147571

### Cross-validated metrics
                  auc  log_loss
run                            
sensitivity  0.556655  0.699828

## Interpretation (what we can/can't conclude)
- This is a provider-matched, spatially blocked presence-only case-control signal test (not a population trend).
- The ALAN two-part covariates reduce sensor-floor dominance; inference is limited to relative differences between microbats and passerines within dr368.
- If shuffled ALAN retains similar coefficients or predictive performance, the model is capturing sampling bias rather than an ALAN-linked signal.
- Sensitivity results on the multi-provider dataset are descriptive only and should not be used for primary inference.
- Any effect should be interpreted as an association in occurrence records, not causal impact.

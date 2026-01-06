# Layer B modelling report (WP0.16)

Generated: 2026-01-06 09:29 UTC

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

## Falsification (ALAN shuffled within IBRA × year)
### Coefficients (log-odds)
   feature  mean_log_odds  std_log_odds  odds_ratio  ci95_low  ci95_high
 any_light       0.163136      0.062740    1.177197  0.040165   0.286107
log1p_alan      -0.001463      0.008311    0.998538 -0.017754   0.014827

### Cross-validated metrics
                    auc  log_loss
run                              
ibra_shuffled  0.516707  0.694683

## Sensitivity (multi-provider)
### Coefficients (log-odds)
   feature  mean_log_odds  std_log_odds  odds_ratio  ci95_low  ci95_high
 any_light       0.731746      0.330202    2.078707  0.084549   1.378943
log1p_alan      -0.331665      0.093925    0.717728 -0.515758  -0.147571

### Cross-validated metrics
                  auc  log_loss
run                            
sensitivity  0.556655  0.699828

## IBRA heterogeneity (log1p(ALAN) coefficient)
- Minimum records per class: 500
- Regions included: 11

ibra_code                 ibra_name  n_microbats  n_birds  mean_log_odds  ci95_low  ci95_high
      BBS       Brigalow Belt South         4737     3220       0.055044  0.006521   0.103567
      MDD Murray Darling Depression          660     1668      -0.483106 -1.034369   0.068157
      NAN                  Nandewar         1988     1156      -0.129783 -0.278307   0.018742
      NET    New England Tablelands         1111      888      -0.227740 -0.323783  -0.131696
      NNC           NSW North Coast         6632     3742      -0.284475 -0.306625  -0.262325
      NSS  NSW South Western Slopes          617     5105       0.127443 -0.202472   0.457359
      RIV                  Riverina          786     2070       0.089905  0.001424   0.178386
      SEC         South East Corner         3968     2042      -0.182668 -0.294066  -0.071270
      SEH   South Eastern Highlands         1650     3570      -0.655957 -0.872295  -0.439620
      SEQ  South Eastern Queensland         1988     2821      -0.206439 -0.341402  -0.071476
      SYB              Sydney Basin        25232    21635      -0.405638 -0.472311  -0.338965

## Interpretation (what we can/can't conclude)
- This is a provider-matched, spatially blocked presence-only case-control signal test (not a population trend).
- The ALAN two-part covariates reduce sensor-floor dominance; inference is limited to relative differences between microbats and passerines within dr368.
- If shuffled ALAN retains similar coefficients or predictive performance, the model is capturing sampling bias rather than an ALAN-linked signal.
- Sensitivity results on the multi-provider dataset are descriptive only and should not be used for primary inference.
- Any effect should be interpreted as an association in occurrence records, not causal impact.

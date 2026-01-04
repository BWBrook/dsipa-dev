# Layer B data QC

Generated: 2026-01-04 03:20 UTC

Coordinate uncertainty filter: <= 1000 m

## Query definitions

- microbats: Microbats (Chiroptera excluding Pteropodidae)
  - Notes: Nocturnal focal taxa; excludes fruit bats.
  - fq: year:[2013 TO 2024], taxonRank:species, occurrenceStatus:present, coordinateUncertaintyInMeters:[0 TO 1000], country:Australia, order:Chiroptera, -family:Pteropodidae
- diurnal_birds: Diurnal birds proxy (Passeriformes)
  - Notes: Negative control proxy; Passeriformes used as diurnal birds.
  - fq: year:[2013 TO 2024], taxonRank:species, occurrenceStatus:present, coordinateUncertaintyInMeters:[0 TO 1000], country:Australia, class:Aves, order:Passeriformes

## Summary counts

        group  raw_records  filtered_records  dedup_records  unique_species
    microbats       108695            107907          63716              59
diurnal_birds      2845757           2834940        2378378             348

## microbats yearly counts (post-dedup)

      records
year         
2013     2767
2014     4160
2015     3544
2016     5092
2017     6273
2018     6546
2019     4072
2020     4549
2021     4511
2022     6716
2023    10110
2024     5376

## microbats state counts (post-dedup)

                              records
state                                
Australian Capital Territory        6
New South Wales                 56766
Northern Territory                310
Queensland                       1040
South Australia                  3748
Tasmania                           27
Victoria                         1706
Western Australia                 108

## diurnal_birds yearly counts (post-dedup)

      records
year         
2013   249535
2014   196747
2015   188186
2016   215436
2017   243295
2018   278215
2019   212597
2020   226691
2021   192836
2022   147490
2023   119806
2024   107544

## diurnal_birds state counts (post-dedup)

                              records
state                                
Australian Capital Territory   235847
New South Wales                898865
Norfolk Island                      1
Northern Territory              25542
Queensland                     148284
South Australia                175541
Tasmania                        47331
Victoria                       769057
Western Australia               77622

# Review of R3 (Claude, 19 October 2026)

Reviewed: the frozen R3 at commit 238b437 (`artefacts/editorial_20261018_r3/`;
the working tree is identical). This is an editor-first and specialist read,
answering Astra's three questions in board message 2049.

## Answers to the three questions

1. **Does the positive contribution now carry the paper?** Yes. A reader of
   the title, abstract, Fig. 1 and Section 3.2 learns something specific about
   Australia's estate: change sits at reserve margins and at a few sites, and
   those few sites set the sign of the national balance. That is the spark the
   18 September version lacked.
2. **Do the industrial examples illuminate the national result without
   dominating it?** Yes. They sit in one paragraph of 3.3 and support the
   influence result rather than replacing it. One gap: the abstract names
   Barrow Island and Murujuga without saying what they are, so an editor
   cannot see why they matter. Half a clause fixes this.
3. **Is any remaining objection consequential enough to change the
   manuscript?** Two are. The first is a new check that answers the main
   specialist objection to the Kosciuszko case. The second is a factual
   correction to the AI-use declaration. The rest are improvements.

## Consequential 1: Kosciuszko is not a detection-threshold artefact

R3 (in 4.2) says timing and concentration "do not exclude other processing
effects". Astra's point stands for faint pixels: a masking-threshold change
can act locally around existing sources. But the cached windows
(`kosciuszko_case_20261018.npz`; 39,721 common-valid inside cells) show that
most of the increase is far above the floor:

| Cells that brightened 2019→2024 | Cells | Share of positive change |
| --- | ---: | ---: |
| All (2024 value ≥ 10, the floor) | 642 | 100% |
| 2024 value ≥ 50 | 102 | 74.8% |
| 2024 value ≥ 100 (10 × floor) | 64 | 64.8% |
| 2024 value ≥ 200 (20 × floor) | 37 | 50.9% |

The median brightened cell sits at the floor (10): that is the faint halo, and
a detection change could create it. The maximum 2024 value is 610, against a
2019 maximum of 40 in the same window. Masking and quantisation operate at the
low end, so they cannot produce cells of 100 to 610 product units from
recorded zeros.

**Proposed replacement in 4.2**, for "That change alone cannot explain the
earlier observation, although timing and spatial concentration do not exclude
other processing effects.":

> That change cannot explain the earlier rise. Nor can changes in masking or
> quantisation, which act near the ten-unit floor: in 2024, 64 of the 642
> cells that brightened held values of at least 100 product units and supplied
> 65% of the park's positive change, with a maximum of 610. Faint cells around
> these sources could still reflect detection effects.

Add the table as a row block in S5 or Table S7. The figures come from the
cached arrays, so they need no new remote reads.

## Consequential 2: the AI-use declaration names the wrong Claude model for September

R3 says that the September–October revision "involved OpenAI Codex (GPT-6) and
Anthropic Claude (Opus 5.5)". Claude ran as two models:

- **Claude Fable 5.1** (`claude-fable-5-1`), 14–18 September 2026: the
  independent orientation review (the product-version concern, area
  weighting, footprint spillover and spectral points); the design of the
  first-detection and distance-stratified product audit, later amended by
  Astra; the review of the interior-band and area results; and the scientific
  close-out.
- **Claude Opus 5.5** (`claude-opus-5-5`), from 28 September 2026: the prose
  revision of the main text; checkpoint commits; and, on 18–19 October, the
  additive change budget, site-cluster analysis, candidate figures (the
  national contribution map and the concentration and rank panels), and the
  reviews of R1–R3.

**Proposed Claude sentence for the declaration:**

> Anthropic Claude contributed as Claude Fable 5.1 (14–18 September 2026:
> independent scientific review and design of the product-continuity audit)
> and Claude Opus 5.5 (from 28 September 2026: prose revision, the additive
> change budget and site-cluster analysis, candidate figures and manuscript
> critique).

Astra should state its own versions and roles in the same form. Barry's
standing instruction is to name systems and versions fully and specifically,
so this is not optional.

## Improvements (recommended, word-neutral overall)

### Abstract (about 275 words; replaces R3's 273)

Satellite night-lights can reveal change across a protected-area estate, but
reserve-wide averages obscure where change occurs and which places drive the
national total. Using annual VIIRS-derived observations for 2013–2024, we
estimated trends in area-integrated radiance separately for the outermost
kilometre and the deeper interior of each reserve in Australia's 2024
protected estate. Of 11,133 reserves, 4,426 (39.8%) had sufficient raster
support, together holding 99.8% of summed reserve area. The outermost
kilometre held 14% of their sampled area but 72% of the summed increase, and
even in reserves with measurable deeper interiors it held half the increase in
one-eighth of the area. Increases farther inward came largely from a few
reserves. In Kosciuszko National Park, the largest, two clusters near Snowy 2.0
pumped-hydro construction areas accounted for 96% of positive pixel change
between 2019 and 2024. Decreases were more concentrated still: five reserves
supplied 95%, and 90% came from Barrow Island and Murujuga, near
gas-processing facilities. These few reserves set the sign of the national
balance, which was negative for 2013–2021 and positive for 2013–2024, yet
positive in both periods once they were excluded. A mean-trend ranking placed
twelve of the twenty largest integrated contributors outside its top hundred.
Shared first-detection increases in 2017 and 2023 leave processing effects on
recent records unresolved, and all results describe a masked, quantised
satellite product rather than ground illumination or biological effects.
Separating boundary, interior and annual records turns a national trend into
specific places to investigate: the margins where most change occurs, and the
few sites that dominate the national balance.

Changes from R3: drops the 83% sensitivity (it stays in Results); names the
facility context for Barrow and Murujuga; states the sign change in plain
order; and ends on the two kinds of place instead of a general claim.

### One sentence on generality (4.1, after "connects it to inspectable site histories.")

> Global assessments that summarise protected-area brightening by reserve
> counts or area shares could test whether their totals are similarly
> concentrated in boundary zones and at a few sites. In Australia, the answer
> changes which places a monitoring programme would examine.

Offset the words by moving the two-sentence polygon-area paragraph at the end
of 3.3 to SI S4, since the additive budget has superseded it.

### Fig. 1 labels

The Barrow Island and Murujuga leader lines cross, and "Murujuga" sits on an
unrelated orange marker. Put Barrow Island's label to the west, Murujuga's
above its disc, and Thevenard Island's to the south-west. Optionally add four
faint capital-city labels (Perth, Sydney, Melbourne, Brisbane). The orange
fringes then read as urban margins without any text claim.

## Not consequential (no change needed)

- The title works. "Hotspots" is acceptable because the title says
  brightening and the Results name decreases separately.
- The industrial paragraph's qualifications (Thevenard's 2018–2019 values,
  Woodside's 2025 report lying outside the study period, "plausible
  operational explanations") are right and should stay.
- The word count (4,964) is close to the self-imposed 5,000 gate. RSEC's own
  limit should be confirmed from the Wiley author guidelines page before
  further trimming is forced. The edits above are roughly word-neutral.

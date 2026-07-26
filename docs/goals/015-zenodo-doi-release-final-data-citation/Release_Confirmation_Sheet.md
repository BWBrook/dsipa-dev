# Goal 015 Zenodo Release Confirmation

Status: **Draft created/uploaded, repaired, and re-previewed 2026-07-26; final
creator metadata matches the confirmed contract and Gate B is complete.
Publication remains unauthorized.**

## Recommended Defaults

| Field | Recommended value |
| --- | --- |
| Resource type | Dataset |
| Title | Australian protected-area dark-sky integrity outputs, 2013-2024 |
| Creator | Brook, Barry W. |
| ORCID | `0000-0002-2491-1517` - Barry to confirm |
| Creator count | Sole creator, unless Barry adds someone |
| Affiliation | School of Natural Sciences, University of Tasmania, Hobart, Tasmania, Australia |
| Version | `0.3.0` |
| Publication date | Actual date the record is first made public |
| Access | Open/public; no embargo |
| Licence | Creative Commons Attribution 4.0 International |
| Rights holder | University of Tasmania - presumptive; Barry must confirm applicability and release authority |
| Contributors | None by default |
| Zenodo community | None by default |
| Funding/grants | Blank unless Barry supplies exact metadata |
| File presentation | 12 flat, individually downloadable files in a separate ignored staging view: nine byte-identical payloads plus deposit-specific `README.md`, `manifest.json`, and `SHA256SUMS`; no ZIP unless the live service imposes a documented constraint |
| Related input identifier | `10.5281/zenodo.17294744` as `IsDerivedFrom`, if Zenodo supports that relation |
| Related manuscript DOI | None until one exists |
| Source repository | Private GitHub repository retained as local provenance only; do not enter it as a Zenodo public access link or public related identifier |
| Keywords | artificial light at night; protected areas; VIIRS; Australia; remote sensing; dark-sky integrity |

## Proposed Description

This dataset contains nine processed national Layer A outputs supporting a
detectability-aware assessment of artificial light at night inside and around
Australian protected areas for 2013-2024. It includes annual inside/buffer
radiance summaries, interior-ring profiles, buffer-validity descriptors,
trends, categorical screening output, protected-area descriptors/geometries,
IBRA assignments, and trend-bootstrap summaries.

Six files reproduce historical hashes exactly. Three are accepted non-exact:
the radiance CSV has no detected primary scientific drift but lacks direct
historical row-level proof; the edge-profile CSV contains an accepted small
threshold-sensitive difference, with current ring-1 feasibility
`1,432/12.9%`; and the GPKG has accepted within-run semantic identity but lacks
direct historical feature-level proof. All accepted primary scientific
headlines match. `pa_risk_rankings_v0_3_0.csv` is categorical screening
output, not a priority ranking. No raw or row-level ALA occurrence data and no
Layer B payload are included.

## Proposed Source Attribution

Derived outputs use CAPAD 2024 and IBRA 7.1 from the Australian Government
Department of Climate Change, Energy, the Environment and Water (CC BY 4.0);
OpenGeoHub/Zenodo VIIRS night-lights v0.4, source DOI
`10.5281/zenodo.17294744` (CC BY 4.0); and the Natural Earth public-domain land
mask. The final deposit README and description will retain source URLs,
versions, and attribution.

## Barry Must Confirm Or Amend

1. **Identity:** creator spelling/order, ORCID, exact affiliation, and whether
   Barry is the sole creator.
2. **Rights:** exact rights-holder wording. Recommended:
   `University of Tasmania`.
3. **Authority:** confirm this dataset falls under the applicable UTas policy
   and Barry has authority or approval to make it public under CC BY 4.0.
4. **Funding:** reply `none` or supply exact funder and grant metadata.
5. **Defaults:** approve or list amendments to title, description, version,
   access, licence, keywords, contributors, community, file presentation, and
   related identifiers.

If rights or authority cannot be confirmed, the release stops. This sheet is
not legal advice and does not require a legal-office process by default.

## Terse Reply

```text
Approve defaults; rights holder: University of Tasmania; I confirm this
dataset falls under the applicable UTas policy and I have authority/approval
to release it under CC BY 4.0; funding: none; authorize draft.
```

Or list amendments in the same reply.

`authorize draft` authorizes candidate revalidation, separate ignored flat
deposit staging, Zenodo draft creation, upload, draft inspection, and DOI
reservation only. It **never authorizes publication**. Publication requires a
later, separate instruction containing `publish` after Barry sees the exact
draft files and metadata.

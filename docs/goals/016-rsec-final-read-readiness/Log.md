# Log: Goal 016 RSEC Final-Read Readiness

## 2026-07-26 - Packet Creation

### Observed baseline

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD:
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`
- `origin/main`:
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`
- Starting status: clean (`## main...origin/main`)
- Goal 015: accepted, committed, pushed, and represented by the baseline above
- Goal 016 directory: absent before packet creation

### Observed local evidence

- RSEC target and article type:
  *Remote Sensing in Ecology and Conservation*, Original Research.
- Fixed title:
  **Detectable change in dark-sky integrity across Australia’s protected
  areas**
- Fixed period: `2013-2024`.
- Public Layer A data DOI:
  <https://doi.org/10.5281/zenodo.21524637>.
- `dsipa-dev` remains private.
- Current documented counts:
  - abstract `235`;
  - IMRAD plus Data accessibility `4,685`;
  - conservative abstract plus body `4,920`;
  - keywords `5`.
- Existing local reader assets:
  - main PDF `492,527` bytes;
  - main DOCX `421,505` bytes;
  - authoritative SI PDF `723,377` bytes.
- Existing diagnostic SI DOCX is not a submission or final-read asset.
- Table S1 contains exactly 20 rows in each of three categories:
  Inside brightening, Surrounding-only brightening, and
  Inside-minus-surrounding contrast.
- Fig. S2 and Fig. S3 captions require exact top-N disclosure.
- Current Layer B prose does not yet state clearly that each shuffle is one
  deterministic seeded realisation rather than a sampled null distribution.
- The manuscript currently distinguishes public Layer A data from private
  source, but the final-read package needs a clearer internal-versus-public
  reproducibility statement.
- No tracked build output exists at the packet baseline.

### Barry-provided authority and fixed decisions

- Barry approved preparation of a full final-read bundle.
- Submission or publication must wait for that read.
- Data, models, numerical results, title, period, DOI, categories, and Fig. 4
  placement are frozen.
- Exact top-N and single-shuffle transparency corrections are required.
- Only modest Layer B compression is permitted.
- Research funding is known as no specific funding.
- All other human-controlled fields remain unconfirmed.
- `dsipa-dev` must remain private.
- A curated clean-history public code repository plus a separate Zenodo
  Software record is the preferred later route, subject to separate Barry
  authorization.

### Current official-source evidence

Official Wiley/ZSL/RSEC sources were checked on 2026-07-26. Direct automated
fetches of the RSEC journal pages returned HTTP 403. Current official indexed
content, crawled within days, supplied the requirements summarized in
`Goal.md`; the live Research Exchange form was not accessed.

Current evidence supports the recorded word, abstract, keyword, structure,
spacing, line-numbering, running-title, component-count, title-page,
declaration, data-accessibility, figure, and SI requirements.

Observed uncertainties retained for later decision:

- live portal fields;
- exact ORCID/CRediT requirements;
- reviewer/editor requests;
- journal licence wording;
- APC/CAUL outcome;
- exact editorial application of the AI-assisted analytical-code policy.

### Executor inference

- The final-read bundle can be completed without resolving submission or
  public-release actions.
- A citable public code release is a material pre-submission decision,
  particularly if Barry confirms AI-assisted analytical code.
- This inference does not authorize code publication or establish exact
  journal-policy application.

### Packet mutation

Authorized packet paths only:

```text
docs/goals/016-rsec-final-read-readiness/Goal.md
docs/goals/016-rsec-final-read-readiness/Plan.md
docs/goals/016-rsec-final-read-readiness/Runbook.md
docs/goals/016-rsec-final-read-readiness/Log.md
```

No existing tracked file is authorized to change during packet creation.

### Actions not performed

No manuscript edit, data or analysis action, code or test change, build,
test, package, reader-bundle assembly, stage, commit, push, network login,
Wiley action, editor contact, public repository action, visibility change,
tag, GitHub release, Zenodo Software action, fee/APC action, open-access
agreement, or journal licence action occurred during packet authoring.

### Packet verification

- Exact footprint passed: the only worktree changes are the four untracked
  packet files listed above; there are no tracked or staged changes.
- The packet directory contains exactly those four Markdown files.
- `git diff --check` passed for the tracked diff, which is empty at this
  packet-authoring stage.
- A direct trailing-whitespace scan of all four untracked files returned no
  hits.
- A targeted contract scan confirmed the required top-20/top-15 definitions,
  single-seeded-realisation wording, counts, human funding draft, decision
  documents, validation ladder, governance updates, acceptance gate, and
  no-submission/no-public-action boundary.
- No build or test was run, as required for packet authoring.

## Future Execution Logging Contract

Append a dated checkpoint after execution. Separate:

1. observed Git and evidence state;
2. Barry-provided decisions;
3. executor inference;
4. exact files changed;
5. top-N and single-shuffle corrections;
6. before/after word counts;
7. tests, builds, citation/lint checks, and scans;
8. provenance, text, and visual QA;
9. reader-bundle names, sizes, and SHA-256 values;
10. focused repair count;
11. unresolved human/public/live-workflow gates;
12. orchestrator acceptance and exact-path Git closeout; and
13. explicit confirmation that no Wiley or public-release action occurred.

Do not record credentials, private account identifiers, tokens, cookies,
emails beyond approved manuscript correspondence metadata, or other
authentication state.

## 2026-07-26 - Execution And Final-Read Candidate

### Observed baseline

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- Starting HEAD and `origin/main`:
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`
- Accepted Goal 015 baseline ancestor check: pass.
- Starting status: only the accepted four untracked Goal 016 packet files.
- `build/final_read/goal016/`: absent before assembly.

### Barry-provided decisions applied

- Science, title, `2013-2024`, DOI, Fig. 4 placement, categories, numbers,
  models, table cells, and figure pixels remained frozen.
- Table S1/Figs S2-S3 and shuffle transparency corrections were applied.
- Layer B compression remained modest.
- Funding draft is exactly `No specific funding.`
- Every other human field remains visibly unresolved.
- `dsipa-dev` remains private.
- The preferred later code route is documented but not executed.

### Executor changes

Direct scientific-reading surfaces:

```text
manuscript/text/manuscript_draft.md
manuscript/text/figures.md
manuscript/text/supplementary_tables.md
manuscript/text/supplementary_figures.md
```

RSEC final-read surfaces:

```text
manuscript/submission/rsec/README.md
manuscript/submission/rsec/submission_checklist.md
manuscript/submission/rsec/submission_metadata.md
manuscript/submission/rsec/submission_counts.md
manuscript/submission/rsec/declarations_draft.md
manuscript/submission/rsec/cover_letter_draft.md
manuscript/submission/rsec/supplementary_frontmatter.md
manuscript/submission/rsec/final_read_guide.md
manuscript/submission/rsec/code_release_decision.md
manuscript/submission/rsec/figure_production_inventory.md
```

Governance/chronology surfaces:

```text
docs/stage4_manuscript_release_plan.md
docs/stage_overview.md
docs/log/136_rsec_final_read_readiness.md
docs/goals/016-rsec-final-read-readiness/Log.md
```

The pre-existing Goal 016 `Goal.md`, `Plan.md`, and `Runbook.md` packet files
remain part of the accepted untracked packet but were not changed during
execution.

### Transparency and compression

- Table S1: top 20 per category, with descending point-estimate
  `inside_slope`, `buffer_1km_slope`, and `retention_1km` rules stated;
  `retention_1km` is defined as inside minus 1 km surrounding slope.
- Fig. S2: top 20 by bootstrap-median inside slope.
- Fig. S3: top 15 pairwise-ordering set.
- Layer B: each shuffle is one deterministic seeded illustrative realisation,
  not a sampled null distribution or causal counterfactual.
- Reproducibility: internal versioned/scripted/tested/pinned/manifest-backed
  state is separated from the public processed Layer A Dataset and private
  software/Layer B route.
- Layer B-facing prose: 1,262 before, 1,194 after, net `-68`.

### Counts

| Component | Count |
| --- | ---: |
| Abstract | 234 |
| IMRAD | 4,565 |
| IMRAD plus Data accessibility | 4,649 |
| Declaration content excluding acknowledgements | 34 |
| Acknowledgements placeholder | 3 |
| Conservative abstract plus all body/declaration markers | 4,947 |
| Rendered references | 454 |
| Main/SI table source | 551 / 2,316 |
| Main/SI figure-legend source | 498 / 406 |
| Keywords | 5 |
| Running title characters | 34 |

The conservative count is below 5,000. Its inclusion of all declaration and
acknowledgement markers avoids hiding uncertainty about live-workflow
treatment.

### Validation and build evidence

- Focused RSEC/provenance tests: 13 passed.
- Full `make test`: 83 passed and 9 expected skips for ignored national
  outputs.
- `draft`, `submission`, and `supplementary` `ms-check` and `ms-build`: pass.
- Makedoc tests: 61 per profile; manuscript lint and author injection pass.
- Main/draft audit: 31 bibliography keys, 25 cited, zero unknown, six
  non-fatal unused.
- SI audit: zero cited, zero unknown, 31 consequently unused/non-fatal.
- Build provenance: DSIPA
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`, `main`, dirty as expected;
  Makedoc `3a52e7059fb069c854b49d8f0a1991aface33d75`, `main`, clean.
- Submission-manifest manuscript input hash equals the current source hash.
- Count, title, period, DOI, top-N, shuffle, funding, reproducibility,
  ranking/causal-boundary, Fig. 4 placement, and `git diff --check` gates pass.
- The orchestrator-triggered repair reran only
  `make PROFILE=supplementary ms-check` and
  `make PROFILE=supplementary ms-build`; both passed, including 61 Makedoc
  tests, manuscript lint, reference audit, author injection, and build
  checks. Exact semantic scans, four-file bundle identity/count checks, and
  `git diff --check` also passed.

The first focused repair added compact funding and unresolved declaration end
matter to the main manuscript after first rendered-text QA showed those fields
were absent from the reader PDF. A second, orchestrator-triggered repair
followed new rendered evidence: Fig. 4's frozen internal title still uses the
legacy word `falsification`, while the accepted manuscript treats both
shuffles as single illustrative benchmarks. The bounded repair changed only
the Table S2 title, final-read residual guidance, figure-production inventory,
these two Goal 016 logs, and ignored SI/bundle copies. No figure pixel, source,
analysis, datum, result, table row, or table cell changed. Repair count: two
total - one executor repair and one orchestrator-triggered repair.

### Text and visual QA

- Main PDF: 28 pages; title, abstract, Data accessibility, declarations,
  Table 1, references, Fig. 4 caption, and Fig. 4 inspected.
- Main DOCX: LibreOffice render is 37 pages; the same reader surfaces pass.
- Authoritative SI PDF: 14 pages; frontmatter, Tables S1-S2, Figs S2-S3
  captions/images, landscape tables, portrait restoration, and labels pass.
  Rebuilt SI page 4 shows the revised Table S2 `illustrative benchmarks` title
  fully legible with no overlap or clipping.
- No overlap, clipping, unintended placeholder leakage, or stale public-code
  claim found.

Optional contact-sheet assembly was stopped after two unchanged ImageMagick
font-resolution failures. Individual 120 dpi page renders supplied fresh
visual evidence; this did not affect acceptance.

### Frozen-content and footprint proof

- Table-row SHA-256 unchanged:
  `27d2b9f3a2dd7c4354351a63dd82483f96c90a7f3e9e3553597b2f267e98b632`.
- Main Table 1, all 11 scientific PNGs, `references/refs.yaml`, and
  `settings/build.yaml` hashes are unchanged.
- Fig. 4 occurs once in the main figure source and zero times in SI.
- No prohibited source, test, data, analysis, settings, reference, artefact,
  or GitHub path changed.
- Fig. 4's frozen pixels remain unchanged for this final-read candidate. Its
  caption and manuscript interpretation control: the two shuffles are
  illustrative benchmarks, not a falsification design. Reproducible removal
  of the internal legacy `falsification` label is a required pre-submission
  production gate after the preserved Layer B snapshot or an independently
  verified summary-only rendering path is available.

### Four-file reader bundle

Ignored local path: `build/final_read/goal016/`

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `dsipa_rsec_final_read_main.docx` | 421,858 | `983ad7c31bea3c6d5548898cf2a366b591f936dcd27783102d2646173fc5948f` |
| `dsipa_rsec_final_read_main.pdf` | 496,322 | `9a9c0159e4d26aa7184a177c80f6a93376a1df778ccf0f5f2829953ddd5ca29a` |
| `dsipa_rsec_final_read_supporting_information.pdf` | 724,893 | `13b64c16c3be6e89b52ffbc80ee4aa8d4de88e287544324e0062962e94cf5bf2` |
| `final_read_guide.md` | 4,109 | `7342b0b6d208a43225f7d5154584c07881c1b3be861e609a147413cc841b508c` |

Exactly four files are present. The diagnostic SI DOCX is absent and the
bundle remains ignored.

### Remaining decisions and actions not performed

Open Barry decisions: author list/order, affiliations/ORCIDs, corresponding
author/contact, contributions, acknowledgements, conflicts, ethics, exact
AI-use disclosure, all-author approval, sole submission, public code/Layer B
route, live workflow, fee/APC, journal licence, final authority, and optional
cover image. Fig. 4's internal legacy `falsification` title must also be
replaced reproducibly before submission; it is not optional production polish.

No Wiley login, upload, submission, editor contact, public code/data action,
visibility change, Zenodo Software action, fee/APC action, licence choice,
tag, release, stage, commit, push, or other external/public mutation occurred.

## 2026-07-26 - Orchestrator Acceptance

The orchestrator independently reviewed and **ACCEPTED** Goal 016 for Barry's
final read and authorized exact-path Git closeout. This is local-readiness
acceptance only; it does not authorize Wiley submission or public release.

Root verification confirmed:

- focused tests: 13 passed;
- full suite: 83 passed and 9 expected skips;
- submission `ms-check`: green;
- main PDF, rendered DOCX, and SI PDF: visually reviewed;
- the acceptance repair: documented; and
- the exact tracked diff and ignored four-file bundle: checked.

At this checkpoint, the authorized stage, commit, and push had not yet
occurred. No Wiley, public-release, or other external action occurred.

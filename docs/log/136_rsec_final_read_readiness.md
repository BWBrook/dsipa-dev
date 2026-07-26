# 136 - RSEC Final-Read Readiness

Date: 2026-07-26

## Conclusion

Goal 016 prepared a decision-ready, explicitly non-submission-ready RSEC
final-read bundle. The manuscript remains Layer A-centred, Fig. 4 remains in
the main text, and no data, model, number, table cell, figure pixel, title,
period, DOI, or scientific conclusion changed.

On 2026-07-26, the orchestrator independently reviewed and **ACCEPTED** Goal
016 for Barry's final read and authorized exact-path Git closeout. This is
local-readiness acceptance only; the authorized commit and push have not yet
occurred, and it does not authorize Wiley submission or public release.

## Baseline

- Repository: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- Starting HEAD and `origin/main`:
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`
- Accepted Goal 015 baseline remained an ancestor.
- Starting worktree change: only the accepted four-file Goal 016 packet.

## Bounded Changes

- Table S1 discloses top 20 within each category and the exact
  `inside_slope`, `buffer_1km_slope`, and `retention_1km` ordering metrics.
- Fig. S2 discloses top 20 by bootstrap-median inside slope.
- Fig. S3 discloses the top 15 pairwise-ordering set.
- Each Layer B shuffle is one deterministic seeded illustrative realisation,
  not a sampled null distribution or causal counterfactual.
- Repeated Layer B caveats were compressed without changing design, results,
  limitations, or Fig. 4.
- Internal versioned/scripted/tested/pinned/manifest-backed state is separated
  from the public Layer A Dataset and not-yet-public software/Layer B route.
- The main manuscript now displays `No specific funding.` and unresolved
  declaration markers for Barry's complete read.
- Final-read, code-release, and figure-production decision documents were
  created.

Layer B-facing prose changed from 1,262 to 1,194 words: a net reduction of 68,
within the 250-word bound.

## Counts

| Component | Goal 016 count |
| --- | ---: |
| Abstract | 234 |
| IMRAD | 4,565 |
| IMRAD plus Data accessibility | 4,649 |
| Declaration content excluding acknowledgements | 34 |
| Acknowledgements placeholder | 3 |
| Conservative abstract plus all body/declaration markers | 4,947 |
| Rendered references | 454 |
| Main table source | 551 |
| SI table source | 2,316 |
| Main figure-legend source | 498 |
| SI figure-legend source | 406 |
| Keywords | 5 |
| Running title characters | 34 |

The 4,947 conservative count is below 5,000. Declaration treatment in the live
workflow remains unconfirmed, so the conservative count includes every
current marker.

## Validation

- Focused provenance/RSEC tests: 13 passed.
- Full `make test`: 83 passed, 9 expected skips for ignored national outputs.
- `draft`, `submission`, and `supplementary`: `ms-check` and `ms-build` passed.
- Each profile ran 61 Makedoc tests; manuscript lint and author injection
  passed.
- Main/draft reference audits: 31 bibliography keys, 25 cited, zero unknown,
  six non-fatal unused.
- SI reference audit: zero cited, zero unknown; all 31 bibliography entries
  are consequently unused and non-fatal.
- Submission manifest input hash for `manuscript_draft.md` matches the current
  source.
- All manifests record DSIPA source
  `4f5e2228511b9d495c2523ddc34a0efea9d7046c`, branch `main`, dirty as expected;
  Makedoc is clean at
  `3a52e7059fb069c854b49d8f0a1991aface33d75`.
- Exact title, `2013-2024`, DOI, top-N, shuffle, funding, public/private,
  ranking, causal-boundary, and Fig. 4 placement scans passed.
- `git diff --check` passed.
- The orchestrator-triggered repair reran only
  `make PROFILE=supplementary ms-check` and
  `make PROFILE=supplementary ms-build`; both passed, including 61 Makedoc
  tests, manuscript lint, reference audit, author injection, and build
  checks. Exact semantic scans and four-file bundle identity/count checks also
  passed.

The first focused repair added the funding and unresolved declaration section
to the main reader source after initial rendered-text QA showed those fields
were present only in side documents. A second, orchestrator-triggered repair
followed new rendered evidence: Fig. 4's frozen internal title still uses the
legacy word `falsification`, while the accepted manuscript treats both
shuffles as single illustrative benchmarks. The bounded repair changed only
the Table S2 title, final-read residual guidance, figure-production inventory,
these two Goal 016 logs, and ignored SI/bundle copies. No figure pixel, source,
analysis, datum, result, table row, or table cell changed. Repair count: two
total - one executor repair and one orchestrator-triggered repair.

## Reader QA

- Main PDF: 28 pages, fresh text extraction and visual inspection passed.
- Main DOCX: fresh LibreOffice rendering produced 37 pages; title, abstract,
  Data accessibility, declarations, Table 1, references, Fig. 4 caption, and
  Fig. 4 passed visual inspection.
- Authoritative SI PDF: 14 pages; frontmatter, Tables S1-S2, Figs S2-S3
  captions and images, landscape readability, portrait restoration, and
  labels passed. Rebuilt SI page 4 shows the revised Table S2 `illustrative
  benchmarks` title fully legible with no overlap or clipping.
- No overlap, clipping, unintended placeholder leakage, or stale public-code
  claim was found.

An optional contact-sheet helper was stopped after two unchanged ImageMagick
font-resolution failures. Individual 120 dpi page renders supplied the visual
evidence, so this was not a validation defect.

## Frozen-Content Proof

- Table S1/S2 Markdown-row SHA-256 remained
  `27d2b9f3a2dd7c4354351a63dd82483f96c90a7f3e9e3553597b2f267e98b632`.
- Main Table 1 SHA-256 remained
  `0b7b9463b8a5eee81cc269b6521b0605ef717a2af53a53dd760d535a14fafebe`.
- All 11 scientific PNG hashes remained unchanged.
- `references/refs.yaml` remained
  `9e07b8b7e39155d6af4a497b8e3a62262a6c92c4bb915e70c353f05b0358314b`.
- `settings/build.yaml` remained
  `4c245c44a82cb92db7c9625e64142ee66dac94e52b61818131f1aa355939cfa2`.
- Final tracked diff contains no prohibited source, test, data, analysis,
  settings, reference, artefact, or GitHub path.
- Fig. 4's frozen pixels remain unchanged for this final-read candidate. Its
  caption and manuscript interpretation control: the two shuffles are
  illustrative benchmarks, not a falsification design. Reproducible removal
  of the internal legacy `falsification` label is a required pre-submission
  production gate after the preserved Layer B snapshot or an independently
  verified summary-only rendering path is available.

## Four-File Reader Bundle

Ignored local path: `build/final_read/goal016/`

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `dsipa_rsec_final_read_main.docx` | 421,858 | `983ad7c31bea3c6d5548898cf2a366b591f936dcd27783102d2646173fc5948f` |
| `dsipa_rsec_final_read_main.pdf` | 496,322 | `9a9c0159e4d26aa7184a177c80f6a93376a1df778ccf0f5f2829953ddd5ca29a` |
| `dsipa_rsec_final_read_supporting_information.pdf` | 724,893 | `13b64c16c3be6e89b52ffbc80ee4aa8d4de88e287544324e0062962e94cf5bf2` |
| `final_read_guide.md` | 4,109 | `7342b0b6d208a43225f7d5154584c07881c1b3be861e609a147413cc841b508c` |

The bundle contains exactly four files. The diagnostic SI DOCX is absent and
the ignored bundle must not be staged.

## Orchestrator Acceptance

Root verification confirmed focused tests at 13 passed; the full suite at 83
passed and 9 expected skips; a green submission `ms-check`; visual review of
the main PDF, rendered DOCX, and SI PDF; the documented acceptance repair; and
checks of the exact tracked diff and ignored four-file bundle.

The orchestrator's 2026-07-26 acceptance is for local readiness and Barry's
final read only. Exact-path Git closeout was authorized but had not yet
occurred. No Wiley, public-release, or other external action occurred.

## Remaining Decisions And Boundary

Barry must still confirm authorship/order, affiliations/ORCIDs,
correspondence, contributions, acknowledgements, conflicts, ethics, exact AI
use, all-author approval, and sole submission. Barry must also decide whether
to authorize the preferred later curated clean-history public code repository
plus separate Zenodo Software record, or retain private code and seek
editorial guidance.

The live workflow, APC/fee, journal licence, final submission authority, and
optional cover image remain later gates.

Fig. 4's internal legacy `falsification` title must be replaced reproducibly
before submission. This semantic correction is required production work, not
optional polish.

No Wiley login, upload, submission, editor contact, public code/data action,
repository visibility change, Zenodo Software action, fee/APC action, licence
choice, tag, release, staging, commit, push, or other external mutation
occurred.

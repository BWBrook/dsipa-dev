# Log: Goal 014 RSEC Release Candidate — Option B Archive

## 2026-07-24 — Orchestrator packet creation

- Starting action-repo state:
  - branch: `main`;
  - HEAD and `origin/main`:
    `f5788ea4ad62237a95bf323930ec477107e7c2f3`;
  - status: clean before packet creation.
- Goal 014 was scoped as one final pre-publication candidate combining
  accepted Goal 011 Option B archive recovery, current release reconciliation,
  DSIPA/Makedoc dual provenance, and RSEC submission assets.
- The hard archive contract fixes the read-only `deep-server-ts` source, the
  ignored local destination, exactly nine Goal 010 payloads, total size
  `265,783,139` bytes, Goal 011 hashes/classifications, six exact files, and
  accepted radiance/edge/GPKG limitations.
- The packet preserves the active `1,432/12.9%` value and historical `1,427`
  only in reconciliation records, excludes raw/row-level ALA, and treats the
  legacy risk-rankings filename as categorical screening rather than priority.
- The packet requires DSIPA-owned Makedoc provenance annotation with
  success-only refresh and failure propagation, plus TDD and full tests.
- The packet fixes the accepted RSEC title and Original Research type, a
  main-only submission profile, a supplementary profile, and explicit
  Barry-confirmation markers for human and rights decisions.
- External actions remain blocked: no Zenodo draft/upload, DOI reservation or
  mint, Git tag/release, Wiley login/submission, fees, OA agreement, commit,
  or push.
- No goal execution, network access, data copy, test, build, manuscript,
  analysis, data, release, or external action occurred during packet creation.
- Pending executor implementation and orchestrator acceptance.

## 2026-07-24 — Executor start and contract reconstruction

- Confirmed the exact authorized baseline before mutation:
  - `pwd`: `/Users/bwbrook/papers/dsipa-dev`;
  - branch: `main`;
  - HEAD and `origin/main`:
    `f5788ea4ad62237a95bf323930ec477107e7c2f3`;
  - status: `## main...origin/main` plus only the untracked Goal 014 packet.
- Read repo-local `AGENTS.md`, then Goal 014 `Goal.md`, `Plan.md`,
  `Runbook.md`, and this log in the required order.
- Read all Goal 010-013 packet and closeout records, the Layer A reference
  contract, Goal 011 preservation manifest/reconciliation, active release
  reports, release/licence evidence, Makedoc wrapper/configuration, upstream
  manifest contract, manuscript assembly, and build entry points.
- Reconstructed the fixed release state:
  - Goal 011 is the authoritative accepted nine-file archive candidate;
  - its payload totals `265,783,139` bytes;
  - six files are historically exact;
  - radiance, edge-profile, and GPKG limitations remain explicit;
  - active release surfaces must use ring-1 `1,432/12.9%`; and
  - Goal 010 remains a blocked historical staging record.
- Checked the four canonical official sources on 2026-07-24. The Zenodo pages
  confirmed the draft/upload/metadata lifecycle and that DOI registration
  occurs only on publication; the reserve-DOI action remains blocked. The
  canonical Wiley RSEC URL returned a direct 403 to the read-only fetch, but
  its current indexed canonical content confirmed Original Research,
  5,000-word, 300-word abstract, 4-6 keyword, double-spacing, continuous
  line-numbering, running-title, count, cover-letter, declaration, data
  accessibility, Supporting Information, AI-disclosure, conflict, sole-
  submission, fee, and open-access requirements.
- No remote filesystem access, data copy, test, build, source edit, manuscript
  edit, external archive action, DOI action, Wiley action, commit, or push had
  occurred at this checkpoint.

## 2026-07-24 — Archive recovery and release reconciliation

- Read-only rsync source listing at the exact Goal 011 payload path showed
  exactly the approved nine-file `data/processed/` allowlist and total size
  `265,783,139` bytes.
- Recovered only those nine files through explicit rsync include filters into
  ignored
  `artefacts/optionB_layerA_archive_candidate_2026-07-24/`.
- Independent destination comparison against
  `analysis/reports/layerA_preservation_manifest_2026-07-23.json` passed for
  all nine paths, byte sizes, Goal 011 SHA-256 values, and total bytes.
  `data/processed/` was not touched.
- Added the only three permitted candidate companions: `README.md`,
  `manifest.json`, and `SHA256SUMS`.
- Candidate validation passed:
  - 9 payload files and 12 files total;
  - 9/9 checksum verification;
  - 6 exact and 3 accepted non-exact classifications;
  - exact Goal 011 and Goal 012 reference-contract classifications retained;
  - raw/row-level ALA and all Layer B/unlisted payloads excluded.
- Reconciled active release surfaces to current ring-1 `1,432/12.9%`.
  Historical `1,427` remains only in explicit Goal 011/012 reconciliation.
- Replaced the stale final release manifest with a current local-candidate
  surface, created dated Option B Markdown/JSON manifest, Zenodo metadata, and
  checklist reports, and narrowly updated data, decisions, and stage pointers.
- Goal 010 remains an explicit blocked historical record. No archive/DOI
  existence is claimed, and the risk-rankings legacy filename is described as
  categorical screening output rather than a priority order.
- No Zenodo draft/upload, DOI reservation/minting, Git tag/release, Wiley
  login/submission, fee/OA agreement, commit, or push occurred.

## 2026-07-24 — Provenance TDD and RSEC production assets

- Added the focused provenance tests before implementation. The first run was
  red as expected: successful `check`/`all` did not refresh provenance and a
  missing successful-build manifest did not fail closed.
- Added one DSIPA-owned annotator and one minimal wrapper hook. No upstream
  Makedoc file was changed.
- Focused provenance tests then passed: `5 passed`.
- The tests prove:
  - successful `check` and `all` annotation;
  - refresh when upstream leaves an existing manifest unchanged;
  - preservation of upstream top-level `git` as Makedoc identity;
  - distinct DSIPA source and Makedoc build-tool SHA/branch/dirty fields;
  - exact upstream failure propagation and byte-identical no-annotation;
  - no annotation for successful non-build targets; and
  - fail-closed behavior when a successful build manifest is absent.
- Updated only `settings/build.yaml` for build profiles:
  - combined `draft` remains 1.5-spaced;
  - `submission` is main-only, double-spaced, continuously line-numbered,
    outputs under `build/submission`, stem `dsipa_rsec_main`;
  - `supplementary` is SI-only and PDF-authoritative, with compact landscape
    tables between portrait frontmatter and figures, outputs under
    `build/supplementary`, stem `dsipa_rsec_supplementary`.
- Added nine bounded RSEC assets under `manuscript/submission/rsec/`.
  Human-owned authorship, contributions, affiliations/ORCIDs, rights/licence,
  date/version, funding, conflict, AI, sole-submission, correspondence,
  ethics/consent applicability, DOI/URL, fee/OA, and final authorization fields
  are visibly marked for Barry confirmation.
- Kept `manuscript/authors.yaml` unchanged for the working draft. The
  submission profile uses a separate placeholder-only author file so its PDF
  and DOCX assert no author, order, affiliation, ORCID, or corresponding
  author before Barry confirms them.
- Reproduced accepted counts from unchanged manuscript/display sources:
  abstract 235; IMRAD 4,609; IMRAD plus Data accessibility 4,683; 5 keywords;
  4/1 main figures/tables; 7/2 SI figures/tables; proposed running title 34
  characters.
- No manuscript science, table cell/value/header/label/prose, reference,
  figure caption/path/image, working author metadata, upstream Makedoc, commit,
  push, or external submission/archive state changed. Layout-only source edits
  are three table delimiters and seven figure-width attributes.

## 2026-07-24 — Final validation and focused repair

- Final focused provenance and submission-contract tests passed: `13 passed`.
- Full repository tests passed: `83 passed, 9 skipped`; each skip is the
  expected absence of national outputs from `data/processed/`, which remained
  untouched.
- Draft, submission, and supplementary `ms-check`/`ms-build` commands passed.
  Each check included 61 upstream Makedoc tests, config validation, manuscript
  lint, zero unknown citation keys, author-metadata checks, build validation,
  and success-only DSIPA provenance annotation.
- Exact candidate revalidation passed:
  - 9 payload files, 12 files total, and `265,783,139` payload bytes;
  - all 9 `SHA256SUMS` entries passed;
  - 6 historical exact files and 3 accepted non-exact files;
  - zero raw/row-level ALA, Layer B, or unlisted payload paths.
- All five generated candidate/build JSON documents passed
  `python3 -m json.tool`. `jq` assertions proved distinct DSIPA source and
  upstream Makedoc tool identities in all three build manifests.
- Counts remained exact: abstract 235; IMRAD 4,609; IMRAD plus Data
  accessibility 4,683; 5 keywords; 4/1 main and 7/2 SI displays; 34-character
  proposed running title.
- Independent review found two production defects in the initial candidate:
  the SI PDF/DOCX tables were unreadable, and main PDF/DOCX asserted
  unconfirmed Barry W. Brook/University of Tasmania authorship.
- The bounded acceptance repair kept the working author file unchanged,
  introduced visible submission placeholders, and made the SI PDF
  authoritative. A local deterministic PDF-layout extender adds
  `pdflscape`; two SI-table formatting-only Markdown delimiter rows assign
  reviewed colspecs, and a separate closing source returns figures to portrait.
- Pandoc AST comparison after normalizing only `colspec` had the identical
  SHA-256 `77628867bdff41861f16f6e4476be8017006d817a221d62b9823e634ac4b3de0`
  before and after. No table caption, header, cell, value, order, alignment,
  label, or prose changed.
- The final SI is 14 A4 pages: page 1 portrait, pages 2-5 landscape tables,
  and pages 6-14 portrait captions/figures. Native-resolution review covered
  every page and found no collision, clipping, one-word table fragmentation,
  overlap, blank/missing figure, or masked `Fig. S1.`-`Fig. S7.` label. S1-S5
  and S7 use 85% widths; the targeted S6 fallback uses 80%.
- Main PDF/DOCX text exports contain six visible `[BARRY CONFIRM]` markers and zero
  `Barry W. Brook` or `University of Tasmania` strings. LibreOffice opened the
  main DOCX, and its rendered first page is readable without overlap. Main
  Table 1 uses the shared `22, 10, 16, 11, 23, 18%` width vector and passed
  complete visual review in PDF pages 17-19 and LibreOffice pages 23-27.
- The autogenerated SI DOCX still opens, but its LibreOffice rendering is 32
  pages with severe header/cell fragmentation. It is now explicitly
  diagnostic, non-submittable, and absent from submission metadata/assets.
- Pandoc re-import returned the same non-decisive diagnostic for all three
  DOCX files: exit 63, `couldn't parse docx file: DocxError`. ZIP/XML and
  LibreOffice openability show the files are containers; this does not
  override the separate visual finding that SI DOCX is unsuitable.
- Main/SI separation passed: the main file contains the exact title and
  Abstract, no SI content/assets/definitions, and the legitimate manuscript
  cross-references to SI. The SI contains the exact title, Supporting
  Information, Tables S1-S2, and Figs S1-S7, with no main Abstract,
  Introduction, Table 1 content/assets/definition, or main-figure assets.
- Active denominator scans found no stale value in the two primary active
  reports. Three `1,427` hits remain only in explicit historical
  Goal 011/012 reconciliation statements; active evidence is
  `1,432/12.9%`.
- Table 1 and SI-figure normalized source identities remained exact after
  omitting only `colspec` or width values:
  `5878534ee812462312c7e07e53908a7756b0a7f75500817ac2168b5462511ed0`
  and `47e5b13e0b930d8d542ba09bcb9d0367defefc926a7ed3f81fd4c9240a9e7887`.
- `bash -n`, Python compilation, `git diff --check`, candidate allowlist,
  external-state, and exact 34-path mutation-footprint checks passed. Upstream
  Makedoc remained clean at
  `3a52e7059fb069c854b49d8f0a1991aface33d75`.
- No Zenodo draft/upload, DOI reservation/minting, Git tag/release, Wiley
  login/submission, fee/OA agreement, commit, or push occurred.

# Runbook: Goal 016 RSEC Final-Read Readiness

Run all commands from:

```text
/Users/bwbrook/papers/dsipa-dev
```

This runbook authorizes local bounded edits, validation, reader-bundle
assembly, and exact-path Git closeout only after orchestrator acceptance. It
does not authorize Wiley or public-release actions.

## Baseline Gate

Record:

```bash
pwd
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git status --short --branch
git log --oneline --decorate -5
git merge-base --is-ancestor \
  4f5e2228511b9d495c2523ddc34a0efea9d7046c HEAD
```

Required packet-authoring baseline:

```text
pwd = /Users/bwbrook/papers/dsipa-dev
branch = main
HEAD = origin/main = 4f5e2228511b9d495c2523ddc34a0efea9d7046c
status = ## main...origin/main
```

At later execution, an accepted packet-only commit is permitted. Every other
change must be explained and fall inside Goal 016. Stop for divergence,
unrelated work, an unexplained untracked file, or a baseline that does not
descend from the accepted Goal 015 state. Never reset, clean, stash, overwrite,
or absorb another person's work.

## Read First

Read:

```text
AGENTS.md
docs/goals/016-rsec-final-read-readiness/Goal.md
docs/goals/016-rsec-final-read-readiness/Plan.md
docs/goals/016-rsec-final-read-readiness/Runbook.md
docs/goals/016-rsec-final-read-readiness/Log.md
manuscript/text/manuscript_draft.md
manuscript/text/figures.md
manuscript/text/supplementary_tables.md
manuscript/text/supplementary_figures.md
manuscript/submission/rsec/README.md
manuscript/submission/rsec/submission_checklist.md
manuscript/submission/rsec/submission_metadata.md
manuscript/submission/rsec/submission_counts.md
manuscript/submission/rsec/declarations_draft.md
manuscript/submission/rsec/cover_letter_draft.md
manuscript/submission/rsec/supplementary_frontmatter.md
settings/build.yaml
docs/stage4_manuscript_release_plan.md
docs/stage_overview.md
```

`settings/build.yaml` is read-only in Goal 016. Do not change build profiles to
make an output pass.

## Record Before Editing

Capture the exact current selection and claim surfaces:

```bash
rg -n -C 3 \
  'Table S1|Table S2|top|screen|category|median|bootstrap|rank' \
  manuscript/text/supplementary_tables.md \
  manuscript/text/manuscript_draft.md

rg -n -C 3 \
  'Fig\. S2|Fig\. S3|shuffle|seed|realis|realiz|null|bootstrap|median|top' \
  manuscript/text/supplementary_figures.md \
  manuscript/text/figures.md \
  manuscript/text/manuscript_draft.md

awk -F'|' \
  '/^\|/ && $2 !~ /category|---/ {
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2)
    print $2
  }' manuscript/text/supplementary_tables.md |
  LC_ALL=C sort |
  uniq -c
```

The category inventory must show exactly:

```text
20 Inside brightening
20 Inside-minus-surrounding contrast
20 Surrounding-only brightening
```

Ignore the four Table S2 design-label rows when checking the Table S1
inventory.

## Transparency Edit Contract

### Table S1

Edit explanatory prose only. Use wording that unambiguously records:

```text
Inside brightening:
top 20 by descending point-estimate inside_slope

Surrounding-only brightening:
top 20 by descending point-estimate buffer_1km_slope

Inside-minus-surrounding contrast:
top 20 by descending point-estimate retention_1km
where retention_1km = inside_slope - buffer_1km_slope
```

Retain:

```text
screening display
source order
not management priority
not competitive ranking
```

Do not edit a table delimiter, row, cell, value, category, or `source_order`.

### Figures S2 And S3

Edit captions only:

```text
Fig. S2 = top 20 by bootstrap-median inside slope
Fig. S3 = top 15 used for pairwise bootstrap ordering frequencies
```

Retain the uncertainty, overlapping-interval, non-posterior, and non-ranking
interpretation. Do not edit image paths, width attributes, or image files.

### Layer B shuffles

Use one compact sentence consistently where needed:

```text
Each shuffle benchmark is one deterministic seeded realisation used as an
illustrative benchmark, not a sampled null distribution.
```

Also preserve:

```text
no causal counterfactual
attenuation does not distinguish biological from observational explanation
provider-bounded observation process
```

Required review surfaces are:

- Methods 2.6;
- the directly corresponding Results/Discussion sentences;
- Table S2 explanatory text; and
- Fig. 4 caption.

Do not describe `AUC 0.505` or `AUC 0.517` as a null distribution, repeated
simulation, empirical null interval, or probability statement.

### Modest Layer B compression

Before and after editing, count the Layer B-facing prose:

```bash
awk '
  /^### 2\.5 / {in_layer_b=1}
  /^### 2\.7 / {in_layer_b=0}
  /^### 3\.4 / {in_layer_b=1}
  /^## 4\. Discussion/ {in_layer_b=0}
  /^### 4\.3 / {in_layer_b=1}
  /^### 4\.5 / {in_layer_b=0}
  in_layer_b
' manuscript/text/manuscript_draft.md | wc -w
```

Treat this as a reproducible comparison, not a journal component count. Remove
only repetition. Stop if more than 250 net words would be removed or any
number, design feature, caveat, or Fig. 4 placement would change.

### Reproducibility

The manuscript and RSEC surfaces must separately state:

```text
internal:
versioned + scripted + tested + pinned + manifest-backed

public:
Layer A processed outputs at 10.5281/zenodo.21524637

not yet public:
source code + complete Layer B reproduction route + citable software release
```

Never call the Zenodo Dataset a software record. Never provide the private
GitHub URL as a public access route.

## Human-Field Contract

The exact known funding draft is:

```text
No specific funding.
```

Keep visibly unresolved:

```text
[BARRY CONFIRM: final author list and order]
[BARRY CONFIRM: affiliations and ORCIDs]
[BARRY CONFIRM: responsible corresponding author, institutional email, and full address]
[BARRY CONFIRM: author contributions]
[BARRY CONFIRM: acknowledgements]
[BARRY CONFIRM: conflicts of interest]
[BARRY CONFIRM: ethics/consent applicability and exact statement]
[BARRY CONFIRM: exact AI-use disclosure]
[BARRY CONFIRM immediately before submission: all-author approval and sole submission]
```

Do not convert dataset creator metadata into manuscript authorship. Do not
infer no conflict, ethics not applicable, sole authorship, AI roles, or final
approval.

## Final-Read Guide Contract

`manuscript/submission/rsec/final_read_guide.md` must be short enough to read
before the manuscript and include:

1. exact four bundle files;
2. fixed title, period, DOI, and scientific non-negotiables;
3. what changed in Goal 016;
4. a reading sequence: main manuscript, SI, then decision checklist;
5. the top-N and shuffle transparency corrections;
6. unresolved author/declaration fields;
7. code/Layer B public-reproducibility decision;
8. exact items Barry should return;
9. explicit statement that reading/approving the bundle is not Wiley
   submission authority.

## Code-Release Decision Contract

`manuscript/submission/rsec/code_release_decision.md` must:

- state the observed current condition without advocacy:
  - Layer A data public;
  - `dsipa-dev` private;
  - Layer B raw/row-level ALA restricted;
  - derived Layer B and source code not publicly archived;
- distinguish:
  - RSEC's general expectation that scripts and artefacts be public whenever
    possible; from
  - the conditional current-source understanding that AI-assisted analytical
    code may require public code, critical tests, and demonstration data;
- label the AI-policy consequence as conditional on Barry's factual AI-use
  disclosure and on live-workflow/editor interpretation;
- describe the preferred later route:
  - curated clean-history public repository;
  - licence and provenance review;
  - critical unit tests;
  - runnable demonstration data that do not redistribute restricted ALA rows;
  - installation/run instructions;
  - separate Zenodo Software record and DOI;
  - version/citation linkage back to the manuscript;
- compare it with keeping code private and requesting editorial guidance;
- identify decisions and risks, not execute them;
- state that `dsipa-dev` remains private and no public action is authorized.

Do not include credentials, private URLs, secrets, raw ALA paths, or a promise
that a public code package already exists.

## Figure Inventory Contract

Use read-only inspection:

```bash
file manuscript/figures/*
identify -format \
  '%f %wx%h density=%x,%y units=%U\n' \
  manuscript/figures/*.png
stat -f '%N %z bytes' manuscript/figures/*.png
```

Record the four main and seven SI figures, their current paths, dimensions,
density metadata, and manuscript role. The inventory must state:

- current PNGs are adequate for the accepted reader build;
- current official Wiley guidance allows legible standard files at initial
  review;
- preferred production preparation is generally PDF/600 dpi for line art and
  PNG/TIFF/300 dpi for images, with at least 1,800 pixels width where
  applicable;
- several current files may need later vector or higher-resolution export;
- Goal 016 does not regenerate figures;
- cover-image choice is optional and Barry-owned.

Do not label a figure production-ready solely because its embedded density
tag is non-zero.

## Component Word Counts

Retain the existing exact commands:

```bash
awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## 1\. Introduction/{on=1}/^## Data accessibility/{on=0}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## 1\. Introduction/{on=1}on' \
  manuscript/text/manuscript_draft.md | wc -w

awk '/^## Keywords/{on=1;next}/^---/{on=0}on' \
  manuscript/text/manuscript_draft.md |
  tr ';' '\n' |
  sed '/^[[:space:]]*$/d' |
  wc -l
```

Record the conservative sum:

```bash
abstract_words="$(
  awk '/^## Abstract/{on=1;next}/^## Keywords/{on=0}on' \
    manuscript/text/manuscript_draft.md | wc -w | tr -d ' '
)"

body_words="$(
  awk '/^## 1\. Introduction/{on=1}on' \
    manuscript/text/manuscript_draft.md | wc -w | tr -d ' '
)"

test "$((abstract_words + body_words))" -le 5000
printf '%s\n' "$((abstract_words + body_words))"
```

For the complete component table, document and run reproducible source-based
counts for:

```bash
wc -w manuscript/text/tables.md
wc -w manuscript/text/supplementary_tables.md
wc -w manuscript/text/figures.md
wc -w manuscript/text/supplementary_figures.md
```

After the submission build, count the rendered reference section using a
saved text extraction under ignored `build/` and record the exact extraction
boundary. Also report acknowledgements and non-exempt declaration counts
separately when those sections exist. Do not pretend source Markdown markup
and rendered prose counts are identical; label the method for every component.

The acceptance gate is:

- abstract `<= 300`;
- keywords `4-6`;
- running title `<= 45`;
- conservative abstract plus body `<= 5,000`; and
- no hidden uncounted submission prose.

If the conservative count exceeds `5,000`, use only the permitted Layer B
compression. Stop if that is insufficient.

## Focused Content Scans

Run:

```bash
rg -n -F \
  "Detectable change in dark-sky integrity across Australia’s protected areas" \
  manuscript docs/stage4_manuscript_release_plan.md docs/stage_overview.md

rg -n \
  '2013[-–]2024|10\.5281/zenodo\.21524637' \
  manuscript docs/stage4_manuscript_release_plan.md docs/stage_overview.md

rg -n -i \
  'top 20|top 15|bootstrap-median|inside_slope|buffer_1km_slope|retention_1km' \
  manuscript/text/manuscript_draft.md \
  manuscript/text/supplementary_tables.md \
  manuscript/text/supplementary_figures.md

rg -n -i \
  'one deterministic seeded realisation|illustrative benchmark|sampled null distribution' \
  manuscript/text/manuscript_draft.md \
  manuscript/text/figures.md \
  manuscript/text/supplementary_tables.md

rg -n -i \
  'public reproduc|private GitHub|private source|software record|Zenodo Software|public code' \
  manuscript/text/manuscript_draft.md \
  manuscript/submission/rsec
```

Manually classify hits from:

```bash
rg -n -i \
  'competitive rank|priority rank|top-ranked|highest-priority|management rank' \
  manuscript

rg -n -i \
  '\bcaus(e|es|ed|al|ality)\b|population decline|population trend|national biodiversity response' \
  manuscript
```

Negative statements such as `not a competitive ranking` and `cannot estimate
population decline` are expected evidence, not failures. Fail only positive
overclaims or ambiguous wording.

Confirm Fig. 4 remains in the main figure surface:

```bash
test "$(rg -c 'fig_layerB_alan_effects\.png' manuscript/text/figures.md)" -eq 1
test "$(rg -c 'fig_layerB_alan_effects\.png' manuscript/text/supplementary_figures.md)" -eq 0
```

## Test And Build Gate

Run the established validation ladder:

```bash
uv run --locked pytest \
  tests/python/test_makedoc_provenance.py \
  tests/python/test_rsec_submission_contract.py -q

make test

make PROFILE=draft ms-check
make PROFILE=draft ms-build

make PROFILE=submission ms-check
make PROFILE=submission ms-build

make PROFILE=supplementary ms-check
make PROFILE=supplementary ms-build

git diff --check
```

Do not weaken tests, edit code/configuration, or change build profiles to make
the gate pass. If the first pass finds one material documentation defect,
perform one focused repair within the permitted paths, then rerun only the
affected checks plus the final acceptance set. Stop on a remaining material
failure.

## Provenance, Text, And Visual QA

After builds:

1. inspect profile manifests for DSIPA source identity, branch, dirty state,
   and distinct Makedoc identity;
2. require zero unknown citation keys and classify any unused keys;
3. extract text from the main and SI PDFs and verify:
   - exact title;
   - `2013-2024`;
   - DOI;
   - top-20/top-15 disclosures;
   - single-seeded-realisation language;
   - funding draft;
   - public-data/private-source distinction;
4. inspect the main PDF/DOCX:
   - title page and visible human placeholders;
   - abstract;
   - Fig. 4;
   - Data accessibility;
   - declarations/end matter;
   - references;
5. inspect the authoritative SI PDF:
   - frontmatter;
   - Table S1 and Table S2 notes;
   - Fig. S2 and Fig. S3 captions;
   - landscape table readability;
   - portrait restoration and complete labels;
6. confirm no overlap, clipping, placeholder leakage outside intended human
   markers, or stale public-reproducibility claim.

Use the existing PDF/DOCX inspection workflow. Do not regenerate scientific
figures.

## Reader Bundle

Require that the target does not already contain unexplained files:

```bash
test ! -e build/final_read/goal016
mkdir -p build/final_read/goal016
```

Copy exactly:

```bash
cp build/submission/dsipa_rsec_main.pdf \
  build/final_read/goal016/dsipa_rsec_final_read_main.pdf

cp build/submission/dsipa_rsec_main.docx \
  build/final_read/goal016/dsipa_rsec_final_read_main.docx

cp build/supplementary/dsipa_rsec_supplementary.pdf \
  build/final_read/goal016/dsipa_rsec_final_read_supporting_information.pdf

cp manuscript/submission/rsec/final_read_guide.md \
  build/final_read/goal016/final_read_guide.md
```

Require exactly four files and no SI DOCX:

```bash
test "$(
  find build/final_read/goal016 -maxdepth 1 -type f | wc -l | tr -d ' '
)" -eq 4

test ! -e \
  build/final_read/goal016/dsipa_rsec_final_read_supporting_information.docx

find build/final_read/goal016 -maxdepth 1 -type f -print |
  LC_ALL=C sort

shasum -a 256 build/final_read/goal016/*
stat -f '%N %z bytes' build/final_read/goal016/*
```

Record the four names, sizes, and hashes in `Log.md` and
`docs/log/136_rsec_final_read_readiness.md`. The bundle is ignored/local and
must not be staged.

## Exact Footprint Review

Before acceptance:

```bash
git status --short --branch --untracked-files=all
git diff --name-status
git diff --stat
git diff --check
git diff
```

The diff must be a subset of the Goal 016 permitted tracked paths. Prove no
prohibited tracked path changed:

```bash
git diff --name-only |
  rg -n '^(src|tests|data|analysis|settings|references|artefacts|\.github)/' &&
  exit 1 || true
```

Manually confirm that no table row, figure path, figure file, bibliography,
source, test, configuration, data, result, or analysis artefact changed.

## Orchestrator Review And Git Closeout

Before staging, give the orchestrator:

- exact diff and status;
- count table;
- transparency-scan results;
- focused and full test results;
- all three check/build results;
- provenance/citation/lint evidence;
- visual/text QA;
- reader-bundle names, sizes, and hashes;
- code-release decision state;
- unresolved human and live-workflow fields;
- repair count; and
- confirmation that no external/public action occurred.

Only after explicit orchestrator acceptance, stage each accepted tracked path
exactly. Never use `git add .`, `git add -A`, a directory-wide add, or a glob.

Then:

```bash
git diff --cached --check
git diff --cached --name-status
git diff --cached
git commit -m "Prepare DSIPA RSEC final-read bundle"
git fetch --prune origin
git status --short --branch
git log --oneline --decorate -3
git push origin main
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
git status --short --branch
```

If `origin/main` moved unexpectedly, stop. Do not merge, rebase, force-push,
reset, or absorb unrelated work.

Git push after acceptance is the only external mutation permitted by Goal 016.
No Wiley action, public repository, visibility change, tag, GitHub release,
Zenodo Software record, additional data publication, fee/APC action, or
journal licence action is authorized.

## Handoff And Stop

Stop at the 80/20 final-read handoff when:

- Barry has the four reader files;
- the guide makes every decision visible;
- all validation is green;
- the source repository remains private;
- no submission/public action occurred; and
- remaining work is Barry's read, human declarations, a public-code decision,
  optional production exports, or a separately authorized submission goal.

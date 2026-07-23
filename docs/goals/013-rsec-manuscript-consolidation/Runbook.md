# Runbook: Goal 013 RSEC Manuscript Consolidation

## Start

From `/Users/bwbrook/papers/dsipa-dev`:

```bash
pwd
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
test -f docs/goals/013-rsec-manuscript-consolidation/Goal.md
```

Required baseline:

```text
branch: main
HEAD/origin/main: b38366110477e69ca92e269faecbe950965a6b92
status: ## main...origin/main plus this authorized untracked Goal 013 packet
```

The orchestrator-created packet is expected to be untracked at execution
start. Stop for any other change.

## Read First

- `AGENTS.md`
- full Goal 013 packet
- `manuscript/text/manuscript_draft.md`
- `manuscript/text/tables.md`
- `manuscript/text/figures.md`
- `manuscript/text/supplementary_tables.md`
- `manuscript/text/supplementary_figures.md`
- `manuscript/text/references.md`
- `references/refs.yaml`
- `docs/goals/012-layerA-consolidation-reproducibility-hardening/LayerA_Consolidation_Closeout.md`
- `settings/layerA_reference_contract_v0_3_0.json`
- `analysis/reports/layerA_denominators_and_censoring.md`
- `analysis/reports/layerA_table1_candidate.md`
- `analysis/reports/layerA_edge_profile_decision.md`
- `analysis/reports/layerA_watchlists_uncertainty.md`
- `analysis/reports/risk_rankings_and_quadrants.md`
- `analysis/reports/layerB_modelling_report.md`
- `analysis/reports/layerB_scope_coverage.md`
- `analysis/reports/layerB_exposure_qc.md`
- `analysis/reports/layerB_ala_license_ledger.md`
- `analysis/reports/final_release_manifest.md`
- `analysis/reports/figure_inventory.md`
- `docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md`
- `docs/stage_overview.md`

Read another repo-local source only when needed to verify a manuscript claim.
Do not read or write outside the action repo.

## Core Evidence To Protect

Layer A:

- PA universe: 11,133.
- Eligible baseline/trend subset: 4,426 (39.8%).
- 2024 zero inside mean: 3,844/4,426 (86.9%).
- Exact-zero inside slopes: 3,969/4,426 (89.7%).
- Positive inside slopes: 420/4,426 (9.5%).
- Retention denominator: 3,858.
- Q1/Q2/Q3/Q4: 305/55/3,308/190.
- Ring 1 valid: 1,432/11,133 (12.9%).
- Complete rings: 383/11,133 (3.4%).

Layer B:

- Response: microbat-versus-passerine occurrence-record identity.
- Provider-matched sample: 50,281 records per class.
- Primary AUC/log loss: about 0.545/0.689.
- Block-shuffle AUC: about 0.505.
- IBRA-by-year-shuffle AUC: about 0.517.
- Multi-provider AUC: about 0.557, descriptive only.

## Required Counts

Record the counting commands, exclusions, and results in the closeout. Counts
must distinguish prose from legends and references. At minimum report:

```text
abstract words <= 300
main-text words <= 5,000; target 4,600-4,800
keywords = 4-6
main figures/tables
supplementary figures/tables
```

Use a reproducible parser or clearly documented section-boundary command.
Do not report a whole-file `wc -w` as the RSEC main-text count.

## Validation

Run from the repo root:

```bash
git status --short --branch
git diff --check
make ms-check
make ms-build
```

Run and manually classify targeted scans:

```bash
rg -n -i 'audit|competitive rank|league table|remain dark|external pressure|penetration' manuscript/text
rg -n '1,427|12\.8%' manuscript/text
rg -n '1,432|12\.9%' manuscript/text
rg -n -i 'population decline|population trend|causal impact|causal response|national biodiversity response' manuscript/text
rg -n -i 'provider.match|observation process|protocol|detector|acoustic|detectability|weak discrimination|AUC|shuffle|null benchmark|falsif' manuscript/text
rg -n -i 'DOI|Zenodo|raw ALA|row-level|redistribut|restricted|public input|archive' manuscript/text
rg -n '11,133|4,426|3,844|86\.9|3,969|89\.7|420|3,858|305|55|3,308|190|1,432|12\.9|383|50,281|0\.545|0\.689|0\.505|0\.517|0\.557' manuscript/text
```

The scans are review aids, not automatic pass/fail gates. Classify every hit
in the closeout. A justified methodological use of `penetration`, a historical
citation title, or a negated causal claim is not automatically a defect.

Also verify:

- every quantitative manuscript claim against Goal 012 or an accepted Layer B
  source;
- every citation key against the bibliography;
- every figure/table reference against its ordered main or supplementary
  assembly;
- every caption against the value and inference used in the text;
- exact title, abstract count, main-text count, and keyword count; and
- the final changed-file list against the permitted mutation boundary.

## Focused Self-Review

After the first successful build, read the built manuscript once as a
scientific reviewer. Repair material defects only:

- story discontinuity;
- text-evidence mismatch;
- incorrect statistical interpretation;
- overclaim;
- missing eligibility or observation-process condition;
- broken display order/reference; or
- journal-limit failure.

Repeat only the checks affected by the repair. Do not begin further
review-and-polish loops unless new material evidence appears.

## Required Closeout

Create:

```text
docs/goals/013-rsec-manuscript-consolidation/RSEC_Manuscript_Consolidation_Closeout.md
```

It must record:

- starting and final branch/HEAD/status;
- exact changed files;
- title and final narrative decision;
- abstract, main-text, keyword, figure, and table counts with method;
- section/display changes;
- all corrected evidence mismatches;
- Layer B interpretation correction;
- quantitative evidence cross-check;
- exact `make ms-check` and `make ms-build` outcomes;
- build-product paths and formats;
- citation/reference and display-order checks;
- claim/terminology/data-accessibility scan classifications;
- focused self-review and any repair;
- residual scientific, accessibility, production, and release limitations;
- whether Goal 013 is ready for orchestrator acceptance; and
- commit/push state.

Also create `docs/log/133_rsec_manuscript_consolidation.md` and append this
goal `Log.md`.

## Wake-Up And Stop

On completion, send:

```text
Goal 013 complete.

Closeout: /Users/bwbrook/papers/dsipa-dev/docs/goals/013-rsec-manuscript-consolidation/RSEC_Manuscript_Consolidation_Closeout.md
```

If blocked, replace `complete` with `blocked` and identify the decision or
evidence needed.

Then stop. Do not commit, push, package, upload, mint a DOI, or begin another
goal.

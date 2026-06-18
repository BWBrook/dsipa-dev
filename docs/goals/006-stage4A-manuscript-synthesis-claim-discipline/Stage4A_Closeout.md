# Stage 4A Closeout: Manuscript Synthesis and Claim Discipline

Status: complete.

## Starting State

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- `git status --short --branch` at start: `## main...origin/main` plus untracked `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/`
- `git rev-parse --short HEAD`: `9793641`
- Goal 006 packet present: yes.
- Repo-local `AGENTS.md` and the full Goal 006 packet were read before edits.

## Work Completed

- Revised `manuscript/text/manuscript_draft.md` so the Abstract, Results, Discussion, and Limitations lead with accepted Stage 2/3 evidence and keep inference bounded.
- Tightened manuscript-facing denominators and selection caveats in `manuscript/text/figures.md`, `manuscript/text/supplementary_figures.md`, and `manuscript/text/tables.md`.
- Preserved Table S1 and Table S2 values after checking them against accepted reports.
- Updated `docs/interpretation_notes.md` with a Stage 4A synthesis entry and refreshed summary.
- Updated `docs/stage1_critique_resolution_matrix.md`:
  - M01, M02, M04, and M05 are now `done`.
  - R06 is now `done` after the narrow plan/roadmap redirect.
  - M03 remains open for later bibliography/CSL/production work.
- Updated `docs/plan.md` and `docs/roadmap.md` only to direct readers to the current stage ladder and active goal packets.
- Added chronological log `docs/log/126_stage4A_manuscript_synthesis.md`.

## Claim Discipline

Layer A is now framed as the primary dark-sky integrity audit with explicit censoring and denominator discipline:

- PA universe: n = 11,133.
- Inside baseline/trend eligibility: n = 4,426.
- 2024 zero inside mean radiance: 3,844/4,426 = 86.9%.
- Exactly zero inside slopes: 3,969/4,426 = 89.7%.
- Positive inside slopes: 420/4,426 = 9.5%.
- 1 km unprotected-land retention denominator: n = 3,858.
- Retention quadrants: Q1 = 305, Q2 = 55, Q3 = 3,308, Q4 = 190.
- Complete interior-ring profiles: n = 383.

Layer B remains a conservative secondary exercise:

- Provider-matched dr368 model: 50,281 microbat and 50,281 passerine records.
- Primary AUC/log loss: 0.545 / 0.689.
- Block-shuffle AUC: 0.505.
- IBRA x year shuffle AUC: 0.517.
- Full multi-provider sensitivity AUC: 0.557, descriptive only.
- Interpreted as weak, provider-bounded, presence-only, associational, and falsification-limited.

The manuscript now explicitly separates the Fig. 2 all-nonzero slope diagnostic subset (n = 457) from the positive brightening subset (n = 420).

## Validation Evidence

- `git diff --check`: passed.
- `make ms-check`: passed.
  - Tool check passed.
  - Build profile config validation passed.
  - 61 tests passed.
  - Manuscript lint passed.
  - Reference audit passed: 30 bibliography keys, 26 cited keys, 0 unknown keys, 4 unused keys reported as non-fatal.
  - Build check passed.
- Claim scan:
  - Hits for `causal`, `population trend`, `population decline`, and `national biodiversity response` are negated, cautionary, or future-method framing.
  - No unsupported causal, population-decline, population-trend, or national biodiversity-response claim remains in the manuscript-facing text reviewed.
- Layer B scan:
  - Provider-matched, provider-bounded, presence-only, falsification, weak discrimination, AUC/log-loss, mixed-licence, and no-raw-ALA/no-redistribution language is present.
- Denominator/source-value scans:
  - Required Layer A and Layer B numbers are present in manuscript text and accepted reports.
  - Caption/table language carries eligibility, censoring/floor, selection, triage, and uncertainty caveats.

## Residual Stage 4 Boundaries

No Stage 4B or Stage 4C work was started.

Remaining later-stage items include:

- final bibliography/style/CSL production pass (M03);
- release/archive/DOI policy and manifests;
- raw or row-level ALA redistribution decisions;
- final publication tooling.

## Blockers or Questions

None for Goal 006.

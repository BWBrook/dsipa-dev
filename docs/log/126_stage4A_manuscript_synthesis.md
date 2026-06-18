# 126 - Stage 4A manuscript synthesis and claim discipline

Date: 2026-06-18

Goal packet: `docs/goals/006-stage4A-manuscript-synthesis-claim-discipline/`

## Starting state

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch/status at start: `## main...origin/main`; untracked Goal 006 packet directory.
- `HEAD`: `9793641`
- Goal 006 packet present: yes.

## Scope

Stage 4A only. This pass used accepted Stage 2/3 evidence to tighten the manuscript, captions, interpretation notes, and critique matrix. It did not run data processing, model fitting, ALA downloads, remote compute, package builds, release packaging, DOI/archive work, commits, pushes, or PR work.

## Changes made

- Reworked the manuscript Abstract, Results, Discussion, and Limitations around evidence-backed claims.
- Made Layer A denominator discipline more explicit:
  - PA universe: n = 11,133.
  - Inside eligibility: n = 4,426.
  - 2024 zero inside mean radiance: 3,844/4,426 = 86.9%.
  - Exactly zero inside slopes: 3,969/4,426 = 89.7%.
  - Positive inside slopes: 420/4,426 = 9.5%.
  - Retention/quadrant denominator: n = 3,858.
  - Complete-ring subset: n = 383.
- Separated the Fig. 2 all-nonzero slope diagnostic subset (n = 457) from the positive brightening subset (n = 420).
- Kept Layer B as weak, provider-bounded, presence-only, associational, and falsification-limited.
- Tightened Fig. 2, Supplementary Fig. S1, and Table 1 notes.
- Updated `docs/interpretation_notes.md` with a Stage 4A synthesis entry and refreshed summary.
- Updated `docs/stage1_critique_resolution_matrix.md` for M01, M02, M04, M05, and the narrow R06 governance redirect.
- Updated `docs/plan.md` and `docs/roadmap.md` only to point current readers to the stage ladder and active goal packets.

## Validation

- `git diff --check`: passed.
- `make ms-check`: passed.
  - Tool/config validation passed.
  - 61 tests passed.
  - Manuscript lint passed.
  - Reference audit passed with 30 bibliography keys, 26 cited keys, 0 unknown keys, and 4 unused keys reported as non-fatal.
  - Build check passed.
- Claim scan over manuscript text and interpretation notes found only negated, cautionary, or future-method uses of causal/population/national-biodiversity-response language.
- Provider/Layer B scan confirmed provider-matched/provider-bounded/falsification/AUC/log-loss/mixed-licence/no-raw-ALA wording remains present.
- Denominator and source-value scans confirmed the manuscript and accepted reports surface the required Layer A and Layer B values.

## Residual boundaries

- Stage 4A is complete.
- Still out of scope and unresolved for later stages: final bibliography/style production, release/archive/DOI policy, raw/row-level ALA redistribution decisions, release manifests, and final publication tooling.

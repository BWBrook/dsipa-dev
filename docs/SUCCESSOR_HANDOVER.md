# DSIPA successor handover

**Current at 2026-09-05. Read this first in a fresh DSIPA thread, then verify
the live Git state before acting.**

## Operating state

Work directly in `/Users/bwbrook/papers/dsipa-dev`. The historical Chief of
Staff, Goal Composer, project-orchestrator, and named action-agent machinery is
not the current control plane. References to it in old goal packets and logs
are provenance, not instructions to recreate that workflow. Use native Codex
work and bounded subagents only when they materially help.

Observed immediately before adding this handover:

- branch `main` was clean and equalled `origin/main` at `e197461`;
- the latest commit is **Simplify DSIPA active execution path** (Goal 017);
- the four-file final-read bundle exists locally under
  `build/final_read/goal016/`;
- GitHub reports `BWBrook/dsipa-dev` as private; and
- the project is **awaiting Barry's scientific/editorial final read and
  pre-submission decisions**, not awaiting another routine analysis run.

This file was the only working-tree change introduced by the handover task. If
the opening Git check shows anything else, classify it before editing.

Some older status prose says an accepted goal still needs commit/push. Trust
the live history above: Goal 016 is committed as `00e43f0`, Goal 017 as
`e197461`, and `main` matches the remote at handover.

## Scientific contract

The paper is an RSEC Original Research manuscript titled:

> **Detectable change in dark-sky integrity across Australia's protected
> areas**

Its stable design is:

- **Layer A, primary:** annual VIIRS radiance during `2013-2024` inside
  Australian protected areas, in surrounding unprotected land, and in
  interior bands where raster support permits. Outputs are detectability-aware
  categorical screens, not causal diagnoses or management rankings.
- **Layer B, secondary:** a provider-matched, presence-only case-control test
  of whether ALAN covariates distinguish microbat from passerine occurrence
  records. It is weakly discriminating and cannot establish abundance,
  occupancy, population change, or a biological response to ALAN.

The headline evidence is settled for the current manuscript:

- 4,426 of 11,133 protected areas (39.8%) met the primary eligibility rules;
- within that subset, 86.9% had zero inside mean radiance in 2024 and 89.7%
  had a zero Theil-Sen slope;
- among 3,858 areas with paired inside and 1 km surrounding trends, 305 showed
  concurrent brightening and 190 surrounding-only brightening;
- complete three-band interior evidence exists for only 383 areas, so it is a
  selected diagnostic rather than a national gradient; and
- Layer B out-of-block discrimination was weak (`AUC = 0.545`). Each shuffle
  result is one deterministic illustrative realisation, not a sampled null
  distribution or causal counterfactual.

Do not silently strengthen these claims. A VIIRS zero is non-detection at the
product scale, not proof of ecological darkness. Screening categories support
local investigation; fine ordering is uncertain and is not a priority rank.

## What has been completed

The project progressed from a national geospatial pipeline through staged
scientific hardening and manuscript synthesis:

1. Layer A data identities, schemas, eligibility rules, trend outputs,
   uncertainty summaries, and manuscript headlines were reproduced and
   hardened. The accepted reference contract preserves the current scientific
   result.
2. Layer B was retained only as a compact data-adequacy/association diagnostic
   with explicit observation-process and causal limits.
3. The RSEC main manuscript and Supporting Information were consolidated,
   checked, built, and visually reviewed. Goal 016 added exact top-N and
   single-shuffle disclosures without changing data, models, numbers, tables,
   or figure pixels.
4. Nine processed national Layer A outputs were published under CC BY 4.0 as
   Zenodo Dataset `0.3.0`: <https://doi.org/10.5281/zenodo.21524637>. This is a
   dataset DOI, not a software release; raw/row-level ALA data and Layer B
   payloads remain excluded.
5. Goal 017 simplified the active execution path: shared fail-closed Git-state
   handling, one canonical Layer B flow, a proportional `make fast` gate, and
   removal of two obsolete release helpers. It did not alter accepted science
   or manuscript surfaces. Its checks passed: `make fast` 57 tests; `make
   test` 97 tests with 9 data-dependent skips; targeted guards, shell syntax,
   a temporary package build, and protected-surface checks also passed.

## Live review surface

Barry's primary reading bundle is:

1. `build/final_read/goal016/dsipa_rsec_final_read_main.pdf`
2. `build/final_read/goal016/dsipa_rsec_final_read_main.docx`
3. `build/final_read/goal016/dsipa_rsec_final_read_supporting_information.pdf`
4. `build/final_read/goal016/final_read_guide.md`

The authoritative tracked guide is
`manuscript/submission/rsec/final_read_guide.md`. Also read, as needed:

- `manuscript/text/manuscript_draft.md` for the scientific narrative;
- `manuscript/submission/rsec/code_release_decision.md` for the public-code
  fork;
- `analysis/reports/final_release_manifest.md` for release provenance; and
- `docs/goals/017-lean-path-consolidation/Lean_Path_Consolidation_Closeout.md`
  for the present engineering surface.

Treat `docs/roadmap.md`, early `docs/plan.md` status cues, and old goal packets
as history unless a live caller or current decision still depends on them.
Do not ingest the whole archive to bootstrap routine work.

## Where the project is heading

The next meaningful boundary is Barry's full read. The recommended sequence is:

1. Receive and classify Barry's manuscript/SI comments and the unresolved
   human metadata: author order, affiliations/ORCIDs, correspondence,
   contributions, acknowledgements, conflicts, ethics, exact AI-use
   disclosure, and final author approvals.
2. Frame one bounded pre-submission tranche that incorporates those decisions,
   updates journal requirements from current official sources, fixes only
   verified issues, rebuilds the reader/submission assets, and reruns the
   decision-relevant validation ladder.
3. Resolve the public-code decision separately. The recorded preferred route
   is a curated clean-history public code repository plus a distinct Zenodo
   Software record, but Barry has not authorized that action. The alternative
   is to retain private code and seek editorial guidance.
4. Ask for explicit final authority before any Wiley login, upload, submission,
   licence, fee/APC, repository-visibility, public-code, tag, release, or other
   external action.

One known pre-submission defect is deliberately unresolved: Fig. 4's internal
plotted title still uses the legacy word `falsification`. Its caption and prose
correctly describe the shuffles as illustrative benchmarks. Fix the title
reproducibly from the preserved Layer B evidence or an independently verified
summary-only rendering route; do not edit figure pixels by hand.

Do not launch national, ALA, model, remote, archive, or manuscript-regeneration
work merely to refresh confidence. Run it only when Barry's review, a changed
claim, or a named release risk makes it decision-relevant.

## Recommended skills and cadence

Use `$twilight-laboratory`
(`/Users/bwbrook/.codex/skills/twilight-laboratory/SKILL.md`) as the primary
programme discipline: recover live state, preserve settled science, propose a
coherent decision-bearing tranche, and involve Barry at consequential
scientific or external-action boundaries. Its governing standard fits this
project: **rigour at the scientific decision boundary; proportional
engineering everywhere else**.

Use `$kill-your-darlings`
(`/Users/bwbrook/.codex/skills/kill-your-darlings/SKILL.md`) when evaluating
additional machinery, tests, reports, compatibility paths, or public-release
scope. Make each part earn its recurring cost; preserve scientific validity,
source integrity, restricted-data boundaries, and independent evidence.

For a fresh-thread orientation, remain read-only until the user asks for a
change. Start with:

```bash
pwd
git status --short --branch
git log --oneline -8
```

Then read this note, `AGENTS.md`, the final-read guide, and only the specific
evidence needed for the requested decision. The useful restart question is
not "what old goal comes next?" but "what decision or manuscript outcome does
Barry now want, and what is the smallest defensible tranche that reaches it?"

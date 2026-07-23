# DSIPA staged improvement overview

Status: draft operating plan, created 2026-05-15.

This document defines the staged workflow for moving from the current rough manuscript and reconciled evidence snapshot to a stronger, more decisive paper. It is intentionally stage-gated. Later stages should not be fully planned until earlier stages have been completed, reviewed, and signed off.

## Operating principles

- Keep stages sequential unless a documented decision says otherwise.
- Do not start new science work until Stage 0 has produced a clean, auditable baseline.
- Treat Layer A as the primary scientific contribution and harden it before expanding Layer B.
- Treat Layer B as a conservative secondary signal test unless a later signed-off stage changes that framing.
- Convert every critique into an explicit evidence, code, manuscript, and validation item before editing the science narrative.
- Preserve the distinction between the Mac mini control-plane checkout, the `deep-server` evidence/HPC checkout, and the `nectar` compute-control repository.
- Each stage must end with a short log entry, validation evidence, and a clear move/no-move recommendation.

## Stage ladder

| Stage | Name | Purpose | Detailed plan status | Exit gate |
| --- | --- | --- | --- | --- |
| 0 | Lock the baseline | Separate, validate, and commit the remote harness/evidence-reconciliation work; record the current manuscript draft as the narrative baseline. | Complete in `docs/stage0_lock_baseline_plan.md`. | Clean or deliberately parked working trees; validated evidence snapshot; Stage 0 closeout accepted. |
| 1 | Critique-resolution matrix | Convert all agreed critiques into a traceable work queue with evidence needs, code changes, manuscript changes, and acceptance tests. | Complete in `docs/stage1_critique_resolution_plan.md`; matrix accepted in `docs/stage1_critique_resolution_matrix.md`. | Every critique has an owner, required artefact, and pass/fail test. |
| 2 | Layer A science hardening | Strengthen the primary protected-area ALAN analysis: denominators, anchors, watchlists, uncertainty, and external-pressure interpretation. | Accepted after Goal 001 signoff-readiness review. | Layer A claims are backed by updated artefacts, sanity checks, and manuscript-ready tables/figures. |
| 3 | Layer B reconciliation | Tighten the conservative biodiversity signal test, falsification interpretation, and any justified sensitivity runs. | Accepted after Stage 3A evidence integration and Stage 3B ALA ingest guardrail review. | Layer B is defensibly retained as conservative secondary evidence with Stage 4 release gates still open. |
| 4 | Evidence-led manuscript rewrite | Rewrite Results, Discussion, tables, captions, and availability statements from the hardened evidence package. | Stage 4A manuscript synthesis accepted after Goal 006; Stage 4B release/data-availability readiness prepared in Goal 007; Stage 4C local validation and reproducibility-audit supplementation completed in Goal 008; Goal 009 prepared the release-blocker decision packet; Goal 010 approved Option B but found eight Layer A payloads absent; Goal 011 regenerated and preserved all nine outputs, matched six historical hashes and every primary headline, and was independently accepted as a concordant non-exact archive candidate with immaterial edge-threshold drift. Goal 012 completed Layer A reproducibility hardening and one national computation; its transparent post-failure continuation validated the unchanged outputs after a column-order-only validator repair, with all nine semantically concordant, zero stable-key descents, exact frozen headlines, and canonical 1,432/12.9% report artefacts. Goal 013 consolidated the accepted evidence into an RSEC-targeted, Layer A-centred manuscript with corrected categorical screening, Layer B null-benchmark interpretation, and current ring evidence. | Manuscript claims and the Layer A archive candidate remain scientifically accepted. DOI upload remains gated by explicit concordant non-exact metadata with radiance/GPKG limitations, external upload authorization, refreshed release evidence, and final orchestrator/Barry approval. |

## Global quality gates

These gates apply to every stage unless a later detailed plan explicitly supersedes them.

1. **Scope gate:** the stage begins with a stated objective, non-goals, and the current git/evidence state.
2. **Evidence gate:** any result claim must link to a generated table, figure, report, or reproducibility/audit artefact.
3. **Validation gate:** relevant tests, build steps, and domain sanity checks must run or be explicitly deferred with a reason.
4. **Manuscript gate:** manuscript changes must be traceable to evidence changes; no prose-only strengthening of unsupported claims.
5. **Git hygiene gate:** DSIPA and `nectar` changes must remain separated by repository and by purpose.
6. **Signoff gate:** the stage ends with a concise closeout note and a recommendation on whether to proceed.

## Stage-plan rule

Only the active stage receives a detailed plan. Future stages stay at overview level until the previous stage has passed its exit gate. This prevents us from locking in false precision before we know what the evidence and critique matrix actually require.

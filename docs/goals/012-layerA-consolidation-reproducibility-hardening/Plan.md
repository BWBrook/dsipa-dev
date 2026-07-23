# Plan: Goal 012 Layer A Consolidation And Reproducibility Hardening

## Purpose

Deliver one bounded engineering pass that makes accepted Layer A execution
deterministic, fail-closed, and clean-checkout reproducible, then prove it
against the accepted Goal 011 archive candidate.

## Execution Steps

1. Confirm the contract and baseline.
   - Read `Goal.md`, `Plan.md`, `Runbook.md`, and `Log.md` in order.
   - Record `pwd`, branch, HEAD, `origin/main`, and status.
   - Inventory the exact intended implementation footprint.
   - Stop for any baseline or unrelated-work drift.

2. Write the single reference contract and its loader.
   - Populate accepted inputs, output classifications/hashes, stable keys,
     frozen headlines, and the historical 1,427/1,432 distinction.
   - Add schema and internal-consistency validation.
   - Replace new release-validation literals with contract lookups.

3. Make clean-checkout triad QA offline.
   - Use provenance-verified tracked fixtures or deterministic temporary
     fixtures.
   - Keep both geometry and buffer checks real and active.
   - Prohibit CAPAD/network calls during pytest.
   - Prove QA leaves the fresh checkout clean.

4. Add fail-closed input checks and cache fingerprints.
   - Validate CAPAD, IBRA, Natural Earth, and all 12 VIIRS identities.
   - Add only the three required union-cache fingerprints.
   - Test positive, missing, malformed, and mismatched fingerprints.

5. Make statewise serialization deterministic.
   - Apply stable canonical sorts to state outputs and merged outputs.
   - Use explicit null placement.
   - Preserve all values, schemas, rows, and keys.
   - Suppress redundant intermediate state artefacts.

6. Harden the canonical runner.
   - Self-locate and change to repository root.
   - Add early environment/fixture checks.
   - Add explicit remote Layer A mode with frozen environment propagation.
   - Order input gate, computation, report-only modules, output gate, tests,
     and build.
   - Add syntax and dry-run/contract tests without contacting a remote host.

7. Run local validation.
   - Run targeted tests after each bounded workstream.
   - Run true fresh-checkout/archive pytest offline.
   - Run full pytest, shell syntax checks, contract assertions, and wheel/sdist
     build.
   - Perform one focused repair pass if necessary.

8. Run exactly one remote national regression.
   - Create an isolated remote sibling from baseline commit
     `1b39dcc1403a40c3962f04c922bb612c41f83a8f`.
   - Overlay only the permitted uncommitted implementation files; preserve the
     overlay diff, inventory, and hashes.
   - Run the explicit Layer A mode once with workers=12 and the frozen states.
   - Monitor to terminal status; polling timeouts are not worker deadlines.

9. Reconcile and close.
   - Compare all nine outputs to the Goal 011 payload.
   - Prove zero key-order descents and semantic equality where bytes differ.
   - Recompute all frozen headline values.
   - Verify canonical reports use 1,432/12.9% and preserve historical
     reconciliation.
   - Write the closeout and stage log.
   - Request independent orchestrator review.
   - Do not commit or push.

## Required Deliverables

- One machine-readable Layer A reference contract.
- Fail-closed input and output validation.
- Offline deterministic triad QA.
- Fingerprinted PA/land/land-unprotected union caches.
- Stable state and merged serialization.
- Explicit local and remote Layer A execution paths.
- Regenerated accepted report surfaces.
- One complete remote regression artefact and reconciliation.
- Goal 012 log, closeout, and orchestrator wake-up.

## Optional Polish

None is required for acceptance. Defer runner replacement, broad module
splitting, public/private API cleanup, generalized caching, and serialization
frameworks.

## 80/20 Stop Rule

Complete the core implementation, perform one focused repair pass, run exactly
one national regression, and stop. Do not spend further cycles on style,
byte-identical containers, unrelated debt, or additional national runs.

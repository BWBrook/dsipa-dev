# 2026-08-06 - Goal 017 lean-path consolidation

Completed a bounded engineering consolidation without scientific-surface
changes. Layer B Git-state handling is centralised and fail-closed; direct runs
require a clean tree, while the canonical runner uses one clean-start gate and
three explicit dirty intra-pipeline handoffs. Two superseded release helpers
were removed; ambiguous or scientifically active candidates were retained.

Local evidence: `make fast` 57 passed; `make test` 97 passed with 9 conditional
data-dependent skips; shell syntax, temporary wheel/sdist build, protected
surface checks, and `git diff --check` passed. See
`docs/goals/017-lean-path-consolidation/Lean_Path_Consolidation_Closeout.md`.

# Layer A Consolidation And Reproducibility Hardening

Date: 2026-07-23 UTC

Goal 012 implemented the bounded reference-contract, deterministic
serialization, cache-fingerprint, offline-triad, input-integrity, and runner
hardening work. Final local and source-only archive validation each passed 70
tests with 9 expected large-output skips, and all four triad tests ran and
passed. Wheel and sdist builds passed.

The first deep-server harness invocation stopped before Layer A at the dev
dependency gate. The runner was repaired to provision the locked dev extra, and
a no-compute environment preflight passed.

The subsequently authorised national run
`20260723T120648Z-goal012-layerA-consolidation` completed all Layer A science
and reports, then terminated failed at its output gate because the validator
required schema tuple order. Exact audit showed five CSVs and the GPKG had only
column-order differences: every file had the same duplicate-free name
multiset, with no missing or extra columns and no scientific drift.

Independent review found no P0/P1 issue. A single narrow repair changed CSV and
GPKG column validation to duplicate-safe name-multiset equality and added
direct permutation/missing/extra/duplicate tests. No writer, threshold,
scientific module, generated output, or report changed.

No second national computation ran. A post-failure continuation on the same
outputs passed output validation, 79 remote tests, wheel/sdist build, and
all-nine semantic reconciliation to Goal 011. All stable-key descents are zero,
all frozen headlines match, generated reports show 1,432/12.9%, and all nine
pre/post output hashes are identical.

The original failed log/status and the successful continuation are preserved
separately under:
`/data/codex/artifacts/dsipa/20260723T120648Z-goal012-layerA-consolidation`.
Its 43-entry checksum index verifies with zero failures. Goal 012 is complete
for orchestrator acceptance; commit, push, DOI, and publication remain gated.

Complete evidence:
`docs/goals/012-layerA-consolidation-reproducibility-hardening/LayerA_Consolidation_Closeout.md`.

# Plan

1. Persist this packet and verify the starting gate.
2. Inventory active Layer B, runner, artefact, manifest, and test surfaces.
3. Record caller evidence for candidate deletions, flags, and modes.
4. Implement one bounded consolidation pass:
   - centralise Git-state handling for artefact runners;
   - make Layer B artefact creation clean-tree coherent;
   - extract small shared helpers only where active callers justify them;
   - retire only caller-free obsolete code.
5. Add deterministic fixture tests for the clean-tree contradiction and any
   touched helper behaviour.
6. Document proportional fast and release gates with existing tooling.
7. Run authorized validation:
   - fast gate;
   - full `make test`;
   - wheel/sdist build;
   - shell syntax and runner-contract tests;
   - frozen surface checks;
   - `git diff --check`.
8. Perform one focused self-review/repair pass.
9. Write the closeout/log, wake the DSIPA orchestrator, and stop.

Stop early if science, schema, output identity, manuscript, DOI/licensing,
remote/national/model execution, ambiguous deletion evidence, broad Layer A
rewrite, general framework design, unrelated state, or cosmetic-only work would
be required.

# Plan: Goal 016 RSEC Final-Read Readiness

## Purpose

Create the smallest complete package Barry can read as the prospective final
RSEC manuscript while preserving every scientific result and every external
gate. The output is decision-ready for Barry, not submission-ready for Wiley.

## Phase 1: Controlled Start And Evidence Lock

1. Re-read `AGENTS.md` and all four Goal 016 packet files.
2. Record repository, branch, HEAD, `origin/main`, merge-base, and status.
3. Require the accepted Goal 015 state to remain in history and explain every
   current change.
4. Read only the permitted manuscript, RSEC, and governance surfaces.
5. Freeze:
   - title;
   - `2013-2024`;
   - DOI `10.5281/zenodo.21524637`;
   - data, models, numbers, table cells, and figure pixels;
   - Fig. 4 in the main text; and
   - screening-not-ranking and non-causal interpretation.
6. Record the current counts and exact Table S1/Fig. S2/Fig. S3/Layer B
   wording before editing.

Stop for unrelated work, upstream divergence, a frozen-content mismatch, or
an evidence need outside the packet.

## Phase 2: Bounded Transparency And Compression

1. Amend Table S1 explanatory text only.
   - State top 20 within each of the three categories.
   - Name each point-estimate selection/order metric.
   - Preserve source order as a transparent screen, not management priority.
2. Amend Fig. S2 and Fig. S3 captions only.
   - Fig. S2: top 20 by bootstrap-median inside slope.
   - Fig. S3: top 15 for pairwise ordering frequencies.
3. Reconcile Layer B shuffle wording.
   - Each of the two shuffles is one deterministic seeded realisation.
   - Each is illustrative, not a null distribution.
   - Neither supplies causal identification.
4. Compress repeated Layer B caveats only as needed for word headroom.
   - Preserve all numbers, limitations, and Fig. 4.
   - Do not remove more than 250 net words without review.
5. Reconcile reproducibility wording.
   - Describe the internal pipeline as versioned, scripted, tested, and
     manifest-backed.
   - State that code and the complete Layer B reproduction route are not yet
     supplied through a citable public software release.
   - Keep public data and private source distinct.

Perform no calculation, table-row edit, figure regeneration, code change, or
new scientific interpretation.

## Phase 3: Decision And Readiness Documents

Create:

1. `final_read_guide.md`
   - identify exactly what Barry should read;
   - list the bounded scientific corrections;
   - distinguish fixed content from decisions;
   - list unresolved human fields;
   - state that this is not the submission package;
   - provide a short return checklist for Barry.
2. `code_release_decision.md`
   - describe current private-source/public-Layer-A state;
   - separate general data/code expectations from the conditional
     source-informed AI-assisted-code issue;
   - compare the preferred curated clean-history repo plus Zenodo Software
     route with retaining private code and seeking editorial guidance;
   - identify the minimum later evidence, licence, provenance, test, demo-data,
     citation, and authorization gates;
   - make no public action or final recommendation on Barry's behalf.
3. `figure_production_inventory.md`
   - list all four main and seven SI figures;
   - record current path, role, pixel dimensions, embedded density, and whether
     a higher-resolution/vector production export is still advisable;
   - distinguish initial-review legibility from later production preference;
   - identify an optional cover-image candidate decision without creating one.

## Phase 4: RSEC Surface Reconciliation

Update only directly relevant RSEC files:

- README: describe the Goal 016 final-read state and bundle.
- Checklist: separate passes, final-read decisions, pre-submission decisions,
  and external actions.
- Metadata: retain exact title/type/counts/DOI; keep human identity fields
  unresolved.
- Counts: add the complete component table and methods.
- Declarations: draft `No specific funding`; preserve visible placeholders for
  authorship, conflict, ethics, AI, and final approval.
- Cover letter: reflect corrected transparency/reproducibility framing and
  preserve Barry confirmation markers.
- SI frontmatter only if needed to keep its final-read status and human
  placeholders unambiguous.

Do not infer manuscript authorship from the sole Zenodo dataset creator.

## Phase 5: Count And Word-Budget Gate

1. Re-run the documented abstract, main-body, and keyword commands.
2. Add reproducible counts for acknowledgements, references, tables, and
   figure legends.
3. Record:
   - abstract;
   - IMRAD;
   - IMRAD plus Data accessibility;
   - conservative abstract plus body;
   - non-exempt declarations if present;
   - acknowledgements;
   - references;
   - tables;
   - figure legends;
   - keywords.
4. Keep the conservative readiness count at or below `5,000`.
5. If the count exceeds the limit, use only the already-authorized modest
   Layer B compression.
6. Stop rather than cut scientific caveats or alter another section for
   convenience.

## Phase 6: Build And Reader Bundle

1. Run the established focused tests and full `make test` gate.
2. Run `ms-check` and `ms-build` for `draft`, `submission`, and
   `supplementary`.
3. Inspect generated provenance and citation/lint results.
4. Create ignored `build/final_read/goal016/` only if it does not already
   contain unexplained files.
5. Copy exactly:
   - submission main PDF;
   - submission main DOCX;
   - authoritative SI PDF;
   - `final_read_guide.md`.
6. Exclude the diagnostic SI DOCX.
7. Record file sizes and SHA-256 values in the Goal 016 log/closeout.
8. Review the exact bundle contents from a reader's perspective.

## Phase 7: Governance And Closeout

1. Update `docs/stage4_manuscript_release_plan.md` narrowly to record the
   final-read readiness tranche and its remaining public-code/human gates.
2. Update `docs/stage_overview.md` with Goal 016 status.
3. Add `docs/log/136_rsec_final_read_readiness.md`.
4. Append the final checkpoint to Goal 016 `Log.md`.
5. Record exact changed paths, commands, outputs, repair count, and residual
   decisions.
6. Run final footprint, content, whitespace, and generated-asset review.

## Phase 8: Orchestrator Acceptance And Git Closeout

1. Present:
   - the four-file reader bundle;
   - exact changed footprint;
   - count table;
   - tests/checks/builds;
   - text and visual QA;
   - code-release decision state;
   - unresolved Barry fields; and
   - explicit statement that no Wiley/public action occurred.
2. Wait for orchestrator acceptance.
3. Only after acceptance:
   - stage exact tracked paths;
   - inspect the complete staged diff;
   - commit;
   - fetch/prune;
   - prove fast-forward safety; and
   - push `main`.
4. Do not stage ignored reader-bundle outputs.
5. Do not tag, create a release, change visibility, publish code/data, or
   contact Wiley.

## Review Priorities

1. frozen science and exact numerical identity;
2. top-N and single-shuffle transparency;
3. screening-not-ranking and non-causal interpretation;
4. honest internal-versus-public reproducibility wording;
5. human claims visibly unresolved;
6. conservative word-count compliance;
7. usable four-file final-read bundle;
8. exact mutation and external-action boundaries.

## Efficiency And Stop Policy

Use one core execution pass and at most one focused repair for a material
defect. Stop at the 80/20 reader handoff when:

- Barry can read the complete main and SI package;
- every material decision is visible;
- validation is proportionate and green; and
- remaining work is submission-form entry, public release, optional
  production polish, or another human decision.

Do not spend Goal 016 on optional cover-art design, speculative portal fields,
perfect production exports, code-publication implementation, or repeated prose
polish.

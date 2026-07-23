# Plan: Goal 013 RSEC Manuscript Consolidation

## Purpose

Produce one high-value manuscript revision that aligns the accepted DSIPA
science with the RSEC Original Research format. Preserve all accepted analyses
and use the revision to clarify the estimand, eligibility, management use, and
observation-process limitations.

## Steps

1. Confirm the baseline.
   - Record `pwd`, branch, HEAD, remote-tracking HEAD, status, and packet
     presence.
   - Stop if the required clean baseline differs.

2. Reconstruct the evidence and journal contracts.
   - Read the full Goal 013 packet.
   - Read the current manuscript and all manuscript tables/captions.
   - Read Goal 012 closeout and reference contract.
   - Read the accepted Layer B modelling, QC, scope, and licence reports.
   - Record the RSEC word, abstract, keyword, structure, and accessibility
     constraints.

3. Build a pre-edit claim and display map.
   - Map each main quantitative claim to its accepted source.
   - Mark overclaims, stale values, duplicate material, and unsupported
     interpretation.
   - Record current section word counts and display order.
   - Decide which existing displays move between main and Supporting
     Information without altering image files.

4. Revise the scientific spine.
   - Apply the exact title.
   - Make Layer A primary throughout.
   - Define dark-sky integrity as an operational detectable-radiance
     assessment.
   - Centre eligibility, floor domination, concentrated change, and the
     corrected unprotected-land comparison.
   - Replace ranking language with categorical screening.
   - Keep rings explicitly conditional.

5. Compress and correct Layer B.
   - State the microbat-versus-passerine record-identity response.
   - Explain surrogate motivation and specialist/acoustic observation.
   - State what provider matching cannot control.
   - Treat ALAN shuffles as null benchmarks rather than proof of confounding or
     non-robustness.
   - Move extended secondary detail to Supporting Information.

6. Reconcile the manuscript package.
   - Update main and supplementary captions/tables.
   - Correct 1,427/12.8% to accepted 1,432/12.9%.
   - Check all display citations, numbering, and ordering.
   - Make data-accessibility wording accurate without claiming a DOI or
     redistributing raw/row-level ALA data.
   - Repair citations only if necessary and supported.

7. Validate the core revision.
   - Record abstract, main-text, and keyword counts.
   - Run stale-number, terminology, inference, Layer B, data-accessibility,
     citation, and display-order scans.
   - Compare every quantitative claim with accepted evidence.
   - Run `git diff --check`, `make ms-check`, and `make ms-build`.

8. Perform one focused scientific self-review.
   - Read the built manuscript in order.
   - Repair only material story, evidence, interpretation, or assembly defects.
   - Repeat affected validation.
   - Stop rather than iterating on marginal prose polish.

9. Close out and wake the orchestrator.
   - Write the chronological log.
   - Write the required closeout.
   - Append the goal log.
   - Send the closeout path and stop without committing or pushing.

## Review Priorities

In descending order:

1. scientific and statistical correctness;
2. agreement with accepted evidence;
3. coherent Layer A-centred contribution;
4. bounded biological inference;
5. RSEC compliance and data accessibility;
6. display hierarchy and readability; and
7. prose polish.

## Non-Goals

No new analysis, 2025 VIIRS, modelling, data processing, figure generation,
source-code change, release-manifest repair, archive/DOI work, packaging,
submission, remote compute, or commit/push.

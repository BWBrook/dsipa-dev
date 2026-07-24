# Plan: Goal 014 RSEC Release Candidate — Option B Archive

## Purpose

Assemble one internally validated RSEC release candidate from accepted Goal
011–013 evidence. Keep archive recovery, release reconciliation, build
provenance, and submission preparation separate but cross-checked, with every
external action blocked pending later authorization.

## Execution Steps

1. Confirm the exact baseline.
   - Record `pwd`, branch, HEAD, `origin/main`, status, and the packet.
   - Stop for any divergence from clean `main` at
     `f5788ea4ad62237a95bf323930ec477107e7c2f3`.

2. Read the contracts and historical decisions.
   - Read `AGENTS.md`, this packet, Goal 010/011/012/013 records,
     `settings/layerA_reference_contract_v0_3_0.json`, active release reports,
     build configuration, manuscript assembly, and RSEC/Zenodo source links.
   - Build a claim, file, and external-action map before mutation.

3. Recover the accepted archive candidate.
   - Narrowly rsync the read-only Goal 011 payload to the ignored candidate
     directory.
   - Verify exactly nine allowlisted payload files, each Goal 011 hash and
     size, the `265,783,139`-byte total, six exact classifications, and the
     accepted radiance/edge/GPKG limitations.
   - Add only README, JSON manifest, and `SHA256SUMS`; prove no raw or
     row-level ALA content and never touch `data/processed/`.

4. Reconcile active release surfaces.
   - Correct active denominators/table/release-manifest surfaces to
     `1,432/12.9%`.
   - Create dated Option B manifest, Zenodo metadata, and checklist.
   - Narrowly update data, decisions, and stage-overview pointers while
     preserving Goal 010 blocked/history and Goal 011/012 reconciliation.

5. Implement Makedoc dual provenance with TDD.
   - Add DSIPA-owned manifest annotation and the minimal wrapper/config hooks.
   - Preserve upstream `git` as tool identity.
   - On successful `check`/`all`, refresh repository and build-tool
     sha/branch/dirty fields; on failure, propagate and annotate nothing.
   - Run focused provenance tests, then full `make test`.

6. Prepare RSEC submission assets.
   - Set the exact title and Original Research type.
   - Make the submission profile main-only and add the supplementary profile.
   - Add README/checklist, counts/running-title metadata, cover-letter and
     declarations drafts, and supplementary frontmatter.
   - Keep submission author/order/affiliation/correspondence visibly pending,
     and treat the final-format SI PDF as authoritative.
   - Mark all Barry-confirmed fields; invent no declarations, rights, DOI, or
     science.

7. Build and validate the candidate.
   - Run the prescribed tests and builds, provenance failure test, candidate
     checksum/allowlist checks, active/historical scans, title/count/word/
     abstract/keyword/citation/display checks, and main/SI separation checks.
   - Perform one focused repair pass only when a material defect is found.

8. Close out and stop.
   - Write `RSEC_Release_Candidate_Closeout.md`,
     `docs/log/134_rsec_release_candidate.md`, and the Goal 014 log entry.
   - Run only the final `git diff --check` and exact footprint check required
     for packet handoff. Do not commit, push, upload, reserve/mint a DOI, tag,
     release, log into Wiley, submit, pay, or agree to OA terms.

## Review Priorities

1. archive identity, allowlist, hashes, sizes, and ALA exclusion;
2. preservation of accepted science and active-versus-historical values;
3. provenance correctness and failure behavior;
4. main/SI submission separation and RSEC contract;
5. honest human-confirmation and external-action gates; and
6. concise release documentation.

## Stop Conditions

Stop and report the evidence if any source/hash/allowlist mismatch, raw or
row-level ALA leakage, new science, unsafe rights or licence claim, scope
expansion, failed upstream command with annotation, or failed acceptance gate
remains after one focused repair.

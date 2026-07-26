# Plan: Goal 015 Zenodo DOI Release And Final Data Citation

## Purpose

Move the accepted Option B Layer A candidate from a local, checksum-proved
release candidate to one verified public Zenodo Dataset record, while keeping
human identity, institutional rights, draft creation, irreversible
publication, final citation edits, and Git publication as separate decisions.

## Gate A: Packet And Confirmation

1. Prove the packet-authoring baseline.
   - Require clean `main` at
     `37ccb4e0f33bc921a09baa06d908f2b8ce284d87`, equal to `origin/main`.
   - Stop for any pre-existing change or divergence.

2. Create only the five Goal 015 files.
   - Define exact archive identity, phase gates, mutation boundaries,
     verification, and stop rules.
   - Present `Release_Confirmation_Sheet.md`.
   - Perform only Markdown/footprint checks; do not rehash, build, test,
     package, commit, push, access Zenodo, or use network services.

3. Wait for Barry.
   - Require explicit creator/ORCID/affiliation/sole-creator confirmation.
   - Require exact rights-holder wording and confirmation of authority or
     approval to release under the selected licence.
   - Require funding/grant details or an explicit `none`.
   - Require approval or amendment of every recommended metadata default.
   - Gate B remains closed unless Barry writes `authorize draft`.

## Gate B: Draft, Files, Metadata, And Reservation

4. Re-establish a controlled start.
   - Re-read the packet, Goal 014 evidence, confirmation response, official
     Zenodo guidance, current Git state, and candidate manifest.
   - Record the accepted packet commit/state and stop for unrelated changes.
   - Keep credentials, account identifiers, tokens, and 2FA material outside
     the repository and logs.

5. Revalidate the frozen candidate.
   - Prove exactly nine allowlisted payloads plus three companions.
   - Verify 9/9 SHA-256 values, nine-file byte total `265,783,139`, six
     exact/three accepted non-exact classifications, categorical-screening
     wording, and zero raw/row-level ALA or Layer B files.
   - Stop on any mismatch. Do not regenerate or substitute.

6. Decide and prove the file presentation.
   - Check current Zenodo file guidance and the live draft interface.
   - Do not assume nested relative paths are preserved.
   - Prefer 12 direct files because the deposit is below the 20-or-more ZIP
     recommendation.
   - If paths cannot be preserved, create a separate ignored flat staging view
     with nine byte-identical, uniquely named payloads and three
     deposit-specific companions mapping them to accepted relative paths.
   - Use a ZIP only for a documented functional constraint, never as casual
     repackaging.

7. Prepare and inspect the final draft.
   - Use the Barry-confirmed Dataset metadata, description, creator, ORCID,
     affiliation, rights holder, CC BY 4.0 licence, access, version, keywords,
     attribution, funding state, and related identifiers.
   - Identify the GitHub URL as private source provenance, not public access
     or a DOI.
   - Create the Zenodo draft and upload the exact 12 logical files.
   - Reserve a DOI only if needed for the pre-publication citation and covered
     by Barry's `authorize draft` instruction.
   - Download and SHA-256 verify all nine uploaded payloads when feasible.
   - Capture exact draft evidence and show it to Barry. Do not publish.

## Gate C: Irreversible Publication

8. Wait for a second Barry decision.
   - Gate C requires a new, separate instruction containing the literal word
     `publish` and referring unambiguously to the verified Goal 015 draft.
   - `proceed`, approval, silence, draft authorization, upload success, or DOI
     reservation never opens Gate C.

9. Recheck and publish once.
   - Re-open the draft and compare its 12 files and all metadata with the
     accepted Gate B evidence.
   - Correct nothing silently. Stop and return to Barry if any state differs.
   - When the state matches and explicit publication authority exists,
     publish once.
   - Stop on service error or ambiguity; do not create or publish a duplicate.

## Gate D: Public Proof, Reconciliation, And Git Publication

10. Independently verify the public record.
    - Resolve the DOI and inspect the public record without relying only on the
      authenticated draft.
    - Download all public files when feasible and verify all nine payload
      SHA-256 values, byte sizes, the 12-file presentation, and companion
      consistency.
    - Verify creator, ORCID, affiliation, title, description, publication
      date, version, access, licence, rights holder, keywords, provenance,
      attribution, and canonical citation.

11. Reconcile only the authorized tracked surfaces.
    - Replace pending archive state with the actual DOI, URL, public date,
      version, licence, and Zenodo citation.
    - Update the repository landing-page release/data-accessibility paragraph
      without implying that the private source repository is public.
    - Update only the manuscript Data accessibility section and narrow RSEC
      data-identifier fields.
    - Recompute only the tracked Data accessibility word count if the final
      DOI wording changes it.
    - Keep raw/row-level ALA and Layer B exclusions explicit.
    - State that the Zenodo data record is public while the GitHub source
      repository remains private.
    - Update confirmed author metadata only when Barry supplied the exact text.
    - Append the Goal log and one chronology log.

12. Validate the RSEC package.
    - Run focused RSEC/provenance tests.
    - Check and rebuild `draft`, `submission`, and `supplementary` profiles.
    - Review generated provenance, citation text, display integrity, and exact
      changed footprint.
    - Perform at most one focused repair for a material defect.

13. Review, commit, and push.
    - Give the orchestrator the public-record evidence, exact diff, tests,
      builds, residual risks, and final Git state.
    - Only after acceptance, stage exact paths, inspect the staged diff, commit,
      fetch/prune, prove a safe fast-forward, and push `main`.
    - Confirm local HEAD, upstream, `origin/main`, and remote `main` agree and
      the worktree is clean.

## Review Priorities

1. irreversible-publication authority;
2. institutional rights and licence authority;
3. payload identity, hashes, bytes, and exclusion boundaries;
4. exact public record metadata and citation;
5. honest distinction between public Zenodo data and private source code;
6. narrow manuscript/release edits and RSEC rebuild integrity; and
7. exact Git footprint and post-push reconciliation.

## Efficiency And Stop Policy

Use one core execution pass and one focused repair only when evidence shows a
material defect. Stop when another pass would only polish wording or repeat a
check without new evidence. Any mismatch in identity, rights, authorization,
publication state, or public verification is a hard stop rather than a prompt
for improvisation.

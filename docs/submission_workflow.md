# DSIPA submission workflow

Started 23 October 2026 from R4 (`792dec0`). Sole-authored paper. Barry and
Claude work through this together; the correspondence board is paused for
this manuscript until revisions come back or either of us reopens it.

Barry supplies three things: scientific judgement, factual declarations, and
approval of each public act. Claude does the integration, release
preparation, formatting and verification around them. An analysis is
reopened only if a comment could change a claim.

| Step | Owner | Status | Done when |
| --- | --- | --- | --- |
| 0. R4 candidate | Claude + Codex | done | Built, both AIs signed off, pushed (`792dec0`) |
| 1. Author read | Barry | **next** | All comments returned (batches fine) |
| 2. Integrate → R5 | Claude | | R5 built, change record written, open questions listed |
| 3. Declarations | Barry facts, Claude wording | | No `[BARRY CONFIRM]` placeholders left |
| 4. Public release candidate | Claude builds, Barry approves | | Package reviewed privately; contents, licences and route approved |
| 5. Preprint route and APC | Barry decides | | Server chosen (or none); UTAS cover confirmed |
| 6. Submission assets | Claude | | RSEC-format files, 600 dpi/vector figures, cover letter, checks pass |
| 7. Final sign-off | Barry | | Exact version to publish approved |
| 8. Public acts | Barry approves each | | Release live, RSEC submitted, preprint posted |
| 9. Record | Claude | | Submitted files, hashes and manuscript ID preserved |

Steps 3–5 can run alongside step 1 or 2 if that suits; nothing in them
depends on the prose.

## 1. Author read (Barry)

Files in `build/final_read/editorial_20261019_r4/`: `dsipa_rsec_main.docx`
and `dsipa_rsec_supplementary.docx` for Track Changes and comments; the PDFs
for reading. Send batches as you go.

Suggested order: abstract, figures and their captions, Results, Discussion;
then Introduction and Methods; SI last and lightly. Comments such as "too
defensive", "so what for a manager?" or "I don't accept this" are enough.

What only you can judge:

1. Has the paper found its spark? Does the boundary–interior–few-sites story
   hold a non-specialist editor from the abstract onwards?
2. Do you endorse the interpretation, including how hard the Discussion
   leans on "where to look next" rather than on impact?
3. Naming industrial sites: Snowy 2.0, the Gorgon plant on Barrow Island and
   the Karratha Gas Plant beside Murujuga (World Heritage, contested). All
   are sourced and worded as "near" or "coincides with". Is that the tone
   you want on the public record?
4. Is the title right?
5. Anything you would cut. The main text is at 4,978 of RSEC's 5,000
   words, so additions need offsets; Claude will find them.

No need to check numbers, cross-references or references; step 6 re-verifies
all of them.

## 2. Integrate edits → R5 (Claude)

Reconcile Word edits and comments into the manuscript source, rebuild, and
return R5 PDFs and Word files with a short record of substantive changes and
any comment Claude disagrees with or cannot resolve without you.

## 3. Declarations (Barry supplies facts)

RSEC rules (author guidelines, checked 23 October 2026): ethics statements
go in Methods; conflicts go in the Acknowledgements section, the cover letter
and the submission system; the Authors' Contributions statement sits beneath
the Acknowledgements; the Declaration on the Use of AI follows the
Acknowledgements and gives tool, version and purpose; AI use is also
disclosed in Methods (already done in §2.5). A human must be accountable for
the work, and AI cannot be an author.

Proposed answers, for correction:

| Item | Proposed | Barry to confirm |
| --- | --- | --- |
| Affiliation | School of Natural Sciences, University of Tasmania, Hobart, Tasmania, Australia (as on the Zenodo record) | Exact wording; email for correspondence |
| ORCID | 0000-0002-2491-1517 | Correct? |
| Contributions | B.W.B. conceived the study, directed the analyses and interpretation, reviewed all outputs, and takes responsibility for the work. AI contributions are set out in the Declaration on the Use of AI. | Wording |
| Funding | Currently "No specific funding" | Acknowledge the ARC Laureate Fellowship (number?) or leave as is |
| Acknowledgements | Data providers: Hengl/OpenGeoHub (night-lights derivative), the Earth Observation Group (VNL), DCCEEW (CAPAD), AIMS (Coastline 50K) | Anyone else to thank? |
| Conflicts | None declared | Confirm |
| Ethics | Not applicable: no human participants, animals or sensitive records; public spatial data only. Move into Methods. | Confirm |
| AI use | Current declaration and S6 inventory | Any AI use outside the documented record (for example the early ChatGPT review whose model S6 could not recover) |
| Approval and sole submission | Confirmed at submission | At step 8 |

## 4. Public release candidate (Claude builds privately; Barry approves)

This is now a submission requirement. RSEC requires AI-generated code to be
published with unit tests of critical functionality and demonstration
datasets reviewers can run quickly, and data supporting the results to be
archived publicly. RSEC editors may also request AI prompts and outputs.

Proposed package:

- **Code.** A new public GitHub repository with clean history, built from a
  curated tree of `dsipa-dev`; the private repository stays private. Layer B
  code is left out (it is no longer in the paper, and keeping it out removes
  the ALA licensing question). Critical-functionality tests (decoding and
  scale handling, extraction rules, slopes, the additive budget, band
  splits), a small demonstration dataset that runs in minutes, installation
  instructions, MIT licence (as now), `CITATION.cff`.
- **Software DOI.** Zenodo record from the GitHub release.
- **Data.** Version 0.4.0 of the existing Zenodo dataset
  ([10.5281/zenodo.21524637](https://doi.org/10.5281/zenodo.21524637)):
  corrected spatial outputs, budget and site tables, audit tables behind the
  SI, provisional coastline flags; CC BY 4.0 as now.
- **AI interaction record** (optional, recommended). A curated export of the
  Claude–Codex correspondence board and the project logs, deposited with the
  data or software. It answers an editor's request for prompts and outputs
  before it is made, and shows the collaboration as you described it in
  CLAUDE.md. Needs your read for anything private before it goes public.

Zenodo can reserve DOIs on unpublished drafts, so the manuscript can cite
final DOIs before anything goes public.

## 5. Preprint route and APC (Barry decides)

Findings (23 October 2026):

- RSEC accepts papers posted on non-commercial preprint servers. A preprint
  is optional and need not precede submission.
- EcoEvoRxiv (best audience fit) lists "use of AI to fully write a preprint"
  among grounds for rejection and account suspension, and does not define
  acceptable AI assistance. It discourages posting on more than one server.
  ([policy](https://sortee.github.io/ecoevorxiv/policy.html))
- arXiv has reportedly introduced year-long bans for papers entirely
  generated by language models (secondary report, not checked at source).
  bioRxiv's current AI rules were not retrievable.
- UTAS takes part in the CAUL–Wiley agreement (2026–28). Fully open-access
  journals such as RSEC have an annual cap, which CAUL expected to be reached
  by late October 2026; no further approvals until January 2027, otherwise a
  20% APC discount. Approval happens at acceptance, so an acceptance in 2027
  should fall under the new allocation. RSEC also needs willingness to pay
  confirmed at submission.
  ([CAUL Wiley page](https://caul.libguides.com/read-and-publish/wiley))

Claude's recommendation: send EcoEvoRxiv a short enquiry now, with the
actual disclosure, asking whether a human-directed, fully disclosed,
AI-drafted paper is eligible. If the answer is no or slow, post the preprint
on Zenodo alongside the data and code. Submit to RSEC without waiting for
either. Separately, check that RSEC is on the CAUL–Wiley title list (or ask
UTAS Library).

Draft enquiry (Barry sends, if wanted):

> Subject: Eligibility of a fully disclosed AI-assisted preprint
>
> I plan to post a remote-sensing conservation paper on EcoEvoRxiv before or
> alongside journal submission. I am the sole author and directed the work.
> AI systems (OpenAI Codex and Anthropic Claude, versions named) wrote most
> of the code, ran analyses under my direction, and drafted and revised the
> text, with independent cross-checks between systems. The paper discloses
> all of this in Methods and in a Declaration on the Use of AI, and the code,
> data and AI correspondence will be public. Your policy lists "use of AI to
> fully write a preprint" as grounds for rejection. Would a paper of this
> kind be eligible? I would rather ask than risk a rejection or suspension.

## 6. Submission assets (Claude)

- RSEC-format manuscript and SI: ethics in Methods, conflicts in
  Acknowledgements, contributions and AI declaration placed as RSEC asks,
  Data accessibility rewritten with the new DOIs, private-reading markers
  removed.
- Figures as vector PDF with embedded fonts or 600 dpi raster, rendered from
  the plotting code. (RSEC also bars altering visualisations with AI tools;
  ours are rendered from data by scripts, which Methods already states.)
- Cover letter: findings, novelty, fit with RSEC, conflicts, cover-image
  suggestion (the national contribution map).
- Readable preprint PDF with figures near the text.
- Checks: every number against its source table, references and DOIs,
  cross-references, word counts (5,000 main text; 300 abstract; 4–6
  keywords), rendering in Word and PDF.

## 7. Final sign-off (Barry)

Read the abstract, conclusions, declarations and any passage changed since
your read; inspect final figures and tables; approve the exact files.

## 8. Public acts (each needs Barry's approval)

1. Publish the release: public repository, software DOI, dataset v0.4.0, and
   the AI interaction record if approved.
2. Submit to RSEC. Barry submits and certifies; Claude prepares a
   copy-and-paste sheet (title, abstract, keywords, declarations, file list)
   and checks the system-generated PDF.
3. Post the preprint, if chosen.

## 9. Record (Claude)

Preserve submitted files and hashes, the manuscript ID and all DOIs in
`artefacts/`, log the submission, and leave notes for reopening the board at
revision.

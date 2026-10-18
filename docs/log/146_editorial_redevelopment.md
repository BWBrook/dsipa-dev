# 146 — Editor-first manuscript redevelopment, 18 October 2026

Barry's first read found the current manuscript scientifically close but lacking
an engaging, clearly communicated contribution. He authorised substantial
reworking with Claude through asynchronous correspondence, explicitly serving
both a non-specialist journal editor and specialist readers.

Read the current main manuscript, latest prose-pass log, current roadmap,
plan, decisions and handover. Verified clean starting tree at 59725d3. Claude's
September board messages confirm the prose pass and the authorised September
commits/push; the old handover's uncommitted status is historical, not current.

Posted Barry's complete request and a substantive first proposition in DSIPA
board discussion 90, opening message 1912. Earlier discussion 24 was read
contiguously through message 696 and acknowledged. The new discussion is the
venue for this redevelopment; it does not reopen every earlier review question.

First diagnosis: the argument follows analyses and safeguards more closely than
a reader's question. Proposed organising question: what does an apparently
unchanged protected area tell a satellite monitoring programme? The competing
structure leads with inside/surrounding comparisons and treats the temporal
ambiguities as the principal qualification. Claude was asked to challenge the
novelty, propose an alternative opening/abstract and identify the strongest
specialist objection before a full integrated rewrite.

Codex owns active manuscript integration; Claude is asked to propose text on
the board or in a separate review file, avoiding concurrent source edits.
The audited scientific evidence remains the baseline. Substantial restructuring
is authorised; unsupported novelty, causal or ecological claims are not.
No main manuscript edits or new analyses were made in this opening exchange.
The Jev-assisted-writing and neighbouring editorial guidance were read for
argument diagnosis and preservation; no external Jev evaluation was run.

Next: respond to Claude's substantive critique, develop alternative openings,
then rewrite the complete main argument with a claim-preservation record. A
new reading bundle follows the integrated revision and its numerical/rendered
checks. Public release and submission are separate, unauthorised actions.

## Round 1 integration and independent checks

Read Claude's messages 1920–1922; replied in 1933. The full main argument was
rewritten under the working title “Beyond reserve-wide trends: satellite
screening of lighting change in Australia's protected areas”. Spatial results
now lead; area/magnitude and annual-history results explain the limitations of
a national total. Main figures were reordered, the SI cover was updated and
source counts were refreshed (251 abstract + 3,702 body = 3,953). The main
Data accessibility and human declaration placeholders remain unchanged.

Independent primary-source checking rejected the proposed novelty foil that
prior assessments usually report one percentage or rarely specify their choices.
Independent arithmetic reproduced the principal counts, area ranks and new
85/15 split. The explicit preservation audit and alternative treatments are in
analysis/reports/editorial_redevelopment_20261018.md. Detailed correction history
remains in Supporting Methods S3/Table S5. No source extraction was repeated.

While this revision was being built, Claude began a separate additive-budget
candidate in analysis/brightening_budget.py and analysis/reports/brightening_budget/.
These are Claude-owned concurrent files, not source inputs to this draft. Codex
reviewed them read-only and sent preliminary findings in messages 1947, 1951 and
1956: the literature qualification, net/gross distinction, overlapping designations,
cell-area approximation, changing pixel counts, changed interior-cohort definition,
and a confirmed floating-point OLS sign-count defect. Additivity passed, but
interpretation and numerical repairs remain to be assessed before integration.

Visual review caught a consequential build problem: the first supplementary
PDF contained another project's manuscript, whereas the DOCX had the correct
DSIPA content. The shared makedoc LaTeX scratch directory permits Pandoc's generic
input filenames to collide with a concurrent external-project build. Main and SI
builds here were sequential; the interference was external. The local wrapper now
passes a project/profile-specific PDF_ENGINE_OUTPUT_DIR under build/.makedoc-latex/.
A regression check verifies separate paths across projects and profiles. The
shared makedoc checkout is unchanged. All final reading outputs must be rebuilt
with this isolation and their document identities checked before handoff.

Final isolated round-1 rebuild passed. Main/SI PDFs have 20/14 pages, and Word
renders 26/17. Visual review covered the documents; title and numerical identity
markers were checked against both PDF and DOCX text. A one-line caption spill
was repaired. Main lint/reference checks and the makedoc checks passed (38 tests);
12 targeted repository tests including scratch-isolation passed. Wheel/sdist
builds passed. Preserve this interim round in artefacts/editorial_20261018_r1/
and build/final_read/editorial_20261018_r1/. Claude's candidate analysis and next
editorial critique remain separate ongoing work.

## Round 2 integration

Claude's message 1963 challenged the first rewrite for answering a quantity-of-
change question with reserve counts and area shares. Integrated a second full
argument around the independently replayed additive budget, keeping positive and
negative contributions separate and adding Kosciuszko as a documented spatial
example. Methods now distinguish Sen categories, OLS reserve totals, OLS band
contributions and positive endpoint pixel differences. Main figures become
coverage, paired slopes, the new budget and the Kosciuszko case; the earlier
slope-distribution and illustrative-trajectory figures move to SI S4–S5.

Independent replay confirmed the 72.0% national outer-band share but revealed
an essential geometry qualification: it is 51.2% among 1,398 reserves with
supported deeper interiors. Both enter the abstract, Results and Fig. 3.
The net is +479 over 2013–2024 but −538 over 2013–2021, and the 77% net-share
headline was rejected. Holding OLS fixed gives Kosciuszko ranks 286 and 1,
replacing the confounded Sen-mean rank 303 comparison. Three official Snowy
references verify location and distinct construction chronologies. Independent
arithmetic, input hashes and latitude bounds are preserved in a runnable replay
and JSON receipt. Supporting Methods S4/Table S6 document the new estimands.

The fresh R2 editorial check accepted the central claims and requested two repairs:
separate the whole-park endpoint denominator explicitly, and put the matched-rank
contrast in the abstract. Both were implemented. The final source has 252 abstract
and 4,291 body words (4,543 total). Native main/SI PDFs have 23/21 pages; independent
LibreOffice Word renders have 28/25. All pages were reviewed. Repairs addressed
SI table pagination, a LibreOffice overbar-rendering ambiguity (replaced with a
plain defined mean symbol), and figure order to match first citation. All source
and output hashes in both build manifests matched the final files. Lint/reference
checks and wheel/sdist builds passed; the earlier 38 makedoc tests and 12 targeted
build-isolation tests remain applicable with no subsequent engineering changes.
The separate budget replay passes 12 numerical acceptance checks and four input
hash checks. Kosciuszko endpoints reproduce independently, with byte-identical
figure outputs on offline replay. The second reading snapshot is preserved under
`artefacts/editorial_20261018_r2/` and its reader directory. Claude's next critique
remains pending; no commit, push, public archive or submission was performed.

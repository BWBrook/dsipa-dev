# Independent Astra adversarial review — commission

Barry requested a full adversarial review of the current research repository
and accompanying paper before his own editing pass. The purpose is to find
concrete further grounds for revision or identify claims that withstand a fresh
external-review challenge. Neither outcome is prescribed.

Reviewer configuration: `gpt-6-astra`, reasoning `max`, `fork_turns="none"`.
The reviewer was given the repository path, current main/SI reading-file paths,
target journal, review remit and execution boundaries. No previous scientific
conclusions, prior reviewer verdicts or list of suspected weaknesses was supplied.
The reviewer was instructed not to use personal memory, correspondence-board
messages or other agents, and to form provisional criticisms from the paper
and direct evidence before consulting previous review/handover judgements.
Repository instructions remain applicable, so this is a fresh-context review,
not a claim that all prior project context is technically inaccessible.

Scope: scientific contribution and journal fit; data/measurement provenance;
design, estimands, statistics and uncertainty; selection and sensitivity;
scientific/ecological inference; agreement of prose, tables, figures, code and
evidence; reproducibility and material implementation defects; clarity for an
external reader. Distinguish actual errors from defensible choices, adequately
disclosed limitations and optional extensions. Require evidence and bounded
remedies for material findings; passing tests alone does not validate science.

Review mode: read-only scientific/code inputs. Lightweight non-destructive checks
and source verification permitted. No expensive reruns, downloads, publication,
commits or implementation. A sustained remote check requires tmux; no heavy
work on the WSL laptop. Reviewer may write only its report and temporary scratch
files, and was instructed not to delegate further.

Requested output: referee-style recommendation; ranked BLOCKER/MAJOR/MINOR
findings with exact evidence; proposed remedies; claims surviving scrutiny;
commands executed and evidence/access limitations; account of independent first
impressions. Report: `astra_adversarial_review_20260918.md`.

Parent role: record review scope and immutable-input hashes, then assess the
reviewer's concrete criticisms against evidence after receiving the report.
No manuscript revision is authorised by this review commission alone.

The initial snapshot is `astra_adversarial_review_20260918_scope.json`.
It records 466 working-tree files and five reading artefacts. The supplied main
and SI PDF/DOCX exactly matched current builds. The existing canonical reading
snapshot's 187 files passed hash verification at commissioning.

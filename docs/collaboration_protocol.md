# Collaboration protocol (PI ↔ Codex ↔ human)

This repo is run as an autonomous “AI for Science” project.

Roles:
- Codex CLI (agent): implements the roadmap end-to-end, including tests, artefacts, and manuscript draft.
- PI (ChatGPT): reviews repo ZIP snapshots and issues high-level critique + roadmap revisions.
- Human scientist: runs Codex locally, uploads repo ZIPs at review gates, answers targeted questions if blocked.

Operating loop:
1) Human instantiates the repo with this harness and runs Codex.
2) Codex reads `AGENTS.md`, then follows `docs/roadmap.md` strictly (first unchecked WP).
3) Codex records decisions in `docs/decisions.md`, writes logs in `docs/log/`, and interpretation notes in `docs/interpretation_notes.md`.
4) At review gates in `docs/roadmap.md`, the human zips the repo and remembers to include generated artefacts/reports (not large raw rasters unless essential).
5) PI reviews the ZIP and returns:
   - conceptual critique,
   - “Round N revisions”,
   - and (if needed) updates to `docs/roadmap.md` and/or `docs/plan.md`.
6) Codex executes the revised roadmap. Repeat until manuscript-ready.

Policies:
- No low-level shell command relay: the agent must make the repo runnable and document run entrypoints in-repo.
- Minimal questions to the human: only when blocked, at a major fork, or after repeated sanity failures.
- “Artefacts first”: every WP produces inspectable artefacts plus sanity/interpretation notes.

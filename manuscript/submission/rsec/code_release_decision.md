# Pre-Submission Code-Release Decision

Status: decision memo only. `dsipa-dev` remains private, and Goal 016
authorizes no public action.

## Observed Current Condition

- Nine processed Layer A outputs are public in the Zenodo Dataset at
  <https://doi.org/10.5281/zenodo.21524637>.
- That DOI identifies a Dataset, not software.
- The `dsipa-dev` source repository, complete runnable environment, and
  derived Layer B materials are not publicly archived.
- Raw and row-level ALA records are not redistributed because provider terms
  are mixed. Exact Layer B reconstruction requires reacquisition under those
  terms.
- The internal pipeline is versioned, scripted, tested, pinned to source
  identities, and supported by manifests. Those internal controls do not by
  themselves provide public reproducibility.

## Policy Evidence And Uncertainty

The current RSEC/Wiley source evidence summarized in the Goal 016 packet
supports a general expectation that analytical scripts and supporting
artefacts be public whenever possible. Current source-informed evidence also
suggests that AI-assisted analytical code may require public code, critical
tests, and demonstration data.

That second consequence is conditional. It depends on Barry's factual AI-use
disclosure and on how the live Research Exchange workflow or editor applies
the policy to this manuscript. Goal 016 did not inspect the live workflow,
contact an editor, or establish a definitive requirement.

## Routes For Barry

### Curated Public Release

The preferred later route is a new, clean-history public repository rather
than changing the visibility of `dsipa-dev`. A separately authorized goal
would:

- define a reviewed code-only allowlist;
- complete licence, copyright, and provenance review;
- remove internal management, infrastructure, contact, and submission
  material;
- include critical unit tests and runnable demonstration data that do not
  redistribute restricted ALA rows;
- provide installation and non-interactive run instructions;
- prove clean-clone execution against the public Layer A data citation;
- publish a versioned release; and
- archive that release as a separate Zenodo Software record with its own DOI
  and an explicit citation link to the manuscript and Layer A Dataset.

Benefits are a citable software object and a clear public reproduction path.
Risks are the extra review burden, accidental disclosure if curation is weak,
licence or authorship mistakes, and delay if attempted inside the manuscript
submission goal.

### Keep Private And Seek Guidance

The alternative is to keep source and derived Layer B materials private,
describe the limitation exactly, and request editorial guidance before
submission. This avoids a rushed release and preserves the restricted-data
boundary, but may be judged insufficient for code or AI-transparency
expectations and could delay review later.

## Decisions Required

Barry should confirm:

1. the factual AI-use record by research role, tool, version, purpose, and
   access date;
2. whether to authorize the curated public-release route before submission or
   retain private code and seek editorial guidance;
3. which Layer B code and derived outputs may enter a public package without
   exposing restricted occurrence rows;
4. software authorship, copyright holder, and institutional release authority;
   and
5. whether the timing risk is acceptable relative to the manuscript plan.

No public repository, visibility change, software archive, DOI, tag, release,
editor contact, or other external action has been performed or authorized.

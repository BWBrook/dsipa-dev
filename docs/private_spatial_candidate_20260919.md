# Private spatial candidate preparation — 2026-09-19

`analysis/package_spatial_candidate.py` prepares a private, curated candidate
for review. It does not publish, commit or push. It seals only a private file inventory. The candidate
contains the current corrected Layer A processed outputs and audit reports,
spatial synthesis/comparison receipts, selected source code, focused tests,
settings, manuscript source/figures, references, and explicit runtime/input
manifests. It excludes raw VIIRS rasters, ALA occurrence data, credentials,
SSH configuration, Git metadata, internal correspondence, and unrelated
historical reports.

The public Zenodo deposit (`10.5281/zenodo.21524637`) is a historical processed
baseline. The candidate's nine processed files are the current corrected private
outputs staged under canonical `data/processed/`;
they must not be described as the public Zenodo payload or as a public release.
Layer B research archive inputs remain omitted. Numerical manuscript outputs
are included only where already present in the curated manuscript source and
current audit receipts.

Run from the repository root:

```text
uv run python analysis/package_spatial_candidate.py \
  --root /home/bwbrook/papers/dsipa-dev \
  --output /home/bwbrook/papers/dsipa-dev/artefacts/spatial_candidate_20260919 \
  --dry-run

uv run python analysis/package_spatial_candidate.py \
  --root /home/bwbrook/papers/dsipa-dev \
  --output /home/bwbrook/papers/dsipa-dev/artefacts/spatial_candidate_20260919 \
  --validate
```

The first command only reports the explicit allowlist count, bytes, and any
forbidden/missing paths. The second validates and copies the candidate, then
writes portable `SHA256SUMS` and `FILE_MANIFEST.json`. The frozen executed source snapshot is retained separately from the current
package source. Current files are identified by their own hashes. Git-free
manuscript builds verify FILE_MANIFEST.json and record its identity, without
inventing a Git commit. Final PDF/DOCX QA and the acceptance memo accompany
the sealed private candidate.

The corrected extraction and synthesis commands were run remotely on
`deep-server-ts` using the Goal 012 Python environment. The candidate records
their resulting manifests and hashes, while raw external dependencies remain
documented by source path and receipt rather than copied into the packet.

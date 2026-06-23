# Zenodo Release Checklist: Option B

Status: blocked. This checklist is a local readiness report only and does not
publish, compress, upload, mint, reserve, tag, release, or submit anything.

Generated: 2026-06-23 UTC by `nightlight` for Goal 010.

## Checklist

| Gate | Status | Evidence |
| --- | --- | --- |
| Barry/orchestrator Option B decision recorded | pass | Goal 010 packet records approval of Option B, Zenodo-style DOI route, and no raw/row-level ALA exception. |
| Repo-local contract read | pass | `AGENTS.md` and the full Goal 010 packet were read. |
| Starting git state recorded | pass | `pwd=/Users/bwbrook/papers/dsipa-dev`; `HEAD=b1c1539`; `origin/main=b1c1539`; status was `## main...origin/main` plus untracked Goal 010 packet. |
| Nine-file Layer A payload available | fail | Only `data/processed/pa_geometries_v0_3_0.csv` was found locally and in checked remote DSIPA paths. |
| Payload checksums verified | fail | One of nine checksums was verified locally; eight files were missing. |
| Local ignored staging directory created | blocked | No staging directory was created because the payload is incomplete. |
| Raw/row-level ALA excluded | pass | Four explicitly excluded ALA files were absent locally and were not staged, copied, compressed, uploaded, or included. |
| Baseline figure checksum classified | pass | Current accepted checksum `ef9d5ac7...` is documented as evidence-snapshot staleness relative to old `e30a5fc5...`. |
| DOI/archive external movement | pass | No DOI mint/reservation, archive upload, GitHub release, tag, PR, package, or submission action was performed. |
| Later external-upload/DOI goal ready | fail | Not ready until the eight missing Layer A payload files are recovered or separately regenerated and accepted. |

## Checked Payload Files

| Path | Expected SHA-256 | Current status |
| --- | --- | --- |
| `data/processed/pa_radiance_buffers_national_v0_3_0.csv` | `493c425c0de2a88773f55d49d99839c98dc0f6082749ccb5c95994583ff05d2e` | missing |
| `data/processed/pa_edge_profiles_national_v0_3_0.csv` | `9d77d1153d5c93789d7f78ae8ff5f28f8cd9d3c4526e853400abeb91cd757888` | missing |
| `data/processed/pa_buffer_validity_v0_3_0.csv` | `407283df182baff585dfe3b28b9450c5750c237d120d5d00aa3539a6227e3e25` | missing |
| `data/processed/pa_trends_v0_3_0.csv` | `d7d33e9cd49dea316355cba5a52afd85953f3b656ee8f2ab7e725c922800ff1f` | missing |
| `data/processed/pa_risk_rankings_v0_3_0.csv` | `554c02ea84d56119f47d13524ab7ec3add66851f61dae3c4f5ac9267da30367a` | missing |
| `data/processed/pa_geometries_v0_3_0.csv` | `781e80b08db4ed3378021ae51feb0c28f9fc7627195b4c208702ebecfdf6695b` | present and verified locally |
| `data/processed/pa_geometries_v0_3_0.gpkg` | `0476ffdc2cd5a609855a20a2af0f373aff25ca571ccc8138e4224e71deb00e11` | missing |
| `data/processed/pa_ibra_assignment_v0_3_0.csv` | `3f0d8f7cc206302a8d266ac747a20e89bd0ad0a724f8c7a3d2a161f0634a82cf` | missing |
| `data/processed/pa_trend_bootstrap_summary_v0_3_0.csv` | `cd3c165ed5857d0fb2fcb3be360fe89dfda6757c296fb5cd1bd7aee509078920` | missing |

## Stop Condition Hit

Goal 010 stop condition: required large files absent after the authorized
retrieval/staging path. External archive upload, DOI minting, release
packaging, GitHub release, and publication submission must remain blocked.

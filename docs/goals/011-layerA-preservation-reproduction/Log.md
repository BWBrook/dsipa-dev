# Log: Goal 011 Layer A Preservation Reproduction

## 2026-07-23 - Execution started

- `pwd`: `/Users/bwbrook/papers/dsipa-dev`
- Branch: `main`
- HEAD and `origin/main`:
  `7f46a00f74c32881034f0129728b3d80eedd2442`
- Starting status: clean (`## main...origin/main`).
- Repo-local and global `AGENTS.md` were read.
- Required repository, workflow, decision, Goal 010, reproducibility,
  evidence, data-provenance, pipeline, remote-harness, sync, and Goal 008-010
  convention files were read.
- Goal 010 established that only one of nine approved Layer A payload files
  remained recoverable, making unchanged regeneration the accepted next
  preservation step.
- Goal 011 packet created before remote mutation.
- Next: read-only `deep-server-ts` preflight, then an isolated checkout pinned
  to the accepted commit.

## 2026-07-23 - Immutable-input preflight blocked execution

- `deep-server-ts` resolved to `deep-server`; host capacity was suitable:
  64 CPUs, 125 GiB RAM, about 4.5 TiB free under `/data`, Python 3.12.3,
  user-local `uv` 0.11.14, and tmux 3.4.
- The only remote DSIPA checkout was dirty at
  `dab3ddb55d04cfbfd39deb35c5e9ed3274f5447e`; it was not modified.
- The accepted commit object was absent from that checkout and the documented
  legacy checkout `/home/bwbrook/papers/dsipa-dev` was absent.
- A bounded search under the permitted DSIPA paths found 0 nightlight
  GeoTIFFs, no accepted PA geometry GPKG, no IBRA GPKG, no Natural Earth
  shapefile/land cache, and no Layer A caches.
- The available PA geometry CSV matched its historical SHA-256, but was
  insufficient for polygon processing.
- The unchanged pipeline would redownload current CAPAD, IBRA, Natural Earth,
  and annual Zenodo inputs. This would not demonstrate unchanged reproduction
  of the accepted input snapshot, so no isolated checkout or tmux run was
  created.
- Recorded terminal `blocked_preflight` evidence under run id
  `20260723T060854Z-goal011-layerA-preservation-blocked`.
- Remote artefact path:
  `/data/codex/artifacts/dsipa/20260723T060854Z-goal011-layerA-preservation-blocked`.
- Corrected the Goal 011 runbook to use harness `custom` mode so
  `DSIPA_SKIP_LAYERB=1` will be propagated in a later run.
- Wrote the compact manifest, reconciliation report, closeout, and stage log.
- Validation passed for remote JSON, remote evidence checksums/presence,
  local JSON, nine historical-hash consistency, 11 accepted headline counts,
  tracked `git diff --check`, explicit untracked-file whitespace checks, and
  the allowed local footprint. One focused repair removed four extra EOF blank
  lines found only by the explicit untracked-file check.
- No source, test, scientific configuration, manuscript, figure, generated
  science data, commit, or remote user checkout was changed.

## 2026-07-23 - Controlled continuation authorized

- The orchestrator's independent provenance audit determined that controlled
  reacquisition can test the accepted analysis if it remains fail-closed.
- The earlier `blocked_preflight` run is retained as provisional Phase 1
  evidence, not the final Goal 011 outcome.
- Authorized gate:
  - stream the exact accepted source tree
    `c82ebdda83c987d2e1dcc79fb2dba2759f9d7739` (354 archive entries) from
    local `git archive`;
  - require CAPAD raw count 14,403 and semantic hash
    `148a813156bc1bb6b94bbf8a0455c517a951985ff03de6d8e18199dc627e53cf`;
  - require IBRA count 89 and semantic hash
    `3ba6e8e10f775a9643da6154bb7cd050a54dbb24ed545277d7ad2e05fb8fe332`;
  - require all 12 annual nightlight files to pass code-pinned MD5 values;
  - acquire Natural Earth from the unchanged official S3 URL, require size
    69,700 bytes and SHA-256
    `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`,
    and retain the historical-byte-pin limitation.
- No download or run was started before this authorization.

## 2026-07-23 - Controlled input gate passed

- Streamed the exact accepted source at commit
  `7f46a00f74c32881034f0129728b3d80eedd2442`, tree
  `c82ebdda83c987d2e1dcc79fb2dba2759f9d7739`, into the isolated remote
  sibling. The source archive contained 354 entries and had SHA-256
  `a0e9b77fb4f6e75d9dac9477a8fa6877b2956e8351e8b142531d7bdf6518b02e`.
- Final controlled run id:
  `20260723T062202Z-goal011-layerA-preservation`.
- The CAPAD gate passed at 14,403 raw features and the accepted semantic hash.
- The IBRA gate passed at 89 features and the accepted semantic hash.
- All 12 Zenodo/OpenGeoHub v0.4 annual rasters passed the unchanged
  code-pinned MD5 values.
- Natural Earth passed version marker `4.1.0`, size 69,700 bytes, and SHA-256
  `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de`;
  it remains classified as version-reacquirable but not historically
  byte-pinned.
- The first gate attempt used an incorrect run-local Natural Earth marker
  expectation; the second check misclassified expected generated input dirt.
  Both attempts and the final cached pass were preserved. No repository source
  or scientific method was edited.

## 2026-07-23 - Pipeline terminal and bounded QA repair

- Launched the unchanged pipeline through the existing tmux harness with
  `DSIPA_SKIP_LAYERB=1`, `DSIPA_WORKERS=12`, and the ten-code state list.
- National Layer A computation, trends, uncertainty, vulnerability, reports,
  and figures completed.
- The pipeline ended terminal `failed`, exit code 1, at QA. The clean source
  archive omitted two ignored smoke-triad GPKG fixtures, so 47 tests passed and
  2 failed before the build step.
- Applied the authorized validation-only repair: generated the missing
  fixtures with the existing `dsipa.triad --skip-artefact` module, then ran
  the existing full test and build commands.
- Full pytest passed: `49 passed in 6.89s`.
- Package build passed and produced both the wheel and source distribution.
- Scientific source integrity remained unchanged. Layer B was skipped.

## 2026-07-23 - Reconciliation complete

- Preserved all nine approved outputs under
  `/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation`.
- Six outputs match their historical SHA-256 exactly: buffer validity, trends,
  risk rankings, geometry CSV, IBRA assignment, and bootstrap summary.
- The radiance CSV is byte-different, but its schema/grain is valid and all
  accepted primary downstream outputs and headline values match. Historical
  row-level equality is unproven because the historical payload is absent.
- The geometry GPKG is byte-different. The pipeline and input-gate copies are
  identical in all attributes and geometry WKB after PA sorting, and the
  geometry CSV is historically exact. Historical feature-level equality is
  still unproven because the old GPKG is absent.
- The edge CSV has bounded secondary threshold-sensitive drift. The canonical
  edge-decision generator returned 0 and changed the 1-5 km valid PA count
  from 1,427 to 1,432; the dashboard's ring-1 non-null PA-years changed from
  116,472 to 116,412. Complete-ring n remains 383 and the edge figure remains
  byte-identical.
- Thirty current 2024 ring-1 PAs sit exactly at the 10-pixel cutoff and 129
  sit within 8-12 pixels. Near-threshold rasterization/environment sensitivity
  is the best bounded diagnosis, not a proved cause.
- All accepted primary headline values were recomputed from the regenerated
  payload and matched exactly.
- Stopped after the focused reconciliation pass. Exact byte reproduction
  cannot be established without the three historical payloads. At this
  checkpoint independent scientific rereview of the edge diagnostic was
  requested; the following entry records its acceptance.

## 2026-07-23 - Independent scientific acceptance

- Independent scientific rereview accepted Goal 011 and the regenerated
  payload as the archive candidate.
- The edge drift was judged immaterial to the paper conclusions:
  - +5 PAs is +0.35% relative to 1,427 and +0.045 percentage points of the
    11,133-PA universe;
  - -60 non-null PA-years is -0.052% of 116,472;
  - complete-ring n remains 383; and
  - conditional non-zero shares remain 18.02%, 9.40%, and 3.66%.
- All primary results remain unchanged. No further Goal 011 science is
  required.
- DOI upload remains on hold only for three release requirements:
  - canonical release surfaces use 1,432 and 12.9% while reconciliation
    preserves the historical 1,427 versus regenerated 1,432 comparison;
  - clean-checkout QA generates or includes the triad fixtures; and
  - archive metadata states concordant non-exact reproduction and retains the
    historical radiance row-level and GPKG feature-level limitations.

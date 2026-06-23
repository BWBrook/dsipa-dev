# Runbook: Goal 008 Stage 4C Final Validation

Run from the repository root:

```bash
pwd
git status --short --branch
git rev-parse --short HEAD
git rev-parse --short refs/remotes/origin/main
test -f docs/goals/008-stage4C-final-validation-reproducibility-audit/Goal.md
```

Read the required files listed in `Goal.md`.

## Command Validation

```bash
git diff --check
make ms-check
make test
make build
```

Evidence reconciliation to `/tmp`:

```bash
uv run python -m dsipa.evidence_reconciliation \
  --output-md /tmp/dsipa_stage4c_evidence_reconciliation.md \
  --output-json /tmp/dsipa_stage4c_evidence_reconciliation.json \
  --audit-md /tmp/dsipa_stage4c_reproducibility_audit.md \
  --write-audit
```

Do not write refreshed evidence reconciliation files into the repo during this
goal. If the `/tmp` check fails, classify why and continue with the validation
report unless the failure prevents a recommendation.

## Manual Scans

Claim discipline:

```bash
rg -n "population decline|population trend|causal|causal impact|national biodiversity|national biodiversity response|provider-bounded|presence-only|falsification" manuscript/text docs
```

Caption/table denominator discipline:

```bash
rg -n "n =|eligible|ineligible|minimum-pixel|zero|censor|complete ring|provider-matched|AUC|log loss|redistribut" manuscript/text
```

Release/licence/checksum discipline:

```bash
rg -n "mixed|raw ALA|row-level|redistribut|restricted|excluded|CC-BY|CC BY|Creative Commons|Zenodo|DOI|archive|release manifest|checksum|a751d630|2257ef67" manuscript/text docs data/README.md analysis/reports
```

Reference hygiene:

```bash
rg -n "doi:|DOI|10\\.|ref_doi|TODO|FIXME|citation needed|\\[@|\\?\\]" manuscript/text references docs/ref_doi.txt
```

Release-manifest consistency:

```bash
rg -n "9082f4f|530e843|f731562|dirty=true|archived-proposed|restricted|regenerated|excluded|tracked|a751d630|2257ef67" analysis/reports/final_release_manifest.md analysis/reports/evidence_reconciliation.md analysis/reports/evidence_reconciliation.json data/README.md docs/goals/007-stage4B-release-data-availability-readiness/Stage4B_Closeout.md
```

Classify hits manually. Do not patch broad text just because a scan found a
historical or contextual term.

## Deliverable Checks

```bash
test -f analysis/reports/stage4C_final_validation_report.md
test -f analysis/reports/final_reproducibility_audit_supplement.md
test -f docs/goals/008-stage4C-final-validation-reproducibility-audit/Stage4C_Closeout.md
test -f docs/log/128_stage4C_final_validation_reproducibility.md
git diff --check
git status --short --branch
```

## Wake-Up

Send the DSIPA orchestrator a short wake-up with:

- complete or blocked;
- closeout path;
- validation recommendation;
- blockers or decisions requiring orchestrator/Barry.

Then stop.

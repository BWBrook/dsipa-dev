#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export DSIPA_REPO_ROOT="$ROOT"
WORKERS=${DSIPA_WORKERS:-6}
STATES=${DSIPA_STATES:-"ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT"}
EVIDENCE_DIR=${DSIPA_RUN_EVIDENCE_DIR:-"$ROOT/analysis/reports"}

cd "$ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required for the DSIPA pipeline." >&2
  exit 1
fi
for fixture in \
  tests/fixtures/layerA_triad/triad_geometries.geojson \
  tests/fixtures/layerA_triad/provenance.json; do
  if [[ ! -f "$fixture" ]]; then
    echo "Required offline triad fixture missing: $fixture" >&2
    exit 1
  fi
done
uv sync --extra dev --frozen
export UV_NO_SYNC=1
uv run python -c 'import build, pytest'
uv run python -m dsipa.layerA_reproducibility validate-contract

printf "Running DSIPA-NBS full pipeline in %s\n" "$DSIPA_REPO_ROOT"

printf "\n[Layer A] Geometry + statewise national metrics\n"
uv run python -m dsipa.pa_geometry
uv run python -m dsipa.ibra
uv run python -m dsipa.layerA_reproducibility validate-inputs \
  --prepare \
  --evidence "$EVIDENCE_DIR/layerA-input-validation.json"
uv run python -m dsipa.layerA_statewise \
  --states "$STATES" \
  --workers "$WORKERS" \
  --skip-artefact

printf "\n[Layer A] Sanity, trends, vulnerability, figures\n"
uv run python -m dsipa.layerA_sanity
uv run python -m dsipa.trends
uv run python -m dsipa.trend_uncertainty
uv run python -m dsipa.vulnerability_model
uv run python -m dsipa.figures_layerA

printf "\n[Layer A] Accepted report modules\n"
uv run python -m dsipa.layerA_tables
uv run python -m dsipa.layerA_buffer_sensitivity
uv run python -m dsipa.layerA_threshold_sensitivity
uv run python -m dsipa.layerA_edge_decision
uv run python -m dsipa.layerA_watchlists --skip-supplement

if [[ "${DSIPA_SKIP_LAYERB:-0}" == "1" ]]; then
  printf "\n[Layer B] Skipped (DSIPA_SKIP_LAYERB=1)\n"
else
  if [[ -z "${ALA_DOWNLOAD_EMAIL:-}" || -z "${ALA_DOWNLOAD_REASON:-}" ]]; then
    echo "ALA_DOWNLOAD_EMAIL and ALA_DOWNLOAD_REASON are required for Layer B downloads."
    echo "Set them or export DSIPA_SKIP_LAYERB=1 to skip Layer B."
    exit 1
  fi

  printf "\n[Layer B] Downloads, QC, modelling, figures\n"
  uv run python -m dsipa.layerB_data --download-retries 5
  uv run python -m dsipa.layerB_qc --groups microbats,diurnal_birds
  uv run python -m dsipa.layerB_model --provider dr368
  uv run python -m dsipa.figures_layerB
fi

printf "\n[Docs] Figure inventory + schema reference\n"
uv run python -m dsipa.figure_inventory
uv run python -m dsipa.schema_reference --skip-artefact

printf "\n[Layer A] Fail-closed output validation\n"
uv run python -m dsipa.layerA_reproducibility validate-outputs \
  --evidence "$EVIDENCE_DIR/layerA-output-validation.json"

printf "\n[QA] Tests + build\n"
uv run pytest -rs
uv run python -m build --sdist --wheel

printf "\nPipeline complete.\n"

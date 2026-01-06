#!/usr/bin/env bash
set -euo pipefail

ROOT=${DSIPA_REPO_ROOT:-$(pwd)}
export DSIPA_REPO_ROOT="$ROOT"
WORKERS=${DSIPA_WORKERS:-6}
STATES=${DSIPA_STATES:-"ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT"}

printf "Running DSIPA-NBS full pipeline in %s\n" "$DSIPA_REPO_ROOT"

printf "\n[Layer A] Geometry + statewise national metrics\n"
uv run python -m dsipa.pa_geometry
uv run python -m dsipa.ibra
uv run python -m dsipa.layerA_statewise --states "$STATES" --workers "$WORKERS"

printf "\n[Layer A] Sanity, trends, vulnerability, figures\n"
uv run python -m dsipa.layerA_sanity
uv run python -m dsipa.trends
uv run python -m dsipa.trend_uncertainty
uv run python -m dsipa.vulnerability_model
uv run python -m dsipa.figures_layerA

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

printf "\n[QA] Tests + build\n"
uv run pytest
uv run python -m build --sdist --wheel

printf "\nPipeline complete.\n"

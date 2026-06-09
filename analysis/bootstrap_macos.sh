#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

PYTHON_VERSION=${DSIPA_PYTHON_VERSION:-3.12}

needs_rebuild=0
if [[ ! -x .venv/bin/python ]]; then
  needs_rebuild=1
elif ! .venv/bin/python - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)
PY
then
  needs_rebuild=1
fi

if [[ "$needs_rebuild" == "1" ]]; then
  uv venv --clear --python "$PYTHON_VERSION"
fi

uv sync --python "$PYTHON_VERSION" --extra dev

uv run python - <<'PY'
import geopandas
import rasterio
import sklearn
import dsipa

print("DSIPA macOS bootstrap imports passed.")
PY

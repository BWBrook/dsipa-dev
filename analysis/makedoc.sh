#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=${DSIPA_SOURCE_ROOT:-$(git rev-parse --show-toplevel)}
MAKEDOC_ROOT=${MAKEDOC_ROOT:-/Users/bwbrook/work/makedoc}
CONFIG=${DSIPA_MAKEDOC_CONFIG:-$REPO_ROOT/settings/build.yaml}
PROFILE=${PROFILE:-draft}
TARGET=${1:-check}
PYTHON=${PYTHON:-python3}
if [[ $# -gt 0 ]]; then
  shift
fi

if [[ ! -d "$MAKEDOC_ROOT" ]]; then
  echo "makedoc checkout not found: $MAKEDOC_ROOT" >&2
  exit 1
fi

set +e
make_args=(-C "$MAKEDOC_ROOT" CONFIG="$CONFIG" PROFILE="$PROFILE")
if [[ "$PROFILE" == "supplementary" ]]; then
  export DSIPA_MAKEDOC_UPSTREAM_LAYOUT_RENDER="$MAKEDOC_ROOT/scripts/render_pdf_layout.py"
  make_args+=("LAYOUT_RENDER=$SCRIPT_DIR/render_rsec_pdf_layout.py")
fi
make "${make_args[@]}" "$TARGET" "$@"
status=$?
set -e

if [[ $status -ne 0 ]]; then
  exit "$status"
fi

if [[ "$TARGET" == "check" || "$TARGET" == "all" ]]; then
  "$PYTHON" "$SCRIPT_DIR/annotate_makedoc_manifest.py" \
    --config "$CONFIG" \
    --profile "$PROFILE" \
    --source-root "$REPO_ROOT" \
    --build-tool-root "$MAKEDOC_ROOT"
fi

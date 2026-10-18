#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ -n "${DSIPA_SOURCE_ROOT:-}" ]]; then
  REPO_ROOT=$DSIPA_SOURCE_ROOT
elif REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then
  :
else
  REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi
MAKEDOC_ROOT=${MAKEDOC_ROOT:-$HOME/work/makedoc}
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
# Pandoc uses generic LaTeX filenames. Keep them out of the shared tool cache
# so another project's build cannot supply our PDF during a concurrent run.
make_args=(-C "$MAKEDOC_ROOT" CONFIG="$CONFIG" PROFILE="$PROFILE"
  "PDF_ENGINE_OUTPUT_DIR=$REPO_ROOT/build/.makedoc-latex/$PROFILE")
# Upstream dependencies omit embedded image changes; reader builds must be fresh.
if [[ "$TARGET" == "all" || "$TARGET" == "check" ]]; then
  make_args+=(-B)
fi
if [[ "$PROFILE" == "submission" || "$PROFILE" == "supplementary" ]]; then
  export DSIPA_MAKEDOC_UPSTREAM_LAYOUT_RENDER="$MAKEDOC_ROOT/scripts/render_pdf_layout.py"
  make_args+=("LAYOUT_RENDER=$SCRIPT_DIR/render_rsec_pdf_layout.py")
fi
if [[ "$PROFILE" == "supplementary" ]]; then
  export DSIPA_MAKEDOC_UPSTREAM_SOURCE_RENDER="$MAKEDOC_ROOT/scripts/prepare_markdown_sources.py"
  make_args+=("SOURCE_RENDER=$SCRIPT_DIR/render_rsec_sources.py")
fi
make "${make_args[@]}" "$TARGET" "$@"
status=$?
set -e

if [[ $status -ne 0 ]]; then
  exit "$status"
fi

if [[ "$TARGET" == "check" || "$TARGET" == "all" ]]; then
  if [[ "$PROFILE" == "submission" || "$PROFILE" == "supplementary" ]]; then
    "$PYTHON" "$SCRIPT_DIR/normalize_rsec_docx.py" \
      --config "$CONFIG" \
      --profile "$PROFILE"
  fi
  "$PYTHON" "$SCRIPT_DIR/annotate_makedoc_manifest.py" \
    --config "$CONFIG" \
    --profile "$PROFILE" \
    --source-root "$REPO_ROOT" \
    --build-tool-root "$MAKEDOC_ROOT"
fi

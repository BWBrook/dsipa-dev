#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
MAKEDOC_ROOT=${MAKEDOC_ROOT:-/Users/bwbrook/work/makedoc}
CONFIG=${DSIPA_MAKEDOC_CONFIG:-$REPO_ROOT/settings/build.yaml}
PROFILE=${PROFILE:-draft}
TARGET=${1:-check}
if [[ $# -gt 0 ]]; then
  shift
fi

if [[ ! -d "$MAKEDOC_ROOT" ]]; then
  echo "makedoc checkout not found: $MAKEDOC_ROOT" >&2
  exit 1
fi

exec make -C "$MAKEDOC_ROOT" CONFIG="$CONFIG" PROFILE="$PROFILE" "$TARGET" "$@"

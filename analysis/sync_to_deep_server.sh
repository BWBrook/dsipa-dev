#!/usr/bin/env bash
set -euo pipefail

HOST=${DSIPA_DEEP_HOST:-deep-server-ts}
REMOTE_PATH=${DSIPA_DEEP_SYNC_PATH:-/data/codex/repos/dsipa-dev-mac-sync}
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: analysis/sync_to_deep_server.sh [options]

Synchronise the current Mac checkout to a scratch DSIPA path on deep-server via
the Tailscale SSH alias. This is for dirty working-tree HPC runs; canonical
release runs should still use a clean commit plus analysis/deep_server_tmux_run.sh.

Options:
  --host HOST          SSH alias (default: deep-server-ts)
  --remote-path PATH   Remote scratch path (default: /data/codex/repos/dsipa-dev-mac-sync)
  --dry-run            Show what would be transferred
  -h, --help           Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST=$2
      shift 2
      ;;
    --remote-path)
      REMOTE_PATH=$2
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

ssh -o BatchMode=yes -o ConnectTimeout="${HPC_SSH_TIMEOUT:-8}" "$HOST" \
  "mkdir -p $(printf '%q' "$REMOTE_PATH")"

args=(
  -az
  --delete
  --exclude .venv/
  --exclude .pytest_cache/
  --exclude __pycache__/
  --exclude build/
  --exclude dist/
  --exclude artefacts/
  --exclude analysis/state_runs/
  --exclude data/raw/ala_occurrences/
  --exclude data/raw/nightlights_zenodo_v0_4/
  --exclude data/processed/layerB/
  --exclude data/processed/cache/
  --exclude '*.tif'
  --exclude '*.tiff'
  --exclude '*.gpkg'
  --exclude '*.nc'
  --exclude '*.h5'
  --exclude '*.hdf'
  --exclude '*.grd'
  --exclude '*.img'
)

if [[ "$DRY_RUN" == "1" ]]; then
  args+=(--dry-run --itemize-changes)
fi

rsync "${args[@]}" ./ "$HOST:$REMOTE_PATH/"

if [[ "$DRY_RUN" == "1" ]]; then
  action="Dry-run checked DSIPA checkout sync to"
else
  action="Synced DSIPA checkout to"
fi

cat <<EOF
$action $HOST:$REMOTE_PATH

Example remote run:
  DSIPA_DEEP_REPO=$REMOTE_PATH analysis/deep_server_tmux_run.sh --mode custom --command 'uv run python -m pytest -rs'
EOF

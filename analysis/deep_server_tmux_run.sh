#!/usr/bin/env bash
set -euo pipefail

HOST=${DSIPA_DEEP_HOST:-deep-server}
REMOTE_REPO=${DSIPA_DEEP_REPO:-/home/bwbrook/papers/dsipa-dev}
RUN_BASE=${DSIPA_DEEP_RUN_BASE:-/data/codex/scratch/dsipa}
ARTIFACT_BASE=${DSIPA_DEEP_ARTIFACT_BASE:-/data/codex/artifacts/dsipa}
RUN_ID=${DSIPA_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)-dsipa}
SESSION=${DSIPA_DEEP_SESSION:-dsipa-$RUN_ID}
MODE=evidence
WORKERS=${DSIPA_WORKERS:-12}
STATES=${DSIPA_STATES:-ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT}
CUSTOM_COMMAND=
REPLACE=0

usage() {
  cat <<'USAGE'
Usage: analysis/deep_server_tmux_run.sh [options]

Starts a DSIPA run inside tmux on deep-server. Defaults to the existing
evidence snapshot at /home/bwbrook/papers/dsipa-dev and writes run logs under
/data/codex/scratch/dsipa/<RUN_ID>.

Options:
  --mode evidence|full|custom   Run evidence inventory, full pipeline, or command.
  --command CMD                 Command for --mode custom.
  --host HOST                   SSH alias (default: deep-server).
  --remote-repo PATH            Remote DSIPA repo root.
  --run-id ID                   Run identifier.
  --session NAME                tmux session name.
  --workers N                   DSIPA worker count for full runs.
  --states CSV                  DSIPA states for full runs.
  --replace                     Kill an existing tmux session with the same name.
  -h, --help                    Show this help.

Examples:
  analysis/deep_server_tmux_run.sh --mode evidence
  analysis/deep_server_tmux_run.sh --mode full --workers 12
  analysis/deep_server_tmux_run.sh --mode custom --command 'uv run pytest -rs'
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE=$2
      shift 2
      ;;
    --command)
      CUSTOM_COMMAND=$2
      shift 2
      ;;
    --host)
      HOST=$2
      shift 2
      ;;
    --remote-repo)
      REMOTE_REPO=$2
      shift 2
      ;;
    --run-id)
      RUN_ID=$2
      SESSION=${DSIPA_DEEP_SESSION:-dsipa-$RUN_ID}
      shift 2
      ;;
    --session)
      SESSION=$2
      shift 2
      ;;
    --workers)
      WORKERS=$2
      shift 2
      ;;
    --states)
      STATES=$2
      shift 2
      ;;
    --replace)
      REPLACE=1
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

if [[ "$MODE" == "custom" && -z "$CUSTOM_COMMAND" ]]; then
  echo "--mode custom requires --command" >&2
  exit 2
fi

quote() {
  printf "%q" "$1"
}

ssh \
  -o BatchMode=yes \
  -o ConnectTimeout="${HPC_SSH_TIMEOUT:-8}" \
  "$HOST" \
  "MODE=$(quote "$MODE") CUSTOM_COMMAND=$(quote "$CUSTOM_COMMAND") REMOTE_REPO=$(quote "$REMOTE_REPO") RUN_BASE=$(quote "$RUN_BASE") ARTIFACT_BASE=$(quote "$ARTIFACT_BASE") RUN_ID=$(quote "$RUN_ID") SESSION=$(quote "$SESSION") WORKERS=$(quote "$WORKERS") STATES=$(quote "$STATES") REPLACE=$(quote "$REPLACE") bash -s" <<'REMOTE'
set -euo pipefail

mkdir -p /data/codex/repos /data/codex/scratch/dsipa /data/codex/artifacts/dsipa /data/codex/tmp

if [[ ! -d "$REMOTE_REPO" ]]; then
  echo "Remote repo not found: $REMOTE_REPO" >&2
  exit 1
fi
if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is required on the remote host" >&2
  exit 1
fi
if tmux has-session -t "$SESSION" 2>/dev/null; then
  if [[ "$REPLACE" == "1" ]]; then
    tmux kill-session -t "$SESSION"
  else
    echo "tmux session already exists: $SESSION" >&2
    echo "Attach with: ssh ${HOST:-deep-server} -t 'tmux attach -t $SESSION'" >&2
    exit 1
  fi
fi

RUN_DIR="$RUN_BASE/$RUN_ID"
ARTIFACT_DIR="$ARTIFACT_BASE/$RUN_ID"
mkdir -p "$RUN_DIR" "$ARTIFACT_DIR"

ENV_FILE="$RUN_DIR/run.env"
{
  printf 'MODE=%q\n' "$MODE"
  printf 'CUSTOM_COMMAND=%q\n' "$CUSTOM_COMMAND"
  printf 'REMOTE_REPO=%q\n' "$REMOTE_REPO"
  printf 'RUN_DIR=%q\n' "$RUN_DIR"
  printf 'ARTIFACT_DIR=%q\n' "$ARTIFACT_DIR"
  printf 'WORKERS=%q\n' "$WORKERS"
  printf 'STATES=%q\n' "$STATES"
} > "$ENV_FILE"

RUN_SCRIPT="$RUN_DIR/run_remote.sh"
cat > "$RUN_SCRIPT" <<'RUNNER'
#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/run.env"

log() {
  printf '[%s] %s\n' "$(date -Is)" "$*"
}

cd "$REMOTE_REPO"
export DSIPA_REPO_ROOT="$REMOTE_REPO"
export DSIPA_WORKERS="$WORKERS"
export DSIPA_STATES="$STATES"

UV_BIN=
if command -v uv >/dev/null 2>&1; then
  UV_BIN="$(command -v uv)"
elif [[ -x "$HOME/.local/bin/uv" ]]; then
  UV_BIN="$HOME/.local/bin/uv"
fi
if [[ -n "$UV_BIN" ]]; then
  export PATH="$(dirname "$UV_BIN"):$PATH"
fi

python_cmd() {
  if [[ -x ".venv/bin/python" ]]; then
    PYTHONPATH=src/python .venv/bin/python "$@"
  elif [[ -n "$UV_BIN" ]]; then
    "$UV_BIN" run python "$@"
  else
    PYTHONPATH=src/python python3 "$@"
  fi
}

{
  log "DSIPA deep-server run starting"
  printf 'mode=%s\n' "$MODE"
  printf 'repo=%s\n' "$REMOTE_REPO"
  printf 'run_dir=%s\n' "$RUN_DIR"
  printf 'artifact_dir=%s\n' "$ARTIFACT_DIR"
  printf 'workers=%s\n' "$WORKERS"
  printf 'states=%s\n' "$STATES"
  printf 'host=%s\n' "$(hostname -f 2>/dev/null || hostname)"
  printf 'date_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'python='
  python_cmd --version
  printf 'uv=%s\n' "${UV_BIN:-missing}"
  printf '\n## git\n'
  git status --short --branch
  git rev-parse HEAD
  printf '\n## resources\n'
  nproc
  free -h
  df -hT / /data
} > "$RUN_DIR/resource-snapshot.txt" 2>&1

cp "$RUN_DIR/resource-snapshot.txt" "$ARTIFACT_DIR/resource-snapshot.txt"

case "$MODE" in
  evidence)
    log "Running evidence reconciliation"
    python_cmd -m dsipa.evidence_reconciliation --write-audit --fail-on-mismatch
    for report in \
      analysis/reports/evidence_reconciliation.md \
      analysis/reports/evidence_reconciliation.json \
      analysis/reports/reproducibility_audit.md; do
      cp "$report" "$RUN_DIR/"
      cp "$report" "$ARTIFACT_DIR/"
    done
    ;;
  full)
    if [[ -z "$UV_BIN" ]]; then
      echo "uv is required for analysis/run_full_pipeline.sh" >&2
      exit 1
    fi
    log "Running full pipeline"
    analysis/run_full_pipeline.sh
    ;;
  custom)
    log "Running custom command"
    bash -lc "$CUSTOM_COMMAND"
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    exit 2
    ;;
esac

log "DSIPA deep-server run complete"
RUNNER
chmod +x "$RUN_SCRIPT"

tmux new-session -d -s "$SESSION" "bash -lc '$RUN_SCRIPT > \"$RUN_DIR/run.log\" 2>&1'"

cat <<EOF
Started tmux session: $SESSION
Run dir: $RUN_DIR
Artifact dir: $ARTIFACT_DIR
Attach: ssh ${HOST:-deep-server} -t 'tmux attach -t $SESSION'
Log: ssh ${HOST:-deep-server} 'tail -f $RUN_DIR/run.log'
EOF
REMOTE

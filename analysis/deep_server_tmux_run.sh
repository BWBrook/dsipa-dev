#!/usr/bin/env bash
set -euo pipefail

HOST=${DSIPA_DEEP_HOST:-deep-server-ts}
REMOTE_REPO=${DSIPA_DEEP_REPO:-/data/codex/repos/dsipa-dev-mac-sync}
RUN_BASE=${DSIPA_DEEP_RUN_BASE:-/data/codex/scratch/dsipa}
ARTIFACT_BASE=${DSIPA_DEEP_ARTIFACT_BASE:-/data/codex/artifacts/dsipa}
RUN_ID=${DSIPA_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)-dsipa}
SESSION=${DSIPA_DEEP_SESSION:-dsipa-$RUN_ID}
MODE=evidence
WORKERS=${DSIPA_WORKERS:-12}
STATES=${DSIPA_STATES:-ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT}
CUSTOM_COMMAND=
REPLACE=0
DRY_RUN=0
REFERENCE_BASELINE=${DSIPA_REFERENCE_BASELINE:-/data/codex/artifacts/dsipa/20260723T062202Z-goal011-layerA-preservation/payload}

usage() {
  cat <<'USAGE'
Usage: analysis/deep_server_tmux_run.sh [options]

Starts a DSIPA run inside tmux on deep-server via the Tailscale SSH alias.
Defaults to the Mac-synced scratch checkout at
/data/codex/repos/dsipa-dev-mac-sync and writes run logs under
/data/codex/scratch/dsipa/<RUN_ID>.

Options:
  --mode evidence|full|layerA|custom
                                Run evidence inventory, full pipeline, frozen Layer A, or command.
  --command CMD                 Command for --mode custom.
  --host HOST                   SSH alias (default: deep-server-ts).
  --remote-repo PATH            Remote DSIPA repo root.
  --run-id ID                   Run identifier.
  --session NAME                tmux session name.
  --workers N                   DSIPA worker count for full runs.
  --states CSV                  DSIPA states for full runs.
  --replace                     Kill an existing tmux session with the same name.
  --dry-run                     Print the remote contract without contacting SSH.
  -h, --help                    Show this help.

Examples:
  analysis/deep_server_tmux_run.sh --mode evidence
  analysis/deep_server_tmux_run.sh --mode full --workers 12
  analysis/deep_server_tmux_run.sh --mode layerA --workers 12
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

if [[ "$MODE" == "custom" && -z "$CUSTOM_COMMAND" ]]; then
  echo "--mode custom requires --command" >&2
  exit 2
fi
if [[ "$MODE" != "evidence" && "$MODE" != "full" && "$MODE" != "layerA" && "$MODE" != "custom" ]]; then
  echo "Unknown mode: $MODE" >&2
  exit 2
fi

quote() {
  printf "%q" "$1"
}

if [[ "$DRY_RUN" == "1" ]]; then
  printf 'mode=%s\n' "$MODE"
  printf 'host=%s\n' "$HOST"
  printf 'remote_repo=%s\n' "$REMOTE_REPO"
  printf 'run_id=%s\n' "$RUN_ID"
  printf 'workers=%s\n' "$WORKERS"
  printf 'states=%s\n' "$STATES"
  if [[ "$MODE" == "layerA" ]]; then
    printf 'DSIPA_SKIP_LAYERB=1\n'
    printf 'command=analysis/run_full_pipeline.sh\n'
  fi
  exit 0
fi

ssh \
  -o BatchMode=yes \
  -o ConnectTimeout="${HPC_SSH_TIMEOUT:-8}" \
  "$HOST" \
  "MODE=$(quote "$MODE") CUSTOM_COMMAND=$(quote "$CUSTOM_COMMAND") REMOTE_REPO=$(quote "$REMOTE_REPO") RUN_BASE=$(quote "$RUN_BASE") ARTIFACT_BASE=$(quote "$ARTIFACT_BASE") RUN_ID=$(quote "$RUN_ID") SESSION=$(quote "$SESSION") WORKERS=$(quote "$WORKERS") STATES=$(quote "$STATES") REFERENCE_BASELINE=$(quote "$REFERENCE_BASELINE") REPLACE=$(quote "$REPLACE") bash -s" <<'REMOTE'
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
    echo "Attach with: ssh ${HOST:-deep-server-ts} -t 'tmux attach -t $SESSION'" >&2
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
  printf 'REFERENCE_BASELINE=%q\n' "$REFERENCE_BASELINE"
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
export UV_LINK_MODE="${UV_LINK_MODE:-copy}"
export DSIPA_RUN_EVIDENCE_DIR="$ARTIFACT_DIR/validation"
mkdir -p "$DSIPA_RUN_EVIDENCE_DIR"
if [[ "$MODE" == "layerA" ]]; then
  export DSIPA_SKIP_LAYERB=1
fi

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

finalize() {
  status=$?
  trap - EXIT
  if [[ "$status" == "0" ]]; then
    terminal=passed
  else
    terminal=failed
  fi
  printf '{"terminal":true,"status":"%s","exit_code":%s}\n' "$terminal" "$status" \
    > "$ARTIFACT_DIR/pipeline-status.json"
  cp "$RUN_DIR/run.env" "$ARTIFACT_DIR/run.env"
  git status --short --branch > "$ARTIFACT_DIR/postrun-git-status.txt"
  git diff --binary > "$ARTIFACT_DIR/implementation-overlay.diff"
  git diff --name-only > "$ARTIFACT_DIR/implementation-overlay-paths.txt"
  git ls-files -co --exclude-standard -z \
    | tar --null -czf "$ARTIFACT_DIR/candidate-source.tar.gz" -T -
  git ls-files -co --exclude-standard -z \
    | sort -z \
    | xargs -0 sha256sum \
    > "$ARTIFACT_DIR/source-inventory-sha256.txt"
  mkdir -p "$ARTIFACT_DIR/payload/data/processed" "$ARTIFACT_DIR/reports" "$ARTIFACT_DIR/build"
  find data/processed -maxdepth 1 -type f \
    \( -name 'pa_radiance_buffers_national_v0_3_0.csv' \
    -o -name 'pa_edge_profiles_national_v0_3_0.csv' \
    -o -name 'pa_buffer_validity_v0_3_0.csv' \
    -o -name 'pa_trends_v0_3_0.csv' \
    -o -name 'pa_risk_rankings_v0_3_0.csv' \
    -o -name 'pa_geometries_v0_3_0.csv' \
    -o -name 'pa_geometries_v0_3_0.gpkg' \
    -o -name 'pa_ibra_assignment_v0_3_0.csv' \
    -o -name 'pa_trend_bootstrap_summary_v0_3_0.csv' \) \
    -exec cp {} "$ARTIFACT_DIR/payload/data/processed/" \;
  for report in \
    national_layerA_coverage_and_sanity.md \
    layerA_sanity_dashboard.md \
    layerA_denominators_and_censoring.csv \
    layerA_denominators_and_censoring.md \
    layerA_edge_profile_decision.csv \
    layerA_edge_profile_decision.md \
    layerA_table1_candidate.md; do
    if [[ -f "analysis/reports/$report" ]]; then
      cp "analysis/reports/$report" "$ARTIFACT_DIR/reports/"
    fi
  done
  if [[ -d dist ]]; then
    cp -R dist/. "$ARTIFACT_DIR/build/"
  fi
  find "$ARTIFACT_DIR" -type f ! -name SHA256SUMS -print0 \
    | sort -z \
    | xargs -0 sha256sum \
    > "$ARTIFACT_DIR/SHA256SUMS"
  exit "$status"
}
trap finalize EXIT

{
  log "DSIPA deep-server run starting"
  printf 'mode=%s\n' "$MODE"
  printf 'repo=%s\n' "$REMOTE_REPO"
  printf 'run_dir=%s\n' "$RUN_DIR"
  printf 'artifact_dir=%s\n' "$ARTIFACT_DIR"
  printf 'workers=%s\n' "$WORKERS"
  printf 'states=%s\n' "$STATES"
  printf 'skip_layerB=%s\n' "${DSIPA_SKIP_LAYERB:-0}"
  printf 'reference_baseline=%s\n' "$REFERENCE_BASELINE"
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
  layerA)
    if [[ -z "$UV_BIN" ]]; then
      echo "uv is required for analysis/run_full_pipeline.sh" >&2
      exit 1
    fi
    printf 'DSIPA_SKIP_LAYERB=1 DSIPA_WORKERS=%q DSIPA_STATES=%q analysis/run_full_pipeline.sh\n' \
      "$WORKERS" "$STATES" > "$ARTIFACT_DIR/pipeline-command.txt"
    log "Running frozen Layer A pipeline"
    analysis/run_full_pipeline.sh
    log "Reconciling all nine outputs to Goal 011"
    python_cmd -m dsipa.layerA_reproducibility reconcile \
      --baseline "$REFERENCE_BASELINE" \
      --evidence "$ARTIFACT_DIR/reconciliation.json"
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
Attach: ssh ${HOST:-deep-server-ts} -t 'tmux attach -t $SESSION'
Log: ssh ${HOST:-deep-server-ts} 'tail -f $RUN_DIR/run.log'
EOF
REMOTE

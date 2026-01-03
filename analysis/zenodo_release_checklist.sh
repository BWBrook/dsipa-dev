#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel)
DATE_UTC=$(date -u +%Y-%m-%d)
SCHEMA_VERSION=${1:-""}
OUT_PATH=${2:-""}

if [[ -z "$SCHEMA_VERSION" ]]; then
  SCHEMA_VERSION=$(python - <<'PY'
from dsipa.schema import SCHEMA_VERSION
print(SCHEMA_VERSION)
PY
)
fi

SCHEMA_SLUG=${SCHEMA_VERSION//./_}
if [[ -z "$OUT_PATH" ]]; then
  OUT_PATH="$ROOT/analysis/reports/zenodo_release_checklist_${DATE_UTC}.md"
fi

required=(
  "data/processed/pa_radiance_buffers_national_v${SCHEMA_SLUG}.csv"
  "data/processed/pa_edge_profiles_national_v${SCHEMA_SLUG}.csv"
  "data/processed/pa_buffer_validity_v${SCHEMA_SLUG}.csv"
  "data/processed/pa_trends_v${SCHEMA_SLUG}.csv"
  "data/processed/pa_risk_rankings_v${SCHEMA_SLUG}.csv"
)

optional=(
  "data/processed/pa_geometries_v${SCHEMA_SLUG}.gpkg"
  "data/processed/pa_geometries_v${SCHEMA_SLUG}.csv"
  "artefacts/wp0_10c_layerA_sanity"
  "artefacts/wp0_11c_trends_censoring"
  "artefacts/wp0_12c_risk_retention"
  "artefacts/wp0_13c_layerA_figures"
)

sha256() {
  local path="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$path" | awk '{print $1}'
  else
    python - <<PY
import hashlib
from pathlib import Path
path = Path("$path")
h = hashlib.sha256()
with path.open('rb') as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b''):
        h.update(chunk)
print(h.hexdigest())
PY
  fi
}

write_section() {
  local label="$1"
  shift
  local items=("$@")
  echo "## ${label}" >> "$OUT_PATH"
  echo "" >> "$OUT_PATH"
  echo "| Path | Status | Size (MB) | SHA256 |" >> "$OUT_PATH"
  echo "| --- | --- | --- | --- |" >> "$OUT_PATH"
  for rel in "${items[@]}"; do
    local path="$ROOT/$rel"
    if [[ -f "$path" ]]; then
      local size
      size=$(du -m "$path" | awk '{print $1}')
      local hash
      hash=$(sha256 "$path")
      echo "| $rel | present | $size | $hash |" >> "$OUT_PATH"
    elif [[ -d "$path" ]]; then
      local size
      size=$(du -sm "$path" | awk '{print $1}')
      echo "| $rel | dir | $size | - |" >> "$OUT_PATH"
    else
      echo "| $rel | missing | - | - |" >> "$OUT_PATH"
    fi
  done
  echo "" >> "$OUT_PATH"
}

cat <<EOF2 > "$OUT_PATH"
# Zenodo release checklist

Generated: ${DATE_UTC} UTC
Schema version: ${SCHEMA_VERSION}

## Checklist
- [ ] Confirm national outputs are regenerated for schema v${SCHEMA_VERSION}.
- [ ] Verify outputs are derived from a clean commit (record commit hash in Zenodo description).
- [ ] Run unit tests and record results.
- [ ] Generate canonical artefacts for WP0.10c–WP0.13c (optional but recommended).
- [ ] Upload required national tables + geometry outputs to Zenodo.
- [ ] Copy SHA256 checksums into the Zenodo record description or an attached manifest.
- [ ] Add repository URL + commit hash, and link to this checklist in Zenodo metadata.
- [ ] After DOI is minted, update data/README.md with the Zenodo DOI and access date.

EOF2

write_section "Required files" "${required[@]}"
write_section "Optional/context files" "${optional[@]}"

echo "Wrote ${OUT_PATH}"

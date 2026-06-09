SHELL := /bin/bash

PYTHON_VERSION ?= 3.12
MAKEDOC_ROOT ?= /Users/bwbrook/work/makedoc
PROFILE ?= draft
DSIPA_WORKERS ?= 6
DSIPA_STATES ?= ACT,NSW,NT,QLD,SA,TAS,VIC,WA,JBT,EXT
CHECK_SSH ?= 1
DEEP_HOST ?= deep-server-ts
DEEP_REPO ?= /data/codex/repos/dsipa-dev-mac-sync
READINESS_SSH_FLAGS := $(if $(filter 1 true yes,$(CHECK_SSH)),--check-ssh,)

.PHONY: bootstrap readiness test build pipeline layerA hpc-evidence hpc-full hpc-sync-dry-run hpc-sync ms-validate ms-check ms-build ms-clean

bootstrap:
	DSIPA_PYTHON_VERSION=$(PYTHON_VERSION) analysis/bootstrap_macos.sh

readiness:
	uv run python analysis/check_macos_readiness.py --deep-host $(DEEP_HOST) --deep-repo $(DEEP_REPO) $(READINESS_SSH_FLAGS) --write-report

test:
	uv run python -m pytest -rs

build:
	uv build --out-dir /tmp/dsipa-build

pipeline:
	DSIPA_WORKERS=$(DSIPA_WORKERS) DSIPA_STATES=$(DSIPA_STATES) analysis/run_full_pipeline.sh

layerA:
	DSIPA_SKIP_LAYERB=1 DSIPA_WORKERS=$(DSIPA_WORKERS) DSIPA_STATES=$(DSIPA_STATES) analysis/run_full_pipeline.sh

hpc-evidence:
	analysis/deep_server_tmux_run.sh --mode evidence

hpc-full:
	analysis/deep_server_tmux_run.sh --mode full --workers $(DSIPA_WORKERS)

hpc-sync-dry-run:
	analysis/sync_to_deep_server.sh --dry-run

hpc-sync:
	analysis/sync_to_deep_server.sh

ms-validate:
	MAKEDOC_ROOT=$(MAKEDOC_ROOT) PROFILE=$(PROFILE) analysis/makedoc.sh validate-config

ms-check:
	MAKEDOC_ROOT=$(MAKEDOC_ROOT) PROFILE=$(PROFILE) analysis/makedoc.sh check

ms-build:
	MAKEDOC_ROOT=$(MAKEDOC_ROOT) PROFILE=$(PROFILE) analysis/makedoc.sh all

ms-clean:
	MAKEDOC_ROOT=$(MAKEDOC_ROOT) PROFILE=$(PROFILE) analysis/makedoc.sh clean

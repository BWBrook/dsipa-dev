# macOS readiness report

Host platform: `macOS-26.5-arm64-arm-64bit`
Python: `3.12.13`

| Status | Check | Detail |
| --- | --- | --- |
| PASS | Host OS | Darwin/macOS |
| PASS | Python runtime | 3.12.13 at /Users/bwbrook/papers/dsipa-dev/.venv/bin/python3 |
| PASS | Python version bound | >=3.12,<3.13 |
| PASS | .python-version | Pinned to 3.12 |
| PASS | Import dsipa | ok |
| PASS | Import geopandas | ok |
| PASS | Import rasterio | ok |
| PASS | Import sklearn | ok |
| PASS | Import numpy | ok |
| PASS | Import pandas | ok |
| PASS | Tool uv | /opt/homebrew/bin/uv |
| PASS | Tool git | /opt/homebrew/bin/git |
| PASS | Tool pandoc | /opt/homebrew/bin/pandoc |
| PASS | Tool xelatex | /opt/homebrew/bin/xelatex |
| PASS | Tool tmux | /opt/homebrew/bin/tmux |
| PASS | Tool ssh | /usr/bin/ssh |
| PASS | Tool rsync | /opt/homebrew/bin/rsync |
| PASS | Tool sha256sum | /sbin/sha256sum |
| PASS | File settings/build.yaml | present |
| PASS | File references/refs.yaml | present |
| PASS | File csl/cambridge-university-press-author-date-cambridge-a.csl | present |
| PASS | File manuscript/authors.yaml | present |
| PASS | File manuscript/text/references.md | present |
| PASS | File analysis/makedoc.sh | present |
| PASS | makedoc checkout | /Users/bwbrook/work/makedoc |
| PASS | makedoc validate-config | draft profile validates |
| PASS | analysis/deep_server_tmux_run.sh | bash syntax ok |
| PASS | analysis/sync_to_deep_server.sh | bash syntax ok |
| PASS | deep-server SSH | deep-server-ts: deep-server; repo=/data/codex/repos/dsipa-dev-mac-sync |

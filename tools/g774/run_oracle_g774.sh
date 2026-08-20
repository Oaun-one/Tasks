#!/usr/bin/env bash
set -euo pipefail
export PATH="/c/Users/Predator 16/.local/bin:$PATH"
set -a; . "E:/WORK/TU/.env"; set +a
export PYTHONUTF8=1
PKG="E:/WORK/TU/tasks/g774/gen-g774-activity-kit-print-spec-audit"
harbor run -p "$PKG" -a oracle --n-attempts 1 -r 1 \
  -o "E:/WORK/TU/runs/g774" --job-name "${1:-oracle-hardened}" -y

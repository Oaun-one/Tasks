#!/usr/bin/env bash
set -euo pipefail
export PATH="/c/Users/Predator 16/.local/bin:$PATH"
set -a; . "E:/WORK/TU/.env"; set +a
export PYTHONUTF8=1
PKG="E:/WORK/TU/tasks/g988/gen-g988-composite-photo-request-rights-audit"
harbor run -p "$PKG" -a oracle --n-attempts 1 -r 1 \
  -o "E:/WORK/TU/runs/g988" --job-name "${1:-oracle-baseline}" -y

#!/usr/bin/env bash
set -euo pipefail
export PATH="/c/Users/Predator 16/.local/bin:$PATH"
set -a; . "E:/WORK/TU/.env"; set +a
export PYTHONUTF8=1
PKG="E:/WORK/TU/tasks/g789/gen-g789-dissertation-formatting-spec-audit"
harbor run -p "$PKG" -a oracle --n-attempts 1 -r 1 \
  -o "E:/WORK/TU/runs/g789" --job-name "${1:-oracle-baseline}" -y

#!/usr/bin/env bash
set -euo pipefail
export PATH="/c/Users/Predator 16/.local/bin:$PATH"
set -a; . "E:/WORK/TU/.env"; set +a
export PYTHONUTF8=1
PKG="E:/WORK/TU/tasks/g970/gen-g970-festival-collateral-signage-permit-audit"
harbor run -p "$PKG" -a oracle --n-attempts 5 -n 5 -r 1 \
  -o "E:/WORK/TU/runs/g970" --job-name "${1:-stability-g970}" -y

#!/bin/bash
# The golden run. Harbor uploads this solution/ directory and executes this
# script; it must leave /app in a state that scores reward 1.0.
set -euo pipefail

SOLUTION_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${HARBOR_TASK_WORKSPACE:-/app}"

mkdir -p "$WORKSPACE"
cp -f "$SOLUTION_DIR/files/preflight_audit.csv" "$WORKSPACE/preflight_audit.csv"
cp -f "$SOLUTION_DIR/files/section_summary.csv" "$WORKSPACE/section_summary.csv"
cp -f "$SOLUTION_DIR/files/preflight_memo.md" "$WORKSPACE/preflight_memo.md"
cp -f "$SOLUTION_DIR/files/results.json" "$WORKSPACE/results.json"

ls -1 "$WORKSPACE/preflight_audit.csv" "$WORKSPACE/section_summary.csv" \
      "$WORKSPACE/preflight_memo.md" "$WORKSPACE/results.json"

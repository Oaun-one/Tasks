#!/usr/bin/env bash
set -euo pipefail
export PATH="/c/Users/Predator 16/.local/bin:$PATH"
set -a; . "E:/WORK/TU/.env"; set +a
export GLM_API_KEY="${GLM_API_KEY:-$OPENAI_API_KEY}"
export JUDGE_MODEL="${JUDGE_MODEL:-openai/glm-5.2}"
export PYTHONUTF8=1

PKG="E:/WORK/TU/Task_3_gen-g988-composite-photo-request-rights-audit-20260819T194448Z-1-001/gen-g988-composite-photo-request-rights-audit"

harbor run \
  -p "$PKG" \
  -a opencode \
  -m glmproxy/glm-5.2 \
  --ak 'opencode_config={"provider":{"glmproxy":{"npm":"@ai-sdk/openai-compatible","name":"GLM via LiteLLM","options":{"baseURL":"{env:OPENAI_BASE_URL}","apiKey":"{env:OPENAI_API_KEY}"},"models":{"glm-5.2":{"name":"GLM 5.2","options":{"max_tokens":96000}}}}}}' \
  --n-attempts 5 \
  --n-concurrent 2 \
  -r 3 \
  --agent-setup-timeout-multiplier 3 \
  --ae "OPENAI_API_KEY=$GLM_API_KEY" \
  --ae "OPENAI_BASE_URL=$OPENAI_BASE_URL" \
  --ve "OPENAI_API_KEY=$GLM_API_KEY" \
  --ve "OPENAI_BASE_URL=$OPENAI_BASE_URL" \
  --ve "JUDGE_MODEL=$JUDGE_MODEL" \
  -o "E:/WORK/TU/jobs-g988" \
  --job-name "${1:-glm-5x-baseline-g988}" \
  -y

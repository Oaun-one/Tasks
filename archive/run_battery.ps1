$ErrorActionPreference = "Stop"
$env:Path = "C:\Users\Predator 16\.local\bin;$env:Path"
$env:PYTHONUTF8 = "1"

# load .env
Get-Content "E:\WORK\TU\.env" | ForEach-Object {
  if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
  $p = $_.Split('=', 2)
  if ($p.Length -eq 2) {
    Set-Item -Path ("Env:" + $p[0].Trim()) -Value ($p[1].Trim().Trim('"').Trim("'"))
  }
}
if (-not $env:GLM_API_KEY) { $env:GLM_API_KEY = $env:OPENAI_API_KEY }
if (-not $env:JUDGE_MODEL) { $env:JUDGE_MODEL = "openai/glm-5.2" }

$pkg = "E:\WORK\TU\Task_1_gen-g780-realestate-fairhousing-collateral-audit\gen-g780-realestate-fairhousing-collateral-audit"
$ocCfg = '{"provider":{"glmproxy":{"npm":"@ai-sdk/openai-compatible","name":"GLM via LiteLLM","options":{"baseURL":"{env:OPENAI_BASE_URL}","apiKey":"{env:OPENAI_API_KEY}"},"models":{"glm-5.2":{"name":"GLM 5.2"}}}}}'

harbor run `
  -p $pkg `
  -a opencode `
  -m glmproxy/glm-5.2 `
  --ak "opencode_config=$ocCfg" `
  --n-attempts 5 `
  --n-concurrent 2 `
  -r 3 `
  --agent-setup-timeout-multiplier 3 `
  --ae "OPENAI_API_KEY=$env:GLM_API_KEY" `
  --ae "OPENAI_BASE_URL=$env:OPENAI_BASE_URL" `
  --ve "OPENAI_API_KEY=$env:GLM_API_KEY" `
  --ve "OPENAI_BASE_URL=$env:OPENAI_BASE_URL" `
  --ve "JUDGE_MODEL=$env:JUDGE_MODEL" `
  -o "E:\WORK\TU\jobs" `
  --job-name "glm-5x-baseline-NONC-B1-1001608" `
  -y

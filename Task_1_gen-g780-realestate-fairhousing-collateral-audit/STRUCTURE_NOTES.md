# Structure check against the folder-structure reference

Task: NONC-B1-1001608 / `gen-g780-realestate-fairhousing-collateral-audit`
Layout: **Native / non-connector** (offline, `mcp_servers = []`)

| # | Rule | Status |
|---|---|---|
| 1 | Single flat folder — no zips | **OK** — upload the folder `gen-g780-realestate-fairhousing-collateral-audit/`. The `_FINAL.zip` beside it exists only because the Shannon QC platform accepts uploads as `.zip`; it is not the Drive deliverable. |
| 2 | `golden_trajectory.json` inside `solution/` | **Not producible on this layout — see below** |
| 3 | All eval evidence inside `evaluations/` | **OK** — oracle, 5 GLM runs, 5 stability repeats |
| 4 | Each run: `agent/` + `verifier/` + `config.json` + `result.json` | **OK** — all four present in all 11 run folders |
| 5 | Stability runs `repeat-01`…`repeat-05` | **OK** — 5 repeats, every one reward 1.0, identical verdicts |

## Rule 2 — why there is no `golden_trajectory.json`

This is a structural property of the native/non-connector layout, not an omission.

- The reference solution for this layout is **`solution/solve.sh`**, which Harbor executes
  with `-a oracle`. There are no MCP tool calls to record, because the task has no
  connectors — the agent writes files to `/app`.
- **Harbor's `OracleAgent` does not emit a trajectory.** In harbor 0.21.0
  (`harbor/agents/oracle.py`) the class declares no `SUPPORTS_ATIF` and no trajectory
  output filename. A completed oracle run writes `agent/oracle.txt` and nothing else:

      $ find jobs/oracle-hardened-v1 -name "*trajector*"
      (no results)

      $ cat evaluations/oracle/agent/oracle.txt
      installed gold deliverables into /app:
      fairhousing_audit.csv
      fairhousing_memo.md
      input
      results.json

- By contrast the GLM runs, which use the `opencode` agent (`SUPPORTS_ATIF = True`), do
  carry `agent/trajectory.json` — present in all five under `evaluations/glm-5.2/r1..r5`.

**No file was fabricated to satisfy this rule.** Writing a hand-authored
`golden_trajectory.json` would misrepresent a captured artifact and would also inflate Ship
check E2, which counts steps in the golden trajectory.

**Question for the reviewer / pod:** for native / non-connector gen tasks, should
`solution/solve.sh` + `evaluations/oracle/` be accepted in place of
`solution/golden_trajectory.json`, or is there a supported way to have Harbor emit one that
I have missed?

## Package contents

    gen-g780-realestate-fairhousing-collateral-audit/     <- upload THIS folder
    ├── README.md
    ├── instruction.md
    ├── task.toml
    ├── environment/          Dockerfile + read-only input fixtures (unmodified)
    ├── solution/             solve.sh + files/ (gold answer) (unmodified)
    ├── tests/                verifier.json (14 -> 22 verifiers) + engine
    └── evaluations/
        ├── oracle/           agent/ verifier/ config.json result.json
        ├── glm-5.2/r1..r5/   agent/trajectory.json + verifier/ + config.json + result.json
        └── stability/repeat-01..05/

Supporting evidence sits **outside** the task folder and is not part of the flat deliverable:
`COLD_READ.md`, `CHANGES.md`, `ESCALATION.md`, `SUBMIT.md`, `evidence_coverage_gap/`,
`ORIGINAL_BACKUP/`, `PROPOSAL_if_fixtures_editable/`.

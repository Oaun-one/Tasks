# Evidence: the 14 verifiers pass a knowingly wrong answer

Reproduce:

    export HARBOR_TASK_WORKSPACE=<this folder>
    uv run --with pytest --with pydantic --with "jsonpath-ng>=1.6,<2" --with "tenacity>=9,<10" \
      python -m pytest <task>/tests/test_outputs.py -rA -q

Result: **14 passed** → reward 1.0.

## What is wrong with this answer

| Defect | Why no verifier catches it |
|---|---|
| Only 4 of 7 rows (SEC-01, SEC-06, SEC-07 absent) | No verifier counts CSV rows; `result_section_count` reads results.json, not the CSV |
| **SEC-04 flagged PROTECTED_CLASS_LANGUAGE — the trap is FAILED** | `mandated_trap_clean` regex `^SEC-04\s*,.*none` scans the whole row and matches the `rationale` text "none of the other rules apply" |
| SEC-07 multi-finding row missing | No verifier references SEC-07 at all |
| Memo names one term, explains nothing | `memo_finding_terms` is `A\|B\|C` — alternation, lowest precedence, any single term passes |
| results.json contradicts the CSV (says 7 sections, CSV has 4) | All five `result_*_count` checks compare to hardcoded constants, never recomputed from the delivered artifact |

## Consequence

The task's primary goal — correctly applying the mandated-disclosure exemption to
SEC-04 — is guarded by exactly one verifier, and that verifier is defeatable by
adding a column. A model can fail the trap and still score 1.0.

Findings: F1 (SEC-07 uncovered), F2 (memo_finding_terms free point),
F3 (trap defeatable), F5 (self-reported counts).

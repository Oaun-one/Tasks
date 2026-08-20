# Evidence — the shipped grader scores 14/14 on a knowingly wrong answer

Reproduction of the coverage gap in the **original** `tests/verifier.json` (14 verifiers),
preserved at `../ORIGINAL_BACKUP/`.

## Reproduce

    cd Task_2_gen-g789-dissertation-formatting-spec-audit
    HARBOR_TASK_WORKSPACE="$(pwd)/evidence_coverage_gap/sabotaged_workspace" \
        python -m pytest ORIGINAL_BACKUP/tests/test_outputs.py -q

    14 passed

## What the sabotaged answer gets wrong

`sabotaged_workspace/` is wrong on **3 of the 6 sections**, including the single trap the
task is built around:

| Section | Correct finding | Sabotaged answer | Why it still passes |
|---|---|---|---|
| `SEC-COVER` | `none` | `MARGIN_NONCOMPLIANT` | No verifier exists for this row. |
| `SEC-CH1` | `none` | `FONT_NONCOMPLIANT` | No verifier exists for this row. |
| `SEC-ANNEX-A` | `none` | `MARGIN_NONCOMPLIANT` | `annex_trap_clean` is `(?mi)^SEC\-ANNEX\-A\s*,.*none` — it scans the whole row, so the third column's phrase *"none of the exceptions were applied"* satisfies the check whose entire purpose is to catch this error. |

`results.json` is left at the correct values. Nothing reconciles it against the delivered
CSV, so a file stating 3 flagged sections passes alongside a CSV flagging 6.

The memo passes on `(?i)\bwrong margin|\bline spacing` — alternation binds loosest, so one
of the two terms alone is enough — and on `(?is)\blandscape\w*\b.*\bexception`, which a memo
saying the annex's exception was *ignored* still satisfies.

## What the rebuilt grader does about it

| Gap | Fix in the new `tests/verifier.json` |
|---|---|
| Ungraded rows | One end-anchored row check for **every** audited section, all 30. |
| Row checks scan the whole row | `(?mi)^SEC\-X\s*,\s*FINDING\s*$` — the `finding` cell is pinned end to end, and the prompt pins the header to exactly two columns (`audit_header_is_two_columns`), so there is no third column to hide a phrase in. |
| Clean rows defeatable | The twelve compliant sections each carry a `not_regex_match` guard: no line of the audit may carry a violation label against them. |
| Self-reported counts | Still compared to constants — the engine's `csv` source exposes only `extract_text`, so the DSL cannot recompute them. But with all 30 rows pinned cell-for-cell, a CSV that contradicts `results.json` now fails the row checks. |
| Free-point memo checks | Split into fourteen single-purpose checks, each tied to one numbered item of Deliverable 2; no alternation across independent requirements. |

# Evidence: the baseline grader scores 1.0 on a knowingly wrong answer

The three files in this folder are graded against the **mined baseline** verifier set
(`../ORIGINAL_BACKUP/tests/`), not the hardened one.

`activity_kit_audit.csv` carries four deliberate false positives:

| page | correct finding | this answer says |
| --- | --- | --- |
| PG-02 | `DPI_TOO_LOW` | `DPI_TOO_LOW\|MARGIN_VIOLATION\|ELEMENT_COUNT_SHORT` |
| PG-05 | `none` | `DPI_TOO_LOW\|MARGIN_VIOLATION` |

PG-05 is a clean page flagged twice, and PG-02 gains two violations it does not have. The
audit also contradicts its own `results.json`, which is left at the correct figures.

Reproduce:

    cd Task_4_gen-g774-activity-kit-print-spec-audit
    HARBOR_TASK_WORKSPACE="$PWD/evidence_negative_check" \
      python -m pytest ORIGINAL_BACKUP/tests/test_outputs.py -q

Result: **14 passed** — reward 1.0.

## Why it passes

The baseline set has one assertion per *rule*, not per *page*, and each is presence-only:

    dpi_flagged      ^PG-02,.*DPI_TOO_LOW
    margin_flagged   ^PG-03,.*MARGIN_VIOLATION
    element_flagged  ^PG-04,.*ELEMENT_COUNT_SHORT
    bleed_trap_clean ^PG-01,.*none

Nothing asserts the *absence* of a code, and PG-05 and PG-06 have no verdict checked at
all. Two of six pages are ungraded and the other four are graded one-sidedly.

## What replaced it

The hardened set asserts the exact finding set for all 30 pages — every required code
present and every other code absent. `../../tools/g774_negative_check.py` runs nine
plausible misreadings of PRINT-KIT-2 through the hardened grader; each loses between 6 and
26 verifiers and none scores 1.0.

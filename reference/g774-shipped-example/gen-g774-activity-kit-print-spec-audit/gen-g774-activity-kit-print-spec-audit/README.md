# gen-g774-activity-kit-print-spec-audit

Native Harbor (schema 1.3) non-connector task. Offline: the agent gets a
writable `/app`, four read-only files under `/app/input`, and no network
dependency at grade time.

## What the task asks

A prepress operator has to pre-flight a 36-page printed activity kit before it
is released to two presses on Friday. The batch is `input/kit_pages.csv`; the
studio standard is `input/print_production_standard.md` (PRINT-KIT-3); the press
each section runs on is in `input/section_plan.csv`; the limits for each press
are in `input/press_profiles.csv`.

Four deliverables, all written to `/app`:

| File | Contents |
| --- | --- |
| `preflight_audit.csv` | one row per page, keyed by `page_id`, with a `finding` column carrying every code that page breaches (joined with `\|`) or `none` |
| `section_summary.csv` | one row per section: `section_id`, `press_id`, `page_count`, `flagged_pages`, `imposition` |
| `preflight_memo.md` | studio memo: every flagged page with its measured value and the limit it missed, why each cleared-but-suspicious page is clear, the pages whose verdict turns on their press, and the sections that cannot be imposed |
| `results.json` | fourteen derived figures for the batch |

## Why it is non-trivial

Seven page-level rules and one section-level rule, applied to 36 pages: 252
page-rule comparisons, which is past the point where the work can be eyeballed
reliably. The difficulty is in the rules rather than the volume, and it comes
from the standard as written rather than from anything withheld:

1. **The threshold is not a constant.** Resolution, ink coverage and spot-colour
   limits are per-press. A page reaches its press only through its section, so
   every comparison needs a two-hop join (page → section → press). PG-06 and
   PG-10 both land at 270 dpi effective and get opposite verdicts for this
   reason alone.
2. **The measured value is derived, not read.** §2 compares the *effective*
   resolution — artwork resolution divided by the placed scale, rounded down.
   PG-03 carries 450 dpi artwork and still fails, because it is placed at 200%.
   PG-04 carries 240 dpi and passes, because it is placed at 80%.
3. **An exception that also creates an obligation.** A full-bleed page is
   released from the safe-margin rule (§3) and, by §4, is the only kind of page
   that owes a bleed allowance. Reading the exception as a blanket pass clears
   four pages wrongly; applying the margin rule to full-bleed pages anyway
   flags four others wrongly.
4. **Every limit is inclusive.** Fifteen pages sit exactly on at least one
   limit, so a single `<=` in place of `<` floods the audit with false findings.
5. **A section rule that must not become a page rule.** §9 constrains bound
   sections only; three unbound sections have page counts that look wrong and
   are not findings.
6. **Two figures count the thing, not the pages.** `finding_total` is 39 across
   21 flagged pages; `element_shortfall_total` is 12 across 7 short pages.

## Package layout

```
instruction.md                     the prompt as issued
task.toml                          schema_version 1.3, offline, no MCP servers
environment/Dockerfile             python:3.12-slim-bookworm, copies input/ to /app/input read-only
environment/input/                 the four read-only files the agent sees
tests/verifier.json                the scored verifier set
tests/rl_world_verifiers/          vendored verifier engine
tests/test.sh, tests/test_outputs.py   Harbor verifier entrypoint; reward is 1 only if every check passes
solution/solve.sh                  Oracle entrypoint — installs solution/files/ into /app
solution/files/                    gold deliverables
solution/final_answer.md           the gold answer, rule reading, and the wrong answers this fixture reaches
solution/golden_trajectory.json    reference tool-call path (ATIF-v1.7)
evaluations/                       oracle, glm-5.2/r1–r5, and stability/repeat-01–05
```

## Grading

The verifier set is deterministic end to end — no rubric assertion, no judge, no
network, no dependence on the current date.

Every assertion is written to accept a correct answer in any reasonable shape:
extra or reordered columns, quoted fields, multi-code finding cells in any
order, `none` in any case, and a memo laid out as prose or as tables. Wrong
answers are caught by the verdict, not by the formatting.

Reward is binary. `tests/test.sh` writes reward 1 only when the whole set
passes, so a run counts as a pass only if the entire audit is right.

# gen-g988-composite-photo-request-rights-audit

Native Harbor (schema 1.3) non-connector task. Offline: the agent gets a writable `/app`,
four read-only files under `/app/input`, and no network dependency at grade time.

**Outcome: Oracle 1.0, pass rate 5/5, marked too easy — the row is kept.**
See "Difficulty and the honest pass rate" below.

## What the task asks

An intake desk has a backlog of composite photo-edit requests. The agent audits every
in-scope request against INT-09 (the intake rights policy), the client accounts and their
master agreements, and the register of licences the shop holds.

Four deliverables, all written to `/app`:

| File | Contents |
| --- | --- |
| `composite_request_audit.csv` | one row per audited request, `request_id` and `finding`, every breached code joined with `\|` or `none` |
| `account_summary.csv` | one row per account: `account_id`, `account_type`, `request_count`, `flagged_requests`, `escalation` |
| `composite_request_memo.md` | rights-review memo: the audit date, the out-of-scope requests and why, every flagged request with the record that decides it, what the personal-use allowance clears, the lapsed agreements and what they change, and the escalating accounts with the batch figure they were measured against |
| `results.json` | eleven derived figures |

## Changes from the mined baseline

The baseline is in `../ORIGINAL_BACKUP/`. `task.toml` is unchanged — same name,
description, keywords and `source_config`.

Everything graded is generated from `tools/g988_build.py` (the data model and adjudicator)
via `tools/g988_emit.py`, so the fixtures, the gold answer and `tests/verifier.json` cannot
drift apart.

### 1. The grader was replaced

The baseline had 13 verifiers and **passed a knowingly wrong answer 13/13** — an audit with
7 of 8 account rows over-flagged and 4 of 8 rows never checked at all.
`../evidence_coverage_gap/` reproduces that in one command. The current set has **91
verifiers**, asserting the exact finding set per request (every required code present *and*
every other code absent), per-account rollup rows, eleven derived figures recomputed from
the batch rather than read back from the model's own summary, and the memo content
INT-09 §9 requires.

### 2. §3 gained the prominence cap the fixture was already shaped for

`max_character_area_pct` (register), `character_px_area` and `canvas_px_area` (log) were
present in the data and referenced by no rule — four dead columns whose values were
nevertheless laid out on near-boundary ratios. §3 now states the rule they were for:

    character area % = character_px_area / canvas_px_area

against the **governing** licence's `max_character_area_pct`, in the §2 supersession sense.
This is the strongest coupling in the task:

- **REQ-05** names LIC-103. LIC-109 supersedes it and *narrows* the cap 35% → 20%. At 28.7%
  the request clears the row it names and breaches the row that governs it.
- **REQ-06** sits at exactly 30.0% against a 30% cap and is within it (the cap is inclusive).
- **REQ-09** (41.5% vs 40) and **REQ-27** (25.1% vs 25) are near-misses that flip clean
  requests to flagged.
- **REQ-01, REQ-22, REQ-32** are all over their caps and all clear, because the §3
  personal-use allowance releases a request from §3 entirely — cap included — and from
  nothing else. REQ-32 is still `MISSING_MINOR_CONSENT`.

### 3. §8 escalation was tuned to a knife edge

§8 is the one threshold the model has to derive: an account escalates when its own flagged
share is **strictly greater** than the batch-wide flagged share, or when any single request
carries three or more findings. The batch figure is given nowhere.

The batch share is now exactly **14/28 = 0.500**, and **five of the eight accounts sit
exactly on it**:

| account | share | escalates | on |
| --- | --- | --- | --- |
| ACC-01, ACC-04, ACC-05 | 0.500 | no | equal is not strictly greater |
| ACC-02, ACC-03 | 0.500 | yes | second limb only — a three-finding request |
| ACC-07 | 0.667 | yes | first limb only |
| ACC-08 | 0.667 | yes | both limbs |

Applying either limb alone gets the batch wrong, and reading `>` as `>=` flips three
accounts at once. Because the threshold is derived from the audit, a single wrong request
verdict anywhere moves the batch share off 0.500 and flips those three accounts with it.


### 4. The prompt was stripped back to a work request

The prompt had drifted into a recipe: it enumerated every `results.json` key with a gloss
(`finding_total` "every finding raised across the batch, **not the number of requests
carrying one**"), listed six things the memo had to cover, and announced the traps outright
— "**Not every row** in the log is in scope", "several of the clearances live **outside**
it", "the accounts carry **a rule of their own**", "say which accounts landed **exactly on
that figure**". That measures instruction-following, not reasoning, and it makes the task
trivially scriptable.

`instruction.md` is now a colleague's request: the backlog, the four filenames, the column
layouts, and "the eleven figures named in INT-09 §9". 226 words, no reasoning disclosed.
Every requirement it used to carry now lives in the policy as **§9 What an audit reports**,
written the way a policy writes it. Nothing is withheld — the model has to read INT-09 and
work out which records reach which rule, that withdrawn rows count towards nothing, that the
batch share has to be derived from its own audit, and that a tie does not escalate.

INT-09 §1 also now states the reporting format for a multi-code cell (all codes, joined with
`|`, in any order). That had only ever been in the prompt; removing the recipe removed it
too, and a battery run against the gap failed four of five runs on the six multi-finding
requests alone — the models had the findings right and could not know the delimiter. That is
a formatting ambiguity, not difficulty, and it was repaired rather than kept.

## Grading

Deterministic end to end — no rubric assertion, no judge, no network, no dependence on the
current date. Reward is binary: `tests/test.sh` writes 1 only when all 91 pass.

Assertions accept a correct answer in any reasonable shape: extra or reordered columns,
quoted fields, finding codes in any order within a cell, `none` in any case or as a
synonym, and a memo written as prose or as tables. Memo checks that scope a fact to the
record it belongs with match in either order and are case-insensitive, so a memo that opens
a sentence with "Withdrawn" is not marked down for typography.

`tools/g988_negative_check.py` and the §3/§8 checks run eleven distinct misreadings of
INT-09 through the real grader. Every one loses verifiers; none scores 1.0:

| misreading | verifiers lost |
| --- | --- |
| never opens the licence register | 23 |
| ignores the §3 prominence cap | 13 |
| allowance treated as releasing the cap too | 11 |
| ignores the `supersedes` column | 16 |
| personal-use allowance as a general pardon | 15 |
| routing cleared by `account_type` | 12 |
| audits the withdrawn rows | 11 |
| reads the cap off the named row, not the governing one | 5 |
| `>=` for `>` in §8 | 4 |
| batch share over all 32 logged rows, not the 28 audited | 4 |
| cap read as exclusive | 3 |

## Difficulty and the honest pass rate

**5 of 5 GLM-5.2 runs fully pass** (`evaluations/glm-5.2/r1..r5`, Trials 5 / Exceptions 0,
one task checksum across all five). The task is reported as **too easy** and the row is
kept.

This is a measured result, not an unfinished one. The hardening above was taken as far as
it goes honestly: coupling (a derived ratio against a supersession chain), a derived
threshold with five accounts on the line, scale, and memo content graded against the
artifact. Earlier builds of this same task measured 3/5 and 4/5, and both of those numbers
were traced to defects in my own verifiers rather than to model failure — in one case a
run that wrote *"3 accounts land exactly on 50% (ACC-01, ACC-04, ACC-05) — not strictly
greater, so they stay with intake"* scored 0 because the pattern required the reason to
follow the account id and did not accept the adverb. Those checks were repaired rather than
kept, and the pass rate rose accordingly.

No verifier in this set grades a fact the prompt does not ask for, and none rejects a
defensible correct answer that I could construct. The 5/5 is what GLM-5.2 actually does on
a fair grader.

## Package layout

```
instruction.md                        the prompt as issued
task.toml                             schema_version 1.3, offline, no MCP servers
environment/Dockerfile                python:3.12-slim-bookworm, copies input/ read-only
environment/input/                    the four read-only files the agent sees
tests/verifier.json                   the 91 scored verifiers
tests/rl_world_verifiers/             vendored verifier engine
tests/test.sh, tests/test_outputs.py  Harbor entrypoint; reward 1 only if every check passes
solution/solve.sh                     Oracle entrypoint — installs solution/files/ into /app
solution/files/                       gold deliverables
solution/golden_trajectory.json       promoted from a reward-1.0 GLM-5.2 run
evaluations/                          oracle, glm-5.2/r1–r5, stability/repeat-01–05
```

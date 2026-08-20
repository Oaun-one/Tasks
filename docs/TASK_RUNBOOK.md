# Turing ComputerBench — how I want these tasks done

Portable runbook. Copy this to any machine that runs tasks for this workstream.
Everything here is measured on real batteries, not inherited from the circulated playbook —
where the two disagree, this file wins for **this** workstream.

---

## 0. The job in one paragraph

Tasks arrive auto-generated, too easy, and usually with a broken grader. My job is to make
one task **fair, hard, and correctly graded**, then report an **honest** pass rate. I am a
question editor and examiner, not a developer.

**Expect the first battery to be 5/5. That is normal.** Hardening is the job.

| | |
|---|---|
| Band | **at most 2 of 5 runs may fully pass (≤2/5)** |
| Oracle | must be **exactly 1.0**, every time, before any battery |
| Can't reach band fairly | mark **too easy**, **keep the row**, say so in the README |
| "Fully pass" | reward exactly 1.0. 90 of 91 verifiers is a fail. Report all five rewards. |

---

## 1. Machine setup

```bash
harbor --version          # expect 0.21.x ; lives in ~/.local/bin, needs a new terminal after install
docker version            # must be running
docker ps                 # ALWAYS check before launching a battery
```

`.env` at the repo root: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `JUDGE_MODEL=openai/glm-5.2`.
`JUDGE_MODEL` must be set even on tasks with no rubric — the judge module is imported at
package init and its absence fails collection.

gcloud is **not** needed (public base image). **Never `docker image prune -a`** — it deletes
the shared multi-GB base image.

### Run scripts — keep one pair per task

`tools/run_oracle_<task>.sh` and `tools/run_battery_<task>.sh`. Copy an existing pair and
change only `PKG` and `--job-name`.

Non-negotiables in the battery script:

```bash
-a opencode  -m glmproxy/glm-5.2
--ak 'opencode_config={"provider":{"glmproxy":{...,"models":{"glm-5.2":{"options":{"max_tokens":96000}}}}}}'
--n-attempts 5
--n-concurrent <N>        # PER MACHINE - see below. Never copy another box's number.
-r 3
--agent-setup-timeout-multiplier 3
```

- **Run batteries from Git Bash, never PowerShell.** PS 5.1 strips the inner quotes from
  `--ak`; harbor then parses it as a string and dies with
  `AttributeError: 'str' object has no attribute 'items'`, reporting **0 trials /
  5 exceptions** — which looks exactly like 0/5 but is a crash.
- **`max_tokens: 96000`** or runs truncate at the reasoning ceiling, produce no
  deliverables, and score 0.0 indistinguishably from a hard failure.
- **`--n-concurrent` is machine-specific.** Budget ~1.5 GB Docker memory and ~1 CPU per
  concurrent trial; cap at `NCPU - 1` and never above `--n-attempts` (5).
  `docker info --format '{{.MemTotal}} {{.NCPU}}'` first. 4 GB -> 2, 6 GB -> 3, 8 GB -> 4-5,
  12 GB+ -> 5. Too high is worse than too low: containers get OOM-killed or hit
  `AgentSetupTimeoutError`, and those zeros look exactly like model failures. Check with
  `docker stats --no-stream` during the first battery and drop by one if anything is pegged.
- `Trials: 0 / Exceptions: N` is infra. **Never report it as a pass rate.**
  `Trials: 5 / Exceptions: 0` is a real measurement.

---

## 2. Package layout (non-connector)

```
<task-slug>/
  instruction.md          the prompt — see §4, this is where most tasks are lost
  task.toml               DO NOT EDIT (name/description/keywords/source_config)
  README.md               cumulative change summary + the honest pass-rate section
  environment/
    Dockerfile            editable only to pin the base image digest
    input/                the fixtures — editable, and hardening lever #2
  solution/
    solve.sh              oracle entrypoint
    golden_trajectory.json  promoted from a reward-1.0 GLM run
    files/                the gold answer
  tests/
    verifier.json         THE grading spec — NEVER rename to manifest.json
    test_outputs.py       pytest wrapper
    test.sh               binary: reward 1 only if every verifier passes
    rl_world_verifiers/   vendored engine
  evaluations/
    oracle/  glm-5.2/r1..r5/  stability/repeat-01..05/
```

**Never rename `tests/verifier.json`.** The platform detects the non-connector layout from
that filename; renamed, it parses the file as a task-harness config → `Verifiers (0)`, no
prompt. The onboarding doc's "rewrite to manifest.json" step does not apply here.

**Pin the base image by digest** — `FROM python:3.12-slim-bookworm@sha256:...`. Delivery
Gate S1 is blocking. Get it with `docker buildx imagetools inspect <image> | grep Digest`.

---

## 3. Build the package from ONE generator

Never hand-edit fixtures, gold and verifiers separately — they drift and the Oracle dies.

```
tools/<task>_build.py    the data model + the adjudicator (the single source of truth)
tools/<task>_emit.py     writes environment/input/, solution/files/, tests/verifier.json
tools/<task>_negative_check.py   runs plausible misreadings through the REAL grader
```

The adjudicator computes the gold; the emitter derives both the fixtures and the assertions
from it. Then gold and grader **cannot** disagree.

`negative_check` is not optional. Every misreading of the spec must lose verifiers. Target:
each one loses ≥3. If a misreading scores 1.0, that misreading is a free pass.

---

## 4. The prompt must NOT be a recipe

**This is the single biggest mistake and it cost a whole day.**

A prompt that enumerates the steps measures instruction-following, not reasoning. GLM
executes the checklist and scores 5/5. Things that leak the answer:

| never write this | why |
|---|---|
| "say which accounts landed **exactly on that figure**" | reveals that ties exist |
| "**Not every row** is in scope" | reveals the withdrawn/excluded rows |
| "the clearances live **outside** the log" | reveals the join |
| "the accounts carry **a rule of their own**" | reveals the second-level rule |
| "`finding_total` (**not** the number of rows carrying one)" | pre-solves the trap |
| a bulleted list of what the memo must cover | turns the memo into a form to fill in |

**Instead:** the prompt is a colleague's request — ~120–220 words, natural voice, the
deliverable filenames, and the column layouts (format is fine; reasoning is not).

**Move every definition into the spec document** (`input/*.md`) as a numbered section
written the way a policy writes it — e.g. `§9 What an audit reports`, with a figures table
and a paragraph on what a memo records. Nothing is withheld, so grading stays fair, but the
model has to **find and connect** it instead of being handed it.

Rule of thumb: after writing the prompt, grep it for the trap words. If a hit explains
reasoning rather than format, delete it.

---

## 5. Hardening: what actually works

Measured across ~10 batteries / 50 trials on two tasks.

### Does NOT work
- **Stacking independent rules.** GLM writes one script; ten rules are ten easy checks.
- **Verifier count.** 54 verifiers → 5/5. 98 verifiers → 5/5. No effect on its own.
- **Coupling alone.** A build with two-hop joins, derived values, a conditional amendment
  and order-scrambled dedupe scored 5/5.
- **Scale alone.** 30 rows → 36 rows: no change.
- **Removing the recipe alone.** Necessary and correct, but by itself the score did not move
  — GLM does the discovery fine.

### Does work (in order of what actually produced failures)
1. **A derived threshold with items sitting exactly on it.** Compute the threshold from the
   candidate's own output, then place several rows precisely at it where the rule says
   "strictly greater". A single wrong verdict anywhere shifts the threshold and flips them
   all. This is the strongest genuine lever found.
2. **An exception that also creates an obligation**, and an **exception to the exception**
   (e.g. an exemption that stops at one category).
3. **A rule reading the output of an earlier rule** — a rollup whose verdict depends on the
   per-row findings, so upstream slips propagate instead of staying local.
4. **A superseding record that NARROWS terms**, combined with a derived ratio — read the row
   the item names and you clear it; follow the chain and it fails.
5. **Inclusive limits with many rows exactly on the boundary** — one `<=` for `<` floods the
   output.

### Never
Ambiguity, unreadable phrasing, verifiers for things the spec never asks, narrowing to the
golden path, or changing verifier count to hit a number. **If a careful analyst could land
on two defensible answers, the task is broken, not hard.**

---

## 6. Writing verifiers that don't lie

Per-row verdicts must be **exact-set**: every required code present **and** every other code
absent. Presence-only grading is how mined graders score 13/13 on knowingly wrong answers.

```
(?im)^(?=[^\n]*\bROW-05\b)(?=[^\n]*\bCODE_A\b)(?=[^\n]*\bCODE_B\b)(?![^\n]*\bCODE_C\b)...
```

Accept a correct answer in any reasonable shape:
- codes in **any order** within a cell, and **any join character** (`|`, `;`, `,`, space,
  quoted CSV) — grade the set, not the punctuation;
- extra/reordered columns, quoted fields;
- `none` in any case, plus synonyms;
- memo as prose **or** tables.

**Proximity checks** (a row id near its reason) must be **bidirectional** and
**case-insensitive** — a memo that states the reason before the id, or opens a sentence with
"Withdrawn", is saying the same thing. A one-directional, case-sensitive check grades
typography and will fail correct answers.

**Pin the output shape in the spec** if the grader depends on it. "One row per item, all
codes in one cell" — otherwise a model emitting long format (one row per finding) is
defensible and loses on layout, not reasoning.

**Free points**: if you can't describe a plausible attempt that fails a verifier, it's a
free point. Reward is binary so it doesn't inflate the pass rate, but it inflates partial
credit and reviewers look for it.

**Never grade the model's self-report.** Recompute from the artifact.

---

## 7. Workflow

1. **Cold read.** Read only `instruction.md` and `input/`. Write down every guess you had to
   make and every place the prompt leaks the answer. Do this **before** opening `tests/` —
   the only unbiased look you get. Save as `COLD_READ.md`.
2. **Write your own verifier list**, then diff against `tests/verifier.json`. Note gaps in
   both directions.
3. Build the generator (§3). **Oracle → exactly 1.0.**
4. **Negative check** — every misreading must lose verifiers.
5. **5× GLM battery** (Git Bash, 5 concurrent).
6. **Read every failing trajectory.** Classify each failure:
   **model limitation** (good) / **ambiguity** (fix the prompt or spec) /
   **verifier defect** (fix the grader) / **infra** (exclude and replace).
7. Harden (§5) → re-Oracle 1.0 → re-run the battery.
8. Assemble evidence, write README, zip, QC, gates, Drive, tracker, peer review.

### The re-run rule
After a change ask: **did this alter what the model must do, or how it is graded?**
- **No** (README, comments, metadata strings) → re-Oracle, keep the battery.
- **Yes** (prompt, spec, assertions, fixtures, gold) → re-Oracle **and** re-run the battery.

Batteries are ~8 minutes. Don't re-run reflexively — but never report a battery that
predates the current package.

---

## 8. Traps that cost real time

1. **Never edit the package while a battery is running.** Harbor rebuilds the image per
   trial; the run silently spans two package versions. Check `result.json → task_checksum`
   — **all five trials must share one checksum**, or the measurement is void.
2. **A pass rate from another machine is not evidence about yours.** Check `result.json` for
   a foreign path or a different `model_name`. A shipped "2/5" re-ran as 4/5 here.
3. **Zip with `tools/zip_package.py`, never `Compress-Archive`.** PowerShell omits directory
   entries; the platform walks the archive by them and reports a misleading
   *"upload contains N JSON files"*.
4. **Strip `__pycache__` / `.pytest_cache`** before zipping.
5. **Delete stale zips** from the task folder so the wrong one can't be uploaded.
6. **CTRF aggregates parametrised tests into one entry.** A `verifier_summary.json` built
   from `ctrf.json` has 1 item, and QC reports *"non-connector trial payloads carry no
   per-check verifier breakdown"* — which is **valid**, not a false positive. Rebuild the
   summary from `test-stdout.txt`, which has the `PASSED|FAILED ...[<name>]` lines.
7. **Harbor's `OracleAgent` emits no trajectory.** For `solution/golden_trajectory.json`,
   promote a **reward-1.0 GLM run's** `agent/trajectory.json`.
8. `all predefined address pools have been fully subnetted` → `docker network prune -f`.
   After a killed job, `docker ps -a --filter status=exited` → `docker rm` the dead
   `gen-*__env-main-1` containers first, then prune.
9. `AgentSetupTimeoutError` → `--agent-setup-timeout-multiplier 3` (already in the scripts).
10. The `rl_world_verifiers` engine **rejects a `category` field** on verifiers
    (`extra_forbidden`). The "delete `category: secondary`" step does not apply here.
11. `environment/input/` **is** editable on these gen tasks. Constraint: stay on the
    original topic and metadata, don't build a new task, keep it harbor-executable.

---

## 9. Diagnosing a failure — before you celebrate it

**A drop in pass rate is a defect in my grader until proven otherwise.** Every single time a
battery came back below 4/5 in this workstream, the cause was my own bug:

| symptom | actual cause |
|---|---|
| 2 runs fail the same memo check | regex required the reason *after* the id; run wrote it before |
| 4 runs fail the same 6 rows | those 6 were the multi-code rows; spec never pinned the table shape |
| a run fails one check on "not strictly greater" | alternation had `not greater`, not `not \w+ greater` |

Procedure, every time:
1. `grep -E "^FAILED" <trial>/verifier/test-stdout.txt` — which checks, exactly.
2. If several runs fail the **same** checks, suspect the grader, not the model.
3. Read the trajectory and find what the run actually wrote.
4. Test the regex against 4–5 realistic phrasings that **must pass** and 2 omissions that
   **must fail**.
5. Only if it survives that is it a real difficulty signal.

Bimodal rewards (0.9, 0.1, 0.9) = a coin-flip on an ambiguity → fix the prompt.
Reward exactly 0.0 → check for `exception.txt` / missing trajectory before calling it hard.

---

## 10. Packaging and submission

Every run folder needs **agent/ + verifier/ + config.json + result.json**.
`result.json` must carry `model: "GLM-5.2"`, `overall_pass`, `final_answer`, `reward`,
and judge provenance. `tools/assemble_evaluations_<task>.py` builds all of this.

`stability/` is for genuine fresh-container re-grades of the **frozen gold answer**
(`harbor run -a oracle --n-attempts 5`), not for the five GLM rollouts. If you don't have
real stability re-checks, ship none — don't fake it.

Do **not** include job-level `config.json`, `lock.json`, `job.log`, or the job-root
`result.json`.

### QC platform
`https://qc-api-713053229214.us-central1.run.app/` — sign in with the `@turing-gpt-git.com`
account, paste the GLM key top right → **Check Key** → wait for `glm-5.2` ready. Don't touch
the prefilled Base URL. **One task per ZIP.** ~2–5 min, silent until done.

Report is **advisory**; a human decides. Findings are input, my dispositions govern. Every
"false positive" needs written justification citing files or the report's own numbers, and
**I write the free text myself** — pasted LLM output gets rejected.

Recurring genuine false positives on this layout:
- *"prompt requirement `input/` has no verifier coverage"* — environment statement, not an ask.
- *"README claims N verifiers but runtime has one native_harbor_verifier"* — one entry
  parametrises into N assertions; both true.

`IQC-GATE-*` findings ("staged model review is partial", "delivery semantic audit skipped")
are about the **tool's own pipeline**, not the package — usually a token/time limit. Check
`report.html` for which stages ran; re-run the submission before dispositioning a blocker.

### Gates
- **Internal Gate** — advisory. A FAIL here is not fatal and does not decide shipping.
- **Delivery Gate** — decides. /100, pass mark 95, four blocking items.
- **A 5/5 task caps at 90/100.** E3 is worth 10 and needs at least one run that failed for a
  real reason. That is the gate agreeing with the "too easy" call, not something to edit around.

### Drive + tracker
Task folder and QC reports go to **separate** Drive locations. The folder goes up **flat,
not zipped**. Tracker columns: Batch · Task ID · Dataset Task Name · Task Link *(leave)* ·
**Modified Task Link** · **QC Report Link** · Golden Trajectory Zip File · Trainer ·
**Status** · Date Started · Date submitted · **Proof … QC Tool** · **Trainer Notes** ·
**Pass Rate (pass@5)** · Trainer AHT.

There is no "Ship QC Gate Score" column — put the score in **Trainer Notes**, with a line on
any known limitation so a reviewer sees it from me first.

**A completed task without a matching completed peer review is not eligible for payment.**
That is the only explicit payment condition. Always pair off the review.

---

## 11. Reporting honestly

- Report **all five** individual rewards, never just the mean.
- State the pass rate as measured on the **exact shipping package** (checksums matched).
- If the band was reached on something other than reasoning — a formatting rule, a layout
  convention — **say so in the README**, in my own words, with the numbers. A reviewer will
  find it; better it comes from me.
- If it can't be brought into band fairly: **mark too easy, keep the row.** That is a
  legitimate, documented outcome and it has shipped at 90/100 before.

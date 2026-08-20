# START HERE — Turing ComputerBench task work

**Addressed to the AI assistant on this machine.** Read this file end to end before running
anything. It is self-contained: setup from a bare machine, the method, and submission.

---

# PART 0 — What this job actually is

Turing builds an evaluation benchmark for an AI lab (the client). Tasks are auto-generated
from mined sources, arrive **too easy**, and usually have **broken graders**. Your operator's
job — and yours — is to turn one draft task into a **good** task, then report an **honest**
measurement of how hard it is.

You are a **teacher writing a test**, not a developer shipping a feature. The task is the
test; GLM-5.2 is the student; the verifiers are the marking rubric.

## What "good" means (the client's five criteria)

1. **Functional** — not broken. The data, logic and harness actually work.
2. **Appropriately difficult** — the target band is **1/5–2/5** GLM runs fully passing.
3. **Realistic** — a prompt a real colleague would send, not a step-by-step recipe.
4. **Fairly and objectively graded** — the rubric marks what the prompt asked, accepts any
   defensible correct answer, and rejects wrong ones.
5. **Correctly packaged** — ≥4 GLM runs, ≥1 successful run, ≥2 stability runs, a delivery QC
   report, standard file layout.

## The rule that overrides everything else

**Do not game the QC score.** The QC system is an approximation of what the client wants, not
the goal. Making verifiers arbitrarily harsh, or stuffing the prompt with guidance, or
re-rolling batteries until a lucky failure appears, will produce a high score and a rejected
task. This is reward hacking and the client screens for it.

A pass rate is only meaningful if the failures are **real** — reasoning or process errors by
the model, not defects in your task or grader. **A 5/5 honestly measured and clearly labelled
"too easy" is a better deliverable than a 1/5 bought with a broken regex.**

Success is client acceptance, not a number. 95/100 is a heuristic, not a gate.

---

# PART 1 — Set up the machine from zero

## 1.1 Docker Desktop

Install Docker Desktop and **start it**. Every trial builds and runs a container.

```bash
docker version          # must print a Server version
docker ps               # must not error
```

- **Never run `docker image prune -a`.** It deletes shared multi-GB base images.
- Give Docker as much RAM as the machine can spare — this is what caps how many trials you can
  run at once. See §1.2.

## 1.2 Decide this machine's concurrency — do not copy a number

`--n-concurrent` is **per-machine**. It is the single biggest lever on how long a battery
takes (5 concurrent ≈ 8 min, 2 concurrent ≈ 13 min), and setting it too high is worse than
too low: containers get OOM-killed or time out during agent setup, and the resulting zeros
look exactly like model failures.

Measure first:

```bash
docker info --format 'docker RAM: {{.MemTotal}} bytes / CPUs: {{.NCPU}}'
# Windows host totals, for comparison:
wmic ComputerSystem get TotalPhysicalMemory   # or: systeminfo | findstr /C:"Total Physical Memory"
```

Budget roughly **~1.5 GB of Docker memory and ~1 CPU per concurrent trial** — the container
itself is small (~400 MB), but each one bootstraps node and runs the opencode agent, and the
image build peaks higher.

| Docker memory allotted | sensible `--n-concurrent` |
|---|---|
| 4 GB | 2 |
| 6 GB | 3 |
| 8 GB | 4–5 |
| 12 GB | 5–6 |
| 16 GB+ | 6–8 (rarely worth more than 5 — `--n-attempts` is only 5) |

Also cap it at `NCPU - 1` so the host stays responsive, and never above `--n-attempts`
(5) — extra slots do nothing.

**Validate the choice on the first battery**, don't assume it:

```bash
docker stats --no-stream        # while a battery runs: check none are pegged at their limit
docker ps --format '{{.Names}}' | wc -l   # should equal your --n-concurrent
```

If you see `AgentSetupTimeoutError`, containers dying mid-run, or the host swapping, **drop
the concurrency by one and re-run**. A battery that finishes slowly is worth infinitely more
than a fast one whose zeros you cannot trust.

## 1.3 Git Bash (Windows)

Install Git for Windows. **All batteries must be launched from Git Bash, never PowerShell.**
PowerShell 5.1 strips the inner quotes out of the `--ak 'opencode_config={...}'` argument;
harbor then parses it as a string and dies with
`AttributeError: 'str' object has no attribute 'items'`, reporting **0 trials / 5
exceptions** — which looks identical to a 0/5 pass rate but is a crash.

## 1.4 uv, then harbor

```bash
# uv (if absent): https://astral.sh/uv  — or `pipx install uv`
uv tool install harbor
harbor --version        # expect 0.21.x
```

`uv` installs shims to `~/.local/bin` (Windows: `C:\Users\<you>\.local\bin`). **Open a new
terminal afterwards** or they will not be on PATH.

> **You do NOT need gcloud, and you do NOT need Artifact Registry access.** These are
> *non-connector* tasks on a **public** Docker base image. If someone suggests chasing IAM on
> a GCP project, stop — it is not part of this workflow.

If `uv tool install harbor` fails, copy a working install between machines (both Windows):

1. `…\AppData\Roaming\uv\tools\harbor\` → same path on the new machine
2. `…\.local\bin\{harbor.exe, hb.exe, hr.exe}` → same path
3. Edit `…\uv\tools\harbor\uv-receipt.toml`, fixing the three `install-path` entries
4. New terminal → `harbor --version`

## 1.5 Python (for the local grader dry-run)

Python 3.12+ with:

```bash
pip install "pytest==8.4.1" "pytest-json-ctrf==0.3.5" "pydantic==2.12.5" \
            "jsonpath-ng>=1.6,<2" "tenacity>=9.0,<10"
```

These mirror the container's pins, so a local pytest verdict means what it means in Harbor.

## 1.6 `.env` at the working-directory root

```
OPENAI_API_KEY=<the personal LiteLLM proxy key>
OPENAI_BASE_URL=<the team proxy base URL>
JUDGE_MODEL=openai/glm-5.2
QC_REASONING_EFFORT=none
QC_MAX_OUTPUT_TOKENS=32768
QC_RETRY_MAX_OUTPUT_TOKENS=65536
QC_STAGE_RETRIES=3
QC_TIMEOUT_SECONDS=600
```

`JUDGE_MODEL` must be set **even on tasks with no rubric verifier** — the judge module is
imported at package init and its absence fails the whole test collection.

The `QC_*` values matter: at the defaults (`120` / `1` retry) the QC platform's own staged
review times out and crashes with
`RuntimeError: judge_api.py failed … timed out`, often masked by a secondary
`UnboundLocalError: 'why'` in its error handler. That is **infra, not a task defect**.

## 1.7 Verify before starting work

```bash
docker version && docker ps
docker info --format 'docker RAM: {{.MemTotal}} / CPUs: {{.NCPU}}'   # sets --n-concurrent
harbor --version
python -c "import pydantic, jsonpath_ng, tenacity, pytest; print('deps ok')"
ls .env
```

Record the concurrency you chose in the battery script so it is not re-guessed each time.

---

# PART 2 — Repo layout and the scripts you need

```
<work-root>/
  .env
  CLAUDE_START_HERE.md          this file
  tools/                        per-task generators + shared helpers
  jobs-<task>/                  harbor output (never edit by hand)
  Task_N_<task-slug>/
    <task-slug>/                THE PACKAGE — this is what gets zipped
    ORIGINAL_BACKUP/            byte copy of the mined draft, for diffing
    COLD_READ.md  CHANGES.md    your working notes
```

Create these three scripts per task. **Only `PKG` and `--job-name` change between tasks.**

### `tools/run_oracle_<task>.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
set -a; . "<work-root>/.env"; set +a
export PYTHONUTF8=1
PKG="<work-root>/Task_N_<slug>/<slug>"
harbor run -p "$PKG" -a oracle --n-attempts 1 -r 1 \
  -o "<work-root>/jobs-<task>" --job-name "${1:-oracle}" -y
```

### `tools/run_battery_<task>.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
set -a; . "<work-root>/.env"; set +a
export GLM_API_KEY="${GLM_API_KEY:-$OPENAI_API_KEY}"
export JUDGE_MODEL="${JUDGE_MODEL:-openai/glm-5.2}"
export PYTHONUTF8=1

PKG="<work-root>/Task_N_<slug>/<slug>"

harbor run \
  -p "$PKG" \
  -a opencode \
  -m glmproxy/glm-5.2 \
  --ak 'opencode_config={"provider":{"glmproxy":{"npm":"@ai-sdk/openai-compatible","name":"GLM via LiteLLM","options":{"baseURL":"{env:OPENAI_BASE_URL}","apiKey":"{env:OPENAI_API_KEY}"},"models":{"glm-5.2":{"name":"GLM 5.2","options":{"max_tokens":96000}}}}}}' \
  --n-attempts 5 \
  --n-concurrent <N> \
  -r 3 \
  --agent-setup-timeout-multiplier 3 \
  --ae "OPENAI_API_KEY=$GLM_API_KEY" \
  --ae "OPENAI_BASE_URL=$OPENAI_BASE_URL" \
  --ve "OPENAI_API_KEY=$GLM_API_KEY" \
  --ve "OPENAI_BASE_URL=$OPENAI_BASE_URL" \
  --ve "JUDGE_MODEL=$JUDGE_MODEL" \
  -o "<work-root>/jobs-<task>" \
  --job-name "${1:-glm-5x}" \
  -y
```

Non-negotiable: **`max_tokens: 96000`** — without it runs truncate at the reasoning ceiling,
produce no deliverables, and score 0.0 indistinguishably from a hard failure.

**Replace `<N>` with the concurrency you worked out in §1.2 for *this* machine** — never copy
another machine's number. On a 4 GB Docker allowance it is `2`; on 8 GB, `4`–`5`.

### `tools/run_stability_<task>.sh`

Same as the oracle script but `--n-attempts 5 -n 5`. Stability = fresh-container re-grades of
the **frozen gold answer**, not the GLM rollouts.

### `tools/zip_package.py`

```python
"""Zip a task package so the QC platform can read it.

PowerShell's Compress-Archive omits directory entries; the platform walks the archive by
them, fails bundle detection and reports a misleading "upload contains N JSON files".

    python tools/zip_package.py <path-to-package-dir>
"""
import os, sys, zipfile

def build(pkg_dir, out):
    parent = os.path.dirname(os.path.abspath(pkg_dir)) or "."
    name = os.path.basename(os.path.abspath(pkg_dir))
    cwd = os.getcwd(); os.chdir(parent)
    try:
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(name):
                rel = os.path.relpath(root, ".").replace(os.sep, "/")
                dirs[:] = [d for d in dirs if d not in ("__pycache__", ".pytest_cache")]
                z.writestr(zipfile.ZipInfo(rel + "/"), b"")
                for f in sorted(files):
                    z.write(os.path.join(root, f), rel + "/" + f)
        ns = zipfile.ZipFile(out).namelist()
        d = sum(1 for n in ns if n.endswith("/"))
        print(f"{out}: {d} dir-entries, {len(ns)-d} files")
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    pkg = sys.argv[1]
    build(pkg, os.path.abspath(pkg) + "_FINAL.zip")
```

---

# PART 3 — Anatomy of a task package

```
<task-slug>/
  instruction.md          the prompt — where most tasks are won or lost
  task.toml               DO NOT EDIT (name/description/keywords/source_config)
  README.md               change summary + the honest pass-rate section
  environment/
    Dockerfile            edit only to pin the base image digest
    input/                the fixtures — EDITABLE, and hardening lever #2
  solution/
    solve.sh              oracle entrypoint (copies solution/files/ into /app)
    golden_trajectory.json  promoted from a reward-1.0 GLM run
    files/                the gold answer
  tests/
    verifier.json         THE grading spec — NEVER rename
    test_outputs.py       pytest wrapper, one test per verifier
    test.sh               binary: reward 1 only if every verifier passes
    rl_world_verifiers/   vendored engine — do not modify
  evaluations/
    oracle/  glm-5.2/r1..r5/  stability/repeat-01..05/
```

**Hard rules**

- **Never rename `tests/verifier.json` to `manifest.json`.** The platform detects the
  non-connector layout from that filename; renamed, it parses the file as a task-harness
  config → `Verifiers (0)`, no prompt.
- **`task.toml` is not editable.**
- **`environment/input/` IS editable** on these generated tasks. Constraint: stay on the
  original topic and metadata, don't invent a different task, keep it harbor-executable.
- **Pin the Docker base image by digest**:
  `FROM python:3.12-slim-bookworm@sha256:...`
  Get it with `docker buildx imagetools inspect <image> | grep Digest`.
- The vendored engine **rejects a `category` field** on verifiers (`extra_forbidden`).

---

# PART 4 — Build the package from ONE generator

Never hand-edit fixtures, gold and verifiers separately. They drift, and the Oracle dies in a
way that costs hours.

```
tools/<task>_build.py            the data model + the adjudicator — single source of truth
tools/<task>_emit.py             writes environment/input/, solution/files/, tests/verifier.json
tools/<task>_negative_check.py   runs plausible misreadings through the REAL grader
```

The adjudicator computes the gold answer. The emitter derives **both** the fixtures and the
assertions from that same computation. Then gold and grader cannot disagree.

`negative_check` is mandatory, not optional. Enumerate every defensible misreading of the
spec — ignores rule X, reads the threshold as inclusive, follows the named record instead of
the governing one, skips the dedupe — build the answer each one produces, and run it through
the real grader. **Every misreading must lose verifiers (target ≥3 each).** If one scores
1.0, that misreading is a free pass and the task does not discriminate.

---

# PART 5 — The prompt must NOT be a recipe

**The single biggest and most expensive mistake.** A prompt that enumerates the steps measures
instruction-following, not reasoning. GLM executes the checklist and scores 5/5.

Never write anything like:

| leak | what it gives away |
|---|---|
| "say which accounts landed **exactly on that figure**" | that ties exist at all |
| "**Not every row** is in scope" | the excluded/withdrawn rows |
| "the clearances live **outside** the log" | the join |
| "the accounts carry **a rule of their own**" | the second-level rule |
| "`finding_total` (**not** the count of rows carrying one)" | the trap, pre-solved |
| a bulleted list of what the memo must cover | turns the memo into a form to fill in |

**Write instead:** a colleague's request — **~120–220 words**, natural voice, naming the
deliverable filenames and the column layouts. Format specifications are fine; reasoning
disclosures are not.

**Move every definition into the spec document** in `input/` as a numbered section written the
way a real policy or standard writes it — e.g. `§9 What an audit reports`, with a figures
table and a paragraph on what the memo records. Nothing is withheld (so grading stays fair),
but the model must **find and connect** it instead of being handed it.

**Pin output shape in the spec, not the prompt.** If your grader expects one row per item with
codes joined, say so in the spec. Otherwise a model emitting long format (one row per finding)
is defensible and loses on layout — that is an ambiguity, not difficulty, and the QC judge
will name it a `task_defect`.

After writing the prompt, grep it for those trap words. If a hit explains **reasoning** rather
than **format**, delete it.

---

# PART 6 — Writing a rubric that doesn't lie

## Exact-set, never presence-only

Assert every required code present **and** every other code absent:

```
(?im)^(?=[^\n]*\bROW-05\b)(?=[^\n]*\bCODE_A\b)(?=[^\n]*\bCODE_B\b)(?![^\n]*\bCODE_C\b)…
```

Presence-only grading is how mined graders score 13/13 on knowingly wrong answers. Reproduce
that on the original grader and keep it as `evidence_coverage_gap/` — it is the clearest
justification for having replaced the rubric.

## Accept any defensible correct answer

- codes in **any order** in a cell, and **any join character** (`|`, `;`, `,`, space, quoted
  CSV) — grade the set, never the punctuation
- extra or reordered columns, quoted fields
- `none` in any case, plus synonyms
- memo as prose **or** tables

## Proximity checks must be bidirectional and case-insensitive

A memo stating the reason **before** the id is as responsive as one stating it after, and one
opening a sentence with "Withdrawn" is not wrong. A one-directional, case-sensitive check
grades typography and **will** fail correct answers.

## Derive numbers, never hardcode them

If a verifier expects a computed figure, generate every legitimate rendering from the actual
value — the fraction, decimals rounded 2–5 places, percentages rounded 0–3 places. A regex
hardcoded for `0.5` will reject a correct `0.5357`.

## Other rules

- **Free points**: if you cannot describe a plausible attempt that fails a verifier, it is a
  free point.
- **Never grade the model's self-report.** Recompute from the artifact it produced.
- **Never grade a fact the prompt/spec does not ask for.** It is the most common unfair
  hardening and QC flags it.

---

# PART 7 — Hardening: what is measured to work

Measured across ~20 batteries / 100 trials on this workstream.

**The goal is a failure of reasoning, not a failure of typing.** E3 scores 10 points for at
least one run that failed for a *real* reason. A pass rate built on formatting, layout or
notation earns zero there and reads as a task defect — the QC judge reads trajectories and
says so. So design for the model to *get the wrong answer*, never for it to trip over the
rubric.

**Design order.** Do these in sequence, re-running the battery after each: strip the recipe
(Part 5) → add a **feedback rule** → put items on the boundaries the cascade moves → deepen
the reference chains → scale the fixture. Every one of these improves the task. **None of
them has yet moved GLM-5.2 below 4/5 on this family** — see the scoreboard below before you
promise anyone a band.

## Does NOT work
- **Stacking independent rules.** GLM writes one script; ten rules are ten easy checks.
- **Verifier count.** 54 → 5/5. 98 → 5/5. No effect on its own.
- **Coupling alone.** Two-hop joins, derived values, conditional amendments, order-scrambled
  dedupe — all present, still 5/5.
- **Scale alone.** 30 rows → 36 rows: no change. (Scale *with* the couplings below is worth
  having; scale by itself is not.)
- **Removing the recipe alone.** Necessary and correct, but the score did not move — GLM does
  the discovery fine.
- **More memo checks, once the prompt asks for them plainly.** Ask explicitly and GLM writes
  it every time. Ask only implicitly and you are grading unrequested facts, which is unfair.
  Either way the memo is not where difficulty lives.
- **Exact ties on a derived threshold**, when the spec resolves them ("equal does not
  escalate"). That is *easier* than a near miss — the model just applies the stated rule.

## Does work

### 1. The feedback rule — the best design available, but MEASURED AT 5/5

> **Measured result, read this first:** on a 62-request fixture this scored **5/5 across 9
> clean trials**. GLM counted its own findings, saw the trigger fire, applied the widened
> rule, re-derived the threshold and got every downstream flip right. It is written up here
> because it is the soundest *design* in this list and it costs a misreader 14 verifiers —
> not because it is known to break the model. Build it for task quality; do not expect it to
> deliver a band on its own.

Every other rule here is single-pass: read the spec, write one script, done. GLM does that
reliably. The hope was that it would **not** reliably notice that **its own output changes
the rules it must apply**. On this task family, it did.

Add a rule whose **trigger is a figure the audit itself produces**, and whose firing
**changes an earlier rule**. Now a single-pass audit is wrong for a *reasoning* reason, not a
formatting one — which is exactly what the Delivery Gate's **E3** asks for.

Worked example (INT-09 §10):

```
§3 findings ──▶ §10 trigger (§3 total reaches 12) ──▶ §7 widens its scope
                                                            │
                                                            ▼
                                        3 clean requests become flagged
                                                            │
                                                            ▼
                                    batch share 0.5645 ──▶ 0.6129
                                                            │
                                                            ▼
                    three accounts at 0.6000 flip from escalating to not
```

Cost of missing it: **14 verifiers** — 3 row verdicts, 3 account verdicts, and 4 derived
figures. Cost of reading "reaches 12" as "more than 12": the same 14.

**Three conditions make it fair rather than a trap:**

- **It must terminate.** Pick a trigger the changed rule cannot move. Here §10 reads the §3
  total, and §7 can never alter a §3 finding — so the trigger is decided once and cannot
  oscillate. **State that property in the spec** ("the trigger reads the §3 total and nothing
  else; §3 cannot be moved by §7"), so a careful reader knows there is exactly one answer.
  Without it, a reader has to wonder whether to iterate, and that is ambiguity.
- **Nothing is announced in the prompt.** The dependency lives in the spec document and is
  found by reading it. That is the work.
- **Everything is stated.** No withheld data, no guessing.

**Land the trigger on a boundary** (fires at exactly 12 of 12) and let the cascade push
downstream items *just* across a threshold (three accounts ending 0.0129 from the new share).
One rule then produces boundary errors at three different levels.

### 2. Everything else

2. **A derived threshold the model must compute from its own output**, with items sitting
   *close to but not exactly on* it. Exact equality is **easier** if the spec says "equal does
   not count" — the model just applies the stated rule. An awkward fraction (e.g. 35/62) with
   items at 0.6000 forces real arithmetic and a close call with no rule to lean on.
3. **An exception that also creates an obligation**, and an **exception to the exception**
   (an exemption that stops at one category).
4. **A rule that reads the output of an earlier rule** — a rollup whose verdict depends on the
   per-row findings, so upstream slips propagate.
5. **A superseding record that NARROWS terms**, combined with a derived ratio: read the record
   the item names and you clear it; follow the chain and it fails. **Chain it three deep**, so
   a reader who stops at the first successor still has the wrong terms.
6. **Inclusive limits with many rows exactly on the boundary** — one `<=` for `<` floods the
   output.
7. **Scale, once the above are in place** — 28 rows is eyeballable; 60+ rows across 12 groups
   and 18 reference records is not. Scale alone changes nothing, but it multiplies the number
   of independent correct judgements the couplings demand.

### Scoreboard — every lever tried, honestly

| lever | measured |
|---|---|
| stacked independent rules | 5/5 |
| verifier count 54 → 98 → 141 | 5/5 |
| coupling: joins, derived values, amendments, dedupe | 5/5 |
| removing the recipe from the prompt | 5/5 |
| scale 28 → 62 rows, 8 → 12 groups, 3-hop chains | 5/5 |
| awkward derived threshold, items 0.036 from it | 5/5 |
| feedback rule (multi-pass dependency) | 5/5 (9 trials) |

Roughly 100 trials across two tasks. **Every sub-5 number traced to an author's own regex or
an infra flake, never to the model.** Budget your time accordingly: get the task *sound*,
measure honestly, and if it will not come into band, say so — that is a legitimate outcome
and a better deliverable than a number you cannot defend.

## Never
Ambiguity, unreadable phrasing, verifiers for unrequested facts, narrowing to the golden path,
or tuning the verifier count to hit a number. **If a careful analyst could land on two
defensible answers, the task is broken, not hard.**

---

# PART 8 — The method, in order

1. **Cold read.** Read only `instruction.md` and `input/` — **before** opening `tests/`. Write
   down every guess you had to make and every place the prompt leaks the answer. Save as
   `COLD_READ.md`. It is the only unbiased look you get.
2. **Write your own verifier list**, then diff it against `tests/verifier.json`. Note gaps in
   both directions.
3. **Build the generator** (Part 4).
4. **Oracle → exactly 1.0.** Not 0.98. Anything less is a defect, never partial credit.
5. **Negative check** — every misreading loses verifiers.
6. **Battery: 5× GLM**, Git Bash, 5 concurrent.
7. **Read every failing trajectory** and classify each failure:
   **model limitation** (good) · **ambiguity** (fix prompt/spec) · **verifier defect** (fix
   grader) · **infra** (exclude and replace).
8. **Harden** (Part 7) → re-Oracle 1.0 → re-run the battery.
9. **Assemble evidence, README, zip, QC, gates, Drive, tracker.**

### The re-run rule
After any change ask: **did this alter what the model must do, or how it is graded?**
- **No** (README, comments, metadata) → re-run Oracle, keep the battery.
- **Yes** (prompt, spec, assertions, fixtures, gold) → re-run Oracle **and** the battery.

Batteries are ~8 minutes. Don't re-run reflexively — but **never report a battery that
predates the current package**.

---

# PART 9 — Diagnosing a failure (the discipline that matters most)

**A drop in pass rate is a defect in your grader until proven otherwise.** In this workstream,
*every single time* a battery came in below 4/5, the cause was the author's own bug:

| symptom | actual cause |
|---|---|
| 2 runs fail the same memo check | regex required the reason *after* the id |
| 4 runs fail the same 6 rows | those were the multi-code rows; spec never pinned table shape |
| 1 run fails on "not strictly greater" | alternation had `not greater`, not `not \w+ greater` |
| 1 run fails the batch-share check | regex hardcoded `0.5`; the real share was `0.5357` |

**Procedure, every time, before reporting a number:**

1. `grep -E "^FAILED" <trial>/verifier/test-stdout.txt` — which checks, exactly.
2. If several runs fail the **same** checks, suspect the grader, not the model.
3. Read the trajectory. Find what the run actually wrote.
4. Test the regex against 4–5 realistic phrasings that **must pass** and 2 omissions that
   **must fail**.
5. Only if it survives all that is it a real difficulty signal.

**And do not re-roll for luck.** If a failure is not reproducible across batteries, it is a
flake. Running batteries until a favourable one appears and shipping that number is reward
hacking with dice.

Other readings:
- **Bimodal rewards** (0.9, 0.1, 0.9) = a coin-flip on an ambiguity → fix the prompt.
- **Reward exactly 0.0** → check for `exception.txt` / missing `trajectory.json` first.
- `Trials: 0 / Exceptions: N` is **infra**, never a pass rate.

---

# PART 10 — Evidence and packaging

Every run folder needs **`agent/` + `verifier/` + `config.json` + `result.json`**, and
`result.json` must carry `model: "GLM-5.2"`, `overall_pass`, `reward`, `final_answer` and
judge provenance. Write a `tools/assemble_evaluations_<task>.py` that copies trials out of
`jobs-<task>/` into `evaluations/` and fills those fields.

- **`stability/`** is fresh-container re-grades of the **frozen gold answer**
  (`harbor run -a oracle --n-attempts 5`), *not* the GLM rollouts. If you have no real
  stability re-checks, ship none. Never fake it.
- **`solution/golden_trajectory.json`**: harbor's OracleAgent emits no trajectory, so promote
  a **reward-1.0 GLM run's** `agent/trajectory.json`.
- **Do not include** job-level `config.json`, `lock.json`, `job.log`, or the job-root
  `result.json`.
- **Strip** `__pycache__` and `.pytest_cache` before zipping.
- **Delete stale zips** from the folder so the wrong one cannot be uploaded.

## Two cleanup steps the QC platform will otherwise flag

**1. Sanitise leaked paths.** Harbor writes the absolute task path, trials directory and the
proxy endpoint into every `config.json` / `result.json`. Replace them with placeholders
(`<task-path>`, `<openai-base-url>`) before zipping. Verify with a scan for drive letters,
`/Users/`, `ip:port`, `sk-`, and your API key. Graded fields must be untouched.

**2. Expand the CTRF.** `pytest-json-ctrf` collapses a parametrised suite into **one** test
entry, so the platform reports *"non-connector trial payloads carry no per-check verifier
breakdown"* — which is **valid, not a false positive**. Rebuild `verifier_summary.json` and
expand `ctrf.json` from the same run's `test-stdout.txt`, which carries the real
`PASSED|FAILED …::test_deliverable[<name>]` lines. Preserve the plugin's original as
`ctrf_raw.json` and record provenance.

---

# PART 11 — QC, gates and submission

## The QC platform

Sign in with the Turing Google account, paste the GLM key top-right → **Check Key** → wait for
`glm-5.2` ready. **Do not touch the prefilled Base URL.** **One task per ZIP.** ~2–5 minutes,
silent until done.

The report is **advisory**; a human decides. Findings are input; your operator's dispositions
govern. Every "false positive" needs a written justification citing files or the report's own
numbers, and **the operator writes that free text themselves** — pasted AI output gets
rejected. Your job is to supply verified facts, not paste-ready prose.

**Genuine recurring false positives on this layout:**
- *"prompt requirement `input/` has no verifier coverage"* — environment statement, not an ask.
- *"README claims N verifiers but runtime has one native_harbor_verifier"* — one entry
  parametrises into N assertions; both true.

**Not false positives — fix these instead:**
- the CTRF per-check breakdown (Part 10)
- leaked local paths (Part 10)
- a shape/format ambiguity the README itself admits

**`IQC-GATE-*` findings** ("staged model review is partial", "delivery semantic audit
skipped") are about the **tool's own pipeline**, not the package — normally a judge timeout.
Raise `QC_TIMEOUT_SECONDS`/`QC_STAGE_RETRIES` and re-run before dispositioning; if it recurs,
escalate as **infra**. No package change will fix them, so do not keep re-uploading.

## Gates

- **Internal Gate** — advisory. A FAIL here does **not** decide shipping.
- **Delivery Gate** — the scored one. Note **E3 requires at least one run that failed for a
  real reason**. A 5/5 scores 0 on E3 because nothing failed; a 1/5 whose failures are task
  defects also scores 0. Only genuine model failures earn it.

## Deliverables

- Download the **report folder .zip** — that is the deliverable; a lone `results.json` is not.
- Report .zip → the batch's Drive **reports** location.
- Task folder → the **separate** Drive location, **flat, not zipped**.
- Tracker: Modified Task Link · QC Report Link · Golden Trajectory Zip · Status · Date
  submitted · Proof…QC Tool · **Pass Rate (pass@5)** · AHT. There is no score column — put the
  score in **Trainer Notes**, with one line on any known limitation.
- Peer review is **not currently enforced**, but pairing off still catches real problems.

---

# PART 12 — Traps that cost real hours

1. **Never edit the package while a battery runs.** Harbor rebuilds the image per trial; the
   run silently spans two versions. Check `result.json → task_checksum` — **all five trials
   must share one checksum**, or the measurement is void.
2. **A pass rate from another machine is not evidence about yours.** Check `result.json` for a
   foreign path or a different `model_name`. A shipped "2/5" re-ran as 4/5 on a new machine.
3. **Zip with the script**, never `Compress-Archive`.
4. `all predefined address pools have been fully subnetted` → `docker network prune -f`. After
   a killed job, `docker ps -a --filter status=exited` → `docker rm` the dead
   `gen-*__env-main-1` containers first, then prune.
5. `AgentSetupTimeoutError` → `--agent-setup-timeout-multiplier 3` (already in the script).
6. **Dead fixture columns.** If the input carries fields no rule uses, decide deliberately:
   write the rule they were shaped for, or leave them as realistic noise — and tell the
   operator, because authoring a rule the mining team didn't write is their call to disclose.
7. Every judged/rubric verifier scoring 0 → `JUDGE_MODEL` was not set.
8. Output truncating mid-reasoning, deliverables missing → `max_tokens` not set to 96000.

---

# PART 13 — How to report

- Report **all five** individual rewards, never just the mean.
- State the pass rate as measured on the **exact shipping package** (checksums matched).
- **Give the reasons for each failure before giving the number.** A number without diagnosed
  reasons is not a measurement.
- If the band was reached on something other than reasoning — a formatting rule, a layout
  convention, a flake — **say so plainly and fix it**, don't bank it.
- If you got something wrong earlier, correct it in one line and move on.
- If the task cannot be brought into band fairly: **mark it too easy, keep the row**, and say
  why in the README. That is a legitimate, documented outcome.

**The operator makes the decisions.** Bring them verified facts, a recommendation, and the
trade-offs — then do what they decide.

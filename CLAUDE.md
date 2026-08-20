# Turing ComputerBench NonConnector — task runbook

Read this before touching a task. It is the hard-won version; the circulated Task Playbook is
written for **CompanyBench** and several of its instructions are wrong for this workstream.

## The job in one paragraph

Turing builds an evaluation benchmark for an AI lab. Tasks are auto-generated (`shannon-200`),
arrive **too easy**, and usually have broken graders. Your job is to make one task fair, hard and
correctly graded, then report an honest pass rate. You are a question editor and examiner, not a
developer.

**Expect the first battery to be 5/5. That is normal, not a failure.** Hardening is the job.

## Bands and outcomes

| | |
|---|---|
| Band (ComputerBench) | **at most 3 of 5 runs may fully pass (≤3/5)** |
| 0/5 with steady partial rewards | good — "what good looks like" |
| Cannot get it in band | mark **too easy**, **keep the row** (never drop it) |
| Oracle | must be exactly **1.0**, every time, before any battery |

The ≤3/5 rule overrides the 1/5–2/5 band in the older playbook (that still applies to CompanyBench).

## Ten gotchas that will cost you hours

1. **Zip with `tools/zip_package.py`, never `Compress-Archive`.** PowerShell omits directory
   entries; the QC platform walks the archive by them, fails bundle detection, and reports a
   misleading *"upload contains N JSON files"*. Windows Explorer right-click also works.
2. **Never rename `tests/verifier.json` to `manifest.json`.** The platform detects the
   non-connector layout from that filename. Renamed, it parses the file as a standalone
   task-harness config → `Verifiers (0)`, no prompt. The onboarding doc's "rewrite to
   manifest.json" packaging step does not work here.
3. **Run batteries from Git Bash, never PowerShell.** PS 5.1 strips the inner quotes from
   `--ak "opencode_config={...}"`; harbor parses it as a string and dies with
   `AttributeError: 'str' object has no attribute 'items'`. The job reports **0 trials /
   5 exceptions**, which looks exactly like a 0/5 pass rate but is a crash.
4. **Set `max_tokens: 96000`** in the opencode model config. Without it runs truncate at the
   reasoning ceiling (`"reason":"length"`, zero output, no deliverables) and score 0.0 —
   indistinguishable from a hard failure unless you read the trajectory. Already in
   `tools/run_battery.sh`.
5. **Pin the Docker base image by digest.** `FROM python:3.12-slim-bookworm@sha256:...`
   Delivery Gate **S1** deducts a point for an unpinned base and that deduction is *blocking*
   (disqualifies the whole run). Get the digest with
   `docker buildx imagetools inspect <image> | grep Digest`.
6. **`Trials: 0 / Exceptions: N` is infra, not a pass rate.** Never report it. `Trials: 5 /
   Mean: 0.000` is a real 0/5.
7. **The `rl_world_verifiers` engine rejects a `category` field** on verifiers
   (`extra_forbidden`). The "delete `category: secondary`" step does not apply.
8. **Harbor's `OracleAgent` emits no trajectory** — only `agent/oracle.txt`. For
   `solution/golden_trajectory.json`, **promote a reward-1.0 GLM run's `agent/trajectory.json`**.
9. **Strip `__pycache__` / `.pytest_cache`** before zipping. They regenerate every time you run
   pytest locally.
10. **`environment/input/` IS editable** on these gen tasks (confirmed by Vahid, delivery
    manager). The playbook's "seed data is not editable" is a CompanyBench rule about the shared
    base image. Constraint: **stay on the original topic and metadata, don't build a new task**,
    and keep it harbor-executable.

## Package layout (non-connector)

    <task-slug>/
      instruction.md          the prompt; most of your work
      task.toml               DO NOT EDIT (name/description/keywords/source_config)
      README.md               cumulative change summary — Ship S2 scores it
      environment/
        Dockerfile            editable only to pin the digest
        input/                the fixtures — editable, this is hardening lever #2
      solution/
        solve.sh              oracle entrypoint
        golden_trajectory.json  promote from a passing run
        files/                the gold answer
      tests/
        verifier.json         THE grading spec — never rename
        test_outputs.py       pytest wrapper, one test per verifier
        test.sh               binary: reward 1 only if every verifier passes
        rl_world_verifiers/   vendored engine
      evaluations/
        oracle/               agent/ verifier/ config.json result.json
        glm-5.2/r1..r5/       same layout, + agent/trajectory.json
        stability/repeat-01..05/

Every run folder needs **agent/ + verifier/ + config.json + result.json**. `result.json` must
carry `model: "GLM-5.2"`, `overall_pass`, `final_answer`, `reward`. `tools/assemble_evaluations.py`
builds all of this and generates `verifier_summary.json` from CTRF.

## Workflow

1. **Cold read.** Read only `instruction.md` and `environment/input/`. Write down every guess you
   had to make and every place the prompt or the input leaks the answer. Do this before opening
   `tests/` — it is the only unbiased look you get.
2. **Write your own verifier list**, then compare to `tests/verifier.json`. Note coverage gaps and
   unfair checks in both directions.
3. **Oracle → must be exactly 1.0.**
4. **5× GLM battery** (Git Bash, `tools/run_battery.sh`).
5. **Read every failing trajectory.** Classify: model limitation (good) / ambiguity (fix the
   prompt) / verifier defect (fix the grader) / infra (exclude and replace).
6. **Harden** — see below. Re-Oracle to 1.0, re-run the battery.
7. **Assemble evidence**, write README, zip.
8. **Gate 1 Review → Gate 2 Finalize → Gate 3 Ship/Delivery.**
9. **Drive + tracker + channel post + peer review.**

### The re-run rule, applied properly

After a change ask: **did this alter what the model must do, or how it is graded?**
- **No** (metadata strings, comments, README, gold memo wording) → re-run Oracle, keep the battery.
- **Yes** (prompt, assertions, fixtures, gold values) → re-run Oracle *and* the battery.

Do not re-run reflexively. Batteries are ~11 minutes each.

## Hardening: what works

**Stacking independent rules does NOT work.** GLM writes a Python script per rule and handles ten
independent rules as ten easy checks. Verified across four batteries on g780.

What works is **coupled reasoning** — correctness depending on interactions:

- **Chained derivation** — a threshold that must itself be derived from the data, then used as a
  filter. (g780: derive the required protected-class list from the standard + its amendments,
  then test every notice against it.)
- **Cross-source synthesis** — the rule in one file, the data in another, the exception in a third.
- **State across steps** — an exclusion discovered late invalidating earlier work.
- **Data-shape sabotage** — near-miss rows a per-rule script misclassifies.
- **Scale** — the doc's own example task has **30 items and 3–4 sources**. 7 items and 2 sources
  will never be hard. Error probability compounds across rows.

Also legitimate: remove leakage from the prompt, remove the recipe, tighten grading to the
artifact rather than the model's self-report.

**Never**: ambiguity, unreadable phrasing, verifiers for things the prompt never asked, narrowing
to the golden path, or changing the verifier count to hit a number. If a careful analyst could
land on two defensible answers, the task is broken, not hard.

### Coupling is necessary but NOT sufficient — the g774 controlled comparison

Two hardenings of the **same** task (g774), same model, same harness, run back to back:

| | shipped version → **2/5** | second attempt → **5/5** |
|---|---|---|
| per-press / per-stock thresholds | 3 of 7 rules | **4 of 5 rules** |
| derived measured value | effective DPI | effective DPI |
| exception that also creates an obligation | yes | yes |
| conditional amendment (rule × binding) | — | **yes** |
| dedupe / supersession, row order scrambled | — | **yes** |
| element minimum | **handed over on the row** | derived from type × binding |
| pages | 36 | 30 |
| finding codes | 7 | 5 |
| deliverables | **4 (two CSVs)** | 3 (one CSV) |
| **verifiers** | **98** | 54 |
|   · per-page verdict | 36 | 30 |
|   · **per-section rollup** | **28** | **0** |
|   · results.json figures | 14 | 11 |
|   · **memo content** | **14** | 7 |

The 5/5 version was **strictly more coupled** and still passed every run. GLM reads the standard
once, writes one script, and joins/dedupes/derivations are free to a script. Coupling buys much
less than the playbook implies.

**What actually moved the pass rate was graded surface area.** Reward is binary, so the pass rate
is P(every check right). The two gaps were:

1. **A second aggregate deliverable.** A per-section (or per-group) rollup CSV with its own rule
   is worth ~28 verifiers and forces a second correct artifact. Make the rollup's rule depend on
   the page-level verdicts — e.g. pages carrying a given finding are held back and the section
   still has to impose — so an upstream slip propagates instead of staying local.
2. **Grade the memo hard — this is the cheapest honest lever.** The CSV and the JSON are script
   output and the model gets them right or wrong as a block; the **memo is hand-written prose**,
   so every required fact is an independent chance to omit something. Aim for ~14 memo verifiers,
   each demanding one specific stated fact:
   `memo_covers_every_flagged_page`, `memo_covers_every_section`, `memo_names_both_presses`,
   `memo_cites_both_dpi_floors`, `memo_cites_ink_cap_and_measurement`, `memo_cites_margin_floor`,
   `memo_cites_bleed_minimum`, `memo_explains_margin_exemption`, `memo_explains_bleed_obligation`,
   `memo_explains_scaled_resolution`, `memo_explains_press_dependent_pass`,
   `memo_names_unimposable_sections`, `memo_states_element_shortfall_total`,
   `memo_reports_clean_page_total`.

**Rule of thumb: budget ~100 verifiers.** 54 was 5/5; 98 was 2/5. Not denominator gaming —
every one of the 98 is a fact the prompt actually asked for, and the prompt has to ask for
enough to carry them. If you cannot reach ~100 honest checks, the task is asking for too
little, and *that* is what to fix.

**Per-page verdicts must be exact-set, not presence-only.** Assert every required code present
**and** every other code absent. The mined g774 grader asserted presence only on 4 of 6 pages and
scored **14/14 on an answer with four false positives, including a clean page flagged twice**
(`Task_4_.../evidence_negative_check/` reproduces it in one command).

## Gates

- **Internal Gate** — advisory. Does **not** decide shipping. A FAIL here is not fatal.
- **Delivery Gate** — decides. Scored /100, pass mark 95. Four items are blocking.

**A 5/5 task caps at 90/100.** E3 is worth 10 and requires at least one run that failed for a real
reason. That is the gate agreeing with the "too easy" call — not something you can fix by editing.

Findings are **advisory input**; you are the judge and your dispositions govern. Every "false
positive" needs written justification citing files or the report's own numbers. Write the
free-text yourself — pasted LLM output gets rejected.

Recurring false positives on this layout:
- *"Prompt requirement `input/` has no verifier coverage"* — environment statement, not an ask.
- *"No five-repeat stability evidence"* / *"non-connector trials carry no per-check breakdown"* —
  the report usually admits the tool cannot map non-connector trials.
- *"README claims N verifiers but runtime has one native_harbor_verifier"* — one entry
  parametrises into N assertions. Both true.

## Tracker columns (this sheet)

Batch · Task ID · Dataset Task Name · Task Link *(leave)* · **Modified Task Link** · **QC Report
Link** · Golden Trajectory Zip File · Trainer · **Status** · Date Started · Date submitted ·
**Proof … QC Tool** · **Trainer Notes** · **Pass Rate (pass@5)** · Trainer AHT (hrs)

There is no "Ship QC Gate Score" column — put the score in Trainer Notes. Task folder and QC
reports go to **separate** Drive locations; the folder goes up **flat, not zipped**.

**A completed task without a matching completed peer review is not eligible for payment.** That is
the only explicit payment condition in the playbook.

## Tools in this repo

    tools/run_battery.sh            5× GLM battery, Git Bash, max_tokens set
    tools/assemble_evaluations.py   builds evaluations/ with all required fields
    tools/zip_package.py            zips with directory entries the QC platform needs

Edit the job names and package path at the top of each before use.

## Reference

- QC platform: https://qc-api-713053229214.us-central1.run.app/
- Env: `.env` at this root — `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `JUDGE_MODEL=openai/glm-5.2`
- `harbor` lives at `C:\Users\Predator 16\.local\bin` (on PATH; new terminal after any install)
- gcloud is **not** needed — these tasks use a public base image
- Never run `docker image prune -a` — it deletes the 50 GB CompanyBench base image

## Worked example

`Task_1_gen-g780-realestate-fairhousing-collateral-audit/` is a complete run of this process:
`COLD_READ.md`, `CHANGES.md`, `SUBMIT.md`, `GUIDANCE.md`, `evidence_coverage_gap/` (a reproduction
of the original grader scoring 14/14 on a knowingly wrong answer), and `ORIGINAL_BACKUP/` for
diffing. Outcome: Delivery Gate 90/100, 0 blocking, pass rate 5/5, marked too easy.

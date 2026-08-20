# gen-g789-dissertation-formatting-spec-audit

A thesis office runs a formatting pre-check on a dissertation before it goes for binding. The
agent has to work out what the formatting specification actually requires of *this*
submission — the base standard as amended, at the submission date — and then audit every
section against it, producing a per-section CSV, a memo and a small set of derived counts.

Topic, `task.toml` name, description and keywords are unchanged from the generated task.

## What changed, and why

The generated task was three independent single-column comparisons over 6 rows and 2 files,
with a single carve-out that both the prompt and the specification announced in words. It
measured `<BASELINE>` on GLM-5.2 against a band of at most 3 of 5, and its grader scored
**14/14 on an answer wrong on 3 of its 6 rows** — including the carve-out the task exists to
test.

Three things were done about it.

### 1. The prompt no longer contains the answer

Removed *"remembering that landscape data annexes follow a different margin rule than the rest
of the document"* and *"the annex the specification clears"* from `instruction.md`, and
*"Flagging a landscape annex for its narrower margin is the commonest false positive"* from
the specification. The rules themselves are all still stated, in the sources where an auditor
would expect to find them.

In their place the prompt now pins the things that were undefined and graded anyway: the
audit's two-column schema, the multi-finding join order, and what each of the five counts
counts. The memo is specified as five numbered items, so it can be graded against the ask
rather than against a guess.

### 2. The fixtures demand coupled reasoning

`environment/input/` goes from 2 files and 6 sections to **4 files and 30 sections** (35 log
rows). Stacking more independent rules does not make this kind of task harder — a model
writes one script per rule and handles ten rules as ten easy checks. What the sources now
require is reasoning where each step depends on the last:

| # | Mechanism | Rows that turn on it |
|---|---|---|
| 1 | **Effective-spec derivation.** A-4 is effective 2026-07-01, after the 2026-03-09 submission, so it is not in force. | 8 body sections invert |
| 2 | **A superseded amendment that is still in date.** A-1 (2.8 cm binding edge) is superseded in full by A-2 (3.0 cm). | `SEC-ABSTRACT`, `SEC-ACK`, `SEC-GLOSSARY` |
| 3 | **A derived threshold used as a filter.** A-3 limits the annex exception to annexes whose widest table exceeds the printable width of a landscape page — 29.7 − 3.0 − 2.5 = **24.2 cm**, a figure that depends on mechanism 2. | `SEC-AN-04` (24.3), `SEC-AN-10` (24.6) |
| 4 | **A rule that survives the exception.** The binding edge is outside every exception. | `SEC-AN-07` — exempt, and still flagged |
| 5 | **Cross-rule coupling.** A-5 fixes compliant exact leading at 18.0 pt: 1.5 × the *required* 12.0 pt, not 1.5 × whatever the section uses. Rules 2 and 3 can no longer be evaluated in separate passes. | `SEC-CH4` (11.0 pt at 16.5 pt) |
| 6 | **A denominator that moves.** The log is an unsorted export carrying every revision; only the highest revision of each `section_id` is audited. 30 sections, 35 rows. Two sections list the current revision first and three list the superseded one first, so neither "first row wins" nor "last row wins" survives. | `SEC-CH1`, `SEC-CH3`, `SEC-CH5`, `SEC-AN-05`, `SEC-AN-07` |
| 7 | **Per-section waivers with expiry.** W-1 is in force, W-2 expired before submission, W-3 is in force but scoped to a rule its section does not breach. | `SEC-AN-01`, `SEC-AN-03`, `SEC-LOF` |

Every one of these is stated plainly in the sources. None of them admits two defensible
answers; the difficulty is that they interact. Six plausible single-mistake readings were
scored against the gold answer, and each gets between 1 and 8 of the 30 rows wrong:

    applies the superseded A-1                            4 rows wrong
    applies the not-yet-effective A-4                     8 rows wrong
    applies no binding-edge amendment at all              6 rows wrong
    exact leading judged against the section's own size   1 row  wrong
    ignores revision numbers, takes the first row         3 rows wrong
    honours the expired waiver W-2                        1 row  wrong

Near-miss data throughout: 2.49 vs 2.50 cm, 12.5 vs 12.0 pt, `TimesNewRomanPSMT` (accepted)
against `Nimbus Roman No9 L` and `Liberation Serif` (metric substitutes, not accepted), a
landscape *body* section with a genuinely oversized table, and a *portrait* annex.

### 3. The grader grades the artifact

`tests/verifier.json` goes from 14 verifiers to **65**, all deterministic, generated from the
gold deliverables so the two cannot drift apart.

- **One end-anchored row check per audited section**, all 30. The shipped grader had no check
  at all for two of its six rows, and its row checks scanned the whole row for a substring —
  which is how a wrong answer scored 14/14. Reproduction in `../evidence_coverage_gap/`.
- **A negative guard on each of the twelve compliant sections**: no line of the audit may
  carry a violation label against them.
- **A header check** pinning the audit to `section_id,finding`, which rejects the
  echo-the-input-log shortcut a baseline trial took.
- **Fourteen single-purpose memo checks**, one per numbered requirement of the ask. The
  shipped `memo_margin` was `(?i)\bwrong margin|\bline spacing` — alternation binds loosest,
  so either term alone passed it, and the font finding had no memo coverage at all.

**Known limitation, stated rather than hidden:** the engine's `csv` source exposes only
`extract_text`, so the five counts in `results.json` cannot be *recomputed* from the delivered
CSV inside the verifier DSL — they are still compared to constants. With all 30 rows pinned
cell-for-cell, a CSV that contradicts `results.json` now fails the row checks instead.

### 4. Packaging

`environment/Dockerfile` pins its base image by digest
(`python:3.12-slim-bookworm@sha256:a116514e…`). Nothing else in it changed.

## Ground truth

30 sections audited, 5 log rows set aside as superseded. 18 sections flagged: 10 margin,
6 font, 5 spacing. Two sections breach more than one rule.

## Measurements

| | |
|---|---|
| Oracle | **1.0**, 65/65 (`oracle-hardened-v1`) |
| Baseline pass rate, GLM-5.2 ×5 | `<BASELINE>` (`glm-5x-baseline-original`) |
| Hardened pass rate, GLM-5.2 ×5 | `<HARDENED>` (`glm-5x-hardened-v1`) |
| Shipped grader vs. a knowingly wrong answer | 14/14 pass — see `../evidence_coverage_gap/` |

## Layout

    instruction.md          the ask
    task.toml               unchanged
    environment/
      Dockerfile            base image pinned by digest
      input/                dissertation_formatting_spec.md, dfs11_amendments.md,
                            thesis_office_record.md, dissertation_section_log.csv
    solution/
      solve.sh              installs the gold deliverables
      files/                formatting_audit.csv, formatting_memo.md, results.json
    tests/
      verifier.json         65 deterministic verifiers
      test_outputs.py       one pytest per verifier
      test.sh               reward 1 only if every verifier passes
      rl_world_verifiers/   vendored engine, unmodified
    evaluations/            oracle and GLM-5.2 run evidence

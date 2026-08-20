# Changes made to gen-g789-dissertation-formatting-spec-audit

Original preserved at `ORIGINAL_BACKUP/` for diffing.
Editable surface used: `instruction.md`, `environment/input/`, `environment/Dockerfile`
(digest pin only), `tests/verifier.json`, `solution/files/`, `README.md` (new).
`task.toml` untouched. The task's topic, name, description and keywords are unchanged: it is
still a section-level dissertation formatting audit against DFS-11.

`environment/input/` is editable on these gen tasks — confirmed by Vahid (delivery manager),
with the constraint that the task stays on its original topic and metadata and remains
harbor-executable. See `GUIDANCE.md`.

## Why the task was changed

The shipped task is three independent single-column comparisons over **6 rows and 2 files**,
with one carve-out that both the prompt *and* the specification announce in words. See
`COLD_READ.md` for the four leakage sites and the six grader gaps.

Two measurements drove the rewrite:

1. **Baseline pass rate on GLM-5.2: 5/5** (job `glm-5x-baseline-original` — 5 trials,
   0 exceptions, mean reward 1.000), against a band of at most 3 of 5.
2. **The shipped grader scores 14/14 on an answer that is wrong on 3 of its 6 rows**,
   including the annex trap the whole task is built around. Reproduction in
   `evidence_coverage_gap/`. A live baseline trial hit the same defect from the other side:
   it flagged the annex `MARGIN_NONCOMPLIANT` and `annex_trap_clean` passed anyway, because
   the row's other columns contained the word "none".

Hardening the ask and the grader alone was tried on the previous task in this batch (g780,
ten batteries, 5/5 throughout) and does not move a task of this shape. Per the runbook,
stacking more independent rules does not work either — GLM writes one script per rule. What
the fixtures now demand is **coupled** reasoning.

## `environment/input/` — 2 files → 4, 6 sections → 30

| File | Status | What it carries |
|---|---|---|
| `dissertation_formatting_spec.md` | rewritten | DFS-11 base text: Rules 1–3, per-side margins, the accepted-font list (Appendix F), the scope rule that only the highest revision of a `section_id` is audited, page geometry, and the definition of printable width. |
| `dfs11_amendments.md` | **new** | A-1…A-5, each with its own effective date. |
| `thesis_office_record.md` | **new** | The submission record for TO-2026-0447: date of submission 2026-03-09, binding, and three standing waivers with expiry dates. |
| `dissertation_section_log.csv` | rewritten | 35 rows covering 30 sections, 13 columns. |

### The seven mechanisms that couple the rules

Each one is stated plainly in the sources — none of this is hidden, and none of it admits two
defensible answers. The difficulty is that they interact, so a per-rule script gets them wrong.

1. **Effective-spec derivation.** A-4 is effective 2026-07-01, *after* the 2026-03-09
   submission, so it is not in force. Applying it inverts the spacing verdict on every body
   section — `SEC-CH5` and `SEC-CH6` are a matched pair that swap clean/dirty under it.
2. **A superseded amendment that is still in date.** A-1 (2.8 cm binding edge) is effective
   before the submission but superseded in full by A-2 (3.0 cm). `SEC-ABSTRACT` (2.9),
   `SEC-ACK` (2.85) and `SEC-GLOSSARY` (2.80) are compliant under A-1 and flagged under A-2.
3. **A derived threshold used as a filter.** A-3 limits the annex exception to annexes whose
   widest table exceeds the *printable width of a landscape page*, which the auditor must
   compute: 29.7 − 3.0 − 2.5 = **24.2 cm**. It depends on step 2. `SEC-AN-04` (24.3 cm) is
   exempt on the true threshold, flagged on the A-1 threshold of 24.4; `SEC-AN-10` (24.6 cm)
   is exempt on the true threshold, flagged if no binding-edge amendment is applied at all
   (24.7).
4. **A rule that survives the exception.** A-3 puts the binding edge outside every exception.
   `SEC-AN-07` qualifies for the exception, has its top/bottom/outer margins cleared by it,
   and is still `MARGIN_NONCOMPLIANT` on a 2.6 cm inner margin.
5. **Cross-rule coupling in the spacing test.** A-5 fixes compliant exact leading at 18.0 pt —
   1.5 × the *required* 12.0 pt, not 1.5 × whatever the section uses. `SEC-CH4` is 11.0 pt at
   16.5 pt leading: 1.5 × its own size, and wrong on both rules. Rule 2 and Rule 3 can no
   longer be evaluated in separate passes.
6. **A denominator that moves.** The log is an unsorted export carrying every revision. Five
   rows are superseded; 30 sections are audited, not 35. `SEC-CH1` and `SEC-AN-07` list the
   current revision *above* the superseded one; `SEC-CH3`, `SEC-CH5` and `SEC-AN-05` list the
   superseded one first. Neither "first row wins" nor "last row wins" survives that. `SEC-CH1`
   rev 1 is set in Arial and `SEC-CH3` rev 1 is compliant, so getting this wrong flags a clean
   section and clears a dirty one.
7. **Per-section waivers with expiry.** W-1 (`SEC-AN-01`) is in force; W-2 (`SEC-AN-03`)
   expired 2026-01-31 and clears nothing; W-3 (`SEC-LOF`) is in force but scoped to a rule
   that section does not breach.

Near-miss rows throughout: 2.49 vs 2.50 cm, 12.5 vs 12.0 pt, `TimesNewRomanPSMT` (accepted)
vs `Nimbus Roman No9 L` and `Liberation Serif` (metric substitutes, not accepted), a landscape
body section with a genuinely oversized table that is not an annex (`SEC-CH7`), and a portrait
annex (`SEC-AN-06`).

### Each mechanism is load-bearing

Six plausible single-mistake readings of the effective specification were scored against the
gold answer. Each is a perfect audit apart from one wrong step, and each still gets rows wrong
— so none of the seven mechanisms is decoration:

| Wrong reading | Rows wrong / 30 | Which |
|---|---|---|
| Applies the superseded A-1 (inner 2.8, threshold 24.4) | 4 | `SEC-ABSTRACT`, `SEC-ACK`, `SEC-AN-04`, `SEC-GLOSSARY` |
| Applies the not-yet-effective A-4 (body double-spaced) | 8 | eight body sections |
| Applies no binding-edge amendment at all (inner 2.5, threshold 24.7) | 6 | `SEC-ABSTRACT`, `SEC-ACK`, `SEC-AN-04`, `SEC-AN-07`, `SEC-AN-10`, `SEC-GLOSSARY` |
| Judges exact leading against the section's own font size | 1 | `SEC-CH4` |
| Ignores revision numbers, takes the first row per `section_id` | 3 | `SEC-AN-05`, `SEC-CH3`, `SEC-CH5` |
| Honours the expired waiver W-2 | 1 | `SEC-AN-03` |

Reward is binary — `tests/test.sh` writes 1 only if all 65 verifiers pass — so one wrong row
is a failed trial.

Ground truth: 30 sections, 18 flagged, 10 margin, 6 font, 5 spacing.

## `instruction.md`

| Change | Type | Rationale |
|---|---|---|
| Removed *"remembering that landscape data annexes follow a different margin rule than the rest of the document, though font and spacing still apply everywhere"* | de-leak | The prompt pre-solved the only piece of reasoning in the task. The rule is still stated in the specification, where it belongs. |
| Removed *"and the annex the specification clears"* | de-leak | Announced both that there is one annex and that its verdict is `none`. |
| Pinned the audit to **exactly two columns**, with an in-world reason (the office's importer) | harden | A baseline trial echoed the input log with four extra columns appended. It also removes the third column a wrong answer used to hide the word "none" in. |
| Defined the **multi-finding join** — `\|`, no spaces, margin → font → spacing | ambiguity fix | `finding` was singular and no row exercised a second breach; the output contract was incomplete. Two rows now breach more than one rule. |
| **Defined all five counts** as counts of *sections*, and said a two-rule section counts once in each | ambiguity fix | The counts were graded but never defined. |
| Specified the memo's contents as five numbered items | gradeability | The memo was ungradeable prose. Every memo verifier now maps to one numbered item of the ask. |
| Rewrote the framing as a thesis-office pre-check on a named submission | realism | Also motivates why the submission record is in scope. |

Nothing in the prompt states which amendments are in force, what the derived threshold is, or
that any log rows are superseded. Those are the task.

## `environment/input/dissertation_formatting_spec.md` — de-leaked

Removed: *"Flagging a landscape annex for its narrower margin is the commonest false
positive."* That sentence is the answer key in prose and is why the trap had no teeth.

## `tests/verifier.json` — 14 verifiers → 65

All deterministic. No judged checks. Generated from the gold deliverables so the spec and the
gold cannot drift apart.

| Gap in the shipped grader | Fix |
|---|---|
| `SEC-COVER` and `SEC-CH1` had **no verifier at all** | One row check per audited section — all 30. |
| Row checks scanned the whole row (`^SEC\-CH2\s*,.*MARGIN_NONCOMPLIANT`) | End-anchored: `(?mi)^SEC\-X\s*,\s*FINDING\s*$`. The `finding` cell is pinned end to end. |
| `annex_trap_clean` defeatable by the word "none" appearing anywhere on the row | The twelve compliant sections each carry a `not_regex_match` guard: no line may carry a violation label against them. |
| No schema check — the input log could be echoed back | `audit_header_is_two_columns` pins the header to `section_id,finding`. |
| `memo_margin` was `(?i)\bwrong margin\|\bline spacing` — alternation binds loosest, so one term alone passed; the font finding had no memo coverage | Fourteen single-purpose memo checks, one per numbered requirement: amendment dispositions (A-1, A-4), the three derived figures, the audited/set-aside counts, five named flagged sections with the measured value responsible, and the two sections the Rule 1 exception does not reach. |
| Counts compared to constants and never reconciled with the CSV | Still constants — the engine's `csv` source exposes only `extract_text`, so the DSL cannot recompute them. With all 30 rows pinned cell-for-cell, a CSV contradicting `results.json` now fails the row checks instead. Stated rather than hidden. |

## `solution/files/` — regenerated

`formatting_audit.csv`, `results.json` and `formatting_memo.md` all rebuilt for the new
fixtures. The audit and the counts are produced by an independent implementation of the
effective specification, not hand-transcribed; the memo is written to the five numbered
requirements.

## `environment/Dockerfile`

Base image pinned by digest —
`FROM python:3.12-slim-bookworm@sha256:a116514e19457bcb7af7efe9c3dd0b9b71e85b317694e7882a1c52aa15a78134`
— for Delivery Gate S1. No other change.

## Verification

- Gold answer: **65/65 pass**, Oracle `oracle-hardened-v1`, reward **1.0**.
- Shipped grader vs. a knowingly wrong answer: **14/14 pass** (`evidence_coverage_gap/`).
- Baseline pass rate: **5/5** (`glm-5x-baseline-original`, 5 trials, 0 exceptions, mean 1.000).
- Hardened pass rate: `<HARDENED>` (`glm-5x-hardened-v1`).

## The v1 battery, and the grader defect it exposed

`glm-5x-hardened-v1` returned **3/5** (5 trials, 0 exceptions, mean 0.600). That is inside the
band, and reporting it would have been wrong.

Reading the two failures: **neither failed on the audit.** All five runs got all 30 row
verdicts and all five counts right. The two failing trials failed on exactly two checks each —
`memo_ch4_leading` and `memo_ch8_margin` — each written as a line anchor requiring the
section id and its measured value on the *same line*. Both runs had named the section, its
findings and the measured value; they had wrapped the sentence. The verifier was grading line
breaks, not content.

Fixed: every memo check that pairs an identifier with a value is now a bounded-window
`(?is)SEC\-CH4.{0,400}?16\.5` instead of a line anchor. Ten checks changed; the content
each one requires is unchanged.

Replaying the two failing runs' own memos against the corrected checks: **both now pass all 15
memo verifiers.** So the honest pass rate of the hardened task is 5/5, and `glm-5x-hardened-v2`
was run against the corrected grader to measure it rather than infer it.

## Outcome

`<OUTCOME>`

## Discarded run, on the record

`jobs-g789/glm-5x-baseline-g789` was discarded and is not reported. Harbor rebuilds the task
image **per trial**, so fixture edits made while that job was in flight reached two of its
five trials, which then ran the new fixtures against the old 14-verifier grader. The clean
baseline was re-measured against `ORIGINAL_BACKUP/` with the package frozen.

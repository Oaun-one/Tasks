# Cold read — gen-g789-dissertation-formatting-spec-audit

Done before opening `tests/`. Sources read: `instruction.md`, `environment/input/` only.

## What the task asks

Audit 6 dissertation sections against DFS-11 (margins / font / line spacing), emit
`formatting_audit.csv` (one row per section + `finding`), `formatting_memo.md`, and
`results.json` with five counts.

## Leakage found (the prompt and the spec both hand over the answer)

| # | Where | Text | Effect |
|---|---|---|---|
| L1 | `instruction.md` | *"remembering that landscape data annexes follow a different margin rule than the rest of the document, though font and spacing still apply everywhere"* | States the entire exception structure. The one piece of reasoning in the task is pre-solved in the ask. |
| L2 | `instruction.md` | *"and the annex the specification clears"* | Announces there is exactly one annex and that its verdict is `none`. |
| L3 | `dissertation_formatting_spec.md` §1 | *"Flagging a landscape annex for its narrower margin is the commonest false positive."* | The answer key in prose. This is the only trap in the task and the spec warns about it by name. |
| L4 | fixture shape | Log has exactly one violation of each type, in order (CH2 margin, CH3 font, CH4 spacing) | The counts (1/1/1) are guessable from the shape without auditing. |

## Guesses I had to make (ambiguities)

| # | Question | Why it is unresolved |
|---|---|---|
| A1 | What if a section violates **two** rules? | `finding` is singular, no precedence and no join convention is defined. No row exercises it, so it never surfaces — but the output contract is incomplete. |
| A2 | What makes an annex a **landscape** annex? | The spec's exemption is for *landscape* data annexes. The log has no orientation column; `section_type=annex` is the only signal. The reader must assume annex ⇒ landscape. |
| A3 | Are the five `results.json` counts counts of sections or of labels? | Undefined in the prompt. Identical here because no row carries two findings. |
| A4 | Is `SEC-COVER` (a cover page) in scope at all? | Prompt says "each section"; the log lists it. Assumed in scope. |

## Difficulty read

Three independent single-column comparisons over **6 rows and 2 files**, with one carve-out
that both the prompt and the spec announce. A per-rule script solves it; there is nothing that
couples the rules to each other. The runbook's own worked example is 30 items over 3–4 sources.
Predicted baseline: 5/5.

## My verifier list, written before reading `tests/verifier.json`

1. `formatting_audit.csv` exists, and has exactly the agreed columns
2. Row-level verdict pinned for **all six** sections (COVER, CH1, CH2, CH3, CH4, ANNEX-A) — including the two `none` rows
3. `SEC-ANNEX-A` carries no violation label anywhere on its row (end-anchored, not "contains none")
4. Row count = section count (no invented or dropped sections)
5. `formatting_memo.md` exists
6. Memo explains **each** flagged section, separately gradeable per finding type
7. Memo states why the annex is cleared, and ties it to the exemption
8. `results.json` exists and parses
9–13. Each of the five counts
14. Counts are consistent with the delivered CSV (not self-reported in isolation)

## Comparison against the shipped `tests/verifier.json` (14 verifiers)

| Gap | Detail |
|---|---|
| **G1 — two rows ungraded** | `SEC-COVER` and `SEC-CH1` have no verifier. A run that flags either still passes 14/14. |
| **G2 — row checks are not end-anchored** | `^SEC-CH2\s*,.*MARGIN_NONCOMPLIANT` scans the whole row. `annex_trap_clean` is `^SEC-ANNEX-A\s*,.*none` — a row reading `SEC-ANNEX-A,MARGIN_NONCOMPLIANT,"none of the exceptions apply"` satisfies the check that exists to catch exactly that error. Same defect class as g780/F3. |
| **G3 — no schema or row-count check** | Nothing stops the model echoing the input log with a `finding` column appended, or inventing rows. |
| **G4 — memo checks give free points** | `memo_margin` is `(?i)\bwrong margin\|\bline spacing`; alternation binds loosest, so either term alone passes. The **font** finding has no memo coverage at all. |
| **G5 — counts are self-reported** | The five `result_*_count` checks compare `results.json` to constants and are never reconciled with the delivered CSV. Combined with G1+G2, a CSV that flags the annex and clears CH2 can still score 14/14. |
| **G6 — nothing grades what the ask emphasises** | The prompt's headline reasoning step (the annex exemption) reduces to one substring search. |

Coverage in the other direction — unfair checks: none found. No verifier asks for anything the
prompt does not request.

# Cold read — gen-g988-composite-photo-request-rights-audit

Read `instruction.md` and `environment/input/` only, before opening `tests/`.

## What the task asks

Audit 8 composite photo-edit requests against intake policy INT-09 on four rules
(licensed-character use with a personal-use allowance, third-party background
licensing, minor consent, commercial distribution routing). Deliver
`composite_request_audit.csv` (one row per request, `finding` column),
`composite_request_memo.md`, and `results.json` with five counts.

## The answer, derived cold

| request | char | background | distribution | minor / consent | finding |
| --- | --- | --- | --- | --- | --- |
| REQ-01 | True | customer_original | personal_only | – | `none` (allowance) |
| REQ-02 | True | customer_original | social_public | – | `UNLICENSED_CHARACTER_USE\|COMMERCIAL_DISTRIBUTION_FLAG` |
| REQ-03 | False | third_party_unlicensed | personal_only | – | `THIRD_PARTY_BACKGROUND_UNLICENSED` |
| REQ-04 | True | customer_original | personal_only | minor, no consent | `MISSING_MINOR_CONSENT` |
| REQ-05 | True | customer_original | personal_only | minor, consent | `none` |
| REQ-06 | False | customer_original | print_for_sale | – | `COMMERCIAL_DISTRIBUTION_FLAG` |
| REQ-07 | False | customer_original | personal_only | – | `none` |
| REQ-08 | False | licensed_stock | social_public | – | `COMMERCIAL_DISTRIBUTION_FLAG` |

`request_count` 8, `flagged_count` 5, `commercial_count` 3, `background_count` 1,
`compliant_count` 3.

This took about four minutes and no judgement calls. Every column is a boolean or a
three-value enum, every rule reads exactly one column, and the rules do not interact
except that the personal-use allowance suppresses the character finding.

## Guesses I had to make

1. **Pipe-order for REQ-02.** The prompt says "pipe-joined combination" and never fixes
   an order. Two defensible answers; the grader must accept either.
2. **Does the personal-use allowance reach the other rules?** REQ-04 is personal-only and
   still gets `MISSING_MINOR_CONSENT` under the gold. The policy says the allowance means
   the character use "is not a defect" — it never says what else it does or does not
   release. Guessable, not stated.
3. **`licensed_stock` vs `customer_original` for §2.** Rule 2 flags a background that is
   "not the customer's own, and not a properly licensed stock image". REQ-08's
   `licensed_stock` is clearly clear. No real ambiguity, but nothing tests the third state.
4. **Does `COMMERCIAL_DISTRIBUTION_FLAG` count as "flagged"?** `flagged_count` = 5 only if
   a routing flag counts as a finding. The prompt never says. Guessed from the gold shape.

## Where the prompt or the input leaks the answer

1. **The prompt names the trap.** "noting its personal-use allowance" and "which request
   the personal-use allowance clears" tell the model there is an allowance, that it
   matters, and — with the singular *request* — that exactly one row turns on it. The
   only real reasoning in the task is handed over in the instruction line.
2. **The policy names the trap again, as a warning.** "Flagging a personal, non-distributed
   request for licensed-character use is the commonest false positive." The fixture's one
   distinguishing rule ships with its own answer key.
3. **The column names are the findings.** `uses_licensed_character` → `UNLICENSED_CHARACTER_USE`,
   `subject_is_minor`/`minor_consent_on_file` → `MISSING_MINOR_CONSENT`,
   `background_source=third_party_unlicensed` → `THIRD_PARTY_BACKGROUND_UNLICENSED`. The
   log is a pre-computed answer sheet; no lookup, derivation or judgement is needed to get
   from a row to its verdict.
4. **The finding-name list is repeated three times** (prompt, policy §5, policy "Finding
   names"), so even the output vocabulary needs no inference.

## My verifier list, written before opening tests/

1. `composite_request_audit.csv` exists, has a `request_id`/`finding` header, and carries
   exactly 8 data rows.
2. Eight per-request assertions on the **exact finding set** — the codes that must appear
   and the codes that must not. (Presence-only checks pass an over-flagging answer.)
3. `REQ-02` must carry both codes; either pipe order accepted.
4. `results.json` — five keys, five values.
5. Memo names every flagged request and says what clears the allowance rows.
6. Memo must not be gradeable by echoing the prompt.

## Compared with `tests/verifier.json` (13 verifiers)

**Coverage gaps — all in the same direction: over-flagging is free.**

- Only 4 of 8 requests are checked at all. **REQ-05, REQ-06, REQ-07 and REQ-08 have no
  row-level assertion.** REQ-05 is the second allowance row and the only row testing
  consent-present; nothing grades it.
- Every row check is a bare `.*CODE` presence regex with **no negative lookahead**. An
  answer that writes all four codes on every row passes `character_flagged`,
  `background_flagged` and `consent_flagged`. Only `trap_clean` (REQ-01 must match
  `.*none`) constrains anything, and `.*none` also matches the substring in the word
  `none` inside e.g. `NONE_OF_THE_ABOVE`, or a `notes` column containing "none apparent".
- `memo_trap` matches `REQ-01 .* allowance` — satisfied by pasting the prompt's own phrase
  next to the request id.
- Nothing checks the audit's row count or header, so an 8-row requirement is unenforced.
- The `results.json` counts are the only checks that actually discriminate, and they are
  five integers over a table the model has already been handed.

**Unfair checks:** none. Nothing is graded that the prompt does not ask for.

## Verdict going in

The fixture is 8 rows × 4 independent single-column rules over 2 files — the shape the
runbook records as never-hard. Expect 5/5, and expect it for the right reason: there is
no reasoning step to get wrong. Hardening has to add coupling (derived thresholds,
cross-source lookup, exceptions with scope, roll-ups over the model's own results), not
more rules.

# Proposed fixture rewrite — staged, NOT applied

This is a **proposal only**. Nothing in `gen-g780-realestate-fairhousing-collateral-audit/`
has been touched. Apply only if the pod confirms `environment/input/` is editable for
ComputerBench NonConnector gen tasks.

## What changes

The shipped `seller_book_sections.csv` hands the agent the verdicts:

    section_id,contains_personal_narrative,mentions_protected_class_terms,is_mandated_disclosure,missing_required_disclaimer
    SEC-02,True,False,False,False

The proposed version hands it **the collateral**, and the agent has to judge it:

    section_id,title,role,body
    SEC-02,A note from the current owners,seller_letter,"We are looking for someone who will love this house..."

Structural metadata (`section_id`, `title`, `role`) is kept because a real inventory would
carry it and §4 needs `role` to work. The **verdict booleans are gone** — that is the
entire point.

## Ground truth is preserved

Same answers, so the existing gold and the 22 verifiers carry over unchanged:

| Section | Expected finding | Why it must be judged, not read off |
|---|---|---|
| SEC-01 | `none` | plain listing copy |
| SEC-02 | `PROHIBITED_PERSONAL_NARRATIVE` | solicits a buyer "love letter" — must be recognised as §1, never labelled |
| SEC-03 | `PROTECTED_CLASS_LANGUAGE` | "family-oriented", "churches", "parish school", "long-established families" — religion + familial status, implied not stated |
| SEC-04 | `none` | **the trap.** Explicitly names race, religion, sex, familial status, national origin, disability — the single most protected-class-dense section in the book. Only §3 saves it, and `role=disclosure_block` is the signal. |
| SEC-05 | `DISCLAIMER_MISSING` | `role=closing_page` must carry the disclosure under §4 and does not |
| SEC-06 | `none` | plain systems copy |
| SEC-07 | all three, `\|`-joined | solicits a personal note, says "churchgoing families", and is a closing_page that omits the disclosure |

SEC-04 is why this works. Under the current fixture it is `mentions_protected_class_terms=True,
is_mandated_disclosure=True` — a two-column lookup. Under the proposal it is a wall of
protected-class terms that a careless model will flag, and the agent must connect
`role=disclosure_block` to §3 to clear it. **That is the task the prompt claims to be asking for.**

SEC-03 and SEC-07 also get materially harder: nothing says "protected class", the model has
to recognise religion and familial-status signals in ordinary marketing prose.

## Companion change to RE-FH-9

§4 currently says "A section responsible for carrying it that omits it is
`DISCLAIMER_MISSING`" without defining *responsible*. Add one sentence:

> Every `closing_page` section is responsible for carrying the mandated disclosure.

And **remove the giveaway** from §3:

> ~~Flagging the mandated disclosure itself as a violation is the commonest false positive
> in this audit.~~

That sentence is the answer key in prose and is the reason the trap currently has no teeth.

## Optional, if the band still is not reached

Add an 8th section that is **both** the mandated disclosure **and** carries a personal
narrative. §3 exempts only from §2, so it should be `PROHIBITED_PERSONAL_NARRATIVE` — the
first row that actually discriminates between the narrow and blanket readings of §3. This
requires updating the gold answer, the counts and three verifiers.

## Work to apply

1. Replace `environment/input/seller_book_sections.csv`
2. Two edits to `environment/input/realestate_fairhousing_standard.md` (above)
3. `instruction.md` — the ask stays; drop any wording that assumes pre-classified columns
4. `solution/files/*` unchanged if ground truth is preserved
5. `tests/verifier.json` unchanged if ground truth is preserved
6. Oracle to 1.0, then a fresh 5× battery from Git Bash

Estimated: under an hour including the battery.

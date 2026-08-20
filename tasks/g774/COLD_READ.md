# Cold read — gen-g774-activity-kit-print-spec-audit (mined baseline)

Read `instruction.md` and `environment/input/` only, before opening `tests/`.

## The baseline task

6 pages, 2 input files, 3 independent rules, 3 deliverables.

    page_id,page_name,dpi,margin_in,full_bleed_design,element_count,min_element_required
    PG-01,Cover,300,0.05,True,1,1
    ...

## Guesses I had to make

None of substance. That is the problem — the task is fully determined and fully
spelled out. There is no ambiguity to fix, and no reasoning to do.

## Where the prompt and the input leak the answer

1. **`min_element_required` is a column in the CSV.** Rule §4 says "each page type has a
   minimum count of required elements" and then the fixture hands that minimum over on
   the row. The rule reduces to `element_count < min_element_required`.
2. **Every threshold is a literal in the prompt or the standard.** 300 DPI, 0.125 in.
   Nothing is derived; nothing depends on anything else.
3. **The prompt signposts the only trap.** "mind the standard's exception for full-bleed
   pages" — and the standard then says outright that flagging a full-bleed page is "the
   commonest false positive in this audit". The one piece of judgment in the task is
   pointed at twice.
4. **6 rows.** Three rules over six rows is 18 comparisons. There is no error compounding
   and the whole batch fits on one screen.

## Verifier list I would have written, vs `tests/verifier.json`

The shipped set has 14 verifiers. Coverage gaps, in both directions:

- **Only 4 of 6 pages have a verdict checked at all.** `PG-05` (clean) and the multi-code
  cell on `PG-06` are never asserted. An answer that flags PG-05 wrongly still scores 1.0.
- **The per-page assertions are one-sided.** `dpi_flagged` requires `PG-02` to contain
  `DPI_TOO_LOW` and asserts nothing about the other codes, so `PG-02` reading
  `DPI_TOO_LOW|MARGIN_VIOLATION|ELEMENT_COUNT_SHORT` — two false positives — passes.
- **Free points.** `audit_exists`, `memo_exists`, `results_exists` and
  `memo_finding_terms` (any one of the three code names anywhere in the memo) cannot fail
  a serious attempt. `result_page_count == 6` is the row count of the input file, which is
  not a derived figure. That is 5 of 14 verifiers, a 0.36 floor on partial credit.
- **`memo_bleed`** wants `full-bleed ... exempt` — reasonable, and the one check with
  content in it.

## Conclusion

Solvable, correctly graded on the four things it does check, and far too easy: a single
pass of pandas with three `if` statements answers it. The grader would also accept several
wrong answers. Hardening has to add reasoning, not rules — see `CHANGES.md`.

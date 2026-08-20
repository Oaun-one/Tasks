# Changes — gen-g774-activity-kit-print-spec-audit

Baseline: `ORIGINAL_BACKUP/` (byte-identical to the mined drop).
`task.toml` is unchanged — same name, description, keywords and `source_config`.

Everything below is generated from `tools/g774_build.py` (the data model and the
adjudicator) via `tools/g774_emit.py`, so the fixtures, the gold answer and
`tests/verifier.json` cannot disagree about a verdict.

## 1. Leakage removed

| Removed | Why |
| --- | --- |
| `min_element_required` column | Handed over the §6 minimum on the row. The minimum is now derived from the page-type table **and** Amendment Rev B, which depends on the section's binding. |
| "mind the standard's exception for full-bleed pages" | The prompt pointed at the only piece of judgment in the task. The standard still documents the exception; the prompt no longer aims the model at it. |
| Flat thresholds in the prompt | 300 DPI and 0.125 in were constants. Every limit is now a property of the paper stock, reached through the page's section. |

## 2. What the task now requires (the hardening)

Difficulty comes from interactions, not from more rules. Five couplings:

1. **Two-hop join.** A page carries a `section_id`; the section carries the binding and
   the `stock_code`; the stock carries `min_dpi`, `min_margin_in`, `max_ink_pct` and
   `min_bleed_in`. No limit can be read off the page row. PG-13 at 298% ink is clear on
   BRD-250 and PG-28 at 241% is over on UNC-120 — the smaller number is the breach.
2. **Derived measured value.** §2 grades `floor(artwork_dpi * 100 / placement_scale_pct)`,
   not `artwork_dpi`. PG-06 is supplied at 450 dpi and fails nothing on resolution only
   because it prints at exactly 300; PG-20 is supplied at 240 dpi and clears a 300 floor.
   Reading the supplied figure straight off the row gets 11 verifiers wrong.
3. **An exception that also creates an obligation.** §4 exempts a full-bleed page from the
   margin rule and makes it the only kind of page that owes a bleed allowance. Treating
   full-bleed as a blanket pass loses 7 verifiers; applying the margin rule to full-bleed
   pages anyway loses 12.
4. **A conditional amendment.** Rev B raises the `mission_cards` and `badge_certificate`
   minimums by 2 in `saddle_stitch` sections only. PG-19 (6 mission cards, perfect-bound)
   is clear on exactly the count that makes PG-13 (6 mission cards, saddle-stitched) short
   by 2. Ignoring the amendment loses 8 verifiers.
5. **State across steps.** The batch lists *artwork*, not pages: four `page_id`s appear
   twice and only the highest `revision` is live. The live revision sits **before** the
   superseded one for PG-12 and PG-27 and **after** it for PG-04 and PG-18, so neither
   "first row wins" nor "last row wins" is right — the dedupe has to be done before any
   comparison, and it changes four verdicts and every derived figure.

Plus scale and shape: **30 live pages, 34 artwork rows, 3 stocks, 6 sections, 5 finding
codes** — 150 page-rule comparisons. Every limit is inclusive and 14 pages sit exactly on
at least one limit, so a single `<=` for `<` floods the audit (26 verifiers lost).

## 3. Deliverables

`activity_kit_audit.csv`, `activity_kit_memo.md` and `results.json` keep their original
names. `results.json` keeps its original five keys (`page_count`, `flagged_count`,
`dpi_low_count`, `margin_count`, `element_short_count`) and gains six:
`superseded_count`, `clean_count`, `finding_total`, `bleed_short_count`, `ink_over_count`,
`element_shortfall_total`.

`page_count` is no longer a free point: it is 30 live pages out of 34 artwork rows, so it
is only right if the supersession is right.

## 4. Grading

14 verifiers → 54, and the shape changed more than the count:

- **One verifier per page (30), asserting the exact finding set** — every required code
  present *and* every other code absent. The baseline asserted presence only, so an answer
  with two false positives on PG-02 still scored 1.0. `evidence_negative_check/` reproduces
  that.
- **`audit_has_one_row_per_page`** — a backreference check that no `page_id` appears on two
  lines, which catches an audit emitted per artwork row rather than per live page.
- **`audit_has_no_pages_outside_batch`**, **`audit_has_page_id_and_finding_columns`**.
- **11 derived figures**, each recomputed from the batch rather than read back from the
  model's own summary.
- **7 memo checks**: every flagged page named, all five codes used, the full-bleed
  exemption, the bleed obligation, the effective-resolution reading, the four superseded
  pages, and Rev B.

Free points are down to the three `*_exists` checks (3 of 54). Reward is binary in
`tests/test.sh`, so a run counts only if the whole audit is right.

Assertions accept a correct answer in any reasonable shape: extra or reordered columns,
quoted fields, finding codes in any order within a cell, `none` in any case or as any of a
list of synonyms, and a memo written as prose or as tables.

## 5. Fairness

- Every rule is stated in `input/activity_kit_print_standard.md`. Nothing is withheld.
- The prompt says the limits are per-stock, that the batch has been re-supplied, and that
  the standard carries an amendment — the model is told where the work is, not how to do it.
- Rounding is specified (`floor`), and no verdict in the fixture turns on the rounding, so
  a model that does not floor is not punished for it.
- Every boundary value is binary-exact (0.125, 0.1875, 0.25), so no verdict turns on
  floating-point noise.
- `tools/g774_negative_check.py` runs nine plausible misreadings through the real grader;
  every one loses at least six verifiers, and none scores 1.0.

## 6. Other

- `environment/Dockerfile`: base image pinned to
  `python:3.12-slim-bookworm@sha256:a116514e…78134`. No other change.
- `tests/verifier.json` keeps its filename (non-connector layout).
- `tests/test.sh`, `tests/test_outputs.py`, `tests/rl_world_verifiers/` unchanged.
- `solution/solve.sh` unchanged; `solution/files/` regenerated.

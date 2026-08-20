# Changes made to NONC-B1-1001608 / gen-g780

Original preserved at `ORIGINAL_BACKUP/` for diffing.
Nothing under `environment/` was touched — no Dockerfile, no input fixtures, no seed data.
Editable surface used: `instruction.md`, `tests/verifier.json`, `README.md` (new).
`solution/` was NOT changed — the gold answer already complied with the tightened spec.

## Why the task was changed

Baseline measurement: **5/5 on GLM 5.2** (job `glm-5x-baseline-v2-NONC-B1-1001608`,
5 trials, 0 exceptions). ComputerBench accepts only 1/5 or 2/5, so the task was out of
band and had to be hardened or discarded.

Trajectory evidence for *why* it was 5/5: **4 of the 5 runs emitted the input inventory
with a `finding` column appended** —
`section_id,contains_personal_narrative,mentions_protected_class_terms,is_mandated_disclosure,missing_required_disclaimer,finding`
— confirming the task collapsed to a boolean-to-label rename. The input CSV's boolean
columns map 1:1 onto the four output labels.

`environment/input/seller_book_sections.csv` is the source of that leakage and is NOT
editable, so the harden works on the ask and the grading instead.

## instruction.md

| Change | Type | Rationale |
|---|---|---|
| Pinned the audit CSV to **exactly two columns** with an in-world reason (print vendor's importer) | harden | Rejects the echo-the-input shortcut 4/5 runs took. Real briefs do specify output schemas. |
| Pinned the `\|` **join order** (narrative → protected → disclaimer) | ambiguity fix | Was undefined; models could sort alphabetically and differ. Now gradeable. |
| **Defined all five counts** as counts of *sections*, not labels | ambiguity fix | `flagged_count` (4 vs 6) and `protected_lang_count` (2 vs 3) were graded but never defined. |
| Removed *"mind the standard's exception for the mandated disclosure itself"* | de-leak | The prompt announced the trap. RE-FH-9 §3 still states the exemption, so no information the model needs was removed. |
| Rewrote the opening as a colleague's message (print deadline, legal sign-off) | realism | The original read as harness scaffolding after the first sentence. |

Note: pinning the join order and the count definitions **raises** the pass rate; pinning
the schema **lowers** it. They were applied together and re-measured once, rather than
chasing the number one change at a time.

## tests/verifier.json — 14 verifiers → 22

All deterministic. No judged checks added or removed.

### Defects fixed

- **F1 uncovered ask.** SEC-07 — the only row exercising the `|` multi-finding rule — had
  no verifier. SEC-01 and SEC-06 were also ungraded. Now one anchored check per row.
- **F2 free point.** `memo_finding_terms` was
  `(?i)\bA|\bB|\bC` — alternation has the lowest precedence, so any *one* term passed.
  Split into `memo_explains_narrative` / `_protected` / `_disclaimer`.
- **F3 defeatable primary goal.** `mandated_trap_clean` was `^SEC-04\s*,.*none`, which
  scans the whole row. Demonstrated defeat in `evidence_coverage_gap/`: SEC-04 flagged
  `PROTECTED_CLASS_LANGUAGE` with a rationale column reading "none of the other rules
  apply" scored 14/14. Replaced with an end-anchored row check plus a negative guard,
  `sec04_carries_no_violation_label`.
- **F4 synonym gap.** `memo_mandated` required literal "mandated"…"exempt". Replaced with
  `memo_names_exempt_section`, which accepts exempt/exempted/exemption/excluded/clears/
  cleared.
- **F5 ungrounded assertions.** The five `result_*_count` values were graded but never
  defined in the prompt. The values are unchanged; the prompt now defines them.

### Known limitation, stated rather than hidden

The verifier engine's `csv` source exposes only `extract_text`, so the counts in
`results.json` cannot be *recomputed* from the delivered CSV inside the DSL — they are
still compared to constants. The row checks now pin every cell of the CSV, so a CSV that
contradicts `results.json` fails the row checks instead. This narrows the gap the QC
platform flagged as "counts are self-reported" but does not fully close it.

## Outcome of the harden

**No change: 5/5 before, 5/5 after** (job `glm-5x-hardened-v1-NONC-B1-1001608`, 5 trials,
0 exceptions, rewards 1,1,1,1,1). All five hardened runs emitted `section_id,finding`
correctly — the pinned schema stated a requirement the model then satisfied rather than
creating difficulty. See ESCALATION.md for the discard recommendation.

## Verification

- Gold answer: **22/22 pass** (Oracle `oracle-hardened-v1`, reward 1.0).
- `evidence_coverage_gap/` sabotage: **13 of 22 fail** (passed 14/14 before).
- The GLM output shape from the baseline runs: **9 of 22 fail**.

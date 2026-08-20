# Cold read — NONC-B1-1001608 / gen-g780-realestate-fairhousing-collateral-audit

Trainer: muhammad.04@turing.com
Workstream: ComputerBench NonConnector, b_batch_1
Cold read completed before opening tests/verifier.json or solution/.

---

## 1. What is being asked

Take a 7-row inventory of seller's-book sections, apply a 4-rule fair-housing
standard (RE-FH-9) to each row, and emit a per-section finding label. It is a
rule-application-and-tabulation task with one deliberate trap: the mandated-
disclosure section mentions protected classes but is exempt, so the naive answer
over-flags it.

## 2. What I would deliver

Three files in `/app`:

1. `fairhousing_audit.csv` — header + 7 data rows.

   | section_id | finding |
   |---|---|
   | SEC-01 | none |
   | SEC-02 | PROHIBITED_PERSONAL_NARRATIVE |
   | SEC-03 | PROTECTED_CLASS_LANGUAGE |
   | SEC-04 | none  (exempt under §3) |
   | SEC-05 | DISCLAIMER_MISSING |
   | SEC-06 | none |
   | SEC-07 | PROHIBITED_PERSONAL_NARRATIVE\|PROTECTED_CLASS_LANGUAGE\|DISCLAIMER_MISSING |

2. `fairhousing_memo.md` — prose explaining each flagged section, naming SEC-04
   as the section the standard clears.

3. `results.json`:
   `{"section_count": 7, "flagged_count": 4, "personal_narrative_count": 2,
     "protected_lang_count": 2, "disclaimer_missing_count": 2}`

## 3. Every place I had to guess

**Q3 — multiple findings per section, and their order.**
Multiple findings: STATED. Both instruction.md and the standard's preamble say
findings are joined with `|`. SEC-07 exercises it.
Order: GUESSED. Nothing states an order. I picked narrative → protected →
disclaimer because that is the order the tokens are listed in both files, and it
tracks §1→§2→§4. That is a convention inferred from listing order, not a rule.
A model sorting alphabetically emits
`DISCLAIMER_MISSING|PROHIBITED_PERSONAL_NARRATIVE|PROTECTED_CLASS_LANGUAGE`
and differs on that cell.

**Q4 — clean sections.**
STATED, clearly. `none` is one of the four legal finding values in both files.
Literal lowercase `none`, not empty, not `None`, not `NONE`. Confident.

**Q5 — scope of the mandated-disclosure exception.**
STATED, narrowly. §3 exempts the mandated disclosure from the protected-class
rule (§2) only — not a blanket clear. A mandated-disclosure section that also
carried a personal narrative would still be flagged for that.
BUT the data never tests this. SEC-04 has only the protected-class flag set, so
the narrow and broad readings produce identical output. The trap has no teeth as
constructed: a model that wrongly reads §3 as "exempt from everything" still
passes. DEFECT — would need a row with `is_mandated_disclosure=True` plus a
second violation to actually discriminate.

**Q6 — `flagged_count`: sections or findings?**
GUESSED. The sharpest ambiguity in the task. Nothing defines it.
Sections with ≥1 finding = 4. Total findings across all sections = 6.
They differ only because SEC-07 carries three. I chose 4 — "flagged" reads as a
property of a section, and the sibling keys already give per-category totals, so
counting findings would make `flagged_count` redundant with their sum. That is
an argument, not an instruction.

Second-order: is SEC-04 "flagged"? Its finding is `none`, so no. But someone
could reasonably count "sections the standard had something to say about". Also
undefined.

Third: does `protected_lang_count` count emitted findings (2 — SEC-03, SEC-07)
or input rows with the flag set (3 — SEC-03, SEC-04, SEC-07)? I chose 2, on the
reasoning that these keys summarise the audit. Genuinely could go either way,
and this is the one place the exemption trap does still bite. Not stated.

**Q7 — CSV columns.**
GUESSED. The prompt names `finding` and implies `section_id` via "one row per
section", and says nothing about anything else. I emit exactly those two, in
that order, with a header. Unstated: whether extra columns are tolerated or
fatal, whether the header is required, whether row order must match input.
Assumed header required and input order preserved.

**Q8 — everything else I had to guess.**
- Whether `|` has surrounding spaces. Assumed none.
- Token case — assumed verbatim uppercase, never stated as case-sensitive.
- `results.json` values as JSON ints, not strings. Assumed ints.
- Whether extra keys beyond the five named are allowed. Emitted exactly five.
- Memo structure entirely undefined — no required headings. Only inferable
  constraint: mention every finding, name the exempted section. Whether it must
  name it as the literal string `SEC-04` is a guess (I would).
- Whether `none` sections need to appear in the memo at all.
- Trailing newline / line endings on the CSV. Assumed `\n` with trailing newline.

## 4. Answer leakage — severe

**Leak 1 — the input CSV is the answer key.** Its columns are
`contains_personal_narrative`, `mentions_protected_class_terms`,
`is_mandated_disclosure`, `missing_required_disclaimer` — a 1:1 map onto the four
output labels. There is no section text. Nothing to actually audit. The whole
"fair-housing analysis" collapses to a boolean-to-string rename plus one
conditional. A real analyst would read section copy and judge whether it contains
a narrative or protected-class language; here that judgment is pre-made and
handed over in the column names.

**Leak 2 — the trap announces itself, twice.**
- instruction.md: "mind the standard's exception for the mandated disclosure"
- standard §3: "Flagging the mandated disclosure itself as a violation is the
  commonest false positive in this audit."

That second sentence is the answer key in prose. A trap that tells you it is a
trap does not discriminate between a careful model and a careless one.

**Leak 3 — mild.** "the exempted section the standard clears" is singular,
confirming exactly one section is exempt before you look.

**Net:** the only genuinely discriminating things left are the join order and the
`flagged_count` / `protected_lang_count` definitions — all three undefined. The
task is easy where it is specified and ambiguous where it is hard. That is
backwards.

## 5. Does the prompt sound like a real person?

Partly. The first paragraph passes:
> "Audit the attached seller's-book section inventory against our fair-housing
> compliance standard before it goes to print."

"our" standard, "before it goes to print" — a person with a deadline and a stake.

It breaks immediately after:
> "Save your deliverables into your current working directory using exactly these
> filenames" … "Writing those files is the required deliverable and must be your
> final action; confirm each one exists before you answer."

No colleague writes that. It is harness scaffolding pasted into a message
addressed to a person, and "confirm each one exists before you answer" instructs
an agent about its turn structure. The `results.json` block with five exact
snake_case keys is a schema, not a request.

The persona also does not survive contact with the payload: someone sending you a
print-ready seller's book would attach the book. Attaching a CSV whose columns
are already the compliance verdicts is a benchmark author's artifact, not a
colleague's. The framing and the payload are from two different worlds.

---

## 6/7. Verifier comparison — after opening tests/verifier.json

14 verifiers, **all deterministic**. No LLM-judged checks anywhere, so judge
variance cannot move the pass rate and verifier stability is near-guaranteed.

### Coverage by row

| Row | Graded | Note |
|---|---|---|
| SEC-01, SEC-06 (clean) | NO | clean rows never checked |
| SEC-02 narrative | yes | `narrative_flagged` |
| SEC-03 protected | yes | `protected_flagged` |
| SEC-04 trap → `none` | yes | `mandated_trap_clean` |
| SEC-05 disclaimer | yes | `disclaimer_flagged` |
| **SEC-07 (multi-finding)** | **NO** | **the only row exercising `\|` is ungraded** |

### Findings

**F1 — Uncovered ask: SEC-07 / the multi-finding rule (coverage gap).**
The prompt explicitly instructs "join multiple findings with `\|`". SEC-07 is the
only row that exercises it and no verifier touches it. The hardest row in the
task is not graded. Consequence: the join-order ambiguity in §3 above is moot in
practice, but for the wrong reason — the requirement is simply unchecked.

**F2 — Free point: `memo_finding_terms` regex is broken.**
`(?i)\bPROHIBITED_PERSONAL_NARRATIVE|\bPROTECTED_CLASS_LANGUAGE|\bDISCLAIMER_MISSING`
Alternation has the lowest precedence in regex, so this is `A or B or C`. It
passes if the memo mentions any ONE of the three terms. Named as though it checks
the memo explains each finding; it checks essentially nothing. `(?i)` also makes
it case-insensitive, so lowercase mentions pass.

**F3 — The trap check can be defeated by an extra column.**
`mandated_trap_clean` is `(?mi)^SEC-04\s*,.*none` and scans the whole row. A model
emitting `section_id,finding,rationale` where SEC-04 reads
`SEC-04,PROTECTED_CLASS_LANGUAGE,"none of the other rules apply"` PASSES the trap
check while failing the trap. The only check with real teeth is defeatable by a
rationale column. The same `.*` looseness applies to F-checks on SEC-02/03/05.

**F4 — Synonym gap: `memo_mandated`.**
`(?is)\bmandated\w*\b.*\bexempt` requires the literal words. A memo saying "the
required disclosure is excluded under §3" fails on correct content.

**F5 — Ungrounded-but-graded values.**
`result_flagged_count` asserts 4 and `result_protected_lang_count` asserts 2.
Neither definition appears anywhere in the prompt or the standard (see §3 Q6).
A model answering 6 and 3 — both defensible readings — fails. This is an
ambiguity fork that is actively graded, and it is the likeliest source of any
failures observed in the GLM battery.

### Primary goal

One sentence: *correctly apply the mandated-disclosure exception so SEC-04 is not
over-flagged, while flagging the three genuine violation types.*

Verifier that checks it: `mandated_trap_clean` — but see F3, it is defeatable.

### Hardening constraint

`environment/` is not editable per the playbook (Dockerfile and seed data are
off-limits), so the §4 input leakage CANNOT be fixed by rewriting
`environment/input/seller_book_sections.csv`. Editable surface is limited to
`instruction.md`, `tests/` and `solution/`.

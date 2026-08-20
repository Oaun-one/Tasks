# Task

The thesis office runs a formatting pre-check before a dissertation is accepted for binding.
Submission TO-2026-0447 is with you. The typesetting system's export of every section is in
`input/dissertation_section_log.csv`; the standard it is measured against is
`input/dissertation_formatting_spec.md`, which is amended by `input/dfs11_amendments.md`; the
office's own record of this submission is `input/thesis_office_record.md`.

Work out what the specification actually requires of *this* submission, then audit every
section against it and report.

## Deliverable 1 — `formatting_audit.csv`

Exactly two columns, with this header line and nothing else on it:

    section_id,finding

One row per audited section. Rows may be in any order.

`finding` is either `none`, or the labels for every rule the section breaches, joined with a
single `|` and no spaces, in this order:

    MARGIN_NONCOMPLIANT | FONT_NONCOMPLIANT | SPACING_NONCOMPLIANT

So a section breaching the margin and spacing rules reads
`MARGIN_NONCOMPLIANT|SPACING_NONCOMPLIANT`. Do not add a rationale column, a revision column,
or any other column — the office's importer rejects the file if the header is not the two
names above.

## Deliverable 2 — `formatting_memo.md`

A markdown memo for the thesis officer, covering:

1. **Which amendments you applied and which you did not**, naming each amendment by its
   identifier and giving the reason for each disposition.
2. **Every figure you derived from the specification and used as a threshold**, with its
   value. Give the number, not just the method.
3. **How many log rows you audited and how many you set aside**, and on what basis.
4. **One entry per flagged section**, naming the section by its `section_id`, the finding or
   findings against it, and the measured value responsible for each.
5. **Which sections the Rule 1 exception applies to**, and why it applies to those and not to
   others.

## Deliverable 3 — `results.json`

A JSON object with exactly these keys, each an integer:

- `section_count` — the number of sections you audited (one per audited `section_id`)
- `flagged_count` — audited sections carrying at least one finding
- `margin_count` — audited sections carrying `MARGIN_NONCOMPLIANT`
- `font_count` — audited sections carrying `FONT_NONCOMPLIANT`
- `spacing_count` — audited sections carrying `SPACING_NONCOMPLIANT`

A section breaching two rules counts once in `flagged_count` and once in each of the
per-rule counts.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `formatting_audit.csv` — Per-section formatting audit
    - `formatting_memo.md` — Markdown memo
    - `results.json` — a JSON object with the keys `section_count`, `flagged_count`, `margin_count`, `font_count`, `spacing_count`
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

# Task

Submission TO-2026-0447 goes to the bindery on Friday and the thesis office needs a full
pre-binding pass over it first. Everything is in `input/`: the section log exported from the
typesetting system, the part plan naming the template each part is set in, the template
profiles, our DFS-12 standard, its amendments, and the office's record of this submission.

Apply the standard as written. Several limits are per-template, so a section is only in
breach against the template its own part is set in, and the parts carry a rule of their own.

## Deliverable 1 — `formatting_audit.csv`

One row per audited section, with these columns in this order:

    section_id,part_id,template_id,finding

`finding` carries the code for every rule that section breaches, joined with `|` and no
spaces, in the order the standard sets them out:

    MARGIN_NONCOMPLIANT | TYPE_AREA_INVALID | LEADING_NONCOMPLIANT | FONT_NONCOMPLIANT
    | HEADING_STYLE_INVALID | CAPTION_MISSING | NUMBERING_INVALID

Use `none` for a section that breaches nothing. Rows may be in any order.

## Deliverable 2 — `part_summary.csv`

One row per part, with these columns in this order:

    part_id,template_id,section_count,flagged_sections,start_page,pagination

`section_count` and `flagged_sections` count audited sections. `start_page` is the page the
part opens on. Use the same `none` convention in `pagination` for a part that paginates
cleanly.

## Deliverable 3 — `formatting_memo.md`

A markdown memo for the thesis officer. Say which amendments you applied and which you did
not, naming each by its identifier and giving your reason in each case, and give the value of
every figure you derived from the standard and used as a threshold — the numbers, not just
the method, and both numbers where a figure differs between the two templates. Say how many
log rows you audited and how many you set aside, and on what basis. Account for every section
carrying a finding, naming it by `section_id` and giving, for each of its findings, the
measured value and the limit it missed. Where a section's numbers look like a breach and the
standard clears it anyway, say what clears it. Call out the sections whose release from the
type-area rule turns on which template their part is set in. Name the parts that cannot be
paginated as planned and the page each one currently opens on. And give the total number of
captions still to be written across the batch.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `formatting_audit.csv` — Per-section formatting audit
    - `part_summary.csv` — Per-part rollup
    - `formatting_memo.md` — Markdown memo
    - `results.json` — a JSON object whose values are all integers, with the keys
      `section_count`, `part_count`, `clean_section_count`, `flagged_section_count`,
      `finding_total` (every finding raised across the batch, not the number of sections
      carrying one), `margin_count`, `type_area_count`, `leading_count`, `font_count`,
      `heading_count`, `caption_missing_count`, `numbering_count` (each of these seven
      counting the audited sections carrying that finding), `caption_shortfall_total` (how
      many captions the batch is missing in total, across the sections carrying
      `CAPTION_MISSING`), `pagination_invalid_parts` (how many parts cannot be paginated as
      planned), `sections_in_invalid_parts` (how many audited sections sit in those parts),
      `flagged_archive_sections` and `flagged_reading_sections` (flagged sections split by
      the template their part is set in)
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

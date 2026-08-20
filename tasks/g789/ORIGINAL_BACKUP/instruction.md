# Task

Audit the attached dissertation section formatting log against the formatting specification before it goes to the thesis office. Check each section's margins, font and line spacing — remembering that landscape data annexes follow a different margin rule than the rest of the document, though font and spacing still apply everywhere. Save `formatting_audit.csv` with one row per section and a `finding` column (`MARGIN_NONCOMPLIANT`, `FONT_NONCOMPLIANT`, `SPACING_NONCOMPLIANT`, `none`). Then write `formatting_memo.md` explaining each finding and the annex the specification clears.

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

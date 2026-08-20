# Task

Audit the attached activity-kit page batch against our print-production standard before we send the files to the printer. Check image resolution, safe margins, and each page's required-element count against its own minimum — mind the standard's exception for full-bleed pages. Save `activity_kit_audit.csv` with one row per page and a `finding` column using `DPI_TOO_LOW`, `MARGIN_VIOLATION`, `ELEMENT_COUNT_SHORT`, or `none` (join multiple findings with `|`). Then write `activity_kit_memo.md` explaining each finding and the exempted page the standard clears.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `activity_kit_audit.csv` — Per-page print-production audit
    - `activity_kit_memo.md` — Markdown memo
    - `results.json` — a JSON object with the keys `page_count`, `flagged_count`, `dpi_low_count`, `margin_count`, `element_short_count`
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

# Task

Audit the attached seller's-book section inventory against our fair-housing compliance standard before it goes to print. Check for buyer personal-narrative content, protected-class language, and whether the required disclaimer is present — mind the standard's exception for the mandated disclosure itself. Save `fairhousing_audit.csv` with one row per section and a `finding` column using `PROHIBITED_PERSONAL_NARRATIVE`, `PROTECTED_CLASS_LANGUAGE`, `DISCLAIMER_MISSING`, or `none` (join multiple findings with `|`). Then write `fairhousing_memo.md` explaining each finding and the exempted section the standard clears.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `fairhousing_audit.csv` — Per-section fair-housing audit
    - `fairhousing_memo.md` — Markdown memo
    - `results.json` — a JSON object with the keys `section_count`, `flagged_count`, `personal_narrative_count`, `protected_lang_count`, `disclaimer_missing_count`
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

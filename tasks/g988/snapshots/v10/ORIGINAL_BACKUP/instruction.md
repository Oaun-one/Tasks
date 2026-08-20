# Task

Audit the attached composite photo-edit request log against the shop's intake rights policy INT-09 — check licensed-character use (noting its personal-use allowance), third-party background licensing, minor consent, and commercial distribution routing. Save `composite_request_audit.csv` with one row per request and a `finding` column (`UNLICENSED_CHARACTER_USE`, `THIRD_PARTY_BACKGROUND_UNLICENSED`, `MISSING_MINOR_CONSENT`, `COMMERCIAL_DISTRIBUTION_FLAG`, `none`, or a pipe-joined combination). Then write `composite_request_memo.md` explaining each finding and which request the personal-use allowance clears.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `composite_request_audit.csv` — Per-request audit
    - `composite_request_memo.md` — Markdown memo
    - `results.json` — a JSON object with the keys `request_count`, `flagged_count`, `commercial_count`, `background_count`, `compliant_count`
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

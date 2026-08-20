# Task

The festival opens Friday and the safety office wants the collateral and signage pass
finished before the walk-round. Everything is in `input/`: the collateral log, the venue
zones, the permit register, and our HLF-7 standard.

Work the log against HLF-7 and give me the per-item verdicts, the zone picture the standard
asks for, a memo I can hand to the safety officer, and the batch figures HLF-7 reports on.

Use HLF-7's own finding names, and its convention for anything that comes back clean.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `collateral_audit.csv` — per-item audit, columns `item_id` and `finding`, in that
      order and with no other columns
    - `zone_summary.csv` — per-zone rollup, columns `zone_id`, `item_count`,
      `pulled_count`, `standing_area_sqft`, `aggregate_allowance_sqft`, `allowance`, in
      that order and with no other columns
    - `collateral_memo.md` — Markdown memo for the safety office
    - `results.json` — a JSON object whose keys are the eleven figures named in HLF-7 §7,
      each a single JSON number
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

# Task

Audit the collateral log in `collateral_log.csv` against the Heritage Landing Festival collateral and signage permit standard. For each item, check its permit number, egress-marker and size compliance, applying the rules only to items classified as installed signage. Save `collateral_audit.csv` with the columns `item_id,finding`, one row per item, where `finding` is one of `PERMIT_NUMBER_MISSING`, `EGRESS_MARKER_OBSTRUCTED`, `OVERSIZE_COLLATERAL` or `none` (joined with `|` if more than one). Then write `collateral_memo.md` explaining each finding and the item that looks like a permit-number finding and is not.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `collateral_audit.csv` — Per-item festival collateral audit
    - `collateral_memo.md` — Markdown collateral audit memo
    - `results.json` — a JSON object with the keys `collateral_count`, `permit_missing_count`, `egress_obstructed_count`, `oversize_count`, `compliant_count`
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

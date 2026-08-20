# Task

Rights review meets Thursday and the composite backlog has not been cleared. Can you
work it against INT-09 and have something for me before then? Everything the shop
holds is in `input/` — the request log, the policy, the client accounts, and the
licence register.

I need the per-request verdicts, the account-level picture that INT-09 asks for, a
memo I can take into the meeting, and the batch figures the policy reports on.

Use INT-09's own finding names and its convention for anything that comes back clean.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `composite_request_audit.csv` — per-request audit, columns `request_id` and
      `finding`, in that order and with no other columns
    - `account_summary.csv` — per-account rollup, columns `account_id`,
      `account_type`, `request_count`, `flagged_requests`, `escalation`, in that
      order and with no other columns
    - `composite_request_memo.md` — Markdown memo for rights review
    - `results.json` — a JSON object whose keys are the eleven figures named in
      INT-09 §9, each a single JSON number
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

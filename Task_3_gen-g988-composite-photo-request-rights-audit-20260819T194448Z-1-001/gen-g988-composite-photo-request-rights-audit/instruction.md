# Task

The intake desk has a backlog of composite photo-edit requests and rights review
wants a full pass over the batch before any of them go into production.
Everything is in `input/`: the request log, our INT-09 intake rights policy, the
client accounts with their master agreements, and the register of licences the
shop holds.

Apply INT-09 as written. Not every row in the log is in scope, several of the
clearances live outside it — in the licence register or in the account's master
agreement — so a request is only cleared by a record that actually reaches it,
and the accounts carry a rule of their own.

Save `composite_request_audit.csv` with one row per audited request, with the
columns `request_id` and `finding`, in that order and with no other columns.
`finding` carries the code for every rule that request breaches — join multiple
codes with `|`, and use `none` for a clean request.

Save `account_summary.csv` with one row per account and the columns `account_id`,
`account_type`, `request_count`, `flagged_requests`, `escalation`, in that order
and with no other columns, using the same `none` convention in `escalation` for
an account that stays with the intake desk.

Then write `composite_request_memo.md` for rights review. State the date the
audit is made as of. Say which requests the policy takes out of the audit and
why. Account for every request carrying a finding, naming the code and the record
that decides it — the licence id, the consent, or the account agreement. Where a
request looks like a breach and the policy clears it, say what clears it, and
name every request whose licensed-character use the personal-use allowance
clears. Name the accounts whose master agreement has lapsed and say what that
changes. And name the accounts that escalate, giving the batch-wide figure you
measured them against and the reason each one escalates.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `composite_request_audit.csv` — Per-request rights audit
    - `account_summary.csv` — Per-account rollup
    - `composite_request_memo.md` — Markdown memo for rights review
    - `results.json` — a JSON object with the keys `request_count` (audited
      requests), `account_count`, `flagged_count` (audited requests carrying at
      least one finding), `compliant_count`, `finding_total` (every finding
      raised across the batch, not the number of requests carrying one),
      `character_count`, `background_count`, `consent_count`, `commercial_count`,
      `disclosure_count` (each of these five counting the requests carrying that
      finding) and `escalated_accounts` (how many accounts escalate, not which).
      Every one of these is a single JSON number.
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

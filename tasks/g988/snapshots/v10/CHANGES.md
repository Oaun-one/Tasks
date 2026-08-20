# CHANGES — gen-g988-composite-photo-request-rights-audit

Cumulative record of every edit made to the shipped package, and why.
Cold read and the pre-change analysis are in `COLD_READ.md`.

## Why the task needed hardening

The task as generated is 8 requests × 4 independent single-column rules over 2 files.
Each rule reads exactly one column whose name is the finding it produces
(`uses_licensed_character` → `UNLICENSED_CHARACTER_USE`), the rules never interact, and
both the prompt and the policy name the one trap in advance — the prompt says "noting its
personal-use allowance" and asks "which request the personal-use allowance clears", and
the policy adds "flagging a personal, non-distributed request … is the commonest false
positive". There is no reasoning step available to get wrong.

The grader was worse than the fixture. `evidence_coverage_gap/` reproduces it: **the
original 13 verifiers score a full 13/13 on an answer that is wrong on 7 of its 8 rows.**
Only 4 of 8 requests are checked at all, every row check is a bare `.*CODE` presence regex
with no negative lookahead, so writing every code on every row passes, and `memo_trap` is
satisfied by echoing the prompt's own phrase next to `REQ-01`.

## What changed

### `environment/input/` — the fixture (hardening lever #2)

Confirmed editable for gen tasks. The topic, the scenario and `task.toml` are unchanged:
this is still a composite photo-edit request rights audit against intake policy INT-09.

- **`composite_request_log.csv` — 8 requests → 32, across 8 client accounts.** 13 columns
  instead of 6. The columns are no longer verdicts in disguise: `character_license_id`,
  `background_license_id`, `intended_distribution`, `minor_consent_type` /
  `minor_consent_valid_until`, `alteration_level` / `alteration_disclosure_on_file`.
- **`client_accounts.csv` — new.** Each account's `account_type`,
  `master_agreement_covers` and `agreement_status`.
- **`licensed_property_register.csv` — new.** The 8 licences the shop holds, with
  `license_type`, `covers_distribution` and `valid_until`.
- **`intake_rights_policy.md` — rewritten as INT-09 rev 4.** Same four original rules,
  restated so their thresholds live outside the request row, plus §2 (a single shared
  definition of when a licence covers a request), §7 (alteration disclosure) and §8
  (account escalation). The "commonest false positive" hint is kept — it is a real
  auditing note and it no longer gives the answer away, because the allowance is now one
  of two independent clearances and its scope is the thing being tested.

### The five things that make it hard

Stacking more independent rules does not work — that is recorded in the runbook and was
re-confirmed on g780. Every lever below is a *coupling*.

1. **Cross-source resolution.** A request reaches its clearance only through another file:
   character and background use through `licensed_property_register.csv`, routing through
   the account's agreement in `client_accounts.csv`. Not one verdict can be read off the
   request row.
2. **A licence is not a boolean.** §2 makes a licence cover a request only when the id
   resolves, the `license_type` matches the use, `covers_distribution` names the request's
   own distribution, and `valid_until` is on or after the audit date. REQ-09 and REQ-10
   run the same property under the same licence and get opposite verdicts, on scope alone.
3. **Inclusive boundaries, on a fixed audit date.** The audit is as of 2026-03-31.
   LIC-102 expires that day and still covers; LIC-103 expired 2026-03-30 and does not.
   Consent dates work the same way (REQ-11 and REQ-28 sit exactly on the date). Reading
   the boundary as exclusive moves 4 rows.
4. **An exception with a stated scope.** The personal-use allowance releases §3 and
   nothing else — REQ-04 and REQ-19 are personal-only and still carry a background
   finding, REQ-32 is personal-only and still carries a consent finding. Reading it as a
   general pardon moves 4 rows. `client_internal` is explicitly not personal use, which
   is what REQ-21 turns on against its twin REQ-22.
5. **A rollup over the model's own results.** §8 escalates an account on two or more
   flagged requests *or* any single request carrying three or more. It cannot be computed
   until the audit is finished, and one wrong row moves the account row, the
   `escalated_accounts` figure and several counts with it. ACC-02 (one flagged request,
   four findings → escalates) and ACC-03 (one flagged request, two findings → does not)
   separate the two limbs.

Scale: 32 requests × 5 request-level rules = 160 comparisons, plus 8 account rollups.
16 requests carry a finding and 16 are clean, so neither over- nor under-flagging is a
cheap strategy.

### Leakage removed from `instruction.md`

- Dropped "noting its personal-use allowance" and "which request the personal-use
  allowance clears". The singular *request* had also told the model that exactly one row
  turns on it. The memo is still graded on the allowance, but the model has to find the
  rows: the prompt now asks it to "name every request whose licensed-character use the
  personal-use allowance clears", and the answer is three rows, not one.
- Dropped the per-rule recipe ("check licensed-character use …, third-party background
  licensing, minor consent, and commercial distribution routing"), which was a worked
  checklist of the policy sections. Replaced with the scenario and one sentence saying the
  clearances live outside the log.
- The finding vocabulary is no longer repeated in the prompt; it is in the policy, once.

### `tests/verifier.json` — 13 verifiers → 80

Regenerated by `tools/g988_emit.py` from the same computation that produces the gold, so
the two cannot drift.

| | original | now |
| --- | --- | --- |
| requests with a row-level assertion | 4 of 8 | **32 of 32** |
| row assertions that reject over-flagging | 0 | **32** |
| account rollup assertions | – | 25 |
| `results.json` figures | 5 | 11 |
| memo assertions | 1 | 7 |

Every row assertion is an **exact-set** check: a positive lookahead for each code the row
must carry and a negative lookahead for each of the five it must not. `none` is accepted
in any of the usual spellings. Assertions are line-scoped and order-free, so a correct
answer passes with the codes in any order, with quoted fields, and in any case.

The memo checks grade the artifact, not a self-report: every one of the 16 flagged
requests named, all five codes explained, the audit date stated, the three allowance rows
named, the two lapsed accounts named, the six escalating accounts named, and the two
register licences that lapsed before the audit date cited by id.

### `environment/Dockerfile`

Base image pinned by digest —
`python:3.12-slim-bookworm@sha256:a116514e19457bcb7af7efe9c3dd0b9b71e85b317694e7882a1c52aa15a78134`
(Delivery Gate S1, blocking). Nothing else changed.

### `solution/`

`solution/files/` regenerated: `composite_request_audit.csv` (32 rows),
`account_summary.csv` (new, 8 rows), `composite_request_memo.md` and `results.json`.
`solve.sh` is unchanged — it still installs `solution/files/` into the workspace.

### Not changed

`task.toml` (name, description, keywords, `source_config` all untouched),
`tests/test.sh`, `tests/test_outputs.py`, `tests/rl_world_verifiers/`.

## Verification

| check | result |
| --- | --- |
| Engine replayed over the gold, locally | **80 / 80 pass** |
| Oracle (`harbor run --agent oracle`) | **Trials 1 / Exceptions 0 / Mean 1.000** |
| Original spec vs. an answer wrong on 7 of 8 rows | 13 / 13 — the gap being fixed |
| Hardened spec vs. "never opens the licence register" | 14 rows wrong → 51 / 80 |
| Hardened spec vs. "allowance as a general pardon" | 4 rows wrong → 65 / 80 |
| Hardened spec vs. "validity dates read as exclusive" | 4 rows wrong → 66 / 80 |
| Hardened spec vs. "routing cleared by `account_type`" | 6 rows wrong → 67 / 80 |
| Hardened spec vs. "disclosure skipped on a pre-cleared channel" | **1 row wrong → 77 / 80** |

The last line is the one that matters: a single misread row costs the run. Reward is
binary, so each of these scores 0.0 while still showing a steady partial signal in CTRF.

Reproduce with `python tools/g988_negative_check.py`
(`evidence_coverage_gap/negative_check_output.txt` is the saved output).

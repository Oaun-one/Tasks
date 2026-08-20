# Guidance on record

## Vahid H. (Delivery Manager), Slack, 2:06-2:07 PM

> don't drop the row
>
> usually you get 5/5 you should make the task harder no task will be initially not 5/5
>
> If the task is hopeless mark it as too easy
>
> You can edit and give us something that is harbor executable

### What this settles

1. **Do not drop the row.** The discard path in ESCALATION.md is void.
2. **5/5 on the first battery is expected**, not a defect. Matches the onboarding doc:
   "Expect your first GLM battery to pass 5/5. That is normal. Hardening it is the actual
   job, not a sign something went wrong."
3. **The fallback is "mark it as too easy", not discard.** Different outcome, same row.
4. **Editing is permitted**, with one binding constraint: the package must stay
   **harbor executable**. Oracle 1.0 is the test of that, and it is green after every
   change so far.

### Still unanswered

The explicit question — *is `environment/input/` editable on ComputerBench NonConnector gen
tasks?* — has not been answered directly yet. Proceeding on:

- "You can edit and give us something that is harbor executable" (no carve-out stated)
- Onboarding doc's lever order: `instruction.md` -> **input data (add edge density)** ->
  `tests/manifest.json`
- These gen tasks ship fixtures inside the package, so an edit affects only this task. The
  Playbook's "seed data is not editable" rule concerns CompanyBench's shared base image.

**Reversibility:** every fixture edit is documented in CHANGES.md and the untouched original
is at `ORIGINAL_BACKUP/`. If the answer comes back "no", reverting is one copy command and
only the fixture edits are lost - the verifier fixes stand either way.

## Band, per the onboarding doc

ComputerBench: **at most 3 of 5 runs may fully pass (<= 3/5)**. This overrides the 1/5-2/5
band in the older Task Playbook, which still applies to CompanyBench. 0/5 with steady
partial rewards (0.15-0.35) is explicitly "what good looks like".

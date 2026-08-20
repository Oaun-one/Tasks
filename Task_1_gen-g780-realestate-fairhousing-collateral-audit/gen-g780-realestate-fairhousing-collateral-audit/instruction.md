# Task

The seller's book goes to print Friday and legal want the fair-housing pass signed off
before it does. The section inventory and our compliance standard RE-FH-9 are both in
`input/`. Work from the standard rather than from memory — it was amended this year and the
book has not entirely caught up.

Give me `fairhousing_audit.csv`: two columns, `section_id` and `finding`, one row per
section in inventory order, with a header. `finding` is `PROHIBITED_PERSONAL_NARRATIVE`,
`PROTECTED_CLASS_LANGUAGE`, `DISCLAIMER_MISSING` or `none`, and where a section trips more
than one rule join the labels with `|` in that same order. Nothing else in that file
please — the print vendor's importer takes the two columns and chokes on anything more.

Then `fairhousing_memo.md` explaining what you found and why, with enough reasoning that
legal can sign off without re-reading RE-FH-9 themselves.

And `results.json` for the sign-off form. Count sections, not labels:

- `section_count` — sections in the inventory
- `flagged_count` — sections whose `finding` is not `none`
- `personal_narrative_count`, `protected_lang_count`, `disclaimer_missing_count` — sections
  whose `finding` includes that label

---

Save all three into your current working directory, at exactly those filenames. Writing them
is the deliverable; confirm each exists before you answer. Your working directory is
writable and the read-only attachments are in `input/`.

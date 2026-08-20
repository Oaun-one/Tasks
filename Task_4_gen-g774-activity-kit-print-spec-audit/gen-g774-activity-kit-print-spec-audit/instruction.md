# Task

The activity kit goes to the printer on Friday and I need a pre-flight pass over the
batch before it does. Everything is in `input/`: the artwork batch, the section list
saying how each section is bound and which stock it runs on, the stock profiles, and
our PRINT-KIT-2 standard.

Apply the standard as written. Most of the limits belong to the paper stock rather than
to the kit, parts of the batch have been re-supplied since the first drop, and the
standard carries an amendment — each of those changes which pages are actually in
breach.

Save `activity_kit_audit.csv` with one row per audited page, keyed by `page_id`, and a
`finding` column carrying the code for every rule that page breaches — join multiple
codes with `|`, and use `none` for a page that breaches nothing.

Then write `activity_kit_memo.md` for the studio. Account for every page carrying a
finding, naming the measured value and the limit it missed. Where a page's numbers look
like a breach but the standard clears it, say what clears it. And say which artwork the
batch supersedes, and what that changes.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `activity_kit_audit.csv` — Per-page print-production audit
    - `activity_kit_memo.md` — Markdown memo
    - `results.json` — a JSON object with the keys `page_count` (pages audited),
      `superseded_count` (artwork rows the batch supersedes), `clean_count`,
      `flagged_count`, `finding_total` (every finding raised across the batch, not the
      number of pages carrying one), `dpi_low_count`, `margin_count`,
      `bleed_short_count`, `ink_over_count`, `element_short_count` (each of these five
      counting the pages carrying that finding) and `element_shortfall_total` (how many
      required elements the batch is missing in total)
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

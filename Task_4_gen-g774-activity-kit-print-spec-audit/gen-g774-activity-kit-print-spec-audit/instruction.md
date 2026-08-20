# Task

The activity kit goes to the printer on Friday and I need a pre-flight pass over the
batch before it does. Everything is in `input/`: the artwork batch, the section list
saying how each section is bound and which stock it runs on, the stock profiles, and
our PRINT-KIT-2 standard.

Apply the standard as written. Most of the limits belong to the paper stock rather than
to the kit, parts of the batch have been re-supplied since the first drop, and the
standard carries an amendment — each of those changes which pages are actually in
breach. The sections carry a rule of their own, and it reads the page audit.

Save `activity_kit_audit.csv` with one row per audited page, keyed by `page_id`, and a
`finding` column carrying the code for every rule that page breaches — join multiple
codes with `|`, and use `none` for a page that breaches nothing.

Save `section_summary.csv` with one row per section and the columns `section_id`,
`binding`, `stock_code`, `live_page_count`, `held_back`, `imposed_page_count`,
`flagged_pages`, `imposition`, in that order, using the same `none` convention in
`imposition` for a section that imposes cleanly.

Then write `activity_kit_memo.md` for the studio. Account for every page carrying a
finding, naming the measured value and the limit it missed. Where a page's numbers look
like a breach but the standard clears it, say what clears it. Say which artwork the
batch supersedes and what that changes. Give me the limits you actually applied — the
stocks in this kit and their resolution floors, ink caps, margin floors and bleed
minimums. Cover every section, and name the ones that cannot be imposed with the number
of pages each of them needs. And state the batch totals: how many pages are clear, how
many carry a finding, and how many required elements the batch is missing altogether.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `activity_kit_audit.csv` — Per-page print-production audit
    - `section_summary.csv` — Per-section rollup
    - `activity_kit_memo.md` — Markdown memo for the studio
    - `results.json` — a JSON object with the keys `page_count` (pages audited),
      `superseded_count` (artwork rows the batch supersedes), `section_count`,
      `clean_count`, `flagged_count`, `finding_total` (every finding raised across the
      batch, not the number of pages carrying one), `dpi_low_count`, `margin_count`,
      `bleed_short_count`, `ink_over_count`, `element_short_count` (each of these five
      counting the pages carrying that finding), `element_shortfall_total` (how many
      required elements the batch is missing in total), `imposition_invalid_sections`
      and `imposition_shortfall_total` (how many pages those sections need between them)
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

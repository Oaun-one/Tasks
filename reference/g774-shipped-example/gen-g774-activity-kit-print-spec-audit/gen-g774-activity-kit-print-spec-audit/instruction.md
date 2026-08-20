# Task

The activity kit goes to press on Friday and I need a full pre-flight pass over
the batch before it does. Everything is in `input/`: the page batch, the section
plan naming the press each section runs on, the press profiles, and our
PRINT-KIT-3 standard.

Apply the standard as written. Several limits are per-press, so a page is only in
breach against the press that is actually going to print it, and the sections
carry a rule of their own.

Save `preflight_audit.csv` with one row per page, keyed by `page_id`, and a
`finding` column carrying the code for every rule that page breaches — join
multiple codes with `|`, and use `none` for a clean page.

Save `section_summary.csv` with one row per section and the columns
`section_id`, `press_id`, `page_count`, `flagged_pages`, `imposition`, in that
order, using the same `none` convention in `imposition` for a section that
imposes cleanly.

Then write `preflight_memo.md` for the studio. Account for every page carrying a
finding, naming the measured value and the limit it missed. Where a page's
numbers look like a breach but the standard clears it, say what clears it. Call
out the pages whose verdict turns on which press they are assigned to. And name
the sections that cannot be imposed as planned, with the page count they need.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `preflight_audit.csv` — Per-page pre-flight audit
    - `section_summary.csv` — Per-section rollup
    - `preflight_memo.md` — Markdown memo for the studio
    - `results.json` — a JSON object with the keys `page_count`, `section_count`,
      `clean_page_count`, `flagged_page_count`, `finding_total` (every finding
      raised across the batch, not the number of pages carrying one),
      `dpi_low_count`, `margin_count`, `bleed_short_count`, `ink_over_count`,
      `spot_unsupported_count`, `font_not_embedded_count`, `element_short_count`
      (each of these seven counting the pages carrying that finding),
      `element_shortfall_total` (how many required elements the batch is missing
      in total) and `imposition_invalid_sections`
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.

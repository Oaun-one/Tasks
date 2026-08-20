# Gold answer — activity-kit print pre-flight audit

36 pages in 9 sections, graded against `input/print_production_standard.md`
(PRINT-KIT-3), with the per-press limits in `input/press_profiles.csv` and the
press assignments in `input/section_plan.csv`.

The audit cannot be done page by page in isolation. Two of the seven page rules
take their threshold from the press the page's **section** is assigned to, so
every page needs a two-hop join (page → section → press) before any comparison
is meaningful, and one rule is a property of the section rather than the page.

## Rule reading

| Rule | Code | Test | Boundary / scope |
|---|---|---|---|
| §2 Effective resolution | `DPI_TOO_LOW` | `floor(artwork_dpi × 100 / placed_scale_pct) < press.min_effective_dpi` | Equal to the floor passes. The comparison is on the **effective** dpi, not the artwork dpi. Floor is 300 on `PRESS-OFFSET-A`, 250 on `PRESS-DIGITAL-B`. |
| §3 Safe margin | `MARGIN_VIOLATION` | `margin_in < 0.125` | Equal passes. **Does not apply** to a full-bleed page. |
| §4 Bleed | `BLEED_SHORT` | `bleed_in < 0.125` | Equal passes. **Applies only** to a full-bleed page. |
| §5 Ink coverage | `INK_OVER_LIMIT` | `ink_tac_pct > press.max_tac_pct` | Equal passes. Cap is 300% offset, 280% digital. |
| §6 Spot colours | `SPOT_UNSUPPORTED` | `spot_colors > press.max_spot_colors` | Cap is 2 offset, 0 digital — the digital press cannot run any spot ink. |
| §7 Fonts | `FONT_NOT_EMBEDDED` | `fonts_embedded is not true` | Press-independent. |
| §8 Required elements | `ELEMENT_COUNT_SHORT` | `element_count < min_element_required` | Equal is complete, not short. |
| §9 Imposition | `IMPOSITION_INVALID` | section page count not a multiple of 4 (`saddle_stitch`) or 2 (`perfect_bound`) | `flat_sheet` is unconstrained. Section-level; not a finding against any page. |

§3 and §4 are a matched pair and the commonest place to go wrong in both
directions: being a full-bleed design releases a page from the margin rule **and
obliges it to carry bleed**. Reading the exception as a blanket pass clears
PG-02, PG-03, PG-22 and PG-35 wrongly; applying the margin rule to full-bleed
pages anyway wrongly flags PG-01, PG-21, PG-29 and PG-34.

## Per-page result

| Page | Sec | Press | dpi @ scale = eff | margin | bleed | full bleed | TAC | spot | fonts | elem | Finding |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PG-01 | SEC-01 | OFFSET-A | 360 @ 120% = 300 | 0.05 | 0.125 | yes | 285% | 2 | yes | 3/3 | `none` |
| PG-02 | SEC-01 | OFFSET-A | 300 @ 100% = 300 | 0.05 | 0.0625 | yes | 240% | 0 | yes | 2/2 | `BLEED_SHORT` |
| PG-03 | SEC-01 | OFFSET-A | 450 @ 200% = 225 | 0.2 | 0.0 | yes | 260% | 0 | yes | 2/2 | `DPI_TOO_LOW|BLEED_SHORT` |
| PG-04 | SEC-01 | OFFSET-A | 240 @ 80% = 300 | 0.125 | 0.0 | no | 300% | 0 | yes | 1/1 | `none` |
| PG-05 | SEC-02 | DIGITAL-B | 200 @ 80% = 250 | 0.2 | 0.0 | no | 275% | 0 | yes | 4/4 | `none` |
| PG-06 | SEC-02 | DIGITAL-B | 270 @ 100% = 270 | 0.2 | 0.0 | no | 270% | 0 | yes | 5/5 | `none` |
| PG-07 | SEC-02 | DIGITAL-B | 270 @ 120% = 225 | 0.2 | 0.0 | no | 260% | 1 | yes | 3/3 | `DPI_TOO_LOW|SPOT_UNSUPPORTED` |
| PG-08 | SEC-02 | DIGITAL-B | 300 @ 100% = 300 | 0.1 | 0.125 | no | 290% | 0 | NO | 2/4 | `MARGIN_VIOLATION|INK_OVER_LIMIT|FONT_NOT_EMBEDDED|ELEMENT_COUNT_SHORT` |
| PG-09 | SEC-03 | OFFSET-A | 600 @ 200% = 300 | 0.3 | 0.0 | no | 250% | 1 | yes | 6/6 | `none` |
| PG-10 | SEC-03 | OFFSET-A | 270 @ 100% = 270 | 0.3 | 0.0 | no | 250% | 0 | yes | 6/6 | `DPI_TOO_LOW` |
| PG-11 | SEC-03 | OFFSET-A | 300 @ 100% = 300 | 0.06 | 0.25 | yes | 310% | 0 | yes | 4/4 | `INK_OVER_LIMIT` |
| PG-12 | SEC-03 | OFFSET-A | 300 @ 100% = 300 | 0.09 | 0.0 | no | 260% | 3 | yes | 5/5 | `MARGIN_VIOLATION|SPOT_UNSUPPORTED` |
| PG-13 | SEC-03 | OFFSET-A | 450 @ 150% = 300 | 0.2 | 0.0 | no | 300% | 2 | yes | 7/7 | `none` |
| PG-14 | SEC-03 | OFFSET-A | 240 @ 120% = 200 | 0.2 | 0.0 | no | 260% | 0 | NO | 3/5 | `DPI_TOO_LOW|FONT_NOT_EMBEDDED|ELEMENT_COUNT_SHORT` |
| PG-15 | SEC-04 | DIGITAL-B | 250 @ 100% = 250 | 0.15 | 0.0 | no | 280% | 0 | yes | 8/8 | `none` |
| PG-16 | SEC-04 | DIGITAL-B | 300 @ 120% = 250 | 0.2 | 0.0 | no | 260% | 0 | yes | 8/8 | `none` |
| PG-17 | SEC-04 | DIGITAL-B | 240 @ 100% = 240 | 0.2 | 0.0 | no | 260% | 0 | yes | 8/8 | `DPI_TOO_LOW` |
| PG-18 | SEC-04 | DIGITAL-B | 300 @ 100% = 300 | 0.2 | 0.0 | no | 281% | 0 | yes | 8/8 | `INK_OVER_LIMIT` |
| PG-19 | SEC-04 | DIGITAL-B | 300 @ 100% = 300 | 0.2 | 0.0 | no | 260% | 2 | yes | 6/8 | `SPOT_UNSUPPORTED|ELEMENT_COUNT_SHORT` |
| PG-20 | SEC-05 | OFFSET-A | 300 @ 100% = 300 | 0.125 | 0.0 | no | 300% | 2 | yes | 9/9 | `none` |
| PG-21 | SEC-05 | OFFSET-A | 300 @ 100% = 300 | 0.0 | 0.125 | yes | 260% | 0 | yes | 9/9 | `none` |
| PG-22 | SEC-05 | OFFSET-A | 300 @ 100% = 300 | 0.0 | 0.1 | yes | 260% | 0 | yes | 9/9 | `BLEED_SHORT` |
| PG-23 | SEC-05 | OFFSET-A | 300 @ 100% = 300 | 0.124 | 0.0 | no | 260% | 0 | yes | 9/9 | `MARGIN_VIOLATION` |
| PG-24 | SEC-06 | DIGITAL-B | 300 @ 100% = 300 | 0.2 | 0.0 | no | 275% | 0 | yes | 12/12 | `none` |
| PG-25 | SEC-06 | DIGITAL-B | 200 @ 100% = 200 | 0.05 | 0.0 | no | 300% | 1 | NO | 3/4 | `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER_LIMIT|SPOT_UNSUPPORTED|FONT_NOT_EMBEDDED|ELEMENT_COUNT_SHORT` |
| PG-26 | SEC-06 | DIGITAL-B | 255 @ 100% = 255 | 0.13 | 0.0 | no | 279% | 0 | yes | 4/4 | `none` |
| PG-27 | SEC-07 | OFFSET-A | 300 @ 100% = 300 | 0.2 | 0.0 | no | 260% | 0 | yes | 2/2 | `none` |
| PG-28 | SEC-07 | OFFSET-A | 300 @ 150% = 200 | 0.2 | 0.0 | no | 260% | 0 | yes | 2/2 | `DPI_TOO_LOW` |
| PG-29 | SEC-07 | OFFSET-A | 360 @ 120% = 300 | 0.04 | 0.5 | yes | 260% | 0 | NO | 2/2 | `FONT_NOT_EMBEDDED` |
| PG-30 | SEC-07 | OFFSET-A | 300 @ 100% = 300 | 0.2 | 0.0 | no | 260% | 0 | yes | 0/2 | `ELEMENT_COUNT_SHORT` |
| PG-31 | SEC-08 | DIGITAL-B | 250 @ 100% = 250 | 0.2 | 0.0 | no | 280% | 0 | yes | 5/5 | `none` |
| PG-32 | SEC-08 | DIGITAL-B | 225 @ 100% = 225 | 0.11 | 0.0 | no | 285% | 0 | yes | 5/5 | `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER_LIMIT` |
| PG-33 | SEC-08 | DIGITAL-B | 300 @ 100% = 300 | 0.2 | 0.0 | no | 260% | 3 | yes | 4/6 | `SPOT_UNSUPPORTED|ELEMENT_COUNT_SHORT` |
| PG-34 | SEC-09 | OFFSET-A | 240 @ 80% = 300 | 0.02 | 0.125 | yes | 300% | 2 | yes | 20/20 | `none` |
| PG-35 | SEC-09 | OFFSET-A | 300 @ 100% = 300 | 0.02 | 0.08 | yes | 260% | 0 | yes | 20/20 | `BLEED_SHORT` |
| PG-36 | SEC-09 | OFFSET-A | 300 @ 100% = 300 | 0.2 | 0.25 | no | 301% | 0 | yes | 19/20 | `INK_OVER_LIMIT|ELEMENT_COUNT_SHORT` |

## Section rollup (`section_summary.csv`)

| section_id | press_id | page_count | flagged_pages | imposition |
|---|---|---|---|---|
| SEC-01 | PRESS-OFFSET-A | 4 | 2 | none |
| SEC-02 | PRESS-DIGITAL-B | 4 | 2 | none |
| SEC-03 | PRESS-OFFSET-A | 6 | 4 | `IMPOSITION_INVALID` |
| SEC-04 | PRESS-DIGITAL-B | 5 | 3 | none |
| SEC-05 | PRESS-OFFSET-A | 4 | 2 | none |
| SEC-06 | PRESS-DIGITAL-B | 3 | 1 | none |
| SEC-07 | PRESS-OFFSET-A | 4 | 3 | none |
| SEC-08 | PRESS-DIGITAL-B | 3 | 2 | `IMPOSITION_INVALID`|
| SEC-09 | PRESS-OFFSET-A | 3 | 2 | none |

SEC-03 is saddle-stitched with 6 pages and needs a multiple of 4, so it goes to
8. SEC-08 is perfect-bound with 3 pages and needs a multiple of 2, so it goes
to 4. SEC-04 (5 pages) and SEC-09 (3 pages) are odd counts too, but they are
`flat_sheet` and §9 does not constrain them — flagging those is the standard
over-application of this rule.

## Derived figures (`results.json`)

```json
{
  "page_count": 36,
  "section_count": 9,
  "clean_page_count": 15,
  "flagged_page_count": 21,
  "finding_total": 39,
  "dpi_low_count": 8,
  "margin_count": 5,
  "bleed_short_count": 4,
  "ink_over_count": 6,
  "spot_unsupported_count": 5,
  "font_not_embedded_count": 4,
  "element_short_count": 7,
  "element_shortfall_total": 12,
  "imposition_invalid_sections": 2
}
```

`flagged_page_count` is 21 pages while `finding_total` is 39 findings: six pages
breach more than one rule and PG-25 breaches six at once. `element_shortfall_total`
counts missing elements (12), not the 7 pages missing them.

## Where a wrong answer comes from

Each of these is a single defensible-looking premise that produces a
self-consistent wrong audit, and every one is reachable from this fixture:

1. **One studio-wide 300 dpi floor.** Ignoring `min_effective_dpi` per press
   wrongly flags PG-05, PG-06, PG-15, PG-16, PG-26 and PG-31 — six pages that
   are correct on the digital press. PG-06 and PG-10 are the proof pair: both
   land at 270 dpi effective, and only PG-10 (offset) is a finding.
2. **Comparing `artwork_dpi` instead of the effective dpi.** PG-03 (450 dpi at
   200%) and PG-28 (300 dpi at 150%) look generous and are both short; PG-04,
   PG-05 and PG-34 look thin and are all fine once the placed scale is applied.
3. **Reading §3's full-bleed exception as a general pass.** It releases the page
   from the safe-margin rule only. §4 then *obliges* that same page to carry
   bleed, which PG-02, PG-03, PG-22 and PG-35 do not.
4. **Applying §4 to every page.** Most non-full-bleed pages carry 0 bleed by
   design; flagging them adds 17 false findings.
5. **Reading a limit as exclusive.** Fifteen pages sit exactly on at least one
   limit — 300 dpi effective, 0.125 in margin, 300% or 280% coverage, 2 spot
   colours, or exactly the element minimum. Using `<=` anywhere floods the audit.
6. **A global spot-colour cap of 2.** The digital press carries none, so PG-07,
   PG-19 and PG-25 are findings that a 2-colour assumption clears.
7. **Imposing §9 on flat-sheet sections.** SEC-04, SEC-06 and SEC-09 have page
   counts that are not multiples of 4, and are not bound.
8. **Counting pages where the ask is findings or elements.** `finding_total` is
   39, not the 21 pages carrying findings; `element_shortfall_total` is 12, not
   the 7 pages that are short.

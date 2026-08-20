# Pre-flight audit — activity kit, PRINT-KIT-3

36 pages across 9 sections, checked against PRINT-KIT-3 before the run. 15 pages are clear and 21 carry at least one finding, 39 findings in all. The batch is 12 required elements short across every page that is missing any, and 2 sections cannot be imposed as they stand.

## Limits applied

| Press | Min effective dpi (§2) | Max coverage (§5) | Spot colours (§6) |
| --- | --- | --- | --- |
| PRESS-OFFSET-A | 300 | 300% | 2 |
| PRESS-DIGITAL-B | 250 | 280% | 0 |

Studio-wide, independent of press: safe margin at least 0.125 in (§3, waived for full-bleed designs), bleed at least 0.125 in on a full-bleed design (§4), fonts embedded (§7), and each page at or above its own element minimum (§8).

## Sections

| Section | Press | Binding | Pages | Flagged | Imposition |
| --- | --- | --- | --- | --- | --- |
| SEC-01 Covers | PRESS-OFFSET-A | flat_sheet | 4 | 2 | none |
| SEC-02 Parent Guide | PRESS-DIGITAL-B | saddle_stitch | 4 | 2 | none |
| SEC-03 Explorer Maps | PRESS-OFFSET-A | saddle_stitch | 6 | 4 | IMPOSITION_INVALID |
| SEC-04 Mission Cards | PRESS-DIGITAL-B | flat_sheet | 5 | 3 | none |
| SEC-05 Station Bingo | PRESS-OFFSET-A | perfect_bound | 4 | 2 | none |
| SEC-06 Badges | PRESS-DIGITAL-B | flat_sheet | 3 | 1 | none |
| SEC-07 Certificates | PRESS-OFFSET-A | saddle_stitch | 4 | 3 | none |
| SEC-08 Activity Sheets | PRESS-DIGITAL-B | perfect_bound | 3 | 2 | IMPOSITION_INVALID |
| SEC-09 Sticker Sheets | PRESS-OFFSET-A | flat_sheet | 3 | 2 | none |

### Sections that cannot be imposed as planned

- **SEC-03 Explorer Maps** is saddle_stitch and carries 6 pages. §9 needs a page count that is a multiple of 4 for that binding, so the section has to go to 8 pages before it can be imposed. `IMPOSITION_INVALID`.
- **SEC-08 Activity Sheets** is perfect_bound and carries 3 pages. §9 needs a page count that is a multiple of 2 for that binding, so the section has to go to 4 pages before it can be imposed. `IMPOSITION_INVALID`.

## Pages carrying findings

### PG-02 — Inside Front Cover (SEC-01, PRESS-OFFSET-A): `BLEED_SHORT`

It is a full-bleed design carrying 0.0625 in of bleed, under the 0.125 in minimum §4 requires of a full-bleed page. Being full-bleed releases it from the safe-margin rule, not from bleed.

### PG-03 — Back Cover (SEC-01, PRESS-OFFSET-A): `DPI_TOO_LOW|BLEED_SHORT`

Artwork is 450 dpi placed at 200%, which lands at 225 dpi effective — under the 300 dpi floor for PRESS-OFFSET-A (§2).
It is a full-bleed design carrying 0.0 in of bleed, under the 0.125 in minimum §4 requires of a full-bleed page. Being full-bleed releases it from the safe-margin rule, not from bleed.

### PG-07 — Safety Notes (SEC-02, PRESS-DIGITAL-B): `DPI_TOO_LOW|SPOT_UNSUPPORTED`

Artwork is 270 dpi placed at 120%, which lands at 225 dpi effective — under the 250 dpi floor for PRESS-DIGITAL-B (§2).
It specifies 1 spot colour(s); PRESS-DIGITAL-B carries 0 (§6).

### PG-08 — Supply Checklist (SEC-02, PRESS-DIGITAL-B): `MARGIN_VIOLATION|INK_OVER_LIMIT|FONT_NOT_EMBEDDED|ELEMENT_COUNT_SHORT`

Safe margin measures 0.1 in, under the 0.125 in floor (§3), and the page is not a full-bleed design, so the §3 exception does not reach it.
Total area coverage is 290%, over the 280% cap for PRESS-DIGITAL-B (§5).
Fonts are not embedded (§7).
Carries 2 of the 4 required elements (§8) — 2 short.

### PG-10 — Trail Map South (SEC-03, PRESS-OFFSET-A): `DPI_TOO_LOW`

Artwork is 270 dpi placed at 100%, which lands at 270 dpi effective — under the 300 dpi floor for PRESS-OFFSET-A (§2).

### PG-11 — Habitat Spread (SEC-03, PRESS-OFFSET-A): `INK_OVER_LIMIT`

Total area coverage is 310%, over the 300% cap for PRESS-OFFSET-A (§5).

### PG-12 — Landmark Key (SEC-03, PRESS-OFFSET-A): `MARGIN_VIOLATION|SPOT_UNSUPPORTED`

Safe margin measures 0.09 in, under the 0.125 in floor (§3), and the page is not a full-bleed design, so the §3 exception does not reach it.
It specifies 3 spot colour(s); PRESS-OFFSET-A carries 2 (§6).

### PG-14 — Field Notes Page (SEC-03, PRESS-OFFSET-A): `DPI_TOO_LOW|FONT_NOT_EMBEDDED|ELEMENT_COUNT_SHORT`

Artwork is 240 dpi placed at 120%, which lands at 200 dpi effective — under the 300 dpi floor for PRESS-OFFSET-A (§2).
Fonts are not embedded (§7).
Carries 3 of the 5 required elements (§8) — 2 short.

### PG-17 — Mission Card C (SEC-04, PRESS-DIGITAL-B): `DPI_TOO_LOW`

Artwork is 240 dpi placed at 100%, which lands at 240 dpi effective — under the 250 dpi floor for PRESS-DIGITAL-B (§2).

### PG-18 — Mission Card D (SEC-04, PRESS-DIGITAL-B): `INK_OVER_LIMIT`

Total area coverage is 281%, over the 280% cap for PRESS-DIGITAL-B (§5).

### PG-19 — Mission Card E (SEC-04, PRESS-DIGITAL-B): `SPOT_UNSUPPORTED|ELEMENT_COUNT_SHORT`

It specifies 2 spot colour(s); PRESS-DIGITAL-B carries 0 (§6).
Carries 6 of the 8 required elements (§8) — 2 short.

### PG-22 — Bingo Grid Three (SEC-05, PRESS-OFFSET-A): `BLEED_SHORT`

It is a full-bleed design carrying 0.1 in of bleed, under the 0.125 in minimum §4 requires of a full-bleed page. Being full-bleed releases it from the safe-margin rule, not from bleed.

### PG-23 — Bingo Call Sheet (SEC-05, PRESS-OFFSET-A): `MARGIN_VIOLATION`

Safe margin measures 0.124 in, under the 0.125 in floor (§3), and the page is not a full-bleed design, so the §3 exception does not reach it.

### PG-25 — Badge Sheet Two (SEC-06, PRESS-DIGITAL-B): `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER_LIMIT|SPOT_UNSUPPORTED|FONT_NOT_EMBEDDED|ELEMENT_COUNT_SHORT`

Artwork is 200 dpi placed at 100%, which lands at 200 dpi effective — under the 250 dpi floor for PRESS-DIGITAL-B (§2).
Safe margin measures 0.05 in, under the 0.125 in floor (§3), and the page is not a full-bleed design, so the §3 exception does not reach it.
Total area coverage is 300%, over the 280% cap for PRESS-DIGITAL-B (§5).
It specifies 1 spot colour(s); PRESS-DIGITAL-B carries 0 (§6).
Fonts are not embedded (§7).
Carries 3 of the 4 required elements (§8) — 1 short.

### PG-28 — Explorer Certificate (SEC-07, PRESS-OFFSET-A): `DPI_TOO_LOW`

Artwork is 300 dpi placed at 150%, which lands at 200 dpi effective — under the 300 dpi floor for PRESS-OFFSET-A (§2).

### PG-29 — Certificate Backer (SEC-07, PRESS-OFFSET-A): `FONT_NOT_EMBEDDED`

Fonts are not embedded (§7).

### PG-30 — Signature Page (SEC-07, PRESS-OFFSET-A): `ELEMENT_COUNT_SHORT`

Carries 0 of the 2 required elements (§8) — 2 short.

### PG-32 — Maze Page (SEC-08, PRESS-DIGITAL-B): `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER_LIMIT`

Artwork is 225 dpi placed at 100%, which lands at 225 dpi effective — under the 250 dpi floor for PRESS-DIGITAL-B (§2).
Safe margin measures 0.11 in, under the 0.125 in floor (§3), and the page is not a full-bleed design, so the §3 exception does not reach it.
Total area coverage is 285%, over the 280% cap for PRESS-DIGITAL-B (§5).

### PG-33 — Colouring Page (SEC-08, PRESS-DIGITAL-B): `SPOT_UNSUPPORTED|ELEMENT_COUNT_SHORT`

It specifies 3 spot colour(s); PRESS-DIGITAL-B carries 0 (§6).
Carries 4 of the 6 required elements (§8) — 2 short.

### PG-35 — Sticker Sheet Two (SEC-09, PRESS-OFFSET-A): `BLEED_SHORT`

It is a full-bleed design carrying 0.08 in of bleed, under the 0.125 in minimum §4 requires of a full-bleed page. Being full-bleed releases it from the safe-margin rule, not from bleed.

### PG-36 — Sticker Sheet Three (SEC-09, PRESS-OFFSET-A): `INK_OVER_LIMIT|ELEMENT_COUNT_SHORT`

Total area coverage is 301%, over the 300% cap for PRESS-OFFSET-A (§5).
Carries 19 of the 20 required elements (§8) — 1 short.

## Pages the standard clears even though the numbers look wrong

These are the pages most likely to be 'fixed' by mistake. Each one is clear under PRINT-KIT-3 as written.

### PG-01 — Front Cover (SEC-01, PRESS-OFFSET-A): `none`

Its safe margin is 0.05 in, far under the 0.125 in floor, and on any other page that would be a MARGIN_VIOLATION. It is a full-bleed design, and the §3 exception releases a full-bleed page from the safe-margin rule because the art is drawn to run off the trim edge. Its 0.125 in of bleed meets the 0.125 in §4 minimum, so the page is genuinely clear — do not re-lay it out. It sits level with several limits at once — exactly 2 spot colours, exactly 300 dpi effective, exactly its 3 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-04 — Inside Back Cover (SEC-01, PRESS-OFFSET-A): `none`

Its artwork is only 240 dpi, which reads as thin, but it is placed at 80% and so lands at 300 dpi effective, at or above the 300 dpi floor for PRESS-OFFSET-A. It sits level with several limits at once — safe margin exactly 0.125 in, coverage exactly 300%, exactly 300 dpi effective, exactly its 1 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-05 — Welcome Letter (SEC-02, PRESS-DIGITAL-B): `none`

It lands at 250 dpi effective, which is under the 300 dpi floor the offset press holds — but SEC-02 runs on PRESS-DIGITAL-B, whose floor is 250 dpi, so the page clears §2 on the press that is printing it. Its artwork is only 200 dpi, which reads as thin, but it is placed at 80% and so lands at 250 dpi effective, at or above the 250 dpi floor for PRESS-DIGITAL-B. It sits level with several limits at once — exactly 250 dpi effective, exactly its 4 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-06 — How To Use This Kit (SEC-02, PRESS-DIGITAL-B): `none`

It lands at 270 dpi effective, which is under the 300 dpi floor the offset press holds — but SEC-02 runs on PRESS-DIGITAL-B, whose floor is 250 dpi, so the page clears §2 on the press that is printing it.

### PG-09 — Trail Map North (SEC-03, PRESS-OFFSET-A): `none`

It sits level with several limits at once — exactly 300 dpi effective, exactly its 6 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-13 — Compass Practice (SEC-03, PRESS-OFFSET-A): `none`

It sits level with several limits at once — coverage exactly 300%, exactly 2 spot colours, exactly 300 dpi effective, exactly its 7 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-15 — Mission Card A (SEC-04, PRESS-DIGITAL-B): `none`

It lands at 250 dpi effective, which is under the 300 dpi floor the offset press holds — but SEC-04 runs on PRESS-DIGITAL-B, whose floor is 250 dpi, so the page clears §2 on the press that is printing it. It sits level with several limits at once — coverage exactly 280%, exactly 250 dpi effective, exactly its 8 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-16 — Mission Card B (SEC-04, PRESS-DIGITAL-B): `none`

It lands at 250 dpi effective, which is under the 300 dpi floor the offset press holds — but SEC-04 runs on PRESS-DIGITAL-B, whose floor is 250 dpi, so the page clears §2 on the press that is printing it. It sits level with several limits at once — exactly 250 dpi effective, exactly its 8 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-20 — Bingo Grid One (SEC-05, PRESS-OFFSET-A): `none`

It sits level with several limits at once — safe margin exactly 0.125 in, coverage exactly 300%, exactly 2 spot colours, exactly 300 dpi effective, exactly its 9 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-21 — Bingo Grid Two (SEC-05, PRESS-OFFSET-A): `none`

Its safe margin is 0.0 in, far under the 0.125 in floor, and on any other page that would be a MARGIN_VIOLATION. It is a full-bleed design, and the §3 exception releases a full-bleed page from the safe-margin rule because the art is drawn to run off the trim edge. Its 0.125 in of bleed meets the 0.125 in §4 minimum, so the page is genuinely clear — do not re-lay it out. It sits level with several limits at once — exactly 300 dpi effective, exactly its 9 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-26 — Badge Backers (SEC-06, PRESS-DIGITAL-B): `none`

It lands at 255 dpi effective, which is under the 300 dpi floor the offset press holds — but SEC-06 runs on PRESS-DIGITAL-B, whose floor is 250 dpi, so the page clears §2 on the press that is printing it.

### PG-27 — Completion Certificate (SEC-07, PRESS-OFFSET-A): `none`

It sits level with several limits at once — exactly 300 dpi effective, exactly its 2 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-31 — Word Search (SEC-08, PRESS-DIGITAL-B): `none`

It lands at 250 dpi effective, which is under the 300 dpi floor the offset press holds — but SEC-08 runs on PRESS-DIGITAL-B, whose floor is 250 dpi, so the page clears §2 on the press that is printing it. It sits level with several limits at once — coverage exactly 280%, exactly 250 dpi effective, exactly its 5 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

### PG-34 — Sticker Sheet One (SEC-09, PRESS-OFFSET-A): `none`

Its safe margin is 0.02 in, far under the 0.125 in floor, and on any other page that would be a MARGIN_VIOLATION. It is a full-bleed design, and the §3 exception releases a full-bleed page from the safe-margin rule because the art is drawn to run off the trim edge. Its 0.125 in of bleed meets the 0.125 in §4 minimum, so the page is genuinely clear — do not re-lay it out. Its artwork is only 240 dpi, which reads as thin, but it is placed at 80% and so lands at 300 dpi effective, at or above the 300 dpi floor for PRESS-OFFSET-A. It sits level with several limits at once — coverage exactly 300%, exactly 2 spot colours, exactly 300 dpi effective, exactly its 20 required elements — and PRINT-KIT-3 treats a value equal to a limit as acceptable, so none of these is a finding.

## Pages clear on every rule

No finding and nothing borderline: PG-24 Badge Sheet One.

## Where the press assignment decides the verdict

Same numbers, different answer depending on which press the section runs on. Moving a section between presses changes these verdicts, so they are worth knowing before anyone reschedules the run.

- **PG-05** — 250 dpi effective clears the 250 dpi floor on PRESS-DIGITAL-B but would be DPI_TOO_LOW on a press held to 300 dpi.
- **PG-06** — 270 dpi effective clears the 250 dpi floor on PRESS-DIGITAL-B but would be DPI_TOO_LOW on a press held to 300 dpi.
- **PG-07** — 1 spot colour(s) cannot run on PRESS-DIGITAL-B at all, though a press carrying 2 would take them.
- **PG-08** — 290% coverage is over the 280% cap on PRESS-DIGITAL-B but inside the 300% a press with the looser cap allows.
- **PG-10** — 270 dpi effective is short of the 300 dpi floor on PRESS-OFFSET-A, though it would clear a press floored at 250 dpi.
- **PG-15** — 250 dpi effective clears the 250 dpi floor on PRESS-DIGITAL-B but would be DPI_TOO_LOW on a press held to 300 dpi.
- **PG-16** — 250 dpi effective clears the 250 dpi floor on PRESS-DIGITAL-B but would be DPI_TOO_LOW on a press held to 300 dpi.
- **PG-18** — 281% coverage is over the 280% cap on PRESS-DIGITAL-B but inside the 300% a press with the looser cap allows.
- **PG-19** — 2 spot colour(s) cannot run on PRESS-DIGITAL-B at all, though a press carrying 2 would take them.
- **PG-25** — 300% coverage is over the 280% cap on PRESS-DIGITAL-B but inside the 300% a press with the looser cap allows; 1 spot colour(s) cannot run on PRESS-DIGITAL-B at all, though a press carrying 2 would take them.
- **PG-26** — 255 dpi effective clears the 250 dpi floor on PRESS-DIGITAL-B but would be DPI_TOO_LOW on a press held to 300 dpi.
- **PG-31** — 250 dpi effective clears the 250 dpi floor on PRESS-DIGITAL-B but would be DPI_TOO_LOW on a press held to 300 dpi.
- **PG-32** — 285% coverage is over the 280% cap on PRESS-DIGITAL-B but inside the 300% a press with the looser cap allows.

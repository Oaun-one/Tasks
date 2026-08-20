# Activity-kit pre-flight — PRINT-KIT-2

36 live pages audited out of 42
artwork rows, across 8 sections. **11 pages are
clear** and **25 carry at least one finding**, 41
findings in total. 4 sections cannot be imposed as planned.

## Superseded artwork

The batch carries more than one revision of 6 pages, and only the highest
revision of a `page_id` is live (§0). Those 6 lower-revision rows
are superseded and were **not** audited: PG-04, PG-12, PG-18, PG-27, PG-33, PG-35.

Row order is not the tie-break — `revision` is. PG-12, PG-27, PG-33 and PG-35 have their live
revision *earlier* in the file than the superseded one; PG-04 and PG-18 have it later. Taking
the first row per page, or the last, gets a different answer from taking the highest revision.

Auditing the superseded rows instead of the live ones changes six verdicts and every derived
figure. PG-27 runs the other way from the rest: rev 1 was 200 dpi and would have been
`DPI_TOO_LOW`, while the live rev 2 is placed at 200% from 480 dpi artwork and clears the
floor exactly.

## The limits actually applied

Every limit in §2–§5 belongs to the **stock**, reached through the page's section
(`page` → `section` → `stock`):

| stock | min effective resolution | max total ink | min safe margin | min bleed |
| --- | --- | --- | --- | --- |
| `CST-100` | 300 dpi | 280% | 0.125 in | 0.125 in |
| `UNC-120` | 240 dpi | 240% | 0.1875 in | 0.25 in |
| `BRD-250` | 260 dpi | 300% | 0.25 in | 0.1875 in |

So the same number lands on either side of the line depending on the section: PG-13 at 298%
ink is clear on BRD-250 and PG-28 at 241% is over on UNC-120 — the smaller number is the
breach.

Resolution is judged on the **effective** figure, not the supplied one: `artwork_dpi` divided
by the placement scale (§2). PG-06 is supplied at 450 dpi and only prints at 300 because it is
placed at 150%; PG-20 is supplied at 240 dpi and prints at 300 because it is placed at 80%.
Reading `artwork_dpi` straight off the row gets both of them wrong.

Every limit is inclusive (§1). PG-05, PG-16, PG-22, PG-27 and PG-34 all sit exactly on at
least one limit and are clear because of it.

## Full bleed: exempt from the margin, and only in a saddle-stitched section

Full-bleed pages in saddle-stitched sections are exempt from §3 — PG-07, PG-10, PG-25 and
PG-32 all carry margins well under their stock's floor and are clear on it. Flagging them is
the commonest false positive here.

But the exemption stops at the binding (§4). A perfect-bound page is glued on the spine and
has no bleed there, so PG-01, PG-02, PG-18, PG-29 and PG-35 are full-bleed *and* carry
`MARGIN_VIOLATION`. Reading the exemption as a blanket pass clears five pages wrongly;
applying §3 to every full-bleed page flags four wrongly.

Full-bleed is also the only status that owes a bleed allowance, and PG-02, PG-18 and PG-25 are
short of their stock's minimum. Pages that are not full-bleed are not assessed on bleed at
all: PG-30 carries 0.30 in of bleed and it is neither a credit nor a finding.

## Required elements and Amendment Rev B

Minimums come from the page-type table in §6, raised by 2 for `mission_cards` and
`badge_certificate` in a `saddle_stitch` section. PG-19 (6 mission cards, perfect-bound) is
clear on exactly the count that makes PG-13 (6 mission cards, saddle-stitched) short by 2.
**The batch is missing 13 required elements in total**
across 10 pages.

## Findings by page

- **PG-01 Front Cover** (SEC-01, BRD-250) — `MARGIN_VIOLATION`: safe margin 0.05 in against a 0.25 in floor on BRD-250 — full-bleed, but the section is perfect-bound, so §4 does not release it from §3.
- **PG-02 Inside Cover** (SEC-01, BRD-250) — `MARGIN_VIOLATION|BLEED_SHORT`: safe margin 0.02 in against a 0.25 in floor on BRD-250 — full-bleed, but the section is perfect-bound, so §4 does not release it from §3; bleed allowance 0.125 in against a 0.1875 in minimum on BRD-250.
- **PG-03 Welcome Letter** (SEC-01, BRD-250) — `DPI_TOO_LOW`: effective resolution 240 dpi (300 dpi placed at 125%) against a 260 dpi floor on BRD-250.
- **PG-04 Kit Map** (SEC-01, BRD-250) — `MARGIN_VIOLATION|INK_OVER`: safe margin 0.24 in against a 0.25 in floor on BRD-250; total ink 305% against a 300% cap on BRD-250.
- **PG-06 Trail Map B** (SEC-02, CST-100) — `MARGIN_VIOLATION`: safe margin 0.12 in against a 0.125 in floor on CST-100.
- **PG-07 Trail Map C** (SEC-02, CST-100) — `INK_OVER|ELEMENT_COUNT_SHORT`: total ink 282% against a 280% cap on CST-100; 3 required elements against a minimum of 4 for a `map` page in a saddle_stitch section (short by 1).
- **PG-08 Trail Activity 1** (SEC-02, CST-100) — `DPI_TOO_LOW`: effective resolution 272 dpi (300 dpi placed at 110%) against a 300 dpi floor on CST-100.
- **PG-12 Mission Cards B** (SEC-03, BRD-250) — `ELEMENT_COUNT_SHORT`: 7 required elements against a minimum of 8 for a `mission_cards` page in a saddle_stitch section (short by 1).
- **PG-13 Mission Cards C** (SEC-03, BRD-250) — `ELEMENT_COUNT_SHORT`: 6 required elements against a minimum of 8 for a `mission_cards` page in a saddle_stitch section (short by 2).
- **PG-14 Mission Cards D** (SEC-03, BRD-250) — `INK_OVER`: total ink 301% against a 300% cap on BRD-250.
- **PG-15 Mission Cards E** (SEC-03, BRD-250) — `DPI_TOO_LOW|MARGIN_VIOLATION|ELEMENT_COUNT_SHORT`: effective resolution 250 dpi (300 dpi placed at 120%) against a 260 dpi floor on BRD-250; safe margin 0.2 in against a 0.25 in floor on BRD-250; 5 required elements against a minimum of 8 for a `mission_cards` page in a saddle_stitch section (short by 3).
- **PG-17 Station Bingo 2** (SEC-04, CST-100) — `ELEMENT_COUNT_SHORT`: 8 required elements against a minimum of 9 for a `bingo` page in a perfect_bound section (short by 1).
- **PG-18 Station Bingo 3** (SEC-04, CST-100) — `MARGIN_VIOLATION|BLEED_SHORT|INK_OVER`: safe margin 0.0 in against a 0.125 in floor on CST-100 — full-bleed, but the section is perfect-bound, so §4 does not release it from §3; bleed allowance 0.1 in against a 0.125 in minimum on CST-100; total ink 285% against a 280% cap on CST-100.
- **PG-20 Mission Cards G** (SEC-04, CST-100) — `ELEMENT_COUNT_SHORT`: 5 required elements against a minimum of 6 for a `mission_cards` page in a perfect_bound section (short by 1).
- **PG-21 Station Activity** (SEC-04, CST-100) — `DPI_TOO_LOW`: effective resolution 290 dpi (290 dpi placed at 100%) against a 300 dpi floor on CST-100.
- **PG-23 Parent Guide 2** (SEC-05, UNC-120) — `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER`: effective resolution 227 dpi (250 dpi placed at 110%) against a 240 dpi floor on UNC-120; safe margin 0.18 in against a 0.1875 in floor on UNC-120; total ink 245% against a 240% cap on UNC-120.
- **PG-25 Badge Sheet B** (SEC-05, UNC-120) — `BLEED_SHORT|ELEMENT_COUNT_SHORT`: bleed allowance 0.2 in against a 0.25 in minimum on UNC-120; 5 required elements against a minimum of 6 for a `badge_certificate` page in a saddle_stitch section (short by 1).
- **PG-26 Certificate A** (SEC-06, UNC-120) — `DPI_TOO_LOW`: effective resolution 200 dpi (200 dpi placed at 100%) against a 240 dpi floor on UNC-120.
- **PG-28 Certificate C** (SEC-06, UNC-120) — `INK_OVER|ELEMENT_COUNT_SHORT`: total ink 241% against a 240% cap on UNC-120; 3 required elements against a minimum of 4 for a `badge_certificate` page in a perfect_bound section (short by 1).
- **PG-29 Reward Activity 1** (SEC-06, UNC-120) — `DPI_TOO_LOW|MARGIN_VIOLATION`: effective resolution 230 dpi (300 dpi placed at 130%) against a 240 dpi floor on UNC-120; safe margin 0.04 in against a 0.1875 in floor on UNC-120 — full-bleed, but the section is perfect-bound, so §4 does not release it from §3.
- **PG-30 Reward Activity 2** (SEC-06, UNC-120) — `MARGIN_VIOLATION`: safe margin 0.15 in against a 0.1875 in floor on UNC-120.
- **PG-32 Trail Sticker Sheet** (SEC-07, CST-100) — `DPI_TOO_LOW`: effective resolution 240 dpi (240 dpi placed at 100%) against a 300 dpi floor on CST-100.
- **PG-33 Mission Cards H** (SEC-07, CST-100) — `INK_OVER|ELEMENT_COUNT_SHORT`: total ink 281% against a 280% cap on CST-100; 7 required elements against a minimum of 8 for a `mission_cards` page in a saddle_stitch section (short by 1).
- **PG-35 Take-home Badges** (SEC-08, BRD-250) — `MARGIN_VIOLATION`: safe margin 0.06 in against a 0.25 in floor on BRD-250 — full-bleed, but the section is perfect-bound, so §4 does not release it from §3.
- **PG-36 Take-home Activity** (SEC-08, BRD-250) — `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER|ELEMENT_COUNT_SHORT`: effective resolution 214 dpi (300 dpi placed at 140%) against a 260 dpi floor on BRD-250; safe margin 0.2 in against a 0.25 in floor on BRD-250; total ink 302% against a 300% cap on BRD-250; 3 required elements against a minimum of 4 for a `activity` page in a perfect_bound section (short by 1).

## Pages that clear the standard

PG-05, PG-09, PG-10, PG-11, PG-16, PG-19, PG-22, PG-24, PG-27, PG-31, PG-34 — no finding.

## Sections

§8 reads the page audit, not the raw batch: a page carrying `ELEMENT_COUNT_SHORT` is held
back for re-supply and leaves the imposition.

| section | binding | stock | live | held back | imposed | flagged | imposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEC-01 | perfect_bound | BRD-250 | 4 | 0 | 4 | 4 | none |
| SEC-02 | saddle_stitch | CST-100 | 6 | 1 | 5 | 3 | IMPOSITION_INVALID (needs 3) |
| SEC-03 | saddle_stitch | BRD-250 | 5 | 3 | 2 | 4 | IMPOSITION_INVALID (needs 2) |
| SEC-04 | perfect_bound | CST-100 | 6 | 2 | 4 | 4 | none |
| SEC-05 | saddle_stitch | UNC-120 | 4 | 1 | 3 | 2 | IMPOSITION_INVALID (needs 1) |
| SEC-06 | perfect_bound | UNC-120 | 5 | 1 | 4 | 4 | none |
| SEC-07 | saddle_stitch | CST-100 | 3 | 1 | 2 | 2 | IMPOSITION_INVALID (needs 2) |
| SEC-08 | perfect_bound | BRD-250 | 3 | 1 | 2 | 2 | none |

Cannot be imposed as planned:

- **SEC-02** (saddle_stitch) imposes 5 pages after 1 held back from 6 live — needs 3 more to reach a multiple of 4.
- **SEC-03** (saddle_stitch) imposes 2 pages after 3 held back from 5 live — needs 2 more to reach a multiple of 4.
- **SEC-05** (saddle_stitch) imposes 3 pages after 1 held back from 4 live — needs 1 more to reach a multiple of 4.
- **SEC-07** (saddle_stitch) imposes 2 pages after 1 held back from 3 live — needs 2 more to reach a multiple of 4.

The hold-back is what decides three of these. SEC-05 has 4 live pages, which fits a
saddle-stitch multiple of 4 on its own, and still fails once PG-25 is held back. SEC-06 (5
live) and SEC-08 (3 live) both look wrong on the raw count and both impose cleanly once a
held-back page is removed. Between them the invalid sections need
8 pages.

## Totals

| figure | value |
| --- | --- |
| pages audited | 36 |
| superseded artwork rows | 6 |
| sections | 8 |
| clear | 11 |
| flagged | 25 |
| findings raised | 41 |
| `DPI_TOO_LOW` pages | 9 |
| `MARGIN_VIOLATION` pages | 11 |
| `BLEED_SHORT` pages | 3 |
| `INK_OVER` pages | 8 |
| `ELEMENT_COUNT_SHORT` pages | 10 |
| required elements missing | 13 |
| sections that cannot be imposed | 4 |
| pages those sections need | 8 |

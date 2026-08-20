# Activity-kit pre-flight — PRINT-KIT-2

30 pages audited from a batch of 34
artwork rows. 10 clear, 20 carry at least one
finding, 29 findings in total.

## Superseded artwork

The batch carries more than one revision of four pages, and only the highest revision of a
`page_id` is live (§0). These four rows are superseded and were **not** audited:

- **PG-04** rev 1 is superseded by rev 2. The live artwork is placed at 80%, has a 0.24 in
  margin and 305% ink; rev 1 would have read `none`.
- **PG-12** rev 1 is superseded by rev 3, which drops to 7 mission cards. Rev 1 carried 9
  and would have read `none`. The live revision appears *before* the superseded one in the
  file, so row order is not the tie-break — `revision` is.
- **PG-18** rev 1 is superseded by rev 2, which cuts the bleed to 0.10 in and pushes ink to
  285%. Rev 1 would have read `none`.
- **PG-27** rev 1 is superseded by rev 2. Here it runs the other way: rev 1 was 200 dpi and
  would have been `DPI_TOO_LOW`, while the live rev 2 is placed at 200% from 480 dpi
  artwork and clears the floor exactly.

Auditing the superseded rows instead of the live ones changes four verdicts and every
derived figure.

## How the limits were read

Every limit in §2–§5 belongs to the **stock**, reached through the page's section
(`page` → `section` → `stock`), so the same number is a breach in one section and clear in
another. PG-13 at 298% ink is clear on BRD-250 (300% cap) while PG-28 at 241% is over on
UNC-120 (240% cap).

Resolution is judged on the **effective** figure, not the supplied one: `artwork_dpi`
divided by the placement scale (§2). PG-06 is supplied at 450 dpi and still only prints at
300 because it is placed at 150%; PG-20 is supplied at 240 dpi and prints at 300 because it
is placed at 80%. Reading `artwork_dpi` straight off the row gets both of them wrong.

Every limit is inclusive (§1). PG-05, PG-16, PG-22 and PG-27 all sit exactly on at least
one limit and are clear because of it.

## Full bleed: exempt from the margin, and only from the margin

Full-bleed pages are exempt from the safe-margin rule (§4) — PG-01 at 0.05 in, PG-10 at
0.00 in and PG-29 at 0.04 in are all clear on margin, and flagging them is the commonest
false positive here. But full-bleed is also the *only* status that owes a bleed allowance,
and PG-02, PG-18 and PG-25 are short of their stock's minimum. Pages that are not
full-bleed are not assessed on bleed at all: PG-30 carries 0.30 in of bleed and it is
neither a credit nor a finding.

## Required elements and Amendment Rev B

Minimums come from the page-type table in §6, raised by 2 for `mission_cards`
and `badge_certificate` in a `saddle_stitch` section. PG-19 (6 mission cards,
perfect-bound) is clear on exactly the same count that makes PG-13 (6 mission cards,
saddle-stitched) short by 2. The batch is missing 11
required elements in total across 8 pages.

## Findings by page

- **PG-02 Inside Cover** (SEC-01, BRD-250) — `BLEED_SHORT`: bleed allowance 0.125 in against a 0.1875 in minimum on BRD-250.
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
- **PG-18 Station Bingo 3** (SEC-04, CST-100) — `BLEED_SHORT|INK_OVER`: bleed allowance 0.1 in against a 0.125 in minimum on CST-100; total ink 285% against a 280% cap on CST-100.
- **PG-20 Mission Cards G** (SEC-04, CST-100) — `ELEMENT_COUNT_SHORT`: 5 required elements against a minimum of 6 for a `mission_cards` page in a perfect_bound section (short by 1).
- **PG-21 Station Activity** (SEC-04, CST-100) — `DPI_TOO_LOW`: effective resolution 290 dpi (290 dpi placed at 100%) against a 300 dpi floor on CST-100.
- **PG-23 Parent Guide 2** (SEC-05, UNC-120) — `DPI_TOO_LOW|MARGIN_VIOLATION|INK_OVER`: effective resolution 227 dpi (250 dpi placed at 110%) against a 240 dpi floor on UNC-120; safe margin 0.18 in against a 0.1875 in floor on UNC-120; total ink 245% against a 240% cap on UNC-120.
- **PG-25 Badge Sheet B** (SEC-05, UNC-120) — `BLEED_SHORT|ELEMENT_COUNT_SHORT`: bleed allowance 0.2 in against a 0.25 in minimum on UNC-120; 5 required elements against a minimum of 6 for a `badge_certificate` page in a saddle_stitch section (short by 1).
- **PG-26 Certificate A** (SEC-06, UNC-120) — `DPI_TOO_LOW`: effective resolution 200 dpi (200 dpi placed at 100%) against a 240 dpi floor on UNC-120.
- **PG-28 Certificate C** (SEC-06, UNC-120) — `INK_OVER|ELEMENT_COUNT_SHORT`: total ink 241% against a 240% cap on UNC-120; 3 required elements against a minimum of 4 for a `badge_certificate` page in a perfect_bound section (short by 1).
- **PG-29 Reward Activity 1** (SEC-06, UNC-120) — `DPI_TOO_LOW`: effective resolution 230 dpi (300 dpi placed at 130%) against a 240 dpi floor on UNC-120.
- **PG-30 Reward Activity 2** (SEC-06, UNC-120) — `MARGIN_VIOLATION`: safe margin 0.15 in against a 0.1875 in floor on UNC-120.

## Pages that clear the standard

PG-01, PG-05, PG-09, PG-10, PG-11, PG-16, PG-19, PG-22, PG-24, PG-27 — no finding.

## Totals

| figure | value |
| --- | --- |
| pages audited | 30 |
| superseded artwork rows | 4 |
| clear | 10 |
| flagged | 20 |
| findings raised | 29 |
| `DPI_TOO_LOW` pages | 7 |
| `MARGIN_VIOLATION` pages | 5 |
| `BLEED_SHORT` pages | 3 |
| `INK_OVER` pages | 6 |
| `ELEMENT_COUNT_SHORT` pages | 8 |
| required elements missing | 11 |

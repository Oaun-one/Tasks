# Printable activity-kit production standard (PRINT-KIT-2)

Binding for `activity_kit_pages.csv`. `finding` is one of `DPI_TOO_LOW`,
`MARGIN_VIOLATION`, `ELEMENT_COUNT_SHORT`, or `none`. A page may carry more than one
finding, joined with `|`.

## 1. Image resolution

Every page must render at or above 300 DPI for print. Below it is `DPI_TOO_LOW`.

## 2. Safe margin

Every page must keep at least 0.125 in of clear margin between any text/graphic
element and the trim edge. Below it is `MARGIN_VIOLATION`.

## 3. Full-bleed exception

A page explicitly designed as full-bleed (art intentionally printed edge-to-edge, tagged
`full_bleed_design`) is **exempt** from the safe-margin rule (§2) — its elements are meant
to run to the trim edge. Flagging a full-bleed page for a thin margin is the commonest
false positive in this audit.

## 4. Required-element count

Each page type has a minimum count of required elements (e.g. mission cards need a minimum
number of missions, the badge/certificate page needs a minimum number of required fields).
A page under its own `min_element_required` is `ELEMENT_COUNT_SHORT`.

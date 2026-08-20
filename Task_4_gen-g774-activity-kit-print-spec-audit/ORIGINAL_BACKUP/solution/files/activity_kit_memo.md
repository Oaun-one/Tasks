# Activity-kit production audit — 6 pages

2 compliant, 4 carry at least one finding.

## PG-02, PG-06 resolution

Rendered under 300 DPI: `DPI_TOO_LOW`.

## PG-03, PG-06 margin

Safe margin under 0.125 in and not a full-bleed page: `MARGIN_VIOLATION`.

## PG-04, PG-06 element count

Fewer elements than the page type's `min_element_required`: `ELEMENT_COUNT_SHORT`.

## PG-01 is the full-bleed exception, not a finding

The Cover page's safe margin is only 0.05 in, under the 0.125 in floor, which
looks exactly like PG-03's violation. But the cover is tagged as a full-bleed design, which
the standard exempts from the safe-margin rule. The finding is `none`.

# Printable activity-kit production standard (PRINT-KIT-2)

Binding for the artwork batch in `activity_kit_pages.csv`.

## 0. Batch scope and revisions

The batch file lists *artwork*, not pages. A page that has been re-supplied appears more
than once, once per `revision`, under the same `page_id`. Only the highest-numbered
revision of a `page_id` is live artwork and goes to press; every lower revision is
superseded and is not audited. The rows are not in revision order. Every figure reported
for the batch counts live pages only.

## 1. Sections, binding and stock

Each page belongs to a section (`kit_sections.csv`), and the section fixes both the binding
and the paper stock that section is printed on. The limits in §2–§5 are properties of the
**stock** (`stock_profiles.csv`), not of the kit as a whole, so the same measurement can be
a breach in one section and clear in another.

Every limit in this standard is inclusive: a measurement exactly equal to its limit meets
the limit. Only a measurement strictly worse than the limit is a breach.

## 2. Effective resolution

Artwork is supplied at `artwork_dpi` and placed on the page at `placement_scale_pct`. What
actually prints is the effective resolution:

    effective_dpi = floor(artwork_dpi * 100 / placement_scale_pct)

A page placed larger than 100% therefore resolves *lower* than its supplied figure, and one
placed smaller resolves higher. Below the stock's `min_dpi` it is `DPI_TOO_LOW`.

## 3. Safe margin

`margin_in` must be at least the stock's `min_margin_in` — the clear distance between any
text or graphic element and the trim edge. Below it is `MARGIN_VIOLATION`.

## 4. Full-bleed pages: one exemption, one obligation

A page tagged `full_bleed_design` is **exempt from §3**. Its art is meant to run to the trim
edge, so a thin margin on a full-bleed page is by design; flagging it is the commonest false
positive in this audit.

It is exempt from nothing else, and it carries an obligation no other page carries: a
full-bleed page must be supplied with `bleed_in` of at least the stock's `min_bleed_in`, or
the trim eats into the art. Below it is `BLEED_SHORT`. `bleed_in` on a page that is not
full-bleed is not assessed.

## 5. Ink coverage

`total_ink_pct` must not exceed the stock's `max_ink_pct`. Above it is `INK_OVER`.

## 6. Required elements

Each page type carries a minimum number of required elements:

| page_type | minimum |
| --- | --- |
| `cover` | 1 |
| `parent_guide` | 2 |
| `map` | 4 |
| `activity` | 4 |
| `mission_cards` | 6 |
| `bingo` | 9 |
| `badge_certificate` | 4 |

**Amendment Rev B.** A saddle-stitched section is trimmed harder at the outer edge, so its
detachable-element pages have to be supplied with spares. In a section bound
`saddle_stitch`, the minimum for `mission_cards` and for `badge_certificate` is
2 higher than the table above. No other page type and no other binding is
affected.

A page below its own minimum is `ELEMENT_COUNT_SHORT`. A page's shortfall is its minimum
less its `element_count`; a page at or above its minimum has a shortfall of zero.

## 7. Findings

`finding` is one or more of `DPI_TOO_LOW`, `MARGIN_VIOLATION`, `BLEED_SHORT`, `INK_OVER`,
`ELEMENT_COUNT_SHORT`, joined with `|`, or `none` for a page that breaches nothing.

# Dissertation formatting specification (DFS-11)

## Rule 1 — margins, with the landscape-annex exception

Every section must use 2.5 cm margins on all four sides. **Exception:
landscape data annexes are exempt from this margin rule** — a narrower margin is needed to
fit wide tables on the page, and the standard does not require 2.5 cm there.
A non-annex section outside the required margin is `MARGIN_NONCOMPLIANT`. Flagging a
landscape annex for its narrower margin is the commonest false positive.

## Rule 2 — font, no exception

Every section, including annexes, must use Times New Roman at 12 pt. Any
section using a different font or size is `FONT_NONCOMPLIANT`.

## Rule 3 — line spacing, no exception

Every section, including annexes, must use 1.5 line spacing. Any section
using a different spacing is `SPACING_NONCOMPLIANT`.

## Finding names

`MARGIN_NONCOMPLIANT`, `FONT_NONCOMPLIANT`, `SPACING_NONCOMPLIANT`, `none`.

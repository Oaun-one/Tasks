# Heritage Landing Festival collateral and signage permit standard

This decides whether a piece of festival collateral is compliant before it ships or goes up
at the venue. Where an item and this standard disagree, this standard decides.

## 1. Scope: installed signage only

The permit-number, egress-marker and size rules below apply **only to items classified as
`installed_signage`** — collateral physically mounted or displayed at the venue (fence
posters, mounted banners, directional signs). A **`standalone_graphic`** — a promotional
image produced for personal or downstream use (such as an overlay graphic meant to be
combined with other artwork elsewhere) and never physically installed at the venue — is not
installed signage under this standard and is exempt from all three rules below, regardless
of its own permit-number, egress or size values. This is the commonest false positive in
this review.

## 2. Permit number

An installed-signage item must display a printed festival permit number. Missing that is
`PERMIT_NUMBER_MISSING`.

## 3. Egress markers

An installed-signage item must not obstruct a designated safety egress marker. Obstructing
one is `EGRESS_MARKER_OBSTRUCTED`.

## 4. Size

An installed-signage item's physical size must not exceed 3.0 sq ft.
Above that is `OVERSIZE_COLLATERAL`.

## Finding names

`PERMIT_NUMBER_MISSING`, `EGRESS_MARKER_OBSTRUCTED`, `OVERSIZE_COLLATERAL`, or `none`. An
item may carry more than one, joined with `|`.

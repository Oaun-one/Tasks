# DFS-12 — dissertation formatting standard

Graduate Thesis Office, revision 12. Supersedes DFS-11. This is the standard the
thesis office's pre-binding audit is run against.

DFS-12 is amended from time to time. The amendments are published separately in
`dfs12_amendments.md`, each carrying its own effective date. **An amendment governs
over this base text from its effective date onward.** An amendment whose effective
date falls after the dissertation's date of submission is not yet in force and has
no bearing on the audit, however recently it was published.

## §1 Scope and how findings are reported

Every section of the dissertation is checked against §2 to §8. Every part is checked
against §9.

A section carries one finding code for each rule it breaches. A section may breach
several rules at once and every breach is reported; a section that breaches none is
reported as clean.

Two of the limits below are **per template** rather than a single office-wide number.
A section takes its template through its part: `part_plan.csv` names the template for
each part, and `template_profiles.csv` holds that template's limits. A section must
be judged against the template its own part is set in.

**Revisions.** The section log is an export from the typesetting system and carries
every revision of a section that was re-typeset during correction. Only the
**highest-numbered revision** of each `section_id` is audited; lower-numbered
revisions are superseded and are retained for history only. A superseded revision
contributes nothing to the audit — not a finding, not a page, not a count. The
export is not sorted and row position carries no meaning.

## §2 Margins — `MARGIN_NONCOMPLIANT`

Margins are recorded per side. **Inner** is the binding edge.

- `margin_top_cm` and `margin_bottom_cm` must each be **not less than the template's
  `min_top_bottom_cm`**.
- `margin_inner_cm` must be not less than the binding-edge minimum. The base text sets
  that minimum at 2.5 cm; see the amendments.

A section short on any of those three is `MARGIN_NONCOMPLIANT`. A section exactly at a
minimum is compliant.

## §3 Type area — `TYPE_AREA_INVALID`

The outer margin is not recorded directly. It is what is left of the page once the
binding edge and the text block are taken off, and it is the figure that decides
whether the outer edge is wide enough:

    implied outer margin = page width − margin_inner_cm − text_block_width_cm

The dissertation is printed on A4. A portrait page is **21.0 cm** wide and a landscape
page is **29.7 cm** wide; take the width from the section's own `orientation`.

A section whose implied outer margin is **less than the template's `min_outer_cm`** is
`TYPE_AREA_INVALID`. Exactly at the minimum is compliant. Work to two decimal places.

**Exception — landscape data annexes.** A section is released from §3, and from §3
only, where **all three** hold:

1. its `section_type` is `annex`;
2. its `orientation` is `landscape`; and
3. it carries an **oversized table** — its `widest_table_cm` is greater than the type
   area a landscape page would otherwise allow under this standard, that being the
   landscape page width less the binding-edge minimum and less the template's
   `min_outer_cm`.

That allowance is not the same number for both templates. The exception releases the
section from §3 and from nothing else; in particular the binding-edge minimum in §2 is
not subject to this or any other exception.

## §4 Leading — `LEADING_NONCOMPLIANT`

Line spacing is recorded as a leading, in `leading_unit` (`pt` or `mm`) and
`leading_value`. **For the purposes of this standard 1 pt is 0.35 mm**, so a leading
recorded in millimetres is converted to points by dividing by 0.35.

The required leading is **1.5 times the body size this standard requires**, which is
1.5 × 12.0 pt = **18.0 pt** — irrespective of the size a section actually uses. A
section set at some other size does not get a proportionally smaller leading; it gets
a §5 finding and a §4 finding.

A section whose converted leading differs from the requirement by more than 0.05 pt is
`LEADING_NONCOMPLIANT`.

## §5 Body font — `FONT_NONCOMPLIANT`

Every section must set its body text in Times New Roman at **12.0 pt**. Both halves
apply to every section, annexes included.

A section whose `body_font_name` is not an accepted identifier, or whose
`body_font_size_pt` is not 12.0, is `FONT_NONCOMPLIANT`.

**Appendix F — accepted font identifiers.** These, and only these, denote the Times
New Roman face for the purposes of DFS-12:

- `Times New Roman`
- `TimesNewRomanPSMT`
- `Times New Roman PS MT Std`

Metrically compatible substitutes are not the face itself and are not accepted.
`Nimbus Roman No9 L`, `Liberation Serif` and `Tinos` are substitutes.

## §6 Heading style — `HEADING_STYLE_INVALID`

Headings must be set in the same face as body text — that is, `heading_font_name` must
also be one of the Appendix F identifiers — and must be large enough to read as a
heading.

A heading is large enough when `heading_font_size_pt` is at least the template's
`min_heading_step_pt` above **the size the section's body text actually uses**, not
above the size §5 requires. Exactly at that figure is compliant.

A section failing either half is `HEADING_STYLE_INVALID`.

## §7 Captions — `CAPTION_MISSING`

Every float — every figure and every table — must carry a caption. `float_count` is
the number of floats in the section and `caption_count` the number of captions.

A section whose `caption_count` is less than its `float_count` is `CAPTION_MISSING`.
The difference is that section's **caption shortfall**: the number of captions still
to be written.

## §8 Page numbering — `NUMBERING_INVALID`

Each part is numbered in one style throughout, given as `numbering` in
`part_plan.csv`. A section whose `page_number_style` is not the style its own part is
numbered in is `NUMBERING_INVALID`.

## §9 Pagination — `PAGINATION_INVALID`

Every part must open on a **recto**, that is on an odd-numbered page.

Pages run continuously from page 1 through the whole dissertation in `sequence` order.
A part's start page is therefore one more than the total page extent of every audited
section that sits before it in `sequence`:

    start page of a part = 1 + Σ page_extent of all audited sections of lower sequence

Count the pages actually present in the audited batch; do not take an extent on trust
from a superseded revision. A part whose start page is even is `PAGINATION_INVALID`
and has to be repaginated before binding.

§9 is a property of the part, not of any one section in it. A `PAGINATION_INVALID`
part is not a finding against its sections.

## Waivers

The thesis office may grant a section a standing waiver of a named rule. Waivers in
force for this dissertation are listed in the submission record. A waiver clears the
finding it names, within the scope it names, and does nothing outside that scope.

## Finding codes

Section: `MARGIN_NONCOMPLIANT`, `TYPE_AREA_INVALID`, `LEADING_NONCOMPLIANT`,
`FONT_NONCOMPLIANT`, `HEADING_STYLE_INVALID`, `CAPTION_MISSING`, `NUMBERING_INVALID`.
Part: `PAGINATION_INVALID`. Clean: `none`.

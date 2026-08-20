# Dissertation formatting specification (DFS-11)

Graduate Thesis Office. Base text, issued 2023-11-01.

DFS-11 is amended from time to time. The amendments are published separately in
`dfs11_amendments.md`, each carrying its own effective date. **An amendment governs
over this base text from its effective date onward.** An amendment whose effective
date falls after the dissertation's date of submission is not yet in force and has no
bearing on the audit.

## Scope

The section log records the measured properties of every section of the dissertation.

- A section may appear in the log more than once, at different `revision` numbers.
  **Only the highest-numbered revision of each `section_id` is audited.** Lower-numbered
  revisions are superseded and are retained for history only. Log order carries no meaning.
- Every `section_id` in the log is audited exactly once, whatever its `section_type`.

## Page geometry

The dissertation is printed on A4: 21.0 cm wide by 29.7 cm tall in portrait, and
29.7 cm wide by 21.0 cm tall in landscape.

The **printable width** of a page is its physical width less the inner and outer margins
this specification requires for that section.

## Rule 1 — margins

Margins are recorded per side: `margin_top_cm`, `margin_bottom_cm`, `margin_inner_cm`,
`margin_outer_cm`. **Inner** is the binding edge.

Every section must have a margin of **not less than 2.5 cm** on each of the four sides.
A section whose margin falls below the requirement on any side is `MARGIN_NONCOMPLIANT`.

### Rule 1 exception — landscape data annexes

A landscape data annex may set narrower margins than Rule 1 requires, so that a wide table
fits on the page. The scope of this exception is narrowed by amendment; see A-3.

## Rule 2 — font

Every section must be set in Times New Roman at **12.0 pt**. Both halves of that
requirement apply to every section, annexes included.

A section whose recorded `font_name` is not an accepted identifier for the Times New Roman
face, or whose `font_size_pt` is not 12.0, is `FONT_NONCOMPLIANT`.

**Appendix F — accepted `font_name` identifiers.** These, and only these, denote the
Times New Roman face for the purposes of Rule 2:

- `Times New Roman`
- `TimesNewRomanPSMT`
- `Times New Roman PS MT Std`

Metrically compatible substitutes are not accepted. `Nimbus Roman No9 L`,
`Liberation Serif` and `Tinos` are substitutes, not the face itself.

## Rule 3 — line spacing

Every section must be set at **1.5 line spacing**, annexes included.

Spacing is recorded as a `spacing_mode` and a `spacing_value`. In `multiple` mode the
value is a multiplier and must be 1.5. The treatment of `exact` mode is set by amendment;
see A-5. A section that does not meet the requirement for its mode is
`SPACING_NONCOMPLIANT`.

## Waivers

The thesis office may grant a section a standing waiver of a named rule. Waivers in force
for this dissertation are listed in the submission record. A waiver clears the finding it
names, within the scope it names, and does nothing outside that scope.

## Finding names

`MARGIN_NONCOMPLIANT`, `FONT_NONCOMPLIANT`, `SPACING_NONCOMPLIANT`, `none`.

A section may breach more than one rule. Each rule is assessed on its own and every breach
is reported.

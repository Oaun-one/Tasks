# PRINT-KIT-3 — pre-flight standard for printed activity kits

Studio standard, revision 3. Supersedes PRINT-KIT-2. This is the standard our
pre-flight audit is run against before a kit is released to a press.

## §1 Scope and how findings are reported

Every page in the batch is checked against §2 to §8. Each section of the kit is
checked against §9.

A page carries one finding code for each rule it breaches. A page may breach
several rules at once and every breach is reported; a page that breaches none is
reported as clean.

Two of the rules below take their threshold from the press the page is assigned
to rather than from a single studio-wide number. A page is assigned to a press
through its section: `section_plan.csv` names the press for each section, and
`press_profiles.csv` holds that press's limits. A page must be judged against
the press that is actually going to print it.

## §2 Effective resolution — `DPI_TOO_LOW`

What matters at the press is not the resolution of the artwork file but the
resolution it lands at once it is placed on the page. Placing artwork at a scale
above 100% spreads the same pixels over more paper and lowers the resolution
that reaches the plate; placing it below 100% raises it.

Effective resolution is the artwork resolution divided by the placed scale,
where the scale is expressed as a fraction of full size. Artwork at 300 dpi
placed at 150% is effectively 200 dpi; the same artwork placed at 75% is
effectively 400 dpi. Round the result down to the whole dpi.

Each press has its own minimum effective resolution, given as
`min_effective_dpi` in `press_profiles.csv`. The sheetfed offset press
`PRESS-OFFSET-A` holds a higher floor than the digital press
`PRESS-DIGITAL-B`, which images at a coarser native grid; take both numbers
from the profile rather than assuming one studio-wide floor.

A page whose effective resolution falls below the floor of its own press is
`DPI_TOO_LOW`. A page that meets the floor exactly is acceptable.

## §3 Safe margin — `MARGIN_VIOLATION`

Live copy and any element that must survive trimming has to sit at least
0.125 in inside the trim edge. A page with less than 0.125 in of safe margin is
`MARGIN_VIOLATION`. A page with exactly 0.125 in is acceptable.

**Exception.** A page marked as a full-bleed design in the batch is not subject
to §3. Its artwork is drawn to run off the trim edge, so a thin or absent safe
margin on such a page is the intended design and is not a finding. This
exception releases the page from §3 and from nothing else.

## §4 Bleed allowance — `BLEED_SHORT`

A page marked as a full-bleed design must carry at least 0.125 in of bleed
beyond the trim edge, so that trimming variation cannot open a white edge. A
full-bleed page with less than 0.125 in of bleed is `BLEED_SHORT`; exactly
0.125 in is acceptable.

§4 applies only to full-bleed pages. A page that is not a full-bleed design has
nothing running off the edge, so its bleed allowance is not a finding whatever
it is.

## §5 Total ink coverage — `INK_OVER_LIMIT`

Total area coverage is the sum of the four process inks at the heaviest point of
the page, in percent. A press cannot carry unlimited ink: beyond its cap the
sheet will not dry and will offset onto the next sheet.

Each press has its own cap, given as `max_tac_pct` in `press_profiles.csv`. The
digital press runs a tighter cap than the offset press; take both numbers from
the profile.

A page whose total area coverage exceeds the cap of its own press is
`INK_OVER_LIMIT`. Coverage equal to the cap is acceptable.

## §6 Spot colours — `SPOT_UNSUPPORTED`

Spot colours are mixed inks run in addition to the four process inks. The number
a press can carry is given as `max_spot_colors` in `press_profiles.csv`. A press
whose `max_spot_colors` is zero cannot run spot inks at all, and any spot colour
specified on a page assigned to it must be raised.

A page specifying more spot colours than its own press can carry is
`SPOT_UNSUPPORTED`.

## §7 Font embedding — `FONT_NOT_EMBEDDED`

Every page must arrive with its fonts embedded. A page whose fonts are not
embedded is `FONT_NOT_EMBEDDED`, whichever press it is going to.

## §8 Required elements — `ELEMENT_COUNT_SHORT`

Each page has its own minimum number of required elements, set when the kit was
specified, and carried on the page's own row in the batch. A page carrying fewer
elements than its own minimum is `ELEMENT_COUNT_SHORT`. A page carrying exactly
its minimum is complete, not short.

## §9 Imposition — `IMPOSITION_INVALID`

A section can only be imposed if its page count fits its binding:

| Binding | Page count must be |
| --- | --- |
| `saddle_stitch` | a multiple of 4 |
| `perfect_bound` | a multiple of 2 |
| `flat_sheet` | unconstrained — the pages are cut apart, not bound |

Count the pages actually present in the batch for that section; do not take the
count on trust from elsewhere. A section whose page count does not fit its
binding is `IMPOSITION_INVALID`, and the section has to be repaginated before
the run.

§9 is a property of the section, not of any one page in it. An
`IMPOSITION_INVALID` section is not a finding against its pages.

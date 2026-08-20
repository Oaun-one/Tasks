# Dissertation formatting audit — 6 sections

3 sections flagged.

## SEC-CH2 wrong margin

Chapter margin is 2.0 cm instead of the required 2.5 cm. `MARGIN_NONCOMPLIANT`.

## SEC-CH3 wrong font

Chapter uses Calibri instead of Times New Roman. `FONT_NONCOMPLIANT`.

## SEC-CH4 wrong line spacing

Chapter uses single spacing instead of 1.5. `SPACING_NONCOMPLIANT`.

## SEC-ANNEX-A is the landscape-annex exception, not a defect

SEC-ANNEX-A uses 1.5 cm margins, which looks like the same margin defect as SEC-CH2. But it
is a landscape data annex, and the formatting specification's margin exception for landscape
annexes covers exactly this section — its font and spacing are still fully compliant.
Finding is `none`. Flagging SEC-ANNEX-A here is the false-positive trap.

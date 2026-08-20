# Pre-binding formatting audit - submission TO-2026-0447

Audited against DFS-12 as it stood on the date of submission, **2026-03-09**.
44 sections audited across 8 parts: 28 carry a finding and 16 are clean, with 50 findings raised in total.

## 1. Amendments applied

| Amendment | Effective | Applied? | Reason |
|---|---|---|---|
| A-1 | 2024-06-01 | **No** | Effective before the submission date, but A-2 supersedes it in full and it ceased to have effect on 2025-01-15. Its 2.8 cm binding-edge figure is not the operative one. |
| A-2 | 2025-01-15 | **Yes** | In force. Sets the inner margin minimum at 3.0 cm, and supplies the binding-edge figure the landscape type-area allowance is built from. |
| A-3 | 2025-09-01 | **Yes** | In force. Confines the landscape-annex exception to section 3 alone. |
| A-4 | 2026-07-01 | **No** | Its effective date falls after the 2026-03-09 submission, so it is not yet in force. Body sections stay at 18.0 pt leading, not 24.0 pt. |
| A-5 | 2025-11-01 | **Yes** | In force. Fixes the millimetre conversion at 1 pt = 0.35 mm. |

## 2. Figures derived and used as thresholds

| Figure | TPL-ARCHIVE | TPL-READING | Where it comes from |
|---|---|---|---|
| Inner (binding-edge) margin minimum | 3.0 cm | 3.0 cm | A-2, office-wide rather than per-template |
| Top and bottom margin minimum | 2.5 cm | 2.0 cm | `min_top_bottom_cm` |
| Outer margin minimum | 2.5 cm | 2.0 cm | `min_outer_cm` |
| Heading step above the body size actually used | 2.0 pt | 1.0 pt | `min_heading_step_pt` |
| Landscape type-area allowance | **24.20 cm** | **24.70 cm** | 29.7 cm landscape page width, less the 3.0 cm binding edge, less the template's outer minimum. This is the oversized-table test in section 3, and it is not the same number for both templates. |
| Required leading | 18.0 pt | 18.0 pt | 1.5 times the 12.0 pt body size the standard requires, irrespective of the size a section actually uses; tolerance 0.05 pt |
| Millimetre conversion | 1 pt = 0.35 mm | 1 pt = 0.35 mm | A-5 |

The outer margin is not recorded anywhere. It is implied: page width less the inner margin less the text block width. That implied figure is what section 3 tests.

## 3. Rows audited and rows set aside

The log holds **49 rows** covering **44 section ids**. 5 rows are lower-numbered revisions of a section that also appears at a higher revision, and only the highest revision of each `section_id` is audited. Set aside:

- `SEC-AN-04` rev 1
- `SEC-CH02` rev 1
- `SEC-CH08` rev 1
- `SEC-CH11` rev 1
- `SEC-GLOSSARY` rev 1

**Audited: 44. Set aside: 5.** The export is not sorted, and the current revision sits above the superseded one in some cases and below it in others, so the revision number decides and row position does not. A superseded revision contributes no page extent either, which matters to the pagination below.

## 4. Sections carrying a finding

| Section | Part | Template | Findings | Measured value against the limit |
|---|---|---|---|---|
| `SEC-ABSTRACT` | PART-00 | TPL-ARCHIVE | `MARGIN_NONCOMPLIANT` | inner 2.90 cm against the 3.0 cm binding-edge minimum |
| `SEC-TOC` | PART-00 | TPL-ARCHIVE | `TYPE_AREA_INVALID` `LEADING_NONCOMPLIANT` | implied outer margin 2.45 cm (21.0 less 3.00 less 15.55) against a 2.5 cm minimum; leading 17.5 pt = 17.50 pt against the required 18.0 pt |
| `SEC-LOT` | PART-00 | TPL-ARCHIVE | `NUMBERING_INVALID` | page numbers set in arabic where PART-00 is numbered in roman |
| `SEC-CH02` | PART-01 | TPL-ARCHIVE | `FONT_NONCOMPLIANT` `HEADING_STYLE_INVALID` | body face Liberation Serif is not an Appendix F identifier; heading face Liberation Serif is not an Appendix F identifier |
| `SEC-CH13` | PART-01 | TPL-ARCHIVE | `TYPE_AREA_INVALID` | implied outer margin 1.60 cm (29.7 less 3.00 less 25.10) against a 2.5 cm minimum |
| `SEC-CH03` | PART-02 | TPL-ARCHIVE | `LEADING_NONCOMPLIANT` `CAPTION_MISSING` | leading 5.95 mm = 17.00 pt against the required 18.0 pt; 1 caption against 4 floats, 3 still to write |
| `SEC-CH04` | PART-02 | TPL-ARCHIVE | `HEADING_STYLE_INVALID` `CAPTION_MISSING` | heading face Cambria is not an Appendix F identifier; 4 captions against 6 floats, 2 still to write |
| `SEC-CH05` | PART-02 | TPL-ARCHIVE | `TYPE_AREA_INVALID` `FONT_NONCOMPLIANT` `NUMBERING_INVALID` | implied outer margin 2.40 cm (21.0 less 3.00 less 15.60) against a 2.5 cm minimum; body size 11.0 pt against the required 12.0 pt; page numbers set in roman where PART-02 is numbered in arabic |
| `SEC-CH07` | PART-03 | TPL-READING | `MARGIN_NONCOMPLIANT` | top 1.90 cm against a 2.0 cm minimum |
| `SEC-CH08` | PART-03 | TPL-READING | `TYPE_AREA_INVALID` `HEADING_STYLE_INVALID` | implied outer margin 1.95 cm (21.0 less 3.00 less 16.05) against a 2.0 cm minimum; heading 12.5 pt against the 13.0 pt this template needs (body 12.0 pt plus a 1.0 pt step) |
| `SEC-CH09` | PART-03 | TPL-READING | `LEADING_NONCOMPLIANT` `HEADING_STYLE_INVALID` `NUMBERING_INVALID` | leading 24.0 pt = 24.00 pt against the required 18.0 pt; heading face Liberation Serif is not an Appendix F identifier; page numbers set in roman where PART-03 is numbered in arabic |
| `SEC-CH15` | PART-03 | TPL-READING | `TYPE_AREA_INVALID` | implied outer margin 1.50 cm (29.7 less 3.00 less 25.20) against a 2.0 cm minimum |
| `SEC-CH10` | PART-04 | TPL-READING | `HEADING_STYLE_INVALID` | heading face Cambria is not an Appendix F identifier |
| `SEC-CH12` | PART-04 | TPL-READING | `MARGIN_NONCOMPLIANT` `LEADING_NONCOMPLIANT` `CAPTION_MISSING` | inner 2.80 cm against the 3.0 cm binding-edge minimum; leading 6.65 mm = 19.00 pt against the required 18.0 pt; 1 caption against 3 floats, 2 still to write |
| `SEC-CH16` | PART-04 | TPL-READING | `LEADING_NONCOMPLIANT` | leading 18.1 pt = 18.10 pt against the required 18.0 pt |
| `SEC-GLOSSARY` | PART-05 | TPL-ARCHIVE | `MARGIN_NONCOMPLIANT` `LEADING_NONCOMPLIANT` | top 2.40 cm against a 2.5 cm minimum; leading 5.6 mm = 16.00 pt against the required 18.0 pt |
| `SEC-BIO` | PART-05 | TPL-ARCHIVE | `MARGIN_NONCOMPLIANT` `HEADING_STYLE_INVALID` `NUMBERING_INVALID` | bottom 2.40 cm against a 2.5 cm minimum; heading face Tinos is not an Appendix F identifier; page numbers set in roman where PART-05 is numbered in arabic |
| `SEC-INDEX` | PART-05 | TPL-ARCHIVE | `CAPTION_MISSING` | 4 captions against 7 floats, 3 still to write |
| `SEC-AN-03` | PART-06 | TPL-READING | `TYPE_AREA_INVALID` | implied outer margin 1.60 cm (29.7 less 3.00 less 25.10) against a 2.0 cm minimum |
| `SEC-AN-04` | PART-06 | TPL-READING | `TYPE_AREA_INVALID` `FONT_NONCOMPLIANT` `HEADING_STYLE_INVALID` | implied outer margin 1.80 cm (21.0 less 3.00 less 16.20) against a 2.0 cm minimum; body size 12.5 pt against the required 12.0 pt; heading 13.0 pt against the 13.5 pt this template needs (body 12.5 pt plus a 1.0 pt step) |
| `SEC-AN-05` | PART-06 | TPL-READING | `FONT_NONCOMPLIANT` | body face Courier New is not an Appendix F identifier |
| `SEC-AN-06` | PART-06 | TPL-READING | `MARGIN_NONCOMPLIANT` | inner 2.70 cm against the 3.0 cm binding-edge minimum |
| `SEC-AN-07` | PART-06 | TPL-READING | `LEADING_NONCOMPLIANT` | leading 6.125 mm = 17.50 pt against the required 18.0 pt |
| `SEC-AN-08` | PART-06 | TPL-READING | `CAPTION_MISSING` | 5 captions against 8 floats, 3 still to write |
| `SEC-AN-15` | PART-06 | TPL-READING | `TYPE_AREA_INVALID` | implied outer margin 1.40 cm (29.7 less 3.00 less 25.30) against a 2.0 cm minimum |
| `SEC-AN-10` | PART-07 | TPL-ARCHIVE | `MARGIN_NONCOMPLIANT` `TYPE_AREA_INVALID` `CAPTION_MISSING` | inner 2.85 cm against the 3.0 cm binding-edge minimum; implied outer margin 1.90 cm (29.7 less 2.85 less 24.95) against a 2.5 cm minimum; 2 captions against 5 floats, 3 still to write |
| `SEC-AN-11` | PART-07 | TPL-ARCHIVE | `HEADING_STYLE_INVALID` | heading 13.5 pt against the 14.0 pt this template needs (body 12.0 pt plus a 2.0 pt step) |
| `SEC-AN-14` | PART-07 | TPL-ARCHIVE | `MARGIN_NONCOMPLIANT` `FONT_NONCOMPLIANT` `HEADING_STYLE_INVALID` `CAPTION_MISSING` `NUMBERING_INVALID` | inner 2.60 cm against the 3.0 cm binding-edge minimum; body face Nimbus Roman No9 L is not an Appendix F identifier; heading face Nimbus Roman No9 L is not an Appendix F identifier; 2 captions against 4 floats, 2 still to write; page numbers set in roman where PART-07 is numbered in arabic |

## 5. Sections the standard clears despite their numbers

- `SEC-LOF` has an implied outer margin of 1.90 cm against TPL-ARCHIVE's 2.5 cm minimum. Waiver **W-3** covers section 3 for this section and runs to 2026-11-30, so there is no type-area finding. It clears nothing else.
- `SEC-CH07` carries 5 floats against 3 captions. Waiver **W-4** covers section 7 for this section and runs to 2026-06-30, so there is no caption finding. Its 1.90 cm top margin is a separate section 2 breach and stands.
- `SEC-AN-01` is set in Courier New. Waiver **W-1** covers the body font identifier and runs to 2026-12-31, so the face is cleared and its 12.0 pt size is compliant on its own. Its 1.20 cm implied outer margin is released by the landscape-annex exception, its 26.0 cm table being wider than TPL-READING's 24.70 cm allowance.
- `SEC-AN-05` looks like the same case and is not. Waiver **W-2** expired on **2026-01-31**, before the submission date, so it clears nothing and the Courier New body face is `FONT_NONCOMPLIANT`. Its margins are still released by the exception.
- `SEC-AN-02`, `SEC-AN-09` and `SEC-AN-12` sit inside their template's outer margin minimum on paper and are cleared by the landscape-annex exception.
- `SEC-AN-06` is the reverse case. The exception releases its 1.10 cm implied outer margin, but the binding edge is outside every exception and its 2.70 cm inner margin is a section 2 breach.
- `SEC-CH05` carries an 11.0 pt body and a 13.0 pt heading. The heading is compliant: the step is measured above the size the section actually uses, so 13.0 pt clears 11.0 plus 2.0. Only the body size is a finding.
- `SEC-AN-13` is at 18.04 pt leading, inside the 0.05 pt tolerance, and is clean; `SEC-CH16` at 18.10 pt is outside it and is not.
- `SEC-ABBREV` and `SEC-AN-16` sit at an implied outer margin of exactly 2.50 cm, which is TPL-ARCHIVE's minimum. Exactly at a minimum is compliant, so neither is a finding. `SEC-CH14` is the same case on the heading step: 14.0 pt against a 12.0 pt body and a 2.0 pt step is exactly enough.
- `SEC-AN-15` is the reverse. Its widest table is 24.70 cm, exactly TPL-READING's landscape allowance. The exception needs a table *greater than* the allowance, so it does not apply and the 1.40 cm implied outer margin is a finding.
- `SEC-CH13` and `SEC-CH15` are landscape and carry genuinely oversized tables, at 26.0 cm and 28.0 cm. Neither is an annex, and the exception reaches annexes only, so both are `TYPE_AREA_INVALID`.

## 6. Sections whose verdict turns on the template

- `SEC-AN-03` sits in PART-06, which is set in **TPL-READING**, and comes out `TYPE_AREA_INVALID`. Its widest table is 24.4 cm. Under **TPL-ARCHIVE** the landscape allowance would be 24.20 cm rather than 24.70 cm, and the same section would come out `MARGIN_NONCOMPLIANT|HEADING_STYLE_INVALID`.
- `SEC-AN-15` sits in PART-06, which is set in **TPL-READING**, and comes out `TYPE_AREA_INVALID`. Its widest table is 24.7 cm. Under **TPL-ARCHIVE** the landscape allowance would be 24.20 cm rather than 24.70 cm, and the same section would come out `MARGIN_NONCOMPLIANT|HEADING_STYLE_INVALID`.
- `SEC-AN-09` sits in PART-07, which is set in **TPL-ARCHIVE**, and comes out `none`. Its widest table is 24.3 cm. Under **TPL-READING** the landscape allowance would be 24.70 cm rather than 24.20 cm, and the same section would come out `TYPE_AREA_INVALID`.

## 7. Pagination

Pages run continuously from 1 in `sequence` order across the audited sections only.

| Part | Template | Sections | Flagged | Opens on | Pagination |
|---|---|---|---|---|---|
| `PART-00` | TPL-ARCHIVE | 8 | 3 | 1 | none |
| `PART-01` | TPL-ARCHIVE | 3 | 2 | 17 | none |
| `PART-02` | TPL-ARCHIVE | 4 | 3 | 49 | none |
| `PART-03` | TPL-READING | 5 | 4 | 83 | none |
| `PART-04` | TPL-READING | 4 | 3 | 134 | PAGINATION_INVALID |
| `PART-05` | TPL-ARCHIVE | 4 | 3 | 164 | PAGINATION_INVALID |
| `PART-06` | TPL-READING | 9 | 7 | 190 | PAGINATION_INVALID |
| `PART-07` | TPL-ARCHIVE | 7 | 3 | 237 | none |

**3 parts cannot be paginated as planned.** `PART-04` opens on page 134. `PART-05` opens on page 164. `PART-06` opens on page 190. Every part must open on a recto, that is on an odd page, and each of these opens on an even one. Both have to be repaginated before the volume is bound.

## 8. Captions outstanding

**18 captions** are still to be written across the batch, over the 7 sections carrying `CAPTION_MISSING`:

- `SEC-CH03`: 4 floats, 1 captions, 3 outstanding
- `SEC-CH04`: 6 floats, 4 captions, 2 outstanding
- `SEC-CH12`: 3 floats, 1 captions, 2 outstanding
- `SEC-INDEX`: 7 floats, 4 captions, 3 outstanding
- `SEC-AN-08`: 8 floats, 5 captions, 3 outstanding
- `SEC-AN-10`: 5 floats, 2 captions, 3 outstanding
- `SEC-AN-14`: 4 floats, 2 captions, 2 outstanding

## 9. Where the findings fall

14 of the flagged sections sit in parts set in TPL-ARCHIVE and 14 in parts set in TPL-READING. 17 audited sections sit inside a part that cannot be paginated as planned and will move when those parts are repaginated.

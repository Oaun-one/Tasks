# Formatting pre-check — submission TO-2026-0447

Audited against DFS-11 as it stood on the date of submission, **2026-03-09**.
30 sections audited, 18 flagged.

## 1. Amendments applied

| Amendment | Effective | Applied? | Reason |
|---|---|---|---|
| A-1 | 2024-06-01 | **No** | Effective before the submission date, but A-2 supersedes it in full and it ceased to have effect on 2025-01-15. Its 2.8 cm binding-edge minimum is not the operative figure. |
| A-2 | 2025-01-15 | **Yes** | In force. Sets the inner (binding-edge) minimum at 3.0 cm for every section. |
| A-3 | 2025-09-01 | **Yes** | In force. Narrows the Rule 1 exception and confirms the binding edge is never exempt. |
| A-4 | 2026-07-01 | **No** | Effective date falls *after* the 2026-03-09 submission, so it is not yet in force. Body sections remain at 1.5 line spacing, not double. |
| A-5 | 2025-11-01 | **Yes** | In force. Fixes the compliant exact leading at 18.0 pt. |

## 2. Figures derived and used as thresholds

| Figure | Value | Where it comes from |
|---|---|---|
| Inner (binding-edge) margin minimum | **3.0 cm** | A-2 |
| Top / bottom / outer margin minimum | **2.5 cm** | Rule 1, unamended |
| Printable width of a landscape page | **24.2 cm** | 29.7 cm physical width − 3.0 cm inner (A-2) − 2.5 cm outer. This is the oversized-table test in A-3(3): an annex qualifies only where `widest_table_cm` > 24.2. |
| Compliant exact leading | **18.0 pt** | A-5: 1.5 × the 12.0 pt Rule 2 requires, irrespective of the size a section actually uses |

## 3. Rows audited and rows set aside

The log holds **35 rows** covering **30 `section_id`s**. Five rows are lower-numbered
revisions of a section that also appears at a higher revision, and under the specification's
scope rule only the highest revision of each `section_id` is audited. Set aside:

- `SEC-CH1` rev 1 (superseded by rev 2)
- `SEC-CH3` rev 1 (superseded by rev 2)
- `SEC-CH5` rev 1 (superseded by rev 2)
- `SEC-AN-05` rev 1 (superseded by rev 2)
- `SEC-AN-07` rev 1 (superseded by rev 2)

The export is not sorted and in two cases the current revision appears above the superseded
one, so the revision number, not row position, decides. Two of these matter to the result:
`SEC-CH1` rev 1 is set in Arial and `SEC-CH3` rev 1 is compliant, so auditing the wrong row
would flag `SEC-CH1` and clear `SEC-CH3`.

**Audited: 30. Set aside: 5.**

## 4. Waivers

- **W-1** (`SEC-AN-01`, Rule 2 font identifier) expires 2026-12-31 — **in force**. Courier New
  is cleared; the 12.0 pt size requirement still applies and is met.
- **W-2** (`SEC-AN-03`, Rule 2 font identifier) expired **2026-01-31**, before the submission
  date — **not in force**. Courier New is not cleared and the finding stands.
- **W-3** (`SEC-LOF`, Rule 1 outer margin) is in force but has nothing to clear: `SEC-LOF`
  meets Rule 1 on all four sides. It does not touch that section's spacing finding.

## 5. Flagged sections

| Section | Finding | Measured value responsible |
|---|---|---|
| `SEC-ABSTRACT` | `MARGIN_NONCOMPLIANT` | inner 2.9 cm, below the 3.0 cm binding-edge minimum |
| `SEC-ACK` | `MARGIN_NONCOMPLIANT` | inner 2.85 cm, below 3.0 cm |
| `SEC-LOF` | `SPACING_NONCOMPLIANT` | exact leading 12.0 pt, not 18.0 pt |
| `SEC-CH2` | `MARGIN_NONCOMPLIANT` | top 2.49 cm, below 2.5 cm |
| `SEC-CH3` | `FONT_NONCOMPLIANT` | Liberation Serif — a metric substitute, not an accepted identifier |
| `SEC-CH4` | `FONT_NONCOMPLIANT\|SPACING_NONCOMPLIANT` | 11.0 pt, not 12.0 pt; exact leading 16.5 pt, not 18.0 pt. 16.5 pt is 1.5 × this section's own 11.0 pt, but A-5 fixes the bar at 18.0 pt whatever size the section uses. |
| `SEC-CH5` | `SPACING_NONCOMPLIANT` | multiple 2.0, not 1.5. Double spacing would be correct only under A-4, which is not yet in force. |
| `SEC-CH7` | `MARGIN_NONCOMPLIANT` | outer 1.8 cm, below 2.5 cm. Landscape with a 26.4 cm table, but its `section_type` is `body`, so A-3 does not reach it. |
| `SEC-CH8` | `MARGIN_NONCOMPLIANT\|FONT_NONCOMPLIANT\|SPACING_NONCOMPLIANT` | top 2.2 cm; Cambria; exact leading 21.0 pt |
| `SEC-CH9` | `FONT_NONCOMPLIANT` | 12.5 pt, not 12.0 pt |
| `SEC-GLOSSARY` | `MARGIN_NONCOMPLIANT` | inner 2.8 cm — exactly the superseded A-1 figure, and below the operative 3.0 cm |
| `SEC-BIO` | `MARGIN_NONCOMPLIANT` | outer 2.4 cm, below 2.5 cm |
| `SEC-AN-03` | `FONT_NONCOMPLIANT` | Courier New, with W-2 expired |
| `SEC-AN-05` | `MARGIN_NONCOMPLIANT` | outer 1.9 cm, below 2.5 cm. Its widest table is 24.0 cm, which is not greater than 24.2 cm, so the section is not an oversized-table annex and the exception does not apply. |
| `SEC-AN-06` | `MARGIN_NONCOMPLIANT` | outer 1.8 cm, below 2.5 cm. An annex, but portrait, so A-3(2) is not satisfied. |
| `SEC-AN-07` | `MARGIN_NONCOMPLIANT` | inner 2.6 cm, below 3.0 cm. The exception *does* apply to this section and clears its 2.0 / 2.0 / 1.5 cm top, bottom and outer margins — but A-3 puts the binding edge outside every exception, so the finding stands. |
| `SEC-AN-08` | `SPACING_NONCOMPLIANT` | exact leading 16.0 pt, not 18.0 pt |
| `SEC-AN-09` | `FONT_NONCOMPLIANT` | Nimbus Roman No9 L — a metric substitute, not an accepted identifier |

The remaining 12 audited sections carry no finding.

## 6. Where the Rule 1 exception applies

It applies to eight sections — every annex that is landscape **and** carries a table wider
than 24.2 cm:

| Section | Widest table | Outcome |
|---|---|---|
| `SEC-AN-01` | 27.6 cm | Exception applies; 1.6 / 1.6 / 1.4 cm cleared. No margin finding. |
| `SEC-AN-02` | 24.9 cm | Exception applies. No margin finding. |
| `SEC-AN-03` | 25.4 cm | Exception applies. Its finding is font, not margin. |
| `SEC-AN-04` | 24.3 cm | Exception applies — 24.3 > 24.2. Under the superseded A-1 the printable width would be 24.4 cm and this section would be flagged; A-2 is what makes it compliant. |
| `SEC-AN-07` | 28.0 cm | Exception applies to top, bottom and outer, but the binding edge is still short. Flagged. |
| `SEC-AN-08` | 26.2 cm | Exception applies. Its finding is spacing, not margin. |
| `SEC-AN-09` | 25.0 cm | Exception applies. Its finding is font, not margin. |
| `SEC-AN-10` | 24.6 cm | Exception applies — 24.6 > 24.2. With no binding-edge amendment applied the threshold would be 24.7 cm and this section would be flagged. |

It does **not** reach three sections that resemble candidates:

- `SEC-AN-05` — an annex, landscape, but its widest table is 24.0 cm and is not oversized.
- `SEC-AN-06` — an annex with a table, but portrait.
- `SEC-CH7` — landscape with a genuinely oversized 26.4 cm table, but `section_type` is
  `body`; A-3(1) restricts the exception to annexes.

# DFS-11 amendments

Graduate Thesis Office. Amendments to the base specification, in order of issue.

Each amendment states its own **effective date**. An amendment is in force for a
dissertation if its effective date falls on or before that dissertation's date of
submission. An amendment that is not in force has no bearing on the audit, however
recently it was published.

---

## A-1 — binding-edge margin

**Effective 2024-06-01.**

The binding edge is the inner margin. Rule 1's minimum for the **inner** margin is raised
from 2.5 cm to **2.8 cm** for every section, so that text is not lost into the gutter when
the volume is bound. The minimum for the top, bottom and outer margins is unchanged.

---

## A-2 — binding-edge margin, revised

**Effective 2025-01-15.**

**A-1 is superseded in full and ceases to have effect on this date.** Trial binding of the
2024 intake showed 2.8 cm to be insufficient for volumes over 300 pages. Rule 1's minimum
for the **inner** margin is **3.0 cm** for every section. The minimum for the top, bottom
and outer margins remains 2.5 cm.

---

## A-3 — landscape data annexes, narrowed

**Effective 2025-09-01.**

The Rule 1 exception for landscape data annexes was being read too broadly. It applies to a
section only where **all three** of the following hold:

1. its `section_type` is `annex`;
2. its `orientation` is `landscape`; and
3. it carries an **oversized table** — that is, its `widest_table_cm` is greater than the
   printable width of a landscape page under the margins this specification requires.

Where the exception applies, it relieves the section of the Rule 1 minimum on the **top,
bottom and outer** margins only.

**The binding-edge (inner) minimum is not subject to this or any other exception.** It
applies to every section of the dissertation without exception, annexes included.

Where the exception does not apply, Rule 1 applies to the section in full, whatever the
section is called.

---

## A-4 — line spacing for body sections

**Effective 2026-07-01.**

Rule 3's requirement for sections of `section_type` `body` becomes **double (2.0) line
spacing**; in `exact` mode the equivalent is 24.0 pt. Front matter, back matter and annexes
are unaffected and remain at 1.5.

---

## A-5 — exact leading

**Effective 2025-11-01.**

Rule 3 may be recorded either as a multiplier (`spacing_mode` = `multiple`) or as an exact
leading in points (`spacing_mode` = `exact`).

A section recorded in `exact` mode complies with Rule 3 only where its `spacing_value` is
**18.0 pt** — 1.5 times the 12.0 pt that Rule 2 requires — **irrespective of the font size
the section actually uses**. A section set at some other size does not get a proportionally
smaller leading; it gets a Rule 2 finding and a Rule 3 finding.

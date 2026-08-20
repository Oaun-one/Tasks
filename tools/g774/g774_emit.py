#!/usr/bin/env python3
"""Writes the hardened gen-g774 package from the model in g774_build.py."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g774_build import (  # noqa: E402
    BASE_MIN_ELEMENTS, CODES, FIELDS, IMPOSITION_MULTIPLE, PKG, REV_B_UPLIFT,
    SECTIONS, STOCKS, as_dicts, effective_dpi, gold, margin_exempt, min_elements,
)

INPUT = PKG / "environment" / "input"
SOLUTION = PKG / "solution" / "files"
TESTS = PKG / "tests"

CLEAN_SYNONYMS = (
    r"(?:\b(?:none|no[ _-]?finding(?:s)?|ok|okay|pass(?:es|ed)?|clean|clear|compliant"
    r"|conform(?:s|ing)?|valid|fine|good|yes|true|n/?a)\b|(?:^|,)\s*[-–—✓]\s*(?:,|$))"
)


def fmt(value):
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


# --------------------------------------------------------------------------- inputs

def write_inputs():
    INPUT.mkdir(parents=True, exist_ok=True)

    lines = [",".join(FIELDS)]
    for row in as_dicts():
        lines.append(",".join(fmt(row[f]) for f in FIELDS))
    (INPUT / "activity_kit_pages.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    sec = ["section_id,section_name,binding,stock_code"]
    for sid, s in SECTIONS.items():
        sec.append(f"{sid},{s['name']},{s['binding']},{s['stock_code']}")
    (INPUT / "kit_sections.csv").write_text("\n".join(sec) + "\n", encoding="utf-8")

    st = ["stock_code,stock_name,min_dpi,min_margin_in,max_ink_pct,min_bleed_in"]
    for code, s in STOCKS.items():
        st.append(f"{code},{s['name']},{s['min_dpi']},{s['min_margin_in']},"
                  f"{s['max_ink_pct']},{s['min_bleed_in']}")
    (INPUT / "stock_profiles.csv").write_text("\n".join(st) + "\n", encoding="utf-8")

    elem_table = "\n".join(f"| `{t}` | {n} |" for t, n in BASE_MIN_ELEMENTS.items())
    imp_table = "\n".join(f"| `{b}` | a multiple of {m} |"
                          for b, m in IMPOSITION_MULTIPLE.items())
    standard = f"""# Printable activity-kit production standard (PRINT-KIT-2)

Binding for the artwork batch in `activity_kit_pages.csv`. §2–§7 are checked against every
live page; §8 is checked against every section.

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

**The exemption is limited to saddle-stitched sections.** Perfect binding glues the spine
edge, so a perfect-bound page has no bleed on that edge and its live copy still has to clear
the trim: a full-bleed page in a `perfect_bound` section is judged under §3 exactly like any
other page. Only a full-bleed page in a `saddle_stitch` section is released from §3.

Every full-bleed page, whatever its binding, carries an obligation no other page carries: it
must be supplied with `bleed_in` of at least the stock's `min_bleed_in`, or the trim eats
into the art. Below it is `BLEED_SHORT`. `bleed_in` on a page that is not full-bleed is not
assessed.

## 5. Ink coverage

`total_ink_pct` must not exceed the stock's `max_ink_pct`. Above it is `INK_OVER`.

## 6. Required elements

Each page type carries a minimum number of required elements:

| page_type | minimum |
| --- | --- |
{elem_table}

**Amendment Rev B.** A saddle-stitched section is trimmed harder at the outer edge, so its
detachable-element pages have to be supplied with spares. In a section bound
`saddle_stitch`, the minimum for `mission_cards` and for `badge_certificate` is
{REV_B_UPLIFT} higher than the table above. No other page type and no other binding is
affected.

A page below its own minimum is `ELEMENT_COUNT_SHORT`. A page's shortfall is its minimum
less its `element_count`; a page at or above its minimum has a shortfall of zero.

## 7. Findings

`finding` is one or more of `DPI_TOO_LOW`, `MARGIN_VIOLATION`, `BLEED_SHORT`, `INK_OVER`,
`ELEMENT_COUNT_SHORT`, joined with `|`, or `none` for a page that breaches nothing.

## 8. Imposition

A page carrying `ELEMENT_COUNT_SHORT` cannot go to press as it stands: it is **held back**
for re-supply and does not sit in the imposition. What has to impose is the section's live
page count *less* the pages held back.

That imposed count has to fit the section's binding:

| binding | imposed page count must be |
| --- | --- |
{imp_table}

A section whose imposed page count does not fit its binding is `IMPOSITION_INVALID` and has
to be repaginated before the run; the pages it needs is the number that would carry it up to
the next multiple. A section that fits is `none`.

§8 is a property of the section, not of any page in it: an `IMPOSITION_INVALID` section is
not a finding against its pages, and a section with no flagged pages at all can still fail
to impose.
"""
    (INPUT / "activity_kit_print_standard.md").write_text(standard, encoding="utf-8")


# --------------------------------------------------------------------- instruction

def write_instruction():
    text = """# Task

The activity kit goes to the printer on Friday and I need a pre-flight pass over the
batch before it does. Everything is in `input/`: the artwork batch, the section list
saying how each section is bound and which stock it runs on, the stock profiles, and
our PRINT-KIT-2 standard.

Apply the standard as written. Most of the limits belong to the paper stock rather than
to the kit, parts of the batch have been re-supplied since the first drop, and the
standard carries an amendment — each of those changes which pages are actually in
breach. The sections carry a rule of their own, and it reads the page audit.

Save `activity_kit_audit.csv` with one row per audited page, keyed by `page_id`, and a
`finding` column carrying the code for every rule that page breaches — join multiple
codes with `|`, and use `none` for a page that breaches nothing.

Save `section_summary.csv` with one row per section and the columns `section_id`,
`binding`, `stock_code`, `live_page_count`, `held_back`, `imposed_page_count`,
`flagged_pages`, `imposition`, in that order, using the same `none` convention in
`imposition` for a section that imposes cleanly.

Then write `activity_kit_memo.md` for the studio. Account for every page carrying a
finding, naming the measured value and the limit it missed. Where a page's numbers look
like a breach but the standard clears it, say what clears it. Say which artwork the
batch supersedes and what that changes. Give me the limits you actually applied — the
stocks in this kit and their resolution floors, ink caps, margin floors and bleed
minimums. Cover every section, and name the ones that cannot be imposed with the number
of pages each of them needs. And state the batch totals: how many pages are clear, how
many carry a finding, and how many required elements the batch is missing altogether.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `activity_kit_audit.csv` — Per-page print-production audit
    - `section_summary.csv` — Per-section rollup
    - `activity_kit_memo.md` — Markdown memo for the studio
    - `results.json` — a JSON object with the keys `page_count` (pages audited),
      `superseded_count` (artwork rows the batch supersedes), `section_count`,
      `clean_count`, `flagged_count`, `finding_total` (every finding raised across the
      batch, not the number of pages carrying one), `dpi_low_count`, `margin_count`,
      `bleed_short_count`, `ink_over_count`, `element_short_count` (each of these five
      counting the pages carrying that finding), `element_shortfall_total` (how many
      required elements the batch is missing in total), `imposition_invalid_sections`
      and `imposition_shortfall_total` (how many pages those sections need between them)
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.
"""
    (PKG / "instruction.md").write_text(text, encoding="utf-8")


# ------------------------------------------------------------------------ solution

SECTION_COLUMNS = ["section_id", "binding", "stock_code", "live_page_count",
                   "held_back", "imposed_page_count", "flagged_pages", "imposition"]


def write_solution(live, verdicts, shortfalls, rollup, results):
    SOLUTION.mkdir(parents=True, exist_ok=True)

    rows = ["page_id,page_name,section_id,stock_code,finding"]
    for r in live:
        stock = SECTIONS[r["section_id"]]["stock_code"]
        finding = "|".join(verdicts[r["page_id"]]) or "none"
        rows.append(f"{r['page_id']},{r['page_name']},{r['section_id']},{stock},{finding}")
    (SOLUTION / "activity_kit_audit.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")

    srows = [",".join(SECTION_COLUMNS)]
    for s in rollup.values():
        srows.append(",".join(str(s[c]) for c in SECTION_COLUMNS))
    (SOLUTION / "section_summary.csv").write_text("\n".join(srows) + "\n", encoding="utf-8")

    (SOLUTION / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    clean = [r["page_id"] for r in live if not verdicts[r["page_id"]]]

    def detail(pid):
        r = next(x for x in live if x["page_id"] == pid)
        sec = SECTIONS[r["section_id"]]
        st = STOCKS[sec["stock_code"]]
        bits = []
        for code in verdicts[pid]:
            if code == "DPI_TOO_LOW":
                bits.append(f"effective resolution {effective_dpi(r)} dpi "
                            f"({r['artwork_dpi']} dpi placed at {r['placement_scale_pct']}%) "
                            f"against a {st['min_dpi']} dpi floor on {sec['stock_code']}")
            elif code == "MARGIN_VIOLATION":
                extra = (" — full-bleed, but the section is perfect-bound, so §4 does not "
                         "release it from §3" if r["full_bleed_design"] else "")
                bits.append(f"safe margin {r['margin_in']} in against a "
                            f"{st['min_margin_in']} in floor on {sec['stock_code']}{extra}")
            elif code == "BLEED_SHORT":
                bits.append(f"bleed allowance {r['bleed_in']} in against a "
                            f"{st['min_bleed_in']} in minimum on {sec['stock_code']}")
            elif code == "INK_OVER":
                bits.append(f"total ink {r['total_ink_pct']}% against a "
                            f"{st['max_ink_pct']}% cap on {sec['stock_code']}")
            else:
                need = min_elements(r["page_type"], r["section_id"])
                bits.append(f"{r['element_count']} required elements against a minimum of "
                            f"{need} for a `{r['page_type']}` page in a "
                            f"{sec['binding']} section (short by {shortfalls[pid]})")
        return (f"- **{pid} {r['page_name']}** ({r['section_id']}, {sec['stock_code']}) — "
                f"`{'|'.join(verdicts[pid])}`: " + "; ".join(bits) + ".")

    flagged_lines = "\n".join(detail(r["page_id"]) for r in live if verdicts[r["page_id"]])

    stock_lines = "\n".join(
        f"| `{code}` | {s['min_dpi']} dpi | {s['max_ink_pct']}% | {s['min_margin_in']} in | "
        f"{s['min_bleed_in']} in |" for code, s in STOCKS.items())

    section_lines = "\n".join(
        f"| {s['section_id']} | {s['binding']} | {s['stock_code']} | {s['live_page_count']} | "
        f"{s['held_back']} | {s['imposed_page_count']} | {s['flagged_pages']} | "
        f"{s['imposition']}" + (f" (needs {s['pages_needed']})" if s["pages_needed"] else "")
        + " |" for s in rollup.values())

    invalid = [s for s in rollup.values() if s["imposition"] != "none"]
    invalid_lines = "\n".join(
        f"- **{s['section_id']}** ({s['binding']}) imposes {s['imposed_page_count']} pages "
        f"after {s['held_back']} held back from {s['live_page_count']} live — needs "
        f"{s['pages_needed']} more to reach a multiple of "
        f"{IMPOSITION_MULTIPLE[s['binding']]}." for s in invalid)

    superseded = sorted({r["page_id"] for r in as_dicts()} &
                        {r["page_id"] for r in as_dicts() if
                         sum(1 for x in as_dicts() if x["page_id"] == r["page_id"]) > 1})

    memo = f"""# Activity-kit pre-flight — PRINT-KIT-2

{results['page_count']} live pages audited out of {results['page_count'] + results['superseded_count']}
artwork rows, across {results['section_count']} sections. **{results['clean_count']} pages are
clear** and **{results['flagged_count']} carry at least one finding**, {results['finding_total']}
findings in total. {results['imposition_invalid_sections']} sections cannot be imposed as planned.

## Superseded artwork

The batch carries more than one revision of {len(superseded)} pages, and only the highest
revision of a `page_id` is live (§0). Those {results['superseded_count']} lower-revision rows
are superseded and were **not** audited: {', '.join(superseded)}.

Row order is not the tie-break — `revision` is. PG-12, PG-27, PG-33 and PG-35 have their live
revision *earlier* in the file than the superseded one; PG-04 and PG-18 have it later. Taking
the first row per page, or the last, gets a different answer from taking the highest revision.

Auditing the superseded rows instead of the live ones changes six verdicts and every derived
figure. PG-27 runs the other way from the rest: rev 1 was 200 dpi and would have been
`DPI_TOO_LOW`, while the live rev 2 is placed at 200% from 480 dpi artwork and clears the
floor exactly.

## The limits actually applied

Every limit in §2–§5 belongs to the **stock**, reached through the page's section
(`page` → `section` → `stock`):

| stock | min effective resolution | max total ink | min safe margin | min bleed |
| --- | --- | --- | --- | --- |
{stock_lines}

So the same number lands on either side of the line depending on the section: PG-13 at 298%
ink is clear on BRD-250 and PG-28 at 241% is over on UNC-120 — the smaller number is the
breach.

Resolution is judged on the **effective** figure, not the supplied one: `artwork_dpi` divided
by the placement scale (§2). PG-06 is supplied at 450 dpi and only prints at 300 because it is
placed at 150%; PG-20 is supplied at 240 dpi and prints at 300 because it is placed at 80%.
Reading `artwork_dpi` straight off the row gets both of them wrong.

Every limit is inclusive (§1). PG-05, PG-16, PG-22, PG-27 and PG-34 all sit exactly on at
least one limit and are clear because of it.

## Full bleed: exempt from the margin, and only in a saddle-stitched section

Full-bleed pages in saddle-stitched sections are exempt from §3 — PG-07, PG-10, PG-25 and
PG-32 all carry margins well under their stock's floor and are clear on it. Flagging them is
the commonest false positive here.

But the exemption stops at the binding (§4). A perfect-bound page is glued on the spine and
has no bleed there, so PG-01, PG-02, PG-18, PG-29 and PG-35 are full-bleed *and* carry
`MARGIN_VIOLATION`. Reading the exemption as a blanket pass clears five pages wrongly;
applying §3 to every full-bleed page flags four wrongly.

Full-bleed is also the only status that owes a bleed allowance, and PG-02, PG-18 and PG-25 are
short of their stock's minimum. Pages that are not full-bleed are not assessed on bleed at
all: PG-30 carries 0.30 in of bleed and it is neither a credit nor a finding.

## Required elements and Amendment Rev B

Minimums come from the page-type table in §6, raised by {REV_B_UPLIFT} for `mission_cards` and
`badge_certificate` in a `saddle_stitch` section. PG-19 (6 mission cards, perfect-bound) is
clear on exactly the count that makes PG-13 (6 mission cards, saddle-stitched) short by 2.
**The batch is missing {results['element_shortfall_total']} required elements in total**
across {results['element_short_count']} pages.

## Findings by page

{flagged_lines}

## Pages that clear the standard

{', '.join(clean)} — no finding.

## Sections

§8 reads the page audit, not the raw batch: a page carrying `ELEMENT_COUNT_SHORT` is held
back for re-supply and leaves the imposition.

| section | binding | stock | live | held back | imposed | flagged | imposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
{section_lines}

Cannot be imposed as planned:

{invalid_lines}

The hold-back is what decides three of these. SEC-05 has 4 live pages, which fits a
saddle-stitch multiple of 4 on its own, and still fails once PG-25 is held back. SEC-06 (5
live) and SEC-08 (3 live) both look wrong on the raw count and both impose cleanly once a
held-back page is removed. Between them the invalid sections need
{results['imposition_shortfall_total']} pages.

## Totals

| figure | value |
| --- | --- |
| pages audited | {results['page_count']} |
| superseded artwork rows | {results['superseded_count']} |
| sections | {results['section_count']} |
| clear | {results['clean_count']} |
| flagged | {results['flagged_count']} |
| findings raised | {results['finding_total']} |
| `DPI_TOO_LOW` pages | {results['dpi_low_count']} |
| `MARGIN_VIOLATION` pages | {results['margin_count']} |
| `BLEED_SHORT` pages | {results['bleed_short_count']} |
| `INK_OVER` pages | {results['ink_over_count']} |
| `ELEMENT_COUNT_SHORT` pages | {results['element_short_count']} |
| required elements missing | {results['element_shortfall_total']} |
| sections that cannot be imposed | {results['imposition_invalid_sections']} |
| pages those sections need | {results['imposition_shortfall_total']} |
"""
    (SOLUTION / "activity_kit_memo.md").write_text(memo, encoding="utf-8")


# ----------------------------------------------------------------------- verifiers

def file_verifier(name, how, why, pattern, path, ftype, comparison="regex_match"):
    return {
        "name": name,
        "metadata": {"how_justification": how, "why_justification": why},
        "source": {"type": "file", "file": {"type": ftype, "command": "extract_text",
                                            "arguments": {"path": path}}},
        "assertion": {"type": "deterministic", "expected": pattern,
                      "deterministic": {"path": "$.text", "comparison": comparison}},
    }


def audit_v(name, how, why, pattern, comparison="regex_match"):
    return file_verifier(name, how, why, pattern, "activity_kit_audit.csv", "csv", comparison)


def section_v(name, how, why, pattern, comparison="regex_match"):
    return file_verifier(name, how, why, pattern, "section_summary.csv", "csv", comparison)


def memo_v(name, how, why, pattern):
    return file_verifier(name, how, why, pattern, "activity_kit_memo.md", "md")


def exists_v(name, path, why):
    return {
        "name": name,
        "metadata": {"how_justification": f"Checks {path} is present as a file in the workspace.",
                     "why_justification": why},
        "source": {"type": "file", "file": {"type": "filesystem", "command": "check_path_exists",
                                            "arguments": {"path": path}}},
        "assertion": {"type": "deterministic", "expected": True,
                      "deterministic": {"path": "$.is_file", "comparison": "equals"}},
    }


def json_v(name, key, value, why):
    return {
        "name": name,
        "metadata": {"how_justification": f"Reads results.json with json.read_file and compares $.{key}.",
                     "why_justification": why},
        "source": {"type": "file", "file": {"type": "json", "command": "read_file",
                                            "arguments": {"path": "results.json"}}},
        "assertion": {"type": "deterministic", "expected": value,
                      "deterministic": {"path": f"$.{key}", "comparison": "equals"}},
    }


def page_pattern(codes):
    parts = [rf"(?=[^\n]*\b{c}\b)" for c in codes] if codes else [rf"(?=[^\n]*{CLEAN_SYNONYMS})"]
    parts += [rf"(?![^\n]*\b{c}\b)" for c in CODES if c not in codes]
    return "".join(parts)


def anywhere(*tokens):
    return "(?is)^" + "".join(rf"(?=[\s\S]*{t})" for t in tokens)


def build_verifiers(live, verdicts, shortfalls, rollup, results):
    page_ids = [r["page_id"] for r in live]
    flagged = [p for p in page_ids if verdicts[p]]
    invalid = [s for s in rollup.values() if s["imposition"] != "none"]

    v = [
        exists_v("audit_csv_exists", "activity_kit_audit.csv", "The per-page audit is the primary deliverable."),
        exists_v("section_csv_exists", "section_summary.csv", "The per-section rollup is a named deliverable."),
        exists_v("memo_exists", "activity_kit_memo.md", "The studio memo is a named deliverable."),
        exists_v("results_exists", "results.json", "The derived figures are a named deliverable."),
        audit_v("audit_has_page_id_and_finding_columns",
                "Requires one line of activity_kit_audit.csv to name both a page_id and a finding column.",
                "The prompt asks for the audit keyed by `page_id` with a `finding` column.",
                r"(?im)^(?=[^\n]*\bpage_id\b)(?=[^\n]*\bfinding\b)"),
        audit_v("audit_has_no_pages_outside_batch",
                "Requires activity_kit_audit.csv to carry no page id outside PG-01..PG-36.",
                "An audit that invents pages is not an audit of this batch.",
                r"PG-(?:00|3[7-9]|[4-9]\d)", comparison="not_regex_match"),
        audit_v("audit_has_one_row_per_page",
                "Requires no page id in activity_kit_audit.csv to appear on two different lines.",
                "The batch carries superseded artwork; an audit emitted per artwork row rather "
                "than per live page duplicates page ids and is not the deliverable asked for.",
                r"(?ms)^[^\n]*\b(PG-(?:0[1-9]|[12]\d|3[0-6]))\b.*?^[^\n]*\b\1\b",
                comparison="not_regex_match"),
    ]

    for pid in page_ids:
        row = next(r for r in live if r["page_id"] == pid)
        sec = SECTIONS[row["section_id"]]
        codes = verdicts[pid]
        why = (f"{pid} ({row['page_name']}, {row['section_id']} on {sec['stock_code']}, "
               f"{sec['binding']}) breaches exactly {', '.join(codes)} under PRINT-KIT-2."
               if codes else
               f"{pid} ({row['page_name']}, {row['section_id']} on {sec['stock_code']}, "
               f"{sec['binding']}) clears every rule in PRINT-KIT-2, so the only correct "
               f"finding is `none`.")
        v.append(audit_v(
            f"audit_{pid.lower().replace('-', '_')}",
            f"Reads activity_kit_audit.csv as text and requires the {pid} row to carry "
            + (f"exactly {', '.join(codes)}" if codes else "a clean verdict and no finding code")
            + ", in any column or code order, case-insensitively.",
            why,
            rf"(?im)^(?=[^\n]*\b{pid}\b)" + page_pattern(codes)))

    v.append(section_v(
        "section_has_required_columns",
        "Requires one line of section_summary.csv to name the columns the prompt specifies.",
        "The prompt fixes the rollup's columns and their order.",
        r"(?im)^(?=[^\n]*\bsection_id\b)(?=[^\n]*\bimposed_page_count\b)"
        r"(?=[^\n]*\bflagged_pages\b)(?=[^\n]*\bimposition\b)"))

    for s in rollup.values():
        sid = s["section_id"]
        key = sid.lower().replace("-", "_")
        v.append(section_v(
            f"section_{key}_counts",
            f"Requires the {sid} row to carry live_page_count {s['live_page_count']}, held_back "
            f"{s['held_back']}, imposed_page_count {s['imposed_page_count']} and flagged_pages "
            f"{s['flagged_pages']}, in the column order the prompt specifies.",
            f"{sid} holds {s['live_page_count']} live pages, of which {s['held_back']} are held "
            f"back under §8 and {s['flagged_pages']} carry a finding.",
            rf"(?im)^[^\n]*?\b{sid}\b[^\n]*?\b{s['live_page_count']}\b[^\n]*?\b{s['held_back']}\b"
            rf"[^\n]*?\b{s['imposed_page_count']}\b[^\n]*?\b{s['flagged_pages']}\b"))
        v.append(section_v(
            f"section_{key}_binding_and_stock",
            f"Requires the {sid} row to name its binding and its stock code.",
            f"{sid} is {s['binding']} on {s['stock_code']}; both come from `kit_sections.csv` "
            f"and both decide which limits its pages are judged against.",
            rf"(?im)^(?=[^\n]*\b{sid}\b)(?=[^\n]*\b{s['binding']}\b)(?=[^\n]*\b{s['stock_code']}\b)"))
        if s["imposition"] == "none":
            why = (f"{sid} imposes {s['imposed_page_count']} pages after {s['held_back']} held "
                   f"back, a multiple of {IMPOSITION_MULTIPLE[s['binding']]}, so it imposes "
                   f"cleanly.")
            pattern = (rf"(?im)^(?=[^\n]*\b{sid}\b)(?![^\n]*IMPOSITION_INVALID)"
                       rf"(?=[^\n]*{CLEAN_SYNONYMS})")
        else:
            why = (f"{sid} imposes {s['imposed_page_count']} pages after {s['held_back']} held "
                   f"back, which is not a multiple of {IMPOSITION_MULTIPLE[s['binding']]}; it "
                   f"needs {s['pages_needed']} more.")
            pattern = rf"(?im)^(?=[^\n]*\b{sid}\b)(?=[^\n]*IMPOSITION_INVALID)"
        v.append(section_v(f"section_{key}_imposition",
                           f"Requires the {sid} row's imposition verdict.", why, pattern))

    figures = [
        ("result_page_count", "page_count", "Live pages audited after superseded artwork is dropped."),
        ("result_superseded_count", "superseded_count", "Artwork rows the batch supersedes."),
        ("result_section_count", "section_count", "Sections in the kit."),
        ("result_clean_count", "clean_count", "Live pages with no finding."),
        ("result_flagged_count", "flagged_count", "Live pages carrying at least one finding."),
        ("result_finding_total", "finding_total", "Every finding raised, which differs from the number of pages carrying one because several pages breach more than one rule."),
        ("result_dpi_low_count", "dpi_low_count", "Pages carrying DPI_TOO_LOW."),
        ("result_margin_count", "margin_count", "Pages carrying MARGIN_VIOLATION."),
        ("result_bleed_short_count", "bleed_short_count", "Pages carrying BLEED_SHORT."),
        ("result_ink_over_count", "ink_over_count", "Pages carrying INK_OVER."),
        ("result_element_short_count", "element_short_count", "Pages carrying ELEMENT_COUNT_SHORT."),
        ("result_element_shortfall_total", "element_shortfall_total", "Required elements missing across the batch, not the number of short pages."),
        ("result_imposition_invalid_sections", "imposition_invalid_sections", "Sections whose imposed page count does not fit their binding."),
        ("result_imposition_shortfall_total", "imposition_shortfall_total", "Pages the invalid sections need between them."),
    ]
    for name, key, why in figures:
        v.append(json_v(name, key, results[key],
                        f"Derived figure `{key}`: {why} Recomputed from the batch, not read back "
                        f"from the model's own summary."))

    dpi_floors = sorted({s["min_dpi"] for s in STOCKS.values()})
    ink_caps = sorted({s["max_ink_pct"] for s in STOCKS.values()})
    edges = sorted({str(s["min_margin_in"]) for s in STOCKS.values()} |
                   {str(s["min_bleed_in"]) for s in STOCKS.values()})

    v += [
        memo_v("memo_covers_every_flagged_page",
               f"Requires all {len(flagged)} flagged page ids to appear in activity_kit_memo.md.",
               "The prompt asks the memo to account for every page carrying a finding.",
               anywhere(*[rf"\b{p}\b" for p in flagged])),
        memo_v("memo_covers_every_section",
               f"Requires all {len(rollup)} section ids to appear in activity_kit_memo.md.",
               "The prompt asks the memo to cover every section.",
               anywhere(*[rf"\b{s}\b" for s in rollup])),
        memo_v("memo_names_every_finding_code",
               "Requires all five PRINT-KIT-2 finding codes to appear in activity_kit_memo.md.",
               "Every code is raised somewhere in this batch, so a memo accounting for the "
               "findings names all five.",
               anywhere(*CODES)),
        memo_v("memo_names_every_stock",
               "Requires all three stock codes to appear in activity_kit_memo.md.",
               "The prompt asks the memo to give the limits actually applied, and the limits "
               "belong to the stocks.",
               anywhere(*[rf"\b{c}\b" for c in STOCKS])),
        memo_v("memo_cites_every_dpi_floor",
               f"Requires the resolution floors {dpi_floors} to appear in activity_kit_memo.md.",
               "The prompt asks the memo to state the resolution floors it applied; the three "
               "stocks in this kit hold three different floors.",
               anywhere(*[rf"\b{d}\b" for d in dpi_floors])),
        memo_v("memo_cites_every_ink_cap",
               f"Requires the ink caps {ink_caps} to appear in activity_kit_memo.md.",
               "The prompt asks the memo to state the ink caps it applied.",
               anywhere(*[rf"\b{c}\b" for c in ink_caps])),
        memo_v("memo_cites_margin_and_bleed_floors",
               f"Requires the margin and bleed floors {edges} to appear in activity_kit_memo.md.",
               "The prompt asks the memo to state the margin floors and bleed minimums it applied.",
               anywhere(*[rf"{e.replace('.', chr(92) + '.')}" for e in edges])),
        memo_v("memo_explains_full_bleed_exemption",
               "Requires activity_kit_memo.md to tie full-bleed pages to a margin exemption.",
               "The prompt asks the memo to say what clears a page whose numbers look like a "
               "breach; the §4 full-bleed margin exemption is that case.",
               r"(?is)full[\s_-]?bleed[\s\S]{0,900}?(?:exempt|waiv|not\s+(?:a\s+)?(?:subject|"
               r"assessed|flagged|graded|checked|held)|does\s+not\s+apply|by\s+design|deliberate)"),
        memo_v("memo_explains_spine_margin_exception",
               "Requires activity_kit_memo.md to tie the binding to the full-bleed margin "
               "exemption, which §4 limits to saddle-stitched sections.",
               "Five full-bleed pages carry MARGIN_VIOLATION because their section is "
               "perfect-bound; a memo explaining them names the binding.",
               r"(?is)perfect[\s_-]?bound[\s\S]{0,900}?(?:margin|spine|§\s*3|section\s*3)"
               r"|(?:margin|spine)[\s\S]{0,900}?perfect[\s_-]?bound"),
        memo_v("memo_explains_bleed_obligation",
               "Requires activity_kit_memo.md to state a bleed allowance requirement in inches.",
               "The full-bleed exemption also creates the §4 bleed obligation; a memo that "
               "explains BLEED_SHORT states the allowance the page owed.",
               r"(?is)bleed[^\n]{0,200}?(?:0\.(?:125|1875|25)|allowance|minimum|at\s+least|min\b)"),
        memo_v("memo_explains_scaled_resolution",
               "Requires activity_kit_memo.md to tie resolution to placement scale.",
               "§2 grades the effective resolution, not the supplied `artwork_dpi`; the memo has "
               "to name the measured value it used.",
               r"(?is)(?:(?:effective|placed?|placement|scal\w+|enlarg\w+|reduc\w+|\d+\s*%)"
               r"[\s\S]{0,160}?(?:dpi|resolution)|(?:dpi|resolution)[\s\S]{0,160}?"
               r"(?:effective|placed?|placement|scal\w+|enlarg\w+|reduc\w+|\d+\s*%))"),
        memo_v("memo_names_superseded_pages",
               "Requires activity_kit_memo.md to name the six pages carrying superseded artwork "
               "and to use supersession language.",
               "The prompt asks the memo to say which artwork the batch supersedes; PG-04, "
               "PG-12, PG-18, PG-27, PG-33 and PG-35 are the pages with more than one revision.",
               anywhere(r"\bPG-04\b", r"\bPG-12\b", r"\bPG-18\b", r"\bPG-27\b", r"\bPG-33\b",
                        r"\bPG-35\b",
                        r"(?:supersed\w*|supercede\w*|replac\w*|(?:latest|highest|newer|later)"
                        r"\s+revision|rev(?:ision)?\s*\d)")),
        memo_v("memo_explains_rev_b_amendment",
               "Requires activity_kit_memo.md to name the saddle-stitch element-count amendment.",
               "Half the ELEMENT_COUNT_SHORT verdicts turn on Amendment Rev B; a memo explaining "
               "them names the binding it depends on.",
               r"(?is)(?:saddle[\s_-]?stitch\w*|rev(?:ision)?\s*b\b|amendment)"),
        memo_v("memo_names_unimposable_sections",
               f"Requires activity_kit_memo.md to name the {len(invalid)} sections that cannot be "
               f"imposed, alongside imposition language.",
               "The prompt asks the memo to name the sections that cannot be imposed; "
               + ", ".join(s["section_id"] for s in invalid) + " are those sections.",
               anywhere(*[rf"\b{s['section_id']}\b" for s in invalid],
                        r"(?:impos\w+|repaginat\w+|multiple\s+of)")),
        memo_v("memo_states_element_shortfall_total",
               f"Requires activity_kit_memo.md to state {results['element_shortfall_total']} as "
               f"the batch's missing-element total, in an element or shortfall context.",
               "The prompt asks the memo to state how many required elements the batch is "
               "missing altogether; it is a different number from the count of short pages.",
               rf"(?is)(?:\b{results['element_shortfall_total']}\b[^\n]{{0,90}}"
               rf"(?:required\s+element|element|shortfall|missing|short)"
               rf"|(?:element|shortfall|missing|short)[^\n]{{0,90}}"
               rf"\b{results['element_shortfall_total']}\b)"),
        memo_v("memo_reports_clean_and_flagged_totals",
               f"Requires activity_kit_memo.md to state {results['clean_count']} clear pages and "
               f"{results['flagged_count']} flagged pages.",
               "The prompt asks the memo to state how many pages are clear and how many carry a "
               "finding.",
               anywhere(rf"\b{results['clean_count']}\b", rf"\b{results['flagged_count']}\b")),
    ]
    return v


def main():
    live, verdicts, shortfalls, rollup, results = gold()
    write_inputs()
    write_instruction()
    write_solution(live, verdicts, shortfalls, rollup, results)

    spec = {"task_id": "gen-G774-activity-kit-print-spec-audit",
            "verifiers": build_verifiers(live, verdicts, shortfalls, rollup, results)}
    (TESTS / "verifier.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {len(spec['verifiers'])} verifiers")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

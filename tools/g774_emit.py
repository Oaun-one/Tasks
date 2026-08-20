#!/usr/bin/env python3
"""Writes the hardened gen-g774 package from the model in g774_build.py."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g774_build import (  # noqa: E402
    CODES, FIELDS, PKG, ROWS, SECTIONS, STOCKS, BASE_MIN_ELEMENTS, REV_B_TYPES,
    REV_B_UPLIFT, as_dicts, effective_dpi, gold, min_elements,
)

INPUT = PKG / "environment" / "input"
SOLUTION = PKG / "solution" / "files"
TESTS = PKG / "tests"

CLEAN_SYNONYMS = (
    r"(?:\b(?:none|no[ _-]?finding(?:s)?|ok|okay|pass(?:es|ed)?|clean|clear|compliant"
    r"|conform(?:s|ing)?|fine|good|yes|true|n/?a)\b|(?:^|,)\s*[-–—✓]\s*(?:,|$))"
)


def fmt(value):
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


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

    elem_table = "\n".join(
        f"| `{t}` | {n} |" for t, n in BASE_MIN_ELEMENTS.items()
    )
    standard = f"""# Printable activity-kit production standard (PRINT-KIT-2)

Binding for the artwork batch in `activity_kit_pages.csv`.

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

It is exempt from nothing else, and it carries an obligation no other page carries: a
full-bleed page must be supplied with `bleed_in` of at least the stock's `min_bleed_in`, or
the trim eats into the art. Below it is `BLEED_SHORT`. `bleed_in` on a page that is not
full-bleed is not assessed.

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
"""
    (INPUT / "activity_kit_print_standard.md").write_text(standard, encoding="utf-8")


def write_instruction():
    text = """# Task

The activity kit goes to the printer on Friday and I need a pre-flight pass over the
batch before it does. Everything is in `input/`: the artwork batch, the section list
saying how each section is bound and which stock it runs on, the stock profiles, and
our PRINT-KIT-2 standard.

Apply the standard as written. Most of the limits belong to the paper stock rather than
to the kit, parts of the batch have been re-supplied since the first drop, and the
standard carries an amendment — each of those changes which pages are actually in
breach.

Save `activity_kit_audit.csv` with one row per audited page, keyed by `page_id`, and a
`finding` column carrying the code for every rule that page breaches — join multiple
codes with `|`, and use `none` for a page that breaches nothing.

Then write `activity_kit_memo.md` for the studio. Account for every page carrying a
finding, naming the measured value and the limit it missed. Where a page's numbers look
like a breach but the standard clears it, say what clears it. And say which artwork the
batch supersedes, and what that changes.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `activity_kit_audit.csv` — Per-page print-production audit
    - `activity_kit_memo.md` — Markdown memo
    - `results.json` — a JSON object with the keys `page_count` (pages audited),
      `superseded_count` (artwork rows the batch supersedes), `clean_count`,
      `flagged_count`, `finding_total` (every finding raised across the batch, not the
      number of pages carrying one), `dpi_low_count`, `margin_count`,
      `bleed_short_count`, `ink_over_count`, `element_short_count` (each of these five
      counting the pages carrying that finding) and `element_shortfall_total` (how many
      required elements the batch is missing in total)
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.
"""
    (PKG / "instruction.md").write_text(text, encoding="utf-8")


def write_solution(live, verdicts, shortfalls, results):
    SOLUTION.mkdir(parents=True, exist_ok=True)

    rows = ["page_id,page_name,section_id,stock_code,finding"]
    for r in live:
        stock = SECTIONS[r["section_id"]]["stock_code"]
        finding = "|".join(verdicts[r["page_id"]]) or "none"
        rows.append(f"{r['page_id']},{r['page_name']},{r['section_id']},{stock},{finding}")
    (SOLUTION / "activity_kit_audit.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")

    (SOLUTION / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    by_code = {c: [r["page_id"] for r in live if c in verdicts[r["page_id"]]] for c in CODES}
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
                bits.append(f"safe margin {r['margin_in']} in against a "
                            f"{st['min_margin_in']} in floor on {sec['stock_code']}")
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

    flagged_lines = "\n".join(detail(p) for p in [r["page_id"] for r in live] if verdicts[p])

    memo = f"""# Activity-kit pre-flight — PRINT-KIT-2

{results['page_count']} pages audited from a batch of {results['page_count'] + results['superseded_count']}
artwork rows. {results['clean_count']} clear, {results['flagged_count']} carry at least one
finding, {results['finding_total']} findings in total.

## Superseded artwork

The batch carries more than one revision of four pages, and only the highest revision of a
`page_id` is live (§0). These four rows are superseded and were **not** audited:

- **PG-04** rev 1 is superseded by rev 2. The live artwork is placed at 80%, has a 0.24 in
  margin and 305% ink; rev 1 would have read `none`.
- **PG-12** rev 1 is superseded by rev 3, which drops to 7 mission cards. Rev 1 carried 9
  and would have read `none`. The live revision appears *before* the superseded one in the
  file, so row order is not the tie-break — `revision` is.
- **PG-18** rev 1 is superseded by rev 2, which cuts the bleed to 0.10 in and pushes ink to
  285%. Rev 1 would have read `none`.
- **PG-27** rev 1 is superseded by rev 2. Here it runs the other way: rev 1 was 200 dpi and
  would have been `DPI_TOO_LOW`, while the live rev 2 is placed at 200% from 480 dpi
  artwork and clears the floor exactly.

Auditing the superseded rows instead of the live ones changes four verdicts and every
derived figure.

## How the limits were read

Every limit in §2–§5 belongs to the **stock**, reached through the page's section
(`page` → `section` → `stock`), so the same number is a breach in one section and clear in
another. PG-13 at 298% ink is clear on BRD-250 (300% cap) while PG-28 at 241% is over on
UNC-120 (240% cap).

Resolution is judged on the **effective** figure, not the supplied one: `artwork_dpi`
divided by the placement scale (§2). PG-06 is supplied at 450 dpi and still only prints at
300 because it is placed at 150%; PG-20 is supplied at 240 dpi and prints at 300 because it
is placed at 80%. Reading `artwork_dpi` straight off the row gets both of them wrong.

Every limit is inclusive (§1). PG-05, PG-16, PG-22 and PG-27 all sit exactly on at least
one limit and are clear because of it.

## Full bleed: exempt from the margin, and only from the margin

Full-bleed pages are exempt from the safe-margin rule (§4) — PG-01 at 0.05 in, PG-10 at
0.00 in and PG-29 at 0.04 in are all clear on margin, and flagging them is the commonest
false positive here. But full-bleed is also the *only* status that owes a bleed allowance,
and PG-02, PG-18 and PG-25 are short of their stock's minimum. Pages that are not
full-bleed are not assessed on bleed at all: PG-30 carries 0.30 in of bleed and it is
neither a credit nor a finding.

## Required elements and Amendment Rev B

Minimums come from the page-type table in §6, raised by {REV_B_UPLIFT} for `mission_cards`
and `badge_certificate` in a `saddle_stitch` section. PG-19 (6 mission cards,
perfect-bound) is clear on exactly the same count that makes PG-13 (6 mission cards,
saddle-stitched) short by 2. The batch is missing {results['element_shortfall_total']}
required elements in total across {results['element_short_count']} pages.

## Findings by page

{flagged_lines}

## Pages that clear the standard

{', '.join(clean)} — no finding.

## Totals

| figure | value |
| --- | --- |
| pages audited | {results['page_count']} |
| superseded artwork rows | {results['superseded_count']} |
| clear | {results['clean_count']} |
| flagged | {results['flagged_count']} |
| findings raised | {results['finding_total']} |
| `DPI_TOO_LOW` pages | {results['dpi_low_count']} |
| `MARGIN_VIOLATION` pages | {results['margin_count']} |
| `BLEED_SHORT` pages | {results['bleed_short_count']} |
| `INK_OVER` pages | {results['ink_over_count']} |
| `ELEMENT_COUNT_SHORT` pages | {results['element_short_count']} |
| required elements missing | {results['element_shortfall_total']} |
"""
    (SOLUTION / "activity_kit_memo.md").write_text(memo, encoding="utf-8")
    return by_code, clean


def csv_verifier(name, how, why, pattern, path="activity_kit_audit.csv", comparison="regex_match"):
    return {
        "name": name,
        "metadata": {"how_justification": how, "why_justification": why},
        "source": {"type": "file", "file": {"type": "csv", "command": "extract_text",
                                            "arguments": {"path": path}}},
        "assertion": {"type": "deterministic", "expected": pattern,
                      "deterministic": {"path": "$.text", "comparison": comparison}},
    }


def md_verifier(name, how, why, pattern):
    return {
        "name": name,
        "metadata": {"how_justification": how, "why_justification": why},
        "source": {"type": "file", "file": {"type": "md", "command": "extract_text",
                                            "arguments": {"path": "activity_kit_memo.md"}}},
        "assertion": {"type": "deterministic", "expected": pattern,
                      "deterministic": {"path": "$.text", "comparison": "regex_match"}},
    }


def exists_verifier(name, path, why):
    return {
        "name": name,
        "metadata": {"how_justification": f"Checks {path} is present as a file in the workspace.",
                     "why_justification": why},
        "source": {"type": "file", "file": {"type": "filesystem", "command": "check_path_exists",
                                            "arguments": {"path": path}}},
        "assertion": {"type": "deterministic", "expected": True,
                      "deterministic": {"path": "$.is_file", "comparison": "equals"}},
    }


def json_verifier(name, key, value, why):
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
    parts = []
    if codes:
        parts += [rf"(?=[^\n]*\b{c}\b)" for c in codes]
    else:
        parts.append(rf"(?=[^\n]*{CLEAN_SYNONYMS})")
    parts += [rf"(?![^\n]*\b{c}\b)" for c in CODES if c not in codes]
    return "".join(parts)


def build_verifiers(live, verdicts, shortfalls, results):
    page_ids = [r["page_id"] for r in live]
    flagged = [p for p in page_ids if verdicts[p]]
    verifiers = [
        exists_verifier("audit_csv_exists", "activity_kit_audit.csv", "The per-page audit is the primary deliverable."),
        exists_verifier("memo_exists", "activity_kit_memo.md", "The studio memo is a named deliverable."),
        exists_verifier("results_exists", "results.json", "The derived figures are a named deliverable."),
        csv_verifier(
            "audit_has_page_id_and_finding_columns",
            "Requires one line of activity_kit_audit.csv to name both a page_id and a finding column.",
            "The prompt asks for the audit keyed by `page_id` with a `finding` column.",
            r"(?im)^(?=[^\n]*\bpage_id\b)(?=[^\n]*\bfinding\b)",
        ),
        csv_verifier(
            "audit_has_no_pages_outside_batch",
            "Requires activity_kit_audit.csv to carry no page id outside PG-01..PG-30.",
            "An audit that invents pages is not an audit of this batch.",
            r"PG-(?:00|3[1-9]|[4-9]\d)",
            comparison="not_regex_match",
        ),
        csv_verifier(
            "audit_has_one_row_per_page",
            "Requires no page id in activity_kit_audit.csv to appear on two different lines.",
            "The batch carries superseded artwork; an audit that emits a row per artwork row "
            "rather than per live page duplicates page ids and is not the deliverable asked for.",
            r"(?ms)^[^\n]*\b(PG-(?:0[1-9]|[12]\d|30))\b.*?^[^\n]*\b\1\b",
            comparison="not_regex_match",
        ),
    ]

    for pid in page_ids:
        row = next(r for r in live if r["page_id"] == pid)
        sec = SECTIONS[row["section_id"]]
        codes = verdicts[pid]
        if codes:
            why = (f"{pid} ({row['page_name']}, {row['section_id']} on {sec['stock_code']}) breaches "
                   f"exactly {', '.join(codes)} under PRINT-KIT-2.")
        else:
            why = (f"{pid} ({row['page_name']}, {row['section_id']} on {sec['stock_code']}) clears every "
                   f"rule in PRINT-KIT-2, so the only correct finding is `none`.")
        verifiers.append(csv_verifier(
            f"audit_{pid.lower().replace('-', '_')}",
            f"Reads activity_kit_audit.csv as text and requires the {pid} row to carry "
            f"{'exactly ' + ', '.join(codes) if codes else 'a clean verdict and no finding code'}, "
            f"in any column or code order, case-insensitively.",
            why,
            rf"(?im)^(?=[^\n]*\b{pid}\b)" + page_pattern(codes),
        ))

    figures = [
        ("result_page_count", "page_count", "Derived figure `page_count`: live pages audited after superseded artwork is dropped."),
        ("result_superseded_count", "superseded_count", "Derived figure `superseded_count`: artwork rows the batch supersedes."),
        ("result_clean_count", "clean_count", "Derived figure `clean_count`: live pages with no finding."),
        ("result_flagged_count", "flagged_count", "Derived figure `flagged_count`: live pages carrying at least one finding."),
        ("result_finding_total", "finding_total", "Derived figure `finding_total`: every finding raised, which differs from the number of pages carrying one because several pages breach more than one rule."),
        ("result_dpi_low_count", "dpi_low_count", "Derived figure `dpi_low_count`, recomputed from the delivered audit."),
        ("result_margin_count", "margin_count", "Derived figure `margin_count`, recomputed from the delivered audit."),
        ("result_bleed_short_count", "bleed_short_count", "Derived figure `bleed_short_count`, recomputed from the delivered audit."),
        ("result_ink_over_count", "ink_over_count", "Derived figure `ink_over_count`, recomputed from the delivered audit."),
        ("result_element_short_count", "element_short_count", "Derived figure `element_short_count`, recomputed from the delivered audit."),
        ("result_element_shortfall_total", "element_shortfall_total", "Derived figure `element_shortfall_total`: required elements missing across the batch, not the number of short pages."),
    ]
    for name, key, why in figures:
        verifiers.append(json_verifier(name, key, results[key], why))

    verifiers += [
        md_verifier(
            "memo_covers_every_flagged_page",
            f"Requires all {len(flagged)} flagged page ids to appear in activity_kit_memo.md.",
            "The prompt asks the memo to account for every page carrying a finding.",
            "(?s)^" + "".join(rf"(?=[\s\S]*\b{p}\b)" for p in flagged),
        ),
        md_verifier(
            "memo_names_every_finding_code",
            "Requires all five PRINT-KIT-2 finding codes to appear in activity_kit_memo.md.",
            "Every code is raised somewhere in this batch, so a memo accounting for the "
            "findings names all five.",
            "(?is)^" + "".join(rf"(?=[\s\S]*{c})" for c in CODES),
        ),
        md_verifier(
            "memo_explains_full_bleed_exemption",
            "Requires activity_kit_memo.md to tie full-bleed pages to a margin exemption.",
            "The prompt asks the memo to say what clears a page whose numbers look like a "
            "breach; the full-bleed margin exemption (§4) is that case.",
            r"(?is)full[\s_-]?bleed[\s\S]{0,800}?(?:exempt|waiv|not\s+(?:a\s+)?(?:subject|assessed|"
            r"flagged|graded|checked|held)|does\s+not\s+apply|by\s+design|deliberate)",
        ),
        md_verifier(
            "memo_explains_bleed_obligation",
            "Requires activity_kit_memo.md to state a bleed allowance requirement in inches.",
            "The full-bleed exemption also creates the §4 bleed obligation; a memo that "
            "explains BLEED_SHORT states the allowance the page owed.",
            r"(?is)bleed[^\n]{0,200}?(?:0\.(?:125|1875|25)|allowance|minimum|at\s+least|min\b)",
        ),
        md_verifier(
            "memo_explains_scaled_resolution",
            "Requires activity_kit_memo.md to tie resolution to placement scale.",
            "§2 grades the effective resolution, not the supplied `artwork_dpi`; the memo has "
            "to name the measured value it used.",
            r"(?is)(?:(?:effective|placed?|placement|scal\w+|enlarg\w+|reduc\w+|\d+\s*%)"
            r"[\s\S]{0,160}?(?:dpi|resolution)|(?:dpi|resolution)[\s\S]{0,160}?"
            r"(?:effective|placed?|placement|scal\w+|enlarg\w+|reduc\w+|\d+\s*%))",
        ),
        md_verifier(
            "memo_names_superseded_pages",
            "Requires activity_kit_memo.md to name the four pages carrying superseded artwork "
            "and to use supersession language.",
            "The prompt asks the memo to say which artwork the batch supersedes; PG-04, PG-12, "
            "PG-18 and PG-27 are the four pages with more than one revision.",
            r"(?is)^(?=[\s\S]*\bPG-04\b)(?=[\s\S]*\bPG-12\b)(?=[\s\S]*\bPG-18\b)"
            r"(?=[\s\S]*\bPG-27\b)(?=[\s\S]*(?:supersed\w*|supercede\w*|replac\w*|"
            r"(?:latest|highest|newer|later)\s+revision|rev(?:ision)?\s*\d))",
        ),
        md_verifier(
            "memo_explains_rev_b_amendment",
            "Requires activity_kit_memo.md to name the saddle-stitch element-count amendment.",
            "Four of the eight ELEMENT_COUNT_SHORT verdicts turn on Amendment Rev B; a memo "
            "explaining them names the binding it depends on.",
            r"(?is)(?:saddle[\s_-]?stitch\w*|rev(?:ision)?\s*b\b|amendment)",
        ),
    ]
    return verifiers


def main():
    live, verdicts, shortfalls, results = gold()
    write_inputs()
    write_instruction()
    write_solution(live, verdicts, shortfalls, results)

    spec = {"task_id": "gen-G774-activity-kit-print-spec-audit",
            "verifiers": build_verifiers(live, verdicts, shortfalls, results)}
    (TESTS / "verifier.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {len(spec['verifiers'])} verifiers")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

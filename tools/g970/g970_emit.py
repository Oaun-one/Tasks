"""Writes the g970 package: standard, prompt, gold deliverables and tests/verifier.json.

Everything graded comes from g970_build.audit(), so gold and grader cannot disagree.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from g970_build import (  # noqa: E402
    AUDIT_DATE, CODES, EGRESS, GOLD, HEIGHTENED_CAP_REDUCTION,
    HEIGHTENED_ZONE_THRESHOLD, INPUT, OVERSIZE, PERMIT, ROOT, TESTS,
    ZONE_BREACH, audit, governing,
)

AUDIT_CSV = "collateral_audit.csv"
ZONE_CSV = "zone_summary.csv"
MEMO = "collateral_memo.md"

NONE_ALT = (r"(?:\b(?:none|no[ _-]?finding(?:s)?|ok|okay|pass(?:es|ed)?|clean|clear|"
            r"compliant|conform(?:s|ing)?|fine|good|yes|true|n/?a)\b|(?:^|,)\s*[-–—✓]\s*(?:,|$))")

ZONE_CLEAN_ALT = (r"(?:\b(?:none|within|under|ok|okay|clear|compliant|pass(?:es|ed)?|"
                  r"yes|true|n/?a)\b|(?:^|,)\s*[-–—✓]\s*(?:,|$))")


def anywhere(*needles):
    return "(?is)^" + "".join(r"(?=[\s\S]*%s)" % n for n in needles)


def near(token, reason, window=600):
    wb = chr(92) + "b"
    bt = wb + token + wb
    gap = r"[\s\S]{0," + str(window) + r"}?"
    return "(?:" + bt + gap + "(?:" + reason + ")|(?:" + reason + ")" + gap + bt + ")"


def num_forms(value):
    """Every reasonable rendering of a number, so a verifier never grades formatting."""
    out = set()
    if float(value) == int(float(value)):
        out.add(str(int(float(value))))
        out.add("%.1f" % float(value))
        out.add("%.2f" % float(value))
    else:
        for places in (1, 2, 3):
            out.add(("%%.%df" % places) % float(value))
        out.add(("%g" % float(value)))
    return "(?:" + "|".join(re.escape(v) for v in sorted(out)) + ")"


def _v(name, how, why, kind, path, expected, comparison, json_path):
    command = {"filesystem": "check_path_exists", "json": "read_file"}.get(kind, "extract_text")
    return {
        "name": name,
        "metadata": {"how_justification": how, "why_justification": why},
        "source": {"type": "file",
                   "file": {"type": kind, "command": command, "arguments": {"path": path}}},
        "assertion": {"type": "deterministic", "expected": expected,
                      "deterministic": {"path": json_path, "comparison": comparison}},
    }


def exists_v(name, path, why):
    return _v(name, "Checks %s is present as a file." % path, why,
              "filesystem", path, True, "equals", "$.is_file")


def csv_v(name, path, pattern, why, comparison="regex_match"):
    return _v(name, "Opens %s with csv.extract_text and applies %s." % (path, comparison),
              why, "csv", path, pattern, comparison, "$.text")


def md_v(name, pattern, why):
    return _v(name, "Opens %s with md.extract_text and applies regex_match." % MEMO,
              why, "md", MEMO, pattern, "regex_match", "$.text")


def json_v(name, key, value, why):
    return _v(name, "Reads results.json and compares $.%s." % key, why,
              "json", "results.json", value, "equals", "$.%s" % key)


def row_regex(key, present):
    parts = ["(?im)^", r"(?=[^\n]*\b%s\b)" % key]
    if present:
        parts += [r"(?=[^\n]*\b%s\b)" % c for c in present]
    else:
        parts.append(r"(?=[^\n]*%s)" % NONE_ALT)
    parts += [r"(?![^\n]*\b%s\b)" % c for c in CODES if c not in present]
    return "".join(parts)


# ------------------------------------------------------------------ standard

def write_standard(zones, register):
    zone_rows = "\n".join(
        "| `%s` | %s | %s ft | %s sq ft | %s sq ft |"
        % (z["zone_id"], z["zone_name"], z["min_egress_clearance_ft"],
           z["max_item_sqft"], z["aggregate_allowance_sqft"])
        for z in zones.values())

    text = f"""# Heritage Landing Festival — collateral and signage permit standard (HLF-7)

Revision 7. Binding for every item recorded in `collateral_log.csv`. Where an item's own
record and this standard disagree, this standard decides.

**This review is made as of {AUDIT_DATE.isoformat()}.** Every currency test below is made
against that date and nothing else. A permit whose validity ends **on**
{AUDIT_DATE.isoformat()} is still current; one that ended before it is not.

## §1 Scope — what counts as installed signage

§2 to §4 apply to **installed signage**: collateral that is physically mounted or displayed
at the venue. Of the types the log records, that is `installed_signage` and
`temporary_banner` — a temporary banner is hung at the venue and is installed signage for
every purpose in this standard.

A `standalone_graphic` (artwork produced for downstream or personal use and never installed)
and a `vehicle_wrap` (applied to a vehicle, not to the venue) are **not** installed signage.
They are outside §2 to §4 whatever their own permit, clearance or size values say, and they
do not sit against a zone's allowance under §5. Reading the scope off a single literal type
string is the commonest error in this review.

An item carries one finding code for each rule it breaches. Its `finding` entry holds every
code it breaches, joined with `|`, in any order; an item that breaches none is `none`.

The audit carries **one row per in-scope item**. An item §1 holds out of scope is not audited
and does not appear in it — it is accounted for in the memo and in the figures instead.

## §2 Permit — `PERMIT_NUMBER_MISSING`

An installed-signage item must be covered by a festival permit that actually reaches it. A
permit reaches an item only when the **governing** row of `permit_register.csv` satisfies all
of:

- it covers the item's zone (`covers_zones`, a `;`-joined list, or `all`);
- it covers the item's recorded type (`covers_item_types`, likewise);
- its `valid_until` is on or after the review date.

The governing row is not always the row the item names. Where a permit has been re-issued,
the register records the replacement with `supersedes` pointing at the row it replaces, and
it is the **last** row in that chain whose terms apply. A chain may run more than one step,
and a re-issue may be narrower than what it replaced — in zones, in item types, or in date.

An item with no permit number, an unknown one, or one whose governing row fails any of the
three tests is `PERMIT_NUMBER_MISSING`.

## §3 Egress markers — `EGRESS_MARKER_OBSTRUCTED`

Every zone sets its own minimum clearance from a designated safety egress marker, because the
zones differ in crowd flow. An item whose `egress_clearance_ft` is below its own zone's
`min_egress_clearance_ft` is `EGRESS_MARKER_OBSTRUCTED`. Clearance exactly equal to the
minimum meets it.

## §4 Size — `OVERSIZE_COLLATERAL`

Every zone sets its own per-item size cap. An item whose `size_sqft` exceeds its own zone's
`max_item_sqft` is `OVERSIZE_COLLATERAL`. A size exactly equal to the cap is within it.

§6 can tighten this cap. Where it does, §4 is applied against the tightened figure.

## §5 Zone allowance — `{ZONE_BREACH}`

Each zone also carries a total allowance for the signage standing in it.

An item that fails §2 has no permit reaching it and comes down: it is **pulled**, and its
area does not sit against the allowance. What counts is the area of the items still standing
— the in-scope items in that zone whose permits do reach them.

A zone whose standing area exceeds its `aggregate_allowance_sqft` is `{ZONE_BREACH}`. A zone
exactly on its allowance is within it. §5 is a property of the zone, not of any item in it,
and is never a finding against an item.

| zone | name | min clearance | per-item cap | zone allowance |
| --- | --- | --- | --- | --- |
{zone_rows}

## §6 Heightened inspection

Where **{HEIGHTENED_ZONE_THRESHOLD} or more** zones are in breach under §5, the festival is
placed under heightened inspection.

While heightened inspection is in force, the per-item size cap in §4 is reduced by
**{HEIGHTENED_CAP_REDUCTION:g} sq ft — in the breaching zones only**. Every other zone keeps
the cap in the table above, and §2, §3 and §5 are unchanged.

The trigger reads the §5 breach count and nothing else. §5 counts standing area, and standing
depends on §2 alone, so §4 can never move the trigger: it is settled once the zone allowances
are, and it does not move again.

## Finding names

Item level: `{PERMIT}`, `{EGRESS}`, `{OVERSIZE}`, or `none`.
Zone level: `{ZONE_BREACH}`, or `none`.
"""
    with open(os.path.join(INPUT, "collateral_permit_standard.md"), "w", encoding="utf-8") as fh:
        fh.write(text)


def write_instruction():
    text = """# Task

The festival opens Friday and the safety office wants the collateral and signage pass
finished before the walk-round. Everything is in `input/`: the collateral log, the venue
zones, the permit register, and our HLF-7 standard.

Work the log against HLF-7 and give me the per-item verdicts, the zone picture the standard
asks for, a memo I can hand to the safety officer, and the batch figures HLF-7 reports on.

Use HLF-7's own finding names, and its convention for anything that comes back clean.

---
Save your deliverables into your current working directory using exactly these filenames:
    - `collateral_audit.csv` — per-item audit, columns `item_id` and `finding`, in that
      order and with no other columns
    - `zone_summary.csv` — per-zone rollup, columns `zone_id`, `item_count`,
      `pulled_count`, `standing_area_sqft`, `aggregate_allowance_sqft`, `allowance`, in
      that order and with no other columns
    - `collateral_memo.md` — Markdown memo for the safety office
    - `results.json` — a JSON object whose keys are the eleven figures named in HLF-7 §7,
      each a single JSON number
- Writing those files is the required deliverable and must be your final action; confirm each one exists before you answer.

---

## Working environment

- Your current working directory is `/app`, and it is writable.
- The read-only attachments referred to as `input/` are at `/app/input`.
- Write every deliverable into `/app`, at the exact filenames listed above.
"""
    with open(os.path.join(ROOT, "instruction.md"), "w", encoding="utf-8") as fh:
        fh.write(text)


RESULTS_KEYS = [
    ("collateral_count", "in-scope items audited"),
    ("zone_count", "venue zones"),
    ("permit_missing_count", "in-scope items carrying `PERMIT_NUMBER_MISSING`"),
    ("egress_obstructed_count", "in-scope items carrying `EGRESS_MARKER_OBSTRUCTED`"),
    ("oversize_count", "in-scope items carrying `OVERSIZE_COLLATERAL`"),
    ("compliant_count", "in-scope items carrying no finding"),
    ("flagged_count", "in-scope items carrying at least one finding"),
    ("finding_total", "findings raised across the batch"),
    ("out_of_scope_count", "logged items §1 holds outside §2 to §4"),
    ("pulled_item_count", "items pulled under §5"),
    ("zones_over_allowance", "zones in breach under §5"),
]


def append_section7():
    """§7 — the reporting spec, kept in the standard rather than the prompt."""
    path = os.path.join(INPUT, "collateral_permit_standard.md")
    text = open(path, encoding="utf-8").read()
    rows = "\n".join("| `%s` | %s |" % (k, d) for k, d in RESULTS_KEYS)
    block = f"""## §7 What the review reports

A completed review closes with four records: the per-item verdicts, the per-zone rollup, a
memo to the safety office, and the batch figures.

**The figures.** Eleven, every one taken over the review as HLF-7 settles it:

| key | counts |
| --- | --- |
{rows}

**The rollup.** One row per zone, carrying how many in-scope items it holds, how many were
pulled under §5, the standing area, the zone's allowance, and its §5 verdict.

**The memo.** The safety office reads the memo, not the tables. It records the date the
review is made as of; the logged items §1 holds out of scope, and why; every item carrying a
finding, with the code and the record that decides it — the permit, the zone minimum, or the
zone cap, named; any item whose numbers would read as a breach that the standard clears, and
what clears it; the zones over their allowance, with the standing area and the allowance they
passed; and whether heightened inspection is in force, with the count that put it there and
what it changed.

## Finding names"""
    text = text.replace("## Finding names", block, 1)
    open(path, "w", encoding="utf-8").write(text)


# ------------------------------------------------------------------- verifiers

def build_verifiers(items, in_scope, zones, register, findings, rollup, results, heightened):
    out_of_scope = [i for i in items if i not in in_scope]
    flagged = [i["item_id"] for i in in_scope if findings[i["item_id"]]]
    breached = [z for z in rollup.values() if z["allowance"] != "none"]

    vs = [
        exists_v("audit_csv_exists", AUDIT_CSV, "Per-item audit delivered."),
        exists_v("zone_csv_exists", ZONE_CSV, "Per-zone rollup delivered."),
        exists_v("memo_exists", MEMO, "Memo delivered."),
        exists_v("results_exists", "results.json", "Derived figures delivered."),
        csv_v("audit_has_required_columns", AUDIT_CSV,
              r"(?im)^[^\n]*\bitem_id\b[^\n]*\bfinding\b",
              "The audit carries the columns the prompt names."),
        csv_v("audit_has_one_row_per_item", AUDIT_CSV,
              r"(?ms)^[^\n]*\b(COL-\d{2})\b.*?^[^\n]*\b\1\b",
              "One row per item; an audit emitted per finding duplicates item ids.",
              comparison="not_regex_match"),
    ]

    for item in in_scope:
        iid = item["item_id"]
        codes = findings[iid]
        vs.append(csv_v(
            "audit_%s" % iid.lower().replace("-", "_"), AUDIT_CSV,
            row_regex(iid, codes),
            "%s (%s in %s) carries exactly %s."
            % (iid, item["item_type"], item["zone_id"], "|".join(codes) if codes else "no finding")))

    for item in out_of_scope:
        iid = item["item_id"]
        vs.append(csv_v(
            "audit_excludes_%s" % iid.lower().replace("-", "_"), AUDIT_CSV,
            r"(?im)^[^\n]*\b%s\b" % iid,
            "%s is a %s — §1 holds it outside §2 to §4, so it is not audited."
            % (iid, item["item_type"]),
            comparison="not_regex_match"))

    vs.append(csv_v("zone_has_required_columns", ZONE_CSV,
                    r"(?im)^(?=[^\n]*\bzone_id\b)(?=[^\n]*\bpulled_count\b)"
                    r"(?=[^\n]*\bstanding_area_sqft\b)(?=[^\n]*\ballowance\b)",
                    "The rollup carries the columns the prompt names."))

    for z in rollup.values():
        zid = z["zone_id"]
        key = zid.lower().replace("-", "_")
        vs.append(csv_v(
            "zone_%s_counts" % key, ZONE_CSV,
            r"(?im)^[^\n]*?\b%s\b[^\n]*?\b%d\b[^\n]*?\b%d\b[^\n]*?%s"
            % (zid, z["item_count"], z["pulled_count"], num_forms(z["standing_area_sqft"])),
            "%s holds %d in-scope items, %d pulled under §5, %g sq ft standing."
            % (zid, z["item_count"], z["pulled_count"], z["standing_area_sqft"])))
        if z["allowance"] == "none":
            pattern = (r"(?im)^(?=[^\n]*\b%s\b)(?![^\n]*%s)(?=[^\n]*%s)"
                       % (zid, ZONE_BREACH, ZONE_CLEAN_ALT))
            why = ("%s stands at %g sq ft against a %g sq ft allowance, so it is within it."
                   % (zid, z["standing_area_sqft"], z["aggregate_allowance_sqft"]))
        else:
            pattern = r"(?im)^(?=[^\n]*\b%s\b)(?=[^\n]*%s)" % (zid, ZONE_BREACH)
            why = ("%s stands at %g sq ft against a %g sq ft allowance."
                   % (zid, z["standing_area_sqft"], z["aggregate_allowance_sqft"]))
        vs.append(csv_v("zone_%s_allowance" % key, ZONE_CSV, pattern, why))

    for key, desc in RESULTS_KEYS:
        vs.append(json_v("result_%s" % key, key, results[key],
                         "Derived figure `%s`: %s, recomputed from the batch." % (key, desc)))

    breach_ids = [z["zone_id"] for z in breached]
    vs += [
        md_v("memo_cites_review_date", r"2026-0?8-20",
             "The memo states the date every currency test is made against."),
        md_v("memo_covers_every_flagged_item",
             anywhere(*[r"\b%s\b" % i for i in flagged]),
             "The memo accounts for all %d items carrying a finding." % len(flagged)),
        md_v("memo_covers_every_zone",
             anywhere(*[r"\b%s\b" % z for z in rollup]),
             "The memo covers every zone."),
        md_v("memo_names_every_finding_code", anywhere(*CODES),
             "All three item-level codes are raised somewhere in this batch."),
        md_v("memo_names_out_of_scope_items",
             anywhere(*([r"\b%s\b" % i["item_id"] for i in out_of_scope]
                        + [r"(?:out of scope|not installed|standalone|vehicle|§\s*1|excluded)"])),
             "The memo says which logged items §1 holds out of scope."),
        md_v("memo_names_breaching_zones",
             anywhere(*([r"\b%s\b" % z for z in breach_ids]
                        + [r"(?:allowance|over|breach\w*|exceed\w*)"])),
             "The memo names the zones over their allowance."),
        md_v("memo_explains_heightened_inspection",
             anywhere(r"(?:heighten\w*|§\s*6|section\s*6)",
                      r"(?:%s|three)" % HEIGHTENED_ZONE_THRESHOLD,
                      num_forms(HEIGHTENED_CAP_REDUCTION)),
             "The prompt asks whether heightened inspection is in force, the count that put "
             "it there, and what it changed. §6 fires on exactly %d breaching zones and cuts "
             "the cap by %g sq ft in those zones only."
             % (HEIGHTENED_ZONE_THRESHOLD, HEIGHTENED_CAP_REDUCTION)),
        md_v("memo_explains_supersession",
             anywhere(r"(?:supersed\w*|re-?issue\w*|replac\w*|governing|later permit)"),
             "§2 turns on the governing row of a supersession chain, not the row an item "
             "names; the memo has to say so where it decides a verdict."),
        md_v("memo_explains_pulled_items",
             anywhere(r"(?:pull\w*|comes? down|removed|does not (?:count|sit)|not standing)",
                      r"(?:allowance|standing)"),
             "§5 counts standing area only; the memo has to explain why the pulled items "
             "do not sit against the allowance."),
    ]

    # §7 asks the memo to give, for each flagged item, the code AND the record that
    # decides it. Graded as one span-everything check the model either names all of them
    # or none; graded per item it is one obligation per item, which is what §7 asks.
    for item in in_scope:
        iid = item["item_id"]
        codes = findings[iid]
        if not codes:
            continue
        zone = zones[item["zone_id"]]
        reasons = []
        if PERMIT in codes:
            pno = item["permit_no"]
            gov = governing(register, pno) if pno not in ("", "none") else None
            ids = {pno} | ({gov["permit_no"]} if gov else set())
            ids = {i for i in ids if i not in ("", "none")}
            if ids:
                reasons.append("|".join(re.escape(i) for i in sorted(ids)))
            else:
                reasons.append(r"no permit|without a permit|missing|blank|unpermitted")
        if EGRESS in codes:
            reasons.append(num_forms(item["egress_clearance_ft"]) + "|"
                           + num_forms(zone["min_egress_clearance_ft"])
                           + "|clearance|egress")
        if OVERSIZE in codes:
            reasons.append(num_forms(item["size_sqft"]) + "|"
                           + num_forms(zone["max_item_sqft"])
                           + "|cap|oversize|sq" + chr(92) + "s*ft")
        vs.append(md_v(
            "memo_item_%s" % iid.lower().replace("-", "_"),
            anywhere(*[near(iid, r) for r in reasons]),
            "HLF-7 §7 asks the memo to give every flagged item with the record that decides "
            "it. %s carries %s, so its entry has to name the deciding record beside it."
            % (iid, "|".join(codes))))


    # §8 — the three standing counterfactuals, graded per entity. Each answer is a fresh
    # application of a rule under a stated change, which a single scripted pass over the
    # inputs does not produce.
    import g970_build as _b

    saved = _b.HEIGHTENED_ZONE_THRESHOLD
    _b.HEIGHTENED_ZONE_THRESHOLD = 10 ** 9
    _, _, _, _, without6, _, _, _ = _b.audit()
    _b.HEIGHTENED_ZONE_THRESHOLD = saved
    cf_a = [k for k in findings if OVERSIZE in findings[k] and OVERSIZE not in without6[k]]

    reg_no_1006 = {k: v for k, v in register.items() if k != "PMT-1006"}
    cf_b = [i["item_id"] for i in in_scope
            if _b.permit_reaches(reg_no_1006, i["permit_no"], i["zone_id"], i["item_type"])
            and not _b.permit_reaches(register, i["permit_no"], i["zone_id"], i["item_type"])]

    cf_c = []
    for zid, z in zones.items():
        own = [i for i in in_scope if i["zone_id"] == zid]
        all_area = round(sum(float(i["size_sqft"]) for i in own), 2)
        if all_area > float(z["aggregate_allowance_sqft"]) and rollup[zid]["allowance"] == "none":
            cf_c.append(zid)

    HEIGHT_WORDS = r"heighten\w*|§\s*6|section\s*6|tighten\w*|reduced cap|without the reduction"
    REISSUE_WORDS = r"PMT-1006|re-?issue\w*|supersed\w*|PMT-1005|chain"
    PULL_WORDS = r"pull\w*|not pulled|had stood|every in-scope|all items|without the pull|standing"

    for iid in cf_a:
        vs.append(md_v("memo_cf_no_heightened_%s" % iid.lower().replace("-", "_"),
                       anywhere(near(iid, HEIGHT_WORDS)),
                       "§8(1): without §6 in force %s would no longer be OVERSIZE_COLLATERAL, "
                       "so the memo has to name it against that counterfactual." % iid))
    for iid in cf_b:
        vs.append(md_v("memo_cf_no_reissue_%s" % iid.lower().replace("-", "_"),
                       anywhere(near(iid, REISSUE_WORDS)),
                       "§8(2): had PMT-1006 never been issued, %s would have a permit "
                       "reaching it; the memo has to name it against that counterfactual." % iid))
    for zid in cf_c:
        vs.append(md_v("memo_cf_no_pull_%s" % zid.lower().replace("-", "_"),
                       anywhere(near(zid, PULL_WORDS)),
                       "§8(3): counting every in-scope item rather than the standing ones, "
                       "%s would be over its allowance; the memo has to name it." % zid))

    return vs


# ------------------------------------------------------------------------ gold

def deciding_record(item, codes, register, zones):
    bits = []
    zone = zones[item["zone_id"]]
    if PERMIT in codes:
        pno = item["permit_no"]
        if pno in ("", "none"):
            bits.append("no permit number is recorded")
        else:
            row = governing(register, pno)
            if row is None:
                bits.append("permit %s is not in the register" % pno)
            else:
                gov = row["permit_no"]
                chain = "" if gov == pno else " (the row cites %s; %s supersedes it and governs)" % (pno, gov)
                if row["covers_zones"] != "all" and item["zone_id"] not in row["covers_zones"].split(";"):
                    bits.append("%s covers %s, not %s%s" % (gov, row["covers_zones"].replace(";", " and "), item["zone_id"], chain))
                elif row["covers_item_types"] != "all" and item["item_type"] not in row["covers_item_types"].split(";"):
                    bits.append("%s covers %s only, not %s%s" % (gov, row["covers_item_types"].replace(";", " and "), item["item_type"], chain))
                else:
                    bits.append("%s expired on %s, before the review date%s" % (gov, row["valid_until"], chain))
    if EGRESS in codes:
        bits.append("clearance %s ft against the %s ft minimum in %s"
                    % (item["egress_clearance_ft"], zone["min_egress_clearance_ft"], item["zone_id"]))
    if OVERSIZE in codes:
        bits.append("%s sq ft against the %s sq ft cap in %s"
                    % (item["size_sqft"], zone["max_item_sqft"], item["zone_id"]))
    return "; ".join(bits)


def write_gold(items, in_scope, zones, register, findings, rollup, results, heightened):
    os.makedirs(GOLD, exist_ok=True)

    with open(os.path.join(GOLD, AUDIT_CSV), "w", newline="", encoding="utf-8") as fh:
        fh.write("item_id,finding\n")
        for i in in_scope:
            fh.write("%s,%s\n" % (i["item_id"], "|".join(findings[i["item_id"]]) or "none"))

    cols = ["zone_id", "item_count", "pulled_count", "standing_area_sqft",
            "aggregate_allowance_sqft", "allowance"]
    with open(os.path.join(GOLD, ZONE_CSV), "w", newline="", encoding="utf-8") as fh:
        fh.write(",".join(cols) + "\n")
        for z in rollup.values():
            fh.write(",".join(str(z[c]) for c in cols) + "\n")

    with open(os.path.join(GOLD, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
        fh.write("\n")

    out_of_scope = [i for i in items if i not in in_scope]
    breached = [z for z in rollup.values() if z["allowance"] != "none"]
    tightened = ", ".join(z["zone_id"] for z in breached)

    # §8 counterfactuals, recomputed the same way the verifiers derive them
    import g970_build as _b
    _saved = _b.HEIGHTENED_ZONE_THRESHOLD
    _b.HEIGHTENED_ZONE_THRESHOLD = 10 ** 9
    _, _, _, _, _without6, _, _, _ = _b.audit()
    _b.HEIGHTENED_ZONE_THRESHOLD = _saved
    cf_a_list = ", ".join(k for k in findings
                          if OVERSIZE in findings[k] and OVERSIZE not in _without6[k])
    _reg_no = {k: v for k, v in register.items() if k != "PMT-1006"}
    cf_b_list = ", ".join(i["item_id"] for i in in_scope
                          if _b.permit_reaches(_reg_no, i["permit_no"], i["zone_id"], i["item_type"])
                          and not _b.permit_reaches(register, i["permit_no"], i["zone_id"], i["item_type"]))
    _cf_c = []
    for _zid, _z in zones.items():
        _own = [i for i in in_scope if i["zone_id"] == _zid]
        _area = round(sum(float(i["size_sqft"]) for i in _own), 2)
        if _area > float(_z["aggregate_allowance_sqft"]) and rollup[_zid]["allowance"] == "none":
            _cf_c.append(_zid)
    cf_c_list = ", ".join(_cf_c)

    lines = []
    for i in in_scope:
        codes = findings[i["item_id"]]
        if not codes:
            continue
        lines.append("- **%s** (%s, %s) — `%s`: %s."
                     % (i["item_id"], i["item_type"], i["zone_id"], "|".join(codes),
                        deciding_record(i, codes, register, zones)))

    zone_rows = "\n".join(
        "| %s | %d | %d | %g | %g | %s |"
        % (z["zone_id"], z["item_count"], z["pulled_count"], z["standing_area_sqft"],
           z["aggregate_allowance_sqft"], z["allowance"]) for z in rollup.values())

    memo = f"""# Heritage Landing Festival — collateral and signage review (HLF-7)

Review made as of **{AUDIT_DATE.isoformat()}**.

{results['collateral_count']} in-scope items across {results['zone_count']} zones.
{results['compliant_count']} clear, {results['flagged_count']} carry at least one finding,
{results['finding_total']} findings in total. {results['zones_over_allowance']} zones are over
their allowance, and heightened inspection **is** in force.

## Out of scope

§1 holds {results['out_of_scope_count']} logged items outside §2 to §4: {', '.join(i['item_id'] for i in out_of_scope)}.
They are `standalone_graphic` and `vehicle_wrap` items — never installed at the venue — so
their permit, clearance and size values are not assessed and their area does not sit against
any zone allowance. `temporary_banner` items, by contrast, **are** installed signage under §1
and are audited in full.

## Permits and the governing row

§2 turns on the **governing** row of the register, not the row an item names. Where a permit
has been re-issued the chain has to be followed to its last row, and a re-issue can be
narrower than what it replaced: PMT-1004 → PMT-1005 → PMT-1006 ends covering ZN-03 and
`installed_signage` only, and PMT-1007 → PMT-1008 ends expired. Reading the cited row instead
of the governing one clears items that should be flagged.

## Findings by item

{chr(10).join(lines)}

## Zones

§5 counts the area **standing** in each zone. An item that fails §2 has no permit reaching it
and comes down, so it is pulled and its area does not sit against the allowance —
{results['pulled_item_count']} items were pulled on that basis.

| zone | in scope | pulled | standing sq ft | allowance | verdict |
| --- | --- | --- | --- | --- | --- |
{zone_rows}

Over allowance: {tightened}.

## Heightened inspection

{results['zones_over_allowance']} zones are in breach under §5, which reaches the §6 trigger of
{HEIGHTENED_ZONE_THRESHOLD}, so the festival is under heightened inspection. While it is in
force the §4 per-item cap drops by {HEIGHTENED_CAP_REDUCTION:g} sq ft **in the breaching zones
only** — {tightened}. Every other zone keeps the cap in the §5 table, and §2, §3 and §5 are
unchanged. The trigger reads the §5 breach count, which §4 cannot move, so it is settled once.

## Counterfactuals (§8)

**Without heightened inspection.** If §6 were not in force the caps in ZN-03, ZN-07 and ZN-08
would stand at their §5-table figures, and {cf_a_list} would no longer be
`OVERSIZE_COLLATERAL`. Nothing else changes: §2, §3 and §5 do not read the reduction.

**Without the latest re-issue.** Had `PMT-1006` never been issued, the Craft Market chain
would end at `PMT-1005`, which still covers ZN-03 and ZN-05 and is not restricted by item
type. On that footing {cf_b_list} would have a permit reaching them; as the register
actually stands, `PMT-1006` governs and they do not.

**Without the pull.** §5 counts only the items still standing. Counting every in-scope item
in a zone instead — including the ones pulled under §2 — {cf_c_list} would also be over
allowance, on top of the zones that already are.

## Figures

| figure | value |
| --- | --- |
""" + "\n".join("| `%s` | %s |" % (k, results[k]) for k, _ in RESULTS_KEYS) + "\n"

    with open(os.path.join(GOLD, MEMO), "w", encoding="utf-8") as fh:
        fh.write(memo)


def main():
    items, in_scope, zones, register, findings, rollup, results, heightened = audit()
    write_standard(zones, register)
    append_section7()
    write_instruction()
    write_gold(items, in_scope, zones, register, findings, rollup, results, heightened)

    spec = {"task_id": "gen-G970-festival-collateral-signage-permit-audit",
            "verifiers": build_verifiers(items, in_scope, zones, register,
                                         findings, rollup, results, heightened)}
    with open(os.path.join(TESTS, "verifier.json"), "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=2)
        fh.write("\n")
    print("wrote %d verifiers and 4 gold deliverables" % len(spec["verifiers"]))


if __name__ == "__main__":
    main()

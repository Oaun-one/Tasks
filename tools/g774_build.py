#!/usr/bin/env python3
"""Builds the hardened gen-g774 package: fixtures, gold deliverables, verifier set.

Fixtures, gold answer and verifier.json all come out of this one file, so the
grader and the gold can never disagree about a verdict.
"""
import json
import math
from pathlib import Path

PKG = Path("E:/WORK/TU/Task_4_gen-g774-activity-kit-print-spec-audit/gen-g774-activity-kit-print-spec-audit")

CODES = ["DPI_TOO_LOW", "MARGIN_VIOLATION", "BLEED_SHORT", "INK_OVER", "ELEMENT_COUNT_SHORT"]

# binding -> the multiple a section's imposed page count has to land on (§8)
IMPOSITION_MULTIPLE = {"saddle_stitch": 4, "perfect_bound": 2}

# stock_code -> min_dpi, min_margin_in, max_ink_pct, min_bleed_in
STOCKS = {
    "CST-100": dict(name="Coated silk 100gsm", min_dpi=300, min_margin_in=0.125, max_ink_pct=280, min_bleed_in=0.125),
    "UNC-120": dict(name="Uncoated offset 120gsm", min_dpi=240, min_margin_in=0.1875, max_ink_pct=240, min_bleed_in=0.25),
    "BRD-250": dict(name="Board 250gsm", min_dpi=260, min_margin_in=0.25, max_ink_pct=300, min_bleed_in=0.1875),
}

# section_id -> name, binding, stock_code
SECTIONS = {
    "SEC-01": dict(name="Front matter", binding="perfect_bound", stock_code="BRD-250"),
    "SEC-02": dict(name="Explorer trail", binding="saddle_stitch", stock_code="CST-100"),
    "SEC-03": dict(name="Mission deck", binding="saddle_stitch", stock_code="BRD-250"),
    "SEC-04": dict(name="Station games", binding="perfect_bound", stock_code="CST-100"),
    "SEC-05": dict(name="Grown-up pack", binding="saddle_stitch", stock_code="UNC-120"),
    "SEC-06": dict(name="Rewards", binding="perfect_bound", stock_code="UNC-120"),
    "SEC-07": dict(name="Trail extras", binding="saddle_stitch", stock_code="CST-100"),
    "SEC-08": dict(name="Take-home pack", binding="perfect_bound", stock_code="BRD-250"),
}

BASE_MIN_ELEMENTS = {
    "cover": 1,
    "parent_guide": 2,
    "map": 4,
    "activity": 4,
    "mission_cards": 6,
    "bingo": 9,
    "badge_certificate": 4,
}
# Rev B: these page types gain 2 in a saddle-stitched section.
REV_B_TYPES = {"mission_cards", "badge_certificate"}
REV_B_UPLIFT = 2

# artwork_id, page_id, revision, page_name, page_type, section_id,
# artwork_dpi, placement_scale_pct, margin_in, full_bleed_design, bleed_in, total_ink_pct, element_count
ROWS = [
    ("AW-1001", "PG-01", 1, "Front Cover", "cover", "SEC-01", 300, 100, 0.05, True, 0.1875, 295, 1),
    ("AW-1002", "PG-02", 1, "Inside Cover", "activity", "SEC-01", 260, 100, 0.02, True, 0.125, 300, 4),
    ("AW-1003", "PG-03", 1, "Welcome Letter", "parent_guide", "SEC-01", 300, 125, 0.25, False, 0.0, 210, 2),
    ("AW-1004", "PG-04", 1, "Kit Map", "map", "SEC-01", 300, 100, 0.30, False, 0.0, 250, 4),
    ("AW-1005", "PG-05", 1, "Trail Map A", "map", "SEC-02", 300, 100, 0.125, False, 0.0, 280, 4),
    ("AW-1006", "PG-06", 1, "Trail Map B", "map", "SEC-02", 450, 150, 0.12, False, 0.0, 275, 4),
    ("AW-1007", "PG-07", 1, "Trail Map C", "map", "SEC-02", 600, 200, 0.03, True, 0.25, 282, 3),
    ("AW-1008", "PG-08", 1, "Trail Activity 1", "activity", "SEC-02", 300, 110, 0.20, False, 0.0, 260, 4),
    ("AW-1009", "PG-09", 1, "Trail Activity 2", "activity", "SEC-02", 320, 100, 0.1875, False, 0.0, 240, 5),
    ("AW-1010", "PG-10", 1, "Trail Activity 3", "activity", "SEC-02", 300, 100, 0.00, True, 0.125, 279, 4),
    ("AW-1011", "PG-11", 1, "Mission Cards A", "mission_cards", "SEC-03", 300, 100, 0.30, False, 0.0, 250, 8),
    ("AW-1030", "PG-12", 3, "Mission Cards B", "mission_cards", "SEC-03", 300, 100, 0.30, False, 0.0, 250, 7),
    ("AW-1013", "PG-13", 1, "Mission Cards C", "mission_cards", "SEC-03", 260, 100, 0.26, False, 0.0, 298, 6),
    ("AW-1014", "PG-14", 1, "Mission Cards D", "mission_cards", "SEC-03", 520, 200, 0.05, True, 0.1875, 301, 9),
    ("AW-1015", "PG-15", 1, "Mission Cards E", "mission_cards", "SEC-03", 300, 120, 0.20, False, 0.0, 260, 5),
    ("AW-1016", "PG-16", 1, "Station Bingo 1", "bingo", "SEC-04", 300, 100, 0.125, False, 0.0, 270, 9),
    ("AW-1017", "PG-17", 1, "Station Bingo 2", "bingo", "SEC-04", 300, 100, 0.15, False, 0.0, 270, 8),
    ("AW-1031", "PG-18", 2, "Station Bingo 3", "bingo", "SEC-04", 300, 100, 0.00, True, 0.10, 285, 11),
    ("AW-1019", "PG-19", 1, "Mission Cards F", "mission_cards", "SEC-04", 300, 100, 0.13, False, 0.0, 240, 6),
    ("AW-1020", "PG-20", 1, "Mission Cards G", "mission_cards", "SEC-04", 240, 80, 0.14, False, 0.0, 279, 5),
    ("AW-1021", "PG-21", 1, "Station Activity", "activity", "SEC-04", 290, 100, 0.125, False, 0.0, 280, 4),
    ("AW-1022", "PG-22", 1, "Parent Guide 1", "parent_guide", "SEC-05", 240, 100, 0.1875, False, 0.0, 240, 2),
    ("AW-1023", "PG-23", 1, "Parent Guide 2", "parent_guide", "SEC-05", 250, 110, 0.18, False, 0.0, 245, 2),
    ("AW-1024", "PG-24", 1, "Badge Sheet A", "badge_certificate", "SEC-05", 300, 100, 0.20, False, 0.0, 230, 6),
    ("AW-1025", "PG-25", 1, "Badge Sheet B", "badge_certificate", "SEC-05", 300, 100, 0.01, True, 0.20, 235, 5),
    ("AW-1026", "PG-26", 1, "Certificate A", "badge_certificate", "SEC-06", 200, 100, 0.25, False, 0.0, 220, 4),
    ("AW-1032", "PG-27", 2, "Certificate B", "badge_certificate", "SEC-06", 480, 200, 0.19, False, 0.0, 239, 5),
    ("AW-1028", "PG-28", 1, "Certificate C", "badge_certificate", "SEC-06", 300, 100, 0.1875, False, 0.0, 241, 3),
    ("AW-1029", "PG-29", 1, "Reward Activity 1", "activity", "SEC-06", 300, 130, 0.04, True, 0.25, 200, 4),
    ("AW-1033", "PG-30", 1, "Reward Activity 2", "activity", "SEC-06", 260, 100, 0.15, False, 0.30, 238, 4),
    ("AW-1035", "PG-31", 1, "Trail Map D", "map", "SEC-07", 300, 100, 0.125, False, 0.0, 280, 4),
    ("AW-1036", "PG-32", 1, "Trail Sticker Sheet", "activity", "SEC-07", 240, 100, 0.02, True, 0.125, 270, 4),
    ("AW-1040", "PG-33", 2, "Mission Cards H", "mission_cards", "SEC-07", 600, 200, 0.13, False, 0.0, 281, 7),
    ("AW-1038", "PG-34", 1, "Take-home Guide", "parent_guide", "SEC-08", 260, 100, 0.25, False, 0.0, 300, 2),
    ("AW-1039", "PG-35", 2, "Take-home Badges", "badge_certificate", "SEC-08", 300, 100, 0.06, True, 0.1875, 290, 4),
    ("AW-1042", "PG-36", 1, "Take-home Activity", "activity", "SEC-08", 300, 140, 0.20, False, 0.0, 302, 3),
    # Superseded artwork. Placed so that neither "first row wins" nor "last row
    # wins" is the right heuristic: PG-12, PG-27, PG-33 and PG-35 have their live
    # revision earlier in the file, PG-04 and PG-18 later.
    ("AW-1012", "PG-12", 1, "Mission Cards B", "mission_cards", "SEC-03", 300, 100, 0.30, False, 0.0, 250, 9),
    ("AW-1027", "PG-27", 1, "Certificate B", "badge_certificate", "SEC-06", 200, 100, 0.19, False, 0.0, 239, 5),
    ("AW-1034", "PG-04", 2, "Kit Map", "map", "SEC-01", 220, 80, 0.24, False, 0.0, 305, 4),
    ("AW-1018", "PG-18", 1, "Station Bingo 3", "bingo", "SEC-04", 300, 100, 0.00, True, 0.25, 260, 11),
    ("AW-1037", "PG-33", 1, "Mission Cards H", "mission_cards", "SEC-07", 600, 200, 0.13, False, 0.0, 281, 9),
    ("AW-1041", "PG-35", 1, "Take-home Badges", "badge_certificate", "SEC-08", 300, 100, 0.30, True, 0.1875, 290, 4),
]

FIELDS = ["artwork_id", "page_id", "revision", "page_name", "page_type", "section_id",
          "artwork_dpi", "placement_scale_pct", "margin_in", "full_bleed_design",
          "bleed_in", "total_ink_pct", "element_count"]


def as_dicts():
    return [dict(zip(FIELDS, r)) for r in ROWS]


def min_elements(page_type, section_id):
    base = BASE_MIN_ELEMENTS[page_type]
    if page_type in REV_B_TYPES and SECTIONS[section_id]["binding"] == "saddle_stitch":
        base += REV_B_UPLIFT
    return base


def effective_dpi(row):
    return math.floor(row["artwork_dpi"] * 100 / row["placement_scale_pct"])


def margin_exempt(row):
    """§4 margin exemption, narrowed by §3a: only saddle-stitched full-bleed pages get it.

    A perfect-bound page is glued on the spine edge, so it carries no bleed there and the
    safe-margin rule applies to it even when the page is designed full-bleed.
    """
    return (row["full_bleed_design"]
            and SECTIONS[row["section_id"]]["binding"] == "saddle_stitch")


def adjudicate(row):
    stock = STOCKS[SECTIONS[row["section_id"]]["stock_code"]]
    findings = []
    if effective_dpi(row) < stock["min_dpi"]:
        findings.append("DPI_TOO_LOW")
    if not margin_exempt(row) and row["margin_in"] < stock["min_margin_in"]:
        findings.append("MARGIN_VIOLATION")
    if row["full_bleed_design"] and row["bleed_in"] < stock["min_bleed_in"]:
        findings.append("BLEED_SHORT")
    if row["total_ink_pct"] > stock["max_ink_pct"]:
        findings.append("INK_OVER")
    shortfall = min_elements(row["page_type"], row["section_id"]) - row["element_count"]
    if shortfall > 0:
        findings.append("ELEMENT_COUNT_SHORT")
    return [c for c in CODES if c in findings], max(shortfall, 0)


def live_rows():
    rows = as_dicts()
    best = {}
    for r in rows:
        pid = r["page_id"]
        if pid not in best or r["revision"] > best[pid]["revision"]:
            best[pid] = r
    return [best[pid] for pid in sorted(best)], len(rows) - len(best)


def impose(live, verdicts):
    """§8. A page held back for re-supply leaves the imposition, so the section rule
    reads the page-level audit rather than the raw batch."""
    rollup = {}
    for sid, sec in SECTIONS.items():
        pages = [r["page_id"] for r in live if r["section_id"] == sid]
        held = [p for p in pages if "ELEMENT_COUNT_SHORT" in verdicts[p]]
        imposed = len(pages) - len(held)
        mult = IMPOSITION_MULTIPLE[sec["binding"]]
        short = (-imposed) % mult
        rollup[sid] = {
            "section_id": sid,
            "binding": sec["binding"],
            "stock_code": sec["stock_code"],
            "live_page_count": len(pages),
            "held_back": len(held),
            "imposed_page_count": imposed,
            "flagged_pages": sum(1 for p in pages if verdicts[p]),
            "pages_needed": short,
            "imposition": "IMPOSITION_INVALID" if short else "none",
        }
    return rollup


def gold():
    live, superseded = live_rows()
    verdicts, shortfalls = {}, {}
    for r in live:
        f, s = adjudicate(r)
        verdicts[r["page_id"]] = f
        shortfalls[r["page_id"]] = s
    flagged = [p for p, f in verdicts.items() if f]
    counts = {c: sum(1 for f in verdicts.values() if c in f) for c in CODES}
    rollup = impose(live, verdicts)
    invalid = [s for s in rollup.values() if s["imposition"] != "none"]
    results = {
        "page_count": len(live),
        "superseded_count": superseded,
        "section_count": len(SECTIONS),
        "clean_count": len(live) - len(flagged),
        "flagged_count": len(flagged),
        "finding_total": sum(len(f) for f in verdicts.values()),
        "dpi_low_count": counts["DPI_TOO_LOW"],
        "margin_count": counts["MARGIN_VIOLATION"],
        "bleed_short_count": counts["BLEED_SHORT"],
        "ink_over_count": counts["INK_OVER"],
        "element_short_count": counts["ELEMENT_COUNT_SHORT"],
        "element_shortfall_total": sum(shortfalls.values()),
        "imposition_invalid_sections": len(invalid),
        "imposition_shortfall_total": sum(s["pages_needed"] for s in invalid),
    }
    return live, verdicts, shortfalls, rollup, results


if __name__ == "__main__":
    live, verdicts, shortfalls, rollup, results = gold()
    for r in live:
        sec = SECTIONS[r["section_id"]]
        st = STOCKS[sec["stock_code"]]
        print("%s r%d %-18s %s eff=%4d/%d m=%-7s/%-7s fb=%-5s bl=%-6s/%-6s ink=%3d/%3d el=%2d/%2d -> %s" % (
            r["page_id"], r["revision"], r["page_type"], sec["stock_code"],
            effective_dpi(r), st["min_dpi"], r["margin_in"], st["min_margin_in"],
            r["full_bleed_design"], r["bleed_in"], st["min_bleed_in"],
            r["total_ink_pct"], st["max_ink_pct"],
            r["element_count"], min_elements(r["page_type"], r["section_id"]),
            "|".join(verdicts[r["page_id"]]) or "none"))
    print()
    for s in rollup.values():
        print("%s %-14s live=%d held=%d imposed=%2d mult=%d flagged=%d -> %s (+%d)" % (
            s["section_id"], s["binding"], s["live_page_count"], s["held_back"],
            s["imposed_page_count"], IMPOSITION_MULTIPLE[s["binding"]],
            s["flagged_pages"], s["imposition"], s["pages_needed"]))
    print()
    print(json.dumps(results, indent=2))

"""Reference solver + data model for gen-g970-festival-collateral-signage-permit-audit.

Single source of truth: the fixtures, the gold answer and tests/verifier.json all come out
of this computation, so the grader and the gold cannot drift apart.

The rules, in the order HLF-7 states them:

  §1  scope      installed signage is defined by nature, not by one literal type string
  §2  permit     the *governing* register row must reach the item's zone and type, in date
  §3  egress     clearance against the item's own zone minimum
  §4  size       against the item's own zone cap (tightened by §6 when it fires)
  §5  aggregate  zone-level, and it reads the item audit: permit-failed items are pulled
  §6  heightened a trigger derived from §5 that reopens §4 -- terminates because §5 cannot
                 be moved by §4
"""

from __future__ import annotations

import csv
import os
from datetime import date

ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "tasks/g970",
    "gen-g970-festival-collateral-signage-permit-audit",
)
INPUT = os.path.join(ROOT, "environment", "input")
GOLD = os.path.join(ROOT, "solution", "files")
TESTS = os.path.join(ROOT, "tests")

AUDIT_DATE = date(2026, 8, 20)

PERMIT = "PERMIT_NUMBER_MISSING"
EGRESS = "EGRESS_MARKER_OBSTRUCTED"
OVERSIZE = "OVERSIZE_COLLATERAL"
CODES = [PERMIT, EGRESS, OVERSIZE]

ZONE_BREACH = "ZONE_ALLOWANCE_BREACH"

# §1 — recorded types that ARE installed signage. The standard defines the class by nature
# (physically mounted or displayed at the venue); these are the recorded types that qualify.
INSTALLED_TYPES = {"installed_signage", "temporary_banner"}

# §6 — the festival goes to heightened inspection when this many zones breach §5.
HEIGHTENED_ZONE_THRESHOLD = 3
# and the per-item cap drops by this many square feet -- but only in the zones that
# are actually over their allowance.
HEIGHTENED_CAP_REDUCTION = 1.0


def read_csv(name):
    with open(os.path.join(INPUT, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def as_date(text):
    return date(*(int(part) for part in text.split("-")))


def governing(register, permit_no):
    """§2 — follow `supersedes` to the row whose terms actually govern."""
    row = register.get(permit_no)
    seen = set()
    while row is not None:
        nxt = next((r for r in register.values() if r["supersedes"] == row["permit_no"]), None)
        if nxt is None or nxt["permit_no"] in seen:
            break
        seen.add(nxt["permit_no"])
        row = nxt
    return row


def permit_reaches(register, permit_no, zone_id, item_type):
    """§2 — all four conditions, against the governing row."""
    if permit_no in ("", "none"):
        return False
    row = governing(register, permit_no)
    if row is None:
        return False
    zones = row["covers_zones"]
    if zones != "all" and zone_id not in zones.split(";"):
        return False
    types = row["covers_item_types"]
    if types != "all" and item_type not in types.split(";"):
        return False
    return as_date(row["valid_until"]) >= AUDIT_DATE


def audit():
    items = read_csv("collateral_log.csv")
    zones = {z["zone_id"]: z for z in read_csv("venue_zones.csv")}
    register = {p["permit_no"]: p for p in read_csv("permit_register.csv")}

    in_scope = [i for i in items if i["item_type"] in INSTALLED_TYPES]

    def base_findings(item, tightened_zones):
        zone = zones[item["zone_id"]]
        cap_reduction = HEIGHTENED_CAP_REDUCTION if item["zone_id"] in tightened_zones else 0.0
        found = []
        if not permit_reaches(register, item["permit_no"], item["zone_id"], item["item_type"]):
            found.append(PERMIT)
        if float(item["egress_clearance_ft"]) < float(zone["min_egress_clearance_ft"]):
            found.append(EGRESS)
        cap = float(zone["max_item_sqft"]) - cap_reduction
        if float(item["size_sqft"]) > cap:
            found.append(OVERSIZE)
        return [c for c in CODES if c in found]

    # pass 1 — §2 to §4 with the caps as written
    findings = {i["item_id"]: base_findings(i, frozenset()) for i in in_scope}

    def zone_rollup(current):
        """§5 — an item whose permit does not reach it is pulled from the display, so its
        area does not sit against the zone allowance."""
        rollup = {}
        for zid, z in zones.items():
            own = [i for i in in_scope if i["zone_id"] == zid]
            pulled = [i for i in own if PERMIT in current[i["item_id"]]]
            standing = [i for i in own if PERMIT not in current[i["item_id"]]]
            area = round(sum(float(i["size_sqft"]) for i in standing), 2)
            allowance = float(z["aggregate_allowance_sqft"])
            rollup[zid] = {
                "zone_id": zid,
                "item_count": len(own),
                "pulled_count": len(pulled),
                "standing_area_sqft": area,
                "aggregate_allowance_sqft": allowance,
                "allowance": ZONE_BREACH if area > allowance else "none",
            }
        return rollup

    rollup = zone_rollup(findings)

    # §6 — the trigger is the §5 breach count, which §4 cannot move (§5 counts standing
    # area, and standing depends on §2 only). So this fires once and does not oscillate.
    breached = sum(1 for z in rollup.values() if z["allowance"] != "none")
    heightened = breached >= HEIGHTENED_ZONE_THRESHOLD
    if heightened:
        tightened = frozenset(z for z, r in rollup.items() if r["allowance"] != "none")
        findings = {i["item_id"]: base_findings(i, tightened) for i in in_scope}
        rollup = zone_rollup(findings)

    flagged = [k for k, f in findings.items() if f]
    counts = {c: sum(1 for f in findings.values() if c in f) for c in CODES}
    results = {
        "collateral_count": len(in_scope),
        "zone_count": len(zones),
        "permit_missing_count": counts[PERMIT],
        "egress_obstructed_count": counts[EGRESS],
        "oversize_count": counts[OVERSIZE],
        "compliant_count": len(in_scope) - len(flagged),
        "flagged_count": len(flagged),
        "finding_total": sum(len(f) for f in findings.values()),
        "out_of_scope_count": len(items) - len(in_scope),
        "pulled_item_count": sum(z["pulled_count"] for z in rollup.values()),
        "zones_over_allowance": sum(1 for z in rollup.values() if z["allowance"] != "none"),
    }
    return items, in_scope, zones, register, findings, rollup, results, heightened


if __name__ == "__main__":
    import json

    items, in_scope, zones, register, findings, rollup, results, heightened = audit()
    print("heightened inspection:", heightened)
    for z in rollup.values():
        print("  %s items=%2d pulled=%d standing=%7.2f / %7.2f -> %s"
              % (z["zone_id"], z["item_count"], z["pulled_count"],
                 z["standing_area_sqft"], z["aggregate_allowance_sqft"], z["allowance"]))
    print()
    print(json.dumps(results, indent=2))

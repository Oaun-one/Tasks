"""Runs every plausible misreading of HLF-7 through the real grader.

If a misreading scores 1.0, that misreading is a free pass and the task does not
discriminate. Target: each one loses at least three verifiers.
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g970_build as b  # noqa: E402
from g970_emit import RESULTS_KEYS  # noqa: E402


def build(scope_literal=False, ignore_supersedes=False, flat_limits=False,
          count_all_items=False, no_section6=False, section6_all_zones=False,
          dates_exclusive=False):
    items = b.read_csv("collateral_log.csv")
    zones = {z["zone_id"]: z for z in b.read_csv("venue_zones.csv")}
    register = {p["permit_no"]: p for p in b.read_csv("permit_register.csv")}

    types = {"installed_signage"} if scope_literal else b.INSTALLED_TYPES
    in_scope = [i for i in items if i["item_type"] in types]

    def reaches(pno, zid, itype):
        if pno in ("", "none"):
            return False
        row = register.get(pno) if ignore_supersedes else b.governing(register, pno)
        if row is None:
            return False
        if row["covers_zones"] != "all" and zid not in row["covers_zones"].split(";"):
            return False
        if row["covers_item_types"] != "all" and itype not in row["covers_item_types"].split(";"):
            return False
        d = b.as_date(row["valid_until"])
        return d > b.AUDIT_DATE if dates_exclusive else d >= b.AUDIT_DATE

    FLAT_CLEAR, FLAT_CAP = 6.0, 12.0

    def findings_for(tightened):
        out = {}
        for i in in_scope:
            z = zones[i["zone_id"]]
            f = []
            if not reaches(i["permit_no"], i["zone_id"], i["item_type"]):
                f.append(b.PERMIT)
            min_clear = FLAT_CLEAR if flat_limits else float(z["min_egress_clearance_ft"])
            if float(i["egress_clearance_ft"]) < min_clear:
                f.append(b.EGRESS)
            cap = FLAT_CAP if flat_limits else float(z["max_item_sqft"])
            if i["zone_id"] in tightened:
                cap -= b.HEIGHTENED_CAP_REDUCTION
            if float(i["size_sqft"]) > cap:
                f.append(b.OVERSIZE)
            out[i["item_id"]] = [c for c in b.CODES if c in f]
        return out

    def rollup_for(cur):
        r = {}
        for zid, z in zones.items():
            own = [i for i in in_scope if i["zone_id"] == zid]
            pulled = [i for i in own if b.PERMIT in cur[i["item_id"]]]
            standing = own if count_all_items else [i for i in own if b.PERMIT not in cur[i["item_id"]]]
            area = round(sum(float(i["size_sqft"]) for i in standing), 2)
            allow = float(z["aggregate_allowance_sqft"])
            r[zid] = dict(zone_id=zid, item_count=len(own), pulled_count=len(pulled),
                          standing_area_sqft=area, aggregate_allowance_sqft=allow,
                          allowance=b.ZONE_BREACH if area > allow else "none")
        return r

    f = findings_for(frozenset())
    roll = rollup_for(f)
    breached = sum(1 for z in roll.values() if z["allowance"] != "none")
    if not no_section6 and breached >= b.HEIGHTENED_ZONE_THRESHOLD:
        tight = (frozenset(zones) if section6_all_zones
                 else frozenset(z for z, r in roll.items() if r["allowance"] != "none"))
        f = findings_for(tight)
        roll = rollup_for(f)

    flagged = [k for k, v in f.items() if v]
    counts = {c: sum(1 for v in f.values() if c in v) for c in b.CODES}
    res = {
        "collateral_count": len(in_scope), "zone_count": len(zones),
        "permit_missing_count": counts[b.PERMIT], "egress_obstructed_count": counts[b.EGRESS],
        "oversize_count": counts[b.OVERSIZE], "compliant_count": len(in_scope) - len(flagged),
        "flagged_count": len(flagged), "finding_total": sum(len(v) for v in f.values()),
        "out_of_scope_count": len(items) - len(in_scope),
        "pulled_item_count": sum(z["pulled_count"] for z in roll.values()),
        "zones_over_allowance": sum(1 for z in roll.values() if z["allowance"] != "none"),
    }
    return in_scope, f, roll, res


VARIANTS = {
    "scope read off the literal type string": dict(scope_literal=True),
    "ignores the supersedes chain": dict(ignore_supersedes=True),
    "one flat clearance and cap for all zones": dict(flat_limits=True),
    "zone allowance counts every item, not standing": dict(count_all_items=True),
    "misses §6 heightened inspection": dict(no_section6=True),
    "§6 tightens every zone, not just breaching": dict(section6_all_zones=True),
    "validity dates read as exclusive": dict(dates_exclusive=True),
}


def run(label, in_scope, f, roll, res, gold_memo):
    ws = tempfile.mkdtemp(prefix="g970neg-")
    shutil.copy(os.path.join(b.GOLD, "collateral_memo.md"), ws)
    with open(os.path.join(ws, "collateral_audit.csv"), "w", newline="", encoding="utf-8") as fh:
        fh.write("item_id,finding\n")
        for i in in_scope:
            fh.write("%s,%s\n" % (i["item_id"], "|".join(f[i["item_id"]]) or "none"))
    cols = ["zone_id", "item_count", "pulled_count", "standing_area_sqft",
            "aggregate_allowance_sqft", "allowance"]
    with open(os.path.join(ws, "zone_summary.csv"), "w", newline="", encoding="utf-8") as fh:
        fh.write(",".join(cols) + "\n")
        for z in roll.values():
            fh.write(",".join(str(z[c]) for c in cols) + "\n")
    json.dump(res, open(os.path.join(ws, "results.json"), "w", encoding="utf-8"), indent=2)
    p = subprocess.run([sys.executable, "-m", "pytest",
                        os.path.join(b.ROOT, "tests", "test_outputs.py"), "-q", "--no-header"],
                       capture_output=True, text=True, cwd=b.ROOT,
                       env={**os.environ, "HARBOR_TASK_WORKSPACE": ws})
    tail = [l for l in p.stdout.splitlines() if "passed" in l or "failed" in l]
    shutil.rmtree(ws, ignore_errors=True)
    return p.returncode, (tail[-1] if tail else "?")


if __name__ == "__main__":
    gold_memo = os.path.join(b.GOLD, "collateral_memo.md")
    ok = True
    for label, kw in VARIANTS.items():
        in_scope, f, roll, res = build(**kw)
        rc, summary = run(label, in_scope, f, roll, res, gold_memo)
        if rc == 0:
            ok = False
        print("  %-46s %-10s %s" % (label, "REJECTED" if rc else "*** ACCEPTED ***", summary))
    print("\n" + ("all misreadings rejected" if ok else "LEAK: a misreading scored 1.0"))

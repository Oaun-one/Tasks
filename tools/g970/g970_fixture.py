"""Writes the g970 fixtures: venue zones, permit register, collateral log.

Boundaries are placed on purpose:
  * items sitting exactly on their zone's size cap and exactly on its egress minimum
  * permits expiring exactly on the audit date (still current) and one day before
  * three-hop supersession chains that narrow zone scope and item-type scope
  * two zones whose standing area lands within 1 sq ft of their allowance
  * out-of-scope types that look auditable, and a `temporary_banner` type that IS
    installed signage but does not match the literal string `installed_signage`
"""
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from g970_build import INPUT  # noqa: E402

IN = pathlib.Path(INPUT)

# zone_id, name, min_egress_clearance_ft, max_item_sqft, aggregate_allowance_sqft, authority
ZONES = [
    ("ZN-01", "Main Gate Approach",   6.0, 12.0, 60.0, "City Fire Marshal"),
    ("ZN-02", "Riverside Promenade",  4.0, 16.0, 80.0, "Parks Authority"),
    ("ZN-03", "Craft Market Row",     4.0,  8.0, 40.0, "Parks Authority"),
    ("ZN-04", "Main Stage Apron",     8.0, 10.0, 50.0, "City Fire Marshal"),
    ("ZN-05", "Heritage Courtyard",   5.0,  6.0, 30.0, "Heritage Trust"),
    ("ZN-06", "Food Court",           6.0, 14.0, 70.0, "City Fire Marshal"),
    ("ZN-07", "North Car Park",       3.0, 20.0, 90.0, "Parks Authority"),
    ("ZN-08", "Volunteer Compound",   3.0, 10.0, 45.0, "Parks Authority"),
]

# permit_no, holder, covers_zones, covers_item_types, valid_until, supersedes
PERMITS = [
    ("PMT-1001", "Heritage Landing Festival Ltd", "all", "all", "2026-12-31", "none"),
    ("PMT-1002", "Riverside Traders Assoc", "ZN-02;ZN-03", "installed_signage", "2026-08-20", "none"),
    ("PMT-1003", "Main Stage Productions", "ZN-04", "all", "2026-08-19", "none"),
    # three-hop chain, narrowing zones then item types
    ("PMT-1004", "Craft Market Collective", "ZN-02;ZN-03;ZN-05", "all", "2026-09-30", "none"),
    ("PMT-1005", "Craft Market Collective", "ZN-03;ZN-05", "all", "2027-03-31", "PMT-1004"),
    ("PMT-1006", "Craft Market Collective", "ZN-03", "installed_signage", "2027-06-30", "PMT-1005"),
    # second chain, ends expired
    ("PMT-1007", "Food Court Vendors", "ZN-06", "all", "2027-01-31", "none"),
    ("PMT-1008", "Food Court Vendors", "ZN-06", "all", "2026-08-19", "PMT-1007"),
    ("PMT-1009", "Heritage Trust Signage", "ZN-05", "temporary_banner", "2027-05-31", "none"),
    ("PMT-1010", "Gate Contractors", "ZN-01", "installed_signage", "2027-02-28", "none"),
    ("PMT-1011", "Parking Services", "ZN-07;ZN-08", "installed_signage", "2026-08-20", "none"),
    ("PMT-1012", "Volunteer Ops", "ZN-08", "temporary_banner", "2027-04-30", "none"),
    ("PMT-1013", "Promenade Arts", "ZN-02", "temporary_banner", "2027-07-31", "none"),
    ("PMT-1014", "Legacy Contractor", "ZN-01;ZN-04", "all", "2026-08-21", "none"),
]

FIELDS = ["item_id", "item_type", "zone_id", "permit_no",
          "egress_clearance_ft", "size_sqft", "installed_on"]

IS = "installed_signage"
TB = "temporary_banner"
SG = "standalone_graphic"
VW = "vehicle_wrap"

# item_type, zone, permit, egress_ft, size_sqft
ITEMS = [
    # ZN-01 cap 12.0, egress 6.0, allowance 60.0
    (IS, "ZN-01", "PMT-1010", 6.0, 12.0),    # both exactly on the limits -> clean
    (IS, "ZN-01", "PMT-1010", 5.9, 11.0),    # egress just under
    (IS, "ZN-01", "PMT-1010", 7.0, 12.5),    # oversize by 0.5
    (IS, "ZN-01", "PMT-1014", 7.0, 10.0),    # permit expires 2026-08-21 -> in date
    (IS, "ZN-01", "PMT-1002", 7.0, 9.0),     # permit does not cover ZN-01
    (TB, "ZN-01", "PMT-1010", 7.0, 8.0),     # banner, but PMT-1010 covers installed_signage only
    (SG, "ZN-01", "", 1.0, 40.0),            # out of scope entirely
    # ZN-02 cap 16.0, egress 4.0, allowance 80.0
    (IS, "ZN-02", "PMT-1002", 4.0, 16.0),    # exactly on both -> clean
    (IS, "ZN-02", "PMT-1002", 3.9, 15.0),
    (IS, "ZN-02", "PMT-1004", 5.0, 14.0),    # chain: 1004 -> 1006 covers ZN-03 only
    (TB, "ZN-02", "PMT-1013", 5.0, 15.0),
    (TB, "ZN-02", "PMT-1002", 5.0, 12.0),    # 1002 is installed_signage only
    (IS, "ZN-02", "PMT-1001", 5.0, 16.5),
    (VW, "ZN-02", "", 0.0, 60.0),            # out of scope
    # ZN-03 cap 8.0, egress 4.0, allowance 40.0
    (IS, "ZN-03", "PMT-1006", 4.0, 8.0),     # on both limits -> clean
    (IS, "ZN-03", "PMT-1004", 4.5, 7.5),     # chain resolves to 1006, covers ZN-03 + IS -> ok
    (TB, "ZN-03", "PMT-1004", 4.5, 7.0),     # chain -> 1006 is installed_signage only -> permit
    (IS, "ZN-03", "PMT-1006", 3.5, 8.5),
    (IS, "ZN-03", "PMT-1006", 4.5, 7.0),
    (IS, "ZN-03", "PMT-1006", 4.5, 7.0),
    (IS, "ZN-03", "PMT-1006", 4.5, 6.5),
    (SG, "ZN-03", "", 1.0, 30.0),
    # ZN-04 cap 10.0, egress 8.0, allowance 50.0
    (IS, "ZN-04", "PMT-1003", 8.0, 10.0),    # 1003 expired 2026-08-19 -> permit
    (IS, "ZN-04", "PMT-1014", 8.0, 10.0),    # clean, on both limits
    (IS, "ZN-04", "PMT-1014", 7.9, 9.0),
    (IS, "ZN-04", "PMT-1014", 9.0, 10.5),
    (TB, "ZN-04", "PMT-1014", 9.0, 9.5),
    (IS, "ZN-04", "PMT-1001", 9.0, 9.0),
    # ZN-05 cap 6.0, egress 5.0, allowance 30.0
    (TB, "ZN-05", "PMT-1009", 5.0, 6.0),     # on both -> clean
    (IS, "ZN-05", "PMT-1009", 5.5, 5.5),     # 1009 is temporary_banner only -> permit
    (IS, "ZN-05", "PMT-1005", 5.5, 5.0),     # chain 1005 -> 1006 covers ZN-03 only -> permit
    (TB, "ZN-05", "PMT-1009", 4.9, 5.0),
    (IS, "ZN-05", "PMT-1001", 5.5, 6.5),
    (TB, "ZN-05", "PMT-1009", 5.5, 6.0),
    # ZN-06 cap 14.0, egress 6.0, allowance 70.0
    (IS, "ZN-06", "PMT-1007", 6.0, 14.0),    # chain 1007 -> 1008 expired -> permit
    (IS, "ZN-06", "PMT-1001", 6.0, 14.0),    # clean, on both
    (IS, "ZN-06", "PMT-1001", 5.9, 13.0),
    (IS, "ZN-06", "PMT-1001", 6.5, 14.5),
    (TB, "ZN-06", "PMT-1001", 6.5, 13.5),
    (IS, "ZN-06", "PMT-1008", 6.5, 12.0),    # 1008 itself expired
    (SG, "ZN-06", "", 1.0, 25.0),
    # ZN-07 cap 20.0, egress 3.0, allowance 90.0
    (IS, "ZN-07", "PMT-1011", 3.0, 20.0),    # on both -> clean
    (IS, "ZN-07", "PMT-1011", 2.9, 19.0),
    (IS, "ZN-07", "PMT-1011", 3.5, 20.5),
    (IS, "ZN-07", "PMT-1011", 3.5, 18.0),
    (TB, "ZN-07", "PMT-1011", 3.5, 17.0),
    (VW, "ZN-07", "", 0.0, 80.0),
    # ZN-08 cap 10.0, egress 3.0, allowance 45.0
    (TB, "ZN-08", "PMT-1012", 3.0, 10.0),    # on both -> clean
    (IS, "ZN-08", "PMT-1012", 3.5, 9.0),     # 1012 is temporary_banner only -> permit
    (IS, "ZN-08", "PMT-1011", 2.9, 9.5),
    (IS, "ZN-08", "PMT-1011", 3.5, 10.5),
    (TB, "ZN-08", "PMT-1012", 3.5, 9.0),
    (IS, "ZN-08", "PMT-1011", 3.5, 9.0),
    (IS, "ZN-08", "", 3.5, 8.0),             # no permit at all
    (SG, "ZN-08", "", 1.0, 20.0),
    # a few more to push two zones close to their allowance
    (IS, "ZN-03", "PMT-1006", 4.5, 6.0),
    (IS, "ZN-06", "PMT-1001", 6.5, 13.0),
    (IS, "ZN-02", "PMT-1001", 5.0, 15.0),
    (IS, "ZN-07", "PMT-1011", 3.5, 16.0),
    # further banner/permit type mismatches, in both directions
    (TB, "ZN-01", "PMT-1010", 6.5, 7.0),
    (TB, "ZN-02", "PMT-1002", 4.5, 11.0),
    (TB, "ZN-03", "PMT-1006", 4.5, 6.0),
    (TB, "ZN-07", "PMT-1011", 3.5, 15.0),
    (TB, "ZN-08", "PMT-1011", 3.5, 8.0),
    (IS, "ZN-05", "PMT-1009", 5.5, 4.5),
    (IS, "ZN-02", "PMT-1013", 4.5, 10.0),
]


def main():
    IN.mkdir(parents=True, exist_ok=True)

    with (IN / "venue_zones.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["zone_id", "zone_name", "min_egress_clearance_ft", "max_item_sqft",
                    "aggregate_allowance_sqft", "permit_authority"])
        w.writerows(ZONES)

    with (IN / "permit_register.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["permit_no", "holder", "covers_zones", "covers_item_types",
                    "valid_until", "supersedes"])
        w.writerows(PERMITS)

    with (IN / "collateral_log.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(FIELDS)
        for n, (itype, zone, permit, egress, size) in enumerate(ITEMS, start=1):
            w.writerow([f"COL-{n:02d}", itype, zone, permit or "none",
                        f"{egress:g}", f"{size:g}", "2026-08-14"])

    print(f"  venue_zones.csv      {len(ZONES)} zones")
    print(f"  permit_register.csv  {len(PERMITS)} permits")
    print(f"  collateral_log.csv   {len(ITEMS)} items")


if __name__ == "__main__":
    main()

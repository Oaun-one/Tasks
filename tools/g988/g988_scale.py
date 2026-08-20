"""Scales the gen-g988 fixture: 8 -> 12 accounts, 10 -> 18 licences, 32 -> 70 log rows.

Existing rows are left untouched, so every trap already designed survives. What is added
is depth and density, not new rules:

  * two three-hop supersession chains, each narrowing at every step, so a reader who
    stops at the first successor still gets the wrong terms
  * many more measurements sitting exactly on a limit (area on the cap, validity on the
    audit date) where inclusive/exclusive decides the verdict
  * enough rows that the audit stops being eyeballable

Run once: python tools/g988_scale.py
"""
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from g988_build import INPUT  # noqa: E402

IN = pathlib.Path(INPUT)

NEW_ACCOUNTS = [
    ("ACC-09", "Vireo Brand Studio", "studio_partner", "social_public;print_for_sale", "active"),
    ("ACC-10", "Alder Street Portraits", "consumer", "none", "active"),
    ("ACC-11", "Kestrel Sports Media", "press_agency", "print_for_sale", "lapsed"),
    ("ACC-12", "Marlow Fan Collective", "studio_partner", "social_public", "active"),
]

# license_id, property, holder, type, covers, valid_until, max_area, supersedes
NEW_LICENCES = [
    # three-hop character chain: 111 -> 112 -> 113, narrowing scope and cap at each step
    ("LIC-111", "Verdant Automata", "Orrery Studios", "character", "social_public;print_for_sale", "2026-05-31", "40", "none"),
    ("LIC-112", "Verdant Automata", "Orrery Studios", "character", "social_public;print_for_sale", "2027-01-31", "30", "LIC-111"),
    ("LIC-113", "Verdant Automata", "Orrery Studios", "character", "social_public", "2027-09-30", "22", "LIC-112"),
    # three-hop background chain: 114 -> 115 -> 116, ending client_internal only
    ("LIC-114", "Tidewater Docks", "Northlight Images", "background", "all", "2026-06-30", "none", "none"),
    ("LIC-115", "Tidewater Docks", "Northlight Images", "background", "all", "2027-02-28", "none", "LIC-114"),
    ("LIC-116", "Tidewater Docks", "Northlight Images", "background", "client_internal", "2028-01-31", "none", "LIC-115"),
    # flat licences, one expiring exactly on the audit date
    ("LIC-117", "Pockets the Fox", "Skyline Animation", "character", "all", "2027-12-31", "35", "none"),
    ("LIC-118", "Gantry Yard Dusk", "Vantage Photo", "background", "social_public;print_for_sale", "2026-03-31", "none", "none"),
]

W = "withdrawn"
A = "active"
CO, CI, SP, PS = "customer_original", "client_internal", "social_public", "print_for_sale"
PO = "personal_only"
TPU, TPL = "third_party_unlicensed", "third_party_licensed"

# request_id, status, account, title, char_prop, char_lic, char_px, canvas_px,
# bg_source, bg_lic, distribution, minor, consent_type, consent_until, alteration, disclosure
NEW_REQUESTS = [
    # --- ACC-09: three-hop chain, area on the cap, boundary dates
    ("REQ-33", A, "ACC-09", "Automata Launch Key Art", "Verdant Automata", "LIC-111", 220000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-34", A, "ACC-09", "Automata Retail Poster", "Verdant Automata", "LIC-111", 210000, 1000000, CO, "none", PS, "False", "none", "none", "none", "False"),
    ("REQ-35", A, "ACC-09", "Automata Teaser Tile", "Verdant Automata", "LIC-112", 221000, 1000000, CO, "none", SP, "False", "none", "none", "substantive", "True"),
    ("REQ-36", A, "ACC-09", "Dockside Editorial", "none", "none", 0, 1000000, TPL, "LIC-114", PS, "False", "none", "none", "none", "False"),
    ("REQ-37", A, "ACC-09", "Dockside Internal Deck", "none", "none", 0, 1000000, TPL, "LIC-114", CI, "False", "none", "none", "none", "False"),
    ("REQ-38", W, "ACC-09", "Automata Sizzle Frame", "Verdant Automata", "LIC-113", 500000, 1000000, TPU, "none", SP, "True", "none", "none", "substantive", "False"),
    # --- ACC-10: consumer, personal-use allowance and its scope
    ("REQ-39", A, "ACC-10", "Family Fox Portrait", "Pockets the Fox", "LIC-117", 600000, 1000000, CO, "none", PO, "False", "none", "none", "none", "False"),
    ("REQ-40", A, "ACC-10", "Nursery Fox Print", "Pockets the Fox", "LIC-117", 350000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-41", A, "ACC-10", "Grandparents Keepsake", "Pockets the Fox", "LIC-117", 800000, 1000000, CO, "none", PO, "True", "basic", "2027-06-30", "none", "False"),
    ("REQ-42", A, "ACC-10", "School Gate Montage", "none", "none", 0, 1000000, CO, "none", SP, "True", "basic", "2027-06-30", "none", "False"),
    # --- ACC-11: lapsed agreement, press distribution
    ("REQ-43", A, "ACC-11", "Match Report Composite", "none", "none", 0, 1000000, TPL, "LIC-118", PS, "False", "none", "none", "none", "False"),
    ("REQ-44", A, "ACC-11", "Terrace Panorama", "none", "none", 0, 1000000, TPL, "LIC-118", SP, "False", "none", "none", "substantive", "True"),
    ("REQ-45", A, "ACC-11", "Youth Cup Feature", "none", "none", 0, 1000000, CO, "none", PS, "True", "publicity", "2026-03-31", "none", "False"),
    ("REQ-46", A, "ACC-11", "Squad Internal Sheet", "none", "none", 0, 1000000, CO, "none", CI, "False", "none", "none", "substantive", "False"),
    ("REQ-47", W, "ACC-11", "Sponsor Board Mock", "none", "none", 0, 1000000, TPU, "none", PS, "False", "none", "none", "none", "False"),
    # --- ACC-12: fan collective, character caps at the edge
    ("REQ-48", A, "ACC-12", "Marlow Anniversary Tile", "Captain Marlow", "LIC-101", 300000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-49", A, "ACC-12", "Marlow Banner Wide", "Captain Marlow", "LIC-101", 301000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-50", A, "ACC-12", "Marlow Merch Sheet", "Captain Marlow", "LIC-101", 250000, 1000000, CO, "none", PS, "False", "none", "none", "substantive", "False"),
    ("REQ-51", A, "ACC-12", "Fan Meetup Backdrop", "none", "none", 0, 1000000, TPL, "LIC-115", SP, "False", "none", "none", "none", "False"),
    # --- back-fill across the original accounts, adding density
    ("REQ-52", A, "ACC-01", "Garden Party Collage", "none", "none", 0, 1000000, CO, "none", PO, "False", "none", "none", "none", "False"),
    ("REQ-53", A, "ACC-01", "Christening Print", "none", "none", 0, 1000000, CO, "none", SP, "True", "publicity", "2026-03-30", "none", "False"),
    ("REQ-54", A, "ACC-02", "Studio Reel Cover", "Verdant Automata", "LIC-112", 300000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-55", A, "ACC-02", "Brand Deck Plate", "none", "none", 0, 1000000, TPL, "LIC-116", CI, "False", "none", "none", "none", "False"),
    ("REQ-56", A, "ACC-03", "Weekend Long Read", "none", "none", 0, 1000000, TPL, "LIC-118", PS, "False", "none", "none", "none", "False"),
    ("REQ-57", A, "ACC-03", "Newsroom Fox Sidebar", "Pockets the Fox", "LIC-117", 351000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-58", W, "ACC-03", "Spiked Feature Art", "none", "none", 0, 1000000, TPU, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-59", A, "ACC-04", "Yearbook Spread", "none", "none", 0, 1000000, CO, "none", CI, "True", "basic", "2026-03-31", "none", "False"),
    ("REQ-60", A, "ACC-05", "Quarry Listing Wide", "none", "none", 0, 1000000, TPL, "LIC-114", PS, "False", "none", "none", "none", "False"),
    ("REQ-61", A, "ACC-05", "Agent Portrait Plate", "none", "none", 0, 1000000, CO, "none", CI, "False", "none", "none", "substantive", "False"),
    ("REQ-62", A, "ACC-06", "Label Poster Reissue", "Verdant Automata", "LIC-111", 219000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-63", A, "ACC-06", "Tour Internal Brief", "none", "none", 0, 1000000, TPL, "LIC-116", CI, "False", "none", "none", "none", "False"),
    ("REQ-64", A, "ACC-07", "Reception Collage", "none", "none", 0, 1000000, CO, "none", PO, "False", "none", "none", "substantive", "False"),
    ("REQ-65", A, "ACC-07", "Save The Date Card", "Nimbus the Cat", "LIC-102", 240000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-66", A, "ACC-08", "Season Ticket Art", "none", "none", 0, 1000000, TPL, "LIC-118", PS, "False", "none", "none", "none", "False"),
    ("REQ-67", A, "ACC-08", "Junior Team Sheet", "none", "none", 0, 1000000, CO, "none", CI, "True", "basic", "2027-01-31", "none", "False"),
    ("REQ-68", A, "ACC-04", "Prize Day Montage", "Captain Marlow", "LIC-101", 299000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
    ("REQ-69", A, "ACC-12", "Marlow Print Run", "Captain Marlow", "LIC-101", 200000, 1000000, TPL, "LIC-115", PS, "False", "none", "none", "none", "False"),
    ("REQ-70", W, "ACC-10", "Cancelled Pet Portrait", "Pockets the Fox", "LIC-117", 400000, 1000000, CO, "none", SP, "False", "none", "none", "none", "False"),
]


def append(path, rows):
    existing = list(csv.reader(path.open(encoding="utf-8")))
    header = existing[0]
    ids = {r[0] for r in existing[1:]}
    added = [r for r in rows if r[0] not in ids]
    with path.open("a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(added)
    print(f"  {path.name}: +{len(added)} rows (now {len(existing) - 1 + len(added)})")
    return len(header)


def main():
    append(IN / "client_accounts.csv", NEW_ACCOUNTS)
    append(IN / "licensed_property_register.csv", NEW_LICENCES)
    append(IN / "composite_request_log.csv", [[str(x) for x in r] for r in NEW_REQUESTS])


if __name__ == "__main__":
    main()

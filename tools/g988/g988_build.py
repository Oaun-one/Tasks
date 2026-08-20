"""Reference solver + package builder for gen-g988-composite-photo-request-rights-audit.

Reads environment/input/, applies INT-09 rev 4 as written, and writes:
  solution/files/composite_request_audit.csv
  solution/files/account_summary.csv
  solution/files/composite_request_memo.md
  solution/files/results.json
  tests/verifier.json

Everything graded is computed here, so the gold and the verifier set cannot drift
apart. Run from anywhere: python tools/g988_build.py
"""

from __future__ import annotations

import csv
import json
import os
from datetime import date

ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "tasks/g988",
    "gen-g988-composite-photo-request-rights-audit",
)
INPUT = os.path.join(ROOT, "environment", "input")
GOLD = os.path.join(ROOT, "solution", "files")
TESTS = os.path.join(ROOT, "tests")

AUDIT_DATE = date(2026, 3, 31)

CHARACTER = "UNLICENSED_CHARACTER_USE"
BACKGROUND = "THIRD_PARTY_BACKGROUND_UNLICENSED"
CONSENT = "MISSING_MINOR_CONSENT"
COMMERCIAL = "COMMERCIAL_DISTRIBUTION_FLAG"
DISCLOSURE = "ALTERATION_DISCLOSURE_MISSING"
CODES = [CHARACTER, BACKGROUND, CONSENT, COMMERCIAL, DISCLOSURE]

PUBLIC_OR_PAID = {"social_public", "print_for_sale"}

# §10 — the batch enters heightened review when the §3 total reaches this.
HEIGHTENED_REVIEW_THRESHOLD = 12


def read_csv(name):
    with open(os.path.join(INPUT, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def as_date(text):
    return date(*(int(part) for part in text.split("-")))


def governing(register, licence_id):
    """INT-09 §2 — follow the supersession chain to the row whose terms govern."""
    lic = register.get(licence_id)
    seen = set()
    while lic is not None:
        successor = next(
            (r for r in register.values() if r["supersedes"] == lic["license_id"]), None
        )
        if successor is None or successor["license_id"] in seen:
            break
        seen.add(successor["license_id"])
        lic = successor
    return lic


def licence_covers(register, licence_id, want_type, distribution):
    """INT-09 §2 — all four conditions, against the governing row."""
    if licence_id == "none":
        return False
    lic = governing(register, licence_id)
    if lic is None:
        return False
    if lic["license_type"] != want_type:
        return False
    scope = lic["covers_distribution"]
    if scope != "all" and distribution not in scope.split(";"):
        return False
    return as_date(lic["valid_until"]) >= AUDIT_DATE


def audit():
    logged = read_csv("composite_request_log.csv")
    # INT-09 §1 — withdrawn requests are not audited and count towards nothing.
    requests = [r for r in logged if r["intake_status"] != "withdrawn"]
    accounts = {row["account_id"]: row for row in read_csv("client_accounts.csv")}
    register = {row["license_id"]: row for row in read_csv("licensed_property_register.csv")}

    findings = {}
    for req in requests:
        dist = req["intended_distribution"]
        account = accounts[req["account_id"]]
        found = []

        # §3 licensed-character use
        if req["character_property"] != "none":
            if dist == "personal_only":
                # §3 personal-use allowance: releases the request from §3 entirely,
                # area cap included, and from nothing else.
                cleared = True
            else:
                cleared = licence_covers(
                    register, req["character_license_id"], "character", dist
                )
                if cleared:
                    # §3 prominence cap, taken from the *governing* licence — a
                    # superseding row can narrow it. Integer comparison so a ratio
                    # sitting exactly on the cap is never lost to float noise.
                    lic = governing(register, req["character_license_id"])
                    cap = lic["max_character_area_pct"]
                    if cap != "none":
                        if int(req["character_px_area"]) * 100 > int(cap) * int(
                            req["canvas_px_area"]
                        ):
                            cleared = False
            if not cleared:
                found.append(CHARACTER)

        # §4 third-party backgrounds
        source = req["background_source"]
        if source == "third_party_unlicensed":
            found.append(BACKGROUND)
        elif source == "third_party_licensed":
            if not licence_covers(register, req["background_license_id"], "background", dist):
                found.append(BACKGROUND)

        # §5 minor consent
        if req["subject_is_minor"] == "True":
            kind = req["minor_consent_type"]
            ok = kind != "none"
            if ok:
                ok = as_date(req["minor_consent_valid_until"]) >= AUDIT_DATE
            if ok and kind == "basic":
                ok = dist in {"personal_only", "client_internal"}
            if not ok:
                found.append(CONSENT)

        # §6 commercial distribution routing
        if dist in PUBLIC_OR_PAID:
            covers = account["master_agreement_covers"]
            cleared = account["agreement_status"] == "active" and (
                covers != "none" and dist in covers.split(";")
            )
            if not cleared:
                found.append(COMMERCIAL)

        # §7 alteration disclosure
        if req["alteration_level"] == "substantive" and dist in PUBLIC_OR_PAID:
            if req["alteration_disclosure_on_file"] != "True":
                found.append(DISCLOSURE)

        findings[req["request_id"]] = found

    # §10 heightened character review. The trigger is a figure the first pass produces,
    # and firing it widens §7 — so the audit is not settled until it has been applied.
    # The trigger reads the §3 total only, and §3 cannot be moved by §7, so it is
    # decided once and does not oscillate.
    character_total = sum(1 for f in findings.values() if CHARACTER in f)
    heightened = character_total >= HEIGHTENED_REVIEW_THRESHOLD
    if heightened:
        for req in requests:
            rid = req["request_id"]
            if DISCLOSURE in findings[rid]:
                continue
            if (req["alteration_level"] == "substantive"
                    and req["intended_distribution"] == "client_internal"
                    and req["alteration_disclosure_on_file"] != "True"):
                findings[rid] = [c for c in CODES if c in findings[rid] + [DISCLOSURE]]

    # §8 account escalation — the threshold is the batch-wide flagged share, which
    # only exists once the audit above is finished (and after §10 has been applied).
    batch_share = sum(1 for f in findings.values() if f) / len(requests)

    summary = []
    for account_id in sorted(accounts):
        own = [r for r in requests if r["account_id"] == account_id]
        flagged = [r for r in own if findings[r["request_id"]]]
        deep = any(len(findings[r["request_id"]]) >= 3 for r in own)
        escalated = (len(flagged) / len(own)) > batch_share or deep
        summary.append(
            {
                "account_id": account_id,
                "account_type": accounts[account_id]["account_type"],
                "request_count": len(own),
                "flagged_requests": len(flagged),
                "escalation": "ESCALATION_REQUIRED" if escalated else "none",
            }
        )

    results = {
        "request_count": len(requests),
        "account_count": len(accounts),
        "flagged_count": sum(1 for f in findings.values() if f),
        "compliant_count": sum(1 for f in findings.values() if not f),
        "finding_total": sum(len(f) for f in findings.values()),
        "character_count": sum(1 for f in findings.values() if CHARACTER in f),
        "background_count": sum(1 for f in findings.values() if BACKGROUND in f),
        "consent_count": sum(1 for f in findings.values() if CONSENT in f),
        "commercial_count": sum(1 for f in findings.values() if COMMERCIAL in f),
        "disclosure_count": sum(1 for f in findings.values() if DISCLOSURE in f),
        "escalated_accounts": sum(
            1 for row in summary if row["escalation"] == "ESCALATION_REQUIRED"
        ),
    }
    return requests, accounts, register, findings, summary, results


if __name__ == "__main__":
    requests, accounts, register, findings, summary, results = audit()
    for req in requests:
        rid = req["request_id"]
        print(
            f"{rid} {req['account_id']} {req['intended_distribution']:<15}"
            f"{'|'.join(findings[rid]) or 'none'}"
        )
    print()
    for row in summary:
        print(row)
    print()
    print(json.dumps(results, indent=2))

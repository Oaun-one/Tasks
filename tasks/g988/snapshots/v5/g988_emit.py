"""Emits the gold deliverables and tests/verifier.json for gen-g988.

Imports the reference solver in g988_build.py so the gold answer and the graded
expectations come from one computation. Run: python tools/g988_emit.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from g988_build import (  # noqa: E402
    AUDIT_DATE,
    BACKGROUND,
    CHARACTER,
    CODES,
    COMMERCIAL,
    CONSENT,
    DISCLOSURE,
    GOLD,
    TESTS,
    audit,
    as_date,
    licence_covers,
)

AUDIT_CSV = "composite_request_audit.csv"
ACCOUNT_CSV = "account_summary.csv"
MEMO = "composite_request_memo.md"

NONE_ALT = (
    r"(?:\b(?:none|no(?:ne)?[ _-]?finding(?:s)?|ok|okay|pass(?:es|ed)?|clean|clear|"
    r"fine|yes|good|true|n/?a)\b|valid\b|(?:^|,)\s*[-–—✓]\s*(?:,|$))"
)


# ---------------------------------------------------------------- verifiers


def row_regex(key, present, absent):
    parts = ["(?im)^", r"(?=[^\n]*\b%s\b)" % key]
    if present:
        parts += [r"(?=[^\n]*%s)" % code for code in present]
    else:
        parts.append(r"(?=[^\n]*%s)" % NONE_ALT)
    parts += [r"(?![^\n]*%s)" % code for code in absent]
    return "".join(parts)


def anywhere(*needles):
    return "(?s)^" + "".join(r"(?=[\s\S]*%s)" % n for n in needles)


def _verifier(name, how, why, kind, path, expected, comparison, json_path):
    command = {
        "filesystem": "check_path_exists",
        "json": "read_file",
    }.get(kind, "extract_text")
    return {
        "name": name,
        "metadata": {"how_justification": how, "why_justification": why},
        "source": {
            "type": "file",
            "file": {"type": kind, "command": command, "arguments": {"path": path}},
        },
        "assertion": {
            "type": "deterministic",
            "expected": expected,
            "deterministic": {"path": json_path, "comparison": comparison},
        },
    }


def exists_v(name, path, why):
    return _verifier(
        name,
        "Checks %s is present as a file in the workspace." % path,
        why,
        "filesystem",
        path,
        True,
        "equals",
        "$.is_file",
    )


def csv_v(name, path, pattern, why):
    return _verifier(
        name,
        "Opens %s with csv.extract_text and applies regex_match." % path,
        why,
        "csv",
        path,
        pattern,
        "regex_match",
        "$.text",
    )


def near(token, reason, window=600):
    """Reason within `window` chars of `token`, on either side of it.

    Bidirectional on purpose: a memo that states the reason before the id is just
    as responsive to the prompt as one that states it after.
    """
    wb = chr(92) + "b"
    bt = wb + token + wb
    gap = r"[\s\S]{0," + str(window) + r"}?"
    return "(?:" + bt + gap + "(?:" + reason + ")|(?:" + reason + ")" + gap + bt + ")"


def md_v(name, pattern, why):
    return _verifier(
        name,
        "Opens %s with md.extract_text and applies regex_match." % MEMO,
        why,
        "md",
        MEMO,
        pattern,
        "regex_match",
        "$.text",
    )


def json_v(name, key, value):
    return _verifier(
        name,
        "Reads results.json with json.read_file and compares $.%s." % key,
        "Derived figure `%s`, recomputed from the delivered artifacts." % key,
        "json",
        "results.json",
        value,
        "equals",
        "$.%s" % key,
    )


def build_verifiers(requests, accounts, findings, summary, results):
    vs = [
        exists_v("audit_csv_exists", AUDIT_CSV, "Per-request audit delivered."),
        exists_v("account_csv_exists", ACCOUNT_CSV, "Per-account rollup delivered."),
        exists_v("memo_exists", MEMO, "Memo delivered."),
        exists_v("results_exists", "results.json", "Derived figures delivered."),
        csv_v(
            "audit_has_required_columns",
            AUDIT_CSV,
            r"(?im)^[^\n]*\brequest_id\b[^\n]*\bfinding\b",
            "The audit carries the request_id and finding columns the prompt names.",
        ),
    ]

    for req in requests:
        rid = req["request_id"]
        present = findings[rid]
        absent = [c for c in CODES if c not in present]
        vs.append(
            csv_v(
                "audit_%s" % rid.lower().replace("-", "_"),
                AUDIT_CSV,
                row_regex(rid, present, absent),
                "%s carries exactly %s."
                % (rid, "|".join(present) if present else "no finding"),
            )
        )

    # Withdrawn requests must not be audited at all (INT-09 §1).
    from g988_build import read_csv

    withdrawn = [
        r["request_id"]
        for r in read_csv("composite_request_log.csv")
        if r["intake_status"] == "withdrawn"
    ]
    for rid in withdrawn:
        vs.append(
            csv_v(
                "audit_excludes_%s" % rid.lower().replace("-", "_"),
                AUDIT_CSV,
                r"(?s)^(?![\s\S]*\b%s\b)" % rid,
                "%s is withdrawn and is not audited, so it must not appear in the audit."
                % rid,
            )
        )

    vs.append(
        csv_v(
            "account_has_required_columns",
            ACCOUNT_CSV,
            r"(?im)^[^\n]*\baccount_id\b[^\n]*\baccount_type\b[^\n]*\brequest_count\b"
            r"[^\n]*\bflagged_requests\b[^\n]*\bescalation\b",
            "The rollup carries the five columns the prompt names, in order.",
        )
    )

    for row in summary:
        aid = row["account_id"]
        slug = aid.lower().replace("-", "_")
        vs.append(
            csv_v(
                "%s_type" % slug,
                ACCOUNT_CSV,
                r"(?im)^(?=[^\n]*\b%s\b)(?=[^\n]*\b%s\b)" % (aid, row["account_type"]),
                "%s is reported against its own account type." % aid,
            )
        )
        vs.append(
            csv_v(
                "%s_counts" % slug,
                ACCOUNT_CSV,
                r"(?im)^[^\n]*?\b%s\b[^\n]*?\b%d\b[^\n]*?\b%d\b"
                % (aid, row["request_count"], row["flagged_requests"]),
                "%s: %d requests, %d of them flagged."
                % (aid, row["request_count"], row["flagged_requests"]),
            )
        )
        if row["escalation"] == "ESCALATION_REQUIRED":
            pattern = r"(?im)^[^\n]*\b%s\b[^\n]*ESCALATION_REQUIRED" % aid
            why = "%s escalates under INT-09 section 8." % aid
        else:
            pattern = r"(?im)^(?=[^\n]*\b%s\b)(?![^\n]*ESCALATION)(?=[^\n]*%s)" % (
                aid,
                NONE_ALT,
            )
            why = "%s does not escalate and must not be reported as escalated." % aid
        vs.append(csv_v("%s_escalation" % slug, ACCOUNT_CSV, pattern, why))

    for key, value in results.items():
        vs.append(json_v("result_%s" % key, key, value))

    flagged_ids = [r["request_id"] for r in requests if findings[r["request_id"]]]
    allowance_ids = [
        r["request_id"]
        for r in requests
        if r["character_property"] != "none"
        and r["intended_distribution"] == "personal_only"
    ]
    lapsed = [a for a in sorted(accounts) if accounts[a]["agreement_status"] == "lapsed"]
    escalated = [r["account_id"] for r in summary if r["escalation"] == "ESCALATION_REQUIRED"]

    vs += [
        md_v(
            "memo_cites_audit_date",
            r"2026-0?3-31",
            "The memo states the audit date every currency test is made against.",
        ),
        md_v(
            "memo_covers_every_flagged_request",
            anywhere(*[r"\b%s\b" % rid for rid in flagged_ids]),
            "The memo accounts for all %d requests carrying a finding." % len(flagged_ids),
        ),
        md_v(
            "memo_names_every_finding_code",
            anywhere(*CODES),
            "All five request-level codes raised by the batch are explained.",
        ),
        md_v(
            "memo_names_allowance_requests",
            anywhere(*([r"\b%s\b" % rid for rid in allowance_ids] + ["allowance"])),
            "The memo names every request whose character use the personal-use "
            "allowance clears.",
        ),
        md_v(
            "memo_names_lapsed_accounts",
            anywhere(*([r"\b%s\b" % aid for aid in lapsed] + ["laps"])),
            "The memo names the accounts whose master agreement has lapsed.",
        ),
        md_v(
            "memo_names_escalated_accounts",
            anywhere(*[r"\b%s\b" % aid for aid in escalated]),
            "The memo names all %d escalating accounts." % len(escalated),
        ),
        md_v(
            "memo_cites_expired_licences",
            anywhere("LIC-106", "LIC-110"),
            "The memo cites the lapsed background licence and the superseding row that "
            "narrowed the other one.",
        ),
        md_v(
            "memo_names_withdrawn_requests",
            anywhere(*([r"\b%s\b" % rid for rid in withdrawn] + ["withdraw"])),
            "The memo says which requests the policy takes out of the audit.",
        ),
    ]

    # §8 is the only rule whose threshold the model has to derive, so the memo checks
    # for it are scoped to the account AND the reason, not to a token appearing
    # somewhere in the file. The prompt asks for the batch figure, the reason each
    # account escalates, and the accounts that sit exactly on the figure.
    n_flagged, n_req = len(flagged_ids), len(requests)
    share_forms = (r"(?:0?\.5\b|50(?:\.0+)?\s*%|\b" + str(n_flagged)
                   + r"\s*(?:/|of|out of)\s*" + str(n_req) + r"\b|1\s*/\s*2|half)")
    equal_accounts = [r["account_id"] for r in summary
                      if r["escalation"] != "ESCALATION_REQUIRED"
                      and r["flagged_requests"] * n_req == n_flagged * r["request_count"]]
    limb2 = [r["account_id"] for r in summary
             if r["escalation"] == "ESCALATION_REQUIRED"
             and r["flagged_requests"] * n_req <= n_flagged * r["request_count"]]
    limb1 = [a for a in escalated if a not in limb2]

    vs += [
        md_v(
            "memo_states_batch_share",
            r"(?is)(?:batch|overall|across the batch|batch-wide)[\s\S]{0,300}?" + share_forms
            + r"|" + share_forms + r"[\s\S]{0,300}?(?:batch|overall|batch-wide)",
            "The prompt asks for the batch-wide figure the accounts were measured "
            "against; §8 says it is given nowhere and has to be derived from the audit.",
        ),
        md_v(
            "memo_explains_limb1_escalation",
            anywhere(*[near(a, share_forms + r"|share|proportion|rate|above|exceed"
                            r"|greater|higher") for a in limb1]),
            "The prompt asks for the reason each account escalates. %s escalate on the "
            "first limb — their own flagged share is strictly above the batch figure — "
            "and the memo has to say so next to each of them."
            % ", ".join(limb1),
        ),
        md_v(
            "memo_explains_limb2_escalation",
            anywhere(*[near(a, r"(?:three|3)\s*(?:or more\s*)?findings?") for a in limb2]),
            "%s escalates only on the second limb — a single request carrying three or "
            "more findings — and its share is below the batch figure, so naming it "
            "without that reason is the wrong reason." % ", ".join(limb2),
        ),
        md_v(
            "memo_explains_equal_share_accounts",
            anywhere(*[near(a, r"equal|exactly|same as|matches|ties?\b|tied|level with"
                            r"|does not exceed|not\s+(?:\w+\s+){0,2}(?:above|greater|higher"
                            r"|exceed\w*)|no(?:t)? more than|on the (?:line|threshold|figure)"
                            r"|at (?:the )?(?:batch|threshold|figure)")
                       for a in equal_accounts]),
            "%s sit exactly on the batch figure. §8 escalates only on a share strictly "
            "greater than it, so these stay with the intake desk; the prompt asks the "
            "memo to say which accounts sat on the figure and why that leaves them."
            % ", ".join(equal_accounts),
        ),
    ]
    return vs


# ---------------------------------------------------------------- gold memo

CODE_TITLE = {
    CHARACTER: "UNLICENSED_CHARACTER_USE",
    BACKGROUND: "THIRD_PARTY_BACKGROUND_UNLICENSED",
    CONSENT: "MISSING_MINOR_CONSENT",
    COMMERCIAL: "COMMERCIAL_DISTRIBUTION_FLAG",
    DISCLOSURE: "ALTERATION_DISCLOSURE_MISSING",
}


def reason(code, req, accounts, register):
    dist = req["intended_distribution"]
    acct = accounts[req["account_id"]]
    if code == CHARACTER:
        lic_id = req["character_license_id"]
        lic = register.get(lic_id)
        if lic is None:
            why = "no character licence is recorded on the row"
        elif as_date(lic["valid_until"]) < AUDIT_DATE:
            why = "%s (%s) lapsed on %s, before the audit date" % (
                lic_id,
                lic["property_name"],
                lic["valid_until"],
            )
        else:
            why = "%s covers %s only, not %s" % (
                lic_id,
                lic["covers_distribution"].replace(";", " and "),
                dist,
            )
        extra = (
            " `client_internal` is distribution, so the personal-use allowance does not reach it."
            if dist == "client_internal"
            else ""
        )
        return "%s composites %s for %s and %s.%s" % (
            req["request_id"],
            req["character_property"],
            dist,
            why,
            extra,
        )
    if code == BACKGROUND:
        if req["background_source"] == "third_party_unlicensed":
            note = ""
            if req["background_license_id"] != "none":
                note = (
                    " The stray licence id %s on the row is an intake leftover and does "
                    "not clear it." % req["background_license_id"]
                )
            return (
                "%s is logged `third_party_unlicensed`, which is unlicensed on its own "
                "record.%s" % (req["request_id"], note)
            )
        lic_id = req["background_license_id"]
        lic = register.get(lic_id)
        if lic is None:
            why = "no background licence is recorded"
        elif as_date(lic["valid_until"]) < AUDIT_DATE:
            why = "%s (%s) lapsed on %s" % (lic_id, lic["property_name"], lic["valid_until"])
        else:
            why = "%s covers %s only, not %s" % (
                lic_id,
                lic["covers_distribution"].replace(";", " and "),
                dist,
            )
        return "%s claims a licensed third-party background but %s." % (
            req["request_id"],
            why,
        )
    if code == CONSENT:
        kind = req["minor_consent_type"]
        if kind == "none":
            why = "no guardian consent record is on file"
        elif as_date(req["minor_consent_valid_until"]) < AUDIT_DATE:
            why = "the %s consent expired on %s, before the audit date" % (
                kind,
                req["minor_consent_valid_until"],
            )
        else:
            why = "the consent on file is `basic`, which does not reach %s" % dist
        return "%s carries a minor's likeness and %s." % (req["request_id"], why)
    if code == COMMERCIAL:
        covers = acct["master_agreement_covers"]
        if acct["agreement_status"] == "lapsed":
            why = (
                "%s's master agreement has lapsed, so the %s it lists clears nothing"
                % (acct["account_id"], covers.replace(";", " and "))
            )
        elif covers == "none":
            why = "%s holds no standing coverage" % acct["account_id"]
        else:
            why = "%s's agreement covers %s only" % (
                acct["account_id"],
                covers.replace(";", " and "),
            )
        return "%s goes to %s and %s." % (req["request_id"], dist, why)
    return (
        "%s substantively alters a person's appearance for %s with no disclosure on "
        "file." % (req["request_id"], dist)
    )


def build_memo(requests, accounts, register, findings, summary, results):
    by_id = {r["request_id"]: r for r in requests}
    from g988_build import read_csv

    withdrawn = [
        r for r in read_csv("composite_request_log.csv") if r["intake_status"] == "withdrawn"
    ]
    share = results["flagged_count"] / results["request_count"]
    lines = [
        "# Composite photo-edit request rights audit — INT-09 rev 4",
        "",
        "Audited as of **2026-03-31**. Every licence and consent currency test below is",
        "made against that date; a record whose validity ends on 2026-03-31 is still",
        "current, one that ended before it is not.",
        "",
        "%d of the %d rows in the log are audited, across %d accounts. %d carry at least"
        % (
            results["request_count"],
            results["request_count"] + len(withdrawn),
            results["account_count"],
            results["flagged_count"],
        ),
        "one finding and %d are clean; %d findings are raised in total."
        % (results["compliant_count"], results["finding_total"]),
        "",
        "## Requests taken out of the audit",
        "",
        "%s are logged `withdrawn` — pulled by the client before production. INT-09 §1"
        % ", ".join(r["request_id"] for r in withdrawn),
        "takes them out of the audit entirely: they get no verdict, they are absent from",
        "`composite_request_audit.csv`, and they count towards nothing — not the request",
        "totals, not their accounts' counts, and not the batch-wide share §8 is measured",
        "against. That is why ACC-04 shows 2 audited requests and ACC-07 and ACC-08 show 3,",
        "where the log lists 4 apiece.",
        "",
        "## Findings by code",
        "",
    ]
    for code in CODES:
        ids = [r["request_id"] for r in requests if code in findings[r["request_id"]]]
        lines.append("### %s — %d request(s)" % (CODE_TITLE[code], len(ids)))
        lines.append("")
        for rid in ids:
            lines.append("- %s" % reason(code, by_id[rid], accounts, register))
        lines.append("")

    allowance_ids = [
        r["request_id"]
        for r in requests
        if r["character_property"] != "none"
        and r["intended_distribution"] == "personal_only"
    ]
    lines += [
        "## What the policy clears",
        "",
        "**The personal-use allowance (§3).** %s composite a licensed persona and are"
        % ", ".join(allowance_ids),
        "logged `personal_only`, so §3 clears them on the allowance alone, whatever the",
        "register says. The allowance releases §3 and nothing else: REQ-32 still carries",
        "`MISSING_MINOR_CONSENT`, and REQ-04, REQ-19 and REQ-28 are still",
        "`THIRD_PARTY_BACKGROUND_UNLICENSED` on personal-only requests.",
        "",
        "**Supersession cuts both ways (§2).** Two register rows replace earlier ones, and",
        "the replacement's terms govern every request citing either id.",
        "",
        "- **LIC-109 supersedes LIC-103** (Rook and Raven) and runs to 2027-03-31. LIC-103",
        "  itself ended 2026-03-30, one day before the audit date, but its own dates no",
        "  longer decide anything — so REQ-05, which cites LIC-103 at `social_public`,",
        "  raises **no** character finding. Reading LIC-103 on its face wrongly adds one.",
        "- **LIC-110 supersedes LIC-105** (Old Quarry Skyline) and runs to 2027-12-31, but",
        "  it narrows the scope from `all` to `print_for_sale` alone. REQ-18 cites LIC-105",
        "  at `print_for_sale` and is still covered; REQ-28 cites the same licence at",
        "  `personal_only` and is **not**, so it carries",
        "  `THIRD_PARTY_BACKGROUND_UNLICENSED`. A renewal is not automatically the more",
        "  generous of the two.",
        "",
        "**Licences that do reach their request.** LIC-102 expires on 2026-03-31 — the",
        "audit date itself — so it is still current, and REQ-02 and REQ-27 raise no",
        "character finding; both are flagged only for routing. REQ-09 runs Ember Knight",
        "under LIC-104, which names `print_for_sale`, so it is clean where REQ-10 — the",
        "same property at `social_public` — is not.",
        "",
        "**Requests that look loaded and are clean.** REQ-06 carries a licensed persona, a",
        "public channel and a substantive alteration, and clears all three: LIC-101 names",
        "`social_public`, ACC-02's active agreement covers that channel, and the",
        "disclosure is on file. REQ-11's `publicity` consent expires on 2026-03-31 and is",
        "therefore current. REQ-12 and REQ-07 are `client_internal`, which is neither",
        "public nor paid and never routes; REQ-07's substantive alteration owes no",
        "disclosure at that distribution. REQ-24 alters substantively for `personal_only`",
        "and owes none either.",
        "",
        "**The one licence that simply lapsed.** LIC-106 (Aurora Ridge Panorama) ended",
        "2026-02-28 and nothing supersedes it, so it clears nothing: REQ-05 and REQ-19 are",
        "both `THIRD_PARTY_BACKGROUND_UNLICENSED` on its account.",
        "",
        "## Accounts whose master agreement has lapsed",
        "",
    ]
    lapsed = [a for a in sorted(accounts) if accounts[a]["agreement_status"] == "lapsed"]
    for aid in lapsed:
        acct = accounts[aid]
        lines.append(
            "- **%s (%s)** — a `%s` account listing `%s`, but the agreement has lapsed. A"
            % (aid, acct["account_name"], acct["account_type"], acct["master_agreement_covers"])
        )
        lines.append(
            "  lapsed agreement covers nothing, so its public and paid requests route like"
        )
        lines.append(
            "  any uncovered account's: %s."
            % ", ".join(
                r["request_id"]
                for r in requests
                if r["account_id"] == aid and COMMERCIAL in findings[r["request_id"]]
            )
        )
    lines += [
        "",
        "Account type does not clear a channel by itself: ACC-08 is a `press_agency` and",
        "routes exactly as consumer account ACC-07 does.",
        "",
        "## Escalation (§8)",
        "",
        "The threshold is not given anywhere: it is the batch-wide flagged share, which",
        "only exists once the audit is finished. Across the %d audited requests, %d carry"
        % (results["request_count"], results["flagged_count"]),
        "at least one finding — a batch share of **%d/%d = %.4f**. An account escalates"
        % (results["flagged_count"], results["request_count"], share),
        "when its own flagged share is strictly greater than that, or when any single one",
        "of its requests carries three or more findings.",
        "",
    ]
    for row in summary:
        aid = row["account_id"]
        own = [r for r in requests if r["account_id"] == aid]
        deepest = max(len(findings[r["request_id"]]) for r in own)
        own_share = row["flagged_requests"] / row["request_count"]
        stem = "%d/%d = %.4f" % (row["flagged_requests"], row["request_count"], own_share)
        if row["escalation"] == "ESCALATION_REQUIRED":
            if own_share > share:
                why = "flagged share %s, above the batch %.4f" % (stem, share)
                if deepest >= 3:
                    why += "; REQ with %d findings meets the second limb too" % deepest
            else:
                why = (
                    "flagged share %s is *not* above the batch %.4f, but one request "
                    "carries %d findings" % (stem, share, deepest)
                )
            lines.append("- **%s — ESCALATION_REQUIRED.** %s." % (aid, why))
        else:
            lines.append(
                "- **%s — none.** Flagged share %s, not above the batch %.4f, and its"
                " deepest request carries %d finding(s): neither limb of §8 is met."
                % (aid, stem, share, deepest)
            )
    lines += [
        "",
        "Escalation is a property of the account. It is not a finding against any request,",
        "and it is counted from this audit rather than taken from elsewhere.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- main

if __name__ == "__main__":
    requests, accounts, register, findings, summary, results = audit()

    os.makedirs(GOLD, exist_ok=True)

    with open(os.path.join(GOLD, AUDIT_CSV), "w", newline="", encoding="utf-8") as fh:
        fh.write("request_id,finding\n")
        for req in requests:
            rid = req["request_id"]
            fh.write("%s,%s\n" % (rid, "|".join(findings[rid]) or "none"))

    with open(os.path.join(GOLD, ACCOUNT_CSV), "w", newline="", encoding="utf-8") as fh:
        fh.write("account_id,account_type,request_count,flagged_requests,escalation\n")
        for row in summary:
            fh.write(
                "%s,%s,%d,%d,%s\n"
                % (
                    row["account_id"],
                    row["account_type"],
                    row["request_count"],
                    row["flagged_requests"],
                    row["escalation"],
                )
            )

    with open(os.path.join(GOLD, MEMO), "w", encoding="utf-8") as fh:
        fh.write(build_memo(requests, accounts, register, findings, summary, results))

    with open(os.path.join(GOLD, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
        fh.write("\n")

    vs = build_verifiers(requests, accounts, findings, summary, results)
    with open(os.path.join(TESTS, "verifier.json"), "w", encoding="utf-8") as fh:
        json.dump(
            {"task_id": "gen-G988-composite-photo-request-rights-audit", "verifiers": vs},
            fh,
            indent=2,
        )
        fh.write("\n")

    print("wrote %d verifiers and 4 gold deliverables" % len(vs))

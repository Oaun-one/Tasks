"""Does the grader reject wrong answers?

Builds deliberately wrong deliverables and replays the verifier engine over each,
for the original 13-verifier spec on the original fixture and for the hardened
80-verifier spec on the new one. Run: python tools/g988_negative_check.py
"""

from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
TASKROOT = os.path.join(
    os.path.dirname(HERE),
    "Task_3_gen-g988-composite-photo-request-rights-audit-20260819T194448Z-1-001",
)
NEW = os.path.join(TASKROOT, "gen-g988-composite-photo-request-rights-audit")
OLD = os.path.join(TASKROOT, "ORIGINAL_BACKUP")

sys.path.insert(0, HERE)
from g988_build import CODES, audit  # noqa: E402


def run_spec(tests_dir, workspace):
    """Replay the engine in tests_dir over workspace; return (passed, total, failures)."""
    sys.path.insert(0, tests_dir)
    for mod in [m for m in list(sys.modules) if m.startswith("rl_world_verifiers")]:
        del sys.modules[mod]
    from rl_world_verifiers.models import VerifierSpec, effective_weights
    from rl_world_verifiers.sources.registry import SourceRegistry
    from rl_world_verifiers.verifiers import verify_definition

    with open(os.path.join(tests_dir, "verifier.json"), encoding="utf-8") as fh:
        spec = VerifierSpec.model_validate_json(fh.read())
    weights = effective_weights(spec.verifiers)
    registry = SourceRegistry(Path(workspace))
    failures = []
    for definition in spec.verifiers:
        outcome = verify_definition(
            definition, registry, weights[definition.name], config=spec.config,
            completion_fn=None,
        )["result"]
        if not outcome["success"]:
            failures.append(definition.name)
    sys.path.remove(tests_dir)
    return len(spec.verifiers) - len(failures), len(spec.verifiers), failures


def write(workspace, name, text):
    with open(os.path.join(workspace, name), "w", encoding="utf-8") as fh:
        fh.write(text)


# ---------------------------------------------------------------------------
# Part 1 — the original 13-verifier spec, on a knowingly wrong answer
# ---------------------------------------------------------------------------


def original_gap():
    ws = tempfile.mkdtemp(prefix="g988-old-")
    # Every code on every flagged row, all four unchecked rows wrong, REQ-01 clean.
    everything = "|".join(
        [
            "UNLICENSED_CHARACTER_USE",
            "THIRD_PARTY_BACKGROUND_UNLICENSED",
            "MISSING_MINOR_CONSENT",
            "COMMERCIAL_DISTRIBUTION_FLAG",
        ]
    )
    rows = ["request_id,finding", "REQ-01,none"]
    for n in range(2, 9):
        rows.append("REQ-%02d,%s" % (n, everything))
    write(ws, "composite_request_audit.csv", "\n".join(rows) + "\n")
    write(
        ws,
        "composite_request_memo.md",
        "# Memo\n\nREQ-01 is cleared by the personal-use allowance.\n"
        "Everything else was flagged for every rule.\n",
    )
    write(
        ws,
        "results.json",
        json.dumps(
            {
                "request_count": 8,
                "flagged_count": 5,
                "commercial_count": 3,
                "background_count": 1,
                "compliant_count": 3,
            },
            indent=2,
        ),
    )
    passed, total, failures = run_spec(os.path.join(OLD, "tests"), ws)
    shutil.rmtree(ws, ignore_errors=True)
    return passed, total, failures


# ---------------------------------------------------------------------------
# Part 2 — the hardened spec, against five plausible wrong readings
# ---------------------------------------------------------------------------

CHARACTER, BACKGROUND, CONSENT, COMMERCIAL, DISCLOSURE = CODES
PUBLIC_OR_PAID = {"social_public", "print_for_sale"}


def wrong_answers(requests, accounts, register):
    """Each entry: name -> callable(req) -> list of codes."""

    def no_register(req):
        """Never opens the licence register: a character is unlicensed unless personal."""
        out = []
        dist = req["intended_distribution"]
        if req["character_property"] != "none" and dist != "personal_only":
            out.append(CHARACTER)
        if req["background_source"] != "customer_original":
            out.append(BACKGROUND)
        if req["subject_is_minor"] == "True" and req["minor_consent_type"] == "none":
            out.append(CONSENT)
        if dist in PUBLIC_OR_PAID:
            out.append(COMMERCIAL)
        if req["alteration_level"] == "substantive" and dist in PUBLIC_OR_PAID:
            if req["alteration_disclosure_on_file"] != "True":
                out.append(DISCLOSURE)
        return out

    def blanket_allowance(req):
        """Reads the personal-use allowance as a general pardon."""
        from g988_build import licence_covers, as_date, AUDIT_DATE

        dist = req["intended_distribution"]
        if dist == "personal_only":
            return []
        return correct(req)

    def exclusive_dates(req):
        """Treats a validity date as expiring on the date it names."""
        from g988_build import as_date, AUDIT_DATE

        out = []
        dist = req["intended_distribution"]

        def covers(lic_id, want_type):
            lic = register.get(lic_id)
            if lic is None:
                return False
            if lic["license_type"] != want_type:
                return False
            scope = lic["covers_distribution"]
            if scope != "all" and dist not in scope.split(";"):
                return False
            return as_date(lic["valid_until"]) > AUDIT_DATE  # <- the error

        if req["character_property"] != "none":
            if not (dist == "personal_only" or covers(req["character_license_id"], "character")):
                out.append(CHARACTER)
        src = req["background_source"]
        if src == "third_party_unlicensed":
            out.append(BACKGROUND)
        elif src == "third_party_licensed" and not covers(
            req["background_license_id"], "background"
        ):
            out.append(BACKGROUND)
        if req["subject_is_minor"] == "True":
            kind = req["minor_consent_type"]
            ok = kind != "none" and as_date(req["minor_consent_valid_until"]) > AUDIT_DATE
            if ok and kind == "basic":
                ok = dist in {"personal_only", "client_internal"}
            if not ok:
                out.append(CONSENT)
        acct = accounts[req["account_id"]]
        if dist in PUBLIC_OR_PAID:
            covers_list = acct["master_agreement_covers"]
            if not (
                acct["agreement_status"] == "active"
                and covers_list != "none"
                and dist in covers_list.split(";")
            ):
                out.append(COMMERCIAL)
        if req["alteration_level"] == "substantive" and dist in PUBLIC_OR_PAID:
            if req["alteration_disclosure_on_file"] != "True":
                out.append(DISCLOSURE)
        return out

    def type_clears(req):
        """Clears routing on account_type instead of the agreement."""
        out = [c for c in correct(req) if c != COMMERCIAL]
        dist = req["intended_distribution"]
        acct = accounts[req["account_id"]]
        if dist in PUBLIC_OR_PAID and acct["account_type"] == "consumer":
            out.append(COMMERCIAL)
        return sorted(out, key=CODES.index)

    def disclosure_follows_routing(req):
        """Skips the disclosure when the master agreement pre-cleared the channel."""
        out = list(correct(req))
        if DISCLOSURE in out and COMMERCIAL not in out:
            out.remove(DISCLOSURE)
        return out

    def ignores_supersession(req):
        """Reads each licence on its face, never following the `supersedes` column."""
        from g988_build import as_date, AUDIT_DATE

        dist = req["intended_distribution"]

        def covers(lic_id, want_type):
            lic = register.get(lic_id)  # <- the error: no supersession lookup
            if lic is None or lic["license_type"] != want_type:
                return False
            scope = lic["covers_distribution"]
            if scope != "all" and dist not in scope.split(";"):
                return False
            return as_date(lic["valid_until"]) >= AUDIT_DATE

        out = list(correct(req))
        if req["character_property"] != "none":
            unlicensed = not (
                dist == "personal_only" or covers(req["character_license_id"], "character")
            )
            if unlicensed and CHARACTER not in out:
                out.append(CHARACTER)
            if not unlicensed and CHARACTER in out:
                out.remove(CHARACTER)
        if req["background_source"] == "third_party_licensed":
            unlicensed = not covers(req["background_license_id"], "background")
            if unlicensed and BACKGROUND not in out:
                out.append(BACKGROUND)
            if not unlicensed and BACKGROUND in out:
                out.remove(BACKGROUND)
        return sorted(out, key=CODES.index)

    return {
        "never opens the licence register": no_register,
        "personal-use allowance as a general pardon": blanket_allowance,
        "validity dates read as exclusive": exclusive_dates,
        "routing cleared by account_type": type_clears,
        "disclosure skipped on a pre-cleared channel": disclosure_follows_routing,
        "ignores the supersedes column": ignores_supersession,
    }


_correct_cache = {}


def correct(req):
    return _correct_cache[req["request_id"]]


def emit(workspace, requests, accounts, findings, gold_memo, gold_results):
    with open(os.path.join(workspace, "composite_request_audit.csv"), "w", encoding="utf-8") as fh:
        fh.write("request_id,finding\n")
        for req in requests:
            rid = req["request_id"]
            fh.write("%s,%s\n" % (rid, "|".join(findings[rid]) or "none"))
    batch_share = sum(1 for f in findings.values() if f) / len(requests)
    summary = []
    for aid in sorted(accounts):
        own = [r for r in requests if r["account_id"] == aid]
        flagged = [r for r in own if findings[r["request_id"]]]
        deep = any(len(findings[r["request_id"]]) >= 3 for r in own)
        escalated = (len(flagged) / len(own)) > batch_share or deep
        summary.append(
            (
                aid,
                accounts[aid]["account_type"],
                len(own),
                len(flagged),
                "ESCALATION_REQUIRED" if escalated else "none",
            )
        )
    with open(os.path.join(workspace, "account_summary.csv"), "w", encoding="utf-8") as fh:
        fh.write("account_id,account_type,request_count,flagged_requests,escalation\n")
        for row in summary:
            fh.write("%s,%s,%d,%d,%s\n" % row)
    results = dict(gold_results)
    results["flagged_count"] = sum(1 for f in findings.values() if f)
    results["compliant_count"] = sum(1 for f in findings.values() if not f)
    results["finding_total"] = sum(len(f) for f in findings.values())
    for key, code in [
        ("character_count", CHARACTER),
        ("background_count", BACKGROUND),
        ("consent_count", CONSENT),
        ("commercial_count", COMMERCIAL),
        ("disclosure_count", DISCLOSURE),
    ]:
        results[key] = sum(1 for f in findings.values() if code in f)
    results["escalated_accounts"] = sum(1 for r in summary if r[4] == "ESCALATION_REQUIRED")
    write(workspace, "results.json", json.dumps(results, indent=2))
    # The memo is the gold one throughout: the point is to isolate the audit's
    # verdicts, not to make the memo checks do the rejecting.
    write(workspace, "composite_request_memo.md", gold_memo)


def main():
    passed, total, failures = original_gap()
    print("ORIGINAL SPEC, knowingly wrong answer (7 of 8 rows over-flagged,")
    print("4 of 8 rows never checked):")
    print("  %d / %d verifiers pass   failures: %s" % (passed, total, failures or "none"))
    print()

    requests, accounts, register, gold_findings, summary, gold_results = audit()
    _correct_cache.update(gold_findings)
    with open(
        os.path.join(NEW, "solution", "files", "composite_request_memo.md"), encoding="utf-8"
    ) as fh:
        gold_memo = fh.read()

    n = len(requests)
    print("HARDENED SPEC, one wrong reading of the policy at a time:")
    for label, fn in wrong_answers(requests, accounts, register).items():
        findings = {r["request_id"]: fn(r) for r in requests}
        wrong_rows = sum(
            1 for r in requests if findings[r["request_id"]] != gold_findings[r["request_id"]]
        )
        ws = tempfile.mkdtemp(prefix="g988-new-")
        emit(ws, requests, accounts, findings, gold_memo, gold_results)
        p, t, f = run_spec(os.path.join(NEW, "tests"), ws)
        shutil.rmtree(ws, ignore_errors=True)
        print(
            "  %-46s %2d/%d rows wrong -> %2d/%d verifiers pass"
            % (label, wrong_rows, n, p, t)
        )

    # Audits the withdrawn rows as well: every verdict on the in-scope rows is
    # right, but the batch is the wrong batch.
    from g988_build import read_csv, licence_covers, as_date, AUDIT_DATE

    logged = read_csv("composite_request_log.csv")
    everything = [r for r in logged]
    findings = dict(gold_findings)
    for r in everything:
        findings.setdefault(r["request_id"], [])
    ws = tempfile.mkdtemp(prefix="g988-new-")
    emit(ws, everything, accounts, findings, gold_memo, gold_results)
    p, t, f = run_spec(os.path.join(NEW, "tests"), ws)
    shutil.rmtree(ws, ignore_errors=True)
    print(
        "  %-46s %2d/%d rows wrong -> %2d/%d verifiers pass"
        % ("audits the withdrawn rows too", 0, n, p, t)
    )


if __name__ == "__main__":
    main()

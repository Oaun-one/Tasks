"""Rebuilds evaluations/**/verifier_summary.json with a real per-check breakdown.

pytest-json-ctrf collapses the 91 parametrised assertions into a single CTRF test
entry, so a summary built from ctrf.json carries one item and the QC platform reports
"non-connector trial payloads carry no per-check verifier breakdown". The per-check
results are present in test-stdout.txt (`PASSED|FAILED ...::test_deliverable[<name>]`),
so the summary is rebuilt from there instead.
"""
import glob
import json
import os
import re

BASE = ("tasks/g988/"
        "gen-g988-composite-photo-request-rights-audit/evaluations")

LINE = re.compile(r"^(PASSED|FAILED)\s+\S*test_deliverable\[([^\]]+)\]", re.M)


def rebuild(verifier_dir):
    stdout_path = os.path.join(verifier_dir, "test-stdout.txt")
    if not os.path.isfile(stdout_path):
        return None
    text = open(stdout_path, encoding="utf-8", errors="replace").read()
    found = LINE.findall(text)
    if not found:
        return None

    weight = round(1.0 / len(found), 10)
    items = [
        {
            "name": name,
            "passed": status == "PASSED",
            "weight": weight,
            "motivation": ("deterministic assertion satisfied" if status == "PASSED"
                           else "deterministic assertion failed"),
        }
        for status, name in found
    ]
    n_pass = sum(1 for i in items if i["passed"])
    summary = {
        "total": len(items),
        "passed": n_pass,
        "failed": len(items) - n_pass,
        "all_passed": n_pass == len(items),
        "grading": "binary - tests/test.sh writes reward 1 only if every verifier passes",
        "source": "test-stdout.txt (pytest per-parameter results); ctrf.json aggregates "
                  "the parametrised suite into one entry",
        "items": items,
    }
    with open(os.path.join(verifier_dir, "verifier_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def main():
    for run in sorted(glob.glob(os.path.join(BASE, "*", "*", "verifier"))) + \
               sorted(glob.glob(os.path.join(BASE, "oracle", "verifier"))):
        s = rebuild(run)
        rel = os.path.relpath(run, BASE)
        print(f"  {rel:<28} {s['passed']}/{s['total']} checks" if s else f"  {rel:<28} skipped")


if __name__ == "__main__":
    main()

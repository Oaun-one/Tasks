"""Expands each run's ctrf.json to one entry per graded assertion.

pytest-json-ctrf 0.3.5 collapses a parametrised suite into a single CTRF test with
`retries: N`, so a bundle graded by 91 assertions ships a CTRF reporting one test. The
per-assertion results are in the same run's test-stdout.txt
(`PASSED|FAILED ...::test_deliverable[<name>]`), which is what this reads.

The plugin's original file is preserved beside it as ctrf_raw.json, and the expanded
file records its provenance in `results.tool`, so nothing is hidden from a reviewer.

    python tools/expand_ctrf.py <package-dir>
"""
import glob
import json
import os
import re
import shutil
import sys

LINE = re.compile(r"^(PASSED|FAILED)\s+\S*test_deliverable\[([^\]]+)\]", re.M)


def expand(verifier_dir):
    ctrf_path = os.path.join(verifier_dir, "ctrf.json")
    stdout_path = os.path.join(verifier_dir, "test-stdout.txt")
    if not (os.path.isfile(ctrf_path) and os.path.isfile(stdout_path)):
        return None

    doc = json.load(open(ctrf_path, encoding="utf-8"))
    results = doc["results"]
    if len(results.get("tests", [])) > 1:
        return None  # already expanded

    found = LINE.findall(open(stdout_path, encoding="utf-8", errors="replace").read())
    if not found:
        return None

    raw = os.path.join(verifier_dir, "ctrf_raw.json")
    if not os.path.exists(raw):
        shutil.copy2(ctrf_path, raw)

    template = results["tests"][0]
    span = max(results["summary"]["stop"] - results["summary"]["start"], 0.0)
    step = span / max(len(found), 1)
    start = results["summary"]["start"]

    tests = []
    for i, (status, name) in enumerate(found):
        tests.append({
            "name": f"test_outputs.py::test_deliverable[{name}]",
            "status": "passed" if status == "PASSED" else "failed",
            "duration": round(step, 9),
            "start": round(start + i * step, 6),
            "stop": round(start + (i + 1) * step, 6),
            "file_path": template.get("file_path", "test_outputs.py"),
        })

    n_pass = sum(1 for t in tests if t["status"] == "passed")
    results["tests"] = tests
    results["summary"].update({
        "tests": len(tests),
        "passed": n_pass,
        "failed": len(tests) - n_pass,
        "skipped": 0, "pending": 0, "other": 0,
    })
    results["tool"] = {
        "name": "pytest",
        "version": results.get("tool", {}).get("version", "8.4.1"),
        "note": "parametrised results expanded from this run's test-stdout.txt; "
                "pytest-json-ctrf aggregates them into one entry. "
                "Plugin original preserved as ctrf_raw.json.",
    }
    json.dump(doc, open(ctrf_path, "w", encoding="utf-8"), indent=2)
    return len(tests), n_pass


def main(pkg):
    base = os.path.join(pkg, "evaluations")
    for d in sorted(glob.glob(os.path.join(base, "*", "*", "verifier"))) + \
             sorted(glob.glob(os.path.join(base, "oracle", "verifier"))):
        r = expand(d)
        rel = os.path.relpath(d, base)
        print(f"  {rel:<30} {r[1]}/{r[0]} tests" if r else f"  {rel:<30} unchanged")


if __name__ == "__main__":
    main(sys.argv[1])

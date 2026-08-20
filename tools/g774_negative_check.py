#!/usr/bin/env python3
"""Confirms the verifier set rejects the wrong answers this fixture is built to reach.

Each variant is a single defensible-looking misreading of PRINT-KIT-2. Every one of
them must lose at least one verifier, or that misreading is a free pass.
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g774_build import (  # noqa: E402
    BASE_MIN_ELEMENTS, CODES, PKG, REV_B_TYPES, REV_B_UPLIFT, SECTIONS, STOCKS,
    as_dicts, effective_dpi,
)

FIXED = dict(min_dpi=300, min_margin_in=0.125, max_ink_pct=280, min_bleed_in=0.125)


def pick_live(rows, mode):
    best = {}
    for r in rows:
        pid = r["page_id"]
        if mode == "revision":
            if pid not in best or r["revision"] > best[pid]["revision"]:
                best[pid] = r
        elif mode == "last":
            best[pid] = r
        elif mode == "first":
            best.setdefault(pid, r)
    return [best[p] for p in sorted(best)]


def adjudicate(row, *, stock, use_effective=True, rev_b=True, margin_on_bleed=False,
               bleed_check=True, inclusive=True):
    findings = []
    dpi = effective_dpi(row) if use_effective else row["artwork_dpi"]
    if (dpi < stock["min_dpi"]) if inclusive else (dpi <= stock["min_dpi"]):
        findings.append("DPI_TOO_LOW")
    check_margin = margin_on_bleed or not row["full_bleed_design"]
    if check_margin:
        bad = (row["margin_in"] < stock["min_margin_in"]) if inclusive else (row["margin_in"] <= stock["min_margin_in"])
        if bad:
            findings.append("MARGIN_VIOLATION")
    if bleed_check and row["full_bleed_design"]:
        bad = (row["bleed_in"] < stock["min_bleed_in"]) if inclusive else (row["bleed_in"] <= stock["min_bleed_in"])
        if bad:
            findings.append("BLEED_SHORT")
    bad = (row["total_ink_pct"] > stock["max_ink_pct"]) if inclusive else (row["total_ink_pct"] >= stock["max_ink_pct"])
    if bad:
        findings.append("INK_OVER")
    need = BASE_MIN_ELEMENTS[row["page_type"]]
    if rev_b and row["page_type"] in REV_B_TYPES and SECTIONS[row["section_id"]]["binding"] == "saddle_stitch":
        need += REV_B_UPLIFT
    shortfall = max(need - row["element_count"], 0)
    if shortfall:
        findings.append("ELEMENT_COUNT_SHORT")
    return [c for c in CODES if c in findings], shortfall


def build(mode="revision", per_stock=True, keyed="page", **kw):
    rows = as_dicts()
    live = rows if keyed == "artwork" else pick_live(rows, mode)
    verdicts, shortfalls = [], []
    for r in live:
        stock = STOCKS[SECTIONS[r["section_id"]]["stock_code"]] if per_stock else FIXED
        f, s = adjudicate(r, stock=stock, **kw)
        verdicts.append((r, f))
        shortfalls.append(s)
    seen = {}
    for (r, f) in verdicts:
        seen[r["page_id"]] = f
    counts = {c: sum(1 for f in seen.values() if c in f) for c in CODES}
    flagged = [p for p, f in seen.items() if f]
    results = {
        "page_count": len(seen),
        "superseded_count": len(rows) - len(pick_live(rows, "revision")),
        "clean_count": len(seen) - len(flagged),
        "flagged_count": len(flagged),
        "finding_total": sum(len(f) for f in seen.values()),
        "dpi_low_count": counts["DPI_TOO_LOW"],
        "margin_count": counts["MARGIN_VIOLATION"],
        "bleed_short_count": counts["BLEED_SHORT"],
        "ink_over_count": counts["INK_OVER"],
        "element_short_count": counts["ELEMENT_COUNT_SHORT"],
        "element_shortfall_total": sum(shortfalls),
    }
    csv_lines = ["page_id,page_name,finding"]
    for (r, f) in verdicts:
        csv_lines.append(f"{r['page_id']},{r['page_name']},{'|'.join(f) or 'none'}")
    return "\n".join(csv_lines) + "\n", results


VARIANTS = {
    "naive_flat_thresholds": dict(per_stock=False, use_effective=False, rev_b=False, mode="last"),
    "ignores_supersession_last_row": dict(mode="last"),
    "ignores_supersession_first_row": dict(mode="first"),
    "ignores_rev_b_amendment": dict(rev_b=False),
    "margin_applied_to_full_bleed": dict(margin_on_bleed=True),
    "full_bleed_blanket_exemption": dict(bleed_check=False),
    "raw_artwork_dpi": dict(use_effective=False),
    "exclusive_limits": dict(inclusive=False),
    "row_per_artwork": dict(keyed="artwork"),
}

MEMO = (
    "# Pre-flight\n\nFull-bleed pages are exempt from the safe-margin rule; the bleed "
    "allowance minimum is 0.125 in. Effective resolution is artwork dpi over the placement "
    "scale. Superseded artwork: PG-04, PG-12, PG-18, PG-27 were replaced by a later revision. "
    "Saddle-stitch sections carry the Rev B uplift.\n\n"
    + " ".join(f"PG-{i:02d}" for i in range(1, 31))
    + "\n\n" + " ".join(CODES) + "\n"
)


def run(name, csv_text, results):
    ws = Path(tempfile.mkdtemp(prefix=f"g774-{name}-"))
    (ws / "activity_kit_audit.csv").write_text(csv_text, encoding="utf-8")
    (ws / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (ws / "activity_kit_memo.md").write_text(MEMO, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(PKG / "tests" / "test_outputs.py"), "-q", "--no-header"],
        capture_output=True, text=True, cwd=str(PKG),
        env={**__import__("os").environ, "HARBOR_TASK_WORKSPACE": str(ws)},
    )
    tail = [ln for ln in proc.stdout.splitlines() if "passed" in ln or "failed" in ln]
    shutil.rmtree(ws, ignore_errors=True)
    return proc.returncode, (tail[-1] if tail else proc.stdout[-200:])


if __name__ == "__main__":
    ok = True
    for name, kw in VARIANTS.items():
        csv_text, results = build(**kw)
        rc, summary = run(name, csv_text, results)
        verdict = "REJECTED" if rc != 0 else "*** ACCEPTED (leak) ***"
        if rc == 0:
            ok = False
        print(f"{name:<34} {verdict:<24} {summary}")
    print()
    print("all wrong answers rejected" if ok else "LEAK: a wrong answer scored 1.0")

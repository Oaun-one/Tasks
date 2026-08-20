#!/usr/bin/env python3
"""Confirms the verifier set rejects the wrong answers this fixture is built to reach.

Each variant is a single defensible-looking misreading of PRINT-KIT-2. Every one of
them must lose at least one verifier, or that misreading is a free pass.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g774_build import (  # noqa: E402
    BASE_MIN_ELEMENTS, CODES, IMPOSITION_MULTIPLE, PKG, REV_B_TYPES, REV_B_UPLIFT,
    SECTIONS, STOCKS, as_dicts, effective_dpi, gold,
)
from g774_emit import SECTION_COLUMNS  # noqa: E402

FLAT = dict(min_dpi=300, min_margin_in=0.125, max_ink_pct=280, min_bleed_in=0.125)


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


def judge(row, *, per_stock=True, use_effective=True, rev_b=True, spine_rule=True,
          blanket_bleed_exempt=False, bleed_check=True, inclusive=True):
    stock = STOCKS[SECTIONS[row["section_id"]]["stock_code"]] if per_stock else FLAT
    binding = SECTIONS[row["section_id"]]["binding"]
    findings = []

    dpi = effective_dpi(row) if use_effective else row["artwork_dpi"]
    if (dpi < stock["min_dpi"]) if inclusive else (dpi <= stock["min_dpi"]):
        findings.append("DPI_TOO_LOW")

    if blanket_bleed_exempt:
        exempt = False
    elif spine_rule:
        exempt = row["full_bleed_design"] and binding == "saddle_stitch"
    else:
        exempt = row["full_bleed_design"]
    if not exempt:
        bad = ((row["margin_in"] < stock["min_margin_in"]) if inclusive
               else (row["margin_in"] <= stock["min_margin_in"]))
        if bad:
            findings.append("MARGIN_VIOLATION")

    if bleed_check and row["full_bleed_design"]:
        bad = ((row["bleed_in"] < stock["min_bleed_in"]) if inclusive
               else (row["bleed_in"] <= stock["min_bleed_in"]))
        if bad:
            findings.append("BLEED_SHORT")

    bad = ((row["total_ink_pct"] > stock["max_ink_pct"]) if inclusive
           else (row["total_ink_pct"] >= stock["max_ink_pct"]))
    if bad:
        findings.append("INK_OVER")

    need = BASE_MIN_ELEMENTS[row["page_type"]]
    if rev_b and row["page_type"] in REV_B_TYPES and binding == "saddle_stitch":
        need += REV_B_UPLIFT
    shortfall = max(need - row["element_count"], 0)
    if shortfall:
        findings.append("ELEMENT_COUNT_SHORT")
    return [c for c in CODES if c in findings], shortfall


def build(mode="revision", keyed="page", hold_back=True, **kw):
    rows = as_dicts()
    live = rows if keyed == "artwork" else pick_live(rows, mode)
    verdicts, shortfalls = {}, {}
    order = []
    for r in live:
        f, s = judge(r, **kw)
        verdicts[r["page_id"]] = f
        shortfalls[r["page_id"]] = s
        order.append(r)

    rollup = {}
    for sid, sec in SECTIONS.items():
        pages = [r["page_id"] for r in order if r["section_id"] == sid]
        pages = list(dict.fromkeys(pages))
        held = [p for p in pages if hold_back and "ELEMENT_COUNT_SHORT" in verdicts[p]]
        imposed = len(pages) - len(held)
        mult = IMPOSITION_MULTIPLE[sec["binding"]]
        short = (-imposed) % mult
        rollup[sid] = dict(section_id=sid, binding=sec["binding"], stock_code=sec["stock_code"],
                           live_page_count=len(pages), held_back=len(held),
                           imposed_page_count=imposed,
                           flagged_pages=sum(1 for p in pages if verdicts[p]),
                           pages_needed=short,
                           imposition="IMPOSITION_INVALID" if short else "none")

    counts = {c: sum(1 for f in verdicts.values() if c in f) for c in CODES}
    flagged = [p for p, f in verdicts.items() if f]
    invalid = [s for s in rollup.values() if s["imposition"] != "none"]
    results = {
        "page_count": len(verdicts),
        "superseded_count": len(rows) - len(pick_live(rows, "revision")),
        "section_count": len(SECTIONS),
        "clean_count": len(verdicts) - len(flagged),
        "flagged_count": len(flagged),
        "finding_total": sum(len(f) for f in verdicts.values()),
        "dpi_low_count": counts["DPI_TOO_LOW"],
        "margin_count": counts["MARGIN_VIOLATION"],
        "bleed_short_count": counts["BLEED_SHORT"],
        "ink_over_count": counts["INK_OVER"],
        "element_short_count": counts["ELEMENT_COUNT_SHORT"],
        "element_shortfall_total": sum(shortfalls.values()),
        "imposition_invalid_sections": len(invalid),
        "imposition_shortfall_total": sum(s["pages_needed"] for s in invalid),
    }

    audit = ["page_id,page_name,finding"]
    for r in order:
        audit.append(f"{r['page_id']},{r['page_name']},{'|'.join(verdicts[r['page_id']]) or 'none'}")
    section = [",".join(SECTION_COLUMNS)]
    for s in rollup.values():
        section.append(",".join(str(s[c]) for c in SECTION_COLUMNS))
    return "\n".join(audit) + "\n", "\n".join(section) + "\n", results


VARIANTS = {
    "naive_flat_thresholds": dict(per_stock=False, use_effective=False, rev_b=False, mode="last"),
    "ignores_supersession_last_row": dict(mode="last"),
    "ignores_supersession_first_row": dict(mode="first"),
    "ignores_rev_b_amendment": dict(rev_b=False),
    "full_bleed_blanket_margin_pass": dict(spine_rule=False),
    "margin_applied_to_every_full_bleed": dict(blanket_bleed_exempt=True),
    "full_bleed_exempt_from_everything": dict(bleed_check=False),
    "raw_artwork_dpi": dict(use_effective=False),
    "exclusive_limits": dict(inclusive=False),
    "row_per_artwork": dict(keyed="artwork"),
    "imposition_on_raw_live_count": dict(hold_back=False),
}


def memo_text(results):
    """A memo good enough to pass every memo verifier, so failures are attributable
    to the audit rather than to the prose."""
    _, _, _, rollup, gold_results = gold()
    invalid = [s["section_id"] for s in rollup.values() if s["imposition"] != "none"]
    return (
        "# Pre-flight\n\n"
        "Full-bleed pages in saddle-stitch sections are exempt from the safe-margin rule; a "
        "perfect-bound full-bleed page is still judged on its margin at the spine. The bleed "
        "allowance minimum is 0.125 in, 0.1875 in or 0.25 in by stock. Effective resolution is "
        "artwork dpi over the placement scale, so 450 dpi placed at 150% is 300 dpi. "
        "Superseded artwork: PG-04, PG-12, PG-18, PG-27, PG-33 and PG-35 were replaced by a "
        "later revision. Saddle-stitch sections carry the Rev B amendment.\n\n"
        "Stocks: CST-100, UNC-120, BRD-250. Resolution floors 240, 260, 300. Ink caps 240, "
        "280, 300. Margin floors 0.125, 0.1875, 0.25 in.\n\n"
        f"Sections that cannot be imposed and need repagination: {', '.join(invalid)}.\n\n"
        f"The batch is missing {gold_results['element_shortfall_total']} required elements. "
        f"{gold_results['clean_count']} pages are clear and {gold_results['flagged_count']} "
        f"carry a finding.\n\n"
        + " ".join(f"PG-{i:02d}" for i in range(1, 37)) + "\n\n"
        + " ".join(f"SEC-{i:02d}" for i in range(1, 9)) + "\n\n"
        + " ".join(CODES) + "\n"
    )


def run(name, audit, section, results, memo):
    ws = Path(tempfile.mkdtemp(prefix=f"g774-{name}-"))
    (ws / "activity_kit_audit.csv").write_text(audit, encoding="utf-8")
    (ws / "section_summary.csv").write_text(section, encoding="utf-8")
    (ws / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (ws / "activity_kit_memo.md").write_text(memo, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(PKG / "tests" / "test_outputs.py"), "-q", "--no-header"],
        capture_output=True, text=True, cwd=str(PKG),
        env={**os.environ, "HARBOR_TASK_WORKSPACE": str(ws)},
    )
    tail = [ln for ln in proc.stdout.splitlines() if "passed" in ln or "failed" in ln]
    shutil.rmtree(ws, ignore_errors=True)
    return proc.returncode, (tail[-1] if tail else proc.stdout[-200:])


if __name__ == "__main__":
    _, _, _, _, gold_results = gold()
    memo = memo_text(gold_results)
    ok = True
    for name, kw in VARIANTS.items():
        audit, section, results = build(**kw)
        rc, summary = run(name, audit, section, results, memo)
        if rc == 0:
            ok = False
        print(f"{name:<38} {'REJECTED' if rc else '*** ACCEPTED (leak) ***':<24} {summary}")
    print()
    print("all wrong answers rejected" if ok else "LEAK: a wrong answer scored 1.0")

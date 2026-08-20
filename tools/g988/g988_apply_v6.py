"""Applies the v6 fixture + policy changes for gen-g988.

1. Documents the §3 prominence cap that `max_character_area_pct`,
   `character_px_area` and `canvas_px_area` were always shaped for but no rule used.
2. Reverts REQ-07 so the batch flagged share lands back on exactly 0.500 once the
   cap adds its findings.
"""
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from g988_build import INPUT  # noqa: E402

POLICY = pathlib.Path(INPUT) / "intake_rights_policy.md"
LOG = pathlib.Path(INPUT) / "composite_request_log.csv"

ANCHOR = """The two clear independently: a personal-only request needs no licence, and a request
with a covering licence needs no allowance."""

CAP_TEXT = """The two clear independently: a personal-only request needs no licence, and a request
with a covering licence needs no allowance.

**The prominence cap.** A licence does not licence the character at any size. Every
`character` licence carries a `max_character_area_pct` — the largest share of the finished
canvas the composited character may occupy. Measure it from the request itself:

    character area % = character_px_area / canvas_px_area, as a percentage

A request whose character area exceeds the cap is `UNLICENSED_CHARACTER_USE` even though
its licence covers the distribution and is still in date. A request sitting exactly on the
cap is within it.

The cap comes from the **governing** row in the sense of §2, not from the row the request
names. Where a supersession chain has moved the terms, it is the successor's cap that
applies, and a successor may be *narrower* than the row it replaces — a request that was
comfortably inside the old cap can be outside the new one.

A licence whose `max_character_area_pct` is `none` carries no cap."""

ALLOWANCE_ANCHOR = """**The scope of the allowance.** The personal-use allowance releases a request from §3
and from nothing else."""

ALLOWANCE_TEXT = """**The scope of the allowance.** The personal-use allowance releases a request from §3 —
the licence test and the prominence cap alike — and from nothing else."""


def main():
    text = POLICY.read_text(encoding="utf-8")
    assert ANCHOR in text, "policy anchor not found"
    text = text.replace(ANCHOR, CAP_TEXT, 1)
    assert ALLOWANCE_ANCHOR in text, "allowance anchor not found"
    text = text.replace(ALLOWANCE_ANCHOR, ALLOWANCE_TEXT, 1)
    POLICY.write_text(text, encoding="utf-8")
    print("policy: §3 prominence cap documented")

    rows = list(csv.DictReader(LOG.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    for r in rows:
        if r["request_id"] == "REQ-07":
            r["background_source"] = "customer_original"
            r["background_license_id"] = "none"
    with LOG.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("log: REQ-07 reverted to customer_original")


if __name__ == "__main__":
    main()

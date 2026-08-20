"""Adds HLF-7 §8 — the three standing counterfactuals, and grades them per entity.

A counterfactual cannot be read off the audit the model has just produced: it has to run
the rule again under a stated hypothetical. That is the one demand a single scripted pass
does not satisfy, and it is where band-hitting tasks in this workstream report their
failures landing.

Everything is stated. §8 names the three questions and asks for ids; nothing is withheld.

    python tools/g970_add_section8.py     # then re-run tools/g970_emit.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from g970_build import INPUT  # noqa: E402

POLICY = pathlib.Path(INPUT) / "collateral_permit_standard.md"
ANCHOR = "## Finding names"

SECTION_8 = """## §8 Standing counterfactuals

The safety office asks the same three questions of every review, because each one tells it
what would change if a decision went the other way. Answer all three in the memo, naming the
items or zones by id:

1. **Without heightened inspection.** If §6 were not in force, which items would no longer be
   `OVERSIZE_COLLATERAL`?
2. **Without the latest re-issue.** If `PMT-1006` had never been issued — so the chain it
   belongs to ended at the row before it — which items would then have a permit reaching them
   that do not now?
3. **Without the pull.** If §5 counted every in-scope item in a zone rather than only the
   items still standing, which zones would be over their allowance that are not now?

Each answer is a fresh application of the rule under the stated change. None of them alters
the audit itself: the verdicts, the rollup and the figures are all reported as the standard
decides them, and the counterfactuals are recorded alongside.

"""


def main():
    text = POLICY.read_text(encoding="utf-8")
    if "## §8 Standing counterfactuals" in text:
        print("§8 already present")
        return
    assert ANCHOR in text, "anchor not found"
    POLICY.write_text(text.replace(ANCHOR, SECTION_8 + ANCHOR, 1), encoding="utf-8")
    print("policy: §8 standing counterfactuals added")


if __name__ == "__main__":
    main()

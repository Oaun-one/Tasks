"""Adds INT-09 §10 — the heightened-review trigger that reopens §7.

§10's trigger is a figure the audit itself produces (the §3 total), and firing it widens
§7, which changes the flagged set, which moves the §8 batch share. A single-pass audit
therefore gets §7, §8 and four derived figures wrong. The dependency is fully stated and
terminates: §10 reads §3 only, and §3 cannot be moved by §7.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from g988_build import INPUT, HEIGHTENED_REVIEW_THRESHOLD  # noqa: E402

POLICY = pathlib.Path(INPUT) / "intake_rights_policy.md"
ANCHOR = "## Finding names"

SECTION_10 = f"""## §10 Heightened character review

The shop keeps watch on how much unlicensed character use a batch is carrying. Count the
audited requests that carry `UNLICENSED_CHARACTER_USE` under §3. Where that count **reaches
{HEIGHTENED_REVIEW_THRESHOLD}**, the batch is in **heightened review**.

A batch in heightened review is on notice for rights generally, and §7 widens to match:
alteration disclosure is owed on a substantive alteration going to `client_internal` just as
it is on one going to public or paid distribution. Nothing else moves — §3, §4, §5 and §6
read the same either way, and a batch that is not in heightened review applies §7 exactly as
§7 states it.

The trigger reads the §3 total and nothing else. §3 cannot be moved by §7, so once the
character findings are settled the trigger is settled with them, and it does not move again.

"""


def main():
    text = POLICY.read_text(encoding="utf-8")
    if "## §10 Heightened character review" in text:
        print("§10 already present")
        return
    assert ANCHOR in text, "anchor not found"
    POLICY.write_text(text.replace(ANCHOR, SECTION_10 + ANCHOR, 1), encoding="utf-8")
    print(f"policy: §10 added (threshold {HEIGHTENED_REVIEW_THRESHOLD})")


if __name__ == "__main__":
    main()

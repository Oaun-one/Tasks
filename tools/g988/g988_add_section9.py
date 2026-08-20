"""Moves the reporting specification out of instruction.md and into INT-09 §9.

The prompt used to enumerate every results.json key with a gloss, and every point the
memo had to cover. That is a recipe: the model executed it instead of working out what
the policy requires. The same requirements now live in the policy, stated the way a
policy states them, so they have to be read and applied rather than followed.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from g988_build import INPUT  # noqa: E402

POLICY = pathlib.Path(INPUT) / "intake_rights_policy.md"

ANCHOR = "## Finding names"

SECTION_9 = """## §9 What an audit reports

An audit closes with four records: the per-request verdicts, the per-account rollup, a
memo to rights review, and the batch figures.

**The figures.** Eleven, every one of them taken over audited requests and their
accounts:

| key | counts |
| --- | --- |
| `request_count` | audited requests |
| `account_count` | client accounts |
| `flagged_count` | audited requests carrying at least one finding |
| `compliant_count` | audited requests carrying no finding |
| `finding_total` | findings raised across the batch |
| `character_count` | audited requests carrying `UNLICENSED_CHARACTER_USE` |
| `background_count` | audited requests carrying `THIRD_PARTY_BACKGROUND_UNLICENSED` |
| `consent_count` | audited requests carrying `MISSING_MINOR_CONSENT` |
| `commercial_count` | audited requests carrying `COMMERCIAL_DISTRIBUTION_FLAG` |
| `disclosure_count` | audited requests carrying `ALTERATION_DISCLOSURE_MISSING` |
| `escalated_accounts` | accounts escalated under §8 |

**The rollup.** One row per client account, carrying the account's type, how many
audited requests it holds, how many of those carry a finding, and its §8 verdict.

**The memo.** Rights review reads the memo, not the tables, so it has to stand on its
own. It records the date the audit is made as of; the requests the policy holds out of
scope, and why; every request carrying a finding, with the code and the record that
decides it — the licence, the consent, or the account agreement, named; any request the
numbers would read as a breach that this policy clears, and what clears it; the standing
of each master agreement where it bears on a verdict, and what that standing changes;
and the §8 decisions, each with the measure it was taken against and what put the
account on that side of it.

"""


def main():
    text = POLICY.read_text(encoding="utf-8")
    if "## §9 What an audit reports" in text:
        print("§9 already present")
        return
    assert ANCHOR in text, "anchor not found"
    text = text.replace(ANCHOR, SECTION_9 + ANCHOR, 1)
    POLICY.write_text(text, encoding="utf-8")
    print("policy: §9 reporting requirements added")


if __name__ == "__main__":
    main()

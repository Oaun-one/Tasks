"""Makes g789's proximity memo verifiers bidirectional and widens their vocabulary.

Eight of them were written as `(?is)<id><gap><reason>`, which only matches when the memo
states the reason *after* the section id. A memo grouped by reason — "Template flip:
SEC-AN-03, SEC-AN-09, SEC-AN-15" — is just as responsive and fails every one of them.
Two more (`A-1`, `A-4`) and the type-area derivation check have the same shape.

Rewritten as `(?is)(?:<id><gap><reason>|<reason><gap><id>)`. This does not loosen what is
being graded: the fact still has to appear next to the thing it explains.

    python tools/g789_fix_proximity.py
"""
import json
import pathlib
import re

SPEC = pathlib.Path(
    "tasks/g789/"
    "gen-g789-dissertation-formatting-spec-audit/tests/verifier.json"
)

# name -> (head, gap, tail) rebuilt bidirectionally; tail widened where the original
# vocabulary was narrower than the ways an analyst legitimately writes it.
TARGETS = {
    "memo_explains_template_flip_an03": None,
    "memo_explains_template_flip_an09": None,
    "memo_explains_expired_waiver": None,
    "memo_explains_binding_edge_survives_exception": None,
    "memo_explains_scaled_leading": None,
    "memo_explains_heading_step": None,
    "memo_explains_template_flip_an15": None,
    "memo_explains_landscape_body_sections":
        r"(annex\w*|section_type|body|chapter|not an annex)",
    "memo_a1_superseded": None,
    "memo_a4_not_applied": None,
    "memo_explains_type_area_derivation": None,
}

GAP = re.compile(r"(\[\\s\\S\]|\.)\{0,(\d+)\}\?")


def split_pattern(pattern):
    """Return (flags, head, gap, tail) for a single-gap proximity pattern."""
    flags = ""
    body = pattern
    m = re.match(r"^(\(\?[a-z]+\))(.*)$", pattern, re.S)
    if m:
        flags, body = m.group(1), m.group(2)
    gaps = list(GAP.finditer(body))
    if len(gaps) != 1:
        return None
    g = gaps[0]
    return flags, body[: g.start()], g.group(0), body[g.end():]


def main():
    doc = json.loads(SPEC.read_text(encoding="utf-8"))
    changed = 0
    for v in doc["verifiers"]:
        if v["name"] not in TARGETS:
            continue
        pat = v["assertion"]["expected"]
        parts = split_pattern(pat)
        if parts is None:
            print(f"  {v['name']:<46} SKIPPED (not a single-gap pattern)")
            continue
        flags, head, gap, tail = parts
        override = TARGETS[v["name"]]
        if override:
            tail = override
        head_g = head if head.startswith("(") else f"(?:{head})"
        tail_g = tail if tail.startswith("(") else f"(?:{tail})"
        v["assertion"]["expected"] = (
            f"{flags or '(?is)'}(?:{head_g}{gap}{tail_g}|{tail_g}{gap}{head_g})"
        )
        v["metadata"]["how_justification"] = (
            v["metadata"].get("how_justification", "").rstrip(".")
            + ". Matches with the explanation on either side of the identifier, so a memo "
              "grouped by reason is accepted as readily as one grouped by section."
        ).lstrip(". ")
        changed += 1
        print(f"  {v['name']:<46} bidirectional")
    SPEC.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"\n{changed} verifier(s) rewritten")


if __name__ == "__main__":
    main()

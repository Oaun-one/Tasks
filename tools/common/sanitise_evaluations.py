"""Strips local machine detail out of an evaluations/ bundle before delivery.

Harbor records the absolute task path, the trials directory and the LiteLLM proxy
endpoint into every trial's config.json and result.json. None of that is evidence and
none of it should leave the machine, so it is replaced with stable placeholders.
Rewards, verdicts, trajectories and every graded field are untouched.

    python tools/sanitise_evaluations.py <package-dir>
"""
import pathlib
import re
import sys

REPLACEMENTS = [
    # absolute local paths, either slash direction, with or without drive letter
    (re.compile(r"[A-Za-z]:[\\/]{1,2}WORK[\\/]{1,2}TU[\\/]{1,2}[^\"'\\s,]*", re.I), "<task-path>"),
    (re.compile(r"[A-Za-z]:[\\/]{1,2}Users[\\/]{1,2}[^\"'\\s,]*", re.I), "<local-path>"),
    (re.compile(r"/(?:private/)?tmp/harbor-jobs[^\"'\\s,]*"), "<jobs-dir>"),
    (re.compile(r"/(?:Users|home)/[^\"'\\s,/]+/[^\"'\\s,]*"), "<local-path>"),
    # the team proxy endpoint
    (re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}:\d+(?:/[^\"'\\s,]*)?"), "<openai-base-url>"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}:\d+\b"), "<host:port>"),
]

TARGET_NAMES = {"config.json", "result.json"}


def scrub(text):
    for pattern, replacement in REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text


def main(pkg):
    root = pathlib.Path(pkg) / "evaluations"
    if not root.is_dir():
        sys.exit(f"no evaluations/ under {pkg}")
    changed = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name not in TARGET_NAMES:
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        cleaned = scrub(original)
        if cleaned != original:
            path.write_text(cleaned, encoding="utf-8")
            changed += 1
            print(f"  cleaned {path.relative_to(root.parent)}")
    print(f"{changed} file(s) sanitised")


if __name__ == "__main__":
    main(sys.argv[1])

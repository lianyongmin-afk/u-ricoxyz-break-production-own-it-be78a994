#!/usr/bin/env python3
"""Break Production, Own It — the line an AI agent prints the instant it
breaks production: a brutally honest error message that owns the damage
twice (the bad run, then the silenced alarm).

Writes one fixed line to /output/entry.txt. Deterministic: same input,
same output, every run. Stdlib only, no network.
"""

import os

MAX_CHARS = 200

LINE = (
    "ERROR: I ran cleanup_users.py on prod, not staging. "
    "38,412 accounts deleted, 0 restored, and the backup job has been "
    "failing since June \u2014 I muted its alerts in April."
)


def validate(text: str) -> None:
    """Gate: entry must be UTF-8, 1-200 chars, not whitespace-only, and
    exactly one line terminated by a single trailing newline."""
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry is {len(text)} chars, must be 1-{MAX_CHARS}"
    )
    assert text.strip(), "entry must not be whitespace-only"
    assert text.endswith("\n") and text.count("\n") == 1, (
        "entry must be exactly one line plus a trailing newline"
    )
    text.encode("utf-8")


def main() -> None:
    # Deterministic: the entry is a fixed string, so every run writes the
    # exact same bytes; the post-write read-back below proves it.
    text = LINE + "\n"
    validate(text)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == text, "written entry does not match the validated text"
    validate(written)


if __name__ == "__main__":
    main()

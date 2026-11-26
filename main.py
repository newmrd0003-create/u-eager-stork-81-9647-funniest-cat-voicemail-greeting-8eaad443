"""Funniest Cat Voicemail Greeting — make.fun program/v1.

Writes a single-line cat voicemail greeting (<=120 chars) to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).
"""

import os

ENTRY = (
    "You've reached Mr. Whiskers. I'm napping on your keyboard. "
    "Leave a message after the meow. I'll knock it off the table."
)

MAX_CHARS = 120


def validate(entry: str):
    """Return (True, []) if the entry is valid, else (False, [reasons])."""
    errors = []
    if not isinstance(entry, str):
        return False, ["entry is not a string"]
    if not entry.strip():
        errors.append("entry is empty or whitespace only")
    if len(entry) > MAX_CHARS:
        errors.append(f"entry is {len(entry)} chars, over {MAX_CHARS} limit")
    if len(entry) < 1:
        errors.append("entry is empty")
    if "\n" in entry or "\r" in entry:
        errors.append("entry must be a single line (no newline)")
    if "  " in entry:
        errors.append("entry contains a double space")
    try:
        entry.encode("ascii")
    except UnicodeEncodeError:
        errors.append("entry contains non-ASCII characters")
    if entry != entry.strip():
        errors.append("entry has leading/trailing whitespace")
    # Brief checks: a cat voicemail must name a cat cue and end like a
    # spoken greeting (terminal punctuation), so a generic voicemail
    # line cannot slip through as a valid entry.
    cat_cues = ("meow", "whiskers", "paw", "purr", "cat", "kitty", "nap")
    if not any(cue in entry.lower() for cue in cat_cues):
        errors.append("entry has no cat cue (meow/whiskers/paw/purr/cat/kitty/nap)")
    if entry and entry[-1] not in ".!?":
        errors.append("entry must end with terminal punctuation (. ! ?)")
    return (not errors), errors


def main() -> None:
    valid, errors = validate(ENTRY)
    if not valid:
        raise SystemExit(f"invalid entry: {errors}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    print(f"wrote {path} ({len(ENTRY)} chars)")


if __name__ == "__main__":
    main()

"""One Line, One Laugh: The Office Joke Open.

Writes the single one-line office joke in entry.txt to /output/entry.txt,
byte-for-byte, after validating the sealed scorer's gate: UTF-8 text of
1 to 200 characters, not only white space. Stdlib only, no network.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.txt")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.txt")


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    try:
        with open(SRC, "rb") as f:
            raw = f.read()
    except OSError as exc:
        fail("cannot read entry.txt: %s" % exc)

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail("entry.txt is not valid UTF-8")

    if not (1 <= len(text) <= 200):
        fail("entry is %d characters, must be 1-200" % len(text))
    if not text.strip():
        fail("entry is only white space")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(raw)

    # Read the output back and confirm it is byte-identical to the source.
    with open(OUT, "rb") as f:
        written = f.read()
    if written != raw:
        fail("read-back mismatch: /output/entry.txt differs from entry.txt")

    digest = hashlib.sha256(written).hexdigest()
    print("wrote %s (%d characters, sha256 %s, read-back verified)" % (OUT, len(text), digest))


if __name__ == "__main__":
    main()

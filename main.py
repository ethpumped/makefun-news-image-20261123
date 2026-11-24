#!/usr/bin/env python3
"""THE DAWN LEDGER — entry program for news-image-20261123 (final2).

The Dawn Ledger is a one-page newspaper of Monday 23 November 2026,
drawn for @ethpumped: Nepal's Shah meets Modi in Delhi on the front,
COP31 and India's record 720/9 beside it, 41 stories in all.

This program does one small job, with the standard library only: it
copies the finished entry.png that sits next to it into the output
directory, after checking the copy source is exactly the file that
was measured and hashed when the entry was built. No Pillow, no
network, no surprises — two runs produce byte-identical output.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 120408
EXPECTED_SHA256 = "d61025feb353f0313615317c63b2878d7819eb50c9dbc57215a09bbc5101fd28"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
HARD_CAP = 1048576  # the competition's 1 MiB ceiling


def fail(msg):
    # Refusals go to stderr so a failed run never looks like a quiet success.
    sys.stderr.write("entry refused: %s\n" % msg)
    sys.exit(1)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")

    with open(source, "rb") as fh:
        blob = fh.read()

    if not blob.startswith(PNG_HEADER):
        fail("entry.png does not start with the PNG magic bytes")
    if len(blob) > HARD_CAP:
        fail("entry.png is %d bytes, over the 1 MiB cap" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        fail("entry.png is %d bytes; expected %d" % (len(blob), EXPECTED_BYTES))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("entry.png sha256 %s does not match the built file" % digest)

    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as fh:
        fh.write(blob)
    sys.stderr.write("wrote %s (%d bytes, sha256 %s)\n" % (target, len(blob), digest))


if __name__ == "__main__":
    run()

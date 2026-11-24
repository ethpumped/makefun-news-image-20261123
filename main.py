#!/usr/bin/env python3
"""Deliver THE DAWN LEDGER's front page (final2, news-image-20261123).

THE DAWN LEDGER sums up Monday 23 November 2026 on a single peach
dawn page: Shah of Nepal across the table from Modi in Delhi at the
top, forty-one stories from seven regions underneath, and a date
check that keeps every other day's news off the page.

The entry image is finished long before this program runs. All the
program does — standard library only, nothing imported beyond
hashlib, os and sys — is verify that entry.png beside it is still
the exact measured file, then copy it into the output directory.
Run it twice and the output bytes do not change.
"""

import hashlib
import os
import sys

MEASURED_BYTES = 120408
MEASURED_SHA256 = "d61025feb353f0313615317c63b2878d7819eb50c9dbc57215a09bbc5101fd28"
MAGIC = b"\x89PNG\r\n\x1a\n"
CEILING = 1048576


def die(reason):
    # A stopped entry must say so out loud; silence would look like success.
    sys.stderr.write("THE DAWN LEDGER entry stopped: %s\n" % reason)
    raise SystemExit(1)


def deliver():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as fh:
        page = fh.read()

    if page[:8] != MAGIC:
        die("entry.png is not a PNG file")
    if len(page) != MEASURED_BYTES:
        die("entry.png measures %d bytes, not %d" % (len(page), MEASURED_BYTES))
    if len(page) > CEILING:
        die("entry.png passes the competition's 1 MiB ceiling")
    if hashlib.sha256(page).hexdigest() != MEASURED_SHA256:
        die("entry.png hash differs from the measured front page")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    with open(destination, "wb") as fh:
        fh.write(page)
    sys.stderr.write(
        "delivered %s — %d bytes, sha256 %s\n"
        % (destination, len(page), MEASURED_SHA256)
    )


if __name__ == "__main__":
    deliver()

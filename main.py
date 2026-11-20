#!/usr/bin/env python3
"""Entry point for the news-image-20261120 make.fun competition.

Copies the pre-rendered front page (entry.png, shipped next to this file)
to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when the variable
is unset). Standard library only; no network; fully deterministic — two
runs write byte-identical files.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

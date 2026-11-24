#!/usr/bin/env python3
"""Entry point (Python 3.13, standard library only).

Copies the meme image beside this file to $MAKEFUN_OUTPUT_DIR/entry.png.
The image itself was drawn by draw_meme.py (Pillow, run locally when the
entry was built); the grader runs standard library only, so this entry
point copies the pre-rendered PNG instead of drawing it.
Deterministic: a copy writes the same bytes on every run.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_DIM = 1024


def png_dimensions(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    src = os.path.join(HERE, "entry.png")
    # Validate the shipped image before copying, so a bad source fails
    # fast instead of writing a bad entry.
    src_w, src_h = png_dimensions(src)
    if src_w > MAX_DIM or src_h > MAX_DIM:
        raise SystemExit("shipped entry.png exceeds 1024x1024")
    if os.path.getsize(src) > MAX_BYTES:
        raise SystemExit("shipped entry.png exceeds 1 MiB")
    shutil.copyfile(src, path)
    width, height = png_dimensions(path)
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit("entry.png exceeds 1024x1024: %dx%d" % (width, height))
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB: %d bytes" % size)
    if os.path.getsize(src) != size:
        raise SystemExit("copied entry.png has the wrong size")
    print("wrote", path, size, "bytes", "%dx%d" % (width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())

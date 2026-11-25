#!/usr/bin/env python3
"""THE WORLD TODAY -- entrypoint for make.fun news-image-20261125.

The front page (1024x1024, Wednesday 25 November 2026) is drawn by
draw_frontpage.py, which produced the entry.png shipped in this repository.
This entrypoint is standard library only: it copies that image to the
grader's output directory, so it runs in the sandbox (no network, a
read-only repository, nothing installed before it runs).

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Flags:
    --check      verify the shipped entry.png is a valid PNG within the
                 competition limits (<=1 MiB, <=1024x1024), exit 0/1.
    --self-test  run the copy into a temporary directory and verify it.
"""

import argparse
import hashlib
import os
import shutil
import struct
import sys
import tempfile
import zlib

MAX_BYTES = 1048576
MAX_DIM = 1024


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def png_size(path):
    """Return (width, height) of a PNG using stdlib only, else None."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def validate_written(src, dst):
    """Read the written entry.png back and verify it is the repo copy.

    Re-checks the on-disk artifact itself (valid PNG, within limits,
    byte-identical sha256 to the repository copy) instead of trusting
    the copy call. Raises ValueError with a clear message on failure.
    """
    if not os.path.isfile(dst):
        raise ValueError("invalid output: %s was not written" % dst)
    problem = check_entry(dst)
    if problem is not None:
        raise ValueError("invalid written entry: " + problem)
    want = sha256_of(src)
    got = sha256_of(dst)
    if want != got:
        raise ValueError(
            "invalid output: written entry.png sha256 %s does not match "
            "the repository copy %s" % (got, want))
    return got


def check_entry(path):
    """Validate the shipped entry.png against the competition gate."""
    if not os.path.isfile(path):
        return "entry.png is missing from the repository"
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return "entry.png is %d bytes, over the 1 MiB limit" % size
    dims = png_size(path)
    if dims is None:
        return "entry.png is not a readable PNG"
    width, height = dims
    if width > MAX_DIM or height > MAX_DIM:
        return "entry.png is %dx%d, over the 1024x1024 limit" % dims
    return None


def write_entry(out_dir):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    problem = check_entry(src)
    if problem is not None:
        raise ValueError("invalid entry: " + problem)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    digest = validate_written(src, dst)
    return dst, digest


def main(argv=None):
    parser = argparse.ArgumentParser(description="Copy entry.png to the output directory.")
    parser.add_argument("--check", action="store_true",
                        help="validate the shipped entry.png and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="copy into a temp dir and verify the copy")
    args = parser.parse_args(argv)

    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")

    if args.check:
        problem = check_entry(src)
        if problem is not None:
            print("check failed: " + problem, file=sys.stderr)
            return 1
        print("check ok: entry.png %dx%d, %d bytes, sha256 %s"
              % (png_size(src) + (os.path.getsize(src), sha256_of(src))))
        return 0

    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                dst, digest = write_entry(tmp)
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                return 1
            print("self-test ok: wrote", dst, "sha256", digest)
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        dst, digest = write_entry(out_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("wrote", dst, "sha256", digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

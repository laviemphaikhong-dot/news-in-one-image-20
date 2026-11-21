#!/usr/bin/env python3
"""Publish the finished front page for the 20 November news bounty.

The page was researched, drawn in code and proofed during the build session;
the result ships in this repository as ``entry.png``. This program delivers
it: the PNG is copied, byte for byte, into the directory the grading harness
names through ``MAKEFUN_OUTPUT_DIR`` (falling back to ``/output``).

The program reads no clock, opens no network connection and rolls no dice,
so repeated runs emit exactly the same bytes.
"""

import os
import pathlib
import shutil

PAGE = pathlib.Path(__file__).resolve().with_name("entry.png")


def output_dir() -> pathlib.Path:
    named = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return pathlib.Path(named) if named else pathlib.Path("/output")


def main() -> None:
    if not PAGE.is_file():
        raise SystemExit(f"entry.png is missing beside {__file__}")
    folder = output_dir()
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PAGE, folder / "entry.png")


if __name__ == "__main__":
    main()

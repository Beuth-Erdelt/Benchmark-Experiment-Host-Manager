#!/usr/bin/env python3
"""
Convert line endings to LF (Unix-style) in documentation, log, and image files.

Processes .md, .txt, Dockerfile*, .sh, and .py files under docs/, logs_tests/,
images/, and scripts/, rewriting each file in UTF-8 without BOM with LF line
endings.

Run from the repo root:
    python scripts/convert-to-lf.py

Author: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""

from pathlib import Path

SEARCH_PATHS = ["docs", "logs_tests", "images", "scripts"]

INCLUDE_SUFFIXES = {".md", ".txt", ".sh", ".py", ".log"}
INCLUDE_NAME_PREFIXES = {"Dockerfile"}


def matches(path: Path) -> bool:
    """Return True if the file should be converted."""
    return (
        path.suffix in INCLUDE_SUFFIXES
        or any(path.name.startswith(prefix) for prefix in INCLUDE_NAME_PREFIXES)
    )


def convert_file(path: Path) -> None:
    """Rewrite a file as UTF-8 without BOM with LF line endings."""
    raw = path.read_bytes()
    # Strip UTF-8 BOM if present
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(text.encode("utf-8"))
    print(f"Converted: {path}")


def main() -> None:
    """Convert all matching files in the configured search paths."""
    repo_root = Path(__file__).parent.parent
    for search_path in SEARCH_PATHS:
        directory = repo_root / search_path
        if not directory.is_dir():
            continue
        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file() and matches(file_path):
                convert_file(file_path)


if __name__ == "__main__":
    main()

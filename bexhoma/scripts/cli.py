"""
Unified ``bexhoma`` CLI dispatcher.

Runs a root-level benchmark script by name and forwards all remaining
arguments to it::

    bexhoma tpch  run  [args...]
    bexhoma tpcds load [args...]
    bexhoma ycsb  run  [args...]

The script is looked up as ``<project_root>/<name>.py``.  In an editable
install the project root is three directories above this file.

Authors: Patrick K. Erdelt
Copyright (C) 2024 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    """
    Entry point for the ``bexhoma`` console script.

    Reads the first positional argument as a script name, locates
    ``<project_root>/<name>.py``, and delegates to it via subprocess,
    forwarding all remaining arguments unchanged.

    :raises SystemExit: mirrors the exit code of the delegated script.
    """
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: bexhoma <script> [args...]")
        print("Example: bexhoma tpch run -m -cx my-context")
        sys.exit(0)

    script_name = sys.argv[1]
    remaining_args = sys.argv[2:]
    script_path = _PROJECT_ROOT / f"{script_name}.py"

    if not script_path.exists():
        print(f"bexhoma: script not found: {script_path}")
        sys.exit(1)

    result = subprocess.run([sys.executable, str(script_path)] + remaining_args)
    sys.exit(result.returncode)

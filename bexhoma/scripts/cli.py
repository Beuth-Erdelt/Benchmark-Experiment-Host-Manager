"""
Unified ``bexhoma`` CLI dispatcher.

Runs a root-level benchmark script by name and forwards all remaining
arguments to it::

    bexhoma tpch  run  [args...]
    bexhoma tpcds load [args...]
    bexhoma ycsb  run  [args...]

The script is located by walking up from the current working directory
until a file named ``<name>.py`` is found.  This works regardless of
whether the package is installed in editable or regular mode.

If the first argument is one of ``EXPERIMENT_MODES`` (``stop``, ``status``,
``summary``, ...), the call is dispatched in-process to
:func:`bexhoma.scripts.experimentsmanager.manage` instead, e.g.
``bexhoma summary -e 12345678``.  The import of ``experimentsmanager``
(and its heavier ``dbmsbenchmarker`` dependency) is deferred to that branch
so that plain script dispatch (``bexhoma tpch run``) does not require it.

Authors: Patrick K. Erdelt
Copyright (C) 2024 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import subprocess
import sys
from pathlib import Path

#: Modes handled by :func:`bexhoma.scripts.experimentsmanager.manage`;
#: defined here (rather than imported from there) so that checking
#: membership does not force-import that module's heavy dependencies.
EXPERIMENT_MODES = ['stop', 'status', 'dashboard', 'messagequeue', 'localdashboard', 'localresults', 'jupyter', 'master', 'data', 'summary']


def _find_script(name: str) -> Path | None:
    """
    Walk up from the current directory until ``<name>.py`` is found.

    :param name: Script base name (without ``.py``).
    :type name: str
    :return: Absolute path to the script, or ``None`` if not found.
    :rtype: pathlib.Path or None
    """
    candidate = Path.cwd()
    while True:
        script = candidate / f"{name}.py"
        if script.exists():
            return script
        parent = candidate.parent
        if parent == candidate:
            return None
        candidate = parent


def main():
    """
    Entry point for the ``bexhoma`` console script.

    If the first positional argument is one of ``EXPERIMENT_MODES``, delegates
    in-process to :func:`bexhoma.scripts.experimentsmanager.manage`.
    Otherwise treats it as a script name, locates ``<name>.py`` by walking up
    from the current working directory, and delegates to it via subprocess,
    forwarding all remaining arguments unchanged.

    :raises SystemExit: mirrors the exit code of the delegated script.
    """
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: bexhoma <script> [args...]")
        print("Example: bexhoma tpch run -m -cx my-context")
        print("Example: bexhoma summary -e 12345678")
        sys.exit(0)

    script_name = sys.argv[1]

    if script_name in EXPERIMENT_MODES:
        from bexhoma.scripts.experimentsmanager import manage
        manage()
        return

    remaining_args = sys.argv[2:]
    script_path = _find_script(script_name)

    if script_path is None:
        print(f"bexhoma: '{script_name}.py' not found in {Path.cwd()} or any parent directory")
        sys.exit(1)

    result = subprocess.run([sys.executable, str(script_path)] + remaining_args)
    sys.exit(result.returncode)

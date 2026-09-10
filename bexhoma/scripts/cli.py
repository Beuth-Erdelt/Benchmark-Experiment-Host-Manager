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

``bexhoma environment <subcommand>`` is dispatched in-process to
:mod:`bexhoma.environment` instead of being treated as a script name, e.g.
``bexhoma environment create -cx my-context``. See ``docs/Environment.md``.

``bexhoma agent <subcommand> [args...]`` runs the optional contract-driven
benchmark agent under ``agent/`` as a subprocess, e.g.
``bexhoma agent design --task "..."`` or ``bexhoma agent lifecycle --task
"..."``. It needs the ``agent`` install extra (``pip install "bexhoma[agent]"``)
and prints a hint rather than a traceback when that is missing. See
``docs/AgentHarness.md``.

Authors: Patrick K. Erdelt
Copyright (C) 2024 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

#: Modes handled by :func:`bexhoma.scripts.experimentsmanager.manage`;
#: defined here (rather than imported from there) so that checking
#: membership does not force-import that module's heavy dependencies.
EXPERIMENT_MODES = ['stop', 'status', 'dashboard', 'messagequeue', 'localdashboard', 'localresults', 'jupyter', 'master', 'data', 'summary']

#: ``bexhoma agent <name>`` -> the module run as ``python -m <module>`` and the
#: arguments prepended before the caller's own. ``design``/``interpret``/
#: ``baseline`` are the three phases of the same agent CLI; ``validate`` and
#: ``lifecycle`` are its standalone tools.
AGENT_SUBCOMMANDS = {
    'design':    ('agent.harness.agent', ['--phase', 'design']),
    'interpret': ('agent.harness.agent', ['--phase', 'interpret']),
    'baseline':  ('agent.harness.agent', ['--phase', 'baseline']),
    'validate':  ('agent.harness.validate', []),
    'lifecycle': ('agent.lifecycle', []),
}


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


def _run_agent(args):
    """
    Dispatch ``bexhoma agent <subcommand> [args...]`` to the agent package.

    Each subcommand maps to a module run as ``python -m <module>`` with the
    caller's arguments appended, mirroring the subprocess dispatch used for the
    root benchmark scripts.

    :param args: Arguments after ``agent`` (the subcommand and its own args).
    :type args: list[str]
    :raises SystemExit: mirrors the delegated module's exit code, or a
        non-zero code for a usage error or a missing ``agent`` extra.
    """
    if not args or args[0] in ("-h", "--help"):
        print("Usage: bexhoma agent <subcommand> [args...]")
        print("Subcommands: " + ", ".join(AGENT_SUBCOMMANDS))
        print('Example: bexhoma agent design --task "is PgDuckDB faster on joins?"')
        print('Example: bexhoma agent lifecycle --task "..." --followups 1')
        sys.exit(0)

    subcommand, forwarded = args[0], args[1:]
    if subcommand not in AGENT_SUBCOMMANDS:
        print(f"bexhoma agent: unknown subcommand '{subcommand}'; "
              f"choose from {', '.join(AGENT_SUBCOMMANDS)}")
        sys.exit(1)

    # The agent speaks to an OpenAI-compatible server and reads a .env file
    # through dependencies that only the `agent` extra installs.
    if any(importlib.util.find_spec(name) is None for name in ("openai", "dotenv")):
        print('bexhoma agent needs the agent extra: pip install "bexhoma[agent]"')
        sys.exit(1)

    module, prefix = AGENT_SUBCOMMANDS[subcommand]
    result = subprocess.run([sys.executable, "-m", module, *prefix, *forwarded])
    sys.exit(result.returncode)


def main():
    """
    Entry point for the ``bexhoma`` console script.

    If the first positional argument is one of ``EXPERIMENT_MODES``, delegates
    in-process to :func:`bexhoma.scripts.experimentsmanager.manage`.
    ``environment`` and ``agent`` are dispatched to their own handlers.
    Otherwise treats it as a script name, locates ``<name>.py`` by walking up
    from the current working directory, and delegates to it via subprocess,
    forwarding all remaining arguments unchanged.

    :raises SystemExit: mirrors the exit code of the delegated script.
    """
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: bexhoma <script> [args...]")
        print("Example: bexhoma tpch run -m -cx my-context")
        print("Example: bexhoma summary -e 12345678")
        print("Example: bexhoma environment create -cx my-context")
        print("Example: bexhoma agent design --task \"...\"")
        sys.exit(0)

    script_name = sys.argv[1]

    if script_name in EXPERIMENT_MODES:
        from bexhoma.scripts.experimentsmanager import manage
        manage()
        return

    remaining_args = sys.argv[2:]

    if script_name == "agent":
        _run_agent(remaining_args)
        return

    if script_name == "environment":
        if not remaining_args or remaining_args[0] in ("-h", "--help"):
            print("Usage: bexhoma environment <subcommand> [args...]")
            print("Subcommands:")
            print("  create   Inspect the live cluster and write environment.yml")
            print("Example: bexhoma environment create -cx my-context -o dev/catalog/environment.yml")
            sys.exit(0)
        subcommand, subcommand_args = remaining_args[0], remaining_args[1:]
        if subcommand == "create":
            from bexhoma.environment import main as environment_main
            environment_main(subcommand_args)
            return
        print(f"bexhoma environment: unknown subcommand '{subcommand}'")
        sys.exit(1)
    script_path = _find_script(script_name)

    if script_path is None:
        print(f"bexhoma: '{script_name}.py' not found in {Path.cwd()} or any parent directory")
        sys.exit(1)

    result = subprocess.run([sys.executable, str(script_path)] + remaining_args)
    sys.exit(result.returncode)

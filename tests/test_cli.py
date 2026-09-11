"""
Unit tests for the ``bexhoma`` CLI dispatcher's ``agent`` subcommand.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import subprocess
import sys
import unittest
from unittest import mock

from bexhoma.scripts import cli

__all__: list[str] = []


class AgentSubcommandTest(unittest.TestCase):
    """Tests for :func:`bexhoma.scripts.cli._run_agent`."""

    def _run(self, args: list[str]) -> tuple[int, list[str]]:
        """Run ``_run_agent`` with the extra present and subprocess stubbed.

        :param args: Arguments after ``agent``.
        :return: The exit code, and the argument vector handed to subprocess
            (empty when nothing was delegated).
        :rtype: tuple[int, list[str]]
        """
        delegated: list[str] = []

        def fake_run(command, *_args, **_kwargs):
            delegated.extend(command)
            return subprocess.CompletedProcess(command, 0)

        with (
            mock.patch.object(cli.subprocess, "run", side_effect=fake_run),
            mock.patch.object(cli.importlib.util, "find_spec", return_value=object()),
            self.assertRaises(SystemExit) as raised,
        ):
            cli._run_agent(args)
        code = raised.exception.code or 0
        return code, delegated

    def test_design_forwards_the_phase_and_the_rest(self) -> None:
        code, command = self._run(["design", "--task", "why?"])
        self.assertEqual(code, 0)
        self.assertEqual(
            command,
            [sys.executable, "-m", "agent.harness.agent",
             "--phase", "design", "--task", "why?"],
        )

    def test_lifecycle_maps_to_its_own_module(self) -> None:
        _code, command = self._run(["lifecycle", "--task", "why?", "--followups", "1"])
        self.assertEqual(
            command,
            [sys.executable, "-m", "agent.lifecycle",
             "--task", "why?", "--followups", "1"],
        )

    def test_validate_takes_no_phase_prefix(self) -> None:
        _code, command = self._run(["validate", "experiment.yml", "--environment", ""])
        self.assertEqual(
            command,
            [sys.executable, "-m", "agent.harness.validate",
             "experiment.yml", "--environment", ""],
        )

    def test_unknown_subcommand_is_rejected(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            cli._run_agent(["frobnicate"])
        self.assertEqual(raised.exception.code, 1)

    def test_no_subcommand_prints_usage_and_exits_zero(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            cli._run_agent([])
        self.assertEqual(raised.exception.code or 0, 0)

    def test_missing_agent_extra_prints_a_hint(self) -> None:
        with (
            mock.patch.object(cli.importlib.util, "find_spec", return_value=None),
            mock.patch.object(cli.subprocess, "run") as delegated,
            self.assertRaises(SystemExit) as raised,
        ):
            cli._run_agent(["design", "--task", "why?"])
        self.assertEqual(raised.exception.code, 1)
        delegated.assert_not_called()

    def test_main_routes_agent_before_script_lookup(self) -> None:
        with (
            mock.patch.object(cli, "_run_agent") as run_agent,
            mock.patch.object(cli, "_find_script") as find_script,
            mock.patch.object(sys, "argv", ["bexhoma", "agent", "design", "--task", "x"]),
        ):
            cli.main()
        run_agent.assert_called_once_with(["design", "--task", "x"])
        find_script.assert_not_called()


if __name__ == "__main__":
    unittest.main()

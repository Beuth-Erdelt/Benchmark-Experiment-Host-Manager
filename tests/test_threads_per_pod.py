"""Tests for the check that a thread total splits evenly across the pods.

``-nbt``/``-nlt`` count the threads of all pods together. With
``-nbp 1,2 -nbt 1`` each of the 2 pods got 0 threads and measured nothing,
without an error; the entry scripts now refuse such a command right after
parsing.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest

from bexhoma.cli_args import threads_per_pod_error

from .test_reset_scripts import _run_script
from .test_tenancy import _refused

__all__ = []


class ThreadsPerPodErrorTest(unittest.TestCase):
    """The message for ``parser.error``, or ``''``."""

    def test_even_splits_are_fine(self) -> None:
        self.assertEqual(threads_per_pod_error('2', '1,2', '-nbt', '-nbp'), '')
        self.assertEqual(threads_per_pod_error('16,32', '1,2', '-nbt', '-nbp'), '')
        self.assertEqual(threads_per_pod_error('1', '1', '-nlt', '-nlp'), '')

    def test_fewer_threads_than_pods_is_refused(self) -> None:
        reason = threads_per_pod_error('1', '1,2', '-nbt', '-nbp')
        self.assertIn('-nbt 1', reason)
        self.assertIn('1 threads on 2 pods', reason)
        self.assertNotIn('1 threads on 1 pods', reason)

    def test_a_remainder_is_refused(self) -> None:
        self.assertIn('3 threads on 2 pods', threads_per_pod_error('3', '2', '-nlt', '-nlp'))

    def test_every_bad_combination_is_named(self) -> None:
        reason = threads_per_pod_error('2,3', '2,4', '-nbt', '-nbp')
        for pair in ('2 threads on 4 pods', '3 threads on 2 pods', '3 threads on 4 pods'):
            self.assertIn(pair, reason)
        self.assertNotIn('2 threads on 2 pods', reason)

    def test_zero_pods_and_non_integers_are_refused(self) -> None:
        self.assertIn('must be at least 1', threads_per_pod_error('2', '0', '-nbt', '-nbp'))
        self.assertIn('comma-separated integers', threads_per_pod_error('x', '1', '-nbt', '-nbp'))


class EntryScriptsTest(unittest.TestCase):
    """The real scripts. A refusal is a usage error right after parsing: no cluster is needed."""

    def test_benchmarking_threads_are_checked(self) -> None:
        for script, dbms in (('ycsb.py', 'PostgreSQL'), ('benchbase.py', 'PostgreSQL'),
                             ('hammerdb.py', 'PostgreSQL')):
            with self.subTest(script=script):
                code, stderr = _refused(script, '-dbms', dbms, '-nbp', '1,2', '-nbt', '1')
                self.assertEqual(code, 2)
                self.assertIn('1 threads on 2 pods', stderr)

    def test_loading_threads_are_checked(self) -> None:
        for script in ('ycsb.py', 'benchbase.py', 'hammerdb.py'):
            with self.subTest(script=script):
                code, stderr = _refused(script, '-dbms', 'PostgreSQL', '-nlp', '8', '-nlt', '4')
                self.assertEqual(code, 2)
                self.assertIn('4 threads on 8 pods', stderr)

    def test_hardware_tools_with_threads_are_checked(self) -> None:
        for tool in ('fio', 'sysbench', 'netperf'):
            with self.subTest(tool=tool):
                code, stderr = _refused('hardware.py', '-dbms', 'Hardware', '-xht', tool,
                                        '-nbp', '1,2', '-nbt', '1')
                self.assertEqual(code, 2)
                self.assertIn('1 threads on 2 pods', stderr)

    def test_sockperf_ignores_the_thread_count(self) -> None:
        _, configurations = _run_script('hardware.py', '-xht', 'sockperf', '-nbp', '1,2', '-nbt', '1')
        self.assertTrue(configurations)

    def test_an_even_split_reaches_the_experiment(self) -> None:
        _, configurations = _run_script('hardware.py', '-xht', 'fio', '-nbp', '1,2', '-nbt', '2')
        self.assertTrue(configurations)


if __name__ == '__main__':
    unittest.main()

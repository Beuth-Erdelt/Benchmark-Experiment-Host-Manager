"""Tests for the round gate of container tenancy (``tenant_per == 'container'``).

Every container tenant is a configuration of its own. A tenant ready for its
next client round waits until every tenant that still runs this round is ready
too; then all of them submit in the same pass, so their reset scripts run side
by side and none runs while another tenant still benchmarks.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""

from __future__ import annotations

import contextlib
import io
import unittest
from types import SimpleNamespace

from bexhoma.experiments.base import ExperimentBase


def _config(name: str, client: int = 1, rounds: int = 2, done: int = 0, repetitions: int = 1,
            experiment_done: bool = False, parallelism: int = 1) -> SimpleNamespace:
    return SimpleNamespace(
        configuration=name,
        client=client,
        experiment_dict={"loader": [], "benchmarker": [[{"parallelism": parallelism}] for _ in range(rounds)]},
        num_experiment_to_apply_done=done,
        num_experiment_to_apply=repetitions,
        experiment_done=experiment_done,
    )


def _experiment(configs: list) -> ExperimentBase:
    experiment = ExperimentBase.__new__(ExperimentBase)
    experiment.configurations = configs
    experiment.tenant_per = 'container'
    experiment.code = '123'
    experiment.client = 1
    counters = {}
    experiment.cluster = SimpleNamespace(
        set_pod_counter=lambda queue, value: counters.__setitem__(queue, value))
    experiment.counters = counters
    return experiment


def _release(experiment: ExperimentBase, ready: dict) -> list:
    with contextlib.redirect_stdout(io.StringIO()):
        return [c.configuration for c in experiment._release_tenant_rounds(ready)]


class NextRoundPositionTest(unittest.TestCase):

    def test_round_of_this_repetition(self):
        experiment = _experiment([])
        self.assertEqual(experiment._next_round_position(_config('a', client=2)), (1, 2))

    def test_rounds_done_next_repetition(self):
        experiment = _experiment([])
        self.assertEqual(experiment._next_round_position(_config('a', client=3, repetitions=2)), (2, 1))

    def test_rounds_done_no_repetition_left(self):
        experiment = _experiment([])
        self.assertIsNone(experiment._next_round_position(_config('a', client=3)))

    def test_done_or_legacy_is_not_waited_for(self):
        experiment = _experiment([])
        self.assertIsNone(experiment._next_round_position(_config('a', experiment_done=True)))
        self.assertIsNone(experiment._next_round_position(_config('a', rounds=0)))


class ReleaseTenantRoundsTest(unittest.TestCase):

    def test_waits_until_last_tenant_is_ready(self):
        configs = [_config('a', client=2), _config('b', client=2), _config('c', client=2)]
        experiment = _experiment(configs)
        # staggered: a and b are ready, c still benchmarks round 1
        self.assertEqual(_release(experiment, {'a': (1, 2), 'b': (1, 2)}), [])
        # c ready in a later pass: all three start together
        self.assertEqual(_release(experiment, {'a': (1, 2), 'b': (1, 2), 'c': (1, 2)}), ['a', 'b', 'c'])

    def test_readiness_counts_per_pass(self):
        configs = [_config('a', client=2), _config('b', client=2)]
        experiment = _experiment(configs)
        # b not ready in this pass (e.g. unhealthy): a waits
        self.assertEqual(_release(experiment, {'a': (1, 2)}), [])

    def test_dropped_out_tenant_is_not_waited_for(self):
        configs = [_config('a', client=2), _config('b', client=2, experiment_done=True),
                   _config('c', client=2, rounds=1)]
        experiment = _experiment(configs)
        self.assertEqual(_release(experiment, {'a': (1, 2)}), ['a'])

    def test_lagging_tenant_runs_its_round_alone(self):
        # b skipped ahead (a round of it was skipped), a still has round 2 to run
        configs = [_config('a', client=2, rounds=3), _config('b', client=3, rounds=3)]
        experiment = _experiment(configs)
        self.assertEqual(_release(experiment, {'a': (1, 2), 'b': (1, 3)}), ['a'])
        configs[0].client = 3
        self.assertEqual(_release(experiment, {'a': (1, 3), 'b': (1, 3)}), ['a', 'b'])

    def test_tenant_between_repetitions_is_waited_for(self):
        # b has run all rounds of repetition 1 and restarts its SUT for repetition 2
        configs = [_config('a', client=1, done=1, repetitions=2), _config('b', client=3, repetitions=2)]
        experiment = _experiment(configs)
        self.assertEqual(_release(experiment, {'a': (2, 1)}), [])
        configs[1].client, configs[1].num_experiment_to_apply_done = 1, 1
        self.assertEqual(_release(experiment, {'a': (2, 1), 'b': (2, 1)}), ['a', 'b'])


class QueueRoundTest(unittest.TestCase):

    def test_counters_set_once_for_all_tenants(self):
        configs = [_config('a', parallelism=2), _config('b', parallelism=3)]
        experiment = _experiment(configs)
        with contextlib.redirect_stdout(io.StringIO()):
            steps = [experiment._queue_round(c, 'bexhoma', None) for c in configs]
        self.assertEqual([c.client for c in configs], [2, 2])
        self.assertEqual(experiment.counters['bexhoma-benchmarker-podcount-round-1-1-a-123'], 2)
        self.assertEqual(experiment.counters['bexhoma-benchmarker-podcount-round-1-1-b-123'], 3)
        self.assertEqual(experiment.counters['bexhoma-benchmarker-podcount-exp-123'], 5)
        self.assertEqual([s.func for s in steps], [experiment._submit_round] * 2)
        self.assertEqual(steps[1].args[1:4], ([{"parallelism": 3}], '1', '1'))


if __name__ == '__main__':
    unittest.main()

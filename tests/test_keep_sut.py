"""Tests for keeping or stopping SUTs at the end of an experiment (``-ks/--keep-sut``, ``-ss``).

Covers how the option resolves per mode, that only the last repetition keeps
its SUT, that a kept SUT never blocks a configuration waiting for its slot
under ``-ms``/``-mse``/``max_sut_dbms``, and that the catalog translators make
agent runs stop their SUTs.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import copy
from types import SimpleNamespace
import unittest
from unittest import mock

import tpch
from bexhoma import spec as catalog_spec
from bexhoma.cli_args import make_base_parser, resolve_keep_sut
from bexhoma.experiments.base import ExperimentBase
from tests.test_tpch_catalog_max_sut import _BASE_SPEC as _TPCH_SPEC, _CATALOG_FILE
from tests.test_ycsb_catalog import _BASE_SPEC as _YCSB_SPEC

__all__ = []


class ResolveKeepSutTest(unittest.TestCase):
    """``-ks auto`` keeps in load and start only; yes/no and -ss override it."""

    def test_auto_follows_the_mode(self):
        for mode, kept in (('run', False), ('profiling', False), ('empty', False),
                           ('load', True), ('start', True)):
            with self.subTest(mode):
                self.assertIs(resolve_keep_sut(mode), kept)

    def test_yes_and_no_override_the_mode(self):
        self.assertTrue(resolve_keep_sut('run', 'yes'))
        self.assertFalse(resolve_keep_sut('load', 'no'))

    def test_skip_shutdown_is_keep_yes(self):
        self.assertTrue(resolve_keep_sut('run', 'auto', True))
        self.assertTrue(resolve_keep_sut('run', 'yes', True))

    def test_contradictions_are_refused(self):
        with self.assertRaisesRegex(ValueError, 'use one'):
            resolve_keep_sut('run', 'no', True)
        with self.assertRaisesRegex(ValueError, 'start'):
            resolve_keep_sut('start', 'no')
        with self.assertRaisesRegex(ValueError, 'must be one of'):
            resolve_keep_sut('run', 'maybe')

    def test_parser_default_is_auto(self):
        args = make_base_parser().parse_args([])
        self.assertEqual(args.keep_sut, 'auto')
        self.assertEqual(make_base_parser().parse_args(['-ks', 'no']).keep_sut, 'no')


def _config(name: str, docker: str = 'PostgreSQL', done: bool = False, sut_exists: bool = False,
            max_sut_dbms=None, repetitions: int = 1, repetitions_done: int = 0) -> SimpleNamespace:
    return SimpleNamespace(
        configuration=name, docker=docker, experiment_done=done, max_sut_dbms=max_sut_dbms,
        num_experiment_to_apply=repetitions, num_experiment_to_apply_done=repetitions_done,
        status=SimpleNamespace(sut_exists=lambda: sut_exists))


def _experiment(configurations: list, max_sut=None, cluster_max_sut=None) -> ExperimentBase:
    experiment = ExperimentBase.__new__(ExperimentBase)
    experiment.configurations = configurations
    experiment.max_sut = max_sut
    experiment.cluster = SimpleNamespace(max_sut=cluster_max_sut)
    experiment.workload = {}
    return experiment


class LeavesSutRunningTest(unittest.TestCase):
    """Only the last repetition keeps its SUT, and never one another configuration waits for."""

    def decide(self, experiment, config, stop_after_starting=False, keep=True):
        with mock.patch('builtins.print'):
            return experiment._leaves_sut_running(config, stop_after_starting, keep)

    def test_only_the_last_repetition_keeps_the_sut(self):
        config = _config('PostgreSQL-1', repetitions=3)
        experiment = _experiment([config])
        self.assertFalse(self.decide(experiment, config))
        config.num_experiment_to_apply_done = 1
        self.assertFalse(self.decide(experiment, config))
        config.num_experiment_to_apply_done = 2
        self.assertTrue(self.decide(experiment, config))
        self.assertFalse(self.decide(experiment, config, keep=False))

    def test_start_keeps_at_once(self):
        config = _config('PostgreSQL-1', repetitions=3)
        self.assertTrue(self.decide(_experiment([config]), config, stop_after_starting=True))

    def test_a_waiting_configuration_gets_the_slot(self):
        """-ms 1 -rst nvme,cephcsi load: PostgreSQL-1 is stopped, PostgreSQL-2 starts."""
        first, second = _config('PostgreSQL-1'), _config('PostgreSQL-2')
        for caps in ({'max_sut': 1}, {'cluster_max_sut': 1}):
            with self.subTest(**caps):
                experiment = _experiment([first, second], **caps)
                self.assertFalse(self.decide(experiment, first))
                self.assertIn('PostgreSQL-2 waited', experiment.workload['sut_stopped']['PostgreSQL-1'])
        first.experiment_done = True
        self.assertTrue(self.decide(_experiment([first, second], max_sut=1), second))

    def test_a_configuration_that_never_started_waits(self):
        """Real status object: deployment_infos is empty until the SUT starts (cluster run 2026-10-19)."""
        from bexhoma.configurations.status import ComponentStatus
        first = _config('PostgreSQL-1')
        second = _config('PostgreSQL-2')
        second.appname, second.deployment_infos = 'bexhoma', {}
        second.status = ComponentStatus(second)
        self.assertFalse(second.status.sut_exists())
        self.assertFalse(self.decide(_experiment([first, second], max_sut=1), first))

    def test_without_a_cap_every_configuration_keeps_its_sut(self):
        first, second = _config('PostgreSQL-1'), _config('PostgreSQL-2')
        self.assertTrue(self.decide(_experiment([first, second]), first))

    def test_a_running_configuration_does_not_wait(self):
        first, second = _config('PostgreSQL-1'), _config('PostgreSQL-2', sut_exists=True)
        self.assertTrue(self.decide(_experiment([first, second], max_sut=2), first))

    def test_dbms_cap_counts_the_same_dbms_only(self):
        first = _config('PostgreSQL-1')
        mysql = _config('MySQL-1', docker='MySQL', max_sut_dbms=1)
        self.assertTrue(self.decide(_experiment([first, mysql]), first))
        postgres = _config('PostgreSQL-2', max_sut_dbms=1)
        self.assertFalse(self.decide(_experiment([first, postgres]), first))

    def test_start_stopped_for_a_waiting_configuration_does_not_restart(self):
        first, second = _config('Hardware-1', repetitions=3), _config('Hardware-2', repetitions=3)
        experiment = _experiment([first, second], max_sut=1)
        self.assertFalse(self.decide(experiment, first, stop_after_starting=True))
        self.assertEqual(first.num_experiment_to_apply_done + 1, first.num_experiment_to_apply)


class PrepareNextRepetitionTest(unittest.TestCase):
    """Between repetitions the SUT is not restarted directly, so the caps are checked again."""

    def test_resets_but_leaves_the_start_to_the_capped_main_loop(self):
        still_there = [True]     # the stopped SUT is gone at the second look
        config = SimpleNamespace(
            configuration='PostgreSQL-2', docker='PostgreSQL', experiment_done=False, max_sut_dbms=None,
            status=SimpleNamespace(sut_exists=lambda: bool(still_there) and still_there.pop()),
            experiment_dict={'benchmarker': []},
            benchmark_list=[], benchmark_list_template=['b1', 'b2'],
            benchmarking_parameters_list=[], benchmarking_parameters_list_template=[{}, {}],
            reset_sut=mock.Mock(), lifecycle=mock.Mock())
        experiment = _experiment([config], cluster_max_sut=1)
        experiment.wait = mock.Mock()
        with mock.patch('builtins.print'):
            experiment._prepare_next_repetition(config)
            # it does not block the loop until the stopped SUT is gone
            experiment.wait.assert_not_called()
            config.reset_sut.assert_called_once_with()
            config.lifecycle.start_sut.assert_not_called()
            self.assertEqual(config.benchmark_list, ['b1', 'b2'])
            self.assertEqual(experiment.client, 0)
            # while its old SUT is removed it already counts as waiting for a slot
            self.assertEqual(experiment._waits_for_slot(_config('PostgreSQL-1')), 'PostgreSQL-2')
            # the loop skips it while the SUT exists, then lets it start again
            self.assertTrue(experiment._sut_still_removing(config))
            self.assertFalse(experiment._sut_still_removing(config))
            self.assertFalse(config.sut_removing)
        # after removal it counts as waiting for a slot, like a configuration that has not started yet
        self.assertEqual(experiment._waits_for_slot(_config('PostgreSQL-1')), 'PostgreSQL-2')


class PrepareTestbedKeepSutTest(unittest.TestCase):
    """The resolved choice lands on the experiment and in its workload info."""

    def build(self, *argv):
        import tempfile
        from tests.test_resource_sweep import _SweepStubCluster
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        cluster = _SweepStubCluster(resultfolder=tmp_dir.name)
        captured = []
        with (
            mock.patch.object(tpch.clusters, 'Kubernetes', return_value=cluster),
            mock.patch.object(ExperimentBase, 'process', lambda experiment: captured.append(experiment)),
            mock.patch('builtins.print'),
        ):
            tpch.run(tpch.build_parser().parse_args([*argv, '-dbms', 'PostgreSQL']))
        return captured[0]

    def test_load_keeps_by_default(self):
        experiment = self.build('load')
        self.assertTrue(experiment.keep_sut)
        self.assertIn('kept running', experiment.workload['info'])

    def test_load_can_stop(self):
        experiment = self.build('load', '-ks', 'no')
        self.assertFalse(experiment.keep_sut)
        self.assertIn('stopped after loading', experiment.workload['info'])

    def test_run_stops_without_saying_so(self):
        experiment = self.build('run')
        self.assertFalse(experiment.keep_sut)
        self.assertNotIn('kept running', experiment.workload['info'])
        self.assertNotIn('stopped after', experiment.workload['info'])

    def test_skip_shutdown_keeps(self):
        self.assertTrue(self.build('run', '-ss').keep_sut)


class CatalogKeepSutTest(unittest.TestCase):
    """Agent runs stop their SUTs in every mode but start."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def argv(self, base, mode):
        experiment = copy.deepcopy(base)
        experiment['mode'] = mode
        return catalog_spec.build_argv(self.catalog, experiment)

    def test_every_mode_but_start_stops(self):
        for name, base in (('tpch', _TPCH_SPEC), ('ycsb', _YCSB_SPEC)):
            for mode in ('run', 'load'):
                with self.subTest(workload=name, mode=mode):
                    argv = self.argv(base, mode)
                    self.assertEqual(argv[argv.index('-ks') + 1], 'no')
            with self.subTest(workload=name, mode='start'):
                self.assertNotIn('-ks', self.argv(base, 'start'))

    def test_emitted_flag_parses_back(self):
        args = tpch.build_parser().parse_args(self.argv(_TPCH_SPEC, 'load'))
        self.assertEqual(args.keep_sut, 'no')


if __name__ == '__main__':
    unittest.main()

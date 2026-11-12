"""
The generic summary works for a benchmark that brings nothing but the generic schema.

Design goal (see :mod:`tests.test_no_benchmark_in_generic`): generic code knows only
what every benchmark has - connections with phase, job, pods and timings - and gets
everything else from the benchmark. This test is the counterpart to the name guard: a
*null benchmark*, whose evaluator returns tables with generic columns only and which
overrides no optional hook, must pass through
:meth:`bexhoma.benchmarks.base.Benchmark.show_summary` without an error, without an
empty section and without a failed test. Generic code that silently relies on a column,
an attribute or a parameter of one particular benchmark fails here.

The result folder is synthetic: a ``queries.config`` and a ``connections.config`` with
one connection of two parallel pods, holding only the keys bexhoma itself writes for
every benchmark.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import os
import tempfile
import unittest

import pandas as pd

from bexhoma.benchmarks.base import Benchmark
from bexhoma.evaluators.logger import LogEvaluator
from bexhoma.experiments.base import ExperimentBase

_CODE = '1'


def _write_result_folder(root: str) -> None:
    """The files of a finished experiment that the generic summary reads."""
    folder = os.path.join(root, _CODE)
    os.makedirs(folder)
    with open(os.path.join(folder, 'connections.config'), 'w', encoding='utf-8') as file:
        file.write(repr([_connection()]))
    with open(os.path.join(folder, 'queries.config'), 'w', encoding='utf-8') as file:
        file.write(repr({'name': 'Null Benchmark', 'type': 'null', 'queries': []}))


def _connection() -> dict:
    """A connection as every benchmark's ``connections.config`` has it, with no tool-specific key."""
    return {
        'name': 'DBMS-1-1-1', 'configuration': 'DBMS-1', 'phase': 'DBMS-1-1', 'job': 'DBMS-1-1-1',
        'time_loading': 10.0, 'time_schema': 1.0, 'time_generated': 2.0, 'time_ingested': 6.0, 'time_index': 1.0,
        'hostsystem': {'datadisk': 100, 'node': 'node-1'},
        'parameter': {'code': _CODE, 'numExperiment': 1, 'numBenchmark': 1, 'client': 1, 'dockerimage': 'dbms:1',
                      'parallelism': 2, 'num_worker': 0, 'connection_parameter': {}},
    }


class NullEvaluator(LogEvaluator):
    """Evaluator of the null benchmark: every summary table has generic columns only."""

    def get_summary_benchmark_per_connection(self) -> pd.DataFrame:
        df = self.get_connections_of_experiment()
        return df[['phase', 'job', 'pods', 'time_load']]

    def get_summary_benchmark_per_phase(self) -> pd.DataFrame:
        df = self.get_connections_of_experiment()
        return df.groupby('phase').agg(pods=('pods', 'first'), time_load=('time_load', 'max'))

    def get_summary_loading_per_run(self) -> pd.DataFrame:
        df = self.get_connections_of_experiment()
        return df.groupby('configuration').agg(time_load=('time_load', 'max'))


class NullBenchmark(Benchmark):
    """Benchmark that implements only what :class:`Benchmark` requires."""

    def create_evaluator(self, code: str, path: str, benchmark_run: int):
        return NullEvaluator(code=code, path=path, benchmark_run=benchmark_run, name=self.name)

    def configure_workload(self, experiment, parameter: dict) -> None:
        pass


class _Experiment:
    """Stand-in for the experiment: the parts of the summary that need a cluster or monitoring data are cut off."""

    num_tenants = 0

    def __init__(self):
        self._test_results = []
        self._runtime_test_results = []
        self.workload = {'workflow_planned': {}, 'monitoring_components': {}}
        for name in ('_record_test', '_record_skipped_test', '_print_test_summary'):
            setattr(self, name, getattr(ExperimentBase, name).__get__(self))

    def show_summary_header(self) -> tuple:
        return [], {}

    def show_summary_monitoring(self) -> None:
        pass

    def benchmarking_is_active(self) -> bool:
        return True

    def loading_is_active(self) -> bool:
        return True

    def test_workflow(self, workflow_actual: dict, workflow_planned: dict) -> bool:
        return True


class NullBenchmarkTest(unittest.TestCase):
    """A benchmark with generic data only gets a complete summary."""

    def summarize(self):
        with tempfile.TemporaryDirectory() as root:
            _write_result_folder(root)
            benchmark = NullBenchmark(name='null')
            benchmark.evaluator = benchmark.create_evaluator(code=_CODE, path=root, benchmark_run=1)
            experiment = _Experiment()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                benchmark.show_summary(experiment)
            return experiment, output.getvalue()

    def test_summary_runs_and_has_all_sections(self) -> None:
        _, text = self.summarize()
        for heading in ('### Workflow', '### Loading', '#### Per Run', '### Benchmarking',
                        '#### Per Connection', '#### Per Phase', '### Tests'):
            self.assertIn(heading, text)

    def test_tables_show_the_connections(self) -> None:
        _, text = self.summarize()
        self.assertIn('DBMS-1-1-1-1', text)
        self.assertIn('DBMS-1-1-1-2', text)

    def test_no_test_fails(self) -> None:
        experiment, text = self.summarize()
        self.assertTrue(experiment._test_results, 'no test was recorded')
        self.assertEqual([label for passed, label in experiment._test_results if passed is False], [])
        self.assertNotIn('TEST failed', text)

    def test_generic_connection_schema(self) -> None:
        """What generic code derives for every connection, without the benchmark's help."""
        with tempfile.TemporaryDirectory() as root:
            _write_result_folder(root)
            df = NullEvaluator(code=_CODE, path=root, benchmark_run=1).get_connections_of_experiment()
        self.assertEqual(len(df), 2)
        for column in ('code', 'connection', 'configuration', 'phase', 'job', 'experiment_run', 'benchmark_run',
                       'client', 'pods', 'time_load', 'time_preload', 'time_generate', 'time_ingest', 'time_postload'):
            self.assertIn(column, df.columns)


if __name__ == '__main__':
    unittest.main()

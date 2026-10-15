"""
Unit tests for the workload description of load-only experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest

from bexhoma.benchmarks.tpch import TPCH


class _FakeExperiment:
    """The parts of an experiment that ``TPCH.configure_workload()`` touches."""

    def __init__(self) -> None:
        self.workload = {}
        self.benchmarking_active = True
        self.loading_active = False
        self.active_queries = None

    def set_queryfile(self, queryfile: str) -> None:
        self.queryfile = queryfile

    def set_workload(self, **kwargs) -> None:
        self.workload = {**self.workload, **kwargs}

    def set_experiment(self, **kwargs) -> None:
        pass

    def loading_is_active(self) -> bool:
        return self.loading_active

    def benchmarking_is_active(self) -> bool:
        return self.benchmarking_active


def _configure(mode: str) -> dict:
    parameter = dict(
        mode=mode, recreate_parameter=False, shuffle_queries=False, limit_import_table='',
        init_indexes=False, init_constraints=False, init_statistics=False, init_columns=False,
        datatransfer=False, num_loading_split='1', num_refresh_streams=0, num_refresh_stream_offset=0,
        duckdb_force_execution=False, verbose_explain=False, store_explain=False, timeout=600,
    )
    experiment = _FakeExperiment()
    TPCH(SF='1').configure_workload(experiment, parameter)
    return experiment.workload


class LoadModeWorkloadTest(unittest.TestCase):
    """Load mode neither claims a benchmark run nor inherits the query template's intro."""

    def test_load_mode(self) -> None:
        workload = _configure('load')
        self.assertIn("TPC-H (SF=1) data is loaded.", workload['info'])
        self.assertNotIn("benchmark is executed", workload['info'])
        self.assertEqual(workload['intro'], 'Load data and do not run a benchmark.')

    def test_run_mode(self) -> None:
        workload = _configure('run')
        self.assertIn("TPC-H (SF=1) data is loaded and benchmark is executed.", workload['info'])
        self.assertNotIn('intro', workload)


if __name__ == '__main__':
    unittest.main()

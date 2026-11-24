"""
Benchmark-Experiment-Host-Manager | tests
Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.

Purpose: A requested post-load step (-xii, -xic, -xis) that a DBMS has no
script for is skipped with a notice at the start (DDL plan item 13b).
"""
import ast
import contextlib
import io
import os
import unittest

from bexhoma.experiments.base import ExperimentBase

from .test_reset_scripts import _run_script

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as _file:
    _VOLUMES = ast.literal_eval(_file.read())['volumes']


def _notices(script: str, *argv: str) -> tuple:
    """Run an entry script up to ``process()`` and return the notices and their output."""
    folder, configurations = _run_script(script, *argv)
    experiment = configurations[0].experiment
    experiment.cluster.experiments_configfolder = folder
    for config in configurations:
        # the harness knows every volume with empty script lists; use the real ones
        config.indexscript = _VOLUMES[experiment.volume]['initscripts'][config.indexing]
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        skipped = ExperimentBase.notice_missing_post_load_scripts(experiment)
    return {c.docker: skipped.get(c.configuration) for c in configurations}, out.getvalue()


class PostLoadNoticeTest(unittest.TestCase):

    def test_tpch_clickhouse_skips_all_three_steps(self):
        skipped, output = _notices('tpch.py', '-xii', '-xic', '-xis')
        self.assertEqual(skipped['ClickHouse'], ['indexes', 'constraints', 'statistics'])
        self.assertIsNone(skipped['PostgreSQL'])
        self.assertIn('no script for indexes, constraints, statistics in this DBMS, skipped', output)

    def test_no_notice_without_post_load_steps(self):
        skipped, output = _notices('tpch.py')
        self.assertEqual(set(skipped.values()), {None})
        self.assertEqual(output, '')

    def test_ssb_flat_has_no_constraints_step(self):
        skipped, _ = _notices('ssb.py', '-xsv', 'flat', '-xic')
        self.assertTrue(all('constraints' not in (steps or []) for steps in skipped.values()))


if __name__ == '__main__':
    unittest.main()

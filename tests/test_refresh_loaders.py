"""
Tests for the TPC-H refresh stream of ClickHouse and ClickHouseCluster, and for the refresh
job each DBMS declares in ``cluster.config``.

They cannot run the loader against a ClickHouse server; they check that the script parses
and states what the docs say, and that the job templates are consistent with each other.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os
import shutil
import subprocess
import unittest

import yaml

from bexhoma import system_descriptors as sd

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOADER = os.path.join(_REPO, 'images', 'tpch_refresh', 'loader_clickhouse', 'loader.sh')
_K8S = os.path.join(_REPO, 'k8s')


def _bash_works() -> bool:
    if not shutil.which('bash'):
        return False
    try:
        return subprocess.run(['bash', '-c', 'true'], capture_output=True, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _template(name: str) -> dict:
    with open(os.path.join(_K8S, f'jobtemplate-benchmarking-tpch-refresh-{name}.yml'), encoding='utf-8') as file:
        return yaml.safe_load(file)


def _env(container: dict) -> dict:
    return {entry['name']: entry['value'] for entry in container['env']}


class ClickHouseLoaderTest(unittest.TestCase):

    @unittest.skipUnless(_bash_works(), 'no working bash (not installed, or a WSL launcher without a distribution)')
    def test_script_parses(self) -> None:
        result = subprocess.run(['bash', '-n', _LOADER], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_script_does_what_the_readme_says(self) -> None:
        with open(_LOADER, encoding='utf-8') as file:
            script = file.read()
        self.assertIn('INSERT INTO $TABLE FORMAT CSV', script)
        self.assertIn('DELETE FROM lineitem$DELETE_SUFFIX WHERE l_orderkey IN', script)
        self.assertIn('DELETE FROM orders$DELETE_SUFFIX WHERE o_orderkey IN', script)
        # a Distributed table cannot be deleted from: the cluster deletes on the local tables of each shard,
        # the coordinator has none (ON CLUSTER would look them up on the coordinator and fail)
        self.assertIn('DELETE_SUFFIX="_local"', script)
        self.assertIn('FROM system.clusters WHERE cluster = ', script)
        self.assertIn('for DELETE_HOST in $DELETE_HOSTS', script)
        self.assertNotIn('ON_CLUSTER', script)
        # lineitem is deleted before orders, as in the other loaders
        self.assertLess(script.index('DELETE FROM lineitem'), script.index('DELETE FROM orders'))
        # a failure is reported, not swallowed
        self.assertIn('exit 1', script)
        for marker in ('BEXHOMA_DURATION:', 'BEXHOMA_START:', 'BEXHOMA_END:'):
            self.assertIn(marker, script)

    def test_dockerfile_defaults_match_the_script(self) -> None:
        with open(os.path.join(os.path.dirname(_LOADER), 'Dockerfile'), encoding='utf-8') as file:
            dockerfile = file.read()
        for variable in ('CLICKHOUSE_PORT=9000', 'BEXHOMA_DATABASE=default', 'BEXHOMA_CLICKHOUSE_CLUSTER=""',
                         'TPCH_REFRESH_STREAMS=1', 'STORE_RAW_DATA=1'):
            self.assertIn(variable, dockerfile)


class ClickHouseTemplatesTest(unittest.TestCase):

    def test_single_node_template(self) -> None:
        job = _template('ClickHouse')
        main = job['spec']['template']['spec']['containers'][0]
        self.assertEqual(main['image'], 'bexhoma/loader_tpch_refresh_clickhouse:BEXHOMA_PACKAGE_VERSION')
        self.assertEqual(job['spec']['backoffLimit'], 0)   # a retry would insert RF1 twice
        env = _env(main)
        self.assertEqual(env['BEXHOMA_BENCHMARK_RUN'], '2')
        self.assertNotIn('BEXHOMA_CLICKHOUSE_CLUSTER', env)
        for variable in ('BEXHOMA_USER', 'BEXHOMA_PASSWORD', 'BEXHOMA_VOLUME'):
            self.assertNotIn(variable, env)

    def test_cluster_template_differs_by_the_cluster_only(self) -> None:
        single, cluster = _template('ClickHouse'), _template('ClickHouseCluster')
        main = cluster['spec']['template']['spec']['containers'][0]
        self.assertEqual(_env(main)['BEXHOMA_CLICKHOUSE_CLUSTER'], 'bexhoma')
        del main['env'][[e['name'] for e in main['env']].index('BEXHOMA_CLICKHOUSE_CLUSTER')]
        self.assertEqual(single, cluster)


class DeclaredJobsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dockers = sd.load_dockers(os.path.join(_REPO, 'k8s-cluster.config'))

    def test_every_tpch_dbms_has_an_existing_job(self) -> None:
        for docker in sd.compatible_dockers(self.dockers, 'tpch'):
            with self.subTest(docker=docker):
                template = sd.refresh_template(self.dockers, [docker], 'tpch')
                self.assertTrue(os.path.isfile(os.path.join(_K8S, template)), template)

    def test_clickhouse_uses_its_own_job_and_postgres_protocol_systems_the_postgres_one(self) -> None:
        job = lambda docker: sd.refresh_template(self.dockers, [docker], 'tpch').split('refresh-')[1]
        self.assertEqual(job('ClickHouse'), 'ClickHouse.yml')
        self.assertEqual(job('ClickHouseCluster'), 'ClickHouseCluster.yml')
        for docker in ('CedarDB', 'Citus', 'DatabaseService', 'PgDuckDB'):
            self.assertEqual(job(docker), 'PostgreSQL.yml', docker)

    def test_dbms_with_different_jobs_cannot_share_a_run(self) -> None:
        with self.assertRaises(sd.IncompatibleBenchmark):
            sd.refresh_template(self.dockers, ['PostgreSQL', 'ClickHouse'], 'tpch')


if __name__ == '__main__':
    unittest.main()

"""
Tests for the DBMS-specific behaviour that the cluster configuration declares
(instead of Python code naming a DBMS):

* ``monitor.<component>.blackbox_database`` -- the database a blackbox probe connects to;
* ``initial_cluster`` -- the members of a component that bootstraps as a cluster.

The expected strings are what the code produced while it named the DBMS itself.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import os
import unittest

from bexhoma.configurations.lifecycle import blackbox_targets, initial_cluster_members

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TARGET = 'user@localhost:5432/{database}?sslmode=disable'


def _dockers() -> dict:
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as file:
        return ast.literal_eval(file.read())['dockers']


class BlackboxTargetsTest(unittest.TestCase):

    monitoring = {'blackbox': True, 'blackbox_target': _TARGET, 'blackbox_database': 'main'}

    def test_one_target_without_tenants(self) -> None:
        self.assertEqual(blackbox_targets(self.monitoring, '', 0),
                         "\n          - user@localhost:5432/main?sslmode=disable\n")

    def test_tenants_per_schema_add_nothing(self) -> None:
        self.assertEqual(blackbox_targets(self.monitoring, 'schema', 3), blackbox_targets(self.monitoring, '', 0))

    def test_tenant_databases_add_a_target_each(self) -> None:
        self.assertEqual(
            blackbox_targets(self.monitoring, 'database', 2),
            "\n          - user@localhost:5432/main?sslmode=disable\n"
            "          - user@localhost:5432/tenant_0?sslmode=disable\n"
            "          - user@localhost:5432/tenant_1?sslmode=disable")

    def test_database_is_required(self) -> None:
        with self.assertRaises(KeyError):
            blackbox_targets({'blackbox_target': _TARGET}, '', 0)

    def test_every_blackbox_dbms_names_its_database(self) -> None:
        for name, docker in _dockers().items():
            for component, monitoring in (docker.get('monitor') or {}).items():
                if monitoring.get('blackbox'):
                    with self.subTest(docker=name, component=component):
                        self.assertTrue(monitoring.get('blackbox_database'))
                        self.assertIn('{database}', monitoring['blackbox_target'])


class InitialClusterTest(unittest.TestCase):

    def test_members(self) -> None:
        self.assertEqual(initial_cluster_members('x-pd', 3, 2380),
                         'x-pd-0=http://x-pd-0.x-pd:2380,x-pd-1=http://x-pd-1.x-pd:2380,x-pd-2=http://x-pd-2.x-pd:2380')

    def test_scheme_and_empty(self) -> None:
        self.assertEqual(initial_cluster_members('n', 1, 1, scheme='https'), 'n-0=https://n-0.n:1')
        self.assertEqual(initial_cluster_members('n', 0, 1), '')

    def test_declared_clusters_are_complete(self) -> None:
        for name, docker in _dockers().items():
            declaration = docker.get('initial_cluster')
            if declaration:
                with self.subTest(docker=name):
                    self.assertEqual(set(declaration) - {'scheme'}, {'component', 'port', 'env'})
                    self.assertIsInstance(declaration['port'], int)


if __name__ == '__main__':
    unittest.main()

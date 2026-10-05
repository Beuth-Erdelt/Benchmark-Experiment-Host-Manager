"""
Regression tests for the tpch catalog's ``loading.pods`` default.

The catalog declares ``default: 8`` for ``workloads.tpch.loading.pods``, while
``tpch.py``'s own ``-nlp`` default is 1 -- so the argv builder must emit the
catalog default explicitly when an experiment omits ``pods``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import unittest

from bexhoma import spec as catalog_spec

_CATALOG_FILE = 'contracts/contract_catalog.yml'

_BASE_SPEC = {
    'mode': 'run',
    'title': 'loading pods default',
    'hypothesis': 'loading.pods falls back to the catalog default',
    'discriminates': ['system'],
    'workload': {
        'name': 'tpch',
        'params': {'scaling_factor': 10},
        'rounds': [1],
        'repetitions': 1,
    },
    'loading': {'threads': 1},
    'systems': [{'name': 'PostgreSQL', 'profile': 'analytical-ssd'}],
    'resources': {
        'cpu': {'request': 16, 'limit': 16},
        'memory': {'request': '64G', 'limit': '64G'},
        'storage': {'size': '50Gi'},
    },
    'placement': {'sut': 'cl-worker36'},
}


def _flag_value(argv, flag):
    return argv[argv.index(flag) + 1]


class LoadingPodsDefaultTest(unittest.TestCase):

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def test_catalog_declares_default_8(self):
        pods = self.catalog['workloads']['tpch']['loading']['pods']
        self.assertEqual(pods['default'], 8)

    def test_omitted_pods_emits_catalog_default(self):
        argv = catalog_spec.build_argv(self.catalog, copy.deepcopy(_BASE_SPEC))
        self.assertEqual(_flag_value(argv, '-nlp'), '8')

    def test_explicit_pods_wins(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['loading']['pods'] = 2
        argv = catalog_spec.build_argv(self.catalog, spec)
        self.assertEqual(_flag_value(argv, '-nlp'), '2')


if __name__ == '__main__':
    unittest.main()

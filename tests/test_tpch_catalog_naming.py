"""
Regression tests for resource-sweep configuration naming.

A ``resources:`` sweep must give every swept cell a *unique* configuration
name, so its SUT pods/PVCs/services don't collide and ``--set`` overrides land
on the right cell. The name is the 1-based cell position (``PostgreSQL-1``,
``PostgreSQL-2`` ...), never a single resource value: two cells can share a
memory request while differing in memory limit or CPU, and a value-based name
(the old ``{docker}-{memory_request}`` scheme) collapsed them onto one name.

Covers both halves of the translator:

* :func:`bexhoma.spec.build_argv` -> :func:`bexhoma.experiments.tpch_catalog.build_tpch_argv`,
  which predicts each cell's name for its scoped ``--set`` operations;
* ``tpch.py``'s own ``_resource_cells`` loop, which must name the same cells
  identically.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import re
import unittest

import tpch
from bexhoma import spec as catalog_spec

_CATALOG_FILE = 'contracts/contract_catalog.yml'

#: Minimal catalog-driven experiment spec; individual tests deep-copy this and
#: overwrite ``resources`` to exercise a particular sweep shape.
_BASE_SPEC = {
    'mode': 'run',
    'title': 'resource-sweep naming regression',
    'hypothesis': 'swept cells get unique, position-based names',
    'discriminates': ['system'],
    'workload': {
        'name': 'tpch',
        'params': {'scaling_factor': 10},
        'rounds': [1],
        'repetitions': 1,
    },
    'loading': {'pods': 1, 'threads': 1},
    'systems': [
        {'name': 'PostgreSQL', 'profile': 'analytical-ssd'},
        {'name': 'PgDuckDB', 'profile': 'analytical-ssd'},
    ],
    'placement': {'sut': 'cl-worker36'},
}

_SET_SCOPE_RE = re.compile(r'@([A-Za-z0-9-]+)\.container')


def _tpch_cell_names(argv):
    """Configuration names ``tpch.py``'s own resource-sweep loop derives from ``argv``."""
    args = tpch.build_parser().parse_args(argv)

    def as_list(value):
        return [entry for entry in str(value).split(',') if entry]

    cells = tpch._resource_cells(
        as_list(args.request_cpu), as_list(args.limit_cpu),
        as_list(args.request_ram), as_list(args.limit_ram),
    )
    names = []
    for docker in ('PostgreSQL', 'PgDuckDB'):
        for cell_number, _ in enumerate(cells, start=1):
            names.append(f'{docker}-{cell_number}' if len(cells) > 1 else '')
    return names, len(cells)


def _catalog_set_scopes(argv):
    """Distinct ``@CONFIG`` scopes the catalog builder attached to ``--set`` ops."""
    return sorted({
        match.group(1)
        for token in argv
        for match in [_SET_SCOPE_RE.search(token)]
        if match
    })


class ResourceSweepNamingTest(unittest.TestCase):
    """Every swept cell gets a unique, position-based configuration name."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _argv(self, resources):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['resources'] = resources
        return catalog_spec.build_argv(self.catalog, spec)

    def test_memory_sweep_names_are_positional_and_unique(self):
        argv = self._argv({
            'cpu': {'request': 16, 'limit': 16},
            'memory': [
                {'request': '64G', 'limit': '64G'},
                {'request': '32G', 'limit': '32G'},
                {'request': '16G', 'limit': '16G'},
            ],
            'storage': {'size': '50Gi'},
        })
        catalog_scopes = _catalog_set_scopes(argv)
        tpch_names, num_cells = _tpch_cell_names(argv)

        self.assertEqual(num_cells, 3)
        self.assertEqual(
            catalog_scopes,
            ['PgDuckDB-1', 'PgDuckDB-2', 'PgDuckDB-3',
             'PostgreSQL-1', 'PostgreSQL-2', 'PostgreSQL-3'],
        )
        self.assertEqual(sorted(tpch_names), catalog_scopes)

    def test_constant_memory_request_swept_cpu_does_not_collide(self):
        """The old ``{docker}-{memory_request}`` scheme collapsed this to
        three identical ``PostgreSQL-64G`` configs — the reported bug."""
        argv = self._argv({
            'cpu': [
                {'request': 16, 'limit': 16},
                {'request': 32, 'limit': 32},
                {'request': 64, 'limit': 64},
            ],
            'memory': {'request': '64G', 'limit': '64G'},
            'storage': {'size': '50Gi'},
        })
        catalog_scopes = _catalog_set_scopes(argv)
        tpch_names, num_cells = _tpch_cell_names(argv)

        self.assertEqual(num_cells, 3)
        self.assertEqual(len(set(tpch_names)), 6)
        self.assertNotIn('PostgreSQL-64G', tpch_names)
        self.assertEqual(sorted(tpch_names), catalog_scopes)

    def test_single_cell_stays_unscoped(self):
        argv = self._argv({
            'cpu': {'request': 16, 'limit': 16},
            'memory': {'request': '64G', 'limit': '64G'},
            'storage': {'size': '50Gi'},
        })
        self.assertEqual(_catalog_set_scopes(argv), [])
        tpch_names, num_cells = _tpch_cell_names(argv)
        self.assertEqual(num_cells, 1)
        self.assertEqual(tpch_names, ['', ''])


if __name__ == '__main__':
    unittest.main()

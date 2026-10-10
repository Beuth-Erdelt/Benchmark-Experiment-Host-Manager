"""
Regression tests for PgDuckDB's own ``duckdb.*`` knobs.

PgDuckDB's ``analytical-ssd`` profile refs PostgreSQL's for parity and adds
``derive:`` entries for ``duckdb.max_memory`` and ``duckdb.threads``, which
PostgreSQL does not have. Covers the ref + local derive merge in
:func:`bexhoma.spec.resolve_system`, and that the dotted GUC names survive
``--set`` parsing and manifest patching.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import unittest

from bexhoma import spec as catalog_spec
from bexhoma.configurations.manifest import ensure_arg_pairs
from bexhoma.experiments.base import parse_set_arg
from bexhoma.experiments.tpch_catalog import format_postgres_memory

_CATALOG_FILE = 'contracts/contract_catalog.yml'

_RESOURCES = {'memory_limit': '64Gi', 'cpu_limit': 16, 'storage_class': None, 'scaling_factor': 10}


class PgDuckDBKnobsTest(unittest.TestCase):
    """PgDuckDB resolves PostgreSQL's profile plus its own duckdb.* knobs."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _resolve(self, system_spec):
        resolved = catalog_spec.resolve_system(
            self.catalog, system_spec, _RESOURCES, memory_formatter=format_postgres_memory)
        return {name: knob.value for name, knob in resolved.knobs.items()}

    def test_ref_profile_adds_duckdb_knobs(self):
        knobs = self._resolve({'name': 'PgDuckDB', 'profile': 'analytical-ssd'})
        self.assertEqual(knobs['duckdb.max_memory'], '16384MB')
        self.assertEqual(knobs['duckdb.threads'], 16)
        self.assertIsInstance(knobs['duckdb.threads'], int)

    def test_ref_profile_keeps_parity_with_postgresql(self):
        postgres = self._resolve({'name': 'PostgreSQL', 'profile': 'analytical-ssd'})
        pgduckdb = self._resolve({'name': 'PgDuckDB', 'profile': 'analytical-ssd'})
        self.assertEqual({name: pgduckdb[name] for name in postgres}, postgres)
        self.assertNotIn('duckdb.max_memory', postgres)

    def test_override_beats_derived_duckdb_knob(self):
        knobs = self._resolve({'name': 'PgDuckDB', 'profile': 'analytical-ssd',
                               'override': {'duckdb.max_memory': '8GB'}})
        self.assertEqual(knobs['duckdb.max_memory'], '8GB')

    def test_dotted_guc_survives_set_and_patch(self):
        selector, value = parse_set_arg(
            'deployment[bexhoma-deployment-pg-duck].container[dbms].duckdb.max_memory=16384MB')
        self.assertEqual(selector['param'], 'duckdb.max_memory')
        self.assertEqual(selector['container'], 'dbms')
        args = ensure_arg_pairs(['-c', 'shared_preload_libraries=pg_duckdb'], [(selector['param'], value)])
        self.assertEqual(args[-2:], ['-c', 'duckdb.max_memory=16384MB'])


if __name__ == '__main__':
    unittest.main()

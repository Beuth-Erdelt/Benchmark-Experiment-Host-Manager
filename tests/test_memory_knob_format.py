"""
Tests for ``catalog_concepts.memory_knob_format`` (catalog contract 1.8.0).

A ``type: memory`` knob takes the system's own units (``40GB``) or a
Kubernetes quantity (``40Gi``), which the resolver rewrites in the system's
units before it reaches the DBMS. These tests check that:

* native values and bare integers pass through unchanged;
* Kubernetes quantities are converted, for overrides and profile knobs alike;
* anything else is rejected as a ``SpecError`` instead of reaching PostgreSQL;
* PgDuckDB inherits PostgreSQL's ``memory_units`` via ``extends:``;
* a ``systems[].override`` of ``40Gi`` ends up as a ``40960MB`` ``--set`` patch.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import unittest

from bexhoma import spec as catalog_spec
from bexhoma.experiments.tpch_catalog import format_postgres_memory
from tests.test_ycsb_catalog import _BASE_SPEC, _CATALOG_FILE

_POSTGRES_UNITS = ['B', 'kB', 'MB', 'GB', 'TB']
_RESOURCES = {'memory_limit': '128Gi', 'cpu_limit': 16, 'storage_class': None}


def _normalize(value):
    return catalog_spec.normalize_memory_knob(
        'shared_buffers', value, _POSTGRES_UNITS, format_postgres_memory
    )


class NormalizeMemoryKnobTest(unittest.TestCase):
    """``normalize_memory_knob`` accepts the three documented forms only."""

    def test_native_units_pass_unchanged(self):
        for value in ('40GB', '512MB', '64kB', '1TB', '8192B'):
            self.assertEqual(_normalize(value), value)

    def test_bare_integers_pass_unchanged(self):
        self.assertEqual(_normalize(16384), 16384)
        self.assertEqual(_normalize('16384'), '16384')

    def test_kubernetes_quantities_are_converted(self):
        self.assertEqual(_normalize('40Gi'), '40960MB')
        self.assertEqual(_normalize('512Mi'), '512MB')
        self.assertEqual(_normalize('1.5Gi'), '1536MB')
        self.assertEqual(_normalize('4G'), '3814MB')

    def test_other_spellings_are_rejected(self):
        for value in ('40gb', '40 GB', '1.5GB', '40PB', 'lots', True, '40Gb'):
            with self.subTest(value=value), self.assertRaises(catalog_spec.SpecError):
                _normalize(value)


class ResolveSystemMemoryKnobTest(unittest.TestCase):
    """``resolve_system`` applies the format to overrides and inherited systems."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def _knob(self, system_spec, name='shared_buffers'):
        resolved = catalog_spec.resolve_system(
            self.catalog, system_spec, _RESOURCES, memory_formatter=format_postgres_memory
        )
        return resolved.knobs[name].value

    def test_derived_value_is_in_postgres_units(self):
        self.assertEqual(self._knob({'name': 'PostgreSQL', 'profile': 'analytical-ssd'}), '40960MB')

    def test_kubernetes_override_is_converted(self):
        spec = {'name': 'PostgreSQL', 'override': {'shared_buffers': '40Gi'}}
        self.assertEqual(self._knob(spec), '40960MB')

    def test_native_override_is_kept(self):
        spec = {'name': 'PostgreSQL', 'override': {'shared_buffers': '40GB'}}
        self.assertEqual(self._knob(spec), '40GB')

    def test_invalid_override_is_rejected(self):
        spec = {'name': 'PostgreSQL', 'override': {'shared_buffers': '40gb'}}
        with self.assertRaises(catalog_spec.SpecError):
            self._knob(spec)

    def test_pgduckdb_inherits_memory_units(self):
        spec = {'name': 'PgDuckDB', 'override': {'work_mem': '1GB', 'shared_buffers': '8Gi'}}
        self.assertEqual(self._knob(spec, 'work_mem'), '1GB')
        self.assertEqual(self._knob(spec), '8192MB')

    def test_non_memory_knobs_are_untouched(self):
        spec = {'name': 'PostgreSQL', 'override': {'max_connections': 100}}
        self.assertEqual(self._knob(spec, 'max_connections'), 100)


class BuildArgvMemoryKnobTest(unittest.TestCase):
    """The converted value is what reaches the ``--set`` patch."""

    def test_override_in_gi_becomes_mb_patch(self):
        catalog = catalog_spec.load_catalog(_CATALOG_FILE)
        spec = copy.deepcopy(_BASE_SPEC)
        spec['systems'] = [{'name': 'PostgreSQL', 'override': {'shared_buffers': '40Gi'}}]
        argv = catalog_spec.build_argv(catalog, spec)
        set_patches = [argv[i + 1] for i, tok in enumerate(argv) if tok == '--set']
        self.assertIn(
            'deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=40960MB',
            set_patches,
        )


if __name__ == '__main__':
    unittest.main()

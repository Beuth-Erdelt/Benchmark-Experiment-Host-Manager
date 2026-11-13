"""
A collector refuses a monitoring component the experiments do not have.

Asking :class:`bexhoma.collectors.base.CollectorBase` for an unknown component (the
collector notebooks asked for ``'stream'`` long after it was renamed ``'benchmarking'``)
used to return an empty DataFrame, and every cell that used the result failed later
with an unrelated ``KeyError``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os
import tempfile
import unittest

from bexhoma.collectors.base import CollectorBase


def _collector(root: str, components_per_code: dict) -> CollectorBase:
    """A collector over synthetic experiments that only have a ``queries.config``."""
    for code, components in components_per_code.items():
        os.makedirs(os.path.join(root, code))
        with open(os.path.join(root, code, 'queries.config'), 'w', encoding='utf-8') as file:
            file.write(repr({'name': 'x', 'monitoring_components': {c: c for c in components}}))
    collector = object.__new__(CollectorBase)
    collector.path = root
    collector.codes = list(components_per_code)
    collector.with_monitoring = True
    return collector


class ComponentCheckTest(unittest.TestCase):

    def test_known_components_are_the_base_ones_and_those_of_the_experiments(self):
        with tempfile.TemporaryDirectory() as root:
            collector = _collector(root, {'1': ['loading', 'benchmarking'], '2': ['datagenerator']})
            self.assertEqual(collector.known_components(),
                             ['benchmarker', 'benchmarking', 'datagenerator', 'loader', 'loading'])

    def test_an_unknown_component_is_refused_with_the_known_ones(self):
        with tempfile.TemporaryDirectory() as root:
            collector = _collector(root, {'1': []})
            with self.assertRaises(ValueError) as raised:
                collector._check_component('stream')
            self.assertIn("'stream'", str(raised.exception))
            self.assertIn('benchmarking', str(raised.exception))

    def test_the_public_methods_check(self):
        with tempfile.TemporaryDirectory() as root:
            collector = _collector(root, {'1': []})
            with self.assertRaises(ValueError):
                collector.get_monitoring_aggregated_per_phase('stream')
            with self.assertRaises(ValueError):
                collector.get_monitoring_timeseries_all('total_cpu_memory', component='stream')

    def test_a_known_component_passes(self):
        with tempfile.TemporaryDirectory() as root:
            collector = _collector(root, {'1': ['datagenerator']})
            collector._check_component('benchmarking')
            collector._check_component('datagenerator')

    def test_without_monitoring_nothing_is_checked(self):
        with tempfile.TemporaryDirectory() as root:
            collector = _collector(root, {'1': []})
            collector.with_monitoring = False
            collector._check_component('stream')
            self.assertTrue(collector.get_monitoring_aggregated_per_phase('stream').empty)


if __name__ == '__main__':
    unittest.main()

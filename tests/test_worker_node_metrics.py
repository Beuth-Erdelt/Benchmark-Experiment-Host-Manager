"""
Tests for the node-level metrics of workers spread over several nodes (#604).

Covers ``worker_host_values()`` (the ``{host}`` and ``{gpuid}`` values of a
worker component) and the node metrics in ``k8s-cluster.config``: they match
``{host}`` as a regex and keep the cores of different nodes apart, so a
query over several nodes still returns one series.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

from bexhoma.configurations.metrics import worker_host_values

_REPO = Path(__file__).resolve().parent.parent
_NODE_METRICS = ('core_variance', 'max_core_util', 'io_wait_pct', 'io_wait_total')


class WorkerHostValuesTest(unittest.TestCase):

    def test_no_workers_fall_back_to_sut(self):
        self.assertEqual(worker_host_values([], 'sut-node', 'g0'), ('sut-node', 'g0'))
        self.assertEqual(worker_host_values([{'node': ''}], 'sut-node', 'g0'), ('sut-node', 'g0'))

    def test_single_node_is_plain_name(self):
        workers = [{'node': 'n1', 'GPUIDs': []}, {'node': 'n1', 'GPUIDs': []}]
        self.assertEqual(worker_host_values(workers, 'sut-node', 'g0'), ('n1', ''))

    def test_several_nodes_give_alternation_in_order(self):
        workers = [{'node': 'n2', 'GPUIDs': ['a']}, {'node': 'n1', 'GPUIDs': ['b']},
                   {'node': 'n2', 'GPUIDs': ['a']}]
        self.assertEqual(worker_host_values(workers, 'sut-node', ''), ('(n2|n1)', 'a|b'))


class NodeMetricQueriesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = ast.literal_eval((_REPO / "k8s-cluster.config").read_text(encoding="utf-8"))
        cls.metrics = config['credentials']['k8s']['monitor']['metrics']

    def test_host_matched_as_regex(self):
        for name in _NODE_METRICS:
            query = self.metrics[name]['query']
            self.assertIn('instance=~"{host}"', query, name)
            self.assertNotIn('instance="{host}"', query, name)

    def test_cores_grouped_per_node(self):
        for name in ('core_variance', 'max_core_util'):
            query = self.metrics[name]['query']
            self.assertNotIn('by (exported_cpu)', query, name)
            self.assertIn('by (instance, exported_cpu)', query, name)

    def test_io_wait_share_pooled_over_nodes(self):
        query = self.metrics['io_wait_pct']['query']
        self.assertNotIn('by (instance)', query)

    def test_queries_format_with_several_nodes(self):
        for name in _NODE_METRICS:
            query = self.metrics[name]['query'].format(host='(n1|n2)')
            self.assertIn('instance=~"(n1|n2)"', query, name)


_AGGREGATIONS = ('sum', 'max', 'min', 'avg', 'count')
_NOT_METRICS = set(_AGGREGATIONS) | {
    'rate', 'irate', 'increase', 'deriv', 'avg_over_time', 'max_over_time', 'min_over_time',
    'time', 'timestamp', 'by', 'without', 'on', 'ignoring', 'group_left', 'group_right',
    'and', 'or', 'unless'}


def _blank(text: str, pattern: str) -> str:
    """Replace each match of ``pattern`` by spaces, keeping positions."""
    return re.sub(pattern, lambda m: ' ' * len(m.group(0)), text)


def _closing(text: str, start: int) -> int:
    """Position of the parenthesis closing the one at ``start``."""
    depth = 0
    for i in range(start, len(text)):
        depth += {'(': 1, ')': -1}.get(text[i], 0)
        if depth == 0:
            return i
    raise ValueError(f"unbalanced: {text}")


def unaggregated_selectors(query: str) -> list:
    """Metric names of ``query`` that no aggregation without grouping encloses.

    Such a selector can return one series per label set, so the query is not
    a single time series.
    """
    # selectors, ranges and strings carry no metric names
    q = _blank(query.replace('{{', '{').replace('}}', '}'), r'"[^"]*"')
    q = _blank(q, r'\{[^}]*\}|\[[^\]]*\]')
    spans = []
    for m in re.finditer(r'\b(' + '|'.join(_AGGREGATIONS) + r')\s*(\b(by|without)\s*\([^)]*\)\s*)?\(', q):
        end = _closing(q, m.end() - 1)
        grouped = m.group(2) or re.match(r'\s*(by|without)\b', q[end + 1:])
        if not grouped:
            spans.append((m.start(), end))
    # label lists of by / on / group_left hold label names, not metrics
    q = _blank(q, r'\b(by|without|on|ignoring|group_left|group_right)\s*\([^)]*\)')
    names = []
    for m in re.finditer(r'\b[a-zA-Z_:][\w:]*', q):
        if m.group(0) in _NOT_METRICS:
            continue
        if not any(a <= m.start() <= b for a, b in spans):
            names.append(m.group(0))
    return names


class SingleSeriesQueriesTest(unittest.TestCase):
    """Every query in k8s-cluster.config returns a single time series."""

    def test_helper(self):
        self.assertEqual(unaggregated_selectors('rate(m[5m])'), ['m'])
        self.assertEqual(unaggregated_selectors('sum by (pod) (m)'), ['m'])
        self.assertEqual(unaggregated_selectors('max(m) by (pod)'), ['m'])
        self.assertEqual(unaggregated_selectors('a / sum(b)'), ['a'])
        self.assertEqual(unaggregated_selectors('sum(max(m{{x="1"}}) by (instance))/1024'), [])
        self.assertEqual(unaggregated_selectors('100 * max(sum by (instance, c) (rate(m[5m])))'), [])

    def test_all_queries_aggregated(self):
        config = ast.literal_eval((_REPO / "k8s-cluster.config").read_text(encoding="utf-8"))
        monitor = config['credentials']['k8s']['monitor']
        sets = {'metrics': monitor['metrics']}
        sets.update({k: v['metrics'] for k, v in monitor.items()
                     if isinstance(v, dict) and isinstance(v.get('metrics'), dict)})
        for set_name, metrics in sets.items():
            for name, metric in metrics.items():
                with self.subTest(set=set_name, metric=name):
                    self.assertEqual(unaggregated_selectors(metric['query']), [], metric['query'])


if __name__ == '__main__':
    unittest.main()

"""
Unit tests for :mod:`bexhoma.environment`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest
from unittest import mock

from bexhoma import environment


class BuildEnvironmentVersionFieldTest(unittest.TestCase):
    """build_environment()'s output must record environment_contract_version --
    the file's own source of truth, since environment.yml is fully generated
    (no separate contract doc to drift out of sync with)."""

    def test_environment_contract_version_is_present(self) -> None:
        fake_cluster = mock.Mock(context='stub-context', namespace='bexhoma')
        with mock.patch.object(environment, 'collect_nodes', return_value=([], [])), \
             mock.patch.object(environment, 'collect_node_usage', return_value=None), \
             mock.patch.object(environment, 'collect_storage_classes', return_value=[]), \
             mock.patch.object(environment, 'collect_resource_limits', return_value={}):
            result = environment.build_environment(fake_cluster)
        self.assertEqual(result['environment_contract_version'], environment.ENVIRONMENT_CONTRACT_VERSION)
        self.assertEqual(result['occupancy_source'], environment.OCCUPANCY_UNAVAILABLE)


def _node(name: str = 'node-1') -> environment.NodeInfo:
    return environment.NodeInfo(
        name=name,
        allocatable={'cpu': '16', 'memory': '64Gi', 'nvidia.com/gpu': '2'},
    )


def _series(node: str, resource: str, value: str) -> dict:
    return {'metric': {'node': node, 'resource': resource}, 'value': [1760000000, value]}


class PrometheusOccupancyTest(unittest.TestCase):
    """Node occupancy read from kube-state-metrics through Prometheus."""

    def setUp(self) -> None:
        self.cluster = mock.Mock(namespace='bexhoma')
        self.cluster.config = {'credentials': {'k8s': {'monitor': {
            'service_monitoring': 'http://bexhoma-service-{service}-default.{namespace}.svc.cluster.local:9090/api/v1/',
        }}}}
        self.cluster.get_dashboard_pod_name.return_value = 'bexhoma-dashboard-0'

    def _answers(self, requests: list, limits: list):
        def query(cluster, pod, url, promql):
            if promql.startswith('count('):
                return [{'metric': {}, 'value': [0, '42']}]
            return requests if 'resource_requests' in promql else limits
        return query

    def test_url_is_formatted_like_the_health_probe(self) -> None:
        self.assertEqual(
            environment._prometheus_url(self.cluster),
            'http://bexhoma-service-monitoring-default.bexhoma.svc.cluster.local:9090/api/v1/',
        )

    def test_requests_and_limits_map_onto_allocatable_keys(self) -> None:
        nodes = [_node()]
        requests = [
            _series('node-1', 'cpu', '4.5'),
            _series('node-1', 'memory', str(16 * 1024 ** 3)),
            _series('node-1', 'nvidia_com_gpu', '1'),
        ]
        limits = [_series('node-1', 'cpu', '32'), _series('node-1', 'memory', str(32 * 1024 ** 3))]
        with mock.patch.object(environment, '_query_prometheus', side_effect=self._answers(requests, limits)):
            self.assertTrue(environment.collect_node_usage_prometheus(self.cluster, nodes))
        node = nodes[0]
        self.assertEqual(node.requested, {'cpu': '4500m', 'memory': str(16 * 1024 ** 3), 'nvidia.com/gpu': '1'})
        self.assertEqual(node.free, {'cpu': '11500m', 'memory': str(48 * 1024 ** 3), 'nvidia.com/gpu': '1'})
        self.assertEqual(node.limits_pct, {'cpu': 200, 'memory': 50, 'nvidia.com/gpu': 0})

    def test_series_for_unknown_nodes_and_nan_are_ignored(self) -> None:
        nodes = [_node()]
        requests = [
            _series('tainted-node', 'cpu', '8'),
            _series('', 'cpu', '1'),
            _series('node-1', 'cpu', 'NaN'),
            _series('node-1', 'unknown_resource', '3'),
        ]
        with mock.patch.object(environment, '_query_prometheus', side_effect=self._answers(requests, [])):
            self.assertTrue(environment.collect_node_usage_prometheus(self.cluster, nodes))
        self.assertEqual(nodes[0].free['cpu'], '16000m')

    def test_missing_kube_state_metrics_falls_back(self) -> None:
        nodes = [_node()]
        with mock.patch.object(environment, '_query_prometheus', return_value=[]):
            self.assertFalse(environment.collect_node_usage_prometheus(self.cluster, nodes))
        self.assertEqual(nodes[0].free, {})

    def test_failed_query_falls_back(self) -> None:
        with mock.patch.object(environment, '_query_prometheus',
                               side_effect=environment.EnvironmentError('boom')):
            self.assertFalse(environment.collect_node_usage_prometheus(self.cluster, [_node()]))

    def test_no_dashboard_pod_falls_back_without_querying(self) -> None:
        self.cluster.get_dashboard_pod_name.return_value = ''
        with mock.patch.object(environment, '_query_prometheus') as query:
            self.assertFalse(environment.collect_node_usage_prometheus(self.cluster, [_node()]))
        query.assert_not_called()

    def test_no_prometheus_configured_falls_back(self) -> None:
        self.cluster.config = {'credentials': {'k8s': {}}}
        self.assertFalse(environment.collect_node_usage_prometheus(self.cluster, [_node()]))

    def test_collect_node_usage_prefers_prometheus(self) -> None:
        with mock.patch.object(environment, 'collect_node_usage_prometheus', return_value=True):
            self.assertEqual(environment.collect_node_usage(self.cluster, [_node()]),
                             environment.OCCUPANCY_PROMETHEUS)
        self.cluster.v1core.list_pod_for_all_namespaces.assert_not_called()

    def test_pod_listing_fallback_also_reports_requested_and_limits(self) -> None:
        container = mock.Mock()
        container.resources.requests = {'cpu': '2', 'memory': '4Gi'}
        container.resources.limits = {'cpu': '8'}
        pod = mock.Mock()
        pod.status.phase = 'Running'
        pod.spec.node_name = 'node-1'
        pod.spec.containers = [container]
        page = mock.Mock(items=[pod])
        page.metadata._continue = None
        self.cluster.v1core.list_pod_for_all_namespaces.return_value = page
        nodes = [_node()]
        with mock.patch.object(environment, 'collect_node_usage_prometheus', return_value=False):
            source = environment.collect_node_usage(self.cluster, nodes)
        self.assertEqual(source, environment.OCCUPANCY_KUBERNETES_API)
        self.assertEqual(nodes[0].requested['cpu'], '2000m')
        self.assertEqual(nodes[0].free['cpu'], '14000m')
        self.assertEqual(nodes[0].limits_pct['cpu'], 50)


if __name__ == '__main__':
    unittest.main()

"""Tests for cluster calls sent through the Kubernetes API instead of kubectl (#800).

Pod logs, pod and PVC labels, deleting a Deployment or the TLS Secrets and
reading Service endpoints go through the Python client; each keeps kubectl
as fallback when there is no API client or the API keeps failing.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest
from unittest import mock

from kubernetes import client as k8s
from kubernetes.client.rest import ApiException

from bexhoma.clusters import API_NOT_CALLED, decode_output
from tests.test_fewer_calls import _bare_cluster

__all__ = []


def _api_cluster():
    """A cluster with mocked API clients that must not fall back to kubectl."""
    cluster = _bare_cluster()
    cluster.v1core = mock.Mock()
    cluster.v1apps = mock.Mock()
    cluster.cluster_access = mock.Mock()
    cluster.kubectl = mock.Mock(side_effect=AssertionError('no kubectl expected'))
    return cluster


class CallApiTest(unittest.TestCase):
    """The shared request helper: retries, definitive answers, fallback."""

    def test_without_client_the_api_is_not_called(self) -> None:
        cluster = _bare_cluster()
        self.assertIs(cluster._call_api('x', mock.Mock()), API_NOT_CALLED)

    def test_definitive_status_is_not_retried(self) -> None:
        cluster = _api_cluster()
        call = mock.Mock(side_effect=ApiException(status=404))
        self.assertIsNone(cluster._call_api('x', call))
        self.assertEqual(call.call_count, 1)

    def test_other_errors_are_retried_with_a_new_token(self) -> None:
        cluster = _api_cluster()
        call = mock.Mock(side_effect=[ApiException(status=500), 'reply'])
        with mock.patch('builtins.print'):
            self.assertEqual(cluster._call_api('x', call), 'reply')
        cluster.cluster_access.assert_called_once()

    def test_a_failing_api_is_given_up(self) -> None:
        cluster = _api_cluster()
        call = mock.Mock(side_effect=ApiException(status=500))
        with mock.patch('builtins.print'):
            self.assertIs(cluster._call_api('x', call), API_NOT_CALLED)
        self.assertEqual(call.call_count, 3)

    def test_connection_error_goes_to_kubectl_at_once(self) -> None:
        cluster = _api_cluster()
        call = mock.Mock(side_effect=OSError('connection refused'))
        with mock.patch('builtins.print'):
            self.assertIs(cluster._call_api('x', call), API_NOT_CALLED)
        self.assertEqual(call.call_count, 1)


class PodLogTest(unittest.TestCase):
    """pod_log() reads through read_namespaced_pod_log."""

    def test_log_of_a_container(self) -> None:
        cluster = _api_cluster()
        cluster.v1core.read_namespaced_pod_log.return_value = mock.Mock(data=b'line 1\nline 2\n')
        self.assertEqual(cluster.pod_log('sut-0', 'dbms', previous=True), 'line 1\nline 2\n')
        cluster.v1core.read_namespaced_pod_log.assert_called_once_with(
            name='sut-0', namespace='benchmarks', previous=True, _preload_content=False, container='dbms')

    def test_log_of_a_pod_without_container(self) -> None:
        cluster = _api_cluster()
        cluster.v1core.read_namespaced_pod_log.return_value = mock.Mock(data=b'x')
        cluster.pod_log('job-pod')
        self.assertNotIn('container', cluster.v1core.read_namespaced_pod_log.call_args.kwargs)

    def test_log_that_is_not_utf8(self) -> None:
        self.assertEqual(decode_output('Größe'.encode('latin1')), 'Größe')

    def test_no_previous_instance_gives_none(self) -> None:
        cluster = _api_cluster()
        cluster.v1core.read_namespaced_pod_log.side_effect = ApiException(status=400)
        self.assertIsNone(cluster.pod_log('sut-0', 'dbms', previous=True))

    def test_fallback_to_kubectl(self) -> None:
        cluster = _bare_cluster()
        cluster.kubectl = mock.Mock(return_value='log')
        self.assertEqual(cluster.pod_log('sut-0', 'dbms'), 'log')
        cluster.kubectl.assert_called_once_with('logs sut-0 --container=dbms --tail=-1')


class LabelTest(unittest.TestCase):
    """label_pod() and label_pvc() patch the labels, values as strings."""

    def test_pod_labels(self) -> None:
        cluster = _api_cluster()
        self.assertTrue(cluster.label_pod('sut-0', {'loaded': True, 'time_index': 30}))
        cluster.v1core.patch_namespaced_pod.assert_called_once_with(
            name='sut-0', namespace='benchmarks',
            body={'metadata': {'labels': {'loaded': 'True', 'time_index': '30'}}})

    def test_pvc_labels(self) -> None:
        cluster = _api_cluster()
        self.assertTrue(cluster.label_pvc('pvc-1', {'volume_size': '100G'}))
        cluster.v1core.patch_namespaced_persistent_volume_claim.assert_called_once_with(
            name='pvc-1', namespace='benchmarks', body={'metadata': {'labels': {'volume_size': '100G'}}})

    def test_missing_object_is_not_labelled(self) -> None:
        cluster = _api_cluster()
        cluster.v1core.patch_namespaced_pod.side_effect = ApiException(status=404)
        self.assertIsNone(cluster.label_pod('gone', {'loaded': True}))

    def test_fallback_to_kubectl(self) -> None:
        cluster = _bare_cluster()
        cluster.kubectl = mock.Mock(return_value='pod/sut-0 labeled')
        self.assertTrue(cluster.label_pod('sut-0', {'loaded': True, 'time_loading_start': 17}))
        cluster.kubectl.assert_called_once_with(
            'label pod sut-0 --overwrite loaded="True" time_loading_start="17"')
        cluster.kubectl = mock.Mock(return_value=None)
        self.assertIsNone(cluster.label_pvc('pvc-1', {'loaded': True}))


class DeleteTest(unittest.TestCase):
    """Deleting a Deployment and the TLS Secrets of an experiment."""

    def test_delete_deployment(self) -> None:
        cluster = _api_cluster()
        cluster.delete_deployment('bexhoma-sut-x')
        kwargs = cluster.v1apps.delete_namespaced_deployment.call_args.kwargs
        self.assertEqual(kwargs['name'], 'bexhoma-sut-x')
        self.assertEqual(kwargs['body'].propagation_policy, 'Background')

    def test_delete_deployment_that_is_gone(self) -> None:
        cluster = _api_cluster()
        cluster.v1apps.delete_namespaced_deployment.side_effect = ApiException(status=404)
        cluster.delete_deployment('bexhoma-sut-x')

    def test_delete_secrets(self) -> None:
        cluster = _api_cluster()
        cluster.delete_secrets('experiment=42,component=tls')
        cluster.v1core.delete_collection_namespaced_secret.assert_called_once_with(
            namespace='benchmarks', label_selector='experiment=42,component=tls')

    def test_fallback_to_kubectl(self) -> None:
        cluster = _bare_cluster()
        cluster.kubectl = mock.Mock()
        cluster.delete_deployment('bexhoma-sut-x')
        cluster.delete_secrets('experiment=42,component=tls')
        self.assertEqual([c.args[0] for c in cluster.kubectl.call_args_list],
                         ['delete deployment bexhoma-sut-x', 'delete secret -l experiment=42,component=tls'])


class ServiceEndpointsTest(unittest.TestCase):
    """get_service_endpoints() reads the Endpoints object of the Service."""

    def test_addresses_of_all_subsets(self) -> None:
        cluster = _api_cluster()
        cluster.v1core.read_namespaced_endpoints.return_value = k8s.V1Endpoints(subsets=[
            k8s.V1EndpointSubset(addresses=[k8s.V1EndpointAddress(ip='10.0.0.1'),
                                            k8s.V1EndpointAddress(ip='10.0.0.2')]),
            k8s.V1EndpointSubset(addresses=None)])
        self.assertEqual(cluster.get_service_endpoints('svc'), ['10.0.0.1', '10.0.0.2'])

    def test_service_without_endpoints(self) -> None:
        cluster = _api_cluster()
        cluster.v1core.read_namespaced_endpoints.return_value = k8s.V1Endpoints(subsets=None)
        self.assertEqual(cluster.get_service_endpoints('svc'), [])
        cluster.v1core.read_namespaced_endpoints.side_effect = ApiException(status=404)
        self.assertEqual(cluster.get_service_endpoints('svc'), [])


class HostRestartsTest(unittest.TestCase):
    """HostProbe.get_host_restarts() reads the pod once via get_pod_restart_counts()."""

    def test_reads_the_restart_counts_of_the_pod(self) -> None:
        from bexhoma.configurations.host import HostProbe
        from types import SimpleNamespace
        cluster = SimpleNamespace(get_pod_restart_counts=mock.Mock(return_value={'dbms': 2, 'monitor': 0}))
        config = SimpleNamespace(logger=mock.Mock(), pod_sut='sut-0', experiment=SimpleNamespace(cluster=cluster))
        self.assertEqual(HostProbe(config).get_host_restarts(), '2 0')
        cluster.get_pod_restart_counts.assert_called_once_with('sut-0')
        cluster.get_pod_restart_counts.return_value = {}
        self.assertEqual(HostProbe(config).get_host_restarts(), '')


if __name__ == '__main__':
    unittest.main()

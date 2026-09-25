"""Tests that a temporarily unreachable cluster is waited out, not fatal."""
from __future__ import annotations

import http.server
import socket
import subprocess
import threading
import unittest
from unittest import mock

import kubernetes.client as kubernetes_client

from bexhoma import clusters
from bexhoma.clusters import Kubernetes, is_cluster_connection_error

__all__ = []

#: kubectl output captured from a real call against a closed port; the OS
#: explanation after the colon is localized.
UNREACHABLE_OUTPUT = (
    'E0925 10:50:05.806342   37340 memcache.go:265] "Unhandled Error" '
    'err="couldn\'t get current server API group list"\n'
    'Unable to connect to the server: dial tcp 127.0.0.1:1: connectex: '
    'Es konnte keine Verbindung hergestellt werden.\n'
)
INTERRUPTED_OUTPUT = 'error: context deadline exceeded\n'
EMPTY_POD_LIST = b'{"kind": "PodList", "apiVersion": "v1", "metadata": {}, "items": []}'


def _bare_cluster() -> Kubernetes:
    """Build a cluster object without reading a config or contacting a cluster."""
    cluster = Kubernetes.__new__(Kubernetes)
    cluster.context = 'test'
    cluster.namespace = 'benchmarks'
    cluster.appname = 'bexhoma'
    cluster.logger = mock.Mock()
    return cluster


def _completed_exec(stdout: str, stderr: str) -> mock.Mock:
    """Build a fake ``kubectl exec`` process with the given output."""
    process = mock.Mock()
    process.communicate.return_value = (stdout.encode(), stderr.encode())
    return process


class _EmptyPodListHandler(http.server.BaseHTTPRequestHandler):
    """Answer every GET like an API server with no pods."""

    def do_GET(self) -> None:
        """Return an empty pod list."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(EMPTY_POD_LIST)))
        self.end_headers()
        self.wfile.write(EMPTY_POD_LIST)

    def log_message(self, *_) -> None:
        """Keep test output quiet."""


class ClusterOutageTest(unittest.TestCase):
    """Verify each path to the cluster survives a temporary outage."""

    def test_connection_errors_are_told_apart_from_command_errors(self) -> None:
        """Only kubectl's own connection messages may trigger a retry."""
        self.assertTrue(is_cluster_connection_error(UNREACHABLE_OUTPUT))
        self.assertTrue(is_cluster_connection_error(INTERRUPTED_OUTPUT))
        self.assertFalse(is_cluster_connection_error(
            INTERRUPTED_OUTPUT, include_interrupted=False))
        self.assertTrue(is_cluster_connection_error(
            UNREACHABLE_OUTPUT, include_interrupted=False))
        # A database refusing connections inside the pod is not a cluster outage.
        self.assertFalse(is_cluster_connection_error(
            'psql: error: connection to server failed: Connection refused\n'))
        self.assertFalse(is_cluster_connection_error(
            'Error from server (NotFound): pods "x" not found\n'))
        # A flaky VPN makes the API server reject requests the account may make;
        # the rejection happens before the command runs, so it is always retried.
        self.assertTrue(is_cluster_connection_error(
            'Error from server (Forbidden): pods "bexhoma-benchmarker-x" is forbidden: '
            'User "keycloak:perdelt" cannot get resource "pods" in API group "" '
            'in the namespace "perdelt"\n', include_interrupted=False))

    def test_api_query_waits_until_the_api_server_is_back(self) -> None:
        """A pod query during an outage must return once the server answers."""
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        backoffs = []

        def pause_then_recover(seconds: float) -> None:
            """Record the backoff and bring the server up on the second pause."""
            backoffs.append(seconds)
            if len(backoffs) == 2:
                # Created only now: constructing the server already accepts
                # connections, which would hang a request nobody answers.
                server = http.server.HTTPServer(('127.0.0.1', port), _EmptyPodListHandler)
                threading.Thread(target=server.serve_forever, daemon=True).start()
                self.addCleanup(server.server_close)
                self.addCleanup(server.shutdown)

        def point_at_local_server(context=None, client_configuration=None) -> None:
            """Stand in for kubeconfig loading."""
            client_configuration.host = f'http://127.0.0.1:{port}'

        cluster = _bare_cluster()
        with mock.patch.object(clusters.kubernetes_config, 'load_kube_config',
                               side_effect=point_at_local_server):
            cluster.v1core = kubernetes_client.CoreV1Api(api_client=cluster._new_api_client())
        with mock.patch('urllib3.util.retry.time.sleep', side_effect=pause_then_recover):
            self.assertEqual(cluster.get_pods(component='sut'), [])
        self.assertEqual(backoffs, [2, 4])

    def test_kubectl_retries_until_the_cluster_is_back(self) -> None:
        """A kubectl command must be repeated until the cluster answers."""
        cluster = _bare_cluster()
        outage = subprocess.CalledProcessError(1, 'kubectl', output=UNREACHABLE_OUTPUT.encode())
        with (
            mock.patch.object(clusters.subprocess, 'check_output',
                              side_effect=[outage, outage, b'labelled']) as run,
            mock.patch.object(clusters.time, 'sleep') as pause,
        ):
            self.assertEqual(cluster.kubectl('label pod x a=b --overwrite'), 'labelled')
        self.assertEqual(run.call_count, 3)
        self.assertEqual(pause.call_count, 2)

    def test_kubectl_gives_up_once_the_budget_is_spent(self) -> None:
        """An outage longer than the budget must end in the old failure value."""
        cluster = _bare_cluster()
        outage = subprocess.CalledProcessError(1, 'kubectl', output=UNREACHABLE_OUTPUT.encode())
        clock = iter(range(0, 10_000, clusters.CLUSTER_OUTAGE_RETRY_SECONDS))
        with (
            mock.patch.object(clusters.subprocess, 'check_output', side_effect=outage),
            mock.patch.object(clusters.time, 'sleep'),
            mock.patch.object(clusters.time, 'monotonic', side_effect=lambda: next(clock)),
        ):
            self.assertIsNone(cluster.kubectl('get pods'))

    def test_create_whose_reply_was_lost_counts_as_created(self) -> None:
        """AlreadyExists on a retried create means the first attempt went through."""
        cluster = _bare_cluster()
        lost_reply = subprocess.CalledProcessError(1, 'kubectl', output=INTERRUPTED_OUTPUT.encode())
        exists = subprocess.CalledProcessError(
            1, 'kubectl',
            output=b'Error from server (AlreadyExists): jobs.batch "loader" already exists')
        with (
            mock.patch.object(clusters.subprocess, 'check_output',
                              side_effect=[lost_reply, exists]),
            mock.patch.object(clusters.time, 'sleep'),
        ):
            self.assertIsNotNone(cluster.kubectl('create -f job.yml'))

    def test_pod_command_retries_until_the_cluster_is_back(self) -> None:
        """A command inside a pod must be repeated until the cluster answers."""
        cluster = _bare_cluster()
        with (
            mock.patch.object(clusters.subprocess, 'Popen', side_effect=[
                _completed_exec('', UNREACHABLE_OUTPUT),
                _completed_exec('OK\n', ''),
            ]),
            mock.patch.object(clusters.time, 'sleep') as pause,
        ):
            _, stdout, _ = cluster.execute_command_in_pod('redis-cli set k 1', pod='mq')
        self.assertEqual(stdout, 'OK\n')
        pause.assert_called_once()

    def test_interrupted_command_that_is_unsafe_to_repeat_is_not_rerun(self) -> None:
        """A command that may have run must not be repeated when the caller forbids it."""
        cluster = _bare_cluster()
        with (
            mock.patch.object(clusters.subprocess, 'Popen', side_effect=[
                _completed_exec('', INTERRUPTED_OUTPUT),
            ]) as run,
            mock.patch.object(clusters.time, 'sleep') as pause,
        ):
            _, _, stderr = cluster.execute_command_in_pod(
                'psql -f reset.sql', pod='sut', retry_interrupted=False)
        self.assertEqual(stderr, INTERRUPTED_OUTPUT)
        self.assertEqual(run.call_count, 1)
        pause.assert_not_called()


if __name__ == "__main__":
    unittest.main()

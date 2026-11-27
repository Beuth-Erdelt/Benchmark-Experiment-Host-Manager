"""Tests that the context's settings in ``cluster.config`` are read with and without an explicit context (#947)."""
from __future__ import annotations

import ast
import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from bexhoma import clusters
from bexhoma.clusters import Kubernetes

__all__ = []

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTEXTS = {
    'current': {'namespace': 'ns-current', 'port': 9091, 'service_sut': '{service}.{namespace}.svc.cluster.local'},
    'other': {'namespace': 'ns-other', 'port': 9092, 'service_sut': '{service}.{namespace}.svc.cluster.local',
              'storage_classes': ['nvme']},
    'incomplete': {'service_sut': '{service}.{namespace}.svc.cluster.local'},
}


class ContextConfigTest(unittest.TestCase):
    """``Kubernetes(clusterconfig, context=...)`` takes the settings of that context."""

    def setUp(self) -> None:
        with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as f:
            config = ast.literal_eval(f.read())
        config['credentials']['k8s']['appname'] = 'app-test'
        config['credentials']['k8s']['context'] = CONTEXTS
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.clusterconfig = os.path.join(folder.name, 'cluster.config')
        with open(self.clusterconfig, 'w', encoding='utf-8') as f:
            f.write(repr(config))
        current = mock.patch.object(clusters.kubernetes_config, 'list_kube_config_contexts',
                                    return_value=([], {'name': 'current'}))
        current.start()
        self.addCleanup(current.stop)

    def cluster(self, context=None) -> tuple[Kubernetes, str]:
        """Build the cluster without connecting; return it and what it printed."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            cluster = Kubernetes(self.clusterconfig, context=context, connect=False)
        return cluster, out.getvalue()

    def test_explicit_context(self) -> None:
        cluster, out = self.cluster('other')
        self.assertEqual(cluster.context, 'other')
        self.assertEqual(cluster.namespace, 'ns-other')
        self.assertEqual(cluster.port, 9092)
        self.assertEqual(cluster.appname, 'app-test')
        self.assertEqual(cluster.storage_classes, ['nvme'])
        self.assertEqual(cluster.contextdata, CONTEXTS['other'])
        self.assertNotIn('WARN', out)

    def test_current_context(self) -> None:
        cluster, out = self.cluster()
        self.assertEqual(cluster.context, 'current')
        self.assertEqual(cluster.namespace, 'ns-current')
        self.assertEqual(cluster.port, 9091)
        self.assertEqual(cluster.appname, 'app-test')
        self.assertEqual(cluster.storage_classes, [])
        self.assertNotIn('WARN', out)

    def test_context_missing_in_config(self) -> None:
        cluster, out = self.cluster('unknown')
        self.assertEqual(cluster.context, 'unknown')
        self.assertEqual(cluster.contextdata, {})
        self.assertIsNone(cluster.port)
        self.assertEqual(cluster.namespace, 'bexhoma')
        self.assertIn('context unknown not found', out)

    def test_context_without_port_and_namespace(self) -> None:
        cluster, out = self.cluster('incomplete')
        self.assertIsNone(cluster.port)
        self.assertEqual(cluster.namespace, 'bexhoma')
        self.assertIn("has no 'port'", out)
        self.assertIn("has no 'namespace'", out)

    def test_no_kubeconfig(self) -> None:
        error = clusters.kubernetes_config.ConfigException('Invalid kube-config file. No configuration found.')
        with mock.patch.object(clusters.kubernetes_config, 'list_kube_config_contexts', side_effect=error):
            cluster, out = self.cluster()
        self.assertIsNone(cluster.context)
        self.assertEqual(cluster.contextdata, {})
        self.assertIn('No current Kubernetes context found in kubeconfig', out)


if __name__ == '__main__':
    unittest.main()

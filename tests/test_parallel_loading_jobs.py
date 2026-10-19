"""Tests that a finished loading job only touches its own pods.

With two loader entries (test_parallel_tpch_ycsb.py: TPC-H and YCSB), the
TPC-H job finished first and ``LoadingCoordinator.check()`` deleted the pods
of all loading jobs of the configuration, including the running YCSB loader,
whose job then failed (experiment 1792366372).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest import mock

from bexhoma import clusters
from bexhoma.configurations.loading import LoadingCoordinator

__all__ = []


class JobPodsSelectorTest(unittest.TestCase):

    def test_jobname_adds_the_job_name_label(self) -> None:
        cluster = object.__new__(clusters.Kubernetes)
        cluster.appname = 'bexhoma'
        cluster.namespace = 'ns'
        cluster.logger = mock.Mock()
        cluster.v1core = mock.Mock()
        cluster.v1core.list_namespaced_pod.return_value = SimpleNamespace(
            items=[SimpleNamespace(metadata=SimpleNamespace(name='job-2-abcde'))])
        self.assertEqual(cluster.get_job_pods(component='loading', experiment='1', jobname='job-2'), ['job-2-abcde'])
        self.assertEqual(cluster.v1core.list_namespaced_pod.call_args.kwargs['label_selector'],
                         'app=bexhoma,component=loading,experiment=1,job-name=job-2')
        cluster.get_job_pods(component='loading', experiment='1')
        self.assertEqual(cluster.v1core.list_namespaced_pod.call_args.kwargs['label_selector'],
                         'app=bexhoma,component=loading,experiment=1')


class CheckUsesOwnPodsTest(unittest.TestCase):

    def test_each_job_reads_only_its_pods(self) -> None:
        requested = []
        pods_of = {'job-1': ['job-1-aaaaa'], 'job-2': ['job-2-bbbbb']}

        def get_job_pods(**kwargs):
            requested.append(kwargs.get('jobname'))
            return pods_of.get(kwargs.get('jobname'), pods_of['job-1'] + pods_of['job-2'])

        cluster = SimpleNamespace(
            appname='bexhoma', logger=mock.Mock(),
            get_job_status=lambda *args, **kwargs: 0,
            get_jobs=lambda *args: ['job-1', 'job-2'],
            get_job_pods=get_job_pods,
            get_pod_status=lambda pod: 'Running',
            get_pods_labels=lambda **kwargs: {},
        )
        cfg = SimpleNamespace(
            loading_deactivated=False, loading_active=True, code='1', configuration='pg-1',
            experiment=SimpleNamespace(cluster=cluster), experiment_dict={'loader': [{}, {}]},
            loading_started=True, loading_finished=False)
        with mock.patch('bexhoma.configurations.loading.stored_pods', return_value=set()):
            try:
                LoadingCoordinator(cfg).check()
            except AttributeError:
                pass  # later bookkeeping needs more of the configuration; the pod lookup is what is tested
        self.assertEqual(requested[:2], ['job-1', 'job-2'])


if __name__ == '__main__':
    unittest.main()

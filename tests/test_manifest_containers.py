"""
Tests for :func:`bexhoma.configurations.lifecycle.record_manifest_containers`.

The pod logs stored at the end of an experiment run come from the containers
recorded in ``deployment_infos``: regular containers, init containers and the
containers of the SUT's Jobs (e.g. CockroachDB's ``cluster-init``).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os
import unittest

import yaml

from bexhoma.configurations.lifecycle import record_manifest_containers

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(template: str) -> list:
    with open(os.path.join(_REPO, 'k8s', template), encoding='utf-8') as f:
        return [d for d in yaml.safe_load_all(f) if d]


class RecordManifestContainersTest(unittest.TestCase):
    def test_cockroachdb_job_is_recorded_apart_from_the_statefulset(self):
        manifest = _load('deploymenttemplate-CockroachDB.yml')
        infos = {'deployment': {'sut': {'containers': ['dbms']}},
                 'statefulset': {'worker': {'containers': ['dbms']}}}
        record_manifest_containers(infos, manifest)
        self.assertEqual(infos['job']['worker'],
                         {'name': 'cluster-init', 'containers': ['cluster-init'], 'init_containers': []})
        # the StatefulSet keeps its own containers
        self.assertEqual(infos['statefulset']['worker']['containers'], ['dbms'])

    def test_init_containers_of_the_final_manifest(self):
        manifest = [
            {'kind': 'Deployment', 'metadata': {'name': 'sut', 'labels': {'component': 'sut'}},
             'spec': {'template': {'spec': {'initContainers': [{'name': 'include-client'}],
                                            'containers': [{'name': 'dbms'}]}}}},
            {'kind': 'StatefulSet', 'metadata': {'name': 'w', 'labels': {'component': 'worker'}},
             'spec': {'template': {'spec': {'containers': [{'name': 'dbms'}]}}}},
        ]
        infos = {'deployment': {'sut': {'containers': ['dbms']}},
                 'statefulset': {'worker': {'containers': ['dbms']}}}
        record_manifest_containers(infos, manifest)
        self.assertEqual(infos['deployment']['sut']['init_containers'], ['include-client'])
        self.assertEqual(infos['statefulset']['worker']['init_containers'], [])
        self.assertEqual(infos['job'], {})

    def test_objects_not_in_deployment_infos_are_left_out(self):
        manifest = [
            {'kind': 'Deployment', 'metadata': {'name': 'other', 'labels': {'component': 'other'}},
             'spec': {'template': {'spec': {'initContainers': [{'name': 'x'}], 'containers': [{'name': 'y'}]}}}},
            {'kind': 'Service', 'metadata': {'name': 's'}},
        ]
        infos = {'deployment': {}, 'statefulset': {}}
        record_manifest_containers(infos, manifest)
        self.assertEqual(infos, {'deployment': {}, 'statefulset': {}, 'job': {}})

    def test_jobs_of_an_earlier_run_are_replaced(self):
        infos = {'deployment': {}, 'statefulset': {}, 'job': {'worker': {'name': 'old'}}}
        record_manifest_containers(infos, [])
        self.assertEqual(infos['job'], {})


if __name__ == '__main__':
    unittest.main()

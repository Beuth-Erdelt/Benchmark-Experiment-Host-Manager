"""Tests that the measured data directory is the one the deployment template mounts.

``HostProbe`` measures the database size (``du``, ``datadisk``) and the volume
(``df``) at the path where the template mounts the storage volume
(``benchmark-storage-volume``, or ``bxw`` for a worker), recorded by
``LifecycleManager.start_sut()`` even when no pvc is attached and the mount is
removed from the rendered manifest. ``cluster.config``'s ``datadir`` is only
the fallback for a template without such a mount.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
import unittest

import yaml

# imported as a module, so unittest does not collect the base classes here again
from tests import test_naming_conformance as naming

__all__ = []

#: Where k8s/deploymenttemplate-PostgreSQL.yml mounts benchmark-storage-volume.
_POSTGRES_DATA = '/var/lib/postgresql/data'


def _rendered_dbms_mounts(test: naming.SutManifestPerRunTest) -> list:
    name = next(p for p in os.listdir(test.tmp_dir.name) if p.startswith('bexhoma-sut-') and p.endswith('-1.yml'))
    with open(os.path.join(test.tmp_dir.name, name), encoding='utf-8') as f:
        deployment = next(d for d in yaml.safe_load_all(f) if isinstance(d, dict) and d.get('kind') == 'Deployment')
    dbms = next(c for c in deployment['spec']['template']['spec']['containers'] if c['name'] == 'dbms')
    return [m['name'] for m in dbms.get('volumeMounts', []) or []]


def _commands_of(host, **kwargs) -> list:
    """Run ``get_host_all`` with every pod command recorded instead of executed."""
    commands = []

    def record(command='', pod='', **_):
        commands.append(command)
        return '', '', ''

    host._config.execute_command_in_pod_sut = record
    host._config.experiment.cluster.kubectl = lambda *a, **kw: ''  # the other probes
    host.get_host_all(**kwargs)
    return commands


class DataPathWithoutPvcTest(naming.SutManifestPerRunTest):
    """Ephemeral storage: the mount is removed from the manifest, its path still recorded."""

    def test_path_recorded_although_the_mount_is_removed(self) -> None:
        self.cfg.num_experiment_to_apply_done = 0
        self.cfg.lifecycle.start_sut()
        self.assertNotIn('benchmark-storage-volume', _rendered_dbms_mounts(self))
        sut = self.cfg.deployment_infos['deployment']['sut']
        self.assertEqual(sut['data_path'], _POSTGRES_DATA)
        self.assertNotIn('mount_path', sut, 'no pvc, so no pvc mount for df')
        self.assertEqual(self.cfg.host.get_data_paths(), (_POSTGRES_DATA, ''))

    def test_du_runs_at_the_template_path(self) -> None:
        self.cfg.num_experiment_to_apply_done = 0
        self.cfg.lifecycle.start_sut()
        self.cfg.dockertemplate['datadir'] = '/somewhere/else/'
        commands = _commands_of(self.cfg.host)
        self.assertTrue(any(c.startswith('du ') and _POSTGRES_DATA in c for c in commands), commands)
        self.assertFalse(any('/somewhere/else' in c for c in commands), commands)


class DataPathWithPvcTest(naming.StorageRemovedPerRepetitionTest):
    """With a pvc the same path is both the data path and the pvc mount."""

    def test_path_and_mount_recorded(self) -> None:
        self._start_repetition(0, request_storage_remove=True)
        self.assertIn('benchmark-storage-volume', _rendered_dbms_mounts(self))
        self.assertEqual(self.cfg.host.get_data_paths(), (_POSTGRES_DATA, _POSTGRES_DATA))
        commands = _commands_of(self.cfg.host)
        self.assertTrue(any(c.startswith('df -hP ' + _POSTGRES_DATA) for c in commands), commands)


class DataPathPerComponentTest(naming.SutManifestPerRunTest):
    """Workers use their own path; a template without a storage mount falls back to datadir."""

    def test_worker_uses_its_own_path(self) -> None:
        self.cfg.deployment_infos['statefulset'] = {'tikv': {'data_path': '/var/lib/tikv', 'mount_path': '/var/lib/tikv'}}
        self.cfg.deployment_infos['deployment'] = {'sut': {}}
        self.assertEqual(self.cfg.host.get_data_paths('tikv', 'statefulset'), ('/var/lib/tikv', '/var/lib/tikv'))
        commands = _commands_of(self.cfg.host, component='tikv', kind='statefulset')
        self.assertTrue(any(c.startswith('du ') and '/var/lib/tikv' in c for c in commands), commands)
        self.assertTrue(any(c.startswith('df -hP /var/lib/tikv') for c in commands), commands)

    def test_no_storage_mount_falls_back_to_datadir(self) -> None:
        self.cfg.deployment_infos['deployment'] = {'sut': {}}
        self.cfg.dockertemplate['datadir'] = '/var/lib/mysql/'
        self.assertEqual(self.cfg.host.get_data_paths(), ('/var/lib/mysql/', ''))


if __name__ == '__main__':
    unittest.main()

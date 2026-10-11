"""Tests that a result folder is downloaded as one archive and unpacked locally."""
from __future__ import annotations

import io
import os
import tarfile
import tempfile
import unittest
from unittest import mock

from bexhoma.clusters import Kubernetes

__all__ = []


def _bare_cluster() -> Kubernetes:
    """Build a cluster object without reading a config or contacting a cluster."""
    cluster = Kubernetes.__new__(Kubernetes)
    cluster.context = 'test'
    cluster.logger = mock.Mock()
    return cluster


def _write_archive(path: str, members: dict) -> None:
    """Write a ``tar.gz`` like ``tar czf x -C dir .`` would, with ``./`` prefixed names."""
    with tarfile.open(path, 'w:gz') as archive:
        for name, content in members.items():
            data = content.encode()
            info = tarfile.TarInfo('./' + name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


class DownloadFolderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.local = os.path.join(self.tmp.name, '1791653201')
        self.cluster = _bare_cluster()
        self.commands = []

    def tearDown(self):
        self.tmp.cleanup()

    def _exec(self, ok=True):
        def execute_command_in_pod(command, pod='', container='', params='', retry_interrupted=True):
            self.commands.append(command)
            if command.startswith('timeout ') and ok:
                return "", "BEXHOMA_ARCHIVE_OK\n", ""
            if command.startswith('timeout '):
                return "", "", "tar: No space left on device\n"
            return "", "", ""
        return execute_command_in_pod

    def test_archive_is_copied_unpacked_and_removed(self):
        members = {'query_1_execution.csv': 'a', 'pgduckdb-1-1-1-1-1/x.log': 'b'}

        def download_file(filename_remote, filename_local, pod, container='dashboard', max_retries=3):
            self.assertEqual(filename_remote, '/tmp/bexhoma-download-1791653201.tar.gz')
            _write_archive(filename_local, members)
            return 'copied'

        os.makedirs(self.local)
        with open(os.path.join(self.local, 'query_1_execution.csv'), 'w') as f:
            f.write('stale')
        with mock.patch.object(self.cluster, 'execute_command_in_pod', side_effect=self._exec()), \
                mock.patch.object(self.cluster, 'download_file', side_effect=download_file):
            result = self.cluster.download_folder('/results/1791653201/.', self.local, pod='dashboard-pod')

        self.assertEqual(result, 'copied')
        self.assertEqual(
            self.commands[0],
            'timeout -s KILL 600 tar czf /tmp/bexhoma-download-1791653201.tar.gz -C /results/1791653201 .'
            ' && echo BEXHOMA_ARCHIVE_OK')
        self.assertEqual(self.commands[-1], 'rm -f /tmp/bexhoma-download-1791653201.tar.gz')
        for name, content in members.items():
            with open(os.path.join(self.local, name)) as f:
                self.assertEqual(f.read(), content)
        self.assertEqual(sorted(os.listdir(self.local)), ['pgduckdb-1-1-1-1-1', 'query_1_execution.csv'])

    def test_failed_copy_still_removes_remote_archive(self):
        def download_file(filename_remote, filename_local, pod, container='dashboard', max_retries=3):
            raise RuntimeError('download_file failed after 3 attempts')

        with mock.patch.object(self.cluster, 'execute_command_in_pod', side_effect=self._exec()), \
                mock.patch.object(self.cluster, 'download_file', side_effect=download_file):
            with self.assertRaises(RuntimeError):
                self.cluster.download_folder('/results/1791653201', self.local, pod='dashboard-pod')
        self.assertEqual(self.commands[-1], 'rm -f /tmp/bexhoma-download-1791653201.tar.gz')

    def test_falls_back_to_plain_copy_when_packing_fails(self):
        download_file = mock.Mock(return_value='copied')
        with mock.patch.object(self.cluster, 'execute_command_in_pod', side_effect=self._exec(ok=False)), \
                mock.patch.object(self.cluster, 'download_file', download_file):
            result = self.cluster.download_folder('/results/1791653201', self.local, pod='dashboard-pod')
        self.assertEqual(result, 'copied')
        download_file.assert_called_once_with(
            filename_remote='/results/1791653201/.', filename_local=self.local,
            pod='dashboard-pod', container='dashboard', max_retries=3)

    def test_packing_timeout_raises_without_fallback(self):
        download_file = mock.Mock(return_value='copied')
        with mock.patch.object(self.cluster, 'execute_command_in_pod', side_effect=self._exec(ok=False)), \
                mock.patch.object(self.cluster, 'download_file', download_file), \
                mock.patch('bexhoma.clusters.time.monotonic', side_effect=[0, 600]):
            with self.assertRaises(RuntimeError):
                self.cluster.download_folder('/results/1791653201', self.local, pod='dashboard-pod')
        download_file.assert_not_called()
        self.assertEqual(self.commands[-1], 'rm -f /tmp/bexhoma-download-1791653201.tar.gz')

    def test_rejects_paths_outside_target(self):
        def download_file(filename_remote, filename_local, pod, container='dashboard', max_retries=3):
            with tarfile.open(filename_local, 'w:gz') as archive:
                info = tarfile.TarInfo('../escape.txt')
                info.size = 1
                archive.addfile(info, io.BytesIO(b'x'))
            return 'copied'

        with mock.patch.object(self.cluster, 'execute_command_in_pod', side_effect=self._exec()), \
                mock.patch.object(self.cluster, 'download_file', side_effect=download_file):
            with self.assertRaises(Exception):
                self.cluster.download_folder('/results/1791653201', self.local, pod='dashboard-pod')
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, 'escape.txt')))


if __name__ == '__main__':
    unittest.main()

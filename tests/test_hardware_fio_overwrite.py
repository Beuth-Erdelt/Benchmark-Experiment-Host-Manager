"""
Unit tests for the fio overwrite option (``hardware.py -xfow``).

Without ``--overwrite=1`` fio writes into a freshly fallocated file, so every
fdatasync also commits an ext4 journal entry; on the nvme pool that gave ~370
instead of ~1,540 commits/s (see dev/plan-tenancy-sweep.md, M0a). Covers the
flag's parsing and refusal, the argument building in
``images/hardware/benchmarker/run_fio.sh`` and the evaluator reading logs
from before the option.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from bexhoma import evaluators
from bexhoma.experiments.base import ExperimentBase

from .test_resource_sweep import _AnyDockers, _AnyVolumes, _SweepStubCluster

RUN_FIO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'images', 'hardware', 'benchmarker', 'run_fio.sh')


def _run_hardware(*argv: str) -> list:
    """Run hardware.py against a stub cluster; return the fio rounds of its configuration."""
    tmp_dir = tempfile.TemporaryDirectory()
    cluster = _SweepStubCluster(resultfolder=tmp_dir.name)
    cluster.volumes = _AnyVolumes(cluster.volumes)
    cluster.dockers = _AnyDockers(cluster.dockers)
    captured = []
    with (
        tmp_dir,
        mock.patch('bexhoma.clusters.Kubernetes', return_value=cluster),
        mock.patch.object(ExperimentBase, 'process', lambda experiment: captured.append(experiment)),
        mock.patch.object(sys, 'argv', ['hardware.py', 'run', *argv]),
        contextlib.redirect_stdout(io.StringIO()),
    ):
        try:
            runpy.run_path('hardware.py', run_name='__main__')
        except SystemExit as exit_:
            if exit_.code not in (None, 0):
                raise
    return captured[0].configurations[0].benchmarking_parameters_list


class OverwriteFlagTest(unittest.TestCase):
    """``-xfow`` sweeps 0/1 and refuses anything else."""

    def test_default_is_fresh_file(self) -> None:
        rounds = _run_hardware()
        self.assertEqual([r['HARDWARE_FIO_OVERWRITE'] for r in rounds], ['0'])

    def test_sweep_adds_one_round_per_value(self) -> None:
        rounds = _run_hardware('-xffd', '1', '-xfow', '0,1', '-nbt', '1,16')
        self.assertEqual(
            [(r['HARDWARE_FIO_OVERWRITE'], r['HARDWARE_FIO_NUMJOBS']) for r in rounds],
            [('0', '1'), ('0', '16'), ('1', '1'), ('1', '16')])

    def test_invalid_value_is_refused(self) -> None:
        for value in ('2', 'yes', '0,true'):
            with self.subTest(value), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    _run_hardware('-xfow', value)
                self.assertEqual(raised.exception.code, 2)


@unittest.skipIf(sys.platform == 'win32', 'run_fio.sh needs a POSIX bash')
class RunFioArgumentsTest(unittest.TestCase):
    """``run_fio.sh`` appends ``--overwrite=1`` only for ``HARDWARE_FIO_OVERWRITE=1``."""

    def fio_command(self, overwrite) -> str:
        with tempfile.TemporaryDirectory() as tmp_dir:
            calls = os.path.join(tmp_dir, 'ssh-calls')
            ssh = os.path.join(tmp_dir, 'ssh')
            with open(ssh, 'w', newline='\n') as file:
                file.write(f'#!/bin/sh\necho "$@" >> "{calls}"\necho "{{}}"\n')
            os.chmod(ssh, 0o755)
            env = {
                'PATH': tmp_dir + os.pathsep + os.environ.get('PATH', ''),
                'HARDWARE_FIO_RW': 'write', 'HARDWARE_FIO_BS': '8k', 'HARDWARE_FIO_IODEPTH': '1',
                'HARDWARE_FIO_NUMJOBS': '1', 'HARDWARE_FIO_ENGINE': 'sync',
                'HARDWARE_FIO_FSYNC': '0', 'HARDWARE_FIO_FDATASYNC': '1',
                'HARDWARE_TEST_DIR': '/database/fio-test', 'HARDWARE_SIZE': '1G',
                'HARDWARE_DURATION': '60', 'BEXHOMA_EXPERIMENT': 'test',
            }
            if overwrite is not None:
                env['HARDWARE_FIO_OVERWRITE'] = overwrite
            result = subprocess.run(['bash', RUN_FIO], env=env, capture_output=True, text=True, timeout=30)
            with open(calls) as file:
                fio = [line for line in file if ' fio ' in f' {line}']
            self.assertEqual(len(fio), 1, result.stdout + result.stderr)
            self.assertIn('HARDWARE_FIO_OVERWRITE:' + (overwrite or '0'), result.stdout)
            return fio[0]

    def test_overwrite_1_adds_flag(self) -> None:
        self.assertIn('--overwrite=1', self.fio_command('1'))

    def test_overwrite_0_and_unset_keep_fresh_file(self) -> None:
        for overwrite in ('0', None):
            with self.subTest(overwrite):
                self.assertNotIn('--overwrite', self.fio_command(overwrite))


class EvaluatorOverwriteTest(unittest.TestCase):
    """Logs from before ``-xfow`` have no ``HARDWARE_FIO_OVERWRITE`` line and read as 0."""

    LOG = (
        "BEXHOMA_CONNECTION:hardware-1-1-1-1\nBEXHOMA_CONFIGURATION:Hardware-1\n"
        "BEXHOMA_EXPERIMENT:1\nBEXHOMA_EXPERIMENT_RUN:1\nBEXHOMA_CLIENT:1\n"
        "BEXHOMA_CHILD:1\nBEXHOMA_NUM_PODS:1\nHARDWARE_TYPE:fio\nHARDWARE_FIO_FDATASYNC:1\n"
        "{overwrite}HARDWARE_FIO_WRITE_IOPS:400\n"
    )

    def parse(self, overwrite_line: str):
        evaluator = evaluators.hardware(code='1', path='/nonexistent', include_loading=False,
                                        include_benchmarking=True, benchmark_run=1, name='hardware')
        with tempfile.TemporaryDirectory() as tmp_dir:
            filename = os.path.join(tmp_dir, 'bexhoma-benchmarker-hardware-1-1-1-1-abcde.log')
            with open(filename, 'w') as file:
                file.write(self.LOG.format(overwrite=overwrite_line))
            df = evaluator.log_to_df(filename)
        return evaluator.benchmarking_set_datatypes(df)

    def test_old_log_without_key_reads_as_0(self) -> None:
        self.assertEqual(self.parse('')['hardware_fio_overwrite'].iloc[0], 0)

    def test_new_log_reads_value(self) -> None:
        self.assertEqual(self.parse('HARDWARE_FIO_OVERWRITE:1\n')['hardware_fio_overwrite'].iloc[0], 1)


if __name__ == '__main__':
    unittest.main()

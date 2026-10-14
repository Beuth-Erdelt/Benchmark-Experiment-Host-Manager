"""Tests for loading-phase timing, repetitions of SUT-keeping modes and image-pull waits."""
from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
import unittest
from unittest import mock

from bexhoma.clusters import Kubernetes
from bexhoma.configurations import loading
from bexhoma.experiments.base import ExperimentBase

__all__ = []


def _fake_datetime(*timestamps: int) -> type:
    """Return a datetime class whose now() yields the given Unix timestamps in turn."""
    moments = iter(timestamps)

    class FakeDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            # str() of a whole second drops the '.%f' part the code parses
            return datetime.fromtimestamp(next(moments)).replace(microsecond=1)

    return FakeDatetime


class LoadDataAsynchTimingTest(unittest.TestCase):
    """A loading phase is timed from its own start, not from the start of the whole load."""

    def run_phase(self, phase_start: int, phase_end: int, **kwargs) -> list[str]:
        """Run load_data_asynch without scripts and return the kubectl commands it issued."""
        commands = []

        def popen(command, **_):
            commands.append(command)
            proc = mock.Mock()
            proc.communicate.return_value = (b'', b'')
            return proc

        with (
            mock.patch.object(loading.subprocess, 'Popen', side_effect=popen),
            mock.patch.object(loading, 'datetime', _fake_datetime(phase_start, phase_end)),
        ):
            loading.load_data_asynch(
                app='bexhoma', component='sut', experiment='42', configuration='PostgreSQL-1',
                pod_sut='sut-pod', scriptfolder='/tmp/', commands=[], loadData='', path='/tmp',
                volume='', context='ctx', service_name='svc', database=[], **kwargs)
        return commands

    @staticmethod
    def final_labels(commands: list[str]) -> dict[str, str]:
        """Parse the labels of the last 'label pods' command."""
        command = [c for c in commands if 'label pods' in c][-1]
        return dict(part.split('=', 1) for part in command.split() if '=' in part)

    def test_index_phase_counts_only_its_own_duration(self) -> None:
        """TPC-C run 2 of 1791970052: schema 6 s + ingest 145 s, index phase 30 s."""
        load_start = 1791973812
        commands = self.run_phase(
            load_start + 198, load_start + 228,
            time_offset=151, time_start_int=load_start, script_type='index')
        labels = self.final_labels(commands)
        self.assertEqual(labels['time_index'], '30')
        self.assertEqual(labels['time_loading'], '181')
        self.assertEqual(labels['index'], 'True')
        start_labels = [c for c in commands if 'label pods' in c][0]
        self.assertIn(f'time_loading_start={load_start}', start_labels)

    def test_first_phase_is_unchanged(self) -> None:
        """Without a given start the phase start is the start of loading."""
        load_start = 1791973812
        commands = self.run_phase(load_start, load_start + 6)
        labels = self.final_labels(commands)
        self.assertEqual(labels['time_schema'], '6')
        self.assertEqual(labels['time_loading'], '6')
        start_labels = [c for c in commands if 'label pods' in c][0]
        self.assertIn(f'time_loading_start={load_start}', start_labels)
        self.assertIn(f'loading_phase_start={load_start}', start_labels)


class LeavesSutRunningTest(unittest.TestCase):
    """Modes that keep the SUT running still run every repetition."""

    def test_only_the_last_repetition_keeps_the_sut(self) -> None:
        config = SimpleNamespace(num_experiment_to_apply=3, num_experiment_to_apply_done=0)
        decide = ExperimentBase._leaves_sut_running
        # -m load / --skip-shutdown
        self.assertFalse(decide(config, False, True))
        config.num_experiment_to_apply_done = 1
        self.assertFalse(decide(config, False, True))
        config.num_experiment_to_apply_done = 2
        self.assertTrue(decide(config, False, True))
        # normal run: never kept
        self.assertFalse(decide(config, False, False))
        # -m start: kept at once
        config.num_experiment_to_apply_done = 0
        self.assertTrue(decide(config, True, True))


class ImagePullWaitTest(unittest.TestCase):
    """A loading pod stuck pulling its image flags the repetition's loading times."""

    def make_experiment(self, reasons: list[str]) -> tuple[ExperimentBase, SimpleNamespace]:
        experiment = ExperimentBase.__new__(ExperimentBase)
        experiment._runtime_test_results = []
        experiment._image_pull_waits_seen = set()
        experiment.cluster = mock.Mock()
        experiment.cluster.get_job_pods.return_value = ['loader-pod']
        experiment.cluster.get_pod_waiting_reasons.return_value = reasons
        config = SimpleNamespace(
            appname='bexhoma', code='42', configuration='PostgreSQL-1',
            loading_started=True, loading_finished=False, num_experiment_to_apply_done=0)
        return experiment, config

    def test_image_pull_backoff_is_reported_once(self) -> None:
        experiment, config = self.make_experiment(['ImagePullBackOff'])
        with mock.patch('builtins.print'):
            experiment._note_image_pull_waits(config)
            experiment._note_image_pull_waits(config)
        self.assertEqual(len(experiment._runtime_test_results), 1)
        passed, label = experiment._runtime_test_results[0]
        self.assertFalse(passed)
        self.assertIn('loader-pod', label)
        self.assertIn('ImagePullBackOff', label)
        self.assertIn('repetition 1', label)

    def test_other_waits_and_finished_loads_are_ignored(self) -> None:
        experiment, config = self.make_experiment(['ContainerCreating'])
        experiment._note_image_pull_waits(config)
        self.assertEqual(experiment._runtime_test_results, [])
        experiment.cluster.get_pod_waiting_reasons.return_value = ['ErrImagePull']
        experiment.cluster.get_job_pods.reset_mock()
        config.loading_finished = True
        experiment._note_image_pull_waits(config)
        self.assertEqual(experiment._runtime_test_results, [])
        experiment.cluster.get_job_pods.assert_not_called()

    def test_cluster_reads_waiting_reasons_of_all_containers(self) -> None:
        cluster = Kubernetes.__new__(Kubernetes)
        cluster.kubectl = mock.Mock(side_effect=['', 'ImagePullBackOff'])
        self.assertEqual(cluster.get_pod_waiting_reasons('loader-pod'), ['ImagePullBackOff'])
        cluster.kubectl = mock.Mock(return_value=None)
        self.assertEqual(cluster.get_pod_waiting_reasons('gone-pod'), [])


if __name__ == '__main__':
    unittest.main()

"""Tests that a benchmark round whose pods do not all start is skipped, not waited for forever."""
from __future__ import annotations

from datetime import datetime, timedelta
from types import SimpleNamespace
import unittest
from unittest import mock

from bexhoma.clusters import Kubernetes
from bexhoma.experiments.base import BENCHMARK_START_TIMEOUT_MINUTES, ExperimentBase

__all__ = []

ROUND_KEY = "bexhoma-benchmarker-podcount-round-1-4-PostgreSQL-1-42"
JOB = "bexhoma-benchmarker-postgresql-1-42-1-4-1"
SUBMITTED_AT = datetime(2026, 9, 25, 8, 34, 0)


class BenchmarkStartTimeoutTest(unittest.TestCase):
    """Verify the start limit covers only the start of a round, and what a skip does."""

    def setUp(self) -> None:
        """Build an experiment with one configuration whose round was just submitted."""
        self.experiment = ExperimentBase.__new__(ExperimentBase)
        self.experiment.code = "42"
        self.experiment.cluster = mock.Mock()
        self.experiment.cluster.appname = "bexhoma"
        self.experiment.cluster.get_job_pods.return_value = ["pod-running", "pod-pending"]
        self.experiment.cluster.get_pod_status.side_effect = (
            lambda pod: "Running" if pod == "pod-running" else "Pending")
        self.experiment.cluster.get_pod_containers.return_value = ["dbmsbenchmarker"]
        self.experiment._runtime_test_results = []
        self.experiment._benchmark_rounds_starting = {"PostgreSQL-1": (ROUND_KEY, SUBMITTED_AT)}
        self.config = SimpleNamespace(configuration="PostgreSQL-1")

    def _skip(self, minutes_after_submission: float) -> bool:
        """Run the check the given number of minutes after submission."""
        now = SUBMITTED_AT + timedelta(minutes=minutes_after_submission)
        return self.experiment._skip_benchmark_round_if_not_started(self.config, [JOB], now)

    def test_started_round_is_never_skipped_however_long_it_runs(self) -> None:
        """Once all pods are in, a long benchmark must not be cut short."""
        self.experiment.cluster.get_pod_counter.return_value = 0
        self.assertFalse(self._skip(1))
        self.assertNotIn("PostgreSQL-1", self.experiment._benchmark_rounds_starting)
        # Hours later the round is no longer tracked, so nothing is checked.
        self.assertFalse(self._skip(600))
        self.experiment.cluster.get_pod_counter.assert_called_once_with(ROUND_KEY)

    def test_round_still_starting_within_the_limit_is_waited_for(self) -> None:
        """Missing pods are fine while the limit has not passed."""
        self.experiment.cluster.get_pod_counter.return_value = 1
        self.assertFalse(self._skip(BENCHMARK_START_TIMEOUT_MINUTES - 1))
        self.experiment.cluster.delete_job.assert_not_called()

    def test_unreadable_counter_never_triggers_a_skip(self) -> None:
        """Without evidence of a stuck round, the round is waited for as before."""
        self.experiment.cluster.get_pod_counter.return_value = None
        self.assertFalse(self._skip(BENCHMARK_START_TIMEOUT_MINUTES + 60))
        self.experiment.cluster.delete_job.assert_not_called()

    def test_round_missing_pods_after_the_limit_is_skipped_with_diagnostics(self) -> None:
        """Diagnostics are saved first, then the job and its pods are deleted."""
        cluster = self.experiment.cluster
        cluster.get_pod_counter.return_value = 1

        self.assertTrue(self._skip(BENCHMARK_START_TIMEOUT_MINUTES))

        cluster.store_job_description.assert_called_once_with(JOB)
        self.assertEqual(
            [call.kwargs["pod_name"] for call in cluster.store_pod_description.call_args_list],
            ["pod-running", "pod-pending"])
        # Only a pod that ran has a log to save.
        cluster.store_pod_log.assert_called_once_with("pod-running", "dbmsbenchmarker")
        order = [name for name, *_ in cluster.method_calls
                 if name in ("store_job_description", "store_pod_description",
                             "delete_job", "delete_job_pods")]
        self.assertEqual(order[-3:], ["delete_job", "delete_job_pods", "delete_job_pods"])
        self.assertNotIn("delete_job", order[:-3])
        self.assertEqual(len(self.experiment._runtime_test_results), 1)
        passed, reason = self.experiment._runtime_test_results[0]
        self.assertFalse(passed)
        self.assertIn("1 pods still missing", reason)
        self.assertNotIn("PostgreSQL-1", self.experiment._benchmark_rounds_starting)

    def test_counter_reply_is_read_as_number_or_unknown(self) -> None:
        """A missing key or failed read must not look like a started round."""
        cluster = Kubernetes.__new__(Kubernetes)
        cluster.logger = mock.Mock()
        cluster.get_pods = mock.Mock(return_value=["bexhoma-messagequeue-1"])
        cluster.execute_command_in_pod = mock.Mock()
        for reply, expected in (("3\n", 3), ("0\n", 0), ("-1\n", -1), ("(nil)\n", None), ("", None)):
            cluster.execute_command_in_pod.return_value = ("", reply, "")
            self.assertEqual(cluster.get_pod_counter(ROUND_KEY), expected)

    def test_configuration_without_a_starting_round_is_not_checked(self) -> None:
        """Rounds submitted before tracking, or already started, cost no Redis read."""
        self.experiment._benchmark_rounds_starting = {}
        self.assertFalse(self._skip(BENCHMARK_START_TIMEOUT_MINUTES + 60))
        self.experiment.cluster.get_pod_counter.assert_not_called()


if __name__ == "__main__":
    unittest.main()

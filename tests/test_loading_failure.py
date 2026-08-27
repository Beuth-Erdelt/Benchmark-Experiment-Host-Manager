"""Tests for bounded loading and diagnostics-before-teardown behavior."""
from __future__ import annotations

from datetime import datetime, timedelta
from types import SimpleNamespace
import unittest
from unittest import mock

from bexhoma.clusters import Kubernetes
from bexhoma.configurations.lifecycle import LifecycleManager
from bexhoma.configurations.loading import LoadingCoordinator
from bexhoma.experiments.base import ExperimentBase

__all__ = []


class LoadingFailureTest(unittest.TestCase):
    """Verify failed and overlong loads preserve their diagnostic evidence."""

    def test_terminal_job_failure_is_distinct_from_an_incomplete_job(self) -> None:
        """A Kubernetes Failed condition must be observable by the execution host."""
        cluster = Kubernetes.__new__(Kubernetes)
        cluster.appname = "bexhoma"
        cluster.namespace = "benchmarks"
        cluster.logger = mock.Mock()
        cluster.v1batches = mock.Mock()
        cluster.v1batches.read_namespaced_job_status.return_value = SimpleNamespace(
            status=SimpleNamespace(conditions=[SimpleNamespace(
                type="Failed", status="True",
            )]),
        )

        self.assertTrue(cluster.get_job_failed("loader-job"))

    def test_load_abort_reason_covers_failure_and_per_configuration_timeout(self) -> None:
        """Failure and timeout must both stop a load, while an active load may continue."""
        experiment = ExperimentBase.__new__(ExperimentBase)
        experiment.max_loading_minutes = 2
        experiment.cluster = mock.Mock()
        experiment.cluster.get_jobs.return_value = ["loader-job"]
        config = SimpleNamespace(
            appname="bexhoma", code="42", configuration="PostgreSQL-1",
            loading_started=True, loading_finished=False,
            loading_started_at=datetime(2026, 8, 25, 12, 0, 0),
        )
        now = datetime(2026, 8, 25, 12, 1, 0)

        experiment.cluster.get_job_failed.return_value = True
        self.assertIn("loader-job", experiment._loading_abort_reason(config, now))

        experiment.cluster.get_job_failed.return_value = False
        self.assertIsNone(experiment._loading_abort_reason(config, now))
        timed_out = experiment._loading_abort_reason(
            config, now + timedelta(minutes=2)
        )
        self.assertIn("2 minute", timed_out)

        config.loading_started = False
        config.loading_started_at = None
        self.assertIsNone(experiment._loading_abort_reason(config, now))
        self.assertIsNone(config.loading_started_at)

        config.loading_started = True
        config.loading_finished = True
        self.assertIsNone(experiment._loading_abort_reason(config, now))
        self.assertIsNone(config.loading_started_at)

        experiment._runtime_test_results = []
        with (
            mock.patch.object(
                ExperimentBase, "_loading_abort_reason", return_value="load failed"
            ),
            mock.patch.object(ExperimentBase, "remove_experiment") as remove,
        ):
            self.assertTrue(experiment._abort_loading_if_needed(config, now))
        self.assertEqual(experiment._runtime_test_results, [(False, "load failed")])
        remove.assert_called_once_with()

    def test_stopping_loading_captures_diagnostics_before_deletion(self) -> None:
        """Logs and Kubernetes descriptions must be stored before objects disappear."""
        calls: list[tuple[str, str]] = []

        class Cluster:
            """Record diagnostic and deletion calls made by the lifecycle manager."""

            def get_jobs(self, *_args):
                return ["loader-job"]

            def get_job_status(self, _job):
                return 0

            def get_job_pods(self, *_args, **_kwargs):
                return ["loader-pod"]

            def get_pods(self, **_kwargs):
                return ["sut-pod"]

            def get_pod_status(self, _pod):
                return "Failed"

            def get_pod_containers(self, _pod):
                return ["loader"]

            def pod_log_exists(self, _pod, _container=""):
                return False

            def pod_description_exists(self, _pod):
                return False

            def job_description_exists(self, _job):
                return False

            def store_pod_log(self, pod_name, container="", number=None):
                calls.append(("pod-log", f"{pod_name}:{container}"))

            def store_pod_description(self, pod_name, number=None):
                calls.append(("pod-description", pod_name))

            def store_job_description(self, jobname):
                calls.append(("job-description", jobname))

            def delete_job(self, job):
                calls.append(("delete-job", job))

            def delete_pod(self, pod):
                calls.append(("delete-pod", pod))

        cluster = Cluster()
        config = SimpleNamespace(
            appname="bexhoma", configuration="PostgreSQL-1", code="42",
            num_experiment_to_apply_done=0,
            experiment=SimpleNamespace(cluster=cluster),
        )

        LifecycleManager(config).stop_loading()

        first_delete = next(
            index for index, call in enumerate(calls) if call[0].startswith("delete")
        )
        self.assertTrue(all(
            not call[0].startswith("delete") for call in calls[:first_delete]
        ))
        self.assertIn(("pod-log", "loader-pod:loader"), calls)
        self.assertIn(("pod-log", "sut-pod:loader"), calls)
        self.assertIn(("job-description", "loader-job"), calls)

    def test_failed_loader_pod_is_captured_while_its_job_may_retry(self) -> None:
        """A failed attempt must be saved without waiting for terminal Job failure."""
        cluster = mock.Mock()
        cluster.appname = "bexhoma"
        cluster.get_job_status.return_value = 0
        cluster.get_jobs.return_value = ["loader-job"]
        cluster.get_job_pods.return_value = ["failed-pod"]
        cluster.get_pod_status.return_value = "Failed"
        cluster.get_pod_containers.return_value = ["loader"]
        cluster.pod_log_exists.return_value = False
        cluster.pod_description_exists.return_value = False
        cluster.get_pods_labels.return_value = {}
        config = SimpleNamespace(
            loading_deactivated=False, loading_active=True,
            appname="bexhoma", code="42", configuration="PostgreSQL-1",
            experiment=SimpleNamespace(cluster=cluster, code="42"),
        )

        LoadingCoordinator(config).check()

        cluster.store_pod_log.assert_called_once_with(
            pod_name="failed-pod", container="loader"
        )
        cluster.store_pod_description.assert_called_once_with(
            pod_name="failed-pod"
        )


if __name__ == "__main__":
    unittest.main()

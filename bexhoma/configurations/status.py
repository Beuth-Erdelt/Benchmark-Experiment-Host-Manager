"""Component status queries for bexhoma SUT configurations."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['ComponentStatus']


class ComponentStatus:
    """Encapsulates all Kubernetes pod-state predicates for a configuration.

    Replaces the ``sut_is_*``, ``monitoring_is_*``, and ``maintaining_is_*``
    methods that were formerly on :class:`~bexhoma.configurations.SutConfiguration`.

    :param config: The parent configuration this status object belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def sut_pending(self) -> bool:
        """Return True iff any SUT pod is in Pending state.

        :return: True if at least one SUT pod is Pending.
        :rtype: bool
        """
        app = self._config.appname
        component = 'sut'
        configuration = self._config.configuration
        status_pending = False
        pods = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration)
        if len(pods) > 0:
            for pod_sut in pods:
                self._config.logger.debug(f"Testing {pod_sut} for pending")
                status = self._config.experiment.cluster.get_pod_status(pod_sut)
                if status == "Pending":
                    status_pending = True
        return status_pending

    def sut_running(self) -> bool:
        """Return True iff all SUT pods are Running.

        :return: True if all SUT pods are Running.
        :rtype: bool
        """
        app = self._config.appname
        component = 'sut'
        configuration = self._config.configuration
        status_running = True
        pods = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration)
        if len(pods) > 0:
            for pod_sut in pods:
                self._config.logger.debug(f"Testing {pod_sut} for running")
                status = self._config.experiment.cluster.get_pod_status(pod_sut)
                if status != "Running":
                    status_running = False
            return status_running
        return False

    def sut_healthy(self) -> bool:
        """Return True iff all SUT pods are Running and Ready.

        :return: True if all SUT pods are running and have passed readiness checks.
        :rtype: bool
        """
        if self._config.is_sut_ready:
            return True
        app = self._config.appname
        component = 'sut'
        configuration = self._config.configuration
        status_healthy = True
        pods = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration)
        if len(pods) > 0:
            for pod_sut in pods:
                self._config.logger.debug(f"Testing {pod_sut} for healthy")
                status = self._config.experiment.cluster.get_pod_status(pod_sut)
                if status == "Running":
                    ready = self._config.experiment.cluster.is_pod_ready(pod_sut)
                    if not ready:
                        status_healthy = False
                else:
                    status_healthy = False
            self._config.is_sut_ready = status_healthy
            return status_healthy
        return False

    def workers_healthy(self) -> bool:
        """Return True iff all worker pods are Running and Ready.

        :return: True if all worker pods are running and ready.
        :rtype: bool
        """
        if self._config.num_worker > 0:
            if self._config.are_worker_ready:
                return True
            self._config.are_worker_ready = True
            components = list(self._config.deployment_infos['statefulset'].keys())
            for component in components:
                num_ready = 0
                pods_worker = self._config.get_worker_pods(
                    component=component, only_stateful=True)
                for pod in pods_worker:
                    status = self._config.experiment.cluster.get_pod_status(pod)
                    if status == "Running":
                        ready = self._config.experiment.cluster.is_pod_ready(pod)
                        if ready:
                            num_ready = num_ready + 1
                print("{:30s}: found {} / {} running workers (component {})".format(
                    self._config.configuration, num_ready, self._config.num_worker, component))
                self._config.are_worker_ready = (
                    self._config.are_worker_ready and (num_ready == self._config.num_worker))
                if self._config.are_worker_ready:
                    self._config.attach_worker()
            return self._config.are_worker_ready
        else:
            return True

    def sut_exists(self) -> bool:
        """Return True iff any SUT component pod exists in the cluster.

        :return: True if at least one SUT pod exists (any state).
        :rtype: bool
        """
        app = self._config.appname
        configuration = self._config.configuration
        components = list(self._config.deployment_infos['deployment'].keys())
        for component in components:
            pods = self._config.experiment.cluster.get_pods(
                app, component, self._config.experiment.code, configuration)
            if len(pods) > 0:
                return True
        components = list(self._config.deployment_infos['statefulset'].keys())
        for component in components:
            pods = self._config.experiment.cluster.get_pods(
                app, component, self._config.experiment.code, configuration)
            if len(pods) > 0:
                return True
        return False

    def maintaining_running(self) -> bool:
        """Return True iff maintaining pods equal the target count (running or succeeded).

        :return: True if maintaining job has reached completion.
        :rtype: bool
        """
        app = self._config.appname
        component = 'maintaining'
        configuration = self._config.configuration
        pods_running = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration, status="Running")
        pods_succeeded = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration, status="Succeeded")
        self._config.logger.debug(
            "maintaining_running found {} running and {} succeeded pods".format(
                len(pods_running), len(pods_succeeded)))
        return len(pods_running) + len(pods_succeeded) == self._config.num_maintaining

    def maintaining_pending(self) -> bool:
        """Return True iff any maintaining pod is in Pending state.

        :return: True if a maintaining pod is pending.
        :rtype: bool
        """
        app = self._config.appname
        component = 'maintaining'
        configuration = self._config.configuration
        pods = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration, status="Pending")
        if len(pods) > 0:
            return True
        return False

    def monitoring_running(self) -> bool:
        """Return True iff the monitoring deployment pod is Running.

        :return: True if monitoring is active and running.
        :rtype: bool
        """
        if (self._config.experiment.cluster.monitor_cluster_exists
                and not self._config.monitor_app_active):
            return True
        app = self._config.appname
        component = 'monitoring'
        configuration = self._config.configuration
        pods = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self._config.experiment.cluster.get_pod_status(pod_sut)
            if status == "Running":
                return True
        return False

    def monitoring_pending(self) -> bool:
        """Return True iff the monitoring pod is in Pending state.

        :return: True if monitoring pod is pending.
        :rtype: bool
        """
        app = self._config.appname
        component = 'monitoring'
        configuration = self._config.configuration
        pods = self._config.experiment.cluster.get_pods(
            app, component, self._config.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = self._config.experiment.cluster.get_pod_status(pod_sut)
            if status == "Pending":
                return True
        return False

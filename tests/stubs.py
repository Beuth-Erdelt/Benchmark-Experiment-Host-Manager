"""
Fake cluster object for testing :mod:`bexhoma.experiment_builder` without a
live Kubernetes cluster.

Deliberately does not subclass :class:`bexhoma.clusters.Kubernetes` — that
class requires an on-disk ``cluster.config`` and, unless ``connect=False``,
live kubeconfig access. ``StubCluster`` instead implements only the minimal
attribute/method surface the code paths under test actually touch (traced by
hand through ``ExperimentBase.__init__``, ``TpchExperiment.__init__``,
``SutConfiguration.__init__``, and ``ExperimentBase.prepare_testbed``).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

__all__ = ["StubCluster"]


class StubCluster:
    """Minimal fake standing in for :class:`bexhoma.clusters.Kubernetes` in tests."""

    def __init__(self, resultfolder: str) -> None:
        """
        :param resultfolder: Directory used as the experiment result folder;
            the caller (a test) owns creating/cleaning it up (e.g. ``tempfile.TemporaryDirectory``).
        """
        self.resultfolder = resultfolder
        self.code = None
        self.appname = 'bexhoma'
        self.namespace = 'bexhoma'
        self.context = 'stub-context'
        self.max_sut = None
        self.storage_classes: list = []
        self.experiments: list = []
        self.experiments_configfolder = ''
        # Minimal 'tpch' volume/init-script catalog: covers every script key
        # TPCH.configure_workload() can select (Schema, and the Index* variants
        # reachable when init_indexes/init_constraints/init_statistics are set).
        self.volumes = {
            'tpch': {
                'id': 'tpch',
                'initscripts': {
                    '': [],
                    'Schema': [],
                    'Index': [],
                    'Index_and_Constraints': [],
                    'Index_and_Constraints_and_Statistics': [],
                },
            },
        }
        self.dockers = {dbms: {} for dbms in (
            'PostgreSQL', 'PgDuckDB', 'MonetDB', 'MariaDB', 'MySQL', 'CedarDB',
        )}

    def set_code(self, code) -> None:
        """Mirror ``Kubernetes.set_code`` without the ``experiments.config`` file check."""
        self.code = code

    def add_experiment(self, experiment) -> None:
        """Mirror ``Kubernetes.add_experiment``."""
        self.experiments.append(experiment)

    def set_experiments_configfolder(self, experiments_configfolder: str) -> None:
        """Mirror ``Kubernetes.set_experiments_configfolder``."""
        self.experiments_configfolder = experiments_configfolder

    def get_available_storage_types(self) -> list:
        """Mirror ``Kubernetes.get_available_storage_types`` without cluster-context storage classes."""
        return [None, '', 'ramdisk'] + list(self.storage_classes)

    def start_datadir(self) -> None:
        """No-op: real implementation provisions a Kubernetes PVC."""

    def start_resultdir(self) -> None:
        """No-op: real implementation provisions a Kubernetes PVC."""

    def start_dashboard(self) -> None:
        """No-op: real implementation deploys the dashboard pod."""

    def start_messagequeue(self) -> None:
        """No-op: real implementation deploys the message-queue pod."""

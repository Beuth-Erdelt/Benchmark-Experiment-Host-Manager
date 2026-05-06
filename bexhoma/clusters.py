"""
Kubernetes cluster management for bexhoma experiments.

Provides :class:`Kubernetes` for managing experiment deployments on Kubernetes,
and :class:`AWS` for AWS-specific Kubernetes clusters.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import time
import kubernetes.client as kubernetes_client
import kubernetes.config as kubernetes_config
from kubernetes.client.rest import ApiException
import subprocess
import traceback
import os
import psutil
import logging
import socket
import ast
import urllib.request
import urllib.parse
from pprint import pprint
from datetime import datetime, timedelta
from pathlib import Path

from dbmsbenchmarker import *
from .__version__ import __version__

import platform


def to_unc(path: str) -> str:
    """
    Convert a local Windows drive path to a UNC administrative share path.

    ``D:/foo`` and ``D:\\foo`` become ``\\\\localhost\\D$\\foo``.
    On Linux/macOS the normalized path is returned unchanged.
    A path that is already UNC is returned unchanged.
    """
    p = Path(path)

    if platform.system() != "Windows":
        return str(p)

    if str(p).startswith("\\\\"):
        return str(p)

    drive = p.drive
    if drive:
        drive_letter = drive.rstrip(":").upper()
        rel = p.relative_to(drive + "\\")
        unc = f"\\\\localhost\\{drive_letter}$\\{rel.as_posix()}"
        return unc.replace("/", "\\")

    return str(p)


class Kubernetes():
    """
    Manages bexhoma experiments on a Kubernetes cluster.

    Provides Kubernetes API wrappers (pod/job/service/PVC queries and deletions),
    cluster component lifecycle methods (dashboard, message queue, monitoring, SUT),
    experiment bookkeeping (code, result folder, experiment list), and pod/job log
    persistence.

    Subclass: :class:`AWS` (K8s on AWS with EKS nodegroup scaling).
    """

    def __init__(
        self,
        clusterconfig='cluster.config',
        experiments_configfolder='experiments/',
        yamlfolder='k8s/',
        context=None,
        code=None,
        instance=None,
        volume=None,
        docker=None,
        script=None,
        queryfile=None,
    ):
        """
        Initialise the Kubernetes cluster manager.

        :param clusterconfig: Path to the cluster configuration file.
        :param experiments_configfolder: Folder containing experiment sub-folders.
        :param yamlfolder: Folder containing Kubernetes manifest templates.
        :param context: kubectl context name.  ``None`` means use the current context.
        :param code: Unique identifier of an existing experiment to resume.
        :param instance: Instance key in ``config['instances']`` (legacy IaaS).
        :param volume: Volume key in ``config['volumes']``.
        :param docker: Docker image key in ``config['dockers']``.
        :param script: Init-script key within the chosen volume.
        :param queryfile: Path to the DBMSBenchmarker query config file.
        """
        self.logger = logging.getLogger('bexhoma')
        self.clusterconfig = clusterconfig
        self.appname = 'bexhoma'
        self.namespace = 'bexhoma'

        with open(clusterconfig) as f:
            config_text = f.read()
            self.config = ast.literal_eval(config_text)

        # Kubernetes API clients — initialised by cluster_access()
        self.v1core = None
        self.v1apps = None
        self.v1batches = None

        # Context metadata defaults; overwritten below if a context is found
        self.yamlfolder = yamlfolder
        self.contextdata = {}
        self.host = 'localhost'
        self.port = None

        if context is None:
            try:
                context = kubernetes_config.list_kube_config_contexts()[1]['name']
                self.contextdata = self.config['credentials']['k8s']['context'][context]
                self.host = 'localhost'
                self.port = self.contextdata['port']
                self.namespace = self.contextdata['namespace']
                self.appname = self.config['credentials']['k8s']['appname']
                self.yamlfolder = yamlfolder
            except Exception:
                print("WARN: No Kubernetes context found")

        self.context = context
        self.experiments = []
        self.benchmark = None
        self.experiments_configfolder = experiments_configfolder
        self.resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        self.queryfile = queryfile
        self.timeLoading = 0
        self.resources = {}
        self.ddl_parameters = {}
        self.connectionmanagement = {
            'numProcesses': None,
            'runsPerConnection': None,
            'timeout': None,
            'singleConnection': False,
        }
        self.querymanagement = {}
        self.workload = {}
        self.monitoring_active = True
        self.monitor_app_active = True
        self.monitor_cluster_active = False
        # True if cAdvisors and Prometheus run independently of bexhoma
        self.monitor_cluster_exists = False

        self.max_sut = None

        # Experiment selection keys — populated by set_experiment()
        self.change_instance = False
        self.instance_key = None
        self.volume_key = None
        self.volume = None
        self.docker_key = None
        self.docker = None
        self.script_key = None
        self.initscript = None

        self.set_experiments(self.config['instances'], self.config['volumes'], self.config['dockers'])
        self.set_experiment(instance, volume, docker, script)
        self.set_code(code)
        self.cluster_access()
        self.experiments = []

    def cluster_access(self):
        """
        Initialise Kubernetes API clients using the configured context.

        Sets ``self.v1core``, ``self.v1apps``, and ``self.v1batches``.
        Prints a warning if the cluster cannot be reached.
        """
        self.logger.debug(f'Kubernetes.cluster_access({self.context})')
        try:
            kubernetes_config.load_kube_config(context=self.context)
            self.v1core = kubernetes_client.CoreV1Api(
                api_client=kubernetes_config.new_client_from_config(context=self.context)
            )
            self.v1apps = kubernetes_client.AppsV1Api(
                api_client=kubernetes_config.new_client_from_config(context=self.context)
            )
            self.v1batches = kubernetes_client.BatchV1Api(
                api_client=kubernetes_config.new_client_from_config(context=self.context)
            )
        except Exception:
            print("WARN: Could not connect to Kubernetes")

    def set_code(self, code):
        """
        Set the unique identifier of the current experiment.

        If ``code`` is not ``None`` and an ``experiments.config`` file exists in
        the result folder, the stored experiment list is loaded from it.

        :param code: Unique experiment identifier string.
        """
        self.code = code
        if self.code is not None:
            resultfolder = self.config['benchmarker']['resultfolder']
            resultfolder += '/' + str(self.code)
            filename = resultfolder + '/experiments.config'
            if os.path.isfile(filename):
                print("experiments found")
                with open(filename, 'r') as f:
                    self.experiments = ast.literal_eval(f.read())

    def set_queryfile(self, queryfile):
        """
        Set the query config file for the DBMSBenchmarker benchmarker component.

        :param queryfile: Path to the DBMSBenchmarker query configuration file.
        """
        self.queryfile = queryfile

    def set_experiments_configfolder(self, experiments_configfolder):
        """
        Set the folder that contains experiment configuration sub-folders.

        Bexhoma expects sub-folders named by experiment type (e.g. ``tpch``),
        each containing a ``queries.config`` file and per-DBMS DDL schema folders.

        :param experiments_configfolder: Relative path to the experiments folder.
        """
        self.experiments_configfolder = experiments_configfolder

    def set_workload(self, **kwargs):
        """
        Set workload metadata for the experiment (e.g. ``name``, ``description``).

        :param kwargs: Arbitrary key/value pairs stored in ``self.workload``.
        """
        self.workload = kwargs

    def set_querymanagement(self, **kwargs):
        """
        Set DBMSBenchmarker query-management parameters.

        :param kwargs: Key/value pairs forwarded to DBMSBenchmarker (e.g. ``numRun=3``).
        """
        self.querymanagement = kwargs

    def set_connectionmanagement(self, **kwargs):
        """
        Set DBMSBenchmarker connection-management parameters.

        Can be overridden per experiment or per DBMS configuration.

        :param kwargs: Key/value pairs (e.g. ``timeout=60``, ``numProcesses=4``).
        """
        self.connectionmanagement = kwargs

    def set_resources(self, **kwargs):
        """
        Set Kubernetes resource requests/limits for the SUT component.

        Can be overridden per experiment or per DBMS configuration.

        :param kwargs: Key/value pairs (e.g. ``requests={'cpu': 4, 'memory': '16Gi'}``).
        """
        self.resources = kwargs

    def set_ddl_parameters(self, **kwargs):
        """
        Set DDL template substitution parameters.

        Values replace placeholders in DDL scripts executed during loading.
        Can be overridden per experiment or per DBMS configuration.

        :param kwargs: Key/value pairs (e.g. ``index='btree'``).
        """
        self.ddl_parameters = kwargs

    def log_experiment(self, experiment):
        """
        Append a step record to the experiment log and persist it to disk.

        The record is enriched with cluster-level metadata and appended to
        ``self.experiments``.  The list is written to ``experiments.config`` in
        the benchmark result folder.

        .. note::
            This method should be updated to produce YAML output and to handle
            detached parallel-loader workflows.

        :param experiment: Dict describing the current experiment step.
        """
        self.logger.debug('Kubernetes.log_experiment()')
        experiment['clusterconfig'] = self.clusterconfig
        experiment['experiments_configfolder'] = self.experiments_configfolder
        experiment['yamlfolder'] = self.yamlfolder
        experiment['queryfile'] = self.queryfile
        experiment['clustertype'] = "K8s"
        self.experiments.append(experiment)
        if self.benchmark is not None and self.benchmark.path is not None:
            filename = self.benchmark.path + '/experiments.config'
            with open(filename, 'w') as f:
                f.write(str(self.experiments))

    def set_experiments(self, instances=None, volumes=None, dockers=None):
        """
        Store the top-level experiment catalog from the cluster configuration.

        :param instances: Dict of IaaS instance specs (legacy, was for IaaS scaling).
        :param volumes: Dict of volume definitions carrying dataset metadata.
        :param dockers: Dict of Docker image descriptors and usage metadata.
        """
        self.logger.debug('Kubernetes.set_experiments()')
        self.instance = None
        self.instances = instances
        self.volumes = volumes
        self.dockers = dockers

    def set_experiment(self, instance=None, volume=None, docker=None, script=None):
        """
        Select a specific instance/volume/docker/script combination for the experiment.

        :param instance: Instance key within ``self.instances`` (legacy IaaS).
        :param volume: Volume key within ``self.volumes``.
        :param docker: Docker image key within ``self.dockers``.
        :param script: Init-script key within the selected volume's ``initscripts``.
        """
        self.logger.debug('Kubernetes.set_experiment()')
        self.change_instance = True
        if instance is not None:
            self.instance_key = instance
        if volume is not None:
            self.volume_key = volume
            self.volume = self.volumes[self.volume_key]['id']
        if docker is not None:
            self.docker_key = docker
            self.docker = self.dockers[self.docker_key]
        if script is not None:
            self.script_key = script
            self.initscript = self.volumes[self.volume_key]['initscripts'][self.script_key]

    def wait(self, sec, silent=False):
        """
        Sleep for ``sec`` seconds, optionally printing progress messages.

        :param sec: Number of seconds to wait.
        :param silent: If ``True``, suppress all output.
        """
        intervals = int(sec)
        if not silent:
            print(f"{'- waiting ' + str(sec) + 's -':30s}: ", end="", flush=True)
        time.sleep(intervals)
        if not silent:
            print("done")

    def delete_deployment(self, deployment):
        """
        Delete a Kubernetes Deployment by name.

        :param deployment: Name of the Deployment to delete.
        """
        self.logger.debug('Kubernetes.delete_deployment()')
        self.kubectl('delete deployment ' + deployment)

    def get_deployments(self, app='', component='', experiment='', configuration=''):
        """
        Return names of Deployments matching the given label selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value (e.g. ``sut``, ``monitoring``).
        :param experiment: ``experiment`` label value (experiment code).
        :param configuration: ``configuration`` label value (DBMS config name).
        :return: List of Deployment names.
        """
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug(f'Kubernetes.get_deployments({label})')
        try:
            api_response = self.v1apps.list_namespaced_deployment(self.namespace, label_selector=label)
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling v1beta->list_namespaced_deployment: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)

    def get_pods(self, app='', component='', experiment='', configuration='', status=''):
        """
        Return names of Pods matching the given label selectors and optional phase.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param status: Pod phase to filter by (e.g. ``Running``, ``Succeeded``).
        :return: List of Pod names.
        """
        self.logger.debug('Kubernetes.get_pods()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        field_selector = 'status.phase=' + status if status else ''
        self.logger.debug(f'get_pods label({label})')
        try:
            api_response = self.v1core.list_namespaced_pod(
                self.namespace, label_selector=label, field_selector=field_selector
            )
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod for get_pods: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_pods(
                app=app, component=component, experiment=experiment,
                configuration=configuration, status=status
            )

    def get_stateful_sets(self, app='', component='', experiment='', configuration=''):
        """
        Return names of StatefulSets matching the given label selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :return: List of StatefulSet names.
        """
        self.logger.debug('Kubernetes.get_stateful_sets()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug('get_stateful_sets' + label)
        try:
            api_response = self.v1apps.list_namespaced_stateful_set(self.namespace, label_selector=label)
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling AppsV1Api->list_namespaced_stateful_set: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_stateful_sets(
                app=app, component=component, experiment=experiment, configuration=configuration
            )

    def get_nodes(self, app='', nodegroup_type='', nodegroup_name=''):
        """
        Return node objects matching the given label selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param nodegroup_type: ``type`` label value (e.g. ``sut``).
        :param nodegroup_name: ``name`` label value (e.g. ``sut_high_memory``).
        :return: List of Kubernetes node objects.
        """
        self.logger.debug('Kubernetes.get_nodes()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if nodegroup_type:
            label += ',type=' + nodegroup_type
        if nodegroup_name:
            label += ',name=' + nodegroup_name
        try:
            api_response = self.v1core.list_node(label_selector=label)
            if api_response.items:
                return api_response.items
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_node for get_nodes: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_nodes(
                app=app, nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name
            )

    def get_pod_status(self, pod, app=''):
        """
        Return the phase of a named Pod.

        :param pod: Pod name to look up.
        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :return: Phase string (e.g. ``Running``, ``Succeeded``) or ``""`` if not found.
        """
        self.logger.debug('Kubernetes.get_pod_status()')
        try:
            if not app:
                app = self.appname
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector='app=' + app)
            if api_response.items:
                for item in api_response.items:
                    if item.metadata.name == pod:
                        return item.status.phase
                return ""
            else:
                return ""
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod for get_pod_status: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_pod_status(pod=pod, app=app)

    def is_pod_ready(self, pod):
        """
        Return whether a Pod's ``Ready`` condition is ``True``.

        :param pod: Name of the Pod to check.
        :return: ``True`` if the Pod is ready, ``False`` otherwise.
        """
        self.logger.debug('Kubernetes.is_pod_ready()')
        try:
            api_response = self.v1core.read_namespaced_pod(name=pod, namespace=self.namespace)
            for condition in api_response.status.conditions:
                if condition.type == "Ready":
                    return condition.status == "True"
            return False
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->read_namespaced_pod for is_pod_ready: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.is_pod_ready(pod=pod)

    def get_pods_labels(self, app='', component='', experiment='', configuration=''):
        """
        Return a dict mapping Pod name to label dict for Pods matching the given selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :return: Dict ``{pod_name: labels_dict}``.
        """
        self.logger.debug('Kubernetes.get_pods_labels()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        pod_labels = {}
        try:
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label)
            if api_response.items:
                for item in api_response.items:
                    pod_labels[item.metadata.name] = item.metadata.labels
            return pod_labels
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod for get_pods_labels: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_pods_labels(
                app=app, component=component, experiment=experiment, configuration=configuration
            )

    def get_services(self, app='', component='', experiment='', configuration=''):
        """
        Return names of Services matching the given label selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :return: List of Service names.
        """
        self.logger.debug('Kubernetes.get_services()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug(f'get_services({label})')
        try:
            api_response = self.v1core.list_namespaced_service(self.namespace, label_selector=label)
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_service: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_services(
                app=app, component=component, experiment=experiment, configuration=configuration
            )

    def get_ports_of_service(self, app='', component='', experiment='', configuration=''):
        """
        Return the port numbers exposed by the first Service matching the given selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :return: List of port number strings from the first matched Service.
        """
        self.logger.debug('Kubernetes.get_ports_of_service()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug('get_ports_of_service' + label)
        try:
            api_response = self.v1core.list_namespaced_service(self.namespace, label_selector=label)
            if api_response.items:
                return [str(p.port) for p in api_response.items[0].spec.ports]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_service: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_ports_of_service(
                app=app, component=component, experiment=experiment, configuration=configuration
            )

    def get_pvc(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return names of PersistentVolumeClaims matching the given selectors.

        If ``pvc`` is provided, only the entry with that exact name is returned.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param pvc: Optional PVC name to filter by.
        :return: List of PVC names.
        """
        self.logger.debug('Kubernetes.get_pvc()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug(f'get_pvc({label})')
        try:
            api_response = self.v1core.list_namespaced_persistent_volume_claim(
                self.namespace, label_selector=label
            )
            if pvc:
                return [p.metadata.name for p in api_response.items if p.metadata.name == pvc]
            else:
                return [p.metadata.name for p in api_response.items]
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_pvc(
                app=app, component=component, experiment=experiment, configuration=configuration
            )

    def pvc_exists(self, name):
        """
        Return whether a PVC with the given name exists in the namespace.

        :param name: Name of the PVC to check.
        :return: ``True`` if the PVC exists, ``False`` if not found (HTTP 404).
        """
        self.logger.debug('Kubernetes.pvc_exists()')
        try:
            self.v1core.read_namespaced_persistent_volume_claim(
                namespace=self.namespace, name=name
            )
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            else:
                print(f"Exception when calling CoreV1Api->read_namespaced_persistent_volume_claim: {e}\n")
                self.cluster_access()
                self.wait(2)
                return self.pvc_exists(name=name)

    def get_pvc_labels(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return label dicts of PVCs matching the given selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param pvc: Optional PVC name to filter by.
        :return: List of label dicts.
        """
        self.logger.debug('Kubernetes.get_pvc_labels()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug('get_pvc' + label)
        try:
            api_response = self.v1core.list_namespaced_persistent_volume_claim(
                self.namespace, label_selector=label
            )
            if api_response.items:
                if pvc:
                    return [p.metadata.labels for p in api_response.items if p.metadata.name == pvc]
                else:
                    return [p.metadata.labels for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_pvc_labels(
                app=app, component=component, experiment=experiment,
                configuration=configuration, pvc=pvc
            )

    def get_pvc_specs(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return spec objects of PVCs matching the given selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param pvc: Optional PVC name to filter by.
        :return: List of PVC spec objects.
        """
        self.logger.debug('Kubernetes.get_pvc_specs()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug('get_pvc' + label)
        try:
            api_response = self.v1core.list_namespaced_persistent_volume_claim(
                self.namespace, label_selector=label
            )
            if api_response.items:
                if pvc:
                    return [p.spec for p in api_response.items if p.metadata.name == pvc]
                else:
                    return [p.spec for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_pvc_specs(
                app=app, component=component, experiment=experiment,
                configuration=configuration, pvc=pvc
            )

    def get_pvc_status(self, app='', component='', experiment='', configuration='', pvc=''):
        """
        Return status objects of PVCs matching the given selectors.

        When ``pvc`` is given, returns the ``status`` of the matching PVC;
        otherwise returns the ``spec`` of all matched PVCs.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param pvc: Optional PVC name to filter by (returns ``status`` for match).
        :return: List of PVC status or spec objects.
        """
        self.logger.debug('Kubernetes.get_pvc_status()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        self.logger.debug('get_pvc' + label)
        try:
            api_response = self.v1core.list_namespaced_persistent_volume_claim(
                self.namespace, label_selector=label
            )
            if api_response.items:
                if pvc:
                    return [p.status for p in api_response.items if p.metadata.name == pvc]
                else:
                    return [p.spec for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_pvc_status(
                app=app, component=component, experiment=experiment,
                configuration=configuration, pvc=pvc
            )

    def get_stateful_set_pods(self, stateful_set=''):
        """
        Return names of Pods belonging to a given StatefulSet.

        :param stateful_set: Name of the StatefulSet.
        :return: List of Pod names.
        """
        self.logger.debug('Kubernetes.get_stateful_set_pods()')
        label = f"statefulset.kubernetes.io/pod-name={stateful_set}"
        self.logger.debug('get_stateful_set_pods' + label)
        try:
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label)
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.get_stateful_set_pods(stateful_set=stateful_set)

    def delete_stateful_set(self, name):
        """
        Delete a StatefulSet by name.

        :param name: Name of the StatefulSet to delete.
        """
        self.logger.debug(f'Kubernetes.delete_stateful_set({name})')
        body = kubernetes_client.V1DeleteOptions()
        try:
            self.v1apps.delete_namespaced_stateful_set(name, self.namespace, body=body)
        except ApiException as e:
            print(f"Exception when calling AppsV1Api->delete_namespaced_stateful_set: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.delete_stateful_set(name=name)

    def delete_pod(self, name):
        """
        Delete a Pod by name.  A 404 (already gone) is silently ignored.

        :param name: Name of the Pod to delete.
        """
        self.logger.debug(f'Kubernetes.delete_pod({name})')
        body = kubernetes_client.V1DeleteOptions()
        try:
            self.v1core.delete_namespaced_pod(name, self.namespace, body=body)
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->delete_namespaced_pod: {e}\n")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.delete_pod(name=name)

    def delete_pvc(self, name):
        """
        Delete a PersistentVolumeClaim by name.

        :param name: Name of the PVC to delete.
        :return: ``True`` if deleted successfully, ``False`` on error.
        """
        self.logger.debug(f'Kubernetes.delete_pvc({name})')
        body = kubernetes_client.V1DeleteOptions()
        try:
            self.v1core.delete_namespaced_persistent_volume_claim(name, self.namespace, body=body)
            return True
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: {e}\n")
            self.cluster_access()
            self.wait(2)
            return False

    def delete_service(self, name):
        """
        Delete a Service by name.

        :param name: Name of the Service to delete.
        """
        self.logger.debug(f'Kubernetes.delete_service({name})')
        body = kubernetes_client.V1DeleteOptions()
        try:
            self.v1core.delete_namespaced_service(name, self.namespace, body=body)
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->delete_namespaced_service: {e}\n")
            self.cluster_access()
            self.wait(2)
            return self.delete_service(name=name)

    def _old_start_port_forwarding(self, service='', app='', component='sut'):
        """
        .. deprecated::
            Legacy port-forwarding helper.  Not used in the current Kubernetes flow.
        """
        self.logger.debug('Kubernetes.startPortforwarding()')
        ports = self.get_ports_of_service(app=app, component=component)
        if not service:
            service = self.service
        if not service:
            service = 'bexhoma-service'
        self.getInfo(component='sut')
        if self.deployments:
            forward = [
                'kubectl',
                f'--context {self.context}',
                'port-forward',
                'service/' + service,
            ]
            forward.extend(ports)
            your_command = " ".join(forward)
            subprocess.Popen(your_command, stdout=subprocess.PIPE, shell=True)

    def _old_get_child_processes(self):
        """
        .. deprecated::
            Legacy helper for enumerating child processes.  Not used.
        """
        self.logger.debug('Kubernetes.getChildProcesses()')
        current_process = psutil.Process()
        children = current_process.children(recursive=False)

    def _old_stop_port_forwarding(self):
        """
        .. deprecated::
            Legacy helper for stopping kubectl port-forward processes.  Not used.
        """
        self.logger.debug('Kubernetes.stopPortforwarding()')
        children = [
            p for p in psutil.process_iter(attrs=['pid', 'name'])
            if 'kubectl' in p.info['name']
        ]
        for child in children:
            try:
                self.logger.debug(
                    f'Kubernetes.stopPortforwarding() - Child {child.pid} {child.name}'
                )
                command = child.cmdline()
                if command and command[3] == 'port-forward':
                    self.logger.debug(
                        f'Kubernetes.stopPortforwarding() - Found child {child.name}'
                    )
                    child.terminate()
            except Exception as e:
                print(e)

    def create_object_from_file(self, filename_source):
        """
        Apply a Kubernetes manifest file via ``kubectl create``.

        The manifest is copied to the experiment result folder with the
        ``BEXHOMA_PACKAGE_VERSION`` placeholder substituted, then applied.

        :param filename_source: Path to the source manifest template file.
        """
        filename = Path(filename_source)
        path = Path(self.config['benchmarker']['resultfolder']) / self.code
        filename_replaced = path / filename.name
        if os.path.isfile(filename_source):
            with open(filename_source, "r") as template:
                data = template.read()
                data = data.replace("BEXHOMA_PACKAGE_VERSION", __version__)
                with open(filename_replaced, "w") as template_filled:
                    template_filled.write(data)
            self.kubectl('create -f ' + filename_replaced.as_posix())
            self.logger.debug(
                f"Copied manifest from {filename_source} to {filename_replaced.as_posix()} and run it"
            )
        else:
            print(f"Manifest not found: {filename_source}")
            exit()

    def kubectl(self, command):
        """
        Run a ``kubectl`` command in the configured context.

        Decodes output using UTF-8, Latin-1, or CP-1252 (in that order).
        On an ``Unauthorized`` response the access token is refreshed and the
        command is retried once.

        :param command: kubectl subcommand string (without ``kubectl --context ...`` prefix).
        :return: Decoded stdout string, or ``None`` on failure.
        """
        def run_with_fallback(fullcommand):
            encodings = ["utf-8", "latin1", "cp1252"]
            try:
                raw = subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print("Command failed!")
                print(f"Return code: {e.returncode}")
                print(f"Command: {e.cmd}")
                if e.output:
                    print("Raw output (bytes):", e.output)
                    for enc in encodings:
                        try:
                            print(f"Decoded with {enc}:")
                            print(e.output.decode(enc))
                            break
                        except UnicodeDecodeError:
                            continue
                    if b'Unauthorized' in e.output:
                        print("Create new access token")
                        self.cluster_access()
                        self.wait(2)
                        return run_with_fallback(fullcommand)
                return None
            except Exception as e:
                print("Unexpected error while running subprocess!")
                print("Exception type:", type(e).__name__)
                print("Exception message:", str(e))
                print("Traceback:")
                traceback.print_exc()
                return None
            for enc in encodings:
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            print("Failed to decode output with any known encoding")
            return None

        fullcommand = f'kubectl --context {self.context} {command}'
        self.logger.debug(f'Kubernetes.kubectl({fullcommand})')
        return run_with_fallback(fullcommand)

    def execute_command_in_pod(self, command, pod='', container='', params=''):
        """
        Execute a shell command inside a container of a running Pod.

        Retries automatically on transient ``error dialing backend`` failures.

        :param command: Shell command string.
        :param pod: Name of the target Pod.
        :param container: Container name within the Pod (optional for single-container pods).
        :param params: Unused; reserved for future use.
        :return: Tuple ``("", stdout_str, stderr_str)``.
        """
        if not pod:
            self.logger.debug(
                f'Kubernetes.execute_command_in_pod({command}): empty pod name given for command'
            )
            return "", "", ""
        command_clean = command.replace('"', '\\"')
        if container:
            fullcommand = (
                f'kubectl --context {self.context} exec {pod} --container={container} -- sh -c "{command_clean}"'
            )
        else:
            fullcommand = (
                f'kubectl --context {self.context} exec {pod} -- sh -c "{command_clean}"'
            )
        self.logger.debug(f'Kubernetes.execute_command_in_pod({fullcommand})')
        proc = subprocess.Popen(
            fullcommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = proc.communicate()
        try:
            str_stdout = stdout.decode('utf-8')
            str_stderr = stderr.decode('utf-8')
            if (
                'Error from server: error dialing backend' in str_stdout
                or 'Error from server: error dialing backend' in str_stderr
            ):
                print("Connection error found")
                self.wait(5)
                return self.execute_command_in_pod(
                    command=command, pod=pod, container=container, params=params
                )
            else:
                return "", str_stdout, str_stderr
        except Exception as e:
            print(e)
            print(stdout, stderr)
            str_stdout = stdout.decode('utf-8')
            str_stderr = stderr.decode('utf-8')
            if (
                'Error from server: error dialing backend' in str_stdout
                or 'Error from server: error dialing backend' in str_stderr
            ):
                print("Connection error found")
                self.wait(5)
                return self.execute_command_in_pod(
                    command=command, pod=pod, container=container, params=params
                )
            else:
                return "", stdout, stderr

    def upload_file(self, filename_remote, filename_local, pod, container="dashboard"):
        """
        Upload a local file into a Pod container using ``kubectl cp``.

        On Windows the local path is converted to a UNC path first.

        :param filename_remote: Destination path inside the container.
        :param filename_local: Source path on the local machine.
        :param pod: Target Pod name.
        :param container: Target container name.  Defaults to ``dashboard``.
        :return: Output of the kubectl command.
        """
        filename_local = to_unc(filename_local)
        cmd = f'cp "{filename_local}" {pod}:{filename_remote} -c {container}'
        return self.kubectl(cmd)

    def download_file(self, filename_remote, filename_local, pod, container="dashboard"):
        """
        Download a file from a Pod container to the local machine using ``kubectl cp``.

        On Windows the local destination path is converted to a UNC path first.

        :param filename_remote: Source path inside the container.
        :param filename_local: Destination path on the local machine.
        :param pod: Source Pod name.
        :param container: Source container name.  Defaults to ``dashboard``.
        :return: Output of the kubectl command.
        """
        filename_local = to_unc(filename_local)
        cmd = f'cp {pod}:{filename_remote} "{filename_local}" -c {container}'
        return self.kubectl(cmd)

    def check_dbms_connection(self, ip, port):
        """
        Test whether a TCP connection to ``ip:port`` can be established.

        Used to probe DBMS readiness before starting a benchmark.

        :param ip: Hostname or IP address to connect to.
        :param port: TCP port number.
        :return: ``True`` if the connection succeeded, ``False`` otherwise.
        """
        found = False
        s = socket.socket()
        s.settimeout(10)
        try:
            s.connect((ip, port))
            found = True
            print(f"Somebody is answering at {ip}:{port}")
        except Exception:
            print(f"Nobody is answering yet at {ip}:{port}")
        finally:
            s.close()
        return found

    def _old_get_timediff(self):
        """
        .. deprecated::
            Legacy helper for measuring clock skew between local host and a remote pod.
            Not used in the current flow.
        """
        print("getTimediff")
        command = 'date +"%s"'
        fullcommand = 'kubectl exec ' + cluster.activepod + ' --container=dbms -- bash -c "' + command + '"'
        timestamp_remote = os.popen(fullcommand).read()
        timestamp_local = os.popen(command).read()
        return int(timestamp_remote) - int(timestamp_local)

    def _old_continue_benchmarks(self, connection=None, query=None):
        """
        .. deprecated::
            Legacy method for resuming a DBMSBenchmarker run from a saved result folder.
            Not used in the current experiment flow.
        """
        self.connection = connection
        self.resultfolder = self.config['benchmarker']['resultfolder']
        resultfolder = self.resultfolder + '/' + str(self.code)
        connectionfile = resultfolder + '/connections.config'
        queryfile = resultfolder + '/queries.config'
        self.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            fixedQuery=query,
            result_path=resultfolder,
            batch=True,
            working='connection'
        )
        self.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        self.benchmark.continueBenchmarks(overwrite=False)
        self.code = self.benchmark.code
        self.copyInits()
        self.copyLog()
        self.downloadLog()
        self.benchmark.reporter.append(benchmarker.reporter.metricer(self.benchmark))
        evaluator.evaluator(self.benchmark, load=False, force=True)
        return self.code

    def _old_run_reporting(self):
        """
        .. deprecated::
            Legacy reporting trigger.  Not used in the current experiment flow.
        """
        evaluator.evaluator(self.benchmark, load=False, force=True)
        self.benchmark.generateReportsAll()

    def _old_copy_log(self):
        """
        .. deprecated::
            Legacy helper for copying the DBMS log file inside a pod.  Not used.
        """
        print("copyLog")
        if len(self.docker['logfile']):
            cmd_prepare = 'mkdir /data/' + str(self.code)
            self.execute_command_in_pod(cmd_prepare, container='dbms')
            cmd_save = (
                'cp ' + self.docker['logfile']
                + ' /data/' + str(self.code) + '/' + self.connection + '.log'
            )
            self.execute_command_in_pod(cmd_save, container='dbms')

    def _old_copy_inits(self):
        """
        .. deprecated::
            Legacy helper for copying init-script logs inside a pod.  Not used.
        """
        print("copyInits")
        cmd_prepare = 'mkdir /data/' + str(self.code)
        self.execute_command_in_pod(cmd_prepare, container='dbms')
        scriptfolder = f'/data/{self.experiments_configfolder}/{self.docker_key}/'
        for idx, script in enumerate(self.initscript):
            cmd_copy = (
                f'cp {scriptfolder + script}'
                + f' /data/{self.code}/{self.connection}_init_{idx}.log'
            )
            self.execute_command_in_pod(cmd_copy, container='dbms')

    def pod_description(self, pod, container=''):
        """
        Return the ``kubectl describe pod`` output for a given Pod.

        The ``container`` parameter is accepted for API compatibility but is not
        forwarded to kubectl (describe is not container-sensitive).

        :param pod: Name of the Pod to describe.
        :param container: Ignored; kept for API compatibility.
        :return: kubectl output string.
        """
        container = ''  # describe pod is not container-sensitive
        if container:
            fullcommand = 'describe pod ' + pod + ' --container=' + container
        else:
            fullcommand = 'describe pod ' + pod
        return self.kubectl(fullcommand)

    def pod_log(self, pod, container=''):
        """
        Return the ``kubectl logs`` output for a given Pod or container.

        :param pod: Name of the Pod.
        :param container: Container name within the Pod (optional).
        :return: kubectl output string.
        """
        if container:
            fullcommand = 'logs ' + pod + ' --container=' + container
        else:
            fullcommand = 'logs ' + pod
        return self.kubectl(fullcommand)

    def get_pod_containers(self, pod):
        """
        Return the names of all containers and init-containers in a Pod.

        :param pod: Name of the Pod.
        :return: List of container name strings (regular containers + init containers).
        """
        fullcommand = 'get pods ' + pod + ' -o jsonpath="{.spec.containers[*].name}"'
        output = self.kubectl(fullcommand)
        containers = output.split(" ")
        fullcommand = 'get pods ' + pod + ' -o jsonpath="{.spec.initContainers[*].name}"'
        output = self.kubectl(fullcommand)
        init_containers = output.split(" ")
        self.logger.debug(f"Pod {pod} has container {containers + init_containers}")
        return containers + init_containers

    def _old_download_log(self):
        """
        .. deprecated::
            Legacy helper for downloading pod logs via ``kubectl cp``.  Not used.
        """
        print("downloadLog")
        self.kubectl(
            'cp --container dbms ' + self.activepod
            + ':/data/' + str(self.code) + '/ '
            + self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
            + "/" + str(self.code)
        )

    def get_jobs(self, app='', component='', experiment='', configuration='', client=''):
        """
        Return names of Jobs matching the given label selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param client: ``client`` label value (legacy, may be unused).
        :return: List of Job names, or ``None`` on a 404 error.
        """
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        if client:
            label += ',client=' + client
        self.logger.debug(f'getJobs({label})')
        try:
            api_response = self.v1batches.list_namespaced_job(self.namespace, label_selector=label)
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling BatchV1Api->list_namespaced_job: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.get_jobs(
                    app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )

    def get_jobs_labels(self, app='', component='', experiment='', configuration='', client=''):
        """
        Return a dict mapping Job name to label dict for Jobs matching the given selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param client: ``client`` label value (legacy).
        :return: Dict ``{job_name: labels_dict}``, or ``[]`` if no Jobs found.
        """
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        if client:
            label += ',client=' + client
        self.logger.debug('get_jobs_labels ' + label)
        job_labels = {}
        try:
            api_response = self.v1batches.list_namespaced_job(self.namespace, label_selector=label)
            if api_response.items:
                for item in api_response.items:
                    job_labels[item.metadata.name] = item.metadata.labels
                return job_labels
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling BatchV1Api->list_namespaced_job: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.get_jobs_labels(
                    app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )

    def get_job_status(self, jobname='', app='', component='', experiment='', configuration='', client=''):
        """
        Return the completion status of a Job.

        If ``jobname`` is empty, the first Job matching the given selectors is used.
        Returns ``True`` if the completion count has been reached, ``0`` if
        in-progress or on error, ``"no job"`` if no matching Job was found.

        :param jobname: Name of the Job (optional).
        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param client: ``client`` label value (legacy).
        :return: ``True``, ``0``, or ``"no job"``.
        """
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        if client:
            label += ',client=' + client
        self.logger.debug('getJobStatus ' + label)
        try:
            if not jobname:
                jobs = self.get_jobs(
                    app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )
                if not jobs:
                    return "no job"
                jobname = jobs[0]
            api_response = self.v1batches.read_namespaced_job_status(jobname, self.namespace)
            self.logger.debug(f"api_response.spec.completions {api_response.spec.completions}")
            self.logger.debug(f"api_response.status.succeeded {api_response.status.succeeded}")
            if (
                api_response.status.succeeded is not None
                and api_response.spec.completions <= api_response.status.succeeded
            ):
                self.logger.debug("Number of completions reached")
                return True
            if (
                api_response.status.succeeded is not None
                and api_response.status.succeeded > 0
                and api_response.status.conditions is not None
                and api_response.status.conditions
            ):
                self.logger.debug(api_response.status.conditions[0].type)
                return api_response.status.conditions[0].type == 'Complete'
            else:
                return 0
        except ApiException as e:
            print(f"Exception when calling BatchV1Api->read_namespaced_job_status: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.get_job_status(
                    jobname=jobname, app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )
            else:
                return 0

    def delete_job(self, jobname='', app='', component='', experiment='', configuration='', client=''):
        """
        Delete a Job by name or by matching label selectors.

        If ``jobname`` is empty, the first Job matching the given selectors is deleted.

        :param jobname: Name of the Job to delete (optional).
        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param client: ``client`` label value (legacy).
        :return: ``True`` on success, or ``None`` if the Job was not found.
        """
        self.logger.debug('Kubernetes.delete_job()')
        try:
            if not jobname:
                jobs = self.get_jobs(
                    app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )
                jobname = jobs[0]
            self.logger.debug(f'Kubernetes.delete_job({jobname})')
            self.v1batches.delete_namespaced_job(jobname, self.namespace)
            return True
        except ApiException as e:
            print(f"Exception when calling BatchV1Api->delete_namespaced_job: {e}\n")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.delete_job(
                    jobname=jobname, app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )

    def delete_job_pods(self, jobname='', app='', component='', experiment='', configuration='', client=''):
        """
        Delete all Pods of a Job identified by name or by matching label selectors.

        If ``jobname`` is empty, all Pods matching the given selectors are deleted
        individually by recursing with their names.

        :param jobname: Pod or Job name (optional).
        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param client: ``client`` label value (legacy).
        """
        self.logger.debug('Kubernetes.delete_job_pods()')
        body = kubernetes_client.V1DeleteOptions()
        try:
            if not jobname:
                pods = self.get_job_pods(
                    app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )
                if pods:
                    for pod in pods:
                        self.delete_job_pods(
                            jobname=pod, app=app, component=component, experiment=experiment,
                            configuration=configuration, client=client
                        )
                    return
            self.logger.debug(f'Kubernetes.delete_job_pods({jobname})')
            self.v1core.delete_namespaced_pod(jobname, self.namespace, body=body)
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->delete_namespaced_pod: {e}\n")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.delete_job_pods(
                    jobname=jobname, app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )

    def get_job_pods(self, app='', component='', experiment='', configuration='', client=''):
        """
        Return names of Pods belonging to Jobs matching the given label selectors.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param component: ``component`` label value.
        :param experiment: ``experiment`` label value.
        :param configuration: ``configuration`` label value.
        :param client: ``client`` label value (legacy).
        :return: List of Pod names, or ``None`` on a 404 error.
        """
        if not app:
            app = self.appname
        label = 'app=' + app
        if component:
            label += ',component=' + component
        if experiment:
            label += ',experiment=' + experiment
        if configuration:
            label += ',configuration=' + configuration
        if client:
            label += ',client=' + client
        self.logger.debug('getJobPods ' + label)
        try:
            api_response = self.v1core.list_namespaced_pod(self.namespace, label_selector=label)
            if api_response.items:
                return [p.metadata.name for p in api_response.items]
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod for getJobPods: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            if e.status != 404:
                return self.get_job_pods(
                    app=app, component=component, experiment=experiment,
                    configuration=configuration, client=client
                )

    def get_dashboard_name(self, app='', component='dashboard'):
        """
        Build a canonical name string for the dashboard component.

        :param app: App name.  Defaults to ``self.appname``.
        :param component: Component label.  Defaults to ``dashboard``.
        :return: Name string in the format ``<app>_<component>``.
        """
        if not app:
            app = self.appname
        name = f"{app}_{component}"
        self.logger.debug(f'Kubernetes.get_dashboard_name({name})')
        return name

    def get_messagequeue_name(self, app='', component='messagequeue'):
        """
        Build a canonical name string for the message-queue component.

        :param app: App name.  Defaults to ``self.appname``.
        :param component: Component label.  Defaults to ``messagequeue``.
        :return: Name string in the format ``<app>_<component>``.
        """
        if not app:
            app = self.appname
        name = f"{app}_{component}"
        self.logger.debug(f'Kubernetes.create_messagequeue({name})')
        return name

    def is_dashboard_running(self):
        """
        Return whether the dashboard Pod exists and is in the ``Running`` phase.

        :return: ``True`` if the dashboard is running.
        """
        pod_dashboard = self.get_dashboard_pod_name(app=self.appname, component='dashboard')
        if pod_dashboard:
            self.logger.debug('Kubernetes.is_dashboard_running()=exists')
            status = self.get_pod_status(pod_dashboard)
            if status == "Running":
                self.logger.debug('Kubernetes.is_dashboard_running() is running')
                return True
        return False

    def start_dashboard(self, app='', component='dashboard'):
        """
        Start the dashboard Deployment and its Service if not already running.

        Manifest template: ``deploymenttemplate-bexhoma-dashboard.yml``.

        :param app: App name passed to :meth:`get_dashboard_name`.
        :param component: Component label.  Defaults to ``dashboard``.
        """
        if len(self.get_dashboard_pod_name()):
            print(f"{'Dashboard':30s}: is running")
            return
        print(f"{'Dashboard':30s}: is starting...", end="", flush=True)
        deployment = 'deploymenttemplate-bexhoma-dashboard.yml'
        self.get_dashboard_name(app, component)
        self.logger.debug(f'Kubernetes.start_dashboard({deployment})')
        self.create_object_from_file(self.yamlfolder + deployment)
        while not self.is_dashboard_running():
            self.wait(10, silent=True)
        print("done")

    def is_monitoring_healthy(self):
        """
        Probe Prometheus by issuing a ``query_range`` request from inside the dashboard pod.

        Queries ``sum(node_memory_MemTotal_bytes)`` over a 5-minute window ending
        4 minutes ago.  Returns ``True`` if Prometheus responds with HTTP 200.

        :return: ``True`` if Prometheus is reachable and healthy.
        """
        self.logger.debug('Kubernetes.is_monitoring_healthy()')
        config_k8s = self.config['credentials']['k8s']
        if 'service_monitoring' in config_k8s['monitor']:
            url = config_k8s['monitor']['service_monitoring'].format(
                namespace=self.contextdata['namespace'], service="monitoring"
            )
            query = "sum(node_memory_MemTotal_bytes)"
            safe_query = urllib.parse.quote_plus(query)
            try:
                pod_dashboard = self.get_dashboard_pod_name()
                self.logger.debug(f'Inside pod {pod_dashboard}')
                now = datetime.utcnow()
                start = now - timedelta(seconds=300)
                end = now - timedelta(seconds=240)
                query_url = (
                    f"{url}query_range?query={safe_query}"
                    f"&start={int(start.timestamp())}&end={int(end.timestamp())}&step=60"
                )
                self.logger.debug(f'Test URL {query_url}')
                command = f"curl -L --max-time 10 -is '{query_url}' | head -n 1 | cut -d ' ' -f2"
                self.logger.debug(f'Command {command}')
                _, stdout, _ = self.execute_command_in_pod(
                    pod=pod_dashboard, command=command, container="dashboard"
                )
                status = stdout
                self.logger.debug(f'Status {status}')
                if status:
                    return int(status) == 200
                return False
            except Exception as e:
                print(e)
                return False

    def start_monitoring_cluster(self, app='', component='monitoring'):
        """
        Start cluster-level monitoring (Prometheus + node exporters) if not healthy.

        Waits up to 100 seconds for an existing Prometheus to become healthy before
        deploying the daemonset.  Manifest template: ``daemonsettemplate-monitoring.yml``.

        :param app: App name (unused; kept for API consistency).
        :param component: Component label.  Defaults to ``monitoring``.
        """
        self.monitor_cluster_active = True
        self.monitor_cluster_exists = self.is_monitoring_healthy()
        if self.monitor_cluster_exists:
            return
        # Give an existing Prometheus up to 100 s to become healthy before deploying
        for _ in range(10):
            self.wait(10, silent=True)
            self.monitor_cluster_exists = self.is_monitoring_healthy()
            if self.monitor_cluster_exists:
                return
        endpoints = self.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
        if endpoints:
            self.logger.debug('Kubernetes.start_monitoring_cluster()=exists')
            print(f"{'Cluster monitoring':30s}: is running")
            return
        self.logger.debug('Kubernetes.start_monitoring_cluster()=deploy')
        deployment = 'daemonsettemplate-monitoring.yml'
        self.create_object_from_file(self.yamlfolder + deployment)
        print(f"{'Cluster monitoring':30s}: starting...")
        while not len(self.get_service_endpoints(service_name="bexhoma-service-monitoring-default")):
            self.wait(10, silent=True)
        print("done")

    def is_messagequeue_running(self, component='messagequeue'):
        """
        Return whether the message-queue Pod exists and is in the ``Running`` phase.

        :param component: Component label to query.  Defaults to ``messagequeue``.
        :return: ``True`` if the message queue is running.
        """
        pods_messagequeue = self.get_pods(component=component)
        if pods_messagequeue:
            pod_messagequeue = pods_messagequeue[0]
            self.logger.debug('Kubernetes.is_messagequeue_running()=exists')
            status = self.get_pod_status(pod_messagequeue)
            if status == "Running":
                self.logger.debug('Kubernetes.is_messagequeue_running() is running')
                return True
        return False

    def start_messagequeue(self, app='', component='messagequeue'):
        """
        Start the message-queue Deployment if not already running.

        Manifest template: ``deploymenttemplate-bexhoma-messagequeue.yml``.

        :param app: App name passed to :meth:`get_messagequeue_name`.
        :param component: Component label.  Defaults to ``messagequeue``.
        """
        pods_messagequeue = self.get_pods(component=component)
        if pods_messagequeue:
            self.logger.debug('Kubernetes.start_messagequeue()=exists')
            print(f"{'Message Queue':30s}: is running")
            return
        print(f"{'Message Queue':30s}: is starting...", end="", flush=True)
        deployment = 'deploymenttemplate-bexhoma-messagequeue.yml'
        self.get_messagequeue_name(app, component)
        self.logger.debug(f'Kubernetes.start_messagequeue({deployment})')
        self.create_object_from_file(self.yamlfolder + deployment)
        while not self.is_messagequeue_running():
            self.wait(10, silent=True)
        print("done")

    def start_datadir(self):
        """
        Provision the shared data-source PVC if it does not exist.

        The PVC is used by data-generator pods for writing and by loader pods
        for reading.  Manifest template: ``pvc-bexhoma-data.yml``.
        """
        app = self.appname
        pvcs = self.get_pvc(app=app, component='data-source', experiment='', configuration='')
        if pvcs:
            print(f"{'Data Directory':30s}: is running")
            return
        print(f"{'Data Directory':30s}: is starting...", end="", flush=True)
        deployment = 'pvc-bexhoma-data.yml'
        self.create_object_from_file(self.yamlfolder + deployment)
        while not len(self.get_pvc(app=app, component='data-source', experiment='', configuration='')):
            self.wait(10, silent=True)
        print("done")

    def start_resultdir(self):
        """
        Provision the shared results PVC if it does not exist.

        Benchmarker pods write results here; the evaluator pod reads from here.
        Collected metrics are also stored here.
        Manifest template: ``pvc-bexhoma-results.yml``.
        """
        app = self.appname
        pvcs = self.get_pvc(app=app, component='results', experiment='', configuration='')
        if pvcs:
            print(f"{'Result Directory':30s}: is running")
            return
        print(f"{'Result Directory':30s}: is starting...", end="", flush=True)
        deployment = 'pvc-bexhoma-results.yml'
        self.create_object_from_file(self.yamlfolder + deployment)
        while not len(self.get_pvc(app=app, component='results', experiment='', configuration='')):
            self.wait(10, silent=True)
        print("done")

    def get_dashboard_pod_name(self, app='', component='dashboard'):
        """
        Return the name of the dashboard Pod, or ``""`` if none exists.

        :param app: App name (passed to :meth:`get_pods`; unused if empty).
        :param component: Component label.  Defaults to ``dashboard``.
        :return: Pod name string, or ``""`` if no dashboard Pod was found.
        """
        pods_dashboard = self.get_pods(component=component)
        if pods_dashboard:
            self.logger.debug('Kubernetes.get_dashboard_pod_name()=exists')
            return pods_dashboard[0]
        self.logger.debug('Kubernetes.get_dashboard_pod_name()=not exists')
        return ""

    def restart_dashboard(self, app='', component='dashboard'):
        """
        Force-restart the dashboard by deleting its Pod (Kubernetes will recreate it).

        :param app: App name (passed to :meth:`get_dashboard_pod_name`).
        :param component: Component label.  Defaults to ``dashboard``.
        """
        self.logger.debug('Kubernetes.restart_dashboard()')
        pod_dashboard = self.get_dashboard_pod_name(app=app, component=component)
        if pod_dashboard:
            self.delete_pod(pod_dashboard)

    def stop_dashboard(self, app='', component='dashboard'):
        """
        Stop the dashboard Deployment and its Service.

        :param app: ``app`` label value.  Defaults to ``self.appname`` via sub-calls.
        :param component: ``component`` label value.  Defaults to ``dashboard``.
        """
        self.logger.debug('Kubernetes.stop_dashboard()')
        for deployment in self.get_deployments(app=app, component=component):
            self.delete_deployment(deployment)
        for service in self.get_services(app=app, component=component):
            self.delete_service(service)

    def stop_maintaining(self, experiment='', configuration=''):
        """
        Stop all maintaining Jobs and their Pods in the cluster.

        :param experiment: Filter by experiment code (optional).
        :param configuration: Filter by DBMS configuration name (optional).
        """
        app = self.appname
        component = 'maintaining'
        jobs = self.get_jobs(app, component, experiment, configuration)
        for job in jobs:
            success = self.get_job_status(job)
            self.logger.debug(f"Job and status {job} {success}")
            self.delete_job(job)
        pods = self.get_job_pods(app, component, experiment, configuration)
        for pod in pods:
            status = self.get_pod_status(pod)
            print(pod, status)
            self.delete_pod(pod)

    def stop_loading(self, experiment='', configuration=''):
        """
        Stop all loading Jobs and their Pods in the cluster.

        :param experiment: Filter by experiment code (optional).
        :param configuration: Filter by DBMS configuration name (optional).
        """
        app = self.appname
        component = 'loading'
        jobs = self.get_jobs(app, component, experiment, configuration)
        for job in jobs:
            success = self.get_job_status(job)
            print(job, success)
            self.delete_job(job)
        pods = self.get_job_pods(app, component, experiment, configuration)
        for pod in pods:
            status = self.get_pod_status(pod)
            print(pod, status)
            self.delete_pod(pod)

    def stop_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Stop all monitoring Deployments and their Services in the cluster.

        :param app: ``app`` label value.
        :param component: Component label.  Defaults to ``monitoring``.
        :param experiment: Filter by experiment code (optional).
        :param configuration: Filter by DBMS configuration name (optional).
        """
        for deployment in self.get_deployments(
            app=app, component=component, experiment=experiment, configuration=configuration
        ):
            self.delete_deployment(deployment)
        for service in self.get_services(
            app=app, component=component, experiment=experiment, configuration=configuration
        ):
            self.delete_service(service)

    def stop_sut(self, app='', component='sut', experiment='', configuration=''):
        """
        Stop all SUT Deployments, StatefulSets, and Services in the cluster.

        When ``component='sut'``, worker and pool sub-components are recursively stopped.

        :param app: ``app`` label value.
        :param component: Component label.  Defaults to ``sut``.
        :param experiment: Filter by experiment code (optional).
        :param configuration: Filter by DBMS configuration name (optional).
        """
        for deployment in self.get_deployments(
            app=app, component=component, experiment=experiment, configuration=configuration
        ):
            self.delete_deployment(deployment)
        for service in self.get_services(
            app=app, component=component, experiment=experiment, configuration=configuration
        ):
            self.delete_service(service)
        for stateful_set in self.get_stateful_sets(
            app=app, component=component, experiment=experiment, configuration=configuration
        ):
            self.delete_stateful_set(stateful_set)
        if component == 'sut':
            self.stop_sut(app=app, component='worker', experiment=experiment, configuration=configuration)
            self.stop_sut(app=app, component='pool', experiment=experiment, configuration=configuration)

    def stop_benchmarker(self, experiment='', configuration=''):
        """
        Stop all benchmarker Jobs and their Pods in the cluster.

        :param experiment: Filter by experiment code (optional).
        :param configuration: Filter by DBMS configuration name (optional).
        """
        app = self.appname
        component = 'benchmarker'
        jobs = self.get_jobs(app, component, experiment, configuration)
        for job in jobs:
            success = self.get_job_status(job)
            print(job, success)
            self.delete_job(job)
        pods = self.get_job_pods(app, component, experiment, configuration)
        for pod in pods:
            status = self.get_pod_status(pod)
            print(pod, status)
            self.delete_pod(pod)

    def forward_dashboard_ports(self):
        """
        Forward the dashboard Pod's ports (8050 and 8888) to localhost.

        Port 8050 is the DBMSBenchmarker result dashboard; port 8888 is Jupyter.
        """
        print("forward_dashboard_ports")
        pod_dashboard = self.get_dashboard_pod_name(component='dashboard')
        if pod_dashboard:
            fullcommand = f'port-forward pod/{pod_dashboard} 8050:8050 8888:8888 --address 0.0.0.0'
            self.kubectl(fullcommand)

    def forward_sut_port(self, experiment='', configuration=''):
        """
        Forward the SUT master service port to localhost.

        :param experiment: Filter by experiment code (optional).
        :param configuration: Filter by DBMS configuration name (optional).
        """
        print("forward_sut_port")
        if experiment is None:
            experiment = ''
        if configuration is None:
            configuration = ''
        pods_master = self.get_services(
            component='sut', experiment=experiment, configuration=configuration
        )
        if pods_master:
            pod_master = pods_master[0]
            print(f"Connect to {pod_master}")
            fullcommand = f'port-forward svc/{pod_master} {self.port} --address 0.0.0.0'
            self.kubectl(fullcommand)

    def add_to_messagequeue(self, queue, data):
        """
        Push ``data`` onto the tail of a Redis list (message queue).

        :param queue: Redis key (queue name).
        :param data: Value to push onto the queue.
        """
        pods_messagequeue = self.get_pods(component='messagequeue')
        if pods_messagequeue:
            pod_messagequeue = pods_messagequeue[0]
        else:
            pod_messagequeue = 'bexhoma-messagequeue-5ff94984ff-mv9zn'
        self.logger.debug(f"I am using messagequeue {pod_messagequeue}")
        redis_command = f'redis-cli rpush {queue} {data} '
        self.execute_command_in_pod(command=redis_command, pod=pod_messagequeue)

    def set_pod_counter(self, queue, value=0):
        """
        Set a Redis key to an integer value (used as a pod-count synchronisation counter).

        :param queue: Redis key to set.
        :param value: Integer value to assign.  Defaults to ``0``.
        """
        pods_messagequeue = self.get_pods(component='messagequeue')
        if pods_messagequeue:
            pod_messagequeue = pods_messagequeue[0]
        else:
            pod_messagequeue = 'bexhoma-messagequeue-5ff94984ff-mv9zn'
        self.logger.debug(f"I am using messagequeue {pod_messagequeue}")
        redis_command = f'redis-cli set {queue} {value} '
        self.execute_command_in_pod(command=redis_command, pod=pod_messagequeue)

    def get_service_endpoints(self, service_name="bexhoma-service-monitoring-default"):
        """
        Return IP addresses of all endpoints for a named Service.

        Particularly useful for headless Services (e.g. to enumerate monitoring nodes).

        :param service_name: Name of the Service to query.
        :return: List of endpoint IP strings, or ``[]`` on error.
        """
        self.logger.debug(f"get_service_endpoints({service_name})")
        endpoints_raw = self.kubectl(
            "get endpoints -o jsonpath=\"{range .items[*]}{.metadata.name},"
            "{.subsets[*].addresses[*].ip}{'\\n'}{end}\""
        )
        try:
            for service_line in endpoints_raw.split("\n"):
                if service_line.startswith(service_name):
                    endpoints_string = service_line[service_line.find(",") + 1:]
                    endpoints_list = endpoints_string.split(" ")
                    self.logger.debug(f"endpoints: {endpoints_list}")
                    return endpoints_list
        except Exception as e:
            print(f"Exception when calling get_service_endpoints: {e}\n")
        return []


    def add_experiment(self, experiment):
        """
        Append an experiment object to this cluster's experiment list.

        :param experiment: Experiment object to add.
        """
        self.experiments.append(experiment)

    def store_pod_description(self, pod_name, container='', number=None):
        """
        Fetch and persist ``kubectl describe pod`` output to the result folder.

        The file is not overwritten if it already exists.  Up to 10 retries are
        attempted in case of transient kubectl failures.

        :param pod_name: Name of the Pod to describe.
        :param container: Accepted for API compatibility but ignored — ``kubectl describe``
            is not container-sensitive.
        :param number: Optional index suffix appended to the filename.
        """
        resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        if number is not None:
            filename_log = f"{resultfolder}/{self.code}/{pod_name}.{number}.describe"
        else:
            filename_log = f"{resultfolder}/{self.code}/{pod_name}.describe"
        if not os.path.isfile(filename_log):
            attempt = 1
            while attempt < 10:
                stdout = self.pod_description(pod_name, container)
                if stdout:
                    with open(filename_log, "w") as f:
                        f.write(stdout)
                    return
                else:
                    attempt += 1

    def pod_description_exists(self, pod_name, container=''):
        """
        Return whether a cached ``describe`` file exists in the result folder.

        :param pod_name: Name of the Pod.
        :param container: Accepted for API compatibility but ignored — ``kubectl describe``
            is not container-sensitive.
        :return: ``True`` if the ``.describe`` file exists on disk.
        """
        resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        filename_log = f"{resultfolder}/{self.code}/{pod_name}.describe"
        return os.path.isfile(filename_log)

    def store_pod_log(self, pod_name, container='', number=None):
        """
        Fetch and persist ``kubectl logs`` output to the result folder.

        The file is not overwritten if it already exists.  Up to 10 retries are
        attempted in case of transient kubectl failures.

        :param pod_name: Name of the Pod.
        :param container: Container name within the Pod (optional).
        :param number: Optional index suffix appended to the filename.
        """
        resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        if number is not None:
            if container:
                filename_log = f"{resultfolder}/{self.code}/{pod_name}.{container}.{number}.log"
            else:
                filename_log = f"{resultfolder}/{self.code}/{pod_name}.{number}.log"
        else:
            if container:
                filename_log = f"{resultfolder}/{self.code}/{pod_name}.{container}.log"
            else:
                filename_log = f"{resultfolder}/{self.code}/{pod_name}.log"
        if not os.path.isfile(filename_log):
            attempt = 1
            while attempt < 10:
                self.logger.debug(f"{'Bexhoma':30s}: (try #{attempt}) stores pod log into {filename_log}")
                stdout = self.pod_log(pod_name, container)
                if stdout is None:
                    print(f"{'Bexhoma':30s}: no data error for log {filename_log}")
                    attempt += 1
                elif stdout:
                    with open(filename_log, "w", encoding='utf-8') as f:
                        f.write(stdout)
                    return
                else:
                    attempt += 1

    def pod_log_exists(self, pod_name, container=''):
        """
        Return whether a cached log file exists in the result folder.

        :param pod_name: Name of the Pod.
        :param container: Container name within the Pod (optional).
        :return: ``True`` if the ``.log`` file exists on disk.
        """
        resultfolder = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")
        if container:
            filename_log = f"{resultfolder}/{self.code}/{pod_name}.{container}.log"
        else:
            filename_log = f"{resultfolder}/{self.code}/{pod_name}.log"
        return os.path.isfile(filename_log)


class AWS(Kubernetes):
    """
    AWS EKS extension of the Kubernetes cluster manager.

    Adds ``eksctl``-based nodegroup scaling and AWS-specific node label handling.
    """

    def __init__(
        self,
        clusterconfig='cluster.config',
        experiments_configfolder='experiments/',
        yamlfolder='k8s/',
        context=None,
        code=None,
        instance=None,
        volume=None,
        docker=None,
        script=None,
        queryfile=None,
    ):
        """
        Construct a new :class:`AWS` cluster manager.

        :param clusterconfig: Path to the cluster configuration file.
        :param experiments_configfolder: Folder containing experiment sub-folders.
        :param yamlfolder: Folder containing Kubernetes manifest templates.
        :param context: kubectl context name (also used as the EKS cluster name).
        :param code: Unique experiment identifier to resume.
        :param instance: Instance key (legacy IaaS).
        :param volume: Volume key in ``config['volumes']``.
        :param docker: Docker image key in ``config['dockers']``.
        :param script: Init-script key within the chosen volume.
        :param queryfile: Path to the DBMSBenchmarker query config file.
        """
        self.code = code
        super().__init__(
            clusterconfig=clusterconfig,
            experiments_configfolder=experiments_configfolder,
            context=context,
            yamlfolder=yamlfolder,
            code=self.code,
            instance=instance,
            volume=volume,
            docker=docker,
            script=script,
            queryfile=queryfile,
        )
        # context doubles as the EKS cluster name for eksctl commands
        self.cluster = self.context

    def eksctl(self, command):
        """
        Run an ``eksctl`` command and return its stdout.

        :param command: eksctl subcommand string (without the ``eksctl`` prefix).
        :return: stdout of the eksctl command.
        """
        fullcommand = f'eksctl {command}'
        self.logger.debug(f'AWS.eksctl({fullcommand})')
        return subprocess.run(fullcommand, shell=True, capture_output=True, text=True).stdout

    def get_nodes(self, app='', nodegroup_type='', nodegroup_name=''):
        """
        Return node objects matching the given selectors.

        Overrides :meth:`Kubernetes.get_nodes` to use the EKS-specific
        ``alpha.eksctl.io/nodegroup-name`` label instead of the generic ``name`` label.

        :param app: ``app`` label value.  Defaults to ``self.appname``.
        :param nodegroup_type: ``type`` label value.
        :param nodegroup_name: EKS nodegroup name (``alpha.eksctl.io/nodegroup-name``).
        :return: List of Kubernetes node objects.
        """
        self.logger.debug('AWS.get_nodes()')
        if not app:
            app = self.appname
        label = 'app=' + app
        if nodegroup_type:
            label += ',type=' + nodegroup_type
        if nodegroup_name:
            label += ',alpha.eksctl.io/nodegroup-name=' + nodegroup_name
        try:
            api_response = self.v1core.list_node(label_selector=label)
            if api_response.items:
                return api_response.items
            else:
                return []
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_node for get_nodes: {e}\n")
            print("Create new access token")
            self.cluster_access()
            self.wait(2)
            return self.get_nodes(
                app=app, nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name
            )

    def scale_nodegroups(self, nodegroup_names, size=None):
        """
        Scale multiple EKS nodegroups.

        :param nodegroup_names: Dict mapping nodegroup name to default target size.
        :param size: If given, overrides the default size for every nodegroup.
        """
        print(f"AWS.scale_nodegroups({nodegroup_names}, {size})")
        for nodegroup_name, size_default in nodegroup_names.items():
            if size is not None:
                size_default = size
            self.scale_nodegroup(nodegroup_name, size_default)

    def scale_nodegroup(self, nodegroup_name, size):
        """
        Scale a single EKS nodegroup to the requested number of nodes.

        No-ops if the nodegroup is already at the target size.

        :param nodegroup_name: EKS nodegroup name.
        :param size: Desired number of nodes.
        :return: eksctl output, or ``None`` if already at the target size.
        """
        print(f"AWS.scale_nodegroup({nodegroup_name}, {size})")
        if not self.check_nodegroup(nodegroup_name=nodegroup_name, num_nodes_aux_planned=size):
            command = f"scale nodegroup --cluster={self.cluster} --nodes={size} --name={nodegroup_name}"
            return self.eksctl(command)

    def get_nodegroup_size(self, nodegroup_type='', nodegroup_name=''):
        """
        Return the current number of ready nodes in an EKS nodegroup.

        :param nodegroup_type: ``type`` label value.
        :param nodegroup_name: EKS nodegroup name.
        :return: Number of nodes currently in the nodegroup.
        """
        nodes = self.get_nodes(nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name)
        num_nodes = len(nodes)
        self.logger.debug(f'AWS.get_nodegroup_size({nodegroup_type},{nodegroup_name}) = {num_nodes}')
        return num_nodes

    def check_nodegroup(self, nodegroup_type='', nodegroup_name='', num_nodes_aux_planned=0):
        """
        Return whether a nodegroup is at the expected size.

        :param nodegroup_type: ``type`` label value.
        :param nodegroup_name: EKS nodegroup name.
        :param num_nodes_aux_planned: Expected node count.
        :return: ``True`` if actual count equals ``num_nodes_aux_planned``.
        """
        num_nodes_actual = self.get_nodegroup_size(
            nodegroup_type=nodegroup_type, nodegroup_name=nodegroup_name
        )
        self.logger.debug(f'AWS.check_nodegroup({nodegroup_type}, {nodegroup_name}, {num_nodes_aux_planned}) = {num_nodes_actual}')
        return num_nodes_aux_planned == num_nodes_actual

    def wait_for_nodegroups(self, nodegroup_names, size=None):
        """
        Block until all listed EKS nodegroups reach their target sizes.

        :param nodegroup_names: Dict mapping nodegroup name to default target size.
        :param size: If given, overrides the default size for every nodegroup.
        """
        print(f"AWS.wait_for_nodegroups({nodegroup_names})")
        for nodegroup_name, size_default in nodegroup_names.items():
            if size is not None:
                size_default = size
            self.wait_for_nodegroup(nodegroup_name=nodegroup_name, num_nodes_aux_planned=size_default)

    def wait_for_nodegroup(self, nodegroup_type='', nodegroup_name='', num_nodes_aux_planned=0):
        """
        Block until a single EKS nodegroup reaches the target size, polling every 30 s.

        :param nodegroup_type: ``type`` label value.
        :param nodegroup_name: EKS nodegroup name.
        :param num_nodes_aux_planned: Desired node count.
        :return: ``True`` once the nodegroup is at the target size.
        """
        while not self.check_nodegroup(
            nodegroup_type=nodegroup_type,
            nodegroup_name=nodegroup_name,
            num_nodes_aux_planned=num_nodes_aux_planned,
        ):
            self.wait(30)
        print(f"Nodegroup {nodegroup_type},{nodegroup_name} ready")
        return True

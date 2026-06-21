"""Core DBMS configuration class for bexhoma experiments."""
from __future__ import annotations

import copy
import logging
import os
import re
import shutil
from typing import List, Optional, Tuple

from bexhoma import experiments

from .benchmarking import BenchmarkRunner
from .host import HostProbe
from .lifecycle import LifecycleManager
from .loading import LoadingCoordinator
from .manifest import ManifestBuilder
from .metrics import MetricsCollector
from .status import ComponentStatus

__all__ = ['SutConfiguration']


class SutConfiguration:
    """Manage a single DBMS configuration plugged into a bexhoma experiment.

    A configuration object is created for each DBMS variant under test and
    attached to a :class:`~bexhoma.experiments.base` experiment.  It holds
    all deployment parameters, tracks loading and benchmarking state, and
    provides access to six specialised helper objects:

    * :attr:`status` — :class:`~.status.ComponentStatus`
    * :attr:`host` — :class:`~.host.HostProbe`
    * :attr:`lifecycle` — :class:`~.lifecycle.LifecycleManager`
    * :attr:`loader` — :class:`~.loading.LoadingCoordinator`
    * :attr:`runner` — :class:`~.benchmarking.BenchmarkRunner`
    * :attr:`metrics` — :class:`~.metrics.MetricsCollector`
    * :attr:`manifest` — :class:`~.manifest.ManifestBuilder`
    """

    #: Class-level counter used to give each configuration a unique suffix.
    configurations: dict = {}

    def __init__(
        self,
        experiment,
        docker: Optional[str] = None,
        configuration: str = '',
        script: Optional[str] = None,
        alias: Optional[str] = None,
        num_experiment_to_apply: Optional[int] = None,
        clients: list = None,
        dialect: str = '',
        worker: int = 0,
        dockerimage: str = '',
    ) -> None:
        """Initialise a DBMS configuration that is plugged into an experiment.

        :param experiment: Parent experiment object this configuration belongs to.
        :param docker: Name of the Docker image (used as SUT template key).
        :param configuration: Human-readable configuration name; defaults to docker + counter suffix.
        :param script: Key of the init script to use for loading; defaults to experiment's script.
        :param alias: Optional display alias shown in result reports.
        :param num_experiment_to_apply: Number of benchmark runs to perform; defaults to
            experiment setting.
        :param clients: Unused legacy parameter.
        :param dialect: SQL dialect string forwarded to dbmsbenchmarker.
        :param worker: Number of worker pods to co-deploy alongside the SUT.
        :param dockerimage: Docker image name of the SUT.
        """
        if clients is None:
            clients = [1]
        self.logger = logging.getLogger('bexhoma')                              #: Logger for this configuration.
        self.experiment = experiment                                             #: Parent experiment object.
        self.docker = docker                                                     #: Name of the Docker image.
        if len(configuration) == 0:
            configuration = docker
            if configuration not in SutConfiguration.configurations:
                SutConfiguration.configurations[configuration] = 1
            else:
                SutConfiguration.configurations[configuration] += 1
            configuration = configuration + '-' + str(SutConfiguration.configurations[configuration])
        self.configuration = configuration                                       #: Name of the configuration; default: docker image name with counter suffix.
        self.volume = self.experiment.volume                                     #: Name of the persistent volume used by this configuration.
        if docker is not None:
            self.dockertemplate = copy.deepcopy(                                 #: Template of the Docker information taken from cluster.config.
                self.experiment.cluster.dockers[self.docker])
        if script is not None:
            self.script = script                                                 #: Key of the init script used for loading.
            self.initscript = self.experiment.cluster.volumes[
                self.experiment.volume]['initscripts'][self.script]              #: Init script definition dict.
        else:
            self.script = self.experiment.script                                 #: Key of the init script used for loading.
            self.initscript = self.experiment.cluster.volumes[
                self.experiment.volume]['initscripts'][self.script]              #: Init script definition dict.
        self.indexing = self.experiment.indexing                                 #: Key of the indexing script, or falsy if no separate indexing step.
        if self.indexing:
            self.indexscript = self.experiment.cluster.volumes[
                self.experiment.volume]['initscripts'][self.indexing]            #: Indexing script definition dict.
        else:
            self.indexscript = []                                                #: Empty when no separate indexing step is configured.
        self.alias = alias                                                       #: Human-readable alias for this configuration in result reports.
        if num_experiment_to_apply is not None:
            self.num_experiment_to_apply = num_experiment_to_apply              #: Number of benchmarking runs to perform.
        else:
            self.num_experiment_to_apply = self.experiment.num_experiment_to_apply  #: Number of benchmarking runs to perform.
        self.num_experiment_to_apply_done = 0                                   #: Number of benchmarking runs completed so far.
        self.appname = self.experiment.cluster.appname                          #: Kubernetes app label used to identify bexhoma resources.
        self.code = self.experiment.cluster.code                                 #: Unique experiment run code shared across all configurations in this run.
        self.path = self.experiment.path                                         #: Filesystem path to the experiment's working directory.
        self.resources = {}                                                      #: Dict of Kubernetes resource requests/limits for the SUT pod.
        self.ddl_parameters = {}                                                 #: DDL schema parameters for init scripts.
        self.eval_parameters = {}                                                #: Parameters forwarded to dbmsbenchmarker for evaluation.
        self.storage = {}                                                        #: Parameters for persistent storage.
        self.nodes = {}                                                          #: Dict of node infos to guide component placement.
        self.maintaining_parameters = {}                                         #: Parameters for the maintaining component.
        self.loading_parameters = {}                                             #: Parameters for the loading component.
        self.sut_parameters = {}                                                 #: Parameters for the SUT and worker components.
        self.pod_sut = ''                                                        #: Name of the SUT's master pod.
        self.set_resources(**self.experiment.resources)
        self.set_ddl_parameters(**self.experiment.ddl_parameters)
        self.set_eval_parameters(**self.experiment.eval_parameters)
        self.connection_management = {}                                          #: Dict of connection management parameters.
        self.set_connection_management(**self.experiment.connection_management)
        self.set_storage(**self.experiment.storage)
        self.set_nodes(**self.experiment.nodes)
        self.set_maintaining_parameters(**self.experiment.maintaining_parameters)
        self.experiment_dict: dict = {"loader": [], "benchmarker": []}          #: Central experiment dict describing all loader and benchmarker jobs.
        self.set_loading_parameters(**self.experiment.loading_parameters)
        self.set_sut_parameters(**self.experiment.sut_parameters)
        self.loading_patch = None                                                #: Patch dict applied to the loading job YAML manifest.
        self.patch_loading(self.experiment.loading_patch)
        self.benchmarking_patch = None                                           #: Patch dict applied to the benchmarking job YAML manifest.
        self.patch_benchmarking(self.experiment.benchmarking_patch)
        self.benchmarking_parameters = {}                                        #: Dict of parameters forwarded to the benchmarking tool.
        self.set_benchmarking_parameters(**self.experiment.benchmarking_parameters)
        self.benchmarking_parameters_list = []                                   #: List of per-run benchmarking parameter dicts.
        self.additional_labels = {}                                              #: Extra Kubernetes labels added to all managed pods.
        self.set_additional_labels(**self.experiment.additional_labels)
        self.experiment.add_configuration(self)
        self.experiment_name = self.code                                         #: Identifier of experiment; may be overwritten when stateful set PVCs forbid per-experiment names.
        self.dialect = dialect                                                   #: SQL dialect string forwarded to dbmsbenchmarker.
        self.use_distributed_datasource = False                                  #: True iff the SUT should mount 'benchmark-data-volume' as source of non-generated data.
        # scaling
        self.num_worker = worker                                                 #: Number of worker pods to deploy alongside the SUT.
        self.num_loading = 0                                                     #: Number of parallel loading threads.
        self.num_maintaining = 0                                                 #: Number of parallel maintaining threads.
        self.num_loading_pods = 0                                                #: Number of loading pods currently active.
        self.num_maintaining_pods = 0                                            #: Number of maintaining pods currently active.
        self.num_tenants = self.experiment.num_tenants                          #: Number of tenants for multi-tenant experiments.
        self.tenant_per = self.experiment.tenant_per                             #: Tenancy mode: '', 'schema', 'database', or 'container'.
        self.tenant_ready_to_load = False                                        #: True once this tenant's SUT is ready to accept loading.
        self.tenant_started_to_load = False                                      #: True once loading for this tenant has been initiated.
        self.tenant_ready_to_index = False                                       #: True once this tenant's SUT is ready to accept indexing.
        self.tenant_started_to_index = False                                     #: True once indexing for this tenant has been initiated.
        # monitoring flags
        self.monitor_app_active = experiment.monitor_app_active                  #: True iff application-level monitoring is active.
        self.monitoring_active = experiment.monitoring_active                    #: True iff Prometheus-based cluster monitoring is active.
        self.prometheus_interval = experiment.prometheus_interval                #: Prometheus scrape interval in seconds.
        self.prometheus_timeout = experiment.prometheus_timeout                  #: Prometheus scrape timeout in seconds.
        self.maintaining_active = experiment.maintaining_active                  #: True iff a maintaining component should be deployed after loading.
        self.loading_active = experiment.loading_active                          #: True iff a loading component should be deployed.
        self.loading_deactivated = experiment.loading_deactivated                #: Do not load at all and do not test for loading.
        self.monitor_loading = True                                              #: Fetch metrics for the loading phase when monitoring is active.
        self.monitoring_sut = True                                               #: Fetch SUT metrics when monitoring is active.
        self.jobtemplate_maintaining = ""                                        #: Name of YAML template file for the maintaining job.
        self._jobtemplate_loading = ""                                           #: Name of YAML template file for the loading job (backing field).
        self.storage_label = experiment.storage_label                            #: Kubernetes node label used to select the storage node for PVs.
        self.experiment_done = False                                             #: True once the SUT has performed the experiment completely.
        self.dockerimage = dockerimage                                            #: Docker image name of the SUT.
        self.sut_template = "deploymenttemplate-" + self.docker + ".yml"        #: Name of YAML manifest in k8s/ for SUT deployment.
        self.path_experiment_docker = self.docker                                #: Experiment subfolder matching the docker image name.
        self.connection_parameter = {}                                           #: Collects parameters that may be interesting for result evaluation.
        self.time_loading = 0                                                     #: Seconds taken for the initial data load.
        self.time_generating = 0                                                  #: Seconds taken for data generation.
        self.time_ingesting = 0                                                   #: Seconds taken for ingesting existing data.
        self.time_schema = 0                                                      #: Seconds taken for schema creation.
        self.time_index = 0                                                       #: Seconds taken for index creation.
        self.times_scripts = {}                                                  #: Per-script timing dict.
        self.loading_started = False                                             #: True once loading has been initiated.
        self.loading_after_time = None                                           #: Optional unix timestamp after which loading should start.
        self.loading_finished = False                                            #: True once loading has completed.
        self.client = 1                                                          #: Current position in the benchmarker sequence.
        self.time_loading_start = 0                                                #: Unix timestamp when loading started.
        self.time_loading_end = 0                                                  #: Unix timestamp when loading ended.
        self.loading_timespans = {}                                              #: Per-container (start, end) pairs for loading pods.
        self.benchmarking_timespans = {}                                         #: Per-container (start, end) pairs for benchmarking pods.
        self.sut_service_name = ""                                               #: Fixed service name for SUTs not controlled by bexhoma.
        self.sut_pod_name = ""                                                   #: Fixed pod name for SUTs not controlled by bexhoma.
        self.sut_container_name = "dbms"                                         #: Container name in the SUT pod used for monitoring and exec.
        self.sut_startup_args = []                                               #: Args set for the SUT container in YAML at startup.
        self.statefulset_name = ""                                               #: Name of the stateful set managing pods of a distributed DBMS.
        self.deployment_infos = {}                                               #: Info about deployed deployments, stateful sets, PVCs, pods, and containers.
        self.sut_has_pool = False                                                #: True iff there is a pool component (for monitoring).
        self.is_sut_ready = False                                                #: True once the SUT pod reports ready.
        self.are_worker_ready = False                                            #: True once all worker pods report ready.
        self.reset_sut()
        self.benchmark = None                                                    #: Optional dbmsbenchmarker instance.
        self.current_benchmark_connection = ""                                   #: Name of the connection currently being benchmarked.
        self.benchmark_list = []                                                 #: Ordered list of benchmarker-instance counts (consumed as a queue).
        self.benchmark_list_template = []                                        #: Original copy of benchmark_list kept as a template.
        self.benchmarking_parameters_list_template = []                         #: Original copy of benchmarking_parameters_list.
        self.volume_per_tenant = False                                           #: True iff each tenant gets its own persistent volume.
        self.service = ""                                                        #: Name of the Kubernetes Service currently exposing the SUT.
        self.worker_startup_args = []                                            #: Args set for the worker container in YAML at startup.
        self.connection = ""                                                     #: Name of the dbmsbenchmarker connection currently being executed.
        self.current_benchmark_start = 0                                         #: Unix timestamp when the current benchmark run started.
        self.volumeid = ""                                                       #: Identifier of the persistent volume claimed by this configuration.
        self.max_sut_dbms = None                                                 #: Max SUT pods of this DBMS type (config.docker) allowed in the cluster at once; None means no limit.
        # Worker naming overrides (replace monkey-patching in entry scripts)
        self.worker_name_app = ''                                                #: App label override for get_worker_name(); empty means use self.appname.
        self.worker_name_component = ''                                          #: Component label override for get_worker_name(); empty means use the method argument.
        self.worker_metric_strip_container = False                               #: When True, strip container filter from Prometheus metric queries (e.g. for YugabyteDB).
        # Specialised helper objects — created last so they can reference self safely.
        self.status = ComponentStatus(self)
        self.host = HostProbe(self)
        self.lifecycle = LifecycleManager(self)
        self.loader = LoadingCoordinator(self)
        self.runner = BenchmarkRunner(self)
        self.metrics = MetricsCollector(self)
        self.manifest = ManifestBuilder(self)

    # ------------------------------------------------------------------
    # jobtemplate_loading property
    # ------------------------------------------------------------------

    @property
    def jobtemplate_loading(self) -> str:
        """Name of the YAML template file used for the loading job.

        :return: Template file name.
        :rtype: str
        """
        return self._jobtemplate_loading

    @jobtemplate_loading.setter
    def jobtemplate_loading(self, template: str) -> None:
        """Set the loading job template and keep the experiment dict in sync.

        When a non-empty template is assigned, the ``template`` field of the
        first loader entry in ``experiment_dict`` is updated.

        :param template: YAML template file name.
        :type template: str
        """
        self._jobtemplate_loading = template
        if template and self.experiment_dict.get('loader'):
            self.experiment_dict['loader'][0]['template'] = template

    # ------------------------------------------------------------------
    # State reset
    # ------------------------------------------------------------------

    def reset_sut(self) -> None:
        """Forget that the SUT has been loaded and benchmarked."""
        self.time_loading = 0
        self.time_generating = 0
        self.time_ingesting = 0
        self.time_schema = 0
        self.time_index = 0
        self.loading_started = False
        self.loading_after_time = None
        self.loading_finished = False
        self.client = 1
        self.is_sut_ready = False
        self.are_worker_ready = False
        self.tenant_ready_to_load = False
        self.tenant_started_to_load = False

    # ------------------------------------------------------------------
    # Benchmark sequence
    # ------------------------------------------------------------------

    def add_benchmark_list(self, list_clients: list) -> None:
        """Add a list of benchmarker-instance counts for the current SUT.

        Example: ``[1, 2, 1]`` schedules three sequential rounds with 1, 2, and 1
        benchmarker instances.  Also reconstructs ``experiment_dict["benchmarker"]``
        so that each client round carries the correct parallelism and the per-round
        parameters accumulated in ``benchmarking_parameters_list``.

        :param list_clients: List of benchmarker-instance counts.
        :type list_clients: list
        """
        self.benchmark_list = copy.deepcopy(list_clients)
        self.benchmark_list_template = copy.deepcopy(list_clients)
        self.benchmarking_parameters_list_template = copy.deepcopy(self.benchmarking_parameters_list)
        if not list_clients:
            self.experiment_dict['benchmarker'] = []
            return
        if self.experiment_dict['benchmarker']:
            template_entries = self.experiment_dict['benchmarker'][0]
            new_benchmarker = []
            for i, parallelism in enumerate(list_clients):
                per_round_params = (
                    self.benchmarking_parameters_list[i]
                    if i < len(self.benchmarking_parameters_list)
                    else {}
                )
                round_entries = [
                    {
                        'name':             tmpl['name'],
                        'benchmarker':      tmpl['benchmarker'],
                        'template':         tmpl['template'],
                        'parallelism':      tmpl['parallelism'] if tmpl.get('fixed_parallelism') else int(parallelism),
                        'num_pods':         tmpl['num_pods']    if tmpl.get('fixed_parallelism') else int(parallelism),
                        'target':           tmpl.get('target', 'sut'),
                        'parameters':       {**tmpl['parameters'], **per_round_params},
                        'fixed_parallelism': tmpl.get('fixed_parallelism', False),
                    }
                    for tmpl in template_entries
                ]
                new_benchmarker.append(round_entries)
            self.experiment_dict['benchmarker'] = new_benchmarker

    def add_benchmarking_parameters(self, parallelism: int = None, **env_vars) -> None:
        """Add a new sequential client round to the experiment dict.

        Clones the first benchmarker entry's header keys and merges ``env_vars``
        on top of that entry's parameters.  When ``parallelism`` is ``None``,
        inherits the template entry's parallelism.

        Also appends ``env_vars`` to ``benchmarking_parameters_list`` for backward
        compatibility.

        :param parallelism: Pod count for this client round; inherits template if ``None``.
        :type parallelism: int
        :param env_vars: ENV vars injected into the job container for this round.
        """
        merged_env_vars = {**self.experiment.default_benchmarking_parameters, **env_vars}
        self.benchmarking_parameters_list.append(merged_env_vars)
        if not self.experiment_dict['benchmarker'] or not self.experiment_dict['benchmarker'][0]:
            return
        template_entries = self.experiment_dict['benchmarker'][0]
        pod_count = parallelism if parallelism is not None else template_entries[0]['parallelism']
        round_entries = [
            {
                'name':        tmpl['name'],
                'benchmarker': tmpl['benchmarker'],
                'template':    tmpl['template'],
                'parallelism': pod_count,
                'num_pods':    pod_count,
                'target':      tmpl.get('target', 'sut'),
                'parameters':  {**tmpl['parameters'], **merged_env_vars},
            }
            for tmpl in template_entries
        ]
        self.experiment_dict['benchmarker'].append(round_entries)

    def add_parallel_benchmark(
        self,
        name: str,
        template: str,
        benchmarker: str,
        parallelism: int = 1,
        target: str = 'sut',
        **env_vars,
    ) -> None:
        """Add a parallel benchmark to the last client round.

        Creates a new entry inside the last inner list of
        ``experiment_dict["benchmarker"]``, enabling multiple benchmarks to run
        simultaneously within one client round.

        :param name: Short identifier for this benchmark entry.
        :param template: K8s job template filename.
        :param benchmarker: Tool name (``'ycsb'``, ``'hammerdb'``, ``'benchbase'``,
            ``'dbmsbenchmarker'``).
        :param parallelism: Number of pods.
        :param target: Component the job runs against (default ``'sut'``).
        :param env_vars: ENV vars injected into the container.
        """
        if not self.experiment_dict['benchmarker']:
            self.experiment_dict['benchmarker'].append([])
        entry = {
            'name':        name,
            'benchmarker': benchmarker,
            'template':    template,
            'parallelism': parallelism,
            'num_pods':    parallelism,
            'target':      target,
            'parameters':  env_vars,
        }
        self.experiment_dict['benchmarker'][-1].append(entry)

    def add_loading_parameters(
        self,
        name: str,
        template: str,
        benchmarker: str,
        parallelism: int = 1,
        num_pods: int = None,
        target: str = 'sut',
        **env_vars,
    ) -> None:
        """Add a parallel loader entry to the experiment dict.

        All loader entries run simultaneously during the loading phase.

        :param name: Short identifier for this loader entry.
        :param template: K8s job template filename.
        :param benchmarker: Tool name — identifies the evaluator's ``log_to_df_loading()``.
        :param parallelism: Max concurrent pods (K8s ``spec.parallelism``).
        :param num_pods: Total pods that must complete (K8s ``spec.completions``).
            Defaults to ``parallelism``.
        :param target: Component the job runs against (default ``'sut'``).
        :param env_vars: ENV vars injected into the container.
        """
        entry = {
            'name':        name,
            'benchmarker': benchmarker,
            'template':    template,
            'parallelism': parallelism,
            'num_pods':    num_pods if num_pods is not None else parallelism,
            'target':      target,
            'parameters':  env_vars,
        }
        self.experiment_dict['loader'].append(entry)

    def set_experiment_dict(self, d: dict) -> None:
        """Replace the entire experiment dict.

        :param d: New experiment dict with ``"loader"`` and ``"benchmarker"`` keys.
        :type d: dict
        """
        self.experiment_dict = d

    # ------------------------------------------------------------------
    # Timing helpers
    # ------------------------------------------------------------------

    def wait(self, sec: int, silent: bool = False) -> None:
        """Wait for a number of seconds, optionally printing a message.

        :param sec: Number of seconds to wait.
        :param silent: When True, suppress output.
        """
        return self.experiment.cluster.wait(sec, silent)

    # ------------------------------------------------------------------
    # Parameter setters
    # ------------------------------------------------------------------

    def set_connection_management(self, **kwargs) -> None:
        """Set connection management data for the benchmarker component.

        :param kwargs: Dict of connection management parameters, e.g. ``timeout=60``.
        """
        self.connection_management = kwargs

    def set_resources(self, **kwargs) -> None:
        """Set Kubernetes resource requests/limits for the SUT.

        :param kwargs: Resource dict, e.g. ``requests={'cpu': 4}``.
        """
        self.resources = {**self.resources, **kwargs}

    def set_storage(self, **kwargs) -> None:
        """Set storage parameters for the SUT's persistent volume.

        :param kwargs: Storage dict, e.g. ``storageSize='100Gi'``.
        """
        self.storage = {**self.storage, **kwargs}

    def set_additional_labels(self, **kwargs) -> None:
        """Set extra Kubernetes labels added to all managed pods.

        :param kwargs: Label dict, e.g. ``SF=100``.
        """
        self.additional_labels = {**self.additional_labels, **kwargs}

    def set_ddl_parameters(self, **kwargs) -> None:
        """Set DDL parameters that are substituted in init scripts.

        :param kwargs: Parameter dict, e.g. ``index='btree'``.
        """
        self.ddl_parameters = kwargs

    def set_eval_parameters(self, **kwargs) -> None:
        """Set evaluation parameters forwarded to the benchmarker component.

        :param kwargs: Parameter dict, e.g. ``type='noindex'``.
        """
        self.eval_parameters = {**self.eval_parameters, **kwargs}

    def set_maintaining_parameters(self, **kwargs) -> None:
        """Set ENV vars for the maintaining component.

        :param kwargs: Parameter dict, e.g. ``PARALLEL='64'``.
        """
        self.maintaining_parameters = kwargs

    def set_maintaining(self, parallel: int, num_pods: int = None) -> None:
        """Set job parameters for the maintaining component.

        :param parallel: Number of parallel pods.
        :param num_pods: Total number of pods; defaults to ``parallel``.
        """
        self.num_maintaining = int(parallel)
        self.num_maintaining_pods = int(num_pods) if num_pods is not None else int(parallel)
        if self.num_maintaining_pods < self.num_maintaining:
            self.num_maintaining_pods = self.num_maintaining

    def set_sut_parameters(self, **kwargs) -> None:
        """Set ENV vars for the SUT and worker components.

        :param kwargs: Parameter dict, e.g. ``PARALLEL='64'``.
        """
        self.sut_parameters = kwargs

    def set_loading_parameters(self, **kwargs) -> None:
        """Set ENV vars for the loading component.

        Merges experiment-wide defaults first; per-configuration ``kwargs`` win on conflict.
        Also updates the first loader entry in ``experiment_dict`` when present.

        :param kwargs: Parameter dict, e.g. ``PARALLEL='64'``.
        """
        self.loading_parameters = {**self.experiment.default_loading_parameters, **kwargs}
        if self.experiment_dict['loader']:
            self.experiment_dict['loader'][0]['parameters'].update(self.loading_parameters)

    def set_loading(self, parallel: int, num_pods: int = None) -> None:
        """Set job parameters for loading: parallel pods and total pod count.

        :param parallel: Number of parallel pods.
        :param num_pods: Total number of pods; defaults to ``parallel``.
        """
        self.num_loading = int(parallel)
        self.num_loading_pods = int(num_pods) if num_pods is not None else int(parallel)
        if self.num_loading_pods < self.num_loading:
            self.num_loading_pods = self.num_loading
        if self.experiment_dict['loader']:
            self.experiment_dict['loader'][0]['parallelism'] = self.num_loading
            self.experiment_dict['loader'][0]['num_pods'] = self.num_loading_pods

    def patch_loading(self, patch) -> None:
        """Apply a YAML patch string to the loading job manifest.

        :param patch: YAML-formatted patch string.
        """
        self.loading_patch = patch

    def patch_benchmarking(self, patch) -> None:
        """Apply a YAML patch string to the benchmarking job manifest.

        :param patch: YAML-formatted patch string.
        """
        self.benchmarking_patch = patch

    def set_benchmarking_parameters(self, **kwargs) -> None:
        """Set ENV vars for the benchmarking component.

        Merges experiment-wide defaults first; per-configuration ``kwargs`` win on conflict.
        Also updates all entries in the first benchmarker round in ``experiment_dict``.

        :param kwargs: Parameter dict.
        """
        self.benchmarking_parameters = {**self.experiment.default_benchmarking_parameters, **kwargs}
        if self.experiment_dict['benchmarker'] and self.experiment_dict['benchmarker'][0]:
            for entry in self.experiment_dict['benchmarker'][0]:
                entry['parameters'].update(self.benchmarking_parameters)

    def set_nodes(self, **kwargs) -> None:
        """Set node selector parameters for experiment components.

        :param kwargs: Node info dict, e.g. ``sut='sut', loading='auxiliary'``.
        """
        self.nodes = kwargs

    def set_experiment(
        self,
        instance=None,
        volume=None,
        docker=None,
        script=None,
        indexing=None,
    ) -> None:
        """Read experiment details from the cluster config.

        :param instance: Unused.
        :param volume: Override the persistent volume.
        :param docker: Unused.
        :param script: Override the init script key.
        :param indexing: Override the indexing script key.
        """
        if volume is not None:
            self.volume = volume
            self.volumeid = self.experiment.cluster.volumes[self.experiment.volume]['id']
        if script is not None:
            self.script = script
            self.initscript = self.experiment.cluster.volumes[
                self.experiment.volume]['initscripts'][self.script]
        if indexing is not None:
            self.indexing = indexing
            self.indexscript = self.experiment.cluster.volumes[
                self.experiment.volume]['initscripts'][self.indexing]

    # ------------------------------------------------------------------
    # Pod config distribution
    # ------------------------------------------------------------------

    def _push_pod_configs(
        self,
        queue_key: str,
        num_pods: int,
        parameters: dict,
        pod_parameters: list,
    ) -> None:
        """Push per-pod merged configurations to Redis.

        For each pod index 1..num_pods, merges ``parameters`` with the
        corresponding entry from ``pod_parameters`` (if present) and stores
        the result as a JSON string at ``{queue_key}-config-{i}``.

        :param queue_key: Base Redis queue key.
        :param num_pods: Number of pods in this job.
        :param parameters: Default parameter dict shared by all pods.
        :param pod_parameters: Per-pod override dicts.
        """
        for i in range(1, num_pods + 1):
            merged = dict(parameters)
            if pod_parameters and i - 1 < len(pod_parameters):
                merged.update(pod_parameters[i - 1])
            config_key = f"{queue_key}-config-{i}"
            self.experiment.cluster.set_pod_config(key=config_key, config=merged)

    # ------------------------------------------------------------------
    # Component naming
    # ------------------------------------------------------------------

    def generate_component_name(
        self,
        app: str = '',
        component: str = '',
        experiment: str = '',
        configuration: str = '',
        experiment_run: str = '',
        client: str = '',
        benchmark_run: str = '',
    ) -> str:
        """Generate a Kubernetes-compatible name for a component.

        Format: ``{app}-{component}-{configuration}-{experiment}[-{experiment_run}][-{client}[-{benchmark_run}]]``

        :param app: App the component belongs to.
        :param component: Component type, e.g. ``'sut'`` or ``'benchmarker'``.
        :param experiment: Unique experiment identifier.
        :param configuration: DBMS configuration name.
        :param experiment_run: Repetition index (omitted when empty).
        :param client: Sequential client-round index (omitted when empty).
        :param benchmark_run: Parallel benchmark index within a client round (omitted when empty).
        :return: Lower-case component name string.
        :rtype: str
        """
        if len(app) == 0:
            app = self.appname
        if len(configuration) == 0:
            configuration = self.configuration
        if len(experiment) == 0:
            experiment = self.code
        if len(experiment_run) != 0:
            experiment_run = '-' + experiment_run
        if len(client) > 0:
            if len(benchmark_run) > 0:
                name = (
                    f"{app}-{component}-{configuration}-{experiment}"
                    f"{experiment_run}-{client}-{benchmark_run}"
                ).lower()
            else:
                name = (
                    f"{app}-{component}-{configuration}-{experiment}"
                    f"{experiment_run}-{client}"
                ).lower()
        else:
            name = f"{app}-{component}-{configuration}-{experiment}{experiment_run}".lower()
        return name

    def get_experiment_name(self) -> str:
        """Return the experiment run code identifying this experiment across all configurations.

        :return: Experiment code string.
        :rtype: str
        """
        return self.code

    def get_service_sut(self, configuration: str) -> str:
        """Return the name of the Kubernetes service for the SUT.

        :param configuration: Name of the DBMS configuration.
        :return: Service name.
        :rtype: str
        """
        if len(self.sut_service_name) > 0:
            return self.sut_service_name
        return self.generate_component_name(
            app=self.appname,
            component='sut',
            experiment=self.get_experiment_name(),
            configuration=configuration,
        )

    # ------------------------------------------------------------------
    # Worker naming and pod discovery
    # ------------------------------------------------------------------

    def get_worker_name(self, component: str = 'worker') -> str:
        """Return a name template for worker pods.

        When :attr:`worker_name_app` or :attr:`worker_name_component` are set,
        the override values are used together with :attr:`experiment_name` (the
        experiment code) instead of :attr:`storage_label`.  This covers
        distributed DBMS workers (e.g. Dragonfly, Redis) that use shorter pod
        names tied to the experiment code rather than the storage label.

        :param component: Component type to use when not overridden.
        :return: Worker name template string.
        :rtype: str
        """
        if self.storage['storageConfiguration']:
            storageConfiguration = self.storage['storageConfiguration']
        else:
            storageConfiguration = self.configuration
        if self.worker_name_app or self.worker_name_component:
            effective_app = self.worker_name_app or self.appname
            effective_component = self.worker_name_component or component
            return self.generate_component_name(
                app=effective_app,
                component=effective_component,
                experiment=self.experiment_name,
                configuration=storageConfiguration,
            )
        return self.generate_component_name(
            app=self.appname,
            component=component,
            experiment=self.storage_label,
            configuration=storageConfiguration,
        )

    def get_worker_pods(self, component: str = 'worker', only_stateful: bool = False) -> list:
        """Return a list of all worker pod names for the current SUT.

        When :attr:`statefulset_name` is set, delegates to the cluster's
        stateful set pod discovery (e.g. for YugabyteDB tservers).
        Otherwise finds pods via the standard bexhoma label selector.

        :param component: Component label used in the label selector.
        :param only_stateful: When True, return only stateful set pods (pods
            whose names end with a numeric index).
        :return: List of pod name strings.
        :rtype: list[str]
        """
        if self.statefulset_name:
            return self.experiment.cluster.get_stateful_set_pods(self.statefulset_name)
        pods_worker = self.experiment.cluster.get_pods(
            app=self.appname,
            component=component,
            experiment=self.code,
            configuration=self.configuration,
        )
        if self.num_worker > 0:
            print("{:30s}: worker pods found: {}".format(self.configuration, pods_worker))
            pods_worker_stateful = [pod for pod in pods_worker if re.search(r"-\d+$", pod)]
            print("{:30s}: worker pods found (only stateful set pods): {}".format(
                self.configuration, pods_worker_stateful))
        if only_stateful:
            return pods_worker_stateful
        return pods_worker

    def get_worker_endpoints(self) -> list:
        """Return endpoints of the headless service monitoring distributed DBMS workers.

        When :attr:`statefulset_name` is set (external stateful set, e.g. YugabyteDB),
        returns bare pod names.  Otherwise returns ``{pod}.{service}`` entries.

        :return: List of endpoint strings.
        :rtype: list[str]
        """
        endpoints = []
        pods_worker = self.get_worker_pods()
        if self.statefulset_name:
            for pod in pods_worker:
                endpoints.append(pod)
                print("{:30s}: worker endpoint: {}".format(self.configuration, pod))
        else:
            name_worker = self.get_worker_name()
            for pod in pods_worker:
                endpoint = f'{pod}.{name_worker}'
                endpoints.append(endpoint)
                print("{:30s}: worker endpoint: {}".format(self.configuration, endpoint))
        self.logger.debug(f"get_worker_endpoints({endpoints})")
        return endpoints

    # ------------------------------------------------------------------
    # Metric query substitution
    # ------------------------------------------------------------------

    def set_metric_of_config_default(
        self,
        metric: str,
        host: str,
        gpuid: str,
        schema: str,
        database: str,
        experiment: str = None,
    ) -> str:
        """Substitute placeholders in a PromQL query for bexhoma-managed components.

        :param metric: Parametrised PromQL query string.
        :param host: Hostname of the node to monitor.
        :param gpuid: GPU identifier (or empty string).
        :param schema: Database schema name.
        :param database: Database name.
        :param experiment: Experiment code; defaults to :attr:`code`.
        :return: Filled PromQL query string.
        :rtype: str
        """
        if experiment is None:
            experiment = self.code
        return metric.format(
            host=host,
            gpuid=gpuid,
            configuration=self.configuration.lower(),
            experiment=self.get_experiment_name(),
            schema=schema,
            database=database,
        )

    def set_metric_of_config(
        self,
        metric: str,
        host: str,
        gpuid: str,
        schema: str,
        database: str,
        component: str = '',
    ) -> str:
        """Substitute placeholders in a PromQL query, routing by deployment type.

        When :attr:`worker_metric_strip_container` is True (e.g. YugabyteDB),
        strips the ``container="dbms"`` filter from the query and uses the
        component name directly as the configuration label — matching the
        external stateful set naming convention.

        :param metric: Parametrised PromQL query string.
        :param host: Hostname of the node to monitor.
        :param gpuid: GPU identifier (or empty string).
        :param schema: Database schema name.
        :param database: Database name.
        :param component: Stateful set component name; optional.
        :return: Filled PromQL query string.
        :rtype: str
        """
        if self.worker_metric_strip_container:
            metric = metric.replace(', container="dbms"', '')
            metric = metric.replace(', container_label_io_kubernetes_container_name="dbms"', '')
            return metric.format(
                host=host, gpuid=gpuid, configuration=component, experiment='')
        if self.num_worker > 0:
            if len(component) == 0:
                components = list(self.deployment_infos['statefulset'].keys())
                names_of_workers = [
                    self.get_worker_name(component=c).lower() for c in components
                ]
                configuration = '(' + '|'.join(names_of_workers) + ')'
                return metric.format(
                    host=host, gpuid=gpuid, configuration=configuration,
                    experiment="", schema=schema, database=database)
            name_worker = self.get_worker_name(component=component)
            return metric.format(
                host=host, gpuid=gpuid, configuration=name_worker,
                experiment="", schema=schema, database=database)
        experiment_name = self.get_experiment_name()
        self.logger.debug(
            f"set_metric_of_config_default({metric}, {host}, {gpuid}, "
            f"experiment={experiment_name}, schema={schema}, database={database})")
        return self.set_metric_of_config_default(
            metric, host, gpuid, experiment=experiment_name,
            schema=schema, database=database)

    # ------------------------------------------------------------------
    # Pod execution and file transfer
    # ------------------------------------------------------------------

    def execute_command_in_pod_sut(
        self,
        command: str,
        pod: str = '',
        container: str = '',
        params: str = '',
    ):
        """Run a shell command inside the SUT container.

        Defaults to the current SUT pod and the container named ``"dbms"``.

        :param command: Shell command to run.
        :param pod: Pod name; defaults to :attr:`pod_sut`.
        :param container: Container name; defaults to :attr:`sut_container_name`.
        :param params: Optional additional parameters (currently unused).
        :return: stdout of the shell command.
        """
        if len(pod) == 0:
            pod = self.pod_sut
        if len(container) == 0:
            container = self.sut_container_name
        if self.pod_sut == '':
            self.check_sut()
        return self.experiment.cluster.execute_command_in_pod(
            command=command, pod=pod, container=container, params=params)

    def upload_experiment_file(self, filename: str):
        """Upload a file to the experiment's result storage.

        :param filename: Path of the file to upload.
        :return: Result of the upload operation.
        """
        return self.experiment.upload_experiment_file(filename)

    def download_experiment_file(self, filename: str):
        """Download a file from the experiment's result storage.

        :param filename: Path of the file to download.
        :return: Result of the download operation.
        """
        return self.experiment.download_experiment_file(filename)

    # ------------------------------------------------------------------
    # SUT lifecycle helpers
    # ------------------------------------------------------------------

    def attach_worker(self) -> None:
        """Attach worker nodes to the SUT master via the ``attachWorker`` command."""
        self.logger.debug('Try to attach worker to master')
        if (self.num_worker > 0
                and 'attachWorker' in self.dockertemplate
                and len(self.dockertemplate['attachWorker']) > 0):
            print("{:30s}: try to attach workers to master".format(self.configuration))
            pods = self.experiment.cluster.get_pods(
                component='sut', configuration=self.configuration, experiment=self.code)
            name_worker = self.get_worker_name()
            if len(pods) > 0:
                print("{:30s}: master found".format(self.configuration))
                pod_sut = pods[0]
                num_worker = 0
                print("{:30s}: looking for worker pods".format(self.configuration))
                while num_worker < self.num_worker:
                    self.wait(5)
                    num_worker = 0
                    pods_worker = self.get_worker_pods()
                    for pod in pods_worker:
                        status = self.experiment.cluster.get_pod_status(pod)
                        if status == "Running":
                            num_worker += 1
                            print("{:30s}: found running worker {}".format(
                                self.configuration, num_worker))
                    print("{:30s}: found {} running workers of {}".format(
                        self.configuration, num_worker, self.num_worker))
                print("{:30s}: list of workers".format(self.configuration))
                pods_worker = self.get_worker_pods()
                resultfolder = (
                    self.experiment.cluster.config['benchmarker']['resultfolder']
                    .replace("\\", "/")
                    .replace("C:", "")
                )
                for pod in pods_worker:
                    print("{:30s}: worker {}.{} attached".format(
                        self.configuration, pod, name_worker))
                    self.logger.debug(
                        'Worker attached: {worker}.{service_sut}'.format(
                            worker=pod, service_sut=name_worker))
                    _, stdout, _ = self.execute_command_in_pod_sut(
                        self.dockertemplate['attachWorker'].format(
                            worker=pod, service_sut=name_worker),
                        pod_sut)
                    filename_log = (
                        f"{resultfolder}/{self.code}/{pod}.attach."
                        f"{self.num_experiment_to_apply_done + 1}.log"
                    )
                    with open(filename_log, "w") as logfile:
                        logfile.write(stdout)

    def check_sut(self) -> bool:
        """Check if the SUT pod is running and store its name in :attr:`pod_sut`.

        :return: True if at least one SUT pod was found.
        :rtype: bool
        """
        pods = self.experiment.cluster.get_pods(
            app=self.appname,
            component='sut',
            configuration=self.configuration,
            experiment=self.code,
        )
        if len(pods) > 0:
            self.pod_sut = pods[0]
            return True
        return False

    # ------------------------------------------------------------------
    # Storage helpers
    # ------------------------------------------------------------------

    def get_list_of_pvc(self) -> list:
        """Return a flat list of all PVC names currently claimed by this configuration.

        :return: List of PVC name strings.
        :rtype: list[str]
        """
        list_of_pvc = []
        if 'deployment' in self.deployment_infos:
            for _, deployment in self.deployment_infos['deployment'].items():
                if 'pvc' in deployment:
                    list_of_pvc.extend(deployment['pvc'])
        if 'statefulset' in self.deployment_infos:
            for _, statefulset in self.deployment_infos['statefulset'].items():
                if 'pvc' in statefulset:
                    list_of_pvc.extend(statefulset['pvc'])
        return list_of_pvc

    def use_ramdisk(self) -> bool:
        """Return True iff the storage class is ``'ramdisk'``.

        :rtype: bool
        """
        return (
            self.storage.get('storageClassName') is not None
            and self.storage['storageClassName'] == 'ramdisk'
        )

    def use_storage(self) -> bool:
        """Return True iff persistent storage is configured for the SUT.

        :rtype: bool
        """
        if not self.storage:
            return False
        storageClassName = self.storage.get('storageClassName', '')
        if storageClassName is None:
            return False
        if 'storageConfiguration' not in self.storage:
            self.storage['storageConfiguration'] = ''
        return True

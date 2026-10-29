"""Core DBMS configuration class for bexhoma experiments."""
from __future__ import annotations

import copy
from datetime import datetime
import logging
import os
import re
import shutil
from typing import List, Optional, Tuple

from bexhoma import ceph_storage, experiments
from bexhoma.cli_args import storage_suffix
from bexhoma.load_durability import DEFAULT_LEVEL, expand_durability_placeholders

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
        self.resetscript = []                                                    #: Scripts exec'd synchronously before each round on the legacy (non experiment_dict) benchmark_list path.
        self.load_durability = getattr(experiment, 'load_durability', DEFAULT_LEVEL)  #: Requested import durability (-xld): durable, relaxed or unsafe.
        self.load_durability_scripts = None                                      #: Durability scripts included in the loading phase; None until loading starts.
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
        self.ddl_storage_suffix = ''                                             #: Volume name part for non-default DDL parameters (see bexhoma.ddl_parameters.storage_suffix).
        self.eval_parameters = {}                                                #: Parameters forwarded to dbmsbenchmarker for evaluation.
        self.storage = {}                                                        #: Parameters for persistent storage.
        self.nodes = {}                                                          #: Dict of node infos to guide component placement.
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
        self.num_loading_pods = 0                                                #: Number of loading pods currently active.
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
        self.loading_active = experiment.loading_active                          #: True iff a loading component should be deployed.
        self.loading_deactivated = experiment.loading_deactivated                #: Do not load at all and do not test for loading.
        self.monitor_loading = True                                              #: Fetch metrics for the loading phase when monitoring is active.
        self.loading_metrics_fetched: dict = {}                                  #: experiment_run -> (connection, component types) whose loading metrics later connections of that run copy.
        self.monitoring_sut = True                                               #: Fetch SUT metrics when monitoring is active.
        self._jobtemplate_loading = ""                                           #: Name of YAML template file for the loading job (backing field).
        self.storage_label = experiment.storage_label                            #: Kubernetes node label used to select the storage node for PVs.
        self.experiment_done = False                                             #: True once the SUT has performed the experiment completely.
        self.dockerimage = dockerimage                                            #: Docker image name of the SUT.
        self.sut_template = "deploymenttemplate-" + self.docker + ".yml"        #: Name of YAML manifest in k8s/ for SUT deployment.
        self.path_experiment_docker = self.docker                                #: Experiment subfolder matching the docker image name.
        self.connection_parameter = {}                                           #: Collects parameters that may be interesting for result evaluation.
        self.time_loading = 0                                                     #: Seconds taken for the initial data load.
        self.storage_reused = False                                              #: True iff the SUT found a loaded volume from an earlier experiment, so loading was skipped and its times inherited.
        self.loading_inherited = False                                           #: True iff this repetition found a loaded volume (of this or an earlier experiment), so it did not load and its loading times are copied.
        self.storage_monitoring = None                                           #: Storage placeholders for Ceph monitoring (see resolve_storage_monitoring()), resolved once after deployment.
        self.time_generating = 0                                                  #: Seconds taken for data generation.
        self.time_ingesting = 0                                                   #: Seconds taken for ingesting existing data.
        self.time_schema = 0                                                      #: Seconds taken for schema creation.
        self.time_index = 0                                                       #: Seconds taken for index creation.
        self.times_scripts = {}                                                  #: Per-script timing dict.
        self.loading_started = False                                             #: True once loading has been initiated.
        self.loading_started_at: Optional[datetime] = None                       #: Local wall-clock start used for the load-only timeout.
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
        self.are_pool_ready = False                                              #: True once all pool (e.g. PGBouncer) pods report ready.
        self.reset_sut()
        self.benchmark = None                                                    #: Optional dbmsbenchmarker instance.
        self.current_benchmark_connection = ""                                   #: Name of the connection currently being benchmarked.
        self.benchmark_list = []                                                 #: Ordered list of benchmarker-instance counts (consumed as a queue).
        self.benchmark_list_template = []                                        #: Original copy of benchmark_list kept as a template.
        self.benchmarking_parameters_list_template = []                         #: Original copy of benchmarking_parameters_list.
        self.volume_per_tenant = False                                           #: True iff each tenant gets its own persistent volume.
        self.service = ""                                                        #: Name of the Kubernetes Service currently exposing the SUT.
        self.worker_startup_args = []                                            #: Args set for the worker container in YAML at startup.
        self.tls_secret = ''                                                     #: Name of the SUT's TLS Secret (see bexhoma.tls); empty when the DBMS uses none.
        self.script_target = 'sut'                                               #: Where shell init/reset scripts run: 'sut' (first SUT pod) or 'workers' (every worker pod).
        self.data_components = None                                              #: StatefulSet components that get the experiment's resources and volume size; None = all.
        self.sut_role = 'data'                                                   #: 'data' (SUT pod holds data) or 'placeholder' (entry point/client/helper; keeps template resources).
        self.pvc_selector = ''                                                   #: Label selector of extra PVCs for storage monitoring (volumes bexhoma did not create, e.g. 'app=yb-tserver').
        self.connection = ""                                                     #: Name of the dbmsbenchmarker connection currently being executed.
        self.current_benchmark_start = 0                                         #: Unix timestamp when the current benchmark run started.
        self.volumeid = ""                                                       #: Identifier of the persistent volume claimed by this configuration.
        self.max_sut_dbms = None                                                 #: Max SUT pods of this DBMS type (config.docker) allowed in the cluster at once; None means no limit.
        self.resource_sweep = True                                               #: False keeps this configuration once in a -rc/-lc/-rr/-lr/-rst sweep, e.g. for a database service outside of K8s.
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
        self.loading_started_at = None
        self.loading_after_time = None
        self.loading_finished = False
        self.loading_inherited = False
        self.storage_monitoring = None
        self.client = 1
        self.is_sut_ready = False
        self.are_worker_ready = False
        self.tenant_ready_to_load = False
        self.tenant_started_to_load = False
        self.tenant_ready_to_index = False
        self.tenant_started_to_index = False

    def removes_storage_now(self) -> bool:
        """Whether starting the SUT now deletes its existing PVCs first.

        ``-rsr`` deletes them before the first repetition only,
        ``-rsrp`` before every repetition (``-nc``). Never once loading has
        finished: the volume then holds this repetition's data.

        :return: True if existing PVCs of the SUT are to be deleted.
        :rtype: bool
        """
        if self.loading_finished:
            return False
        # entry scripts with their own parser may not know -rsrp
        args = self.experiment.args_dict
        if args.get('request_storage_remove_per_repetition'):
            return True
        return bool(args.get('request_storage_remove')) and self.num_experiment_to_apply_done == 0

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
                        'resetscript':      tmpl.get('resetscript', []),
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
                'resetscript': tmpl.get('resetscript', []),
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
        resetscript: list = None,
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
        :param resetscript: Scripts exec'd synchronously on the SUT before this
            entry's pod is submitted (e.g. ``['reset-benchbase.sql']``).
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
            'resetscript': resetscript if resetscript is not None else [],
        }
        self.experiment_dict['benchmarker'][-1].append(entry)

    def set_benchmark_resetscript(self, scripts: list, name: str = None) -> None:
        """Attach a reset-script list to entries of the benchmarker round template.

        Sets ``resetscript`` on entries of ``experiment_dict["benchmarker"][0]``,
        which :meth:`add_benchmark_list` and :meth:`add_benchmarking_parameters`
        use as the template for every subsequent round, so calling this once
        before either of them applies the scripts to all rounds.

        :param scripts: List of script filenames exec'd synchronously on the SUT
            before this entry's pod is submitted (e.g. ``['reset-benchbase.sql']``).
        :param name: Name of the entry to target; ``None`` targets every entry
            in the round template.
        """
        if not self.experiment_dict['benchmarker'] or not self.experiment_dict['benchmarker'][0]:
            return
        for entry in self.experiment_dict['benchmarker'][0]:
            if name is None or entry['name'] == name:
                entry['resetscript'] = scripts

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

        All loader entries run simultaneously during the loading phase, each as
        an independent Kubernetes Job (see :meth:`.loading.LoadingCoordinator.start_pod`).
        Experiment-wide :attr:`~bexhoma.experiments.base.default_loading_parameters`
        are merged in first, same as :meth:`set_loading_parameters` does for the
        primary (index-0) entry; ``env_vars`` win on conflict.

        :param name: Short identifier for this loader entry.
        :param template: K8s job template filename.
        :param benchmarker: Tool name — identifies the evaluator's ``log_to_df_loading()``.
        :param parallelism: Max concurrent pods (K8s ``spec.parallelism``).
        :param num_pods: Total pods that must complete (K8s ``spec.completions``).
            Defaults to ``parallelism``.
        :param target: Component the job runs against (default ``'sut'``).
        :param env_vars: ENV vars injected into the container.
        """
        parameters = {**self.experiment.default_loading_parameters, **env_vars}
        entry = {
            'name':        name,
            'benchmarker': benchmarker,
            'template':    template,
            'parallelism': parallelism,
            'num_pods':    num_pods if num_pods is not None else parallelism,
            'target':      target,
            'parameters':  parameters,
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

    def set_script_target(self, target: str) -> None:
        """Set where shell init and reset scripts run.

        ``'workers'`` runs ``.sh`` scripts in every stateful worker pod (where the
        data of a cluster is, e.g. ``SAVE`` per Dragonfly or Redis cluster node);
        SQL scripts keep running once through ``loadData``.

        :param target: ``'sut'`` (default) or ``'workers'``.
        :raises ValueError: For any other value.
        """
        if target not in ('sut', 'workers'):
            raise ValueError(f"script target must be 'sut' or 'workers', got {target!r}")
        self.script_target = target

    def set_data_components(self, components: Optional[list]) -> None:
        """Set the StatefulSet components that hold data.

        Only these get the experiment's ``-rc/-rr/-lc/-lr`` and ``-rss``; the
        others (e.g. TiDB's PD) keep the resources and volume size of the
        template. ``None`` means all StatefulSets (the default).

        :param components: ``component`` labels, e.g. ``['tikv']``, or ``None``.
        """
        self.data_components = None if components is None else list(components)

    def receives_experiment_resources(self, component: str) -> bool:
        """Return True iff a StatefulSet component gets the experiment's resources and volume size.

        :param component: ``component`` label of the StatefulSet.
        :rtype: bool
        """
        data_components = getattr(self, 'data_components', None)
        return data_components is None or component in data_components

    def set_sut_role(self, role: str) -> None:
        """Set whether the SUT Deployment holds data.

        A ``'placeholder'`` SUT (entry point, client or helper pod of a cluster)
        keeps the resources of its template; node pinning (``-rnn``) still applies.

        :param role: ``'data'`` (default) or ``'placeholder'``.
        :raises ValueError: For any other value.
        """
        if role not in ('data', 'placeholder'):
            raise ValueError(f"SUT role must be 'data' or 'placeholder', got {role!r}")
        self.sut_role = role

    def set_pvc_selector(self, label_selector: str) -> None:
        """Add the PVCs of a label selector to the volumes of the storage metrics.

        For volumes bexhoma does not create itself, e.g. the tserver PVCs of the
        YugabyteDB Helm chart (``app=yb-tserver``), so ``{rbd_images}`` covers them.

        :param label_selector: Kubernetes label selector; empty switches it off.
        """
        self.pvc_selector = label_selector or ''

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

        Merges into the parameters set so far (e.g. the experiment's).

        :param kwargs: Parameter dict, e.g. ``index='btree'``.
        """
        self.ddl_parameters = {**self.ddl_parameters, **kwargs}

    def set_eval_parameters(self, **kwargs) -> None:
        """Set evaluation parameters forwarded to the benchmarker component.

        :param kwargs: Parameter dict, e.g. ``type='noindex'``.
        """
        self.eval_parameters = {**self.eval_parameters, **kwargs}

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
        Also broadcasts onto every entry in the first benchmarker round in
        ``experiment_dict`` — an entry's own pre-existing ``parameters`` (e.g. a
        co-running different-tool benchmark's own ``SF`` override) win over this
        broadcast on conflict, mirroring the precedence ``create_manifest_benchmarking()``
        applies at job-submission time.

        :param kwargs: Parameter dict.
        """
        self.benchmarking_parameters = {**self.experiment.default_benchmarking_parameters, **kwargs}
        if self.experiment_dict['benchmarker'] and self.experiment_dict['benchmarker'][0]:
            for entry in self.experiment_dict['benchmarker'][0]:
                entry['parameters'] = {**self.benchmarking_parameters, **entry['parameters']}

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

    def apply_load_durability(self) -> list:
        """Replace the ``-xld`` placeholders of the init and post-load scripts (once).

        ``durability.sql`` and ``restoredurability.sql`` in :attr:`initscript` /
        :attr:`indexscript` (from the cluster config) become the scripts of the
        level that the DBMS folder (``experiments/<benchmark>/<path_experiment_docker>``)
        has, as for index or constraint scripts.

        :return: The included durability scripts.
        :rtype: list
        """
        if self.load_durability_scripts is not None:
            return self.load_durability_scripts
        folder = os.path.join(self.experiment.cluster.experiments_configfolder, self.path_experiment_docker)
        before = set(self.initscript) | set(self.indexscript)
        self.initscript = expand_durability_placeholders(self.initscript, self.load_durability, folder)
        self.indexscript = expand_durability_placeholders(self.indexscript, self.load_durability, folder)
        self.load_durability_scripts = [s for s in self.initscript + self.indexscript if s not in before]
        print("{:30s}: load durability {}, scripts {}".format(
            self.configuration, self.load_durability, self.load_durability_scripts))
        self.connection_parameter['load_durability'] = self.load_durability
        return self.load_durability_scripts

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
        self.experiment.cluster.set_redis_values(self._pod_configs(queue_key, num_pods, parameters, pod_parameters))

    @staticmethod
    def _pod_configs(queue_key: str, num_pods: int, parameters: dict, pod_parameters: list) -> dict:
        """Per-pod merged configurations, as :meth:`_push_pod_configs` stores them.

        :param queue_key: Base Redis queue key.
        :param num_pods: Number of pods in this job.
        :param parameters: Default parameter dict shared by all pods.
        :param pod_parameters: Per-pod override dicts.
        :return: ``{queue_key}-config-{i}`` to the merged dict, for i in 1..num_pods.
        """
        configs = {}
        for i in range(1, num_pods + 1):
            merged = dict(parameters)
            if pod_parameters and i - 1 < len(pod_parameters):
                merged.update(pod_parameters[i - 1])
            configs[f"{queue_key}-config-{i}"] = merged
        return configs

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
        storageConfiguration = self.get_storage_configuration()
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

    def get_num_worker(self, component: str = 'worker') -> int:
        """Return the resolved replica count for a StatefulSet-kind component.

        Falls back to :attr:`num_worker` when no ``replicas_<component>`` override
        was set via :meth:`set_resources`. This is what lets a SUT with a single
        StatefulSet component (e.g. CockroachDB's or Redis's ``worker``) keep
        using ``-nw`` unchanged, while a SUT with several independently-sized
        StatefulSet components (e.g. TiDB's ``pd`` and ``tikv``) can size each
        one separately by setting ``replicas_<component>`` via :meth:`set_resources`.

        :param component: Component label of the StatefulSet, e.g. ``'worker'`` or ``'pd'``.
        :return: Number of replicas to run for this component.
        :rtype: int
        """
        return self.resources.get('replicas_{}'.format(component), self.num_worker)

    def get_worker_pods(self, component: str = 'worker', only_stateful: bool = False) -> list:
        """Return a list of all worker pod names for the current SUT.

        When :attr:`statefulset_name` is set (StatefulSets bexhoma did not
        create, e.g. YugabyteDB's ``yb-tserver`` and ``yb-master``), returns
        the pods of the component's own StatefulSet (``deployment_infos``),
        falling back to :attr:`statefulset_name` for an unknown component.
        Otherwise finds pods via the standard bexhoma label selector.

        :param component: Component label used in the label selector.
        :param only_stateful: When True, return only stateful set pods (pods
            whose names end with a numeric index).
        :return: List of pod name strings.
        :rtype: list[str]
        """
        if self.statefulset_name:
            name = (self.deployment_infos.get('statefulset', {}).get(component, {}).get('name')
                    or self.statefulset_name)
            return self.experiment.cluster.get_stateful_set_pods(name)
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

    @staticmethod
    def pods_pattern(configuration: str, experiment: str) -> str:
        """Pod regex for ``{pods}``: every pod whose name contains ``<configuration>-<experiment>``.

        The pattern the cAdvisor templates had literally before ``{pods}``.

        :param configuration: Configuration name, or a regex group of worker names.
        :param experiment: Experiment code; empty for workers.
        :return: The regex.
        :rtype: str
        """
        return f"(.*){configuration}-{experiment}(.*)"

    def job_pods_pattern(self, jobname: str, all_jobs_with_prefix: bool = False) -> str:
        """Pod regex for ``{pods}`` selecting the pods of one job.

        Kubernetes names a job's pods ``<jobname>-<5 characters>`` and cuts
        ``<jobname>-`` to 58 characters first. Prometheus anchors the regex, so
        ``…-1-1`` does not match the pods of ``…-1-10``.

        :param jobname: Job name, as :meth:`generate_component_name` gives it.
        :param all_jobs_with_prefix: Match every job whose name starts with
            ``<jobname>-`` instead (the loading jobs of a repetition).
        :return: The regex.
        :rtype: str
        """
        if all_jobs_with_prefix:
            return (jobname + "-")[:58] + ".+"
        return (jobname + "-")[:58] + "[a-z0-9]{5}"

    def monitoring_namespace(self) -> str:
        """Namespace for ``{namespace}`` in metric templates.

        :return: The cluster context's namespace; empty without a cluster context (tests).
        :rtype: str
        """
        contextdata = getattr(self.experiment.cluster, 'contextdata', None) or {}
        return contextdata.get('namespace', '')

    def set_metric_of_config_default(
        self,
        metric: str,
        host: str,
        gpuid: str,
        schema: str,
        database: str,
        experiment: str = None,
        pods: str = None,
    ) -> str:
        """Substitute placeholders in a PromQL query for bexhoma-managed components.

        :param metric: Parametrised PromQL query string.
        :param host: Hostname of the node to monitor.
        :param gpuid: GPU identifier (or empty string).
        :param schema: Database schema name.
        :param database: Database name.
        :param experiment: Experiment code; defaults to :attr:`code`.
        :param pods: Pod regex for ``{pods}``; defaults to :meth:`pods_pattern`
            of this configuration (a job's own pods: :meth:`job_pods_pattern`).
        :return: Filled PromQL query string.
        :rtype: str
        """
        if experiment is None:
            experiment = self.code
        configuration = self.configuration.lower()
        experiment_name = self.get_experiment_name()
        if pods is None:
            pods = self.pods_pattern(configuration, experiment_name)
        return metric.format(
            host=host,
            gpuid=gpuid,
            configuration=configuration,
            experiment=experiment_name,
            schema=schema,
            database=database,
            pods=pods,
            namespace=self.monitoring_namespace(),
            **self.storage_placeholder_values(),
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
                host=host, gpuid=gpuid, configuration=component, experiment='',
                pods=self.pods_pattern(component, ''), namespace=self.monitoring_namespace(),
                **self.storage_placeholder_values())
        if self.num_worker > 0:
            if len(component) == 0:
                components = list(self.deployment_infos['statefulset'].keys())
                names_of_workers = [
                    self.get_worker_name(component=c).lower() for c in components
                ]
                configuration = '(' + '|'.join(names_of_workers) + ')'
                return metric.format(
                    host=host, gpuid=gpuid, configuration=configuration,
                    experiment="", schema=schema, database=database,
                    pods=self.pods_pattern(configuration, ''), namespace=self.monitoring_namespace(),
                    **self.storage_placeholder_values())
            name_worker = self.get_worker_name(component=component)
            return metric.format(
                host=host, gpuid=gpuid, configuration=name_worker,
                experiment="", schema=schema, database=database,
                pods=self.pods_pattern(name_worker, ''), namespace=self.monitoring_namespace(),
                **self.storage_placeholder_values())
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
        retry_interrupted: bool = True,
        api: bool = False,
    ):
        """Run a shell command inside the SUT container.

        Defaults to the current SUT pod and the container named ``"dbms"``.

        :param command: Shell command to run.
        :param pod: Pod name; defaults to :attr:`pod_sut`.
        :param container: Container name; defaults to :attr:`sut_container_name`.
        :param params: Optional additional parameters (currently unused).
        :param retry_interrupted: Whether to rerun the command after the
            cluster connection broke mid-command; ``False`` for commands that
            are not safe to repeat.
        :param api: Run it through the Python client
            (``cluster.execute_command_in_pod_api()``, falls back to kubectl);
            only for read-only commands that are safe to repeat.
        :return: stdout of the shell command.
        """
        if len(pod) == 0:
            pod = self.pod_sut
        if len(container) == 0:
            container = self.sut_container_name
        if self.pod_sut == '':
            self.check_sut()
        if api and hasattr(self.experiment.cluster, 'execute_command_in_pod_api'):
            return self.experiment.cluster.execute_command_in_pod_api(
                command=command, pod=pod, container=container)
        return self.experiment.cluster.execute_command_in_pod(
            command=command, pod=pod, container=container, params=params,
            retry_interrupted=retry_interrupted)

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
                    with open(filename_log, "w", encoding='utf-8') as logfile:
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

    def resolve_storage_monitoring(self) -> dict:
        """Resolve the storage placeholders of monitoring queries, once.

        Fills ``{storage_class}``, ``{pool}`` and ``{rbd_images}`` from this
        configuration's volumes (see :mod:`bexhoma.ceph_storage`). Ephemeral
        and ``ramdisk`` storage make no API call. Never raises: whatever
        cannot be resolved stays empty and ``reason`` says why, so the metrics
        that need it are switched off. Call it only after the SUT is
        deployed, when its PVCs exist.

        :return: The ``storage_monitoring`` record, also kept on the configuration.
        :rtype: dict
        """
        if getattr(self, 'storage_monitoring', None) is not None:
            return self.storage_monitoring
        storage_class = self.storage.get('storageClassName') if self.storage else None
        if storage_class is None:
            record = ceph_storage.storage_monitoring_record(reason='ephemeral storage: no Ceph volume')
        elif storage_class == 'ramdisk':
            record = ceph_storage.storage_monitoring_record(reason='ramdisk: no Ceph volume')
        else:
            record = self._resolve_ceph_storage(storage_class)
        self.storage_monitoring = record
        return record

    def _resolve_ceph_storage(self, configured_class: str) -> dict:
        """Look up class, pool, RBD images and Prometheus support of this configuration's PVCs.

        :param configured_class: ``storageClassName`` as configured (``''`` is
            the cluster's default class).
        :return: The ``storage_monitoring`` record.
        :rtype: dict
        """
        cluster = self.experiment.cluster
        pvcs = self.get_list_of_pvc()
        pvc_selector = getattr(self, 'pvc_selector', '')
        if pvc_selector:
            # volumes bexhoma did not create (e.g. a Helm chart's tservers)
            pvcs = pvcs + [pvc for pvc in cluster.get_pvc_by_selector(pvc_selector) if pvc not in pvcs]
        storage_class = configured_class
        if pvcs:
            storage_class = cluster.get_pvc_storage_class(pvcs[0]) or configured_class
        if not storage_class:
            return ceph_storage.storage_monitoring_record(reason='no PVC found to resolve the default storage class')
        info = cluster.get_storage_class_info(storage_class)
        provisioner, pool, kind = info.get('provisioner', ''), info.get('pool', ''), info.get('kind', '')
        if not info:
            return ceph_storage.storage_monitoring_record(
                storage_class, reason=f'StorageClass {storage_class} could not be read')
        if not pool:
            return ceph_storage.storage_monitoring_record(
                storage_class, provisioner, reason=f'{provisioner or "unknown provisioner"} is not a Ceph CSI provisioner')
        images = ''
        if kind == 'rbd':
            images = ceph_storage.rbd_images_pattern(
                [image for image in (cluster.get_pvc_rbd_image(pvc) for pvc in pvcs) if image])
        support = cluster.get_ceph_metrics_support(pool)
        if support is None:
            return ceph_storage.storage_monitoring_record(
                storage_class, provisioner, pool, kind, images,
                pool_metrics=None, volume_metrics=None,
                reason='Prometheus could not be asked for Ceph metrics')
        pool_metrics = support['pool_metrics']
        volume_metrics = pool_metrics and support['volume_metrics'] and bool(images)
        reasons = []
        if not pool_metrics:
            reasons.append(f'Prometheus has no Ceph metrics for pool {pool}')
        elif kind != 'rbd':
            reasons.append(f'{kind}: no per-volume statistics')
        elif not support['volume_metrics']:
            reasons.append(f'Prometheus has no per-image statistics for pool {pool}')
        elif not images:
            reasons.append('no RBD image found for the PVCs ' + ', '.join(pvcs) if pvcs else 'no PVC found')
        return ceph_storage.storage_monitoring_record(
            storage_class, provisioner, pool, kind, images,
            pool_metrics=pool_metrics, volume_metrics=volume_metrics, reason='; '.join(reasons))

    def storage_placeholder_values(self) -> dict:
        """Return the storage placeholder values for monitoring queries.

        Empty strings until :meth:`resolve_storage_monitoring` has run, so a
        query using them is switched off rather than formatted with a guess.

        :return: ``{'storage_class': ..., 'pool': ..., 'rbd_images': ...}``.
        :rtype: dict
        """
        record = getattr(self, 'storage_monitoring', None)
        placeholders = (record or {}).get('placeholders', {})
        return {name: placeholders.get(name, '') for name in ceph_storage.STORAGE_PLACEHOLDERS}

    def use_ramdisk(self) -> bool:
        """Return True iff the storage class is ``'ramdisk'``.

        :rtype: bool
        """
        return (
            self.storage.get('storageClassName') is not None
            and self.storage['storageClassName'] == 'ramdisk'
        )

    def uses_tls_secret(self) -> bool:
        """Return True iff the DBMS entry in the cluster config asks for a TLS Secret.

        Set by ``'tls': {'secret': True}`` in the docker entry of ``cluster.config``.

        :rtype: bool
        """
        tls = (getattr(self, 'dockertemplate', None) or {}).get('tls') or {}
        return bool(tls.get('secret', False))

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

    def get_storage_configuration(self) -> str:
        """Return the name that identifies this configuration's volumes.

        It is ``storageConfiguration`` (the configuration name when unset),
        followed by the storage class when the SUT gets a volume of a named
        class, e.g. ``postgresql-cephcsi``. A volume is found again by this
        name alone, so the class has to be part of it: otherwise data loaded
        on one backend would be reused on another. Ephemeral storage, the
        cluster's default class (``''``) and ``ramdisk`` add nothing. A name
        that already ends with the class is kept as it is. DDL parameters
        that differ from their defaults add :attr:`ddl_storage_suffix` before
        the class, so data loaded with other DDL values is not found again.

        :return: Name used for the SUT's PVC, its ``configuration`` label and
            the worker StatefulSets.
        :rtype: str
        """
        storage_configuration = self.storage.get('storageConfiguration') or self.configuration
        storage_class = self.storage.get('storageClassName')
        suffix = '' if not storage_class or storage_class == 'ramdisk' else storage_suffix(storage_class)
        has_class = bool(suffix) and storage_configuration.lower().endswith(f'-{suffix}')
        ddl_suffix = getattr(self, 'ddl_storage_suffix', '')
        if ddl_suffix:
            if has_class:
                storage_configuration = storage_configuration[:-len(suffix) - 1]
                has_class = False
            storage_configuration = f'{storage_configuration}-{ddl_suffix}'
        if not suffix or has_class:
            return storage_configuration
        return f'{storage_configuration}-{suffix}'

    def use_ephemeral_storage(self) -> bool:
        """Return True iff ephemeral-storage resources should be requested for the SUT.

        This is the case when a storage size is configured but no storage class
        is set, meaning no persistent volume is created and the database files
        live in the container's ephemeral storage.

        :rtype: bool
        """
        if not self.storage:
            return False
        return (
            self.storage.get('storageClassName') is None
            and bool(self.storage.get('storageSize', ''))
        )

"""Kubernetes manifest builders for bexhoma jobs and deployments."""
from __future__ import annotations

import copy
from datetime import datetime, timedelta
from io import StringIO
from typing import TYPE_CHECKING, List, Optional, Tuple

import hiyapyco
import yaml

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['ManifestBuilder', 'find_workloads', 'ensure_arg_pairs', 'patch_container']


def find_workloads(doc: dict, kind: str, name: str) -> bool:
    """Return True if this YAML document matches the requested kind and name.

    :param doc: Parsed YAML document dict.
    :param kind: Resource kind (``'deployment'`` or ``'statefulset'``).
    :param name: Expected ``metadata.name`` value.
    :return: True iff the document kind and name match.
    :rtype: bool
    """
    k = doc.get("kind", "")
    if kind == "deployment" and k != "Deployment":
        return False
    if kind == "statefulset" and k != "StatefulSet":
        return False
    md = doc.get("metadata", {}) or {}
    return md.get("name") == name


def ensure_arg_pairs(
    args_list: Optional[List[str]], updates: List[Tuple[str, str]]
) -> List[str]:
    """Update or append ``-c key=value`` pairs in a container args list.

    :param args_list: Existing container args (e.g. ``["-c","max_connections=3000"]``).
    :param updates: List of ``(key, value)`` pairs to apply.
    :return: New args list with updates applied.
    :rtype: list[str]
    """
    args = list(args_list or [])
    pos_by_key = {}
    i = 0
    while i < len(args) - 1:
        if args[i] == "-c":
            val = args[i + 1]
            if isinstance(val, str) and "=" in val:
                k = val.split("=", 1)[0]
                pos_by_key[k] = i + 1
            i += 2
        else:
            i += 1
    for k, v in updates:
        if k in pos_by_key:
            args[pos_by_key[k]] = f"{k}={v}"
        else:
            args.extend(["-c", f"{k}={v}"])
    return args


def patch_container(doc: dict, container_name: str, param: str, value: str) -> bool:
    """Patch a single container's args in a Deployment/StatefulSet YAML doc.

    :param doc: Parsed YAML document dict.
    :param container_name: Name of the container to patch.
    :param param: Parameter key to set inside ``-c key=value``.
    :param value: Parameter value.
    :return: True iff any changes were made.
    :rtype: bool
    """
    spec = doc.get("spec", {}) or {}
    tpl = spec.get("template", {}) or {}
    pspec = tpl.get("spec", {}) or {}
    containers = pspec.get("containers", []) or []
    changed = False
    for c in containers:
        if c.get("name") != container_name:
            continue
        old_args = c.get("args", [])
        new_args = ensure_arg_pairs(old_args, [(param, value)])
        if new_args != old_args:
            c["args"] = new_args
            changed = True
    return changed


class ManifestBuilder:
    """Builds and writes Kubernetes job/deployment YAML manifests.

    Wraps ``create_manifest_job``, ``create_manifest_benchmarking``,
    ``create_manifest_maintaining``, ``create_manifest_loading``,
    ``get_patched_yaml``, and ``patch_dbms_args``.

    :param config: The parent configuration this builder belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def get_patched_yaml(self, file: str, patch: str = "") -> list:
        """Load a YAML file, optionally deep-merging a patch string, and return parsed docs.

        :param file: Path to the base YAML file.
        :param patch: Optional YAML-formatted patch string.
        :return: List of parsed YAML document dicts.
        :rtype: list
        """
        if len(patch) > 0:
            merged = hiyapyco.load([file, patch], method=hiyapyco.METHOD_MERGE)
            self._config.logger.debug(hiyapyco.dump(merged, default_flow_style=False))
            stream = StringIO(hiyapyco.dump(merged))
            result = yaml.safe_load_all(stream)
            result = [data for data in result]
            return result
        else:
            with open(file) as f:
                result = yaml.safe_load_all(f)
                result = [data for data in result]
                return result

    def patch_dbms_args(
        self, yaml_docs: List[dict], operations: List[Tuple[dict, str]]
    ) -> List[dict]:
        """Apply parameter-patch operations across all documents in a manifest.

        :param yaml_docs: List of parsed YAML document dicts.
        :param operations: List of ``(selector_dict, value_str)`` pairs.
        :return: Modified list of YAML document dicts.
        :rtype: list[dict]
        """
        for sel, val in operations:
            kind = sel["kind"]
            workload = sel["workload"]
            container = sel["container"]
            param = sel["param"]
            found_doc = False
            found_container = False
            changed_this = False
            for doc in yaml_docs:
                if not isinstance(doc, dict):
                    continue
                if not find_workloads(doc, kind, workload):
                    continue
                found_doc = True
                if patch_container(doc, container, param, val):
                    changed_this = True
                spec = doc.get("spec", {}) or {}
                tpl = spec.get("template", {}) or {}
                pspec = tpl.get("spec", {}) or {}
                containers = pspec.get("containers", []) or []
                if any(c.get("name") == container for c in containers):
                    found_container = True
            if not found_doc:
                print("{:30s}: {}[{}] not found in file".format(
                    self._config.configuration, kind, workload))
            elif not found_container:
                print("{:30s}: container[{}] not found in {}[{}]".format(
                    self._config.configuration, container, kind, workload))
            elif changed_this:
                print("{:30s}: updated {}[{}].container[{}].{} = {}".format(
                    self._config.configuration, kind, workload, container, param, val))
            else:
                print("{:30s}: {}[{}].container[{}].{} already set to desired value".format(
                    self._config.configuration, kind, workload, container, param))
        return yaml_docs

    def create_manifest_job(
        self,
        app: str = '',
        component: str = 'benchmarker',
        experiment: str = '',
        configuration: str = '',
        experimentRun: str = '',
        client: str = '1',
        parallelism: int = 1,
        env: dict = {},
        template: str = '',
        nodegroup: str = '',
        num_pods: int = 1,
        connection: str = '',
        patch_yaml: str = '',
        benchmark_run: str = '',
        template_override: str = '',
    ) -> str:
        """Create a Kubernetes job manifest and write it to the experiment path.

        :param app: App label for the job.
        :param component: Component label (e.g. ``'benchmarker'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param experimentRun: Repetition index string.
        :param client: Sequential client-round index.
        :param parallelism: Number of parallel pods.
        :param env: Extra environment variable dict merged into the job manifest.
        :param template: YAML template filename.
        :param nodegroup: Node selector group key.
        :param num_pods: Total number of pods (``spec.completions``).
        :param connection: Connection name label.
        :param patch_yaml: Optional hiyapyco YAML patch string.
        :param benchmark_run: Parallel benchmark index within a client round.
        :param template_override: When non-empty, overrides ``template``.
        :return: Path to the written YAML manifest file.
        :rtype: str
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        code = str(int(experiment))
        if not experimentRun:
            experimentRun = str(cfg.num_experiment_to_apply_done + 1)
        if template_override:
            template = template_override
        jobname = cfg.generate_component_name(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experiment_run=experimentRun,
            client=str(client), benchmark_run=benchmark_run)
        servicename = cfg.get_service_sut(configuration=configuration)
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        time_now = str(datetime.now())
        time_now_int = int(datetime.timestamp(
            datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')))
        c = copy.deepcopy(cfg.dockertemplate['template'])
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = cfg.connection_management['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = cfg.connection_management['runsPerConnection']
        c['connectionmanagement']['timeout'] = cfg.connection_management['timeout']
        c['connectionmanagement']['singleConnection'] = cfg.connection_management.get('singleConnection', True)
        env_default = dict()
        env_default['BEXHOMA_HOST'] = servicename
        env_default['BEXHOMA_CLIENT'] = int(cfg.client) - 1
        env_default['BEXHOMA_BENCHMARK_RUN'] = benchmark_run if benchmark_run else '1'
        env_default['BEXHOMA_EXPERIMENT'] = experiment
        env_default['BEXHOMA_CONNECTION'] = configuration
        env_default['BEXHOMA_CONFIGURATION'] = configuration
        env_default['BEXHOMA_SLEEP'] = '60'
        env_default['BEXHOMA_VOLUME'] = cfg.volume
        env_default['BEXHOMA_EXPERIMENT_RUN'] = experimentRun
        env_default['BEXHOMA_PARALLEL'] = str(parallelism)
        env_default['BEXHOMA_NUM_PODS'] = str(num_pods)
        env_default['BEXHOMA_DBMS'] = str(cfg.docker)
        if cfg.num_tenants > 0 and cfg.tenant_per == 'container':
            env_default['BEXHOMA_NUM_PODS_TOTAL'] = str(int(num_pods) * cfg.num_tenants)
        else:
            env_default['BEXHOMA_NUM_PODS_TOTAL'] = str(num_pods)
        env_default['PARALLEL'] = str(parallelism)
        env_default['NUM_PODS'] = str(num_pods)
        name = cfg.generate_component_name(
            app=app, component='sut', experiment=cfg.get_experiment_name(),
            configuration=configuration)
        name_worker = cfg.get_worker_name()
        name_service_headless = name_worker
        list_of_workers = []
        for worker in range(cfg.num_worker):
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(
                name_worker=name_worker, worker_number=worker,
                worker_service=name_service_headless)
            list_of_workers.append(worker_full_name)
        list_of_workers_as_string = ",".join(list_of_workers)
        env_default['BEXHOMA_WORKER_LIST'] = list_of_workers_as_string
        list_of_workers_as_string_space = " ".join(list_of_workers)
        env_default['BEXHOMA_WORKER_LIST_SPACE'] = list_of_workers_as_string_space
        env_default['BEXHOMA_SUT_NAME'] = name
        if 'JDBC' in c:
            database = c['JDBC']['database'] if 'database' in c['JDBC'] else cfg.experiment.volume
            schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else ''
            if cfg.tenant_per == 'schema':
                schema = 'DBMSBENCHMARKER_SCHEMA'
            elif cfg.tenant_per == 'database':
                database = 'DBMSBENCHMARKER_DATABASE'
            env_default['BEXHOMA_URL'] = c['JDBC']['url'].format(
                serverip=servicename,
                dbname=cfg.experiment.volume,
                DBNAME=cfg.experiment.volume.upper(),
                timout_s=c['connectionmanagement']['timeout'],
                timeout_ms=c['connectionmanagement']['timeout'] * 1000,
                namespace=cfg.experiment.cluster.namespace,
                database=database,
                schema=schema,
            )
            env_default['BEXHOMA_URL_LIST'] = c['JDBC']['url'].format(
                serverip=list_of_workers_as_string,
                dbname=cfg.experiment.volume,
                DBNAME=cfg.experiment.volume.upper(),
                timout_s=c['connectionmanagement']['timeout'],
                timeout_ms=c['connectionmanagement']['timeout'] * 1000,
                namespace=cfg.experiment.cluster.namespace,
                database=database,
                schema=schema,
            )
            env_default['BEXHOMA_USER'] = c['JDBC']['auth'][0]
            env_default['BEXHOMA_PASSWORD'] = c['JDBC']['auth'][1]
            env_default['BEXHOMA_DRIVER'] = c['JDBC']['driver']
            env_default['BEXHOMA_DATABASE'] = database
            env_default['BEXHOMA_SCHEMA'] = schema
            env_default['BEXHOMA_VOLUME'] = cfg.experiment.volume
            if isinstance(c['JDBC']['jar'], str):
                env_default['BEXHOMA_JAR'] = c['JDBC']['jar']
            else:
                env_default['BEXHOMA_JAR'] = c['JDBC']['jar'][0]
        else:
            env_default['BEXHOMA_USER'] = c['auth'][0]
            env_default['BEXHOMA_PASSWORD'] = c['auth'][1]
        if cfg.num_worker > 0:
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(
                name_worker=name_worker, worker_number=0,
                worker_service=name_service_headless)
            env_default['BEXHOMA_WORKER_FIRST'] = worker_full_name
        env = {**env_default, **env}
        cfg.logger.debug('ManifestBuilder.create_manifest_job({})'.format(jobname))
        cfg.logger.debug(env)
        job_experiment = (
            cfg.experiment.path
            + '/{app}-{component}-{configuration}-{experimentRun}-{client}.yml'.format(
                app=app, component=component, configuration=configuration,
                experimentRun=experimentRun, client=client).lower()
        )
        try:
            result = self.get_patched_yaml(
                cfg.experiment.cluster.yamlfolder + template, patch_yaml)
        except yaml.YAMLError as exc:
            print(exc)
        for dep in result:
            if dep['kind'] == 'Job':
                dep['metadata']['name'] = jobname
                dep['spec']['completions'] = num_pods
                dep['spec']['parallelism'] = parallelism
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['component'] = component
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['connection'] = connection
                dep['metadata']['labels']['dbms'] = cfg.docker
                dep['metadata']['labels']['experiment'] = str(experiment)
                dep['metadata']['labels']['client'] = str(client)
                dep['metadata']['labels']['experimentRun'] = str(experimentRun)
                dep['metadata']['labels']['volume'] = cfg.volume
                for label_key, label_value in cfg.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['metadata']['labels']['start_time'] = str(time_now_int)
                dep['spec']['template']['metadata']['labels']['app'] = app
                dep['spec']['template']['metadata']['labels']['component'] = component
                dep['spec']['template']['metadata']['labels']['configuration'] = configuration
                dep['spec']['template']['metadata']['labels']['connection'] = connection
                dep['spec']['template']['metadata']['labels']['dbms'] = cfg.docker
                dep['spec']['template']['metadata']['labels']['experiment'] = str(experiment)
                dep['spec']['template']['metadata']['labels']['client'] = str(client)
                dep['spec']['template']['metadata']['labels']['experimentRun'] = str(experimentRun)
                dep['spec']['template']['metadata']['labels']['volume'] = cfg.volume
                for label_key, label_value in cfg.additional_labels.items():
                    dep['spec']['template']['metadata']['labels'][label_key] = str(label_value)
                dep['spec']['template']['metadata']['labels']['start_time'] = str(time_now_int)
                for i_container, cont in enumerate(dep['spec']['template']['spec']['containers']):
                    env_manifest = {}
                    envs = cont['env']
                    for _, e in enumerate(envs):
                        env_manifest[e['name']] = e['value']
                    env_merged = {**env_manifest, **env}
                    cfg.logger.debug(
                        'ManifestBuilder.create_manifest_job({})'.format(str(env_merged)))
                    dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    for i, e in env_merged.items():
                        dep['spec']['template']['spec']['containers'][i_container]['env'].append(
                            {'name': i, 'value': str(e)})
                if 'initContainers' in dep['spec']['template']['spec']:
                    for i_container, cont in enumerate(
                            dep['spec']['template']['spec']['initContainers']):
                        env_manifest = {}
                        envs = cont['env']
                        for _, e in enumerate(envs):
                            env_manifest[e['name']] = e['value']
                        env_merged = {**env_manifest, **env}
                        dep['spec']['template']['spec']['initContainers'][i_container]['env'] = []
                        for i, e in env_merged.items():
                            dep['spec']['template']['spec']['initContainers'][i_container]['env'].append(
                                {'name': i, 'value': str(e)})
                if len(nodegroup) and nodegroup in cfg.nodes:
                    if 'nodeSelector' not in dep['spec']['template']['spec']:
                        dep['spec']['template']['spec']['nodeSelector'] = dict()
                    if dep['spec']['template']['spec']['nodeSelector'] is None:
                        dep['spec']['template']['spec']['nodeSelector'] = dict()
                    dep['spec']['template']['spec']['nodeSelector']['type'] = cfg.nodes[nodegroup]
        with open(job_experiment, "w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        return job_experiment

    def create_manifest_benchmarking(
        self,
        connection: str,
        app: str = '',
        component: str = 'benchmarker',
        experiment: str = '',
        configuration: str = '',
        experimentRun: str = '',
        client: str = '1',
        parallelism: int = 1,
        alias: str = '',
        env: dict = {},
        template: str = '',
        num_pods: int = 1,
        benchmark_run: str = '',
        template_override: str = '',
    ) -> str:
        """Create a benchmarker job manifest.

        Template resolution priority: ``template_override`` > ``template`` argument >
        ``self.experiment.jobtemplate_benchmarking`` > default
        ``"jobtemplate-benchmarking-dbmsbenchmarker.yml"``.

        :param connection: Connection/configuration name for dbmsbenchmarker.
        :param app: App label.
        :param component: Component label (default ``'benchmarker'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param experimentRun: Repetition index string.
        :param client: Sequential client-round index.
        :param parallelism: Number of parallel pods.
        :param alias: Alias name forwarded to dbmsbenchmarker.
        :param env: Extra environment variables merged into the job ENV.
        :param template: Optional YAML template filename override.
        :param num_pods: Total pod count.
        :param benchmark_run: Parallel benchmark index within a client round.
        :param template_override: When non-empty, takes precedence over all other template resolution.
        :return: Path to the written YAML manifest file.
        :rtype: str
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        code = str(int(experiment))
        experimentRun = str(cfg.num_experiment_to_apply_done + 1)
        cfg.logger.debug('ManifestBuilder.create_manifest_benchmarking()')
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        base_env = {
            'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_PODS': str(num_pods),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias,
        }
        env = {**base_env, **env, **cfg.loading_parameters, **cfg.benchmarking_parameters}
        if len(template) == 0:
            if len(cfg.experiment.jobtemplate_benchmarking) > 0:
                template = cfg.experiment.jobtemplate_benchmarking
            else:
                template = "jobtemplate-benchmarking-dbmsbenchmarker.yml"
        return self.create_manifest_job(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experimentRun=experimentRun,
            client=client, parallelism=parallelism, env=env, template=template,
            num_pods=num_pods, nodegroup='benchmarking', connection=connection,
            patch_yaml=cfg.benchmarking_patch, benchmark_run=benchmark_run,
            template_override=template_override)

    def create_manifest_maintaining(
        self,
        app: str = '',
        component: str = 'maintaining',
        experiment: str = '',
        configuration: str = '',
        parallelism: int = 1,
        alias: str = '',
        num_pods: int = 1,
        connection: str = '',
    ) -> str:
        """Create a maintaining job manifest.

        :param app: App label.
        :param component: Component label (default ``'maintaining'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param parallelism: Number of parallel pods.
        :param alias: Alias forwarded to dbmsbenchmarker.
        :param num_pods: Total pod count.
        :param connection: Connection name label.
        :return: Path to the written YAML manifest file.
        :rtype: str
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        code = str(int(experiment))
        experimentRun = str(cfg.num_experiment_to_apply_done + 1)
        connection = cfg.configuration
        servicename = cfg.get_service_sut(configuration=configuration)
        cfg.logger.debug('ManifestBuilder.create_manifest_maintaining()')
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        start = now + timedelta(seconds=180)
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        env = {
            'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': start_string,
            'DBMSBENCHMARKER_CLIENT': str(parallelism),
            'DBMSBENCHMARKER_CODE': code,
            'DBMSBENCHMARKER_CONNECTION': connection,
            'BEXHOMA_CONNECTION': connection,
            'DBMSBENCHMARKER_SLEEP': str(60),
            'DBMSBENCHMARKER_ALIAS': alias,
            'SENSOR_DATABASE': 'postgresql://postgres:@{}:9091/postgres'.format(servicename),
        }
        env = {**env, **cfg.maintaining_parameters}
        template = "jobtemplate-maintaining.yml"
        if len(cfg.experiment.jobtemplate_maintaining) > 0:
            template = cfg.experiment.jobtemplate_maintaining
        return self.create_manifest_job(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experimentRun=experimentRun,
            client=1, parallelism=parallelism, env=env, template=template,
            num_pods=num_pods, nodegroup='maintaining', connection=connection)

    def create_manifest_loading(
        self,
        app: str = '',
        component: str = 'loading',
        experiment: str = '',
        configuration: str = '',
        parallelism: int = 1,
        alias: str = '',
        num_pods: int = 1,
        connection: str = '',
        benchmark_run: str = '',
        template_override: str = '',
    ) -> str:
        """Create a loading job manifest.

        :param app: App label.
        :param component: Component label (default ``'loading'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param parallelism: Number of parallel pods.
        :param alias: Alias (unused, kept for API symmetry).
        :param num_pods: Total pods that must complete (``spec.completions``).
        :param connection: Connection name label.
        :param benchmark_run: Loader index forwarded to :meth:`create_manifest_job`.
        :param template_override: When non-empty, overrides template resolution.
        :return: Path to the written YAML manifest file.
        :rtype: str
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        experimentRun = str(cfg.num_experiment_to_apply_done + 1)
        connection = cfg.configuration
        cfg.logger.debug('ManifestBuilder.create_manifest_loading()')
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        env = {
            'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,
        }
        if len(cfg.loading_parameters):
            cfg.connection_parameter['loading_parameters'] = cfg.loading_parameters
        env = {**env, **cfg.loading_parameters}
        cfg.logger.debug("create_manifest_loading:env={}".format(env))
        template = "jobtemplate-loading.yml"
        if len(cfg.experiment.jobtemplate_loading) > 0:
            template = cfg.experiment.jobtemplate_loading
        if len(cfg.jobtemplate_loading) > 0:
            template = cfg.jobtemplate_loading
        return self.create_manifest_job(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experimentRun=experimentRun,
            client=1, parallelism=parallelism, env=env, template=template,
            nodegroup='loading', num_pods=num_pods, connection=connection,
            patch_yaml=cfg.loading_patch, benchmark_run=benchmark_run,
            template_override=template_override)

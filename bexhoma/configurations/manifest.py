"""Kubernetes manifest builders for bexhoma jobs and deployments."""
from __future__ import annotations

import copy
from datetime import datetime, timedelta
from io import StringIO
from typing import TYPE_CHECKING, List, Optional, Tuple

import hiyapyco
import yaml

from ..tls import TLS_ENV, TLS_VOLUME, apply_tls_volume

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = [
    'ManifestBuilder', 'find_workloads', 'ensure_arg_pairs', 'ensure_arg_flags', 'ensure_env',
    'detect_arg_style', 'patch_container', 'ARG_STYLE_ANNOTATION', 'ARG_STYLE_PG', 'ARG_STYLE_FLAG',
    'ENV_PARAM_PREFIX',
]

#: Workload annotation that declares how ``--set`` writes container args.
ARG_STYLE_ANNOTATION = 'bexhoma/arg-style'
#: PostgreSQL style: ``["-c", "key=value"]`` pairs.
ARG_STYLE_PG = 'pg'
#: MySQL/MariaDB style: one ``"--key=value"`` element per setting.
ARG_STYLE_FLAG = 'flag'
#: ``--set`` parameter prefix that targets the container's ``env`` list instead of its args.
ENV_PARAM_PREFIX = 'env.'


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


def _flag_name(name: str) -> str:
    """Normalise a flag name for comparison: MySQL treats ``-`` and ``_`` alike."""
    return name.replace("-", "_").lower()


def ensure_arg_flags(
    args_list: Optional[List[str]], updates: List[Tuple[str, str]]
) -> List[str]:
    """Update or append ``--key=value`` elements in a container args list.

    Names match regardless of ``-``/``_`` (``innodb_buffer_pool_size`` replaces
    ``--innodb-buffer-pool-size=96G``); a replaced element keeps the template's
    spelling of the name. Valueless flags (``--skip-log-bin``) are left alone.

    :param args_list: Existing container args (e.g. ``["--max_connections=1500"]``).
    :param updates: List of ``(key, value)`` pairs to apply.
    :return: New args list with updates applied.
    :rtype: list[str]
    """
    args = list(args_list or [])
    pos_by_key = {}
    for i, arg in enumerate(args):
        if isinstance(arg, str) and arg.startswith("--") and "=" in arg:
            name = arg[2:].split("=", 1)[0]
            pos_by_key[_flag_name(name)] = (i, name)
    for k, v in updates:
        hit = pos_by_key.get(_flag_name(k))
        if hit is not None:
            args[hit[0]] = f"--{hit[1]}={v}"
        else:
            args.append(f"--{k}={v}")
            pos_by_key[_flag_name(k)] = (len(args) - 1, k)
    return args


def ensure_env(env_list: Optional[list], name: str, value: str) -> list:
    """Set or replace one entry in a container ``env`` list.

    An existing entry (also one with ``valueFrom``) is replaced by a plain
    ``{name, value}``; a new one is appended.

    :param env_list: Existing container env list.
    :param name: Environment variable name.
    :param value: Value; stored as a string.
    :return: New env list.
    :rtype: list
    """
    env = [dict(e) for e in (env_list or [])]
    for e in env:
        if e.get("name") == name:
            e.pop("valueFrom", None)
            e["value"] = str(value)
            return env
    env.append({"name": name, "value": str(value)})
    return env


def detect_arg_style(doc: dict, args_list: Optional[List[str]]) -> str:
    """Return how ``--set`` writes args into this workload's container.

    The ``bexhoma/arg-style`` annotation of the workload wins (``pg`` or ``flag``).
    Otherwise the existing args decide: ``-c key=value`` pairs -> ``pg``,
    ``--key=value`` elements -> ``flag``; no hint -> ``pg`` (backward compatible).

    :param doc: Parsed Deployment/StatefulSet document.
    :param args_list: Args of the container that is patched.
    :return: :data:`ARG_STYLE_PG` or :data:`ARG_STYLE_FLAG`.
    :rtype: str
    """
    md = doc.get("metadata", {}) or {}
    annotations = md.get("annotations", {}) or {}
    declared = str(annotations.get(ARG_STYLE_ANNOTATION, "")).strip().lower()
    if declared in (ARG_STYLE_PG, ARG_STYLE_FLAG):
        return declared
    args = list(args_list or [])
    if any(a == "-c" for a in args):
        return ARG_STYLE_PG
    if any(isinstance(a, str) and a.startswith("--") and "=" in a for a in args):
        return ARG_STYLE_FLAG
    return ARG_STYLE_PG


def patch_container(doc: dict, container_name: str, param: str, value: str) -> bool:
    """Patch a single container in a Deployment/StatefulSet YAML doc.

    ``param`` of the form ``env.NAME`` sets the environment variable ``NAME``;
    any other ``param`` is written into the args in the workload's arg style
    (see :func:`detect_arg_style`): ``-c key=value`` or ``--key=value``.

    :param doc: Parsed YAML document dict.
    :param container_name: Name of the container to patch.
    :param param: Parameter key, or ``env.NAME``.
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
        if param.startswith(ENV_PARAM_PREFIX):
            old_env = c.get("env", []) or []
            new_env = ensure_env(old_env, param[len(ENV_PARAM_PREFIX):], value)
            if new_env != old_env:
                c["env"] = new_env
                changed = True
            continue
        old_args = c.get("args", [])
        if detect_arg_style(doc, old_args) == ARG_STYLE_FLAG:
            new_args = ensure_arg_flags(old_args, [(param, value)])
        else:
            new_args = ensure_arg_pairs(old_args, [(param, value)])
        if new_args != old_args:
            c["args"] = new_args
            changed = True
    return changed


class ManifestBuilder:
    """Builds and writes Kubernetes job/deployment YAML manifests.

    Wraps ``create_manifest_job``, ``create_manifest_benchmarking``,
    ``create_manifest_loading``, ``get_patched_yaml``, and ``patch_dbms_args``.

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

        An operation whose selector carries a ``config`` scope (parsed from
        ``deployment[NAME]@CONFIG...``, see :func:`~bexhoma.experiments.base.parse_set_arg`)
        is silently skipped when it does not name this configuration's own
        :attr:`~bexhoma.configurations.base.SutConfiguration.configuration`. This is what
        lets several configurations built from the same docker image (a resource sweep)
        each receive their own derived knob values from one shared, experiment-wide
        ``--set`` list — every configuration is patched with the same operations, but
        each only applies the ones scoped to it (or unscoped, which apply to all).

        :param yaml_docs: List of parsed YAML document dicts.
        :param operations: List of ``(selector_dict, value_str)`` pairs.
        :return: Modified list of YAML document dicts.
        :rtype: list[dict]
        """
        for sel, val in operations:
            config_scope = sel.get("config")
            if config_scope and config_scope != self._config.configuration:
                continue
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
        experiment_run: str = '',
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
        :param experiment_run: Repetition index string.
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
        if not experiment_run:
            experiment_run = str(cfg.num_experiment_to_apply_done + 1)
        if template_override:
            template = template_override
        jobname = cfg.generate_component_name(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experiment_run=experiment_run,
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
        env_default['BEXHOMA_EXPERIMENT_RUN'] = experiment_run
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
        # Suffixed by benchmark_run (when given) so that two entries sharing the same
        # (app, component, configuration, experiment_run, client) — e.g. two parallel
        # loader entries, always client=1, distinguished only by data_job/benchmark_run,
        # or two parallel benchmarker entries in the same client round — get their own
        # manifest file on disk instead of the later one silently overwriting the earlier
        # one's.
        benchmark_run_suffix = '-{}'.format(benchmark_run) if benchmark_run else ''
        job_experiment = (
            cfg.experiment.path
            + '/{app}-{component}-{configuration}-{experiment}-{experiment_run}-{client}{benchmark_run_suffix}.yml'.format(
                app=app, component=component, configuration=configuration,
                experiment=code, experiment_run=experiment_run, client=client,
                benchmark_run_suffix=benchmark_run_suffix).lower()
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
                dep['metadata']['labels']['experiment_run'] = str(experiment_run)
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
                dep['spec']['template']['metadata']['labels']['experiment_run'] = str(experiment_run)
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
                # the CA of the SUT's TLS Secret, for clients that need a CA file (HammerDB)
                pod_spec = dep['spec']['template']['spec']
                if apply_tls_volume(pod_spec, getattr(cfg, 'tls_secret', '')):
                    for cont in pod_spec['containers']:
                        if any(m.get('name') == TLS_VOLUME for m in cont.get('volumeMounts') or []):
                            cont['env'] = ensure_env(cont.get('env'), TLS_ENV, 'true')
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
        experiment_run: str = '',
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
        :param experiment_run: Repetition index string.
        :param client: Sequential client-round index.
        :param parallelism: Number of parallel pods.
        :param alias: Alias name forwarded to dbmsbenchmarker.
        :param env: Extra environment variables merged into the job ENV; take
            precedence over :attr:`SutConfiguration.benchmarking_parameters` on
            conflict, so a non-primary round entry (e.g. a benchmark registered
            via ``experiment.add_benchmark()`` alongside the primary, such as the
            TPC-H refresh stream or a co-running different-tool benchmark) can
            override a shared default like ``SF`` instead of inheriting a value
            that may not even be valid for its own tool's format.
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
        experiment_run = str(cfg.num_experiment_to_apply_done + 1)
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
        env = {**base_env, **cfg.loading_parameters, **cfg.benchmarking_parameters, **env}
        if len(template) == 0:
            if len(cfg.experiment.jobtemplate_benchmarking) > 0:
                template = cfg.experiment.jobtemplate_benchmarking
            else:
                template = "jobtemplate-benchmarking-dbmsbenchmarker.yml"
        return self.create_manifest_job(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experiment_run=experiment_run,
            client=client, parallelism=parallelism, env=env, template=template,
            num_pods=num_pods, nodegroup='benchmarking', connection=connection,
            patch_yaml=cfg.benchmarking_patch, benchmark_run=benchmark_run,
            template_override=template_override)

    def create_manifest_loading(
        self,
        app: str = '',
        component: str = 'loading',
        experiment: str = '',
        configuration: str = '',
        parallelism: int = 1,
        alias: str = '',
        env: dict = {},
        num_pods: int = 1,
        connection: str = '',
        benchmark_run: str = '',
        template_override: str = '',
    ) -> str:
        """Create a loading job manifest.

        Template resolution priority: ``template_override`` > ``self.jobtemplate_loading``
        (config-level) > ``self.experiment.jobtemplate_loading`` (experiment-level) >
        default ``"jobtemplate-loading.yml"``.

        :param app: App label.
        :param component: Component label (default ``'loading'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param parallelism: Number of parallel pods.
        :param alias: Alias (unused, kept for API symmetry).
        :param env: Extra environment variables merged into the job ENV; take
            precedence over :attr:`SutConfiguration.loading_parameters` on conflict,
            so a non-primary :class:`~bexhoma.configurations.loading.LoadingCoordinator`
            entry (see :meth:`SutConfiguration.add_loading_parameters`) does not
            inherit the primary entry's env vars where they collide.
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
        experiment_run = str(cfg.num_experiment_to_apply_done + 1)
        connection = cfg.configuration
        cfg.logger.debug('ManifestBuilder.create_manifest_loading()')
        now = datetime.utcnow()
        now_string = now.strftime('%Y-%m-%d %H:%M:%S')
        base_env = {
            'BEXHOMA_TIME_NOW': now_string,
            'BEXHOMA_TIME_START': 0,
        }
        if len(cfg.loading_parameters):
            cfg.connection_parameter['loading_parameters'] = cfg.loading_parameters
        env = {**base_env, **cfg.loading_parameters, **env}
        cfg.logger.debug("create_manifest_loading:env={}".format(env))
        template = "jobtemplate-loading.yml"
        if len(cfg.experiment.jobtemplate_loading) > 0:
            template = cfg.experiment.jobtemplate_loading
        if len(cfg.jobtemplate_loading) > 0:
            template = cfg.jobtemplate_loading
        return self.create_manifest_job(
            app=app, component=component, experiment=experiment,
            configuration=configuration, experiment_run=experiment_run,
            client=1, parallelism=parallelism, env=env, template=template,
            nodegroup='loading', num_pods=num_pods, connection=connection,
            patch_yaml=cfg.loading_patch, benchmark_run=benchmark_run,
            template_override=template_override)

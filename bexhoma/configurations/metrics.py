"""Prometheus metrics collection for bexhoma configurations."""
from __future__ import annotations

import copy
import os
import shutil
from typing import TYPE_CHECKING, Optional

from bexhoma import ceph_storage, expected_metrics, missing_metrics
from bexhoma.monitoring_math import JOB_QUERY_SETS

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['MetricsCollector', 'apply_metric_override', 'switch_off_unresolved', 'uses_storage_placeholders',
           'worker_host_values']


def apply_metric_override(metricname: str, metricdata: dict, overrides: dict) -> dict:
    """Copy one ``cluster.config`` metric definition, applying the experiment's ``active`` override.

    dbmsbenchmarker's fetcher and bexhoma's evaluation both skip a metric whose
    ``active`` is false, so this flag is all that decides whether it is collected.

    :param metricname: Metric key in ``monitor.metrics``.
    :param metricdata: The metric's definition from ``cluster.config``.
    :param overrides: Experiment's ``monitoring_metric_overrides`` (key -> active).
    :return: A copy of the definition, ``active`` replaced when overridden.
    :rtype: dict
    """
    metric = metricdata.copy()
    if metricname in overrides:
        metric['active'] = overrides[metricname]
    return metric


def switch_off_unresolved(metric: dict, values: dict) -> dict:
    """Switch a metric off when its query needs a storage placeholder that is empty.

    Applied after :func:`apply_metric_override`, so an experiment cannot
    switch on a metric its storage cannot serve (e.g. a Ceph volume metric on
    ``ramdisk``). The metric is then skipped, not fetched with an empty label
    and not reported as missing.

    :param metric: A metric definition, query still a template (modified in place).
    :param values: Storage placeholder values (``storage_class``, ``pool``, ``rbd_images``).
    :return: ``metric``.
    :rtype: dict
    """
    unresolved = ceph_storage.unresolved_placeholders(str(metric.get('query', '')), values)
    if unresolved:
        metric['active'] = False
        metric['inactive_reason'] = 'storage placeholder unresolved: ' + ', '.join(unresolved)
    return metric


def worker_host_values(workers: list, node: str, gpuid: str) -> tuple:
    """``{host}`` and ``{gpuid}`` for the metrics of one worker component.

    A worker component may run on several nodes (``-rnw``), so ``{host}`` is a
    regex alternation of those nodes, for ``instance=~"{host}"``, and
    ``{gpuid}`` joins the GPU UUIDs of all of them. A single node gives its
    plain name, as for the SUT.

    :param workers: Host infos of the component's pods (``c['worker'][component]``).
    :param node: Node of the SUT, used when no worker node is known.
    :param gpuid: GPU UUIDs of the SUT, used when no worker node is known.
    :return: ``(host, gpuid)``.
    :rtype: tuple[str, str]
    """
    nodes = list(dict.fromkeys(w['node'] for w in workers if w.get('node')))
    if not nodes:
        return node, gpuid
    gpuids = list(dict.fromkeys(g for w in workers for g in (w.get('GPUIDs') or [])))
    host = nodes[0] if len(nodes) == 1 else '(' + '|'.join(nodes) + ')'
    return host, '|'.join(gpuids)


def uses_storage_placeholders(monitor: dict) -> bool:
    """Whether any metric template in ``cluster.config``'s ``monitor`` section uses a storage placeholder.

    :param monitor: ``credentials.k8s.monitor``.
    :return: True when storage placeholders have to be resolved.
    :rtype: bool
    """
    templates = list((monitor.get('metrics') or {}).values())
    for section in monitor.values():
        if isinstance(section, dict) and isinstance(section.get('metrics'), dict):
            templates.extend(section['metrics'].values())
    return any(
        ceph_storage.query_placeholders(str(template.get('query', ''))) & set(ceph_storage.STORAGE_PLACEHOLDERS)
        for template in templates if isinstance(template, dict))


class MetricsCollector:
    """Builds connection configs and fetches Prometheus metrics for a configuration.

    :param config: The parent configuration this collector belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def get_connection_config(
        self,
        connection: str,
        alias: str = '',
        dialect: str = '',
        serverip: str = 'localhost',
        monitoring_host: str = 'localhost',
        job_pods: Optional[dict] = None,
    ) -> dict:
        """Build the dbmsbenchmarker connection config dict for this SUT.

        Collects host system information, worker information, resource limits,
        connection management settings, and monitoring metric queries.

        :param connection: Name of the dbmsbenchmarker connection.
        :param alias: Optional display alias for the connection.
        :param dialect: Optional SQL dialect string.
        :param serverip: Service IP/hostname used in JDBC URL formatting.
        :param monitoring_host: Prometheus monitoring service name.
        :param job_pods: Query set name (``metrics_benchmarker``,
            ``metrics_loading``) -> pod regex of the connection's jobs; each
            becomes a copy of ``metrics`` with ``{pods}`` set to it.
        :return: Connection config dict compatible with dbmsbenchmarker.
        :rtype: dict
        """
        cfg = self._config
        info = []
        cfg.connection = connection
        c = copy.deepcopy(cfg.dockertemplate['template'])
        if len(alias) > 0:
            c['alias'] = alias
        elif cfg.alias is not None:
            c['alias'] = cfg.alias
        else:
            c['alias'] = connection
        if len(dialect) > 0:
            c['dialect'] = dialect
        c['active'] = True
        c['name'] = connection
        c['configuration'] = cfg.configuration
        c['docker'] = cfg.docker
        c['script'] = cfg.script
        c['info'] = info
        c['time_loading'] = cfg.time_loading
        c['time_generated'] = cfg.time_generating
        c['time_ingested'] = cfg.time_ingesting
        c['time_schema'] = cfg.time_schema
        c['time_index'] = cfg.time_index
        c['script_times'] = cfg.times_scripts
        c['priceperhourdollar'] = 0.0 + cfg.dockertemplate['priceperhourdollar']
        # collect host information
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        cfg.pod_sut = pods[0]
        pod_sut = cfg.pod_sut
        c['hostsystem'] = cfg.host.get_host_all()
        c['storage'] = cfg.storage
        c['storage_reused'] = cfg.storage_reused
        c['loading_inherited'] = cfg.loading_inherited
        # loading switched off (-sl, or skip_loading of a YAML system): nothing was loaded or measured
        c['loading_deactivated'] = bool(getattr(cfg, 'loading_deactivated', False))
        # reused volume: its DDL and loading values against the requested ones
        c['volume_check'] = getattr(cfg, 'volume_check', {})
        # listed loading scripts that are not in the script folder (not run)
        c['loading_skipped'] = getattr(cfg, 'loading_skipped', [])
        # why this repetition's load counts as failed (empty: it did not fail)
        c['loading_failed'] = list(getattr(cfg, 'loading_failed', []))
        # UID of the SUT pod when loading started; hostsystem['pod_uid'] is the one of this round
        c['sut_pod_uid_loading'] = getattr(cfg, 'sut_pod_uid_at_loading_start', '') or ''
        # collect worker information
        c['worker'] = {}
        components = list(cfg.deployment_infos['statefulset'].keys())
        for component in components:
            c['worker'][component] = []
            pods_worker = cfg.get_worker_pods(component=component)
            for pod in pods_worker:
                cfg.pod_sut = pod
                print(f"{cfg.configuration:30s}: distributed system - get host info for worker {pod}")
                worker_infos = cfg.host.get_host_all(component=component, kind='statefulset')
                # StatefulSets bexhoma did not render (YugabyteDB's Helm chart) record no args
                worker_infos['args'] = cfg.deployment_infos['statefulset'][component].get('args', [])
                c['worker'][component].append(worker_infos)
        # additional Deployment-based components (e.g. pool), excluding sut itself
        components_deployment = [
            component for component in cfg.deployment_infos['deployment'].keys()
            if component != 'sut'
        ]
        for component in components_deployment:
            c['worker'][component] = []
            pods_worker = cfg.get_worker_pods(component=component)
            for pod in pods_worker:
                cfg.pod_sut = pod
                print(f"{cfg.configuration:30s}: distributed system - get host info for worker {pod}")
                worker_infos = cfg.host.get_host_all(component=component, kind='deployment')
                c['worker'][component].append(worker_infos)
        c['sut'] = []
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        if len(pods) > 1:
            for pod in pods:
                cfg.pod_sut = pod
                print(f"{cfg.configuration:30s}: distributed system - get host info for sut {pod}")
                sut_infos = cfg.host.get_host_all()
                sut_infos['args'] = cfg.sut_startup_args
                c['sut'].append(sut_infos)
        cfg.pod_sut = pod_sut
        # resource limits
        if 'requests' in cfg.resources:
            c['hostsystem']['requests_cpu'] = cfg.resources['requests']['cpu']
            c['hostsystem']['requests_memory'] = cfg.resources['requests']['memory']
        else:
            c['hostsystem']['requests_cpu'] = 0
            c['hostsystem']['requests_memory'] = 0
        if 'limits' in cfg.resources:
            c['hostsystem']['limits_cpu'] = cfg.resources['limits']['cpu']
            c['hostsystem']['limits_memory'] = cfg.resources['limits']['memory']
        else:
            c['hostsystem']['limits_cpu'] = 0
            c['hostsystem']['limits_memory'] = 0
        c['connectionmanagement'] = {}
        c['connectionmanagement']['numProcesses'] = cfg.connection_management['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = cfg.connection_management['runsPerConnection']
        c['connectionmanagement']['timeout'] = cfg.connection_management['timeout']
        c['connectionmanagement']['singleConnection'] = cfg.connection_management.get(
            'singleConnection', True)
        c['deployment_infos'] = cfg.deployment_infos
        c['monitoring'] = {}
        config_K8s = cfg.experiment.cluster.config['credentials']['k8s']
        if cfg.experiment.monitoring_active and 'monitor' in config_K8s:
            if len(c['hostsystem']['GPUIDs']) > 0:
                gpuid = '|'.join(c['hostsystem']['GPUIDs'])
            else:
                gpuid = ""
            node = c['hostsystem']['node']
            database = ""
            schema = ""
            if 'JDBC' in c:
                database = c['JDBC']['database'] if 'database' in c['JDBC'] else cfg.experiment.volume
                schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else 'default'
                if cfg.tenant_per == 'schema' and 'TENANT' in cfg.eval_parameters:
                    schema = 'tenant_' + cfg.eval_parameters['TENANT']
                elif cfg.tenant_per == 'database' and 'TENANT' in cfg.eval_parameters:
                    database = 'tenant_' + cfg.eval_parameters['TENANT']
            if 'grafanatoken' in config_K8s['monitor']:
                c['monitoring']['grafanatoken'] = config_K8s['monitor']['grafanatoken']
            if 'grafanaurl' in config_K8s['monitor']:
                c['monitoring']['grafanaurl'] = config_K8s['monitor']['grafanaurl']
            # window adjustments read by dbmsbenchmarker's fetchMetric; the grafana* names are legacy
            for key in ('shift', 'extend'):
                for name in (key, 'grafana' + key):
                    if name in config_K8s['monitor']:
                        c['monitoring'][key] = config_K8s['monitor'][name]
                        break
            if 'prometheus_url' in config_K8s['monitor']:
                c['monitoring']['prometheus_url'] = config_K8s['monitor']['prometheus_url']
            if 'service_monitoring' in config_K8s['monitor']:
                c['monitoring']['prometheus_url'] = config_K8s['monitor'][
                    'service_monitoring'].format(
                    service=monitoring_host,
                    namespace=cfg.experiment.cluster.contextdata['namespace'])
            if 'service_monitoring_application' in config_K8s['monitor']:
                c['monitoring']['prometheus_url_application'] = config_K8s['monitor'][
                    'service_monitoring_application'].format(
                    service=monitoring_host,
                    namespace=cfg.experiment.cluster.contextdata['namespace'])
            overrides = getattr(cfg.experiment, 'monitoring_metric_overrides', {})
            c['monitoring']['metrics'] = {}
            c['monitoring']['metrics_special'] = {}
            c['monitoring']['metrics_custom'] = {}
            # storage placeholders ({storage_class}, {pool}, {rbd_images}) are
            # only looked up when some query uses them; the SUT and its PVCs
            # exist by now
            if uses_storage_placeholders(config_K8s['monitor']):
                c['storage_monitoring'] = cfg.resolve_storage_monitoring()
            storage_values = cfg.storage_placeholder_values()
            if 'metrics' in config_K8s['monitor']:
                if 'deployment' in cfg.deployment_infos:
                    for name, deployment in cfg.deployment_infos['deployment'].items():
                        print(f"{connection:30s}: needs monitoring (common metrics) for deployment {name}")
                if 'statefulset' in cfg.deployment_infos:
                    for name, statefulset in cfg.deployment_infos['statefulset'].items():
                        print(f"{connection:30s}: needs monitoring (custom metrics) for stateful set {name}")
                        metrics_type = f"metrics_{name}"
                        c['monitoring'][metrics_type] = {}
                        host_worker, gpuid_worker = worker_host_values(
                            c['worker'].get(name, []), node, gpuid)
                        for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                            c['monitoring'][metrics_type][metricname] = switch_off_unresolved(
                                apply_metric_override(metricname, metricdata, overrides), storage_values)
                            c['monitoring'][metrics_type][metricname]['query'] = (
                                cfg.set_metric_of_config(
                                    metric=c['monitoring'][metrics_type][metricname]['query'],
                                    host=host_worker, gpuid=gpuid_worker, schema=schema,
                                    database=database, component=name))
                for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                    c['monitoring']['metrics'][metricname] = switch_off_unresolved(
                        apply_metric_override(metricname, metricdata, overrides), storage_values)
                    c['monitoring']['metrics'][metricname]['query'] = (
                        cfg.set_metric_of_config_default(
                            metric=c['monitoring']['metrics'][metricname]['query'],
                            host=node, gpuid=gpuid, schema=schema, database=database))
                # the connection's own jobs; a template without {pods} gives copies of metrics
                for metrics_type, pods_job in (job_pods or {}).items():
                    c['monitoring'][metrics_type] = {}
                    for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                        c['monitoring'][metrics_type][metricname] = switch_off_unresolved(
                            apply_metric_override(metricname, metricdata, overrides), storage_values)
                        c['monitoring'][metrics_type][metricname]['query'] = (
                            cfg.set_metric_of_config_default(
                                metric=c['monitoring'][metrics_type][metricname]['query'],
                                host=node, gpuid=gpuid, schema=schema, database=database,
                                pods=pods_job))
            if cfg.monitor_app_active and 'monitor' in cfg.dockertemplate:
                for component, application_monitoring in cfg.dockertemplate['monitor'].items():
                    print(f"{cfg.configuration:30s}: need application metrics for {component}")
                    application_metrics_name = application_monitoring['metrics']
                    print(f"{cfg.configuration:30s}: load application metrics of type {application_metrics_name}")
                    if application_metrics_name in config_K8s['monitor']:
                        metrics_template = config_K8s['monitor'][application_metrics_name][
                            'metrics'].copy()
                        for metricname, metricdata in metrics_template.items():
                            c['monitoring']['metrics'][metricname] = switch_off_unresolved(
                                metricdata.copy(), storage_values)
                            c['monitoring']['metrics'][metricname]['component'] = component
                            c['monitoring']['metrics'][metricname]['query'] = (
                                cfg.set_metric_of_config_default(
                                    metric=c['monitoring']['metrics'][metricname]['query'],
                                    host=node, gpuid=gpuid, schema=schema, database=database))
                        if 'statefulset' in cfg.deployment_infos:
                            for name, statefulset in cfg.deployment_infos['statefulset'].items():
                                metrics_type = f"metrics_{name}"
                                host_worker, gpuid_worker = worker_host_values(
                                    c['worker'].get(name, []), node, gpuid)
                                for metricname, metricdata in metrics_template.items():
                                    c['monitoring'][metrics_type][metricname] = switch_off_unresolved(
                                        metricdata.copy(), storage_values)
                                    c['monitoring'][metrics_type][metricname]['component'] = component
                                    c['monitoring'][metrics_type][metricname]['query'] = (
                                        cfg.set_metric_of_config(
                                            metric=c['monitoring'][metrics_type][metricname]['query'],
                                            host=host_worker, gpuid=gpuid_worker, schema=schema,
                                            database=database, component=name))
                    else:
                        print("{:30s}: application metrics of type {} not found!".format(
                            cfg.configuration,
                            cfg.dockertemplate['monitor']['metrics']))
        if 'JDBC' in c:
            database = c['JDBC']['database'] if 'database' in c['JDBC'] else cfg.experiment.volume
            schema = c['JDBC']['schema'] if 'schema' in c['JDBC'] else ''
            if cfg.tenant_per == 'schema':
                schema = 'DBMSBENCHMARKER_SCHEMA'
            elif cfg.tenant_per == 'database':
                database = 'DBMSBENCHMARKER_DATABASE'
            c['JDBC']['url'] = c['JDBC']['url'].format(
                serverip=serverip,
                dbname=cfg.experiment.volume,
                DBNAME=cfg.experiment.volume.upper(),
                timout_s=c['connectionmanagement']['timeout'],
                timeout_ms=c['connectionmanagement']['timeout'] * 1000,
                namespace=cfg.experiment.cluster.namespace,
                database=database,
                schema=schema,
            )
        return c

    def fetch(
        self,
        connection: str,
        connection_file: str,
        container: str,
        component: str,
        component_type: str,
        title: str,
        experiment: str,
        time_start: int,
        time_end: int,
        metrics_type: str,
        pod_dashboard: str,
        optional: bool = False,
        register: bool = True,
        upload: bool = True,
    ) -> str:
        """Fetch Prometheus metrics into the experiment result via the dashboard pod.

        :param connection: dbmsbenchmarker connection name.
        :param connection_file: Filename of the connection config (e.g. ``"PostgreSQL.config"``).
        :param container: Container name whose metrics to query (e.g. ``"dbms"``).
        :param component: Component label used in metric routing.
        :param component_type: Key under ``monitoring_components`` in the workload dict.
        :param title: Human-readable label stored in ``monitoring_components``.
        :param experiment: Experiment code.
        :param time_start: Unix timestamp of metric window start.
        :param time_end: Unix timestamp of metric window end.
        :param metrics_type: Key selecting the metric set in the connection config.
            ``metrics`` for a job component (loader, data generator,
            benchmarker) becomes its own query set (:data:`JOB_QUERY_SETS`)
            when the connection has one.
        :param pod_dashboard: Name of the dashboard pod to run metrics.py in.
        :param optional: When True, the component is added to ``optional_monitoring_components``.
        :param register: Register the component and its expected metrics first (see
            :meth:`register`, :meth:`expect`); a
            :class:`~bexhoma.metric_fetching.MetricFetchBatch` does that when queuing.
        :param upload: Upload ``connections.config`` afterwards, which ``metrics.py``
            may have overwritten in the pod; a batch uploads it once at its end.
        :return: Combined stdout and stderr of ``metrics.py``.
        """
        cfg = self._config
        if register:
            self.register(component_type, title, optional)
            self.expect(connection, component, component_type, metrics_type, time_start, time_end)
        config_folder = '/results/' + cfg.code
        monitoring = cfg.benchmark.dbms[connection].connectiondata['monitoring']
        if metrics_type == 'metrics' and JOB_QUERY_SETS.get(component_type) in monitoring:
            metrics_type = JOB_QUERY_SETS[component_type]
        metrics = monitoring[metrics_type]
        metric_example = metrics['total_cpu_memory'].copy()
        if container != 'dbms':
            metric_example['query'] = metric_example['query'].replace(
                'container_label_io_kubernetes_container_name="dbms"',
                f'container_label_io_kubernetes_container_name="{container}"')
            metric_example['query'] = metric_example['query'].replace(
                'container_label_io_kubernetes_container_name!="dbms"',
                f'container_label_io_kubernetes_container_name!="{container}"')
            metric_example['query'] = metric_example['query'].replace(
                'container="dbms"', f'container="{container}"')
            metric_example['query'] = metric_example['query'].replace(
                'container!="dbms"', f'container!="{container}"')
        print(f"{connection:30s}: example metric {metric_example}")
        cmd = (
            f'python metrics.py -r /results/ -db -mt {metrics_type} -ct {component_type}'
            f' -com {component} -cn {container} -c {connection} -cf {connection_file}'
            f' -f {config_folder} -e {experiment} -ts {time_start} -te {time_end}'
        )
        _, stdout, stderr = cfg.experiment.cluster.execute_command_in_pod(
            command=cmd, pod=pod_dashboard, container="dashboard")
        cfg.logger.debug(stdout)
        cfg.logger.debug(stderr)
        # keep the output: dbmsbenchmarker zero-fills a metric Prometheus did not
        # return and only logs it, so the report scans this file for that message
        output = ''.join(
            part.decode('utf-8', errors='replace') if isinstance(part, bytes) else (part or '')
            for part in (stdout, stderr))
        filename_log = cfg.path + '/' + missing_metrics.fetch_log_name(connection, component_type)
        with open(filename_log, 'a', encoding='utf-8') as f:
            f.write(f"### {cmd}\n{output}\n")
        for missing in missing_metrics.parse_missing_metrics(output):
            print(f"{connection:30s}: WARNING metric missing for {component_type}: {missing.title}")
        if upload:
            # re-upload connections.config because metrics.py may have overwritten it
            stdout = cfg.upload_experiment_file('connections.config')
            cfg.logger.debug(stdout)
        return output

    def register(self, component_type: str, title: str, optional: bool = False) -> None:
        """Record a monitored component in the workload, for the report.

        :param component_type: Key under ``monitoring_components``.
        :param title: Human-readable label.
        :param optional: When True, also list it in ``optional_monitoring_components``.
        """
        workload = self._config.experiment.workload
        workload.setdefault('monitoring_components', {})[component_type] = title
        if optional:
            optional_components = workload.setdefault('optional_monitoring_components', [])
            if component_type not in optional_components:
                optional_components.append(component_type)

    def _record_expected(self, rows: list) -> None:
        """Add rows to the result folder's expected-metrics list and keep its size in the workload."""
        if not rows:
            return
        cfg = self._config
        count = expected_metrics.record(cfg.path, rows)
        cfg.experiment.workload[expected_metrics.WORKLOAD_KEY] = count

    def expect(self, connection: str, component: str, component_type: str, metrics_type: str,
               time_start: int, time_end: int) -> None:
        """Write down the metric files a fetch is going to produce (see :mod:`bexhoma.expected_metrics`).

        Called when the fetch is queued (or, without a batch, when it starts), so a
        fetch that later fails or is lost still has its rows. Only the local result
        folder is written; the list reaches the dashboard pod with the final upload.

        :param connection: dbmsbenchmarker connection name.
        :param component: ``component`` of the fetch.
        :param component_type: Monitoring component type.
        :param metrics_type: ``metrics_type`` of the fetch.
        :param time_start: Start of the window.
        :param time_end: End of the window.
        """
        cfg = self._config
        try:
            connectiondata = cfg.benchmark.dbms[connection].connectiondata
        except (AttributeError, KeyError):
            return
        monitoring = connectiondata.get('monitoring') or {}
        set_name = expected_metrics.query_set(monitoring, metrics_type, component_type)
        names = expected_metrics.expected_metric_names(connectiondata, metrics_type, component, component_type)
        self._record_expected([
            dict(connection=connection, configuration=getattr(cfg, 'configuration', ''),
                 component_type=component_type,
                 metrics_type=set_name, metric=name, time_start=time_start, time_end=time_end, source='fetch')
            for name in names])

    def copy_fetched(self, source: str, target: str, component_types: list, pod_dashboard: str) -> None:
        """Reuse metrics already fetched for another connection of the same window.

        Loading metrics cover the loading window of a repetition, which is the
        same for every benchmarker connection of that repetition. Instead of
        querying Prometheus again, the CSVs of ``source`` are copied to the
        names of ``target`` (header line = connection name), in the pod, and the
        local ``metrics.py`` logs are copied too, so the missing-metrics report
        stays as before.

        :param source: Connection whose metrics were fetched.
        :param target: Connection that gets the same metrics.
        :param component_types: Component types fetched for ``source`` (e.g. ``loading``, ``loader``).
        :param pod_dashboard: Name of the dashboard pod.
        """
        cfg = self._config
        # the copies are expected like fetched files: the script copies only what exists
        self._record_expected([
            dict(row, connection=target, source='copy')
            for row in (expected_metrics.read(cfg.path) or [])
            if row['connection'] == source and row['component_type'] in component_types])
        script = cfg.experiment.ensure_copy_metrics_script()
        cmd = 'sh /results/{code}/{script} /results/{code} {source} {target} {types}'.format(
            code=cfg.code, script=script, source=source, target=target, types=' '.join(component_types))
        _, stdout, stderr = cfg.experiment.cluster.execute_command_in_pod(
            command=cmd, pod=pod_dashboard, container="dashboard")
        cfg.logger.debug(stdout)
        cfg.logger.debug(stderr)
        for component_type in component_types:
            log_source = os.path.join(cfg.path, missing_metrics.fetch_log_name(source, component_type))
            if os.path.isfile(log_source):
                shutil.copyfile(log_source, os.path.join(cfg.path, missing_metrics.fetch_log_name(target, component_type)))
        print("{:30s}: reused loading metrics of {} ({})".format(target, source, ', '.join(component_types)))

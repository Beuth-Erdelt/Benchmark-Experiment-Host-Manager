"""Prometheus metrics collection for bexhoma configurations."""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['MetricsCollector']


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
    ) -> dict:
        """Build the dbmsbenchmarker connection config dict for this SUT.

        Collects host system information, worker information, resource limits,
        connection management settings, and monitoring metric queries.

        :param connection: Name of the dbmsbenchmarker connection.
        :param alias: Optional display alias for the connection.
        :param dialect: Optional SQL dialect string.
        :param serverip: Service IP/hostname used in JDBC URL formatting.
        :param monitoring_host: Prometheus monitoring service name.
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
        c['timeLoad'] = cfg.timeLoading
        c['timeGenerate'] = cfg.timeGenerating
        c['timeIngesting'] = cfg.timeIngesting
        c['timeSchema'] = cfg.timeSchema
        c['timeIndex'] = cfg.timeIndex
        c['script_times'] = cfg.times_scripts
        c['priceperhourdollar'] = 0.0 + cfg.dockertemplate['priceperhourdollar']
        # collect host information
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        cfg.pod_sut = pods[0]
        pod_sut = cfg.pod_sut
        c['hostsystem'] = cfg.host.get_host_all()
        c['storage'] = cfg.storage
        # collect worker information
        c['worker'] = {}
        components = list(cfg.deployment_infos['statefulset'].keys())
        for component in components:
            c['worker'][component] = []
            pods_worker = cfg.get_worker_pods(component=component)
            for pod in pods_worker:
                cfg.pod_sut = pod
                print("{:30s}: distributed system - get host info for worker {}".format(
                    cfg.configuration, pod))
                worker_infos = cfg.host.get_host_all()
                worker_infos['args'] = cfg.deployment_infos['statefulset'][component]['args']
                c['worker'][component].append(worker_infos)
        c['sut'] = []
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        if len(pods) > 1:
            for pod in pods:
                cfg.pod_sut = pod
                print("{:30s}: distributed system - get host info for sut {}".format(
                    cfg.configuration, pod))
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
        c['connectionmanagement']['numProcesses'] = cfg.connectionmanagement['numProcesses']
        c['connectionmanagement']['runsPerConnection'] = cfg.connectionmanagement['runsPerConnection']
        c['connectionmanagement']['timeout'] = cfg.connectionmanagement['timeout']
        c['connectionmanagement']['singleConnection'] = cfg.connectionmanagement.get(
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
            if 'grafanashift' in config_K8s['monitor']:
                c['monitoring']['shift'] = config_K8s['monitor']['grafanashift']
            if 'grafanaextend' in config_K8s['monitor']:
                c['monitoring']['extend'] = config_K8s['monitor']['grafanaextend']
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
            c['monitoring']['metrics'] = {}
            c['monitoring']['metrics_special'] = {}
            c['monitoring']['metrics_custom'] = {}
            if 'metrics' in config_K8s['monitor']:
                if 'deployment' in cfg.deployment_infos:
                    for name, deployment in cfg.deployment_infos['deployment'].items():
                        print("{:30s}: needs monitoring (common metrics) for deployment {}".format(
                            connection, name))
                if 'statefulset' in cfg.deployment_infos:
                    for name, statefulset in cfg.deployment_infos['statefulset'].items():
                        print("{:30s}: needs monitoring (custom metrics) for stateful set {}".format(
                            connection, name))
                        metrics_type = f"metrics_{name}"
                        c['monitoring'][metrics_type] = {}
                        for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                            c['monitoring'][metrics_type][metricname] = metricdata.copy()
                            c['monitoring'][metrics_type][metricname]['query'] = (
                                cfg.set_metric_of_config(
                                    metric=c['monitoring'][metrics_type][metricname]['query'],
                                    host=node, gpuid=gpuid, schema=schema,
                                    database=database, component=name))
                for metricname, metricdata in config_K8s['monitor']['metrics'].items():
                    c['monitoring']['metrics'][metricname] = metricdata.copy()
                    c['monitoring']['metrics'][metricname]['query'] = (
                        cfg.set_metric_of_config_default(
                            metric=c['monitoring']['metrics'][metricname]['query'],
                            host=node, gpuid=gpuid, schema=schema, database=database))
            if cfg.monitor_app_active and 'monitor' in cfg.dockertemplate:
                for component, application_monitoring in cfg.dockertemplate['monitor'].items():
                    print("{:30s}: need application metrics for {}".format(
                        cfg.configuration, component))
                    application_metrics_name = application_monitoring['metrics']
                    print("{:30s}: load application metrics of type {}".format(
                        cfg.configuration, application_metrics_name))
                    if application_metrics_name in config_K8s['monitor']:
                        metrics_template = config_K8s['monitor'][application_metrics_name][
                            'metrics'].copy()
                        for metricname, metricdata in metrics_template.items():
                            c['monitoring']['metrics'][metricname] = metricdata.copy()
                            c['monitoring']['metrics'][metricname]['component'] = component
                            c['monitoring']['metrics'][metricname]['query'] = (
                                cfg.set_metric_of_config_default(
                                    metric=c['monitoring']['metrics'][metricname]['query'],
                                    host=node, gpuid=gpuid, schema=schema, database=database))
                        if 'statefulset' in cfg.deployment_infos:
                            for name, statefulset in cfg.deployment_infos['statefulset'].items():
                                metrics_type = f"metrics_{name}"
                                for metricname, metricdata in metrics_template.items():
                                    c['monitoring'][metrics_type][metricname] = metricdata.copy()
                                    c['monitoring'][metrics_type][metricname]['component'] = component
                                    c['monitoring'][metrics_type][metricname]['query'] = (
                                        cfg.set_metric_of_config(
                                            metric=c['monitoring'][metrics_type][metricname]['query'],
                                            host=node, gpuid=gpuid, schema=schema,
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
    ) -> None:
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
        :param pod_dashboard: Name of the dashboard pod to run metrics.py in.
        :param optional: When True, the component is added to ``optional_monitoring_components``.
        """
        cfg = self._config
        if 'monitoring_components' not in cfg.experiment.workload:
            cfg.experiment.workload['monitoring_components'] = {}
        cfg.experiment.workload['monitoring_components'][component_type] = title
        if optional:
            if 'optional_monitoring_components' not in cfg.experiment.workload:
                cfg.experiment.workload['optional_monitoring_components'] = []
            if component_type not in cfg.experiment.workload['optional_monitoring_components']:
                cfg.experiment.workload['optional_monitoring_components'].append(component_type)
        config_folder = '/results/' + cfg.code
        metrics = cfg.benchmark.dbms[connection].connectiondata['monitoring'][metrics_type]
        metric_example = metrics['total_cpu_memory'].copy()
        if container != 'dbms':
            metric_example['query'] = metric_example['query'].replace(
                'container_label_io_kubernetes_container_name="dbms"',
                'container_label_io_kubernetes_container_name="{}"'.format(container))
            metric_example['query'] = metric_example['query'].replace(
                'container_label_io_kubernetes_container_name!="dbms"',
                'container_label_io_kubernetes_container_name!="{}"'.format(container))
            metric_example['query'] = metric_example['query'].replace(
                'container="dbms"', 'container="{}"'.format(container))
            metric_example['query'] = metric_example['query'].replace(
                'container!="dbms"', 'container!="{}"'.format(container))
        print("{:30s}: example metric {}".format(connection, metric_example))
        cmd = (
            f'python metrics.py -r /results/ -db -mt {metrics_type} -ct {component_type}'
            f' -com {component} -cn {container} -c {connection} -cf {connection_file}'
            f' -f {config_folder} -e {experiment} -ts {time_start} -te {time_end}'
        )
        _, stdout, stderr = cfg.experiment.cluster.execute_command_in_pod(
            command=cmd, pod=pod_dashboard, container="dashboard")
        cfg.logger.debug(stdout)
        cfg.logger.debug(stderr)
        # re-upload connections.config because metrics.py may have overwritten it
        filename = 'connections.config'
        stdout = cfg.experimentupload_file(filename)
        cfg.logger.debug(stdout)

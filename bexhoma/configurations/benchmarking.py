"""Benchmarker pod lifecycle for bexhoma configurations."""
from __future__ import annotations

import os
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from dbmsbenchmarker import benchmarker, tools

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['BenchmarkRunner']


class BenchmarkRunner:
    """Creates and monitors benchmarker Kubernetes jobs for a configuration.

    :param config: The parent configuration this runner belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def run_pod(
        self,
        connection: Optional[str] = None,
        alias: str = '',
        dialect: str = '',
        query: Optional[str] = None,
        app: str = '',
        component: str = 'benchmarker',
        experiment: str = '',
        configuration: str = '',
        client: str = '1',
        parallelism: int = 1,
        only_prepare: bool = False,
        benchmark_run: str = '',
        template_override: str = '',
    ) -> None:
        """Start a benchmarker job pod, upload configs, and optionally wait for it.

        Sets metadata in the connection config, copies ``query.config`` and
        ``connection.config`` to the first pod of the job (result folder is
        mounted into every pod), then optionally submits the job.

        :param connection: dbmsbenchmarker connection name; defaults to
            ``self._config.configuration``.
        :param alias: Display alias to anonymise the DBMS name.
        :param dialect: SQL dialect override string.
        :param query: Fix the benchmark to a single query; None means all.
        :param app: App label override; defaults to ``self._config.appname``.
        :param component: Component label (default ``'benchmarker'``).
        :param experiment: Experiment code (defaults to ``self._config.code``).
        :param configuration: DBMS configuration name; defaults to ``connection``.
        :param client: Sequential client-round index string.
        :param parallelism: Number of parallel benchmarker pods.
        :param only_prepare: When True, upload configs but do not submit the job.
        :param benchmark_run: 1-based parallel benchmark index within one client round.
        :param template_override: When non-empty, overrides the default YAML job template.
        """
        cfg = self._config
        cfg.logger.debug('BenchmarkRunner.run_pod()')
        resultfolder = cfg.experiment.cluster.config['benchmarker']['resultfolder']
        experiments_configfolder = cfg.experiment.cluster.experiments_configfolder
        app = cfg.appname
        if connection is None:
            connection = cfg.configuration
        if len(configuration) == 0:
            configuration = connection
        code = cfg.code
        if not isinstance(client, str):
            client = str(client)
        if not cfg.client:
            cfg.client = client
        if len(dialect) == 0 and len(cfg.dialect) > 0:
            dialect = cfg.dialect
        experimentRun = str(cfg.num_experiment_to_apply_done + 1)
        tools.query.template = cfg.experiment.query_management
        cfg.current_benchmark_connection = connection
        cfg.logger.debug(
            'BenchmarkRunner.run_pod(current_benchmark_connection = {})'.format(
                cfg.current_benchmark_connection))
        now = datetime.utcnow()
        time_now = str(datetime.now())
        time_now_int = int(datetime.timestamp(
            datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')))
        cfg.current_benchmark_start = int(time_now_int)
        monitoring_host = cfg.generate_component_name(
            component='monitoring', configuration=configuration, experiment=cfg.code)
        service_name = cfg.get_service_sut(configuration=configuration)
        service_namespace = cfg.experiment.cluster.contextdata['namespace']
        service_host = cfg.experiment.cluster.contextdata['service_sut'].format(
            service=service_name, namespace=service_namespace)
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=configuration, experiment=cfg.code)
        cfg.pod_sut = pods[0]
        c = cfg.metrics.get_connection_config(
            connection, alias, dialect,
            serverip=service_host, monitoring_host=monitoring_host)
        if len(cfg.loading_parameters) > 0:
            cfg.connection_parameter['loading_parameters'] = cfg.loading_parameters.copy()
        if len(cfg.benchmarking_parameters) > 0:
            cfg.connection_parameter['benchmarking_parameters'] = cfg.benchmarking_parameters.copy()
        if len(cfg.sut_parameters) > 0:
            cfg.connection_parameter['sut_parameters'] = cfg.sut_parameters.copy()
        if len(cfg.eval_parameters) > 0:
            cfg.connection_parameter['eval_parameters'] = cfg.eval_parameters.copy()
        if len(cfg.ddl_parameters) > 0:
            cfg.connection_parameter['ddl_parameters'] = cfg.ddl_parameters.copy()
        c['parameter'] = cfg.eval_parameters.copy()
        c['parameter']['parallelism'] = parallelism
        c['parameter']['client'] = client
        c['parameter']['numExperiment'] = experimentRun
        c['parameter']['numBenchmark'] = benchmark_run
        c['parameter']['num_worker'] = cfg.num_worker
        c['parameter']['dockerimage'] = cfg.dockerimage
        c['parameter']['connection_parameter'] = cfg.connection_parameter
        c['hostsystem']['loading_timespans'] = cfg.loading_timespans
        c['hostsystem']['benchmarking_timespans'] = cfg.benchmarking_timespans
        cfg.host.check_volumes()
        if 'JDBC' in c:
            if isinstance(c['JDBC']['jar'], list):
                for idx, jar_entry in enumerate(c['JDBC']['jar']):
                    c['JDBC']['jar'][idx] = (
                        cfg.experiment.cluster.config['benchmarker']['jarfolder'] + jar_entry)
            elif isinstance(c['JDBC']['jar'], str):
                c['JDBC']['jar'] = (
                    cfg.experiment.cluster.config['benchmarker']['jarfolder'] + c['JDBC']['jar'])
        cfg.logger.debug('BenchmarkRunner.run_pod(): {}'.format(connection))
        cfg.benchmark = benchmarker.benchmarker(
            fixedConnection=connection,
            fixedQuery=query,
            result_path=resultfolder,
            batch=True,
            working='connection',
            code=code,
        )
        cfg.code = cfg.benchmark.code
        print("{:30s}: benchmarking results in folder {}".format(
            configuration, cfg.benchmark.path))
        cfg.logger.debug('BenchmarkRunner.run_pod(Code={})'.format(cfg.code))
        connectionfile = cfg.benchmark.path + '/connections.config'
        if not os.path.isfile(connectionfile):
            connectionfile = experiments_configfolder + '/connections.config'
        if cfg.experiment.queryfile is not None:
            queryfile = experiments_configfolder + '/' + cfg.experiment.queryfile
        else:
            queryfile = experiments_configfolder + '/queries.config'
        cfg.benchmark.getConfig(connectionfile=connectionfile, queryfile=queryfile)
        if c['name'] in cfg.benchmark.dbms:
            print("Rerun connection " + connection)
        else:
            cfg.benchmark.connections.append(c)
        cfg.benchmark.dbms[c['name']] = tools.dbms(c, False)
        filename = cfg.benchmark.path + '/connections.config'
        with open(filename, 'w') as output_file:
            output_file.write(str(cfg.benchmark.connections))
        filename = cfg.benchmark.path + '/' + c['name'] + '.config'
        with open(filename, 'w') as output_file:
            output_file.write(str([c]))
        if len(cfg.experiment.workload) > 0:
            for workload_key, workload_val in cfg.experiment.workload.items():
                cfg.benchmark.queryconfig[workload_key] = workload_val
            filename = cfg.benchmark.path + '/queries.config'
            with open(filename, 'w') as output_file:
                output_file.write(str(cfg.benchmark.queryconfig))
        cfg.benchmark.reporterStore.readProtocol()
        cfg.benchmark.generateAllParameters()
        cfg.benchmark.reporterStore.writeProtocol()
        experiment_log = {
            'delay': 0,
            'step': "runBenchmarks",
            'connection': connection,
            'connectionmanagement': cfg.connection_management.copy(),
        }
        cfg.experiment.cluster.log_experiment(experiment_log)
        pods = cfg.experiment.cluster.get_pods(component='dashboard')
        if len(pods) > 0:
            pod_dashboard = pods[0]
            cmd_prepare_log = 'mkdir -p /results/' + str(cfg.code)
            cfg.experiment.cluster.execute_command_in_pod(
                command=cmd_prepare_log, pod=pod_dashboard, container="dashboard")
            cfg.upload_experiment_file('queries.config')
            cfg.upload_experiment_file(c['name'] + '.config')
            cfg.upload_experiment_file(c['name'] + '.config')
            cfg.upload_experiment_file('connections.config')
            cfg.upload_experiment_file('protocol.json')
        redisQueue = '{}-{}-{}-{}'.format(app, component, connection, cfg.code)
        for i in range(1, parallelism + 1):
            cfg.experiment.cluster.add_to_messagequeue(queue=redisQueue, data=i)
        round_index = int(client) - 1
        benchmark_run_index = (int(benchmark_run) - 1) if benchmark_run else 0
        benchmarker_rounds = cfg.experiment_dict.get('benchmarker', [])
        if round_index < len(benchmarker_rounds):
            round_entries = benchmarker_rounds[round_index]
            if benchmark_run_index < len(round_entries):
                bm_entry = round_entries[benchmark_run_index]
                cfg._push_pod_configs(
                    queue_key=redisQueue,
                    num_pods=parallelism,
                    parameters=bm_entry.get('parameters', {}),
                    pod_parameters=bm_entry.get('pod_parameters', []),
                )
        job_counter_key = '{}-{}-podcount-job-{}-{}'.format(
            app, component, connection, cfg.code)
        cfg.experiment.cluster.set_pod_counter(queue=job_counter_key, value=parallelism)
        if not only_prepare:
            yamlfile = cfg.manifest.create_manifest_benchmarking(
                connection=connection, component=component,
                configuration=configuration, experiment=cfg.code,
                experimentRun=experimentRun, client=client, parallelism=parallelism,
                alias=c['alias'], num_pods=parallelism, benchmark_run=benchmark_run,
                template_override=template_override)
            cfg.experiment.cluster.create_object_from_file(yamlfile)
            job_pods = []
            while len(job_pods) == 0:
                cfg.wait(10)
                job_pods = cfg.experiment.cluster.get_job_pods(
                    component=component, configuration=configuration,
                    experiment=cfg.code, client=client)
            client_pod_name = job_pods[0]
            status = cfg.experiment.cluster.get_pod_status(client_pod_name)
            cfg.logger.debug('Pod={} has status={}'.format(client_pod_name, status))
            print("{:30s}: benchmarking is waiting for job {}: ".format(
                configuration, client_pod_name), end="", flush=True)
            while status != "Running" and status != "Succeeded":
                cfg.logger.debug('Pod={} has status={}'.format(client_pod_name, status))
                print(".", end="", flush=True)
                job_pods = []
                while len(job_pods) == 0:
                    cfg.wait(10, silent=True)
                    job_pods = cfg.experiment.cluster.get_job_pods(
                        component=component, configuration=configuration,
                        experiment=cfg.code, client=client)
                client_pod_name = job_pods[0]
                status = cfg.experiment.cluster.get_pod_status(client_pod_name)
            print("found")
        pods = cfg.experiment.cluster.get_pods(component='dashboard')
        if len(pods) > 0:
            pod_dashboard = pods[0]
            if cfg.monitoring_active and cfg.monitor_loading:
                if 'deployment' in cfg.deployment_infos:
                    for name, deployment in cfg.deployment_infos['deployment'].items():
                        print("{:30s}: needs monitoring (common metrics) for deployment {}".format(
                            connection, name))
                        if name == 'sut' and cfg.monitoring_sut:
                            print("{:30s}: collecting loading metrics of SUT at connection {}".format(
                                connection, cfg.current_benchmark_connection))
                            cfg.metrics.fetch(
                                title="Loading phase: SUT deployment",
                                connection=cfg.current_benchmark_connection,
                                connection_file=c['name'] + '.config',
                                container="dbms",
                                component=name,
                                component_type="loading",
                                experiment=cfg.code,
                                time_start=cfg.time_loading_start,
                                time_end=cfg.time_loading_end,
                                metrics_type="metrics",
                                pod_dashboard=pod_dashboard,
                            )
                        elif name != 'sut':
                            print("{:30s}: collecting loading metrics of {} at connection {}".format(
                                connection, name, cfg.current_benchmark_connection))
                            cfg.metrics.fetch(
                                title=f"Loading phase: component {name}",
                                connection=cfg.current_benchmark_connection,
                                connection_file=c['name'] + '.config',
                                container=deployment['containers'][0],
                                component=name,
                                component_type=f"{name}loading",
                                experiment=cfg.code,
                                time_start=cfg.time_loading_start,
                                time_end=cfg.time_loading_end,
                                metrics_type="metrics",
                                pod_dashboard=pod_dashboard,
                            )
                if 'statefulset' in cfg.deployment_infos:
                    for name, statefulset in cfg.deployment_infos['statefulset'].items():
                        print("{:30s}: needs monitoring (custom metrics) for stateful set {}".format(
                            connection, name))
                        cfg.metrics.fetch(
                            title=f"Loading phase: component {name}",
                            connection=cfg.current_benchmark_connection,
                            connection_file=c['name'] + '.config',
                            container="dbms",
                            component=name,
                            component_type=f"{name}loading",
                            experiment=cfg.code,
                            time_start=cfg.time_loading_start,
                            time_end=cfg.time_loading_end,
                            metrics_type=f"metrics_{name}",
                            pod_dashboard=pod_dashboard,
                        )
                endpoints_cluster = cfg.experiment.cluster.get_service_endpoints(
                    service_name="bexhoma-service-monitoring-default")
                if len(endpoints_cluster) > 0 or cfg.experiment.cluster.monitor_cluster_exists:
                    if "datagenerator" in cfg.experiment.components["loader"]:
                        print("{:30s}: collecting metrics of data generator at connection {}".format(
                            connection, cfg.current_benchmark_connection))
                        cfg.metrics.fetch(
                            title="Loading phase: component data generator",
                            connection=cfg.current_benchmark_connection,
                            connection_file=c['name'] + '.config',
                            container="datagenerator",
                            component="datagenerator",
                            component_type="datagenerator",
                            experiment=cfg.code,
                            time_start=cfg.time_loading_start,
                            time_end=cfg.time_loading_end,
                            metrics_type="metrics",
                            pod_dashboard=pod_dashboard,
                            optional=True,
                        )
                    print("{:30s}: collecting metrics of data injector at connection {}".format(
                        connection, cfg.current_benchmark_connection))
                    cfg.metrics.fetch(
                        title="Loading phase: component loader",
                        connection=cfg.current_benchmark_connection,
                        connection_file=c['name'] + '.config',
                        container="sensor",
                        component="loader",
                        component_type="loader",
                        experiment=cfg.code,
                        time_start=cfg.time_loading_start,
                        time_end=cfg.time_loading_end,
                        metrics_type="metrics",
                        pod_dashboard=pod_dashboard,
                    )

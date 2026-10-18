"""Benchmarker pod lifecycle for bexhoma configurations."""
from __future__ import annotations

import os
import time
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from dbmsbenchmarker import benchmarker, tools

from bexhoma.cluster_calls import CALL_STATS

if TYPE_CHECKING:
    from bexhoma.metric_fetching import MetricFetchBatch
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
        reset_seconds: float = 0.0,
        fetch_batch: Optional[MetricFetchBatch] = None,
    ) -> None:
        """Start a benchmarker job pod and upload configs; the job is not waited for.

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
        :param reset_seconds: Seconds spent running this connection's reset script
            (0 if none ran), recorded on the connection as ``time_reset``.
        :param fetch_batch: Queue the loading-metric fetches here instead of
            fetching right away, so the fetches of all configurations of one loop
            pass run in parallel.
        :raises RuntimeError: If the chunk-assignment queue cannot be filled
            with exactly ``parallelism`` items, which would otherwise let pods
            race on a corrupted assignment.
        """
        cfg = self._config
        started = time.monotonic()
        calls_started = CALL_STATS.snapshot()
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
        experiment_run = str(cfg.num_experiment_to_apply_done + 1)
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
        # {pods} of the job query sets: this connection's benchmarker job (named as
        # in create_manifest_job()) and every loading job of this repetition
        jobname_benchmarker = cfg.generate_component_name(
            app=app, component=component, experiment=cfg.code, configuration=configuration,
            experiment_run=experiment_run, client=client, benchmark_run=benchmark_run)
        jobname_loading = cfg.generate_component_name(
            component='loading', experiment_run=experiment_run)
        job_pods = {
            'metrics_benchmarker': cfg.job_pods_pattern(jobname_benchmarker),
            'metrics_loading': cfg.job_pods_pattern(jobname_loading, all_jobs_with_prefix=True),
        }
        c = cfg.metrics.get_connection_config(
            connection, alias, dialect,
            serverip=service_host, monitoring_host=monitoring_host, job_pods=job_pods)
        c['time_reset'] = reset_seconds
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
        c['parameter']['numExperiment'] = experiment_run
        c['parameter']['numBenchmark'] = benchmark_run
        c['parameter']['num_worker'] = cfg.num_worker
        c['parameter']['dockerimage'] = cfg.dockerimage
        c['parameter']['connection_parameter'] = cfg.connection_parameter
        c['hostsystem']['loading_timespans'] = cfg.loading_timespans
        c['hostsystem']['benchmarking_timespans'] = cfg.benchmarking_timespans
        # the SUT pod's volume was just measured for the host info, at the same path
        cfg.host.check_volumes(measured={cfg.pod_sut: (
            c['hostsystem'].get('volume_size'), c['hostsystem'].get('volume_used'))})
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
        active_queries = getattr(cfg.experiment, 'active_queries', None)
        if active_queries is not None:
            for query_number, query_entry in enumerate(cfg.benchmark.queryconfig['queries'], start=1):
                query_entry['active'] = query_number in active_queries
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
            # atomic write: benchmarker pods read this shared file concurrently via
            # shutil.copyfile() while other configs' run_pod() calls may rewrite it;
            # a plain open(filename, 'w') truncates before writing, so a pod can
            # observe a 0-byte file mid-write. os.replace() is a single directory-entry
            # swap, so a concurrent reader always sees either the old or the new
            # complete file, never a truncated one.
            tmp_filename = filename + '.tmp'
            with open(tmp_filename, 'w') as output_file:
                output_file.write(str(cfg.benchmark.queryconfig))
            os.replace(tmp_filename, filename)
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
            # one copy and one exec for all four; the upload creates /results/{code}
            cfg.experiment.upload_experiment_files(
                ['queries.config', c['name'] + '.config', 'connections.config', 'protocol.json'])
        redisQueue = '{}-{}-{}-{}'.format(app, component, connection, cfg.code)
        cfg.experiment.cluster.fill_messagequeue(queue=redisQueue, length=parallelism)
        round_index = int(client) - 1
        benchmark_run_index = (int(benchmark_run) - 1) if benchmark_run else 0
        benchmarker_rounds = cfg.experiment_dict.get('benchmarker', [])
        bm_entry = {}
        # per-pod configs and the job counter in one MSET
        redis_values = {}
        if round_index < len(benchmarker_rounds):
            round_entries = benchmarker_rounds[round_index]
            if benchmark_run_index < len(round_entries):
                bm_entry = round_entries[benchmark_run_index]
                redis_values.update(cfg._pod_configs(
                    queue_key=redisQueue,
                    num_pods=parallelism,
                    parameters=bm_entry.get('parameters', {}),
                    pod_parameters=bm_entry.get('pod_parameters', []),
                ))
        job_counter_key = '{}-{}-podcount-job-{}-{}'.format(
            app, component, connection, cfg.code)
        redis_values[job_counter_key] = parallelism
        cfg.experiment.cluster.set_redis_values(redis_values)
        if not only_prepare:
            yamlfile = cfg.manifest.create_manifest_benchmarking(
                connection=connection, component=component,
                configuration=configuration, experiment=cfg.code,
                experiment_run=experiment_run, client=client, parallelism=parallelism,
                alias=c['alias'], num_pods=parallelism, benchmark_run=benchmark_run,
                env=bm_entry.get('parameters', {}), template_override=template_override)
            cfg.experiment.cluster.create_object_from_file(yamlfile)
            # No waiting for the pod here: the experiment loop watches the job, and a
            # round whose pods do not start is skipped after BENCHMARK_START_TIMEOUT_MINUTES.
            # Waiting per job made N tenants start one after another.
            print("{:30s}: submitted benchmarker job in {:.1f}s ({})".format(
                configuration, time.monotonic() - started, CALL_STATS.since(calls_started)))
        pods = cfg.experiment.cluster.get_pods(component='dashboard')
        if len(pods) > 0 and cfg.monitoring_active and cfg.monitor_loading:
            self._loading_metrics(connection, c['name'] + '.config', pods[0], fetch_batch)

    def _loading_metrics(self, connection: str, connection_file: str, pod_dashboard: str,
                         fetch_batch: Optional[MetricFetchBatch]) -> None:
        """Fetch the loading-phase metrics for a connection, once per repetition.

        The loading window is the same for every benchmarker connection of a
        repetition, so only the first one queries Prometheus; later ones get a
        copy (see :meth:`MetricsCollector.copy_fetched`).

        :param connection: Benchmarker connection that needs the loading metrics.
        :param connection_file: Its connection config file.
        :param pod_dashboard: Name of the dashboard pod.
        :param fetch_batch: Batch to queue into; None fetches right away.
        """
        cfg = self._config
        experiment_run = cfg.num_experiment_to_apply_done + 1
        fetched = cfg.loading_metrics_fetched.get(experiment_run)
        if fetched is not None and fetched[0] != connection:
            source, component_types = fetched

            def copy() -> None:
                cfg.metrics.copy_fetched(source, connection, component_types, pod_dashboard)
            if fetch_batch is None:
                copy()
            else:
                fetch_batch.add_after(copy)
            return
        window = dict(connection=connection, connection_file=connection_file, experiment=cfg.code,
                      time_start=cfg.time_loading_start, time_end=cfg.time_loading_end,
                      pod_dashboard=pod_dashboard)
        fetches = []
        if 'deployment' in cfg.deployment_infos:
            for name, deployment in cfg.deployment_infos['deployment'].items():
                print("{:30s}: needs monitoring (common metrics) for deployment {}".format(connection, name))
                if name == 'sut' and cfg.monitoring_sut:
                    print("{:30s}: collecting loading metrics of SUT at connection {}".format(connection, connection))
                    fetches.append(dict(title="Loading phase: SUT deployment", container="dbms", component=name,
                                        component_type="loading", metrics_type="metrics"))
                elif name != 'sut':
                    print("{:30s}: collecting loading metrics of {} at connection {}".format(connection, name, connection))
                    fetches.append(dict(title=f"Loading phase: component {name}", container=deployment['containers'][0],
                                        component=name, component_type=f"{name}loading", metrics_type="metrics"))
        if 'statefulset' in cfg.deployment_infos:
            for name in cfg.deployment_infos['statefulset']:
                print("{:30s}: needs monitoring (custom metrics) for stateful set {}".format(connection, name))
                fetches.append(dict(title=f"Loading phase: component {name}", container="dbms", component=name,
                                    component_type=f"{name}loading", metrics_type=f"metrics_{name}"))
        endpoints_cluster = cfg.experiment.cluster.get_service_endpoints(
            service_name="bexhoma-service-monitoring-default")
        if len(endpoints_cluster) > 0 or cfg.experiment.cluster.monitor_cluster_exists:
            if "datagenerator" in cfg.experiment.components["loader"]:
                print("{:30s}: collecting metrics of data generator at connection {}".format(connection, connection))
                fetches.append(dict(title="Loading phase: component data generator", container="datagenerator",
                                    component="datagenerator", component_type="datagenerator",
                                    metrics_type="metrics", optional=True))
            print("{:30s}: collecting metrics of data injector at connection {}".format(connection, connection))
            fetches.append(dict(title="Loading phase: component loader", container="sensor", component="loader",
                                component_type="loader", metrics_type="metrics"))
        if not fetches:
            return
        cfg.loading_metrics_fetched[experiment_run] = (connection, [f['component_type'] for f in fetches])
        for fetch in fetches:
            if fetch_batch is None:
                cfg.metrics.fetch(**window, **fetch)
            else:
                fetch_batch.add_fetch(cfg, **window, **fetch)

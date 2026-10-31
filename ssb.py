"""
CLI entry point for Star Schema Benchmark (SSB) experiments in a Kubernetes cluster.

Generates SSB data on a distributed filesystem (Ceph), loads it into one or more
DBMS with parallel, synchronised loaders, and runs the 13 SSB queries.
Supports the star schema and the denormalized flat table (-xsv), the
constants of the specification and random parameters (-xqv), monitoring,
optional index, constraint and statistics creation, and fixed node assignment.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import *
from bexhoma.cli_args import make_base_parser, resolve_scaling_factor
from bexhoma.benchmarks.ssb import SCHEMA_VARIANTS, QUERY_VARIANTS, DIMENSION_VARIANTS, resolve_dimension_folder
from dbmsbenchmarker import *
import logging
import urllib3
import argparse


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Run the Star Schema Benchmark (SSB) queries against a DBMS in Kubernetes.
    Data is generated on a shared distributed filesystem and loaded in parallel.
    Star schema or flat table, queries with the constants of the specification or random parameters.
    Supports optional index, constraint, and statistics creation; multi-stream query ordering.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase: profile import, run queries, start SUT only, load data, empty tables, or summarize results', choices=['profiling', 'run', 'start', 'load', 'empty', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='one or more DBMS engines to test (default: PostgreSQL, MonetDB, ClickHouse)', choices=['PostgreSQL', 'MonetDB', 'ClickHouse', 'CedarDB', 'ClickHouseCluster', 'PgDuckDB', 'Citus', 'MySQL', 'MariaDB'], default=[], nargs='*')
    parser.add_argument('-xsv',   '--xschema-variant', help='normal: star schema (4 dimensions + lineorder); flat: one denormalized table lineorder_flat, generated as flat files', choices=SCHEMA_VARIANTS, default='normal', dest='schema_variant')
    parser.add_argument('-xdim',  '--xdimensions', help='star schema on a multi-node DBMS (ClickHouseCluster, Citus): replicated = a full copy of each dimension on every node (Citus: reference tables), joins run locally per shard; distributed = dimensions spread over the nodes like lineorder, joined across nodes per query (ignored by single-node DBMS and with -xsv flat)', choices=DIMENSION_VARIANTS, default='replicated', dest='dimensions')
    parser.add_argument('-xqv',   '--xquery-variant', help='spec: the 13 queries with the constants of the SSB specification; random: random parameters that keep the filter factor of each query', choices=QUERY_VARIANTS, default='spec', dest='query_variant')
    parser.add_argument('-xlit',  '--xlimit-import-table', help='import only this table (customer, supplier, part, dates, lineorder or lineorder_flat)', default='', dest='limit_import_table')
    parser.add_argument('-xdt',   '--xdata-transfer', help='also measure data transfer volume per query', action='store_true', default=False, dest='datatransfer')
    parser.add_argument('-xqr',   '--xnum-query-runs', help='number of times to repeat each query', default=1, dest='num_run')
    parser.add_argument('-xnls',  '--xnum-loading-split', help='number of parallel loader batches (total loaders ÷ this = batch size)', default="1", dest='num_loading_split')
    parser.add_argument('-xii',   '--xinit-indexes', help='create indexes after loading', action='store_true', default=False, dest='init_indexes')
    parser.add_argument('-xic',   '--xinit-constraints', help='add primary-key and foreign-key constraints after loading (star schema only)', action='store_true', default=False, dest='init_constraints')
    parser.add_argument('-xis',   '--xinit-statistics', help='run ANALYZE after loading', action='store_true', default=False, dest='init_statistics')
    parser.add_argument('-xrcp',  '--xrecreate-parameter', help='with -xqv random: draw new random query parameters for each stream', action='store_true', default=False, dest='recreate_parameter')
    parser.add_argument('-xshq',  '--xshuffle-queries', help='shuffle query execution order independently per stream', action='store_true', default=False, dest='shuffle_queries')
    parser.add_argument('-xaq',   '--xactive-queries', help='comma-separated 1-based query numbers to run, e.g. 1,4,7 for Q1.1, Q2.1, Q3.1 (all other queries are set inactive in the query config uploaded to the cluster; unset = run all 13 queries)', default='', dest='active_queries')
    parser.add_argument('-xdfe',  '--xduckdb-force-execution', help='run queries on PostgreSQL tables in pg_duckdb\'s DuckDB engine (PgDuckDB only); off by default, so they run in PostgreSQL\'s own executor', action='store_true', default=False, dest='duckdb_force_execution')
    parser.add_argument('-xve',   '--xverbose-explain', help='run and print configured EXPLAIN statements after each benchmark query (requires an \'explain\' key in the DBMS connection\'s JDBC config)', action='store_true', default=False, dest='verbose_explain')
    parser.add_argument('-xse',   '--xstore-explain', help='run configured EXPLAIN statements after the first run of each benchmark query and store the result in the protocol (requires an \'explain\' key in the DBMS connection\'s JDBC config)', action='store_true', default=False, dest='store_explain')
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    debugging = int(args.debug)
    if args.debug:
        logger_bexhoma = logging.getLogger('bexhoma')
        logger_bexhoma.setLevel(logging.DEBUG)
        logger_loader = logging.getLogger('load_data_asynch')
        logger_loader.setLevel(logging.DEBUG)
    if int(args.multi_tenant_num) > 0:
        parser.error('SSB does not support multi-tenancy (-mtn) yet')
    ##############
    ### set parameters
    ##############
    command_args = vars(args)
    ##############
    ### workflow parameters
    ##############
    # start with old experiment?
    code = args.experiment
    # only create testbed or also run a benchmark?
    mode = str(args.mode)
    # timeout of a benchmark
    timeout = int(args.timeout)
    # how often to repeat experiment?
    num_experiment_to_apply = int(args.num_config)
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
    ##############
    ### specific to: dbmsbenchmarker SSB
    ##############
    schema_variant = args.schema_variant
    # placement of the dimensions on multi-node DBMS
    dimensions = args.dimensions
    num_worker = int(args.num_worker)
    num_worker_replicas = int(args.num_worker_replicas)
    num_worker_shards = int(args.num_worker_shards)
    # shuffle ordering and random parameters
    recreate_parameter = args.recreate_parameter
    shuffle_queries = args.shuffle_queries
    # run and print configured EXPLAIN statements after each query
    verbose_explain = args.verbose_explain
    # run and store configured EXPLAIN statements in the protocol
    store_explain = args.store_explain
    # limit to one table
    limit_import_table = args.limit_import_table
    # restrict to a subset of queries by 1-based query number
    active_queries = [int(x) for x in args.active_queries.split(",") if len(x) > 0] or None
    ##############
    ### set cluster
    ##############
    aws = args.aws
    if aws:
        cluster = clusters.AWS(context=args.context)
    else:
        cluster = clusters.Kubernetes(context=args.context)
    # limit number of sut
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    # summary mode resumes an existing experiment: use its own persisted SF
    # instead of the -sf CLI default (see resolve_scaling_factor docstring)
    SF = resolve_scaling_factor(cluster, code, mode, args.scaling_factor)
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.ssb(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    if args.max_sut_experiment is not None:
        experiment.max_sut = int(args.max_sut_experiment)
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    experiment.set_active_queries(active_queries)
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_split = experiment.get_parameter_as_list('num_loading_split')
    # set node groups for components
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'auxiliary',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="ssb",
        experiment_design="parallel-loading"
    )
    experiment.set_default_loading_parameters(
        SF = SF,
        STORE_RAW_DATA = 1,
        STORE_RAW_DATA_RECREATE = 0,
        BEXHOMA_SYNCH_LOAD = 1,
        BEXHOMA_SYNCH_GENERATE = 1,
        SSB_SCHEMA_VARIANT = schema_variant,
        SSB_TABLE = limit_import_table,
    )
    experiment.set_default_benchmarking_parameters(
        SF = SF,
        DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
        DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
        DBMSBENCHMARKER_DEV = debugging,
        DBMSBENCHMARKER_VERBOSE_EXPLAIN = verbose_explain,
        DBMSBENCHMARKER_STORE_EXPLAIN = store_explain,
    )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_pods_split in num_loading_split: # should be a number of splits, e.g. 4 for 1/4th of all pods
        for loading_pods_total in num_loading_pods: # number of loading pods in total
            # split number of loading pods into parallel potions
            if loading_pods_total < loading_pods_split:
                # thats not possible
                continue
            # how many in parallel?
            split_portion = int(loading_pods_total/loading_pods_split)
            if ("PostgreSQL" in args.dbms or len(args.dbms) == 0):
                # PostgreSQL
                config = configurations.default(experiment=experiment, docker='PostgreSQL', dialect='PostgreSQL', alias='DBMS A2')
                # With -ar: VACUUM ANALYZE, CHECKPOINT and a stats reset before each round
                config.set_benchmark_resetscript(['reset-ssb.sql'])
                config.set_storage(
                    storageConfiguration = 'postgresql'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-ssb-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("PgDuckDB" in args.dbms):
                # PgDuckDB (pg_duckdb extension on PostgreSQL, reuses PostgreSQL's scripts and loading job)
                config = configurations.default(experiment=experiment, docker='PgDuckDB', dialect='PostgreSQL', alias='DBMS A4')
                config.path_experiment_docker = 'PostgreSQL'
                # With -ar: reset of PostgreSQL
                config.set_benchmark_resetscript(['reset-ssb.sql'])
                config.set_storage(
                    storageConfiguration = 'PgDuckDB'
                    )
                config.sut_parameters = {
                    # read by deploymenttemplate-PgDuckDB.yml's postStart hook to decide
                    # whether to ALTER ROLE ... SET duckdb.force_execution
                    'DUCKDB_FORCE_EXECUTION': str(args.duckdb_force_execution).lower(),
                }
                config.jobtemplate_loading = "jobtemplate-loading-ssb-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("CedarDB" in args.dbms):
                # CedarDB (PostgreSQL protocol, reuses PostgreSQL's loading job; own scripts)
                config = configurations.default(experiment=experiment, docker='CedarDB', dialect='PostgreSQL', alias='DBMS A7')
                # With -ar: ANALYZE before each round; no CHECKPOINT and no counters to reset
                config.set_benchmark_resetscript(['reset-ssb.sql'])
                config.set_storage(
                    storageConfiguration = 'cedardb'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-ssb-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MonetDB" in args.dbms or len(args.dbms) == 0):
                # MonetDB
                config = configurations.default(experiment=experiment, docker='MonetDB', dialect='MonetDB', alias='DBMS A1')
                # With -ar: ANALYZE of every table
                config.set_benchmark_resetscript(['reset-ssb.sql'])
                config.set_storage(
                    storageConfiguration = 'monetdb'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-ssb-MonetDB.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("ClickHouse" in args.dbms or len(args.dbms) == 0):
                # ClickHouse
                config = configurations.default(experiment=experiment, docker='ClickHouse', dialect='Clickhouse', alias='DBMS A3')
                # With -ar: sync of the loaded parts to disk before each round
                config.set_benchmark_resetscript(['reset-flush.sh'])
                config.set_storage(
                    storageConfiguration = 'clickhouse'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-ssb-ClickHouse.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MySQL" in args.dbms):
                # MySQL
                config = configurations.default(experiment=experiment, docker='MySQL', dialect='MySQL', alias='DBMS A5')
                # With -ar: ANALYZE TABLE, then flush of the dirty pages and FLUSH STATUS before each round
                config.set_benchmark_resetscript(['reset-ssb.sql' if schema_variant == 'normal' else 'reset-ssb-flat.sql', 'reset-flush.sh'])
                config.set_storage(
                    storageConfiguration = 'mysql'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-ssb-MySQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MariaDB" in args.dbms):
                # MariaDB
                config = configurations.default(experiment=experiment, docker='MariaDB', dialect='MySQL', alias='DBMS A6')
                # With -ar: ANALYZE TABLE, then flush of the dirty pages and FLUSH STATUS before each round
                config.set_benchmark_resetscript(['reset-ssb.sql' if schema_variant == 'normal' else 'reset-ssb-flat.sql', 'reset-flush.sh'])
                config.set_storage(
                    storageConfiguration = 'mariadb'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-ssb-MariaDB.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                # the container creates the database and grants it to the user bexhoma
                config.set_sut_parameters(
                    MARIADB_DATABASE = "ssb",
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("ClickHouseCluster" in args.dbms):
                # ClickHouse cluster: coordinator (SUT) and num_worker shards
                config = configurations.default(experiment=experiment, docker='ClickHouseCluster', dialect='Clickhouse', alias='DBMS C1', worker=num_worker)
                # -xdim distributed: scripts in ClickHouseCluster/distributed, and a volume of its own
                config.path_experiment_docker = resolve_dimension_folder('ClickHouseCluster', schema_variant, dimensions)
                if config.path_experiment_docker != 'ClickHouseCluster':
                    config.storage_label = f'ssb-distributed-{SF}'
                # With -ar: rows held by the Distributed tables are sent to the shards and the
                # replicated dimensions are synced (coordinator), then the loaded parts are
                # synced to disk (every worker)
                config.set_benchmark_resetscript(['reset-ssb.sql' if schema_variant == 'normal' else 'reset-ssb-flat.sql', 'reset-flush.sh'])
                config.set_script_target('workers')
                config.set_storage(
                    storageConfiguration = 'clickhousecluster'
                    )
                config.set_eval_parameters(
                    BEXHOMA_WORKERS = num_worker,
                    )
                # the loader writes to the coordinator's tables, which send the rows to the shards
                config.jobtemplate_loading = "jobtemplate-loading-ssb-ClickHouse.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("Citus" in args.dbms):
                # Citus: coordinator (SUT) and num_worker workers
                config = configurations.default(experiment=experiment, docker='Citus', dialect='PostgreSQL', alias='DBMS C2', worker=num_worker)
                # -xdim distributed: scripts in Citus/distributed, and a volume of its own
                config.path_experiment_docker = resolve_dimension_folder('Citus', schema_variant, dimensions)
                if config.path_experiment_docker != 'Citus':
                    config.storage_label = f'ssb-distributed-{SF}'
                # With -ar: VACUUM ANALYZE, then CHECKPOINT and a stats reset on the
                # coordinator and every worker before each round
                config.set_benchmark_resetscript(['reset-ssb.sql' if schema_variant == 'normal' else 'reset-ssb-flat.sql'])
                config.set_storage(
                    storageConfiguration = 'citus'
                    )
                config.set_sut_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    BEXHOMA_SHARDS = num_worker_shards,
                    )
                config.set_eval_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    BEXHOMA_SHARDS = num_worker_shards,
                    BEXHOMA_WORKERS = num_worker,
                    )
                # the loader writes to the coordinator, which sends the rows to the shards
                config.jobtemplate_loading = "jobtemplate-loading-ssb-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
    ##############
    ### branch for workflows
    ##############
    experiment.add_benchmark_list(list_clients)
    experiment.process()
exit()
